# 工作流语法指南

本指南解释了BiXFlow中工作流的语法和结构。工作流以YAML格式定义，描述了一系列通过MCP服务器执行的步骤。

## 目录

1. [工作流结构](#工作流结构)
2. [工作流元数据](#工作流元数据)
3. [输入模式](#输入模式)
4. [步骤定义](#步骤定义)
5. [步骤属性](#步骤属性)
6. [变量替换](#变量替换)
7. [控制流](#控制流)
8. [示例](#示例)

## 工作流结构

工作流是一个YAML文档，具有以下顶层结构：

```yaml
name: workflow_name
display_name: 显示名称
description: 工作流功能的简要描述

inputSchema:
  # 输入模式定义
  type: object
  properties:
    # 属性定义
  required:
    # 必需属性

steps:
  # 步骤定义数组
  - name: step_name
    tool: server_name/tool_name
    # 其他步骤属性
```

## 工作流元数据

### name (必需)
工作流的唯一标识符。在内部用于引用工作流。

```yaml
name: api_health_monitor
```

### display_name (可选)
用于显示的人类可读名称。

```yaml
display_name: API健康监控
```

### description (可选)
工作流功能的简要描述。

```yaml
description: 监控API端点并生成健康报告
```

## 输入模式

`inputSchema`部分定义了工作流的预期输入参数，遵循JSON Schema规范。

### 基本结构

```yaml
inputSchema:
  type: object
  properties:
    parameter_name:
      type: string|number|boolean|array|object
      description: "参数的描述"
      default: 默认值
  required:
    - parameter_name
```

### 示例

```yaml
inputSchema:
  type: object
  properties:
    api_endpoints:
      type: array
      description: "要监控的API端点列表"
      default: []
    timeout:
      type: number
      description: "超时时间（秒）"
      default: 30
  required:
    - api_endpoints
```

## 步骤定义

`steps`部分是一个步骤定义数组，将按顺序执行。每个步骤代表对MCP服务器的工具调用。

### 基本步骤结构

```yaml
steps:
  - name: step_identifier
    tool: server_name/tool_name
    inputs:
      parameter_name: parameter_value
    outputs: output_variable_name
```

## 步骤属性

### name (必需)
工作流内步骤的唯一标识符。

```yaml
name: check_api_status
```

### tool (必需)
指定要调用的MCP工具，格式为`server_name/tool_name`。

```yaml
tool: monitor_alert_mcp/api_checker
```

### inputs (可选)
传递给工具的输入参数。值可以是字面量或使用Jinja2语法的变量。

```yaml
inputs:
  endpoint: "{{ endpoint_url }}"
  timeout: 30
  headers:
    Authorization: "Bearer {{ api_token }}"
```

### outputs (可选)
存储工具执行结果的变量名。此变量可在后续步骤中使用。

```yaml
outputs: api_status_result
```

### when (可选)
确定是否应执行步骤的条件表达式。使用Jinja2表达式语法。

```yaml
when: "{{ api_status_result.status == 'healthy' }}"
```

### on_fail (可选)
定义步骤失败时的行为。可能的值：
- `break`：停止工作流执行（默认）
- `continue`：继续执行下一步

```yaml
on_fail: continue
```

### foreach (可选)
为列表中的每个项目执行步骤。为步骤创建循环上下文。

```yaml
foreach:
  endpoint: "{{ api_endpoints }}"
```

### loop (可选)
执行步骤的特定次数。

```yaml
loop: 5
```

### until (可选)
当条件满足时可以提前终止循环的条件表达式。

```yaml
until: "{{ result.success == true }}"
```

## 变量替换

BiXFlow在工作流定义中使用Jinja2模板进行变量替换。

### 基本变量替换

```yaml
inputs:
  endpoint: "{{ endpoint_url }}"
  timeout: "{{ config.timeout | default(30) }}"
```

### 变量过滤器

支持的常用Jinja2过滤器：
- `default(value)`：如果变量未定义，则提供默认值
- `length`：获取列表或字符串的长度
- `upper/lower`：转换字符串大小写

```yaml
when: "{{ api_endpoints | length > 0 }}"
inputs:
  name: "{{ user_name | default('匿名用户') }}"
```

### 复杂表达式

```yaml
when: "{{ result.status == 'success' and result.count > 0 }}"
inputs:
  message: "成功处理了 {{ result.count }} 个项目"
```

## 控制流

### 条件执行

使用`when`属性条件性地执行步骤：

```yaml
- name: response_time_log
  tool: monitor_alert_mcp/response_logger
  inputs:
    endpoint: "{{ endpoint }}"
    sample_count: 3
  outputs: performance_data
  when: "{{ api_status.status == 'healthy' }}"
```

### 循环

#### Foreach循环

遍历项目列表：

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

#### 计数循环

执行步骤特定次数：

```yaml
- name: retry_operation
  tool: some_server/retryable_tool
  inputs:
    data: "{{ input_data }}"
  loop: 3
  outputs: result
  until: "{{ result.success }}"
```

### 错误处理

控制步骤失败时的工作流行为：

```yaml
- name: critical_operation
  tool: important_server/critical_tool
  inputs:
    data: "{{ input_data }}"
  outputs: result
  on_fail: break  # 失败时停止工作流（默认）

- name: optional_operation
  tool: optional_server/optional_tool
  inputs:
    data: "{{ input_data }}"
  outputs: result
  on_fail: continue  # 即使步骤失败也继续工作流
```

## 示例

### 简单的API健康检查工作流

```yaml
name: api_health_check
display_name: API健康检查
description: 检查API端点的健康状态

inputSchema:
  type: object
  properties:
    api_endpoints:
      type: array
      description: "要检查的API端点列表"
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

### 数据处理工作流

```yaml
name: data_processing
display_name: 数据处理管道
description: 使用验证和清理处理和分析数据

inputSchema:
  type: object
  properties:
    raw_data:
      type: array
      description: "要处理的原始数据"
      default: []
    validation_rules:
      type: object
      description: "数据验证规则"
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

### 嵌套工作流执行

```yaml
name: comprehensive_analysis
display_name: 综合分析
description: 使用嵌套工作流执行综合数据分析

inputSchema:
  type: object
  properties:
    raw_data:
      type: array
      description: "用于分析的原始数据"
      default: []
    api_endpoints:
      type: array
      description: "要监控的API端点"
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

### Excel文件合并工作流

```yaml
name: merge_excel_files
display_name: Excel文件合并器
description: 遍历目录并将所有Excel文件合并为单个Excel文件

inputSchema:
  type: object
  properties:
    input_directory:
      type: string
      description: "包含要合并的Excel文件的目录"
    output_file:
      type: string
      description: "输出合并后的Excel文件路径"
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

## 最佳实践

1. **描述性名称**：为工作流和步骤使用清晰、描述性的名称
2. **一致的命名**：为变量和参数遵循一致的命名约定
3. **输入验证**：定义全面的输入模式并提供适当的默认值
4. **错误处理**：适当使用`on_fail`来控制错误时的工作流行为
5. **文档**：为工作流和复杂步骤包含描述
6. **模块化**：将复杂的工作流分解为更小的可重用组件
7. **条件逻辑**：使用`when`条件使工作流更加灵活
8. **循环优化**：使用`until`条件避免不必要的迭代
