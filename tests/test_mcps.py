"""Tests for MCP tools functionality."""

import pytest
from BiXFlow import MCPClient


class TestMCPServerTools:
    """Test MCP server tools functionality."""

    @pytest.mark.asyncio
    async def test_monitor_alert_mcp_tools(self):
        """Test monitor alert MCP tools listing and calling."""
        # Create actual MCP client instance, connecting to the started server
        client = MCPClient({
            "monitor_alert_mcp": {
                "url": "http://localhost:8002/mcp/",
                "transport": "streamable_http"
            }
        })
        
        # Test tool listing
        tools_result = await client.list_tools("monitor_alert_mcp")
        assert tools_result['status'] == 'done'
        assert len(tools_result['tools']) >= 3  # Should have at least 3 tools
        
        # Get tool names list
        tool_names = [tool.name for tool in tools_result['tools']]
        assert "api_checker" in tool_names
        assert "response_logger" in tool_names
        assert "alert_sender" in tool_names
        
        # Test tool calling
        # Test api_checker tool
        async for result in client.call_tool("monitor_alert_mcp", "api_checker", {"endpoint": "http://httpbin.org/get"}):
            assert result['status'] == 'done'
            assert 'status' in result['data']
            
        # Test response_logger tool
        async for result in client.call_tool("monitor_alert_mcp", "response_logger", {"endpoint": "http://httpbin.org/get", "sample_count": 3}):
            assert result['status'] == 'done'
            assert 'summary' in result['data']
            
        # Test alert_sender tool
        async for result in client.call_tool("monitor_alert_mcp", "alert_sender", {
            "report": {
                "system_status": {"healthy_endpoints": 3, "total_endpoints": 3},
                "identified_issues": [],
                "recommendations": []
            }, 
            "recipients": ["admin@example.com"],
            "severity": "info"
        }):
            assert result['status'] == 'done'
            assert 'delivery_status' in result['data']

    @pytest.mark.asyncio
    async def test_data_processor_mcp_tools(self):
        """Test data processor MCP tools listing and calling."""
        # Create actual MCP client instance, connecting to the started server
        client = MCPClient({
            "data_processor_mcp": {
                "url": "http://localhost:8001/mcp/",
                "transport": "streamable_http"
            }
        })
        
        # Test tool listing
        tools_result = await client.list_tools("data_processor_mcp")
        assert tools_result['status'] == 'done'
        assert len(tools_result['tools']) >= 3  # Should have at least 3 tools
        
        # Get tool names list
        tool_names = [tool.name for tool in tools_result['tools']]
        assert "validator" in tool_names
        assert "cleaner" in tool_names
        assert "analyzer" in tool_names
        
        # Test tool calling
        sample_data = [
            {"id": 1, "value": 10, "category": "A"},
            {"id": 2, "value": 20, "category": "B"},
            {"id": 3, "value": 15, "category": "A"}
        ]
        
        validation_rules = {
            "required_fields": ["id", "value"],
            "field_types": {"id": "int", "value": "int"}
        }
        
        # Test validator tool
        async for result in client.call_tool("data_processor_mcp", "validator", {
            "data": sample_data,
            "rules": validation_rules
        }):
            assert result['status'] == 'done'
            assert 'valid' in result['data']
            
        # Test cleaner tool
        async for result in client.call_tool("data_processor_mcp", "cleaner", {
            "raw_data": sample_data,
            "issues": []
        }):
            assert result['status'] == 'done'
            assert 'cleaned_count' in result['data']
            
        # Test analyzer tool
        async for result in client.call_tool("data_processor_mcp", "analyzer", {
            "data": sample_data,
            "metrics": ["mean", "median", "min", "max"]
        }):
            assert result['status'] == 'done'
            assert 'count' in result['data']

    @pytest.mark.asyncio
    async def test_report_generator_mcp_tools(self):
        """Test report generator MCP tools listing and calling."""
        # Create actual MCP client instance, connecting to the started server
        client = MCPClient({
            "report_generator_mcp": {
                "url": "http://localhost:8003/mcp/",
                "transport": "streamable_http"
            }
        })
        
        # Test tool listing
        tools_result = await client.list_tools("report_generator_mcp")
        assert tools_result['status'] == 'done'
        assert len(tools_result['tools']) >= 3  # Should have at least 3 tools
        
        # Get tool names list
        tool_names = [tool.name for tool in tools_result['tools']]
        assert "generator" in tool_names
        assert "health_reporter" in tool_names
        assert "formatter" in tool_names
        
        # Test tool calling
        # Test generator tool
        async for result in client.call_tool("report_generator_mcp", "generator", {
            "basic_stats": {"count": 10, "mean": 15.5},
            "anomalies": {"anomaly_count": 0, "anomalies": []},
            "validation_result": {"valid": True, "valid_count": 10, "total_count": 10}
        }):
            assert result['status'] == 'done'
            assert 'report_id' in result['data']
            
        # Test health_reporter tool
        async for result in client.call_tool("report_generator_mcp", "health_reporter", {
            "status_results": [
                {"status": "healthy", "endpoint": "service1"},
                {"status": "healthy", "endpoint": "service2"}
            ],
            "performance_data": {
                "summary": {
                    "avg_response_time": 150,
                    "success_rate": 99.5
                }
            }
        }):
            assert result['status'] == 'done'
            assert 'system_status' in result['data']
            
        # Test formatter tool
        async for result in client.call_tool("report_generator_mcp", "formatter", {
            "report_data": {
                "title": "Test Report",
                "content": "This is a test report"
            },
            "format": "markdown"
        }):
            assert result['status'] == 'done'
            assert 'format' in result['data']

if __name__ == "__main__":
    pytest.main([__file__])
