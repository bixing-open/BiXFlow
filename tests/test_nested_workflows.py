"""
BiXFlow Framework - Nested Workflows Test Suite
================================================

This test suite validates the nested workflow functionality of the BiXFlow framework,
ensuring proper integration and orchestration of multiple MCP services through
both direct tool calls and YAML-based workflow executions.

Test Coverage:
1. Comprehensive analyzer tool availability and functionality
2. Nested tool call execution with multiple MCP service interactions
3. Workflow execution using predefined YAML workflow definitions
4. Error handling for disconnected or unavailable MCP services

"""

import pytest
import asyncio

from BiXFlow import (
    BiXFlowExecutor, 
    MCPClient
)


def test_comprehensive_analyzer_tool_exists() -> None:
    """
    Test that the comprehensive_analyzer tool is properly registered and available.
    
    This test verifies that the composite tool which orchestrates multiple MCP services
    is correctly exposed through the report_generator_mcp service interface.
    """
    # Configure MCP client for report generator service
    config_dict = {
        "report_generator_mcp": {
            "url": "http://localhost:8003/mcp/",
            "transport": "streamable_http"
        }
    }
    client = MCPClient(config_dict)
    
    # Verify tool listing functionality
    result = asyncio.run(client.list_tools("report_generator_mcp"))
    
    # Extract tool names from the result
    tool_names = [tool.name for tool in result['tools']]
    
    # Assert that our composite tool is available
    assert "comprehensive_analyzer" in tool_names, (
        "comprehensive_analyzer tool not found in report_generator_mcp tools. "
        f"Available tools: {tool_names}"
    )


# Async tests
@pytest.mark.asyncio
async def test_comprehensive_analyzer_execution() -> None:
    """
    Test comprehensive_analyzer tool execution with nested service calls.
    
    This test validates that the composite tool correctly orchestrates calls to:
    1. data_processor_mcp/validator for data validation
    2. data_processor_mcp/analyzer for statistical analysis
    3. monitor_alert_mcp/api_checker for API health monitoring
    4. report_generator_mcp/generator for report creation
    5. report_generator_mcp/formatter for report formatting
    
    The test verifies proper data flow and result structure across all nested calls.
    """
    # Configure MCP client with all required services
    config_dict = {
        "data_processor_mcp": {
            "url": "http://localhost:8001/mcp/",
            "transport": "streamable_http"
        },
        "monitor_alert_mcp": {
            "url": "http://localhost:8002/mcp/",
            "transport": "streamable_http"
        },
        "report_generator_mcp": {
            "url": "http://localhost:8003/mcp/",
            "transport": "streamable_http"
        }
    }
    client = MCPClient(config_dict)
    
    # Prepare test data for comprehensive analysis
    sample_data = [
        {"id": 1, "value": 10, "category": "A"},
        {"id": 2, "value": 20, "category": "B"},
        {"id": 3, "value": 15, "category": "A"}
    ]
    
    # Define data validation rules
    validation_rules = {
        "required_fields": ["id", "value"],
        "field_types": {"id": "int", "value": "int"}
    }
    
    # Specify API endpoints to monitor
    api_endpoints = ["https://httpbin.org/get"]
    
    # Execute comprehensive analyzer tool with nested service calls
    async for result in client.call_tool("report_generator_mcp", "comprehensive_analyzer", {
        "raw_data": sample_data,
        "validation_rules": validation_rules,
        "api_endpoints": api_endpoints
    }):
        if result['status'] == 'done':
            # Verify that we received a response
            assert result['data'] is not None, "Expected data in successful result"
            
            # Validate the nested data structure - data is wrapped in result['data']['data']
            analysis_data = result['data'].get('data', {})
            assert analysis_data, "Expected nested data structure in result"
            
            # Verify all expected components from nested service calls
            assert 'validation_result' in analysis_data, "Missing validation result from data_processor_mcp"
            assert 'analysis_result' in analysis_data, "Missing analysis result from data_processor_mcp"
            assert 'api_status_results' in analysis_data, "Missing API status results from monitor_alert_mcp"
            assert 'final_report' in analysis_data, "Missing final report from report_generator_mcp"
            assert 'formatted_report' in analysis_data, "Missing formatted report from report_generator_mcp"
            
            # Additional validation of key result structures
            validation_result = analysis_data['validation_result']
            assert 'valid' in validation_result, "Validation result missing 'valid' field"
            assert 'total_count' in validation_result, "Validation result missing 'total_count' field"
            
            analysis_result = analysis_data['analysis_result']
            assert 'count' in analysis_result, "Analysis result missing 'count' field"
            
            api_results = analysis_data['api_status_results']
            assert isinstance(api_results, list), "API status results should be a list"
            
            final_report = analysis_data['final_report']
            assert isinstance(final_report, dict), "Final report should be a dictionary"
            
            formatted_report = analysis_data['formatted_report']
            assert isinstance(formatted_report, dict), "Formatted report should be a dictionary"
            assert 'format' in formatted_report, "Formatted report missing 'format' field"
            assert 'content' in formatted_report, "Formatted report missing 'content' field"
            break
            
        elif result['status'] == 'error':
            # Handle expected connection errors when services are not running
            error_message = str(result['data'])
            assert ("Connection refused" in error_message or 
                    "连接被拒绝" in error_message or
                    "timed out" in error_message or
                    "超时" in error_message), (
                f"Unexpected error message: {error_message}. "
                "Expected connection refusal or timeout when services are not running."
            )
            break


