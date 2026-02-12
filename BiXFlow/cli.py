"""Command-line interface for BiXFlow."""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

from BiXFlow import run_workflow_from_file_sync, run_workflow_from_content_sync, __version__


def load_args_from_json(json_str: str) -> Dict[str, Any]:
    """Load arguments from JSON string."""
    try:
        # Handle escaped quotes in command line arguments
        if '\\"' in json_str:
            json_str = json_str.replace('\\"', '"')
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON for arguments: {e}")


def print_table_result(result: Dict[str, Any]) -> None:
    """Print result in table format."""
    if result.get('status') == 'done':
        print("Workflow Execution Result:")
        print("=" * 50)
        print(f"Status: {result.get('status', 'N/A')}")
        print(f"Message: {result.get('message', 'N/A')}")
        
        data = result.get('data', {})
        if isinstance(data, dict):
            print("\nData:")
            for key, value in data.items():
                print(f"  {key}: {value}")
        else:
            print(f"\nData: {data}")
    else:
        print("Workflow Execution Result:")
        print("=" * 50)
        print(f"Status: {result.get('status', 'N/A')}")
        print(f"Data: {result.get('data', 'N/A')}")


def print_simple_workflows(workflows_dir: Path) -> None:
    """Print workflows in simple format."""
    print("Available workflows:")
    for service_dir in workflows_dir.iterdir():
        if service_dir.is_dir():
            print(f"  Service: {service_dir.name}")
            for workflow_file in service_dir.glob("*.yaml"):
                workflow_name = workflow_file.stem
                print(f"    - {workflow_name}")


def print_detailed_workflows(workflows_dir: Path) -> None:
    """Print workflows in detailed format."""
    print("Available workflows (detailed):")
    for service_dir in workflows_dir.iterdir():
        if service_dir.is_dir():
            print(f"\nService: {service_dir.name}")
            print("-" * (len(service_dir.name) + 9))
            for workflow_file in service_dir.glob("*.yaml"):
                workflow_name = workflow_file.stem
                # Try to read workflow file to get description
                try:
                    with open(workflow_file, 'r', encoding='utf-8') as f:
                        import yaml
                        workflow_content = yaml.safe_load(f)
                        description = workflow_content.get('description', 'No description')
                        display_name = workflow_content.get('display_name', workflow_name)
                        print(f"  {workflow_name}:")
                        print(f"    Display Name: {display_name}")
                        print(f"    Description: {description}")
                except Exception:
                    print(f"  {workflow_name}:")
                    print(f"    Display Name: {workflow_name}")
                    print(f"    Description: No description available")


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="BiXFlow - Execute workflows through Model Context Protocol servers",
        prog="BiXFlow"
    )
    
    # Add version argument
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    
    # Global options
    parser.add_argument(
        "--format",
        choices=["json", "table"],
        default="json",
        help="Output format (default: json)"
    )
    parser.add_argument(
        "--verbose", "-V",
        action="store_true",
        help="Enable verbose output"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Run named workflow command
    run_named_parser = subparsers.add_parser(
        "run-named", 
        help="Run a named workflow from the standard workflows directory"
    )
    run_named_parser.add_argument(
        "service_name", 
        help="Name of the service directory under workflows/"
    )
    run_named_parser.add_argument(
        "workflow_name", 
        help="Name of the workflow (without .yaml extension)"
    )
    run_named_parser.add_argument(
        "--args", 
        help="JSON string of arguments to pass to the workflow"
    )
    run_named_parser.add_argument(
        "--config", 
        help="Path to the MCP servers configuration file"
    )
    
    # Run workflow from file command
    run_parser = subparsers.add_parser(
        "run", 
        help="Run a workflow from a YAML file"
    )
    run_parser.add_argument(
        "workflow_path", 
        help="Path to the workflow YAML file"
    )
    run_parser.add_argument(
        "--args", 
        help="JSON string of arguments to pass to the workflow"
    )
    run_parser.add_argument(
        "--config", 
        help="Path to the MCP servers configuration file"
    )
    
    # Run workflow from content command
    run_content_parser = subparsers.add_parser(
        "run-content", 
        help="Run a workflow from YAML content"
    )
    run_content_parser.add_argument(
        "workflow_content", 
        help="YAML content defining the workflow"
    )
    run_content_parser.add_argument(
        "--args", 
        help="JSON string of arguments to pass to the workflow"
    )
    run_content_parser.add_argument(
        "--config", 
        help="Path to the MCP servers configuration file or JSON string"
    )
    
    # List workflows command
    list_parser = subparsers.add_parser(
        "list-workflows", 
        help="List available workflows"
    )
    list_parser.add_argument(
        "--format",
        choices=["simple", "detailed"],
        default="simple",
        help="Output format for workflow list (default: simple)"
    )
    
    args = parser.parse_args()
    
    try:
        # Handle global verbose option
        if args.verbose:
            print(f"Running BiXFlow CLI version {__version__}")
        
        if args.command == "run":
            # Parse arguments if provided
            workflow_args = {}
            if args.args:
                workflow_args = load_args_from_json(args.args)
            
            # Run the workflow
            result = run_workflow_from_file_sync(
                workflow_path=args.workflow_path,
                mcp_config=args.config,
                args=workflow_args
            )
            
            # Print result based on format
            if args.format == "table":
                print_table_result(result)
            else:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            
        elif args.command == "run-content":
            # Parse arguments if provided
            workflow_args = {}
            if args.args:
                workflow_args = load_args_from_json(args.args)
            
            # Parse config if provided as JSON string
            config = args.config
            if config and config.startswith('{') and config.endswith('}'):
                try:
                    config = json.loads(config)
                except json.JSONDecodeError:
                    # If it's not valid JSON, treat as file path
                    pass
            
            # Process escape sequences in workflow content
            workflow_content = args.workflow_content.encode().decode('unicode_escape')
            
            # Run the workflow
            result = run_workflow_from_content_sync(
                workflow_content=workflow_content,
                mcp_config=config,
                args=workflow_args
            )
            
            # Print result based on format
            if args.format == "table":
                print_table_result(result)
            else:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            
        elif args.command == "list-workflows":
            # List available workflows
            workflows_dir = Path("workflows")
            if workflows_dir.exists():
                if args.format == "detailed":
                    print_detailed_workflows(workflows_dir)
                else:
                    print_simple_workflows(workflows_dir)
            else:
                print("No workflows directory found.")
        else:
            parser.print_help()
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
