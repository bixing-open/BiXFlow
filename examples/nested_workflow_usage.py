"""Test nested workflow execution for BiXFlow.

This example demonstrates how to execute nested workflows using the BiXFlow framework,
specifically using the data_cleaning_analysis workflow which contains nested tool calls.
"""

import asyncio
import json
from BiXFlow import BiXFlowExecutor


async def test_nested_workflow_execution():
    """Test nested workflow execution with progress handling."""
    print("=== Testing Nested Workflow Execution ===\n")
    
    # Read the MCP configuration content
    try:
        with open("mcps/mcp_servers_setting.json", "r", encoding="utf-8") as f:
            mcp_config_content = json.load(f)
    except FileNotFoundError:
        print("MCP configuration file not found. Please ensure you're running this script from the project root directory.")
        return
    
    # Read the workflow YAML content
    try:
        with open("workflows/data_cleaning_analysis/data_workflow.yaml", "r", encoding="utf-8") as f:
            workflow_content = f.read()
    except FileNotFoundError:
        print("Workflow file not found. Please ensure you're running this script from the project root directory.")
        return
    
    # Create executor with configuration content
    executor = BiXFlowExecutor(mcp_config_content)
    
    # Prepare workflow arguments
    workflow_args = {
        "raw_data": [
            {"id": 1, "value": 10, "category": "A"},
            {"id": 2, "value": 20, "category": "B"},
            {"id": 3, "value": 15, "category": "A"},
            {"id": 4, "value": 30, "category": "C"},
            {"id": 5, "value": 25, "category": "B"}
        ],
        "validation_rules": {
            "required_fields": ["id", "value"],
            "field_types": {"id": "int", "value": "int"}
        },
        "api_endpoints": [
            "https://httpbin.org/get",
            "https://httpbin.org/status/200"
        ]
    }
    
    print("Executing nested workflow: data_cleaning_analysis")
    print("This workflow demonstrates:")
    print("- Calling comprehensive_analyzer tool (nested calls to multiple MCP services)")
    print("- Formatting the result with report formatter")
    print("-" * 50)
    
    # Execute workflow from content and handle progress updates
    async for result in executor.execute_workflow_content(
        workflow_content=workflow_content,
        args=workflow_args
    ):
        # Handle different types of results
        if result['status'] == 'progress':
            print(f"[PROGRESS] {result['data']}")
        elif result['status'] == 'step_done':
            print(f"[STEP DONE] {result['data']}")
        elif result['status'] == 'error':
            print(f"[ERROR] {result['data']}")
            break
        elif result['status'] == 'done':
            print("[DONE] Nested workflow completed successfully")
            try:
                print(f"Final result: {json.dumps(result['data'], ensure_ascii=False, indent=2)}")
            except UnicodeEncodeError:
                # Fallback for systems that can't handle Unicode characters
                print(f"Final result: {json.dumps(result['data'], ensure_ascii=True, indent=2)}")
            break


async def main():
    """Main function to run all tests."""
    print("BiXFlow Nested Workflow Test")
    print("=" * 50)
    
    # Test asynchronous execution
    print("\n1. Testing asynchronous nested workflow execution:")
    await test_nested_workflow_execution()
    
    print("\n" + "=" * 50)
    print("Nested workflow testing completed!")


if __name__ == "__main__":
    asyncio.run(main())
