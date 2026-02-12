# Contributing to mcp

Thank you for your interest in contributing to BiXFlow! We welcome contributions from the community and are grateful for any help you can provide.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [Community Guidelines](#community-guidelines)

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Familiarity with Python, YAML, and basic software development practices

### Setting Up Development Environment

1. **Fork and Clone the Repository**

```bash
# Fork the repository on GitHub
# Clone your fork locally
git clone https://github.com/your-username/BiXFlow.git
cd BiXFlow
```

2. **Create a Virtual Environment**

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

3. **Install Development Dependencies**

```bash
# Install the package in development mode with all dev dependencies
pip install -e ".[dev]"
```

4. **Verify Installation**

```bash
# Run tests to ensure everything is set up correctly
python -m pytest tests/ -v
```

## Development Workflow

### 1. Create a Branch

Create a new branch for your contribution:

```bash
# Use a descriptive branch name
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

Branch naming conventions:

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions or changes
- `chore/` - Maintenance tasks

### 2. Make Changes

- Write clear, concise code
- Add comments for complex logic
- Update tests for new functionality
- Update documentation as needed

### 3. Test Your Changes

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_BiXFlow.py -v

# Run tests with coverage
python -m pytest tests/ --cov=BiXFlow --cov-report=html
```

### 4. Commit Your Changes

Write meaningful commit messages following our commit message convention:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build process or auxiliary tool changes

Examples:

```
feat(workflow): add parallel execution support for workflow steps

Add ability to execute multiple workflow steps in parallel when they
don't have dependencies. This improves performance for workflows with
independent steps.

Closes #123
```

```
fix(client): handle connection timeout gracefully

Previously, connection timeouts would cause unhandled exceptions.
Now they are caught and proper error messages are returned.

Fixes #456
```

### 5. Push Your Changes

```bash
# Push to your fork
git push origin feature/your-feature-name
```

### 6. Create a Pull Request

1. Go to the original repository on GitHub
2. Click "New Pull Request"
3. Select your branch from your fork
4. Fill in the PR template:
   - Title should be descriptive
   - Describe what you changed and why
   - Reference related issues
   - Add screenshots if applicable
5. Submit the PR

## Coding Standards

### Python Code Style

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines:

- Use 4 spaces for indentation (no tabs)
- Maximum line length: 88 characters (Black default)
- Use descriptive variable and function names
- Add docstrings to all modules, classes, and functions
- Type hints are recommended for function signatures

### Code Formatting

We use [Black](https://github.com/psf/black) for code formatting:

```bash
# Format all Python files
black BiXFlow/ tests/ examples/
```

### Code Linting

We use [Flake8](https://github.com/PyCQA/flake8) for code quality checks:

```bash
# Lint all Python files
flake8 BiXFlow/ tests/ examples/
```

### Type Checking

We use [mypy](https://github.com/python/mypy) for static type checking:

```bash
# Type check the codebase
mypy BiXFlow/
```

### Code Organization

```
BiXFlow/
├── __init__.py          # Package initialization, public API
├── client.py            # MCP client implementation
├── workflow.py          # Workflow execution logic
├── config.py            # Configuration management
├── utils.py             # Utility functions
├── exceptions.py        # Custom exceptions
└── cli.py               # Command-line interface
```

## Testing

### Test Structure

```
tests/
├── __init__.py
├── test_BiXFlow.py      # Core functionality tests
├── test_mcps.py         # MCP server integration tests
└── test_nested_workflows.py  # Nested workflow tests
```

### Writing Tests

1. Use `pytest` as the testing framework
2. Write descriptive test names
3. Use fixtures for common test data
4. Test both success and failure cases
5. Mock external dependencies (MCP servers, network calls)

Example test:

```python
import pytest
from BiXFlow import BiXFlowExecutor

def test_workflow_execution_basic():
    """Test basic workflow execution."""
    workflow_content = """
    name: test_workflow
    steps:
      - name: test_step
        tool: test_server/test_tool
    """
  
    executor = BiXFlowExecutor({})
    result = executor.run_workflow_from_content_sync(
        workflow_content=workflow_content,
        args={}
    )
  
    assert result is not None
    assert "status" in result
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run with verbose output
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_BiXFlow.py::test_workflow_executor_initialization -v

# Run with coverage
python -m pytest tests/ --cov=BiXFlow --cov-report=html

# Run tests for MCP servers (requires servers running)
python -m pytest tests/test_mcps.py -v
```

### Test Coverage

We aim for at least 80% code coverage. You can view the coverage report:

```bash
# Generate HTML coverage report
python -m pytest tests/ --cov=BiXFlow --cov-report=html
open htmlcov/index.html  # On Linux/Mac
start htmlcov/index.html  # On Windows
```

## Documentation

### Documentation Style

- Use clear, concise language
- Provide code examples
- Use Markdown formatting
- Keep Chinese and English versions in sync

### Updating Documentation

When making changes:

1. Update relevant documentation files
2. Update README.md or README_en.md for user-facing changes
3. Update docs/ files for detailed documentation
4. Add examples for new features
5. Update CHANGELOG.md

### Documentation Files

- `README.md` - Chinese overview and quick start
- `README_en.md` - English overview and quick start
- `docs/index.md` - Documentation index
- `docs/workflow_syntax.md` - Workflow syntax guide (Chinese)
- `docs/workflow_syntax_en.md` - Workflow syntax guide (English)

### Writing Examples

Examples should:

- Be runnable without modifications
- Include necessary imports
- Use realistic data
- Have clear comments
- Demonstrate best practices

## Submitting Changes

### Before Submitting

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages follow convention
- [ ] No merge conflicts with main branch

### Pull Request Checklist

- [ ] Title is descriptive and follows convention
- [ ] Description explains the changes
- [ ] Related issues are referenced
- [ ] Tests are included/updated
- [ ] Documentation is updated
- [ ] CI checks pass
- [ ] Code review requests addressed

### Review Process

1. Maintainers will review your PR
2. They may request changes or clarifications
3. Address feedback promptly
4. Once approved, your PR will be merged

## Community Guidelines

### Getting Help

- Check existing documentation
- Search existing issues
- Ask questions in discussions
- Be patient and respectful

### Reporting Bugs

- Use the issue template
- Provide clear steps to reproduce
- Include error messages and logs
- Specify environment details

### Suggesting Features

- Use the feature request template
- Explain the use case
- Consider implementation feasibility
- Be open to discussion

### Code Review

- Be constructive and respectful
- Focus on code, not the person
- Explain your reasoning
- Accept feedback graciously

## Recognition

Contributors will be recognized in:

- AUTHORS.md file
- Release notes
- Project documentation

Thank you for contributing to BiXFlow! 🎉
