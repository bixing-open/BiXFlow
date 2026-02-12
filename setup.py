"""Setup script for BiXFlow package."""

from setuptools import setup, find_packages

# Read the contents of README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="BiXFlow",
    version="0.9.0",
    author="Bixing Development Team, China Mobile Research Institute",
    author_email="bixing_support@chinamobile.com",
    description="A framework for executing agentic workflows through Model Context Protocol servers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-organization/BiXFlow",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Distributed Computing",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires=">=3.8",
    keywords="workflow mcp model-context-protocol agent orchestration automation",
    project_urls={
        "Bug Reports": "https://github.com/your-organization/BiXFlow/issues",
        "Source": "https://github.com/your-organization/BiXFlow",
        "Documentation": "https://github.com/your-organization/BiXFlow/tree/main/docs",
        "Changelog": "https://github.com/your-organization/BiXFlow/blob/main/CHANGELOG.md",
    },
    install_requires=[
        "mcp>=1.0.0",
        "uvicorn>=0.24.0",
        "httpx>=0.25.0",
        "jinja2>=3.0.0",
        "pyyaml>=6.0.0",
        "pandas>=1.5.0",
        "openpyxl>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio>=0.18.0",
            "black>=22.0",
            "flake8>=4.0",
            "build>=0.10.0",
            "twine>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "BiXFlow=BiXFlow.cli:main",
        ],
    },
)
