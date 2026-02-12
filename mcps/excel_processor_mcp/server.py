import os
import pandas as pd
from typing import List, Dict
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Create Excel processing MCP server instance
excel_processor_mcp = FastMCP(
    name="excel_processor_mcp",
    instructions="Excel file processing service, providing Excel file reading, writing, merging, and data manipulation functions"
)

@excel_processor_mcp.tool(
    name="list_excel_files",
    description="List all Excel files in a directory"
)
def list_excel_files(directory: str) -> Dict:
    """List all Excel files in a directory"""
    try:
        # Convert to Path object
        dir_path = Path(directory)
        
        # If it's not an absolute path, make it relative to the current working directory
        if not dir_path.is_absolute():
            dir_path = Path.cwd() / directory
        
        # Resolve to absolute path
        dir_path = dir_path.resolve()
        
        # Check if directory exists
        if not dir_path.exists():
            return {
                "status": 'error',
                "message": f"Directory does not exist: {directory} (resolved to: {dir_path})"
            }
        
        if not dir_path.is_dir():
            return {
                "status": 'error',
                "message": f"Path is not a directory: {directory}"
            }
        
        excel_extensions = ['.xlsx', '.xls']
        excel_files = []
        
        for file_path in dir_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in excel_extensions:
                excel_files.append(str(file_path.absolute()))
        
        return {
            "status": 'success',
            "files": sorted(excel_files),
            "count": len(excel_files)
        }
    except Exception as e:
        return {
            "status": 'error',
            "message": f"Failed to list Excel files: {str(e)}"
        }

@excel_processor_mcp.tool(
    name="read_excel",
    description="Read data from an Excel file"
)
def read_excel(file_path: str, sheet_name: str = None) -> Dict:
    """Read data from an Excel file"""
    try:
        if not os.path.exists(file_path):
            return {
                "status": 'error',
                "message": f"File does not exist: {file_path}"
            }
        
        # Read Excel file
        if sheet_name:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
        else:
            df = pd.read_excel(file_path)
        
        # Convert DataFrame to list of dictionaries
        data = df.to_dict('records')
        
        return {
            "status": 'success',
            "file_path": file_path,
            "sheet_name": sheet_name or "Sheet1",
            "rows": len(data),
            "columns": len(df.columns) if len(data) > 0 else 0,
            "data": data,
            "column_names": list(df.columns)
        }
    except Exception as e:
        return {
            "status": 'error',
            "message": f"Failed to read Excel file: {str(e)}"
        }

@excel_processor_mcp.tool(
    name="merge_excel_files",
    description="Merge multiple Excel files into a single Excel file"
)
def merge_excel_files(file_paths: List[str], output_path: str, sheet_name: str = "MergedData") -> Dict:
    """Merge multiple Excel files into a single Excel file"""
    try:
        merged_data = []
        file_info = []
        
        # Read data from all Excel files
        for file_path in file_paths:
            if not os.path.exists(file_path):
                return {
                    "status": 'error',
                    "message": f"File does not exist: {file_path}"
                }
            
            try:
                # Read Excel file
                df = pd.read_excel(file_path)
                
                # Add source file column
                df['source_file'] = os.path.basename(file_path)
                
                # Convert to dictionary and add to merged data
                data = df.to_dict('records')
                merged_data.extend(data)
                
                # Record file info
                file_info.append({
                    "file": file_path,
                    "rows": len(data),
                    "columns": len(df.columns)
                })
            except Exception as e:
                return {
                    "status": 'error',
                    "message": f"Failed to read Excel file {file_path}: {str(e)}"
                }
        
        # Create DataFrame from merged data
        merged_df = pd.DataFrame(merged_data)
        
        # Write merged data to output file
        merged_df.to_excel(output_path, sheet_name=sheet_name, index=False)
        
        return {
            "status": 'success',
            "output_file": output_path,
            "total_rows": len(merged_data),
            "total_files": len(file_paths),
            "file_info": file_info
        }
    except Exception as e:
        return {
            "status": 'error',
            "message": f"Failed to merge Excel files: {str(e)}"
        }

@excel_processor_mcp.tool(
    name="write_excel",
    description="Write data to an Excel file"
)
def write_excel(data: List[Dict], file_path: str, sheet_name: str = "Sheet1") -> Dict:
    """Write data to an Excel file"""
    try:
        # Create DataFrame from data
        df = pd.DataFrame(data)
        
        # Write to Excel file
        df.to_excel(file_path, sheet_name=sheet_name, index=False)
        
        return {
            "status": 'success',
            "file_path": file_path,
            "rows": len(data),
            "columns": len(df.columns) if len(data) > 0 else 0
        }
    except Exception as e:
        return {
            "status": 'error',
            "message": f"Failed to write Excel file: {str(e)}"
        }

@excel_processor_mcp.tool(
    name="filter_data",
    description="Filter data based on specified criteria"
)
def filter_data(data: List[Dict], filter_conditions: Dict) -> Dict:
    """Filter data based on specified criteria"""
    try:
        filtered_data = []
        
        for row in data:
            match = True
            for column, condition in filter_conditions.items():
                if column not in row:
                    match = False
                    break
                
                value = row[column]
                
                # Handle different condition types
                if isinstance(condition, dict):
                    if 'equals' in condition and value != condition['equals']:
                        match = False
                    elif 'contains' in condition and isinstance(value, str) and condition['contains'] not in value:
                        match = False
                    elif 'greater_than' in condition and isinstance(value, (int, float)) and value <= condition['greater_than']:
                        match = False
                    elif 'less_than' in condition and isinstance(value, (int, float)) and value >= condition['less_than']:
                        match = False
                elif value != condition:
                    match = False
            
            if match:
                filtered_data.append(row)
        
        return {
            "status": 'success',
            "original_count": len(data),
            "filtered_count": len(filtered_data),
            "data": filtered_data
        }
    except Exception as e:
        return {
            "status": 'error',
            "message": f"Failed to filter data: {str(e)}"
        }

# Main function to start the server
if __name__ == "__main__":
    import uvicorn
    import argparse
    
    parser = argparse.ArgumentParser(description="Start Excel processor MCP server")
    parser.add_argument("--port", type=int, default=8004, help="Server port")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Server host address")
    parser.add_argument("--transport", type=str, choices=['stdio', 'sse', 'streamable_http'], 
                       default='streamable_http', help="Transport protocol")
    
    args = parser.parse_args()
    
    if args.transport == 'streamable_http':
        app = excel_processor_mcp.streamable_http_app()
        print(f"Starting Excel processor MCP server on {args.host}:{args.port}")
        uvicorn.run(app, host=args.host, port=args.port)
    elif args.transport == 'sse':
        app = excel_processor_mcp.sse_app()
        print(f"Starting Excel processor MCP server on {args.host}:{args.port}")
        uvicorn.run(app, host=args.host, port=args.port)
    else:
        print("Starting Excel processor MCP server with stdio transport")
        import asyncio
        asyncio.run(excel_processor_mcp.run_stdio_async())
