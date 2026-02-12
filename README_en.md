# BiXFlow

[![PyPI version](https://badge.fury.io/py/BiXFlow.svg)](https://pypi.org/project/BiXFlow/)
[![Python version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

BiXFlow is an efficient and deterministic workflow built on MCP, developed by the BiXing Team at China Mobile Research Institute (CMRI). It provides a simple and easy-to-use interface for defining, managing, and executing complex workflows. Unlike traditional fixed workflow file approaches, BiXFlow allows users to directly provide YAML workflow content and MCP configuration content to execute workflows.

## Directory Structure

```
BiXFlow/
├── README.md
├── README_en.md
├── .gitignore
├── requirements.txt
├── setup.py
├── BiXFlow/                     # Main package directory
│   ├── __init__.py              # Package entry point, exposes core API
│   ├── client.py                # MCP client implementation
│   ├── workflow.py              # Workflow executor
│   ├── config.py                # Configuration management
│   ├── utils.py                 # Utility functions
│   ├── exceptions.py            # Custom exceptions
│   └── cli.py                   # Command-line interface
├── examples/                    # Usage examples
├── workflows/                   # Sample workflow definition files
├── mcps/                        # Sample MCP service configurations and implementations
│   ├── excel_processor_mcp/     # Excel processing service
│   └── ...                      # Other MCP services
├── tests/                       # Test code
└── docs/                        # Documentation
```

## Features

- **Flexible Workflow Execution**: Supports executing workflows directly from YAML content without predefined files
- **Dynamic Configuration**: Supports dynamically loading MCP server configurations from JSON content
- **Standardized Protocol**: Implements the Model Context Protocol to ensure interoperability with various MCP services
- **Simple API**: Provides an easy-to-use interface for executing YAML-defined workflows
- **Flexible Workflow Execution**: Supports both synchronous and asynchronous workflow execution
- **Nested Workflow Support**: Supports defining sub-workflows in MCP services and using them as tools
- **Standardized Directory Structure**: Follows Python package best practices
- **Comprehensive Error Handling**: Provides detailed error information and exception handling mechanisms

## Workflow Purpose and Role

BiXFlow provides an agent workflow mechanism designed specifically to address the instability of large models when processing complex tasks. By decomposing complex tasks into a series of controllable steps, workflows ensure the reliability and consistency of task execution. Most importantly, BiXFlow workflows are implemented entirely through assembling MCP tools, making them extremely flexible and convenient.

### Direct Agent Invocation

Workflows can be directly invoked and executed by agents, enabling agents to stably handle complex business processes. Agents only need to provide workflow definitions and necessary parameters, and BiXFlow will be responsible for executing the entire workflow and returning results.

### Solving Large Model Instability Issues

Large models often encounter the following problems when processing complex tasks:

- Inconsistent output, with different results from multiple executions of the same task
- Prone to hallucinations or topic deviation when processing long tasks
- Difficulty handling tasks requiring multi-step coordination

BiXFlow effectively solves these issues by decomposing complex tasks into clearly defined workflow steps:

- Each step has clearly defined input and output specifications
- Data transfer between steps is precise and controllable
- Supports conditional judgment and loop control, improving processing flexibility
- Errors can be precisely located to problematic steps for appropriate error handling

### Completely Based on MCP Tool Assembly

The greatest advantage of BiXFlow workflows is that they implement complex functionalities entirely through assembling existing MCP tools, rather than developing from scratch. This approach brings significant benefits:

- **High Flexibility**: Different MCP tools can be freely combined according to requirements to build customized workflows
- **Convenient Extensibility**: When new MCP tools become available, they can be easily integrated into existing workflows
- **Reduced Development Costs**: There's no need to implement functionalities from zero, directly leveraging existing mature tools
- **Better Maintainability**: Individual tools are relatively independent, making updates and maintenance easier

### Nested Workflow Support

Workflows can not only function as independent execution units but also be nested and invoked as part of MCP tools. This means:

- One workflow can call another workflow as one of its steps
- Supports building hierarchical, modular workflow systems
- Improves workflow reusability and maintainability
- Makes complex business process management much simpler

This nested invocation capability makes BiXFlow a powerful workflow orchestration platform capable of handling various complex business scenarios.

## Installation

BiXFlow supports multiple installation methods to meet the needs of different users.

### 1. Install from PyPI (Recommended for Regular Users)

For regular users who only need to use BiXFlow, you can install directly from PyPI:

```bash
# Install the latest version
pip install BiXFlow

# Install a specific version
pip install BiXFlow==0.9.0
```

### 2. Install from Source

For users who want to get the latest development version or do secondary development, you can install from source:

```bash
# Clone the repository
git clone <repository-url>
cd BiXFlow

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode (recommended)
pip install -e .
```

### 3. Install Pre-compiled Packages

For users who don't want to build from source, you can download pre-compiled wheel or tar.gz packages for installation:

```bash
# Install wheel package
pip install BiXFlow-0.9.0-py3-none-any.whl

# Install tar.gz package
pip install BiXFlow-0.9.0.tar.gz
```

After installation, you can import the `BiXFlow` package in your Python code or use the `BiXFlow` command-line tool.

## Building and Publishing Python Packages

If you are a project maintainer and want to build and publish Python packages to PyPI, please follow these steps:

### Using the Release Script (Recommended)

The project provides a convenient release script to help you automate the build and publish process:

```bash
# Run the release script
python scripts/release.py

# The script will guide you through the following steps:
# 1. Check prerequisites
# 2. Clean previous build artifacts
# 3. Build source distribution and wheel packages
# 4. Check package quality
# 5. Ask whether you want to publish to TestPyPI or PyPI
```

### Manual Build Distribution Packages

```bash
# Install build tools
pip install build twine

# Build source distribution and wheel packages
python -m build

# The built packages will be located in the dist/ directory, including:
# - BiXFlow-0.9.0-py3-none-any.whl (wheel package)
# - BiXFlow-0.9.0.tar.gz (source distribution package)
```

### Verify Built Packages

```bash
# Check package quality
python -m twine check dist/*

# Check should display: PASSED
```

### Publish to PyPI

```bash
# Upload to PyPI (requires PyPI account)
twine upload dist/*

# Upload to TestPyPI for testing
twine upload --repository testpypi dist/*
```

### Publish to Private Repository

```bash
# Upload to private repository
twine upload --repository-url https://your-private-pypi.com/simple/ dist/*
```

## Quick Start

For detailed information about defining workflows, please see the [Workflow Syntax Guide](docs/workflow_syntax_en.md). This guide covers all aspects of workflow definition, including metadata, input schemas, step properties, variable substitution, and control flow constructs.

### Basic Usage - Executing Workflows from Content

```python
from BiXFlow import run_workflow_from_content_sync
import json

# User-provided YAML workflow content
workflow_content = """
name: api_health_monitor
display_name: API Health Monitor
description: Monitor API endpoint health status and perform performance testing and alerts

inputSchema:
  type: object
  properties:
    api_endpoints:
      type: array
      description: "List of API endpoints to monitor"
      default: []
  required:
    - api_endpoints

steps:
  - name: check_api_status
    tool: monitor_alert_mcp/api_checker
    inputs:
      timeout: 30
      expected_status: 200
    foreach:
      endpoint: "{{ api_endpoints }}"
    outputs: api_status_results
"""

# User-provided MCP configuration content
mcp_config_content = {
  "monitor_alert_mcp": {
    "name": "monitor_alert_mcp",
    "timeout": 60,
    "url": "http://localhost:8002/mcp/",
    "transport": "streamable_http"
  }
}

# Execute the workflow
result = run_workflow_from_content_sync(
    workflow_content=workflow_content,
    mcp_config=mcp_config_content,
    args={"api_endpoints": ["https://httpbin.org/get"]}
)

print("Execution result:", result)
```

### Asynchronous Usage - Executing Workflows from Content

```python
import asyncio
from BiXFlow import run_workflow_from_content

async def main():
    # User-provided YAML workflow content
    workflow_content = """
name: api_health_monitor
# ... (workflow definition content)
"""

    # User-provided MCP configuration content
    mcp_config_content = {
      "monitor_alert_mcp": {
        "name": "monitor_alert_mcp",
        "timeout": 60,
        "url": "http://localhost:8002/mcp/",
        "transport": "streamable_http"
      }
    }
  
    # Execute the workflow asynchronously
    result = await run_workflow_from_content(
        workflow_content=workflow_content,
        mcp_config=mcp_config_content,
        args={"api_endpoints": ["https://httpbin.org/get"]}
    )
  
    print("Execution result:", result)

# Run the async function
asyncio.run(main())
```

### Using the BiXFlow.BiXFlowExecutor Class

```python
from BiXFlow import BiXFlowExecutor

# User-provided MCP configuration content
mcp_config_content = {
  "monitor_alert_mcp": {
    "name": "monitor_alert_mcp",
    "timeout": 60,
    "url": "http://localhost:8002/mcp/",
    "transport": "streamable_http"
  }
}

# Create a workflow executor
executor = BiXFlowExecutor(mcp_config_content)

# User-provided YAML workflow content
workflow_content = """
name: api_health_monitor
# ... (workflow definition content)
"""

# Execute the workflow
result = executor.run_workflow_from_content_sync(
    workflow_content=workflow_content,
    args={"api_endpoints": ["https://httpbin.org/get"]}
)

print("Execution result:", result)
```

## Command-Line Tool

BiXFlow also provides a command-line tool for executing workflows directly from the command line:

```bash
# Show version information
BiXFlow --version

# List available workflows
BiXFlow list-workflows

# List available workflows (detailed format)
BiXFlow list-workflows --format detailed

# Execute a workflow from a file (using default configuration file)
BiXFlow run workflows/api_health_monitor/api_health_monitor_workflow.yaml --args '{"api_endpoints": ["https://httpbin.org/get"]}'

# Execute a workflow from a file (specifying configuration file)
BiXFlow run workflows/api_health_monitor/api_health_monitor_workflow.yaml --args '{"api_endpoints": ["https://httpbin.org/get"]}' --config mcps/mcp_servers_setting.json

# Execute a workflow from content (using JSON string as configuration)
BiXFlow run-content "name: test\nsteps: []" --args '{"api_endpoints": ["https://httpbin.org/get"]}' --config '{"monitor_alert_mcp": {"url": "http://localhost:8002/mcp/", "transport": "streamable_http"}}'

# Execute a workflow from content (using configuration file path)
BiXFlow run-content "name: test\nsteps: []" --args '{"api_endpoints": ["https://httpbin.org/get"]}' --config mcps/mcp_servers_setting.json
```

## Nested Workflow Functionality

BiXFlow supports defining sub-workflows in MCP services and packaging them as tools. For example, the `report_generator_mcp` service contains a comprehensive analysis workflow that can handle the complete process of data validation, cleaning, analysis, and report generation.

### Starting MCP Servers

Before running nested workflow examples, you need to start the MCP servers first:

```bash
# Start all MCP servers
./mcps/start_servers.sh
```

### Running Nested Workflow Examples

```bash
# Run nested workflow example
python examples/nested_workflow_usage.py
```

This example demonstrates how to:

1. Execute the `data_cleaning_analysis` workflow that contains nested tool calls
2. Handle progress updates and final results during workflow execution

## Running Examples

The project provides multiple examples to demonstrate BiXFlow's functionality. Before running these examples, you need to start the MCP servers:

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

## Development Guide

1. Fork this project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Building and Testing Python Packages

As a project maintainer, you can build and test Python packages to ensure their quality:

```bash
# Install development dependencies (including build and publishing tools)
pip install -e ".[dev]"

# Build packages
python -m build

# Check package quality
twine check dist/*

# Test installation in a clean environment
pip install dist/BiXFlow-0.9.0-py3-none-any.whl

# Run tests
python -m pytest tests/
```

## Contributing

We welcome contributions of any form! Before contributing, please ensure:

1. Read and understand the project's code style
2. Add corresponding tests for new features
3. Ensure all existing tests pass
4. Update relevant documentation

### Development Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd BiXFlow

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# Or
venv\Scripts\activate  # Windows

# Install development dependencies
pip install -e ".[dev]"

# Run tests
python -m pytest tests/
```

### Code Style

This project follows PEP 8 code standards and uses the following tools for code formatting:

- Black: Code formatting
- Flake8: Code checking

### Testing

Before submitting code, please ensure all tests pass:

# Run all tests (basic tests)

python -m pytest tests/

# Run specific tests

python -m pytest tests/test_BiXFlow.py::test_workflow_executor_initialization_with_file

Note: To run tests involving MCP servers, you need to start the MCP servers first:

```bash
# Run MCP servers in one terminal:
./mcps/start_servers.sh

# Then run MCP server tool tests in another terminal:
python -m pytest tests/test_mcps.py -v
```

### Commit Message Convention

Please use meaningful commit messages following this format:

- `feat: ` New feature
- `fix: ` Bug fix
- `docs: ` Documentation update
- `style: ` Code formatting adjustment
- `refactor: ` Code refactoring
- `test: ` Test-related
- `chore: ` Build process or auxiliary tool changes

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for more details.

### Third-Party Licenses

BiXFlow incorporates various third-party libraries, each with their respective licenses. All third-party dependencies use permissive licenses that are compatible with the MIT License.

For a complete list of third-party dependencies and their licenses, please refer to:

- **[NOTICE](NOTICE)** - Attribution notice for all third-party dependencies
- **[third-party-licenses/README.md](third-party-licenses/README.md)** - Detailed license information and compatibility analysis
- **[licenses.json](licenses.json)** - Machine-readable license information

### License Summary

BiXFlow uses the following types of licenses for its dependencies:

- **MIT License** - Most dependencies (27 libraries)
- **BSD License (BSD-2-Clause)** - 6 libraries
- **BSD-3-Clause** - 9 libraries
- **Mozilla Public License 2.0 (MPL 2.0)** - 2 libraries
- **Apache-2.0** - 3 libraries
- **Apache-2.0 OR BSD-3-Clause** - 1 library
- **Apache-2.0 OR BSD-2-Clause** - 1 library
- **Multiple Permissive Licenses** (BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0) - 1 library (numpy)
- **Python Software Foundation License** - 1 library (pywin32)
- **PSF-2.0** - 1 library (typing_extensions)

All licenses are permissive and compatible with commercial use and distribution.

## Migration Guide

If you're upgrading from an older version, please check our [Migration Guide](docs/migration_guide.md) to learn how to migrate to the latest version.

## Contact

If you have any questions or suggestions, please contact us through the following channels:

- Submit an Issue
- Send email to [bixing_support@chinamobile.com](mailto:bixing_support@chinamobile.com)
