"""Custom exceptions for the BiXFlow framework.

This module defines custom exception classes used throughout the BiXFlow framework.
"""

class BiXFlowError(Exception):
    """Base exception class for BiXFlow errors."""
    pass


class WorkflowNotFoundError(BiXFlowError):
    """Raised when a requested workflow is not found."""
    def __init__(self, workflow_path: str):
        self.workflow_path = workflow_path
        super().__init__(f"Workflow not found: {workflow_path}")


class InvalidWorkflowError(BiXFlowError):
    """Raised when a workflow definition is invalid."""
    def __init__(self, message: str):
        super().__init__(f"Invalid workflow: {message}")


class WorkflowExecutionError(BiXFlowError):
    """Raised when there is an error during workflow execution."""
    def __init__(self, message: str):
        super().__init__(f"Workflow execution error: {message}")


class MCPClientError(BiXFlowError):
    """Raised when there is an error with the MCP client."""
    def __init__(self, message: str):
        super().__init__(f"MCP client error: {message}")


class ConfigurationError(BiXFlowError):
    """Raised when there is a configuration error."""
    def __init__(self, message: str):
        super().__init__(f"Configuration error: {message}")
