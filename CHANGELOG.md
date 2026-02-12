# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.9.0] - 2025-01-30

### Added

- Initial stable release of BiXFlow
- Support for executing workflows from YAML content
- Support for executing workflows from YAML files
- Dynamic MCP server configuration loading
- Synchronous and asynchronous workflow execution
- Nested workflow support in MCP services
- Command-line interface (CLI) tool
- Comprehensive workflow syntax guide (Chinese and English)
- Example workflows and usage scripts
- Full documentation with internationalization support

### Features

- Flexible workflow execution from content without predefined files
- JSON Schema based input validation
- Jinja2 template engine for variable substitution
- Control flow structures: conditionals (when), loops (foreach, loop), error handling (on_fail)
- Variable filters and complex expressions
- Progress tracking and result streaming
- Comprehensive error handling and exception classes
- MCP client with streamable HTTP transport support

### Workflow Syntax

- Metadata fields: name, display_name, description
- Input schema definition with JSON Schema
- Step properties: name, tool, inputs, outputs, when, on_fail, foreach, loop, until
- Variable substitution using Jinja2 syntax
- Conditional execution with when expressions
- Loop constructs: foreach for list iteration, loop for count-based iteration
- Error handling with on_fail: break/continue options

### Documentation

- README.md (Chinese) with comprehensive installation and usage guide
- README_en.md (English) with comprehensive installation and usage guide
- docs/index.md - Documentation index
- docs/workflow_syntax.md - Workflow syntax guide (Chinese)
- docs/workflow_syntax_en.md - Workflow syntax guide (English)

### Examples

- Basic usage examples (sync and async)
- Advanced usage examples
- Nested workflow usage examples
- Excel merge demonstration
- CLI demonstration

### Testing

- Unit tests for core functionality
- Test coverage for workflow execution

### MCP Services Included

- data_processor_mcp - Data validation, cleaning, and analysis
- excel_processor_mcp - Excel file processing and merging
- monitor_alert_mcp - API monitoring and alerting
- report_generator_mcp - Report generation with nested workflows


---

## Version Classification

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security vulnerability fixes
