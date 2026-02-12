# BiXFlow 示例代码

本目录包含 BiXFlow 框架的使用示例,帮助您快速了解和掌握框架的各项功能。

## 📋 目录

- [运行示例前的准备](#运行示例前的准备)
- [示例列表](#示例列表)
- [常见问题](#常见问题)

## 🚀 运行示例前的准备

### 1. 安装核心依赖

所有示例都需要安装 BiXFlow 核心包及其依赖:

```bash
# 从源码安装(推荐用于开发)
cd BiXFlow
pip install -e .

# 或者从 PyPI 安装
pip install BiXFlow
```

### 2. 启动 MCP 服务器

大多数示例需要运行 MCP 服务器。请在**一个终端窗口**中启动所有服务器:

```bash
# 在项目根目录下运行
./mcps/start_servers.sh

# Windows 用户可以使用 Git Bash 或 WSL
# 或单独启动每个服务器(见下文)
```

**单独启动各个服务器(可选):**

```bash
# 终端1: 启动数据处理服务器
python -m mcps.data_processor_mcp.server --port 8001 --transport streamable_http

# 终端2: 启动监控告警服务器
python -m mcps.monitor_alert_mcp.server --port 8002 --transport streamable_http

# 终端3: 启动报告生成服务器
python -m mcps.report_generator_mcp.server --port 8003 --transport streamable_http

# 终端4: 启动Excel处理服务器
python -m mcps.excel_processor_mcp.server --port 8004 --transport streamable_http
```

### 3. 确认服务器状态

启动服务器后,您应该看到类似的输出:

```
Starting data processor MCP server on 127.0.0.1:8001
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8001
```

## 📚 示例列表

### 1. basic_usage.py - 基础用法示例

**功能说明:**
演示 BiXFlow 的四种基本用法:
- 同步执行(从内容)
- 异步执行(从内容)
- 同步执行(从文件)
- 异步执行(从文件)

**依赖要求:**
- ✅ 仅需核心依赖(无需额外安装)

**适用场景:**
- 初次接触 BiXFlow
- 了解基本 API 使用方法
- 学习同步和异步执行的区别

**运行方式:**

```bash
# 确保在项目根目录
cd BiXFlow

# 确保已启动 MCP 服务器
./mcps/start_servers.sh

# 在另一个终端运行示例
python examples/basic_usage.py
```

**预期输出:**
```
=== Basic BiXFlow Examples ===

1. Running synchronous example with content...
Workflow execution result: {
  "status": "done",
  "data": {...}
}

2. Running asynchronous example with content...
Workflow execution result: {...}
```

---

### 2. advanced_usage.py - 高级特性示例

**功能说明:**
展示 BiXFlow 的高级功能:
- 自定义客户端配置
- 工作流进度处理
- 详细的错误处理
- 异常分类和处理

**依赖要求:**
- ✅ 仅需核心依赖(无需额外安装)

**适用场景:**
- 需要监听工作流执行进度
- 需要细粒度的错误处理
- 了解高级 API 使用方法

**运行方式:**

```bash
# 确保已启动 MCP 服务器
./mcps/start_servers.sh

# 运行示例
python examples/advanced_usage.py
```

**预期输出:**
```
=== Advanced BiXFlow Examples ===

1. Configuring custom client with content:
Available servers: ['data_processor_mcp', 'monitor_alert_mcp', 'report_generator_mcp']

2. Handling workflow progress with content:
[PROGRESS] Starting execution of step check_api_status
[STEP DONE] Step check_api_status completed
[DONE] Workflow completed successfully
```

---

### 3. nested_workflow_usage.py - 嵌套工作流示例

**功能说明:**
演示工作流嵌套调用功能:
- 一个工作流调用另一个工作流
- 多个 MCP 服务的协同工作
- 数据在不同服务间的流转
- 复杂业务流程的编排

**依赖要求:**
- ✅ 仅需核心依赖(无需额外安装)

**适用场景:**
- 需要组合多个 MCP 服务
- 构建复杂的多步骤流程
- 了解工作流嵌套机制

**运行方式:**

```bash
# 确保已启动所有 MCP 服务器
./mcps/start_servers.sh

# 运行示例
python examples/nested_workflow_usage.py
```

**预期输出:**
```
BiXFlow Nested Workflow Test
==================================================

1. Testing asynchronous nested workflow execution:
=== Testing Nested Workflow Execution ===

Executing nested workflow: data_cleaning_analysis
This workflow demonstrates:
- Calling comprehensive_analyzer tool (nested calls to multiple MCP services)
- Formatting the result with report formatter
--------------------------------------------------
[PROGRESS] Starting execution of step data_validation
[STEP DONE] Step data_validation completed
[DONE] Nested workflow completed successfully
```

---

### 4. excel_merge_demo.py - Excel 文件合并示例

**功能说明:**
展示实际业务场景的应用:
- 自动创建示例 Excel 文件
- 使用工作流合并多个 Excel 文件
- 处理文件路径和目录
- 完整的数据处理流程

**依赖要求:**
- ⚠️ **需要额外依赖**: `pandas` 和 `openpyxl`

**安装额外依赖:**

```bash
# 方法1: 安装所有开发依赖(包含pandas和openpyxl)
pip install -e ".[dev]"

# 方法2: 仅安装Excel处理所需的依赖
pip install pandas openpyxl
```

**适用场景:**
- 需要处理 Excel 文件
- 了解文件操作工作流
- 学习实际业务场景的应用

**运行方式:**

```bash
# 1. 安装额外依赖
pip install pandas openpyxl

# 2. 确保已启动 MCP 服务器
./mcps/start_servers.sh

# 3. 运行示例
python examples/excel_merge_demo.py
```

**预期输出:**
```
Excel Merge Workflow Demo
==================================================

Created sample Excel files in sample_excel_files/
Running Excel merge workflow...
Input directory: c:/chengtong/workspace2025/BiXFlow/sample_excel_files
Output file: c:/chengtong/workspace2025/BiXFlow/merged_employees.xlsx
--------------------------------------------------
Progress: Starting workflow execution
✅ Workflow completed successfully!
Final result: {...}

Demo completed!
```

**生成文件:**
运行后会在项目根目录生成:
- `sample_excel_files/` - 包含3个示例Excel文件
- `merged_employees.xlsx` - 合并后的Excel文件

---

## 🔍 示例对比表

| 示例文件 | 难度 | 额外依赖 | 运行时间 | 学习重点 |
|---------|------|---------|---------|---------|
| `basic_usage.py` | ⭐ | 无 | ~10秒 | 基础API、同步/异步 |
| `advanced_usage.py` | ⭐⭐ | 无 | ~10秒 | 进度处理、错误处理 |
| `nested_workflow_usage.py` | ⭐⭐⭐ | 无 | ~15秒 | 工作流嵌套、服务协同 |
| `excel_merge_demo.py` | ⭐⭐ | pandas, openpyxl | ~20秒 | 文件处理、实际应用 |

## ❓ 常见问题

### Q1: 运行示例时提示 "Connection refused" 或 "连接被拒绝"

**原因:** MCP 服务器未启动或端口被占用

**解决方案:**
```bash
# 1. 检查服务器是否启动
ps aux | grep python | grep mcp  # Linux/Mac
tasklist | findstr python       # Windows

# 2. 重新启动服务器
./mcps/start_servers.sh

# 3. 如果端口被占用,修改端口
# 编辑 mcps/mcp_servers_setting.json
# 修改相应端口号
```

### Q2: 运行 excel_merge_demo.py 时提示 "pandas not installed"

**原因:** 缺少 Excel 处理所需的依赖

**解决方案:**
```bash
pip install pandas openpyxl
```

### Q3: 示例运行很慢或超时

**原因:** 网络连接问题或服务器响应慢

**解决方案:**
```bash
# 1. 检查网络连接
curl https://httpbin.org/get

# 2. 增加超时时间
# 修改 mcps/mcp_servers_setting.json
# 添加或修改 "timeout" 字段

# 3. 使用本地API端点进行测试
# 修改示例中的 api_endpoints 参数
```

### Q4: 想修改示例的参数

**解决方案:**
- 直接编辑示例文件中的参数
- 或在运行时通过命令行传递参数(如果示例支持)

### Q5: 如何在 CI/CD 环境中运行测试?

**解决方案:**
```yaml
# GitHub Actions 示例
name: Run Examples

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -e .
          pip install -e ".[dev]"
      - name: Start MCP servers
        run: ./mcps/start_servers.sh &
      - name: Run examples
        run: |
          python examples/basic_usage.py
          python examples/advanced_usage.py
          python examples/nested_workflow_usage.py
```

### Q6: 示例可以用于生产环境吗?

**答案:** 
- ✅ 示例代码展示了正确的使用方式
- ⚠️ 但需要根据实际需求进行调整:
  - 添加更完善的错误处理
  - 实现日志记录和监控
  - 配置生产环境的参数
  - 考虑安全性和性能优化

## 💡 学习路径建议

### 初学者
1. 先运行 `basic_usage.py` 了解基础概念
2. 阅读 `advanced_usage.py` 学习错误处理
3. 尝试修改示例参数,观察结果变化

### 进阶开发者
1. 深入研究 `nested_workflow_usage.py`
2. 理解工作流的嵌套和协同机制
3. 尝试创建自己的工作流定义

### 高级开发者
1. 分析 `excel_merge_demo.py` 的实际应用
2. 学习如何将业务逻辑抽象为工作流
3. 尝试开发自定义的 MCP 服务器

## 📖 相关文档

- [主 README](../README.md) - 项目概述
- [工作流语法指南](../docs/workflow_syntax.md) - YAML工作流定义语法
- [贡献指南](../CONTRIBUTING.md) - 如何参与项目贡献

## 🤝 反馈与支持

如果您在运行示例时遇到问题:

1. 查看本文档的"常见问题"部分
2. 检查项目的 [Issue](https://github.com/your-organization/BiXFlow/issues)
3. 提交新的 Issue 并包含:
   - 运行的示例文件名
   - 完整的错误信息
   - 您的操作系统和Python版本
   - 已尝试的解决方案

## 📝 许可证

所有示例代码遵循项目的 MIT 许可证。您可以自由使用、修改和分发这些代码。

---

**祝您使用愉快!** 🎉
