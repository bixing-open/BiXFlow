#!/usr/bin/env python3
"""
Demo script for Excel file merging workflow.
"""

import asyncio
from pathlib import Path
from BiXFlow import BiXFlowExecutor

def create_sample_excel_files():
    """Create sample Excel files for testing."""
    try:
        import pandas as pd
    except ImportError:
        print("pandas not installed. Please install it with: pip install pandas openpyxl")
        return False
    
    # Create sample data directory
    sample_dir = Path("sample_excel_files")
    sample_dir.mkdir(exist_ok=True)
    
    # Sample data for first file
    data1 = {
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['New York', 'London', 'Tokyo']
    }
    df1 = pd.DataFrame(data1)
    df1.to_excel(sample_dir / "employees_2023.xlsx", index=False)
    
    # Sample data for second file
    data2 = {
        'Name': ['David', 'Eve', 'Frank'],
        'Age': [28, 32, 29],
        'City': ['Paris', 'Berlin', 'Sydney']
    }
    df2 = pd.DataFrame(data2)
    df2.to_excel(sample_dir / "employees_2024.xlsx", index=False)
    
    # Sample data for third file
    data3 = {
        'Name': ['Grace', 'Henry', 'Ivy'],
        'Age': [27, 31, 26],
        'City': ['Toronto', 'Moscow', 'Dubai']
    }
    df3 = pd.DataFrame(data3)
    df3.to_excel(sample_dir / "employees_2025.xlsx", index=False)
    
    print(f"Created sample Excel files in {sample_dir}/")
    return True

async def run_excel_merge_workflow():
    """Run the Excel merge workflow."""
    # Create BiXFlow executor
    executor = BiXFlowExecutor("mcps/mcp_servers_setting.json")
    
    # Use absolute paths to avoid directory resolution issues
    import os
    project_root = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(project_root)  # Go up one level to project root
    
    # Workflow arguments with absolute paths
    workflow_args = {
        "input_directory": os.path.join(project_root, "sample_excel_files"),
        "output_file": os.path.join(project_root, "merged_employees.xlsx")
    }
    
    print("Running Excel merge workflow...")
    print(f"Input directory: {workflow_args['input_directory']}")
    print(f"Output file: {workflow_args['output_file']}")
    print("-" * 50)
    
    try:
        # Execute workflow
        async for result in executor.execute_workflow(
            "workflows/excel_merge/merge_excel_files_workflow.yaml",
            workflow_args
        ):
            if result['status'] == 'progress':
                print(f"Progress: {result['data']}")
            elif result['status'] == 'done':
                print("Workflow completed successfully!")
                print(f"Final result: {result['data']}")
                break
            elif result['status'] == 'error':
                print(f"Workflow failed: {result['data']}")
                break
    except Exception as e:
        print(f"Error running workflow: {e}")

def main():
    """Main function."""
    print("Excel Merge Workflow Demo")
    print("=" * 50)
    
    # Create sample Excel files
    if not create_sample_excel_files():
        return
    
    # Run the workflow
    asyncio.run(run_excel_merge_workflow())
    
    print("\nDemo completed!")

if __name__ == "__main__":
    main()
