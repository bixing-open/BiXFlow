# Support

## Getting Help

There are several ways to get help with BiXFlow:

### Documentation

- [README.md](README.md) - BiXFlow项目概览和快速入门指南（中文）
- [README_en.md](README_en.md) - BiXFlow项目概览和快速入门指南（英文）
- [Workflow Syntax Guide](docs/workflow_syntax.md) - 工作流语法详细文档（中文）
- [Workflow Syntax Guide](docs/workflow_syntax_en.md) - 工作流语法详细文档（英文）
- [Migration Guide](docs/migration_guide.md) - 版本迁移指南
- [Contributing Guide](CONTRIBUTING.md) - 如何为项目做贡献

### Community Support

#### GitHub Discussions
Join our community discussions to ask questions, share ideas, and connect with other users:
- [GitHub Discussions](https://github.com/your-organization/BiXFlow/discussions)

#### GitHub Issues
Report bugs, request features, or ask questions by opening an issue:
- [GitHub Issues](https://github.com/your-organization/BiXFlow/issues)

Please use the appropriate issue template:
- [Bug Report](.github/ISSUE_TEMPLATE/bug_report.md) - For reporting bugs
- [Feature Request](.github/ISSUE_TEMPLATE/feature_request.md) - For suggesting new features
- [Documentation Issue](.github/ISSUE_TEMPLATE/documentation.md) - For documentation improvements

### Direct Contact

For questions that cannot be addressed through public channels:

- **Email**: [bixing_support@chinamobile.com](mailto:bixing_support@chinamobile.com)
- **Subject**: Please include "BiXFlow Support" in your email subject

When contacting us directly, please provide:
1. A clear description of your question or issue
2. Your environment details (OS, Python version, BiXFlow version)
3. Any relevant code snippets or error messages
4. Steps to reproduce the issue (if applicable)

## Frequently Asked Questions

### Installation

**Q: How do I install BiXFlow?**

A: You can install BiXFlow using pip:
```bash
pip install BiXFlow
```

For more installation options, see the [Installation Guide](README.md#安装).

**Q: What are the system requirements?**

A: BiXFlow requires:
- Python 3.8 or higher
- Operating system: Windows, Linux, or macOS

### Usage

**Q: How do I execute a workflow from YAML content?**

A: Use the `run_workflow_from_content_sync` function:
```python
from BiXFlow import run_workflow_from_content_sync

result = run_workflow_from_content_sync(
    workflow_content=workflow_content,
    mcp_config=mcp_config_content,
    args={"your": "parameters"}
)
```

**Q: Can I execute workflows asynchronously?**

A: Yes! Use the `run_workflow_from_content` function:
```python
import asyncio
from BiXFlow import run_workflow_from_content

async def main():
    async for result in run_workflow_from_content(
        workflow_content=workflow_content,
        mcp_config=mcp_config,
        args=args
    ):
        print(result)

asyncio.run(main())
```

**Q: How do I connect to MCP servers?**

A: Provide MCP server configuration as a JSON object:
```json
{
  "server_name": {
    "name": "server_name",
    "timeout": 60,
    "url": "http://localhost:8001/mcp/",
    "transport": "streamable_http"
  }
}
```

### Troubleshooting

**Q: I'm getting a connection error when connecting to MCP servers.**

A: Check the following:
1. Ensure MCP servers are running: `./mcps/start_servers.sh`
2. Verify the URL and port in your configuration
3. Check network connectivity to the MCP server
4. Confirm the transport type matches the server's configuration

**Q: My workflow is failing with "Tool not found" error.**

A: Ensure:
1. The tool name format is correct: `server_name/tool_name`
2. The MCP server is registered in your configuration
3. The tool exists on the MCP server

**Q: How do I debug my workflow?**

A: Try these approaches:
1. Use the CLI with verbose output: `BiXFlow run workflow.yaml --args '{"key":"value"}'`
2. Check the workflow syntax against the [Workflow Syntax Guide](docs/workflow_syntax.md)
3. Test each step individually
4. Review error messages carefully

### Migration

**Q: How do I upgrade from an older version?**

A: See the [Migration Guide](docs/migration_guide.md) for detailed instructions on upgrading between versions.

**Q: Will upgrading break my existing workflows?**

A: We maintain backward compatibility within major versions. However, always check the [CHANGELOG.md](CHANGELOG.md) for any breaking changes before upgrading.

## Contributing

We welcome contributions! Please see the [Contributing Guide](CONTRIBUTING.md) for details on:
- Setting up a development environment
- Coding standards
- Testing requirements
- Submitting pull requests

## Reporting Issues

When reporting issues, please include:

1. **Environment Information**
   - Operating system and version
   - Python version
   - BiXFlow version

2. **Description**
   - Clear description of the issue
   - Steps to reproduce
   - Expected behavior vs. actual behavior

3. **Relevant Code**
   - Workflow definition (YAML)
   - MCP configuration (JSON)
   - Minimal reproducible example

4. **Error Messages**
   - Complete error message
   - Stack trace (if applicable)

## Feature Requests

We appreciate feature requests! When suggesting a new feature:

1. Describe the problem you're trying to solve
2. Explain why existing solutions don't work
3. Provide use cases and examples
4. Consider if you'd be willing to contribute the feature

## Security

For security-related issues, please do **not** use public channels. Instead:

- Email: [bixing_support@chinamobile.com](mailto:bixing_support@chinamobile.com)
- Subject: [SECURITY] BiXFlow Security Issue

See the [Security Policy](SECURITY.md) for more details.

## Professional Support

For enterprise users or organizations requiring dedicated support:

- Contact: [bixing_support@chinamobile.com](mailto:bixing_support@chinamobile.com)
- Subject: [ENTERPRISE] BiXFlow Support Inquiry

## Resources

### Official Resources
- [Project Repository](https://github.com/your-organization/BiXFlow)
- [Documentation](https://github.com/your-organization/BiXFlow/tree/main/docs)
- [Change Log](CHANGELOG.md)
- [Roadmap](ROADMAP.md)

### External Resources
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Python Documentation](https://docs.python.org/3/)
- [YAML Specification](https://yaml.org/spec/)

## Community Guidelines

Please follow these guidelines when seeking support:

1. **Be Respectful**: Treat all community members with respect
2. **Be Patient**: Our maintainers are volunteers and may not respond immediately
3. **Be Clear**: Provide clear, concise information about your issue
4. **Search First**: Check existing issues and documentation before asking
5. **Give Back**: Help others when you can

## Response Times

- **GitHub Issues**: Typically within 1-3 business days
- **Email**: Typically within 1-2 business days
- **Security Issues**: Within 48 hours

Response times may vary based on complexity and volume of requests.

## License

BiXFlow is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

Thank you for using BiXFlow! We're here to help you succeed.
