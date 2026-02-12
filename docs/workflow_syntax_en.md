# Workflow Syntax Guide

This guide explains the syntax and structure of workflows in BiXFlow. Workflows are defined in YAML format and describe a sequence of steps to be executed through MCP servers.

## Table of Contents

1. [Workflow Structure](#workflow-structure)
2. [Workflow Metadata](#workflow-metadata)
3. [Input Schema](#input-schema)
4. [Steps Definition](#steps-definition)
5. [Step Properties](#step-properties)
6. [Variable Substitution](#variable-substitution)
7. [Control Flow](#control-flow)
8. [Examples](#examples)

## Workflow Structure

A workflow is a YAML document with the following top-level structure:

```yaml
name: workflow_name
display_name: Display Name
description: A brief description of what the workflow does

inputSchema:
  # Input schema definition
  type: object
  properties:
    # Property definitions
  required:
    # Required properties

steps:
  # Array of step definitions
  - name: step_name
    tool: server_name/tool_name
    # Additional step properties
```

## Workflow Metadata

### name (Required)
Unique identifier for the workflow. Used internally to reference the workflow.

```yaml
name: api_health_monitor
```

### display_name (Optional)
Human-readable name for display purposes.

```yaml
display_name: API Health Monitor
```

### description (Optional)
Brief description of what the workflow does.

```yaml
description: Monitor API endpoints and generate health reports
```

## Input Schema

The `inputSchema` section defines the expected input parameters for the workflow, following JSON Schema specification.

### Basic Structure

```yaml
inputSchema:
  type: object
  properties:
    parameter_name:
      type: string|number|boolean|array|object
      description: "Description of the parameter"
      default: default_value
  required:
    - parameter_name
```

### Example

```yaml
inputSchema:
  type: object
  properties:
    api_endpoints:
      type: array
      description: "List of API endpoints to monitor"
      default: []
    timeout:
      type: number
      description: "Timeout in seconds"
      default: 30
  required:
    - api_endpoints
```

## Steps Definition

The `steps` section is an array of step definitions that will be executed in order. Each step represents a tool call to an MCP server.

### Basic Step Structure

```yaml
steps:
  - name: step_identifier
    tool: server_name/tool_name
    inputs:
      parameter_name: parameter_value
    outputs: output_variable_name
```

## Step Properties

### name (Required)
Unique identifier for the step within the workflow.

```yaml
name: check_api_status
```

### tool (Required)
Specifies the MCP tool to call in the format `server_name/tool_name`.

```yaml
tool: monitor_alert_mcp/api_checker
```

### inputs (Optional)
Input parameters to pass to the tool. Values can be literals or variables using Jinja2 syntax.

```yaml
inputs:
  endpoint: "{{ endpoint_url }}"
  timeout: 30
  headers:
    Authorization: "Bearer {{ api_token }}"
```

### outputs (Optional)
Variable name to store the result of the tool execution. This variable can be used in subsequent steps.

```yaml
outputs: api_status_result
```

### when (Optional)
Conditional expression that determines whether the step should be executed. Uses Jinja2 expression syntax.

```yaml
when: "{{ api_status_result.status == 'healthy' }}"
```

### on_fail (Optional)
Defines behavior when the step fails. Possible values:
- `break`: Stop workflow execution (default)
- `continue`: Continue to next step

```yaml
on_fail: continue
```

### foreach (Optional)
Execute the step for each item in a list. Creates a loop context for the step.

```yaml
foreach:
  endpoint: "{{ api_endpoints }}"
```

### loop (Optional)
Execute the step a specific number of times.

```yaml
loop: 5
```

### until (Optional)
Conditional expression that can terminate a loop early when the condition is met.

```yaml
until: "{{ result.success == true }}"
```

## Variable Substitution

BiXFlow uses Jinja2 templating for variable substitution in workflow definitions.

### Basic Variable Substitution

```yaml
inputs:
  endpoint: "{{ endpoint_url }}"
  timeout: "{{ config.timeout | default(30) }}"
```

### Variable Filters

Common Jinja2 filters supported:
- `default(value)`: Provide a default value if variable is undefined
- `length`: Get the length of a list or string
- `upper/lower`: Convert string case

```yaml
when: "{{ api_endpoints | length > 0 }}"
inputs:
  name: "{{ user_name | default('Anonymous') }}"
```

### Complex Expressions

```yaml
when: "{{ result.status == 'success' and result.count > 0 }}"
inputs:
  message: "Processed {{ result.count }} items successfully"
```

## Control Flow

### Conditional Execution

Use the `when` property to conditionally execute steps:

```yaml
- name: response_time_log
  tool: monitor_alert_mcp/response_logger
  inputs:
    endpoint: "{{ endpoint }}"
    sample_count: 3
  outputs: performance_data
  when: "{{ api_status.status == 'healthy' }}"
```

### Loops

#### Foreach Loop

Iterate over a list of items:

```yaml
- name: check_api_status
  tool: monitor_alert_mcp/api_checker
  inputs:
    endpoint: "{{ endpoint }}"
    timeout: 30
  foreach:
    endpoint: "{{ api_endpoints }}"
  outputs: api_status_results
```

#### Count Loop

Execute a step a specific number of times:

```yaml
- name: retry_operation
  tool: some_server/retryable_tool
  inputs:
    data: "{{ input_data }}"
  loop: 3
  outputs: result
  until: "{{ result.success }}"
```

### Error Handling

Control workflow behavior when steps fail:

```yaml
- name: critical_operation
  tool: important_server/critical_tool
  inputs:
    data: "{{ input_data }}"
  outputs: result
  on_fail: break  # Stop workflow on failure (default)

- name: optional_operation
  tool: optional_server/optional_tool
  inputs:
    data: "{{ input_data }}"
  outputs: result
  on_fail: continue  # Continue workflow even if step fails
```

## Examples

### Simple API Health Check Workflow

```yaml
name: api_health_check
display_name: API Health Check
description: Check the health status of API endpoints

inputSchema:
  type: object
  properties:
    api_endpoints:
      type: array
      description: "List of API endpoints to check"
      default: []
  required:
    - api_endpoints

steps:
  - name: check_endpoints
    tool: monitor_alert_mcp/api_checker
    inputs:
      endpoint: "{{ endpoint }}"
      timeout: 30
    foreach:
      endpoint: "{{ api_endpoints }}"
    outputs: health_results

  - name: generate_report
    tool: report_generator_mcp/health_reporter
    inputs:
      status_results: "{{ health_results }}"
    outputs: health_report
```

### Data Processing Workflow

```yaml
name: data_processing
display_name: Data Processing Pipeline
description: Process and analyze data using validation and cleaning

inputSchema:
  type: object
  properties:
    raw_data:
      type: array
      description: "Raw data to process"
      default: []
    validation_rules:
      type: object
      description: "Data validation rules"
      default: {}
  required:
    - raw_data

steps:
  - name: validate_data
    tool: data_processor_mcp/validator
    inputs:
      data: "{{ raw_data }}"
      rules: "{{ validation_rules }}"
    outputs: validation_result

  - name: clean_data
    tool: data_processor_mcp/cleaner
    inputs:
      raw_data: "{{ raw_data }}"
      issues: "{{ validation_result.issues }}"
    outputs: cleaned_data
    when: "{{ validation_result.valid and validation_result.issues | length > 0 }}"

  - name: analyze_data
    tool: data_processor_mcp/analyzer
    inputs:
      data: "{{ cleaned_data | default(raw_data) }}"
      metrics: ["count", "mean", "std", "min", "max"]
    outputs: analysis_result

  - name: generate_report
    tool: report_generator_mcp/generator
    inputs:
      basic_stats: "{{ analysis_result }}"
      anomalies: "{{ analysis_result }}"
      validation_result: "{{ validation_result }}"
    outputs: final_report
```

### Nested Workflow Execution

```yaml
name: comprehensive_analysis
display_name: Comprehensive Analysis
description: Execute comprehensive data analysis using nested workflows

inputSchema:
  type: object
  properties:
    raw_data:
      type: array
      description: "Raw data for analysis"
      default: []
    api_endpoints:
      type: array
      description: "API endpoints to monitor"
      default: []
  required:
    - raw_data

steps:
  - name: comprehensive_data_analysis
    tool: report_generator_mcp/comprehensive_analyzer
    inputs:
      raw_data: "{{ raw_data }}"
      validation_rules:
        required_fields: ["id", "value"]
        field_types:
          id: int
          value: int
      api_endpoints: "{{ api_endpoints }}"
    outputs: comprehensive_result

  - name: format_report
    tool: report_generator_mcp/formatter
    inputs:
      report_data: "{{ comprehensive_result }}"
      format: "markdown"
    outputs: formatted_report
    when: "{{ comprehensive_result.status == 'done' }}"
```

### Excel File Merging Workflow

```yaml
name: merge_excel_files
display_name: Excel File Merger
description: Traverse a directory and merge all Excel files into a single Excel file

inputSchema:
  type: object
  properties:
    input_directory:
      type: string
      description: "Directory containing Excel files to merge"
    output_file:
      type: string
      description: "Path to the output merged Excel file"
      default: "./merged_output.xlsx"
  required:
    - input_directory

steps:
  - name: list_excel_files
    tool: excel_processor_mcp/list_excel_files
    inputs:
      directory: "{{ input_directory }}"
    outputs: excel_files

  - name: check_files_found
    tool: data_processor_mcp/analyzer
    inputs:
      data: "{{ excel_files.files }}"
      metrics: ["count"]
    outputs: file_count_analysis
    when: "{{ excel_files.status == 'success' }}"

  - name: merge_files
    tool: excel_processor_mcp/merge_excel_files
    inputs:
      file_paths: "{{ excel_files.files }}"
      output_path: "{{ output_file }}"
      sheet_name: "MergedData"
    outputs: merge_result
    when: "{{ excel_files.status == 'success' and excel_files.count > 0 }}"

  - name: generate_report
    tool: report_generator_mcp/generator
    inputs:
      basic_stats: "{{ file_count_analysis }}"
      anomalies: {}
      validation_result: 
        valid: "{{ excel_files.count > 0 }}"
        valid_count: "{{ excel_files.count }}"
        total_count: "{{ excel_files.count }}"
    outputs: final_report
    when: "{{ excel_files.status == 'success' }}"
```

## Best Practices

1. **Descriptive Names**: Use clear, descriptive names for workflows and steps
2. **Consistent Naming**: Follow consistent naming conventions for variables and parameters
3. **Input Validation**: Define comprehensive input schemas with appropriate defaults
4. **Error Handling**: Use `on_fail` appropriately to control workflow behavior on errors
5. **Documentation**: Include descriptions for workflows and complex steps
6. **Modularity**: Break complex workflows into smaller, reusable components
7. **Conditional Logic**: Use `when` conditions to make workflows more flexible
8. **Loop Optimization**: Use `until` conditions to avoid unnecessary iterations
