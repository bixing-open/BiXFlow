# BiXFlow Examples

This directory contains usage examples for the BiXFlow framework to help you quickly understand and master its features.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Example List](#example-list)
- [Common Issues](#common-issues)

## 🚀 Prerequisites

### 1. Install Core Dependencies

All examples require the BiXFlow core package and its dependencies:

```bash
# Install from source (recommended for development)
cd BiXFlow
pip install -e .

# Or install from PyPI
pip install BiXFlow
```

### 2. Start MCP Servers

Most examples require running MCP servers. Start all servers in **one terminal window**:

```bash
# Run from project root directory
./mcps/start_servers.sh

# Windows users can use Git Bash or WSL
# Or start each server individually (see below)
```

**Starting servers individually (optional):**

```bash
# Terminal 1: Start data processor server
python -m mcps.data_processor_mcp.server --port 8001 --transport streamable_http

# Terminal 2: Start monitor alert server
python -m mcps.monitor_alert_mcp.server --port 8002 --transport streamable_http

# Terminal 3: Start report generator server
python -m mcps.report_generator_mcp.server --port 8003 --transport streamable_http

# Terminal 4: Start Excel processor server
python -m mcps.excel_processor_mcp.server --port 8004 --transport streamable_http
```

### 3. Verify Server Status

After starting servers, you should see output similar to:

```
Starting data processor MCP server on 127.0.0.1:8001
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8001
```

## 📚 Example List

### 1. basic_usage.py - Basic Usage

**Description:**
Demonstrates four basic usage patterns of BiXFlow:
- Synchronous execution (from content)
- Asynchronous execution (from content)
- Synchronous execution (from file)
- Asynchronous execution (from file)

**Dependencies:**
- ✅ Core dependencies only (no additional installation needed)

**Use Cases:**
- First time using BiXFlow
- Learn basic API usage
- Understand synchronous vs asynchronous execution

**How to Run:**

```bash
# Ensure you're in the project root
cd BiXFlow

# Ensure MCP servers are started
./mcps/start_servers.sh

# Run the example in another terminal
python examples/basic_usage.py
```

**Expected Output:**
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

### 2. advanced_usage.py - Advanced Features

**Description:**
Shows advanced features of BiXFlow:
- Custom client configuration
- Workflow progress handling
- Detailed error handling
- Exception classification and handling

**Dependencies:**
- ✅ Core dependencies only (no additional installation needed)

**Use Cases:**
- Need to monitor workflow execution progress
- Need fine-grained error handling
- Learn advanced API usage

**How to Run:**

```bash
# Ensure MCP servers are started
./mcps/start_servers.sh

# Run the example
python examples/advanced_usage.py
```

**Expected Output:**
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

### 3. nested_workflow_usage.py - Nested Workflows

**Description:**
Demonstrates nested workflow functionality:
- One workflow calling another workflow
- Multiple MCP services working together
- Data flow between services
- Complex business process orchestration

**Dependencies:**
- ✅ Core dependencies only (no additional installation needed)

**Use Cases:**
- Need to combine multiple MCP services
- Build complex multi-step workflows
- Understand workflow nesting mechanism

**How to Run:**

```bash
# Ensure all MCP servers are started
./mcps/start_servers.sh

# Run the example
python examples/nested_workflow_usage.py
```

**Expected Output:**
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

### 4. excel_merge_demo.py - Excel File Merge

**Description:**
Shows real-world application scenarios:
- Automatically create sample Excel files
- Merge multiple Excel files using workflow
- Handle file paths and directories
- Complete data processing workflow

**Dependencies:**
- ⚠️ **Additional dependencies required**: `pandas` and `openpyxl`

**Install Additional Dependencies:**

```bash
# Method 1: Install all dev dependencies (includes pandas and openpyxl)
pip install -e ".[dev]"

# Method 2: Install only Excel processing dependencies
pip install pandas openpyxl
```

**Use Cases:**
- Need to process Excel files
- Learn file operation workflows
- Real-world application scenarios

**How to Run:**

```bash
# 1. Install additional dependencies
pip install pandas openpyxl

# 2. Ensure MCP servers are started
./mcps/start_servers.sh

# 3. Run the example
python examples/excel_merge_demo.py
```

**Expected Output:**
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

**Generated Files:**
After running, the following files will be generated in the project root:
- `sample_excel_files/` - Contains 3 sample Excel files
- `merged_employees.xlsx` - Merged Excel file

---

## 🔍 Example Comparison Table

| Example File | Difficulty | Extra Dependencies | Runtime | Learning Focus |
|--------------|-----------|-------------------|---------|----------------|
| `basic_usage.py` | ⭐ | None | ~10s | Basic API, sync/async |
| `advanced_usage.py` | ⭐⭐ | None | ~10s | Progress handling, error handling |
| `nested_workflow_usage.py` | ⭐⭐⭐ | None | ~15s | Workflow nesting, service coordination |
| `excel_merge_demo.py` | ⭐⭐ | pandas, openpyxl | ~20s | File processing, real-world application |

## ❓ Common Issues

### Q1: "Connection refused" or "连接被拒绝" error when running examples

**Cause:** MCP servers not started or ports are occupied

**Solution:**
```bash
# 1. Check if servers are running
ps aux | grep python | grep mcp  # Linux/Mac
tasklist | findstr python       # Windows

# 2. Restart servers
./mcps/start_servers.sh

# 3. If port is occupied, change the port
# Edit mcps/mcp_servers_setting.json
# Modify the corresponding port number
```

### Q2: "pandas not installed" error when running excel_merge_demo.py

**Cause:** Missing Excel processing dependencies

**Solution:**
```bash
pip install pandas openpyxl
```

### Q3: Examples run slowly or timeout

**Cause:** Network connection issues or slow server response

**Solution:**
```bash
# 1. Check network connection
curl https://httpbin.org/get

# 2. Increase timeout
# Modify mcps/mcp_servers_setting.json
# Add or modify "timeout" field

# 3. Use local API endpoints for testing
# Modify api_endpoints parameter in examples
```

### Q4: Want to modify example parameters

**Solution:**
- Directly edit parameters in example files
- Or pass parameters via command line (if supported by the example)

### Q5: How to run tests in CI/CD environment?

**Solution:**
```yaml
# GitHub Actions example
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

### Q6: Can examples be used in production?

**Answer:** 
- ✅ Example code demonstrates correct usage patterns
- ⚠️ But requires adjustments for production use:
  - Add more comprehensive error handling
  - Implement logging and monitoring
  - Configure production environment parameters
  - Consider security and performance optimizations

## 💡 Learning Path Recommendations

### Beginners
1. Run `basic_usage.py` first to understand basic concepts
2. Read `advanced_usage.py` to learn error handling
3. Try modifying example parameters and observe results

### Intermediate Developers
1. Deep dive into `nested_workflow_usage.py`
2. Understand workflow nesting and coordination mechanisms
3. Try creating your own workflow definitions

### Advanced Developers
1. Analyze real-world application in `excel_merge_demo.py`
2. Learn how to abstract business logic into workflows
3. Try developing custom MCP servers

## 📖 Related Documentation

- [Main README](../README.md) - Project overview
- [Workflow Syntax Guide](../docs/workflow_syntax.md) - YAML workflow definition syntax
- [Contributing Guide](../CONTRIBUTING.md) - How to contribute to the project

## 🤝 Feedback and Support

If you encounter issues while running examples:

1. Check the "Common Issues" section of this document
2. Check project [Issues](https://github.com/your-organization/BiXFlow/issues)
3. Submit a new Issue with:
   - Example file name being run
   - Complete error message
   - Your operating system and Python version
   - Solutions you've tried

## 📝 License

All example code follows the project's MIT license. You are free to use, modify, and distribute this code.

---

**Happy coding!** 🎉
