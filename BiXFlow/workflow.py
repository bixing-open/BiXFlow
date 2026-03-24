"""Workflow execution utilities for BiXFlow.

This module provides utilities for executing workflows through MCP servers,
including the BiXFlowProcessor and BiXFlowExecutor classes for simplified workflow management.
"""

import asyncio
import json
import yaml
import re
from typing import Dict, Any, Optional, Union, AsyncGenerator

from .client import MCPClient
from .config import MCPConfig
from .exceptions import WorkflowExecutionError


# Re-export utility functions from client module for backward compatibility
from .utils import (
    get_leaf_key_paths,
    get_logger,
    replace_vars_in_dict,
    deep_update,
    process_optional_params
)

class BiXFlowProcessor:
    """Workflow processor for executing MCP workflows (renamed from WorkflowProcessor).
    
    This class handles the parsing and execution of workflows defined in YAML format,
    including support for loops, conditional steps, and output registration.
    
    This class is a renamed version of WorkflowProcessor from client.py, moved here
    for better organization and separation of concerns.
    """
    
    def __init__(self, mcp_client: Any):
        """Initialize the workflow processor.
        
        Args:
            mcp_client: MCP client instance for executing tools
        """
        self.name = 'workflow'    # Default workflow name
        self.mcp = mcp_client
        self.context = {}
        
        self.required_params = []

        # Record multi-step output data for the workflow
        self.output_data: Dict = {}

    def _initialize_outputs_variable(self, loop_context: Dict, step_inputs: Dict, outputs_var: str, loop_index: int):
        """Initialize outputs variable for handling outputs variable references in inputs during first loop iteration.
        
        Args:
            loop_context: Loop context
            step_inputs: Step inputs
            outputs_var: Outputs variable name
            loop_index: Loop index
        """
        # Only process during first iteration
        if loop_index != 0:
            return
        
        # Convert step_inputs to string for searching
        inputs_str = str(step_inputs)
        
        # Check if outputs variable is referenced in inputs
        if outputs_var in inputs_str:
            # Check if outputs variable already exists in context
            if outputs_var not in loop_context:
                # Set outputs variable to empty dict on first iteration, not None
                loop_context[outputs_var] = {}

            # Handle nested outputs variables, e.g., loop_outputs.original
            # Use regex to find all {{outputs_var.xxx}} patterns
            # Match {{loop_outputs.xxx}} patterns
            pattern = r'\{\{\s*' + re.escape(outputs_var) + r'\.([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}'
            matches = re.findall(pattern, inputs_str)
            
            # Set None value for each matched nested variable in context
            for match in matches:
                nested_var_name = f"{outputs_var}.{match}"
                # Ensure flattened variable name is set in context (avoid duplicates)
                if nested_var_name not in loop_context:
                    loop_context[nested_var_name] = None

                # Ensure parent variable is dict structure for accessing nested properties
                if isinstance(loop_context[outputs_var], dict):
                    # Only set if key doesn't exist, avoid overriding existing values
                    if match not in loop_context[outputs_var]:
                        loop_context[outputs_var][match] = None
                else:
                    # If outputs_var is not dict, reinitialize as dict
                    loop_context[outputs_var] = {match: None}

    def _parse_workflow(self, content: str) -> Dict[str, Any]:
        """Parse workflow content (YAML format only)
        
        Returns:
            Dict[str, Any]: Workflow configuration containing 'steps' key
            
        Raises:
            ValueError: If no valid YAML configuration is found
        """
        logger = get_logger()
        logger.debug(f"Parsing workflow content: {repr(content)}")
        
        # Try parsing pure YAML content (without Markdown wrapper)
        try:
            workflow_config = yaml.safe_load(content)
            logger.debug(f"YAML parsing result: {workflow_config}")
            logger.debug(f"Type of workflow_config: {type(workflow_config)}")
            if workflow_config is not None:
                logger.debug(f"'steps' in workflow_config: {'steps' in workflow_config}")
                if 'steps' in workflow_config:
                    logger.debug(f"Type of workflow_config['steps']: {type(workflow_config['steps'])}")
            
            if isinstance(workflow_config, dict) and isinstance(workflow_config.get('steps'), list):
                logger.debug(f"Direct YAML parsing result: {workflow_config}")
                # Get name field from YAML data, use default if not present
                if 'name' in workflow_config:
                    self.name = workflow_config['name']
                else:
                    self.name = 'workflow'
                self.mcp.task_name = self.name
                return workflow_config
        except yaml.YAMLError as e:
            logger.debug(f"Direct YAML parsing failed: {str(e)}")
        
        # If direct YAML parsing fails, raise error since we no longer support Markdown
        raise ValueError("Invalid YAML configuration. Please ensure your workflow file is in valid YAML format.")

    async def _execute_single_step(
        self,
        step: Dict[str, Any],
        step_index: int,
        total_steps: int
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Execute a single workflow step
        
        Args:
            step: Workflow step definition (to be converted to Dict[str, Any])
        """
        step_name = step.get('name', f"Step {step_index + 1}")
        
        # Check when condition
        if 'when' in step:
            # First replace variables in when condition
            processed_step = replace_vars_in_dict({'when': step['when']}, self.context)
            if processed_step.get('result') == 'error':
                message = processed_step.get('message', '')
                yield {
                    'status': 'error',
                    'data': f"Error replacing variables in when condition for step {step_name}: {message}"
                }
                return
                
            try:
                if not processed_step['when']:
                    yield {
                        'status': 'skipped',
                        'data': f"Step {step['name']} skipped because condition not met. Current value: {processed_step['when']}"
                    }
                    return
            except Exception as e:
                yield {
                    'status': 'error',
                    'data': f"Error evaluating condition: {str(e)}"
                }
                return
        
        # Handle loop execution
        if 'loop' in step or 'foreach' in step:
            async for result in self._execute_loop_step(step, step_index):
                yield result
        else:
            # Execute regular step
            async for result in self._execute_regular_step(step, step_index):
                yield result

    async def _execute_regular_step(
        self,
        step: Dict[str, Any],
        step_index: int
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Execute regular step (non-loop step)
        
        Args:
            step: Workflow step definition
            step_index: Step index
        """
        step_name = step.get('name', f"Step {step_index + 1}")
        step = replace_vars_in_dict(step, self.context)
        if step.get('result') == 'error':
            message = step.get('message', '')
            missing_vars = step.get('missing_vars', [])
            context_hint = f" Available variables: {', '.join(get_leaf_key_paths(self.context))}" if missing_vars else ""
            yield {
                'status': 'error',
                'data': f"Error replacing variables in step {step_name}: {message}{context_hint}"
            }
            return
        
        # Parse tool format "server/tool"
        tool_parts = step['tool'].split('/')
        if len(tool_parts) != 2:
            yield {
                'status': 'error',
                'data': "Invalid tool format. Should be 'server/tool' format"
            }
            return
        
        server_name = tool_parts[0]
        tool_name = tool_parts[1]
        if 'inputs' in step:
            step_args = step.get('inputs', {})
        else:
            step_args = {}
        
        
        try:
            tool_iter = self.mcp.call_tool(server_name, tool_name, step_args)
            async for result in tool_iter:
                yield result
        except Exception as e:
            yield {
                'status': 'error',
                'data': f"Tool call failed: {str(e)}"
            }

    async def _execute_loop_step(
        self,
        step: Dict[str, Any],
        step_index: int
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Execute loop step
        
        Args:
            step: Workflow step definition
            step_index: Step index
        """
        step_name = step.get('name', f"Step {step_index + 1}")
        
        # Check that loop and foreach cannot be used together
        if 'loop' in step and 'foreach' in step:
            yield {
                'status': 'error',
                'data': f"Step {step_name} cannot use both loop and foreach"
            }
            return
        
        # Handle loop iteration
        if 'loop' in step:
            loop_count = step['loop']
            # Replace variables in loop_count
            processed_step = replace_vars_in_dict({'loop': loop_count}, self.context)
            if processed_step.get('result') == 'error':
                message = processed_step.get('message', '')
                yield {
                    'status': 'error',
                    'data': f"Error replacing variables in loop count for step {step_name}: {message}"
                }
                return
            loop_count = processed_step['loop']
            
            try:
                loop_count = int(loop_count)
            except (ValueError, TypeError):
                yield {
                    'status': 'error',
                    'data': f"Step {step_name} loop count must be an integer"
                }
                return
                
            for i in range(loop_count):
                # Update loop context
                loop_context = self.context.copy()
                loop_context['loop_index'] = i
                
                # Initialize outputs variable during first loop iteration
                if 'outputs' in step:
                    outputs_var = step['outputs']
                    # Check if outputs variable is referenced in inputs
                    step_inputs = step.get('inputs', {})
                    self._initialize_outputs_variable(loop_context, step_inputs, outputs_var, i)
                
                # Replace variables in step
                processed_step = replace_vars_in_dict(step, loop_context)
                if processed_step.get('result') == 'error':
                    message = processed_step.get('message', '')
                    yield {
                        'status': 'error',
                        'data': f"Error replacing variables in step {step_name} iteration {i+1}: {message}"
                    }
                    return
                
                # Check until condition
                if 'until' in processed_step:
                    try:
                        if processed_step['until'] == 'False':
                            yield {
                                'status': 'progress',
                                'data': f"Step {step_name} iteration {i+1} meets until condition, terminating loop early"
                            }
                            break
                    except Exception as e:
                        yield {
                            'status': 'error',
                            'data': f"Error evaluating until condition in step {step_name} iteration {i+1}: {str(e)}"
                        }
                        return
                
                # Execute step
                async for step_result in self._execute_regular_step(processed_step, step_index):
                    # Handle step result
                    result = await self._handle_step_result(processed_step, step_result, loop_context)
                    yield result
                    
        # Handle foreach iteration
        elif 'foreach' in step:
            # Parse foreach configuration
            foreach_config = step['foreach']
            
            if not isinstance(foreach_config, dict):
                yield {
                    'status': 'error',
                    'data': f"Step {step_name} foreach must be dict format: {{variable_name: list}}"
                }
                return
                
            if len(foreach_config) != 1:
                yield {
                    'status': 'error',
                    'data': f"Step {step_name} foreach must contain exactly one key-value pair: {{variable_name: list}}"
                }
                return
                
            # Get variable name and list
            item_var, list_name = list(foreach_config.items())[0]
            
            # Replace variables to get list
            processed_config = replace_vars_in_dict({'list': list_name}, self.context)
            if processed_config.get('result') == 'error':
                message = processed_config.get('message', '')
                yield {
                    'status': 'error',
                    'data': f"Error replacing variables in foreach list for step {step_name}: {message}"
                }
                return
            
            foreach_list = processed_config['list']
            
            if not isinstance(foreach_list, list):
                yield {
                    'status': 'error',
                    'data': f"Step {step_name} foreach value must be a list, current type: {type(foreach_list)}"
                }
                return
            
            # Initialize result list (for foreach output)
            outputs_list = []
            
            for i, item in enumerate(foreach_list):
                # Update loop context
                loop_context = self.context.copy()
                # Store variable name and value in context
                loop_context[item_var] = item
                loop_context['loop_index'] = i
                
                # Copy step and prepare for execution
                step_copy = step.copy()
                # Ensure inputs field exists
                if 'inputs' not in step_copy:
                    step_copy['inputs'] = {}
                
                # Add iterated item to inputs
                step_copy['inputs'][item_var] = item
                
                # Replace variables in step
                processed_step = replace_vars_in_dict(step_copy, loop_context)
                if processed_step.get('result') == 'error':
                    message = processed_step.get('message', '')
                    yield {
                        'status': 'error',
                        'data': f"Error replacing variables in step {step_name} iteration {i+1}: {message}"
                    }
                    return
                
                # Check until condition
                if 'until' in processed_step:
                    try:
                        if processed_step['until'] == 'False':
                            yield {
                                'status': 'progress',
                                'data': f"Step {step_name} iteration {i+1} meets until condition, terminating loop early"
                            }
                            break
                    except Exception as e:
                        yield {
                            'status': 'error',
                            'data': f"Error evaluating until condition in step {step_name} iteration {i+1}: {str(e)}"
                        }
                        return
                
                # Execute step
                async for step_result in self._execute_regular_step(processed_step, step_index):
                    # Handle step result
                    result = await self._handle_step_result(processed_step, step_result, loop_context)
                    
                    # Check if this is a foreach step result
                    if result.get('status') == 'step_done' and 'foreach_result' in result:
                        # Save to result list
                        if isinstance(result['foreach_result'], dict) and 'result' in result['foreach_result']:
                            display_result = result['foreach_result']['result']
                            if isinstance(display_result, list):
                                outputs_list.extend(display_result)
                            else:
                                outputs_list.append(display_result)
                        else:
                            outputs_list.append(result['foreach_result'])
                    
                    yield result
            
            # After loop completes, save result list to context
            if 'outputs' in step and outputs_list:
                outputs_key = step['outputs']
                
                # Extract actual computation results from tool results
                actual_results = []
                for item in outputs_list:
                    if isinstance(item, dict) and 'result' in item:
                        # Assume tool returns format: {"result": 8, "status": "success"}
                        actual_results.append(item['result'])
                    elif isinstance(item, (int, float, str)):
                        # If it's a direct value
                        actual_results.append(item)
                    else:
                        # Other cases, keep as is
                        actual_results.append(item)
                
                # Save result list to global context
                deep_update(self.context, {outputs_key: actual_results})
                
                # Add to output data
                deep_update(self.output_data, {outputs_key: actual_results})
                
                yield {
                    'status': 'progress',
                    'data': f"Step {step_name} foreach loop completed, saved result list to variable {outputs_key}\n"
                }

    async def _handle_step_result(
        self, 
        step: Dict[str, Any], 
        tool_result: Dict[str, Any],
        loop_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle step execution result"""
        try:
            result_data = tool_result.get('data', {})
        except Exception as e:
            logger = get_logger()
            logger.error(f"Error handling step result: {str(e)}")
            return {
                'status': 'error',
                'data': {'error': f"Error handling step result: {str(e)}"}
            }
            
        # Check failure conditions
        is_failed = (
            not result_data or
            tool_result.get('isError', False) or 
            tool_result.get('status') == 'error' or
            (isinstance(result_data, dict) and result_data.get('success') is False)
        )

        # Handle failure cases
        if is_failed:
            error_reason = ""
            if isinstance(result_data, dict):
                error_reason = result_data.get('message', str(result_data))
            else:
                error_reason = str(result_data)
                
            if 'on_fail' in step and step['on_fail'] == 'break':
                return {
                    'status': 'error',
                    'data': f"Step {step.get('name', 'Unknown')} failed - workflow terminated",
                    'error_reason': error_reason
                }
            elif 'on_fail' in step and step['on_fail'] == 'continue':
                return {
                    'status': 'warning', 
                    'data': f"Step {step.get('name', 'Unknown')} failed - workflow continues"
                }
            else:
                return {
                    'status': 'error', 
                    'data': f"Step {step.get('name', 'Unknown')} failed - workflow terminated (specify on_fail to continue). Failure details: {tool_result}"
                }

        # Handle completion case
        if isinstance(tool_result, dict) and tool_result.get('status') == 'done':
            result = {
                'status': 'step_done',
                'data': f"Step {step.get('name', 'Unnamed')} completed\n"
            }

            if isinstance(result_data, str):
                try:
                    result_data = json.loads(result_data)
                except Exception:
                    pass

            # Register output in context
            outputs_key = step.get('outputs')
                
            # Handle outputs variable replacement in loops
            if outputs_key and loop_context:
                # Replace outputs variable in loop context
                processed_outputs = replace_vars_in_dict({'outputs': outputs_key}, loop_context)
                if processed_outputs.get('result') != 'error':
                    outputs_key = processed_outputs['outputs']
            
            # For foreach loops, we don't save to global context here, let _execute_loop_step handle it
            if 'foreach' in step and outputs_key:
                # For foreach loops, we only return result, don't save to global context
                result['foreach_result'] = result_data
                result['foreach_outputs_key'] = outputs_key
                result['data'] = f"Step {step.get('name', 'Unnamed')} iteration {loop_context.get('loop_index', 0) + 1} completed"
                logger = get_logger()
                logger.info(f"\n===Current self.context:{self.context}")
                
                # But to ensure subsequent steps in loop can use it, we need to update loop_context
                loop_context[outputs_key] = result_data
                return result
            
            # Normal processing logic for non-foreach steps
            if outputs_key:
                deep_update(self.context, {outputs_key: result_data})
                result['data'] += f"Saved output of step {step.get('name', 'Unnamed')} to variable {outputs_key}\n"
                logger = get_logger()
                logger.info(f"\n===Current self.context:{self.context}")
                # Add to output data
                deep_update(self.output_data, {outputs_key: result_data})
            else:
                if not isinstance(result_data, dict):
                    result_data = {step.get('name', 'Unnamed'): result_data}
                deep_update(self.context, result_data)
                # Add to output data (always, since there's no key to check)
                deep_update(self.output_data, result_data)

            return result
        
        return tool_result

    def pre_process_steps(self, steps: list) -> list:
        """Process steps - for inheritance classes to customize step processing
        
        Args:
            steps: Step list
            
        Returns:
            Processed step list
        """
        return steps

    async def execute_workflow(
        self, 
        content: str, 
        args: Optional[Dict[str, Any]] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Execute workflow
        
        Args:
            content: Workflow content in YAML format
            args: Arguments to pass to the workflow
            
        Yields:
            Dict[str, Any]: Progress and result updates during workflow execution
        """
        try:
            workflow_config = self._parse_workflow(content)
        except ValueError as e:
            yield {
                'status': 'error',
                'data': f"Failed to parse workflow: {str(e)}"
            }
            return
        except Exception as e:
            yield {
                'status': 'error',
                'data': f"Unexpected error while parsing workflow: {str(e)}"
            }
            return
        
        start_info = f'Starting workflow task {self.name}'
        
        # Reset context and output data for new workflow execution
        self.context = {}
        self.output_data = {}
        
        # Process input schema and required parameters
        if 'inputSchema' in workflow_config and 'required' in workflow_config['inputSchema']:
            self.required_params = workflow_config['inputSchema']['required']
        else:
            self.required_params = []

        # Process optional parameters, set default values for keys defined in inputSchema properties 
        # but not in args and not in required_params
        if 'inputSchema' in workflow_config:
            args = process_optional_params(args, self.required_params, workflow_config['inputSchema'])
            
        # Validate required parameters
        missing_params = []
        for param in self.required_params:
            if not args or param not in args:
                missing_params.append(param)
                
        if missing_params:
            yield {
                'status': 'error',
                'data': f"Missing required parameters: {', '.join(missing_params)}"
            }
            return
            
        if args:
            deep_update(self.context, args)
            
        yield {
            'status': 'progress', 
            'data': f"{start_info}\n"
        }

        # Get and process steps
        steps = workflow_config.get('steps', [])
        if not steps:
            yield {
                'status': 'error',
                'data': "No steps defined in workflow"
            }
            return
            
        steps = self.pre_process_steps(steps)

        total_steps = len(steps)
        for idx, step in enumerate(steps):
            # Validate step has required fields
            if 'tool' not in step:
                yield {
                    'status': 'error',
                    'data': f"Step {idx + 1} is missing required 'tool' field"
                }
                return
                
            step_name = step.get('name', f"Step {idx + 1}")
            yield {
                'status': 'progress', 
                'data': f"Starting execution of step {step_name}"
            }
            
            try:
                async for step_result in self._execute_single_step(step, idx, total_steps):
                    # For loop steps, results are already handled in _execute_loop_step
                    # For regular steps, we need to handle results here
                    if 'loop' not in step and 'foreach' not in step:
                        result = await self._handle_step_result(step, step_result)
                        yield result

                        # Record step error info for later processing
                        if result.get('status') not in ('progress', 'step_done'):
                            deep_update(self.output_data, {step_name: result.get('data', result)})

                        if result.get('status') == 'error' and (('on_fail' not in step) or ('on_fail' in step and step.get('on_fail') == 'break')):
                            return
                    else:
                        # Loop step results are already yielded and handled in _execute_loop_step
                        yield step_result
                        # Check if it's an error and workflow needs to be terminated
                        if step_result.get('status') == 'error' and (('on_fail' not in step) or ('on_fail' in step and step.get('on_fail') == 'break')):
                            return
                    
            except Exception as e:
                yield {
                    'status': 'error',
                    'data': f"Step {step_name} failed: {str(e)}"
                }
                if (('on_fail' not in step) or ('on_fail' in step and step.get('on_fail') == 'break')):
                    return
        
        yield {
            'status': 'done',
            'message': f'Task {self.name} execution completed',
            'data': self.output_data
        }


# Maintain backward compatibility: WorkflowProcessor is now an alias for BiXFlowProcessor
WorkflowProcessor = BiXFlowProcessor


class BiXFlowExecutor:
    """Workflow executor for simplified workflow management.
    
    This class provides a high-level interface for executing workflows
    defined in YAML content through MCP servers.
    """
    
    def __init__(self, mcp_config: Optional[Union[str, Dict[str, Any]]] = None):
        """Initialize the workflow executor.
        
        Args:
            mcp_config: MCP servers configuration. Can be:
                       - A path to a JSON configuration file (str)
                       - A dictionary containing the configuration
                       - None to use default configuration discovery
        """
        if isinstance(mcp_config, str):
            # Load configuration from file
            self.config = MCPConfig(mcp_config)
            self.client = MCPClient(mcp_config)
        elif isinstance(mcp_config, dict):
            # Use provided configuration dictionary directly
            self.config = None  # No config manager needed
            self.client = MCPClient(mcp_config)
        else:
            # Use default configuration discovery
            self.config = MCPConfig()
            self.client = MCPClient()
        
    async def execute_workflow_content(self, workflow_content: str, args: Optional[Dict[str, Any]] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """Asynchronously execute a workflow from YAML content.
        
        Args:
            workflow_content: YAML content defining the workflow
            args: Arguments to pass to the workflow
            
        Yields:
            Dict[str, Any]: Progress and result updates during workflow execution
            
        Raises:
            WorkflowExecutionError: If workflow execution fails
        """
        try:
            async for result in self.client.execute_workflow_content(workflow_content, args):
                yield result
        except Exception as e:
            raise WorkflowExecutionError(f"Failed to execute workflow: {str(e)}")
            
    async def execute_workflow(self, workflow_path: str, args: Optional[Dict[str, Any]] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """Asynchronously execute a workflow from a YAML file.
        
        Args:
            workflow_path: Path to the workflow YAML file
            args: Arguments to pass to the workflow
            
        Yields:
            Dict[str, Any]: Progress and result updates during workflow execution
            
        Raises:
            WorkflowExecutionError: If workflow execution fails
        """
        try:
            async for result in self.client.execute_workflow(workflow_path, args):
                yield result
        except Exception as e:
            raise WorkflowExecutionError(f"Failed to execute workflow: {str(e)}")
            
    async def run_named_workflow(self, service_name: str, workflow_name: str, args: Optional[Dict[str, Any]] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """Asynchronously execute a named workflow from the standard workflows directory.
        
        Args:
            service_name: Name of the service directory under workflows/
            workflow_name: Name of the workflow (without .yaml extension)
            args: Arguments to pass to the workflow
            
        Yields:
            Dict[str, Any]: Progress and result updates during workflow execution
            
        Raises:
            WorkflowExecutionError: If workflow execution fails
        """
        try:
            async for result in self.client.execute_named_workflow(service_name, workflow_name, args):
                yield result
        except Exception as e:
            raise WorkflowExecutionError(f"Failed to execute workflow: {str(e)}")
            
    def run_workflow_from_content_sync(self, workflow_content: str, args: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Synchronously execute a workflow from YAML content.
        
        Args:
            workflow_content: YAML content defining the workflow
            args: Arguments to pass to the workflow
            
        Returns:
            Dict[str, Any]: Final result of workflow execution
            
        Raises:
            WorkflowExecutionError: If workflow execution fails
        """
        try:
            # Run the async generator in a new event loop
            async def _run():
                final_result = None
                async for result in self.client.execute_workflow_content(workflow_content, args):
                    # Just consume the stream, we'll return the final result
                    final_result = result
                return final_result or {}
            
            return asyncio.run(_run())
        except Exception as e:
            raise WorkflowExecutionError(f"Failed to execute workflow: {str(e)}")
            
    def run_workflow_from_file_sync(self, workflow_path: str, args: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Synchronously execute a workflow from a YAML file.
        
        Args:
            workflow_path: Path to the workflow YAML file
            args: Arguments to pass to the workflow
            
        Returns:
            Dict[str, Any]: Final result of workflow execution
            
        Raises:
            WorkflowExecutionError: If workflow execution fails
        """
        try:
            # Run the async generator in a new event loop
            async def _run():
                final_result = None
                async for result in self.client.execute_workflow(workflow_path, args):
                    # Just consume the stream, we'll return the final result
                    final_result = result
                return final_result or {}
            
            return asyncio.run(_run())
        except Exception as e:
            raise WorkflowExecutionError(f"Failed to execute workflow: {str(e)}")
            
    def run_named_workflow_sync(self, service_name: str, workflow_name: str, args: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Synchronously execute a named workflow from the standard workflows directory.
        
        Args:
            service_name: Name of the service directory under workflows/
            workflow_name: Name of the workflow (without .yaml extension)
            args: Arguments to pass to the workflow
            
        Returns:
            Dict[str, Any]: Final result of workflow execution
            
        Raises:
            WorkflowExecutionError: If workflow execution fails
        """
        try:
            # Run the async generator in a new event loop
            async def _run():
                final_result = None
                async for result in self.client.execute_named_workflow(service_name, workflow_name, args):
                    # Just consume the stream, we'll return the final result
                    final_result = result
                return final_result or {}
            
            return asyncio.run(_run())
        except Exception as e:
            raise WorkflowExecutionError(f"Failed to execute workflow: {str(e)}")


# Convenience functions for direct import and use
async def run_workflow_from_content(
    workflow_content: str, 
    mcp_config: Union[str, Dict[str, Any]],
    args: Optional[Dict[str, Any]] = None
) -> AsyncGenerator[Dict[str, Any], None]:
    """Execute a workflow from content.
    
    Args:
        workflow_content: YAML content defining the workflow
        mcp_config: MCP servers configuration. Can be:
                   - A path to a JSON configuration file (str)
                   - A dictionary containing the configuration
        args: Arguments to pass to the workflow
        
    Yields:
        Dict[str, Any]: Progress and result updates during workflow execution
    """
    executor = BiXFlowExecutor(mcp_config)
    async for result in executor.execute_workflow_content(workflow_content, args):
        yield result


async def run_workflow_from_file(
    workflow_path: str, 
    mcp_config: Union[str, Dict[str, Any]],
    args: Optional[Dict[str, Any]] = None
) -> AsyncGenerator[Dict[str, Any], None]:
    """Execute a workflow from a file.
    
    Args:
        workflow_path: Path to the workflow YAML file
        mcp_config: MCP servers configuration. Can be:
                   - A path to a JSON configuration file (str)
                   - A dictionary containing the configuration
        args: Arguments to pass to the workflow
        
    Yields:
        Dict[str, Any]: Progress and result updates during workflow execution
    """
    executor = BiXFlowExecutor(mcp_config)
    async for result in executor.execute_workflow(workflow_path, args):
        yield result


def run_workflow_from_content_sync(
    workflow_content: str, 
    mcp_config: Union[str, Dict[str, Any]],
    args: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Synchronously execute a workflow from content and return the final result.
    
    Args:
        workflow_content: YAML content defining the workflow
        mcp_config: MCP servers configuration. Can be:
                   - A path to a JSON configuration file (str)
                   - A dictionary containing the configuration
        args: Arguments to pass to the workflow
        
    Returns:
        Dict[str, Any]: Final result of the workflow execution
    """
    executor = BiXFlowExecutor(mcp_config)
    return executor.run_workflow_from_content_sync(workflow_content, args)


def run_workflow_from_file_sync(
    workflow_path: str, 
    mcp_config: Union[str, Dict[str, Any]],
    args: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Synchronously execute a workflow from a file and return the final result.
    
    Args:
        workflow_path: Path to the workflow YAML file
        mcp_config: MCP servers configuration. Can be:
                   - A path to a JSON configuration file (str)
                   - A dictionary containing the configuration
        args: Arguments to pass to the workflow
        
    Returns:
        Dict[str, Any]: Final result of the workflow execution
    """
    executor = BiXFlowExecutor(mcp_config)
    return executor.run_workflow_from_file_sync(workflow_path, args)
