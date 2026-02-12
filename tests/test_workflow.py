"""Tests for the BiXFlow framework."""

import pytest
import json
from unittest.mock import patch, MagicMock

from BiXFlow import (
    BiXFlowExecutor, 
    MCPClient, 
    run_workflow_from_content_sync, 
    run_workflow_from_file_sync,
    BiXFlowError,
    WorkflowNotFoundError,
    ConfigurationError
)


def test_workflow_executor_initialization_with_file():
    """Test BiXFlowExecutor initialization with config file."""
    mock_config = {
        "test_service": {
            "url": "http://test-service:8000/mcp/",
            "transport": "streamable_http"
        }
    }
    with patch('pathlib.Path.exists', return_value=True):
        with patch('builtins.open', MagicMock()) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(mock_config)
            executor = BiXFlowExecutor("test_config.json")
            assert isinstance(executor, BiXFlowExecutor)
            assert hasattr(executor, 'client')


def test_workflow_executor_initialization_with_dict():
    """Test BiXFlowExecutor initialization with config dict."""
    config_dict = {
        "test_service": {
            "url": "http://test-service:8000/mcp/",
            "transport": "streamable_http"
        }
    }
    executor = BiXFlowExecutor(config_dict)
    assert isinstance(executor, BiXFlowExecutor)
    assert hasattr(executor, 'client')


def test_mcp_client_initialization_with_file():
    """Test MCPClient initialization with config file."""
    mock_config = {
        "test_service": {
            "url": "http://test-service:8000/mcp/",
            "transport": "streamable_http"
        }
    }
    with patch('pathlib.Path.exists', return_value=True):
        with patch('builtins.open', MagicMock()) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(mock_config)
            client = MCPClient("test_config.json")
            assert isinstance(client, MCPClient)


def test_mcp_client_initialization_with_dict():
    """Test MCPClient initialization with config dict."""
    config_dict = {
        "test_service": {
            "url": "http://test-service:8000/mcp/",
            "transport": "streamable_http"
        }
    }
    client = MCPClient(config_dict)
    assert isinstance(client, MCPClient)


def test_run_workflow_from_content_sync_import():
    """Test that run_workflow_from_content_sync can be imported."""
    # This is a basic test to ensure the function exists
    assert callable(run_workflow_from_content_sync)


def test_run_workflow_from_file_sync_import():
    """Test that run_workflow_from_file_sync can be imported."""
    # This is a basic test to ensure the function exists
    assert callable(run_workflow_from_file_sync)


def test_exceptions_import():
    """Test that exceptions can be imported."""
    # This is a basic test to ensure the exceptions exist
    assert issubclass(BiXFlowError, Exception)
    assert issubclass(WorkflowNotFoundError, BiXFlowError)
    assert issubclass(ConfigurationError, BiXFlowError)


# Async tests
@pytest.mark.asyncio
async def test_async_workflow_execution_with_content():
    """Test asynchronous workflow execution with content."""
    config_dict = {
        "test_service": {
            "url": "http://test-service:8000/mcp/",
            "transport": "streamable_http"
        }
    }
    executor = BiXFlowExecutor(config_dict)
    # We can't actually run a workflow without MCP servers
    # but we can test that the method exists and is callable
    assert hasattr(executor, 'run_workflow_from_content_sync')
    assert hasattr(executor, 'run_workflow_from_file_sync')


def test_run_workflow_from_content_function():
    """Test run_workflow_from_content function."""
    config_dict = {
        "test_service": {
            "url": "http://test-service:8000/mcp/",
            "transport": "streamable_http"
        }
    }
    
    # Test that the function can be called (we can't actually execute without servers)
    with patch('BiXFlow.workflow.BiXFlowExecutor.run_workflow_from_content_sync') as mock_run:
        mock_run.return_value = {"status": "done", "data": "test"}
        
        result = run_workflow_from_content_sync(
            workflow_content="name: test\nsteps: []",
            mcp_config=config_dict,
            args={}
        )
        assert result == {"status": "done", "data": "test"}


if __name__ == "__main__":
    pytest.main([__file__])
