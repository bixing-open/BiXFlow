# BiXFlow Documentation

[English Version](../README_en.md) | [中文版本](../README.md)

Welcome to the BiXFlow documentation. This documentation will help you understand how to use the BiXFlow framework to execute workflows through Model Context Protocol servers.

## Table of Contents

1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Core Concepts](#core-concepts)
6. [API Reference](#api-reference)
7. [Examples](#examples)
8. [Workflow Syntax](#workflow-syntax)
9. [Configuration](#configuration)
10. [CLI Usage](#cli-usage)
11. [Contributing](#contributing)
12. [License](#license)

## Introduction

BiXFlow is a framework for executing workflows through Model Context Protocol (MCP) servers. It provides a simple and intuitive API for defining, managing, and executing complex workflows defined in YAML format.

## Project Structure

```
BiXFlow/
├── BiXFlow/                     # Main package directory
│   ├── __init__.py              # Package entry point exposing core API
│   ├── client.py                # MCP client implementation
│   ├── workflow.py              # Workflow executor
│   ├── config.py                # Configuration management
│   ├── utils.py                 # Utility functions
│   ├── exceptions.py            # Custom exceptions
│   └── cli.py                   # Command-line interface
├── examples/                    # Usage examples
├── workflows/                   # Workflow definition files
├── mcps/                        # MCP service configurations and implementations
│   ├── excel_processor_mcp/     # Excel processing service
│   └── ...                      # Other MCP services
├── tests/                       # Test code
├── docs/                        # Documentation
├── scripts/                     # Utility scripts
├── requirements.txt             # Dependencies
├── setup.py                     # Package installation configuration
├── README.md                    # Project overview and usage instructions
├── LICENSE                      # License information
└── .gitignore                   # Git ignore rules
```

## Installation

To install BiXFlow, you can use pip:

```bash
# Clone the repository
git clone <repository-url>
cd BiXFlow

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode (recommended)
pip install -e .
```

After installation, you can import the `BiXFlow` package in your Python code or use the `BiXFlow` command-line tool.

## Quick Start

Here's a quick example of how to use BiXFlow:

```python
from BiXFlow import BiXFlowExecutor

# Create a workflow executor
executor = BiXFlowExecutor()

# Execute a named workflow
result = executor.run_named_workflow_sync(
    service_name="api_health_monitor",
    workflow_name="api_health_monitor_workflow",
    args={"api_endpoints": ["https://httpbin.org/get"]}
)

print("Result:", result)
```

## Core Concepts

### Workflow

A workflow is a sequence of steps defined in a YAML file. Each step represents a tool call to an MCP server.

### MCP Client

The MCP client is responsible for communicating with MCP servers to execute tools and retrieve resources.

### Workflow Executor

The workflow executor is the main interface for executing workflows. It handles the orchestration of workflow steps.

## API Reference

### BiXFlow.BiXFlowExecutor

The main class for executing workflows.

#### Methods

- `run_workflow_from_file(workflow_path, args)` - Asynchronously execute a workflow from a file (returns async generator)
- `run_named_workflow(service_name, workflow_name, args)` - Asynchronously execute a named workflow (returns async generator)
- `run_workflow_from_content(workflow_content, args)` - Asynchronously execute a workflow from content (returns async generator)
- `run_workflow_from_file_sync(workflow_path, args)` - Synchronously execute a workflow from a file
- `run_named_workflow_sync(service_name, workflow_name, args)` - Synchronously execute a named workflow
- `run_workflow_from_content_sync(workflow_content, args)` - Synchronously execute a workflow from content

### MCPClient

The MCP client for communicating with MCP servers.

#### Methods

- `execute_workflow(workflow_path, args)` - Execute a workflow from a file
- `execute_named_workflow(service_name, workflow_name, args)` - Execute a named workflow
- `execute_workflow_content(workflow_content, args)` - Execute a workflow from content
- `call_tool(service_name, tool_name, args)` - Call a specific tool on an MCP server
- `get_available_tools(service_name)` - Get available tools for an MCP server

## Examples

You can find more examples in the [examples](../examples/) directory:

- [Basic Usage](../examples/basic_usage.py) - Simple examples of using the API
- [Advanced Usage](../examples/advanced_usage.py) - Advanced features and techniques

To run these examples, you need to start the MCP servers first:

```bash
# Start all MCP servers in one terminal:
./mcps/start_servers.sh
```

Then run the examples in another terminal:

```bash
# Run basic usage example
python examples/basic_usage.py

# Run advanced usage example
python examples/advanced_usage.py

# Run nested workflow example (includes workflow nesting)
python examples/nested_workflow_usage.py
```

## Configuration

BiXFlow uses a JSON configuration file to define MCP server connections. By default, it looks for `mcps/mcp_servers_setting.json`.

Example configuration:

```json
{
  "data_processor_mcp": {
    "name": "data_processor_mcp",
    "timeout": 60,
    "url": "http://localhost:8001/mcp/",
    "transport": "streamable_http"
  }
}
```

## CLI Usage

BiXFlow provides a command-line interface for executing workflows:

```bash
# Show version information
BiXFlow --version

# List available workflows
BiXFlow list-workflows

# List available workflows (detailed format)
BiXFlow list-workflows --format detailed

# Run a named workflow
BiXFlow run-named api_health_monitor api_health_monitor_workflow --args '{"api_endpoints": ["https://httpbin.org/get"]}'

# Run a workflow from a file
BiXFlow run workflows/api_health_monitor/api_health_monitor_workflow.yaml --args '{"api_endpoints": ["https://httpbin.org/get"]}'
```

## Testing

Before submitting code, please make sure all tests pass:

```bash
# Run all tests (basic tests)
python -m pytest tests/

# Run specific tests
python -m pytest tests/test_BiXFlow.py::test_workflow_executor_initialization_with_file
```

Note: To run tests involving MCP servers, you need to start the MCP servers first:

```bash
# Start MCP servers in one terminal:
./mcps/start_servers.sh

# Then run MCP server tool tests in another terminal:
python -m pytest tests/test_mcps.py -v
```

## Workflow Syntax

For detailed information about defining workflows in YAML format, please see the [Workflow Syntax Guide](workflow_syntax_en.md). This guide covers all aspects of workflow definition, including metadata, input schemas, step properties, variable substitution, and control flow constructs.

## Contributing

We welcome contributions to BiXFlow! Please follow these steps to contribute:

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes and commit them
4. Push your changes to your fork
5. Submit a pull request

Please make sure to add tests for any new features or bug fixes, and follow the existing code style.

## License

BiXFlow is licensed under the MIT License. See the [LICENSE](../LICENSE) file for more information.
