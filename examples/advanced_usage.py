"""Advanced usage examples for BiXFlow.

This example demonstrates advanced features of the BiXFlow framework,
including workflow content execution and custom configuration.
"""

import asyncio
import json
from BiXFlow import BiXFlowExecutor


async def configure_custom_client_with_content():
    """Example of configuring a custom MCP client with configuration content."""
    # Read the MCP configuration content
    try:
        with open("mcps/mcp_servers_setting.json", "r", encoding="utf-8") as f:
            mcp_config_content = json.load(f)
    except FileNotFoundError:
        print("MCP configuration file not found. Please ensure you're running this script from the project root directory.")
        return
    
    # Create a client with custom configuration content
    executor = BiXFlowExecutor(mcp_config_content)
    
    # Get server configurations
    print("Available servers:", list(executor.client._all_mcp_servers_settings.keys()))
    
    # Get available tools for a service
    try:
        tools = await executor.client.get_available_tools("monitor_alert_mcp")
        print("Available tools in monitor_alert_mcp:", tools)
    except Exception as e:
        print(f"Error getting tools: {e}")


async def handle_workflow_progress_with_content():
    """Example of handling workflow progress updates with content execution."""
    # Read the workflow YAML content
    try:
        with open("workflows/api_health_monitor/api_health_monitor_workflow.yaml", "r", encoding="utf-8") as f:
            workflow_content = f.read()
    except FileNotFoundError:
        print("Workflow file not found. Please ensure you're running this script from the project root directory.")
        return
    
    # Read the MCP configuration content
    try:
        with open("mcps/mcp_servers_setting.json", "r", encoding="utf-8") as f:
            mcp_config_content = json.load(f)
    except FileNotFoundError:
        print("MCP configuration file not found. Please ensure you're running this script from the project root directory.")
        return
    
    # Create executor with configuration content
    executor = BiXFlowExecutor(mcp_config_content)
    
    # Execute workflow from content and handle progress updates
    async for result in executor.execute_workflow_content(
        workflow_content=workflow_content,
        args={
            "api_endpoints": [
                "https://httpbin.org/get",
                "https://httpbin.org/status/200"
            ]
        }
    ):
        # Handle different types of results
        if result['status'] == 'progress':
            print(f"[PROGRESS] {result['data']}")
        elif result['status'] == 'step_done':
            print(f"[STEP DONE] {result['data']}")
        elif result['status'] == 'error':
            print(f"[ERROR] {result['data']}")
        elif result['status'] == 'done':
            print("[DONE] Workflow completed successfully")
            print(f"Final result: {json.dumps(result, ensure_ascii=False, indent=2)}")


def sync_with_error_handling_and_content():
    """Example of synchronous execution with error handling using content."""
    from BiXFlow import run_workflow_from_content_sync
    from BiXFlow.exceptions import BiXFlowError, WorkflowExecutionError, ConfigurationError
    
    # Read the workflow YAML content
    try:
        with open("workflows/api_health_monitor/api_health_monitor_workflow.yaml", "r", encoding="utf-8") as f:
            workflow_content = f.read()
    except FileNotFoundError:
        print("Workflow file not found. Please ensure you're running this script from the project root directory.")
        return
    
    # Read the MCP configuration content
    try:
        with open("mcps/mcp_servers_setting.json", "r", encoding="utf-8") as f:
            mcp_config_content = json.load(f)
    except FileNotFoundError:
        print("MCP configuration file not found. Please ensure you're running this script from the project root directory.")
        return
    
    try:
        result = run_workflow_from_content_sync(
            workflow_content=workflow_content,
            mcp_config=mcp_config_content,
            args={
                "api_endpoints": [
                    "https://httpbin.org/get"
                ]
            }
        )
        
        if result['status'] == 'done':
            print("Workflow completed successfully!")
            print(f"Result: {json.dumps(result['data'], ensure_ascii=False, indent=2)}")
        else:
            print(f"Workflow failed with status: {result['status']}")
            print(f"Error: {result.get('data', 'Unknown error')}")
            
    except WorkflowExecutionError as e:
        print(f"Workflow execution error: {e}")
    except ConfigurationError as e:
        print(f"Configuration error: {e}")
    except BiXFlowError as e:
        print(f"BiXFlow error: {e}")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")


async def main():
    """Run all examples."""
    print("=== Advanced BiXFlow Examples ===\n")
    
    print("1. Configuring custom client with content:")
    await configure_custom_client_with_content()
    
    print("\n2. Handling workflow progress with content:")
    await handle_workflow_progress_with_content()
    
    print("\n3. Synchronous execution with error handling and content:")
    # Run synchronous example in a separate thread to avoid event loop conflicts
    import threading
    sync_thread = threading.Thread(target=sync_with_error_handling_and_content)
    sync_thread.start()
    sync_thread.join()


if __name__ == "__main__":
    asyncio.run(main())
