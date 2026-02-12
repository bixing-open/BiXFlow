"""Basic usage examples for BiXFlow.

This example demonstrates how to use the BiXFlow framework to execute workflows
using YAML content and MCP configuration content provided by the user.
"""

import asyncio
import json


async def async_example_with_content():
    """Example of asynchronous workflow execution using YAML content."""
    # Import the function for executing workflow from content
    from BiXFlow import run_workflow_from_content
    import asyncio
    
    # Read the workflow YAML content (in real usage, this would come from user input)
    with open("workflows/api_health_monitor/api_health_monitor_workflow.yaml", "r", encoding="utf-8") as f:
        workflow_content = f.read()
    
    # Read the MCP configuration content (in real usage, this would come from user input)
    with open("mcps/mcp_servers_setting.json", "r", encoding="utf-8") as f:
        mcp_config_content = json.load(f)
    
    # Execute the workflow using the content
    try:
        async def run_workflow():
            final_result = None
            async for result in run_workflow_from_content(
                workflow_content=workflow_content,
                mcp_config=mcp_config_content,
                args={
                    "api_endpoints": [
                        "https://httpbin.org/get",
                        "https://httpbin.org/status/200"
                    ]
                }
            ):
                final_result = result
            return final_result
            
        final_result = await run_workflow()
        print("Workflow execution result:", json.dumps(final_result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error executing workflow: {e}")


def sync_example_with_content():
    """Example of synchronous workflow execution using YAML content."""
    # Import the synchronous function for executing workflow from content
    from BiXFlow import run_workflow_from_content_sync
    
    # Read the workflow YAML content (in real usage, this would come from user input)
    with open("workflows/api_health_monitor/api_health_monitor_workflow.yaml", "r", encoding="utf-8") as f:
        workflow_content = f.read()
    
    # Read the MCP configuration content (in real usage, this would come from user input)
    with open("mcps/mcp_servers_setting.json", "r", encoding="utf-8") as f:
        mcp_config_content = json.load(f)
    
    # Execute the workflow using the content
    try:
        result = run_workflow_from_content_sync(
            workflow_content=workflow_content,
            mcp_config=mcp_config_content,
            args={
                "api_endpoints": [
                    "https://httpbin.org/get",
                    "https://httpbin.org/status/200"
                ]
            }
        )
        print("Workflow execution result:", json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error executing workflow: {e}")


async def async_example_with_file():
    """Example of asynchronous workflow execution using file paths (legacy support)."""
    # Import the function for executing workflow from file
    from BiXFlow import run_workflow_from_file
    import asyncio
    
    # Read the MCP configuration content (in real usage, this would come from user input)
    with open("mcps/mcp_servers_setting.json", "r", encoding="utf-8") as f:
        mcp_config_content = json.load(f)
    
    # Execute the workflow using file paths
    try:
        async def run_workflow():
            final_result = None
            async for result in run_workflow_from_file(
                workflow_path="workflows/api_health_monitor/api_health_monitor_workflow.yaml",
                mcp_config=mcp_config_content,
                args={
                    "api_endpoints": [
                        "https://httpbin.org/get",
                        "https://httpbin.org/status/200"
                    ]
                }
            ):
                final_result = result
            return final_result
            
        final_result = await run_workflow()
        print("Workflow execution result:", json.dumps(final_result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error executing workflow: {e}")


def sync_example_with_file():
    """Example of synchronous workflow execution using file paths (legacy support)."""
    # Import the synchronous function for executing workflow from file
    from BiXFlow import run_workflow_from_file_sync
    
    # Read the MCP configuration content (in real usage, this would come from user input)
    with open("mcps/mcp_servers_setting.json", "r", encoding="utf-8") as f:
        mcp_config_content = json.load(f)
    
    # Execute the workflow using file paths
    try:
        result = run_workflow_from_file_sync(
            workflow_path="workflows/api_health_monitor/api_health_monitor_workflow.yaml",
            mcp_config=mcp_config_content,
            args={
                "api_endpoints": [
                    "https://httpbin.org/get",
                    "https://httpbin.org/status/200"
                ]
            }
        )
        print("Workflow execution result:", json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error executing workflow: {e}")


if __name__ == "__main__":
    print("=== Basic BiXFlow Examples ===\n")
    
    # Run the synchronous example with content
    print("1. Running synchronous example with content...")
    sync_example_with_content()
    
    # Run the asynchronous example with content
    print("\n2. Running asynchronous example with content...")
    asyncio.run(async_example_with_content())
    
    # Run the synchronous example with file (legacy support)
    print("\n3. Running synchronous example with file (legacy)...")
    sync_example_with_file()
    
    # Run the asynchronous example with file (legacy support)
    print("\n4. Running asynchronous example with file (legacy)...")
    asyncio.run(async_example_with_file())
