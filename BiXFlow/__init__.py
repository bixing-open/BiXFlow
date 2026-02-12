"""BiXFlow: A framework for executing workflows through Model Context Protocol servers.

This package provides a high-level interface for executing workflows defined in YAML format
through MCP servers.
"""

from .client import MCPClient
from .workflow import (
    BiXFlowExecutor, 
    run_workflow_from_file, 
    run_workflow_from_file_sync, 
    run_workflow_from_content, 
    run_workflow_from_content_sync
)
from .config import MCPConfig, get_config
from .exceptions import BiXFlowError, WorkflowNotFoundError, InvalidWorkflowError, MCPClientError, ConfigurationError

__version__ = "0.9.0"
__author__ = "BiXFlow Development Team"
