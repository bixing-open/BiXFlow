"""MCP Client for interacting with MCP servers.

This module provides a high-level interface for interacting with MCP servers,
allowing users to easily execute workflows and manage connections to various services.
"""

import json
import ssl
from typing import AsyncGenerator, Dict, Any, Optional, Union
from contextlib import asynccontextmanager
from pathlib import Path

import httpx
import asyncio
import logging
from mcp import ClientSession
from mcp.client.sse import sse_client
from mcp.client.streamable_http import streamablehttp_client
from .utils import get_logger

# Global logger instance
_LOGGER: Union[logging.Logger, None] = None

class MCPClient:
    """High-level MCP Client for workflow execution.
    
    This client provides a simplified interface for executing workflows defined
    in YAML files or content through MCP servers.
    """
    
    def __init__(self, config: Optional[Union[str, Dict[str, Any]]] = None):
        """Initialize the MCP client.
        
        Args:
            config: MCP servers configuration. Can be:
                   - A path to a JSON configuration file (str)
                   - A dictionary containing the configuration
                   - None to use default configuration discovery
        """
        self.logger = get_logger()
        
        # Handle different config types
        if config is None:
            # Default to standard location
            default_path = Path("mcps") / "mcp_servers_setting.json"
            if default_path.exists():
                config_path = str(default_path)
            else:
                raise FileNotFoundError(
                    "MCP configuration file not found. Please provide a config "
                    "or ensure 'mcps/mcp_servers_setting.json' exists."
                )
            # Load configuration from file
            with open(config_path, 'r', encoding='utf-8') as f:
                mcp_config = json.load(f)
        elif isinstance(config, str):
            # Load configuration from file path
            with open(config, 'r', encoding='utf-8') as f:
                mcp_config = json.load(f)
        elif isinstance(config, dict):
            # Use provided configuration dictionary directly
            mcp_config = config
        else:
            raise ValueError("Invalid config type. Must be str, dict, or None.")
            
        # Store configuration directly
        self._all_mcp_servers_settings = mcp_config
        self.task_name: str = ""

    async def _get_server_url(self, service_name: str) -> str:
        """Get the server URL for a given service name.
        
        Args:
            service_name: Name of the service to get URL for
            
        Returns:
            str: Server URL
            
        Raises:
            ValueError: If service name is not found in configuration
        """
        if service_name in self._all_mcp_servers_settings:
            url = self._all_mcp_servers_settings[service_name]['url']
            return url
        
        raise ValueError(
            f"MCP configuration not found for service '{service_name}'. "
            f"Please check if the service name is correct and available."
        )


    @asynccontextmanager
    async def _create_session(self, service_name: str) -> AsyncGenerator[Any, None]:
        """Create a session based on transport type.
        
        Args:
            service_name: Name of the service to create session for
            
        Yields:
            ClientSession: MCP client session
            
        Raises:
            ValueError: If transport type is not supported
        """
        server_url = await self._get_server_url(service_name)
        transport_type = self._all_mcp_servers_settings[service_name].get('transport', 'streamable_http')
        
        # Configure HTTPX client parameters
        client_params = {
            "timeout": httpx.Timeout(
                connect=10.0,  # Connection timeout 10 seconds
                read=60.0,     # Read timeout 60 seconds
                write=10.0,    # Write timeout 10 seconds
                pool=5.0       # Pool timeout 5 seconds
            )
        }
        
        try:
            if transport_type == "sse":
                async with sse_client(
                    url=server_url,
                    timeout=60,  # Increase total timeout
                    httpx_client_factory=lambda **kwargs: httpx.AsyncClient(
                        **{**client_params, **kwargs}
                    ),
                ) as (read_stream, write_stream):
                    async with ClientSession(read_stream, write_stream) as session:
                        yield session
                        
            elif transport_type == "streamable_http":
                async with streamablehttp_client(
                    url=server_url,
                    timeout=60,  # Increase total timeout
                    httpx_client_factory=lambda **kwargs: httpx.AsyncClient(
                        **{**client_params, **kwargs}
                    ),
                    auth=None
                ) as (read_stream, write_stream, get_session_id):
                    async with ClientSession(read_stream, write_stream) as session:
                        if get_session_id and (session_id := get_session_id()):
                            self.logger.debug(f"Session ID: {session_id}")
                        yield session
            else:
                raise ValueError(f"Unsupported transport type: {transport_type}")
                
        except (ssl.SSLError, httpx.ConnectError) as e:
            self.logger.error(f"SSL/Connection error for {service_name}: {e}")
            raise
        except asyncio.TimeoutError:
            self.logger.error(f"Connection timeout for {service_name}")
            raise

    async def list_tools(self, service_name: str) -> Dict[str, Any]:
        """List all available tools for a specified MCP service.
        
        Args:
            service_name: Name of the MCP service to query
            
        Returns:
            Dict[str, Any]: Dictionary containing status and tool data
            
        Example:
            >>> client = MCPClient()
            >>> result = await client.list_tools("web_browser_example")
            >>> if result['status'] == 'done':
            ...     print(result['data'])
            ['get_page_content_example', 'get_page_links_example']
        """
        try:
            async with self._create_session(service_name) as session:
                await session.initialize()
                result = await session.list_tools()
                if hasattr(result, 'isError') and getattr(result, 'isError'):
                    return {
                        'status': 'error',
                        'data': f"Failed to get tools list from {service_name}: {result}"
                    }
                    
                return {
                    'status': 'done',
                    'mcp_name': service_name,
                    'tools': result.tools
                }
        except Exception as e:
            return {
                'status': 'error',
                'data': f"Unknown error while getting tools list from {service_name}: {str(e)}"
            }

    async def call_tool(
        self,
        service_name: str, 
        tool_name: str, 
        args: Dict[str, Any]
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Call a specific tool on an MCP service.
        
        Args:
            service_name: Name of the MCP service
            tool_name: Name of the tool to call
            args: Arguments to pass to the tool
            
        Yields:
            Dict[str, Any]: Status updates and results during tool execution
            
        Example:
            >>> client = MCPClient()
            >>> async for result in client.call_tool(
            ...     "web_browser_example",
            ...     "get_page_content_example",
            ...     {"url": "https://example.com"}
            ... ):
            ...     print(result)
            {'status': 'progress', 'data': {'percentage': 30}}
            {'status': 'done', 'data': '<html>...</html>'}
        """
        self.logger.info(f"Calling {service_name} {tool_name} tool with args: {args}")
        if not self.task_name:
            self.task_name = f"{service_name}_{tool_name}"

        # Create progress message queue
        progress_queue = asyncio.Queue()
        final_result: Optional[Any] = None
        error_info: Optional[str] = None
        
        async def progress_callback(progress: int, total: int, message: str) -> Dict[str, Any]:
            """Progress callback function."""
            # Put progress message in queue
            await progress_queue.put({
                'status': 'progress',
                'data': message,
                'percentage': progress / total * 100 if total > 0 else 0
            })
            return {'status': 'progress', 'data': message}

        async def tool_executor() -> None:
            """Execute the tool asynchronously."""
            nonlocal final_result, error_info
            try:
                async with self._create_session(service_name) as session:
                    await session.initialize()                        
                    result = await session.call_tool(tool_name, args, progress_callback=progress_callback)
                    self.logger.debug(f"Tool result: {result}")
                    
                    if hasattr(result, 'isError') and getattr(result, 'isError'):
                        error_info = f"Tool error: {result}"
                        return
                    
                    content_list = getattr(result, 'content', [])
                    if not content_list or not hasattr(content_list[0], 'text'):
                        error_info = f"Invalid response format: {result}"
                        return
                    
                    text_result = []
                    for content in content_list:
                        try:
                            text_data = json.loads(content.text)
                            text_result.append(text_data)
                        except json.JSONDecodeError:
                            text_result.append(content.text)
                    
                    final_result = text_result[0] if len(text_result) == 1 else text_result
                    
            except Exception as e:
                error_info = f"Error calling tool {tool_name}: {str(e)}"
            finally:
                # Send termination signal
                await progress_queue.put(None)

        # Create tool execution task
        tool_task = asyncio.create_task(tool_executor())
        
        try:
            # Process all progress messages first
            while not tool_task.done() or not progress_queue.empty():
                item = await progress_queue.get()
                if item is None:  # Termination signal
                    break
                yield item
            
            # Process final result or error
            if error_info:
                yield {'status': 'error', 'data': error_info}
            elif final_result is not None:
                # Check if it's a workflow response
                if isinstance(final_result, dict) and final_result.get('status') == 'workflow':
                    context = final_result.get('context', {})
                    from .workflow import BiXFlowProcessor
                    processor = BiXFlowProcessor(self)
                    async for item in processor.execute_workflow(final_result.get('data', ''), context):
                        yield item
                else:
                    yield {'status': 'done', 'data': final_result}
        
        except asyncio.CancelledError:
            # Cancel tool task if generator is cancelled
            tool_task.cancel()
            raise
            
        finally:
            # Ensure task cleanup
            if not tool_task.done():
                tool_task.cancel()
            else:
                # Capture unhandled exceptions in task
                try:
                    await tool_task
                except Exception:
                    pass

    async def execute_workflow(
        self, 
        workflow_path: str, 
        args: Optional[Dict[str, Any]] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Execute a workflow from a YAML file.
        
        Args:
            workflow_path: Path to the workflow YAML file
            args: Arguments to pass to the workflow
            
        Yields:
            Dict[str, Any]: Progress updates and results during workflow execution
        """
        # Read workflow file
        with open(workflow_path, 'r', encoding='utf-8') as f:
            workflow_content = f.read()
            
        # Create processor and execute
        from .workflow import BiXFlowProcessor
        processor = BiXFlowProcessor(self)
        async for result in processor.execute_workflow(workflow_content, args or {}):
            yield result
            
    async def execute_named_workflow(
        self,
        service_name: str,
        workflow_name: str,
        args: Optional[Dict[str, Any]] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Execute a named workflow from the standard workflows directory.
        
        Args:
            service_name: Name of the service directory under workflows/
            workflow_name: Name of the workflow (without .yaml extension)
            args: Arguments to pass to the workflow
            
        Yields:
            Dict[str, Any]: Progress updates and results during workflow execution
        """
        # Construct standard path
        workflow_path = Path("workflows") / service_name / f"{workflow_name}.yaml"
        
        # Execute workflow
        async for result in self.execute_workflow(str(workflow_path), args):
            yield result
            
    async def execute_workflow_content(
        self, 
        workflow_content: str, 
        args: Optional[Dict[str, Any]] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Execute a workflow from YAML content.
        
        Args:
            workflow_content: YAML content defining the workflow
            args: Arguments to pass to the workflow
            
        Yields:
            Dict[str, Any]: Progress updates and results during workflow execution
        """
        # Create processor and execute
        from .workflow import BiXFlowProcessor
        processor = BiXFlowProcessor(self)
        async for result in processor.execute_workflow(workflow_content, args or {}):
            yield result
            
    async def get_available_tools(self, service_name: str) -> Dict[str, Any]:
        """Get all available tools for a specified MCP service.
        
        Args:
            service_name: Name of the MCP service to query
            
        Returns:
            Dict[str, Any]: Dictionary containing status and tool data
        """
        return await self.list_tools(service_name)
