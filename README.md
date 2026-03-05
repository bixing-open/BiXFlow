# BiXFlow
[![Featured in awesome-mcp-devtoos](https://img.shields.io/badge/Featured_in-awesome--mcp-orange)](https://github.com/punkpeye/awesome-mcp-devtools)
[![PyPI version](https://badge.fury.io/py/BiXFlow.svg)](https://pypi.org/project/BiXFlow/)
[![Python version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[English Version](README_en.md)

BiXFlow 是由中国移动研究院CMRI的BiXing（必行）团队开发的基于 Model Context Protocol (MCP) 的高效、确定性工作流执行框架。它提供了一套简单易用的接口，用于定义、管理和执行复杂的工作流。与传统的固定工作流文件方式不同，BiXFlow允许用户直接提供YAML工作流内容和MCP配置内容来执行工作流。

## 目录结构

```
BiXFlow/
├── README.md
├── .gitignore
├── requirements.txt
├── setup.py
├── BiXFlow/                     # 主包目录
│   ├── __init__.py              # 包入口，暴露核心API
│   ├── client.py                # MCP客户端实现
│   ├── workflow.py              # 工作流执行器
│   ├── config.py                # 配置管理
│   ├── utils.py                 # 工具函数
│   ├── exceptions.py            # 自定义异常
│   └── cli.py                   # 命令行接口
├── examples/                    # 使用示例
├── workflows/                   # 示例工作流定义文件
├── mcps/                        # 示例MCP服务配置和实现
│   ├── excel_processor_mcp/     # Excel处理服务
│   └── ...                      # 其他MCP服务
├── tests/                       # 测试代码
└── docs/                        # 文档
```

## 功能特性

- **灵活的工作流执行**: 支持直接从YAML内容执行工作流，无需预定义文件
- **动态配置**: 支持从JSON内容动态加载MCP服务器配置
- **标准化协议**: 实现了 Model Context Protocol，确保与各种MCP服务的互操作性
- **简洁的API**: 提供简单易用的接口来执行YAML定义的工作流
- **灵活的工作流执行**: 支持同步和异步方式执行工作流
- **嵌套工作流支持**: 支持在MCP服务中定义子工作流并作为工具使用
- **标准化目录结构**: 遵循Python包的最佳实践
- **完善的错误处理**: 提供详细的错误信息和异常处理机制

## 工作流的用途和作用

BiXFlow提供了一种智能体工作流机制，专为解决大模型在处理复杂任务时的不稳定性而设计。通过将复杂任务分解为一系列可控的步骤，工作流确保了任务执行的可靠性和一致性。最重要的是，BiXFlow工作流完全通过组装MCP工具来实现，这使得工作流极其灵活便捷。

### 智能体直接调用

工作流可以直接被智能体调用执行，使得智能体能够稳定地处理复杂的业务流程。智能体只需提供工作流定义和必要的参数，BiXFlow就会负责执行整个工作流并返回结果。

### 解决大模型不稳定性问题

大模型在处理复杂任务时往往会出现以下问题：

- 输出不一致，同一次任务多次执行结果不同
- 处理长任务时容易出现幻觉或偏离主题
- 难以处理需要多步骤协调的任务

BiXFlow通过将复杂任务分解为明确定义的工作流步骤，有效解决了这些问题：

- 每个步骤都有明确的输入输出定义
- 步骤间的数据传递是精确可控的
- 支持条件判断和循环控制，提高处理灵活性
- 出错时可以精确定位问题步骤并进行相应的错误处理

### 完全基于MCP工具组装

BiXFlow工作流的最大优势在于完全通过组装现有的MCP工具来实现复杂功能，而不是重新开发。这种方式带来了显著的好处：

- **极高的灵活性**：可以根据需求自由组合不同的MCP工具，构建定制化的工作流
- **便捷的扩展性**：当有新的MCP工具可用时，可以轻松地将其集成到现有工作流中
- **降低开发成本**：无需从零开始实现功能，直接利用现有的成熟工具
- **更好的可维护性**：各个工具相对独立，便于单独更新和维护

### 嵌套工作流支持

工作流不仅可以作为独立的执行单元，还可以作为MCP工具的一部分嵌套调用。这意味着：

- 一个工作流可以调用另一个工作流作为其步骤之一
- 支持构建层次化、模块化的工作流体系
- 提高了工作流的复用性和可维护性
- 使得复杂业务流程的管理变得更加简单

这种嵌套调用的能力使得BiXFlow成为一个强大的工作流编排平台，能够应对各种复杂的业务场景。

## 安装

BiXFlow支持多种安装方式，以满足不同用户的需求。

### 1. 从PyPI安装（推荐用于普通用户）

对于只需要使用BiXFlow的普通用户，可以直接从PyPI安装：

```bash
# 安装最新版本
pip install BiXFlow

# 安装特定版本
pip install BiXFlow==0.9.0
```

### 2. 从源码安装

对于想要获取最新开发版本或进行二次开发的用户，可以从源码安装：

```bash
# 克隆仓库
git clone <repository-url>
cd BiXFlow

# 安装依赖
pip install -r requirements.txt

# 以开发模式安装包（推荐）
pip install -e .
```

### 3. 安装预编译包

对于不想从源码构建的用户，可以下载预编译的wheel包或tar.gz包进行安装：

```bash
# 安装wheel包
pip install BiXFlow-0.9.0-py3-none-any.whl

# 安装tar.gz包
pip install BiXFlow-0.9.0.tar.gz
```

安装完成后，您就可以在Python代码中导入 `BiXFlow`包，或使用命令行工具 `BiXFlow`了。

## 构建和发布Python包

如果您是项目的维护者并希望构建和发布Python包到PyPI，请按照以下步骤操作：

### 使用发布脚本（推荐）

项目提供了一个便捷的发布脚本，可以帮助您自动化构建和发布过程：

```bash
# 运行发布脚本
python scripts/release.py

# 脚本将引导您完成以下步骤：
# 1. 检查先决条件
# 2. 清理之前的构建产物
# 3. 构建源码分发包和wheel包
# 4. 检查包的质量
# 5. 询问您希望发布到TestPyPI还是PyPI
```

### 手动构建分发包

```bash
# 安装构建工具
pip install build twine

# 构建源码分发包和wheel包
python -m build

# 构建后的包将位于dist/目录下，包括：
# - BiXFlow-0.9.0-py3-none-any.whl (wheel包)
# - BiXFlow-0.9.0.tar.gz (源码分发包)
```

### 验证构建的包

```bash
# 检查包的质量
python -m twine check dist/*

# 检查应该显示：PASSED
```

### 发布到PyPI

```bash
# 上传到PyPI（需要PyPI账户）
twine upload dist/*

# 上传到TestPyPI进行测试
twine upload --repository testpypi dist/*
```

### 发布到私有仓库

```bash
# 上传到私有仓库
twine upload --repository-url https://your-private-pypi.com/simple/ dist/*
```

## 快速开始

有关如何定义工作流的详细信息，请参阅[工作流语法指南](docs/workflow_syntax.md)。该指南涵盖了工作流定义的所有方面，包括元数据、输入模式、步骤属性、变量替换和控制流结构。

### 基本用法 - 从内容执行工作流

```python
from BiXFlow import run_workflow_from_content_sync
import json

# 用户提供的YAML工作流内容
workflow_content = """
name: api_health_monitor
display_name: API健康监控
description: 监控API端点健康状态，记录响应时间和告警

inputSchema:
  type: object
  properties:
    api_endpoints:
      type: array
      description: "要监控的API端点列表"
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

# 用户提供的MCP配置内容
mcp_config_content = {
  "monitor_alert_mcp": {
    "name": "monitor_alert_mcp",
    "timeout": 60,
    "url": "http://localhost:8002/mcp/",
    "transport": "streamable_http"
  }
}

# 执行工作流
result = run_workflow_from_content_sync(
    workflow_content=workflow_content,
    mcp_config=mcp_config_content,
    args={"api_endpoints": ["https://httpbin.org/get"]}
)

print("执行结果:", result)
```

### 异步用法 - 从内容执行工作流

```python
import asyncio
from BiXFlow import run_workflow_from_content

async def main():
    # 用户提供的YAML工作流内容
    workflow_content = """
name: api_health_monitor
# ... (工作流定义内容)
"""

    # 用户提供的MCP配置内容
    mcp_config_content = {
      "monitor_alert_mcp": {
        "name": "monitor_alert_mcp",
        "timeout": 60,
        "url": "http://localhost:8002/mcp/",
        "transport": "streamable_http"
      }
    }
  
    # 异步执行工作流
    result = await run_workflow_from_content(
        workflow_content=workflow_content,
        mcp_config=mcp_config_content,
        args={"api_endpoints": ["https://httpbin.org/get"]}
    )
  
    print("执行结果:", result)

# 运行异步函数
asyncio.run(main())
```

### 使用BiXFlow.BiXFlowExecutor类

```python
from BiXFlow import BiXFlowExecutor

# 用户提供的MCP配置内容
mcp_config_content = {
  "monitor_alert_mcp": {
    "name": "monitor_alert_mcp",
    "timeout": 60,
    "url": "http://localhost:8002/mcp/",
    "transport": "streamable_http"
  }
}

# 创建工作流执行器
executor = BiXFlowExecutor(mcp_config_content)

# 用户提供的YAML工作流内容
workflow_content = """
name: api_health_monitor
# ... (工作流定义内容)
"""

# 执行工作流
result = executor.run_workflow_from_content_sync(
    workflow_content=workflow_content,
    args={"api_endpoints": ["https://httpbin.org/get"]}
)

print("执行结果:", result)
```

## 命令行工具

BiXFlow还提供了一个命令行工具，可以直接从命令行执行工作流：

```bash
# 显示版本信息
BiXFlow --version

# 列出可用的工作流
BiXFlow list-workflows

# 列出可用的工作流（详细格式）
BiXFlow list-workflows --format detailed

# 从文件执行工作流（使用默认配置文件）
BiXFlow run workflows/api_health_monitor/api_health_monitor_workflow.yaml --args '{"api_endpoints": ["https://httpbin.org/get"]}'

# 从文件执行工作流（指定配置文件）
BiXFlow run workflows/api_health_monitor/api_health_monitor_workflow.yaml --args '{"api_endpoints": ["https://httpbin.org/get"]}' --config mcps/mcp_servers_setting.json

# 从内容执行工作流（使用JSON字符串作为配置）
BiXFlow run-content "name: test\nsteps: []" --args '{"api_endpoints": ["https://httpbin.org/get"]}' --config '{"monitor_alert_mcp": {"url": "http://localhost:8002/mcp/", "transport": "streamable_http"}}'

# 从内容执行工作流（使用配置文件路径）
BiXFlow run-content "name: test\nsteps: []" --args '{"api_endpoints": ["https://httpbin.org/get"]}' --config mcps/mcp_servers_setting.json
```

## 嵌套工作流功能

BiXFlow支持在MCP服务中定义子工作流并将其封装为工具使用。例如，`report_generator_mcp`服务中包含一个综合分析工作流，可以处理数据验证、清洗、分析和报告生成的完整流程。

### 启动MCP服务器

在运行嵌套工作流示例之前，需要先启动MCP服务器：

```bash
# 启动所有MCP服务器
./mcps/start_servers.sh
```

### 运行嵌套工作流示例

```bash
# 运行嵌套工作流示例
python examples/nested_workflow_usage.py
```

该示例展示了如何：

1. 执行包含嵌套工具调用的 `data_cleaning_analysis` 工作流
2. 处理工作流执行过程中的进度更新和最终结果

## 运行示例

项目提供了多个示例来展示BiXFlow的功能。详细的示例说明、依赖要求和运行指南，请查看:

- [examples/README.md](examples/README.md) (中文版)
- [examples/README_en.md](examples/README_en.md) (English Version)

### 快速开始

运行这些示例前需要先启动MCP服务器：

```bash
# 在一个终端中启动所有MCP服务器：
./mcps/start_servers.sh
```

然后在另一个终端中运行示例：

```bash
# 运行基本用法示例（无需额外依赖）
python examples/basic_usage.py

# 运行高级用法示例（无需额外依赖）
python examples/advanced_usage.py

# 运行嵌套工作流示例（无需额外依赖）
python examples/nested_workflow_usage.py

# 运行Excel文件合并示例（需要额外安装 pandas 和 openpyxl）
python examples/excel_merge_demo.py
```

### 示例说明

| 示例                                                       | 难度   | 额外依赖         | 说明                       |
| ---------------------------------------------------------- | ------ | ---------------- | -------------------------- |
| [basic_usage.py](examples/basic_usage.py)                     | ⭐     | 无               | 基础API使用，同步/异步执行 |
| [advanced_usage.py](examples/advanced_usage.py)               | ⭐⭐   | 无               | 进度处理、错误处理         |
| [nested_workflow_usage.py](examples/nested_workflow_usage.py) | ⭐⭐⭐ | 无               | 工作流嵌套、多服务协同     |
| [excel_merge_demo.py](examples/excel_merge_demo.py)           | ⭐⭐   | pandas, openpyxl | Excel文件处理实际应用      |

📖 **查看完整文档**: [examples/README.md](examples/README.md) 包含详细的运行说明、常见问题解答和学习路径建议。

## 开发指南

1. Fork 本项目
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

### 构建和测试Python包

作为项目维护者，您可以构建和测试Python包以确保其质量：

```bash
# 安装开发依赖（包括构建和发布工具）
pip install -e ".[dev]"

# 构建包
python -m build

# 检查包的质量
twine check dist/*

# 在干净的环境中测试安装
pip install dist/BiXFlow-0.9.0-py3-none-any.whl

# 运行测试
python -m pytest tests/
```

## 贡献

我们欢迎任何形式的贡献！在贡献之前，请确保：

1. 阅读并理解项目的代码风格
2. 为新功能添加相应的测试
3. 确保所有现有测试都能通过
4. 更新相关文档

### 开发环境设置

```bash
# 克隆仓库
git clone <repository-url>
cd BiXFlow

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或者
venv\Scripts\activate  # Windows

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
python -m pytest tests/
```

### 代码风格

本项目遵循PEP 8代码规范，使用以下工具进行代码格式化：

- Black: 代码格式化
- Flake8: 代码检查

### 测试

在提交代码之前，请确保所有测试都能通过：

```bash
# 运行所有测试（基本测试）
python -m pytest tests/
```

注意：要运行涉及MCP服务器的测试，需要先启动MCP服务器：

```bash
# 在一个终端中运行MCP服务器：
./mcps/start_servers.sh

# 然后在另一个终端中运行MCP服务器工具测试：
python -m pytest tests/test_mcps.py -v
```

### 提交信息规范

请使用有意义的提交信息，遵循以下格式：

- `feat: ` 新功能
- `fix: ` 修复bug
- `docs: ` 文档更新
- `style: ` 代码格式调整
- `refactor: ` 代码重构
- `test: ` 测试相关
- `chore: ` 构建过程或辅助工具的变动

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解更多细节。

## 迁移指南

如果您是从旧版本升级，请查看我们的[迁移指南](docs/migration_guide.md)了解如何迁移到最新版本。

## 联系方式

如果您有任何问题或建议，请通过以下方式联系我们：

- 提交 Issue
- 发送邮件至 [bixing_support@chinamobile.com](mailto:bixing_support@chinamobile.com)