@pytest.mark.asyncio
async def test_data_cleaning_workflow_execution() -> None:
    """
    Test data_cleaning_analysis workflow execution using YAML definition.
    
    This test validates that the predefined workflow correctly orchestrates:
    1. Data validation and cleaning through data_processor_mcp
    2. Statistical analysis of processed data
    3. API health monitoring via monitor_alert_mcp
    4. Comprehensive reporting through report_generator_mcp
    5. Proper result aggregation and return structure
    
    The test ensures YAML-based workflow definitions properly integrate
    with the nested tool call mechanism.
    """
    # Configure BiXFlow executor with all required services
    config_dict = {
        "data_processor_mcp": {
            "url": "http://localhost:8001/mcp/",
            "transport": "streamable_http"
        },
        "monitor_alert_mcp": {
            "url": "http://localhost:8002/mcp/",
            "transport": "streamable_http"
        },
        "report_generator_mcp": {
            "url": "http://localhost:8003/mcp/",
            "transport": "streamable_http"
        }
    }
    executor = BiXFlowExecutor(config_dict)
    
    # Prepare workflow arguments with test data
    workflow_args = {
        "raw_data": [
            {"id": 1, "value": 10, "category": "A"},
            {"id": 2, "value": 20, "category": "B"},
            {"id": 3, "value": 15, "category": "A"}
        ],
        "validation_rules": {
            "required_fields": ["id", "value"],
            "field_types": {"id": "int", "value": "int"}
        },
        "api_endpoints": ["https://httpbin.org/get"]
    }
    
    # Execute the data cleaning and analysis workflow
    async for result in executor.execute_workflow(
        "workflows/data_cleaning_analysis/data_workflow.yaml", 
        workflow_args
    ):
        if result['status'] == 'done':
            # Verify that we received a response
            assert result['data'] is not None, "Expected data in successful workflow result"
            
            # Validate the result structure from the YAML workflow
            assert 'comprehensive_result' in result['data'], (
                "Expected 'comprehensive_result' in workflow output. "
                f"Available keys: {list(result['data'].keys())}"
            )
            
            # Verify the nested result structure
            comprehensive_result = result['data']['comprehensive_result']
            assert isinstance(comprehensive_result, dict), "Comprehensive result should be a dictionary"
            assert 'status' in comprehensive_result, "Comprehensive result missing 'status' field"
            assert comprehensive_result['status'] == 'done', (
                f"Expected comprehensive result status 'done', got '{comprehensive_result['status']}'"
            )
            
            # Validate that the comprehensive result contains the expected nested data
            assert 'data' in comprehensive_result, "Comprehensive result missing 'data' field"
            nested_data = comprehensive_result['data']
            assert isinstance(nested_data, dict), "Nested data should be a dictionary"
            
            # Verify key components from the nested analysis
            expected_components = [
                'validation_result', 
                'analysis_result', 
                'api_status_results', 
                'final_report', 
                'formatted_report'
            ]
            
            for component in expected_components:
                assert component in nested_data, f"Missing '{component}' in comprehensive result data"
            
            # Additional validation of critical data structures
            validation_result = nested_data['validation_result']
            assert validation_result.get('valid') is True, "Data validation should pass with valid test data"
            assert validation_result.get('total_count') == 3, "Expected 3 records in validation result"
            
            analysis_result = nested_data['analysis_result']
            assert analysis_result.get('count') == 3, "Expected analysis of 3 records"
            
            api_results = nested_data['api_status_results']
            assert len(api_results) == 1, "Expected results for 1 API endpoint"
            assert api_results[0].get('status') in ['healthy', 'unhealthy'], (
                "API status should be either 'healthy' or 'unhealthy'"
            )
            break
            
        elif result['status'] == 'error':
            # Handle expected connection errors when services are not running
            error_message = str(result['data'])
            assert ("Connection refused" in error_message or 
                    "连接被拒绝" in error_message or
                    "timed out" in error_message or
                    "超时" in error_message), (
                f"Unexpected error message: {error_message}. "
                "Expected connection refusal or timeout when services are not running."
            )
            break


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
