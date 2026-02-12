import statistics
from typing import List, Dict
from mcp.server.fastmcp import FastMCP

# Create data processing and statistics MCP server instance
data_processor_mcp = FastMCP(
    name="data_processor_mcp",
    instructions="Data processing and statistical analysis service, providing data validation, cleaning, basic statistics, and advanced analysis functions"
)

@data_processor_mcp.tool(
    name="validator",
    description="Validate data format and integrity, check required fields and type constraints"
)
def data_validator(data: List[Dict], rules: Dict) -> Dict:
    """Validate data format and integrity"""
    try:
        issues = []
        valid_count = 0
        
        for i, item in enumerate(data):
            item_issues = []
            
            # Check required fields
            for field in rules.get('required_fields', []):
                if field not in item:
                    item_issues.append(f"Missing required field: {field}")
            
            # Check field types
            for field, expected_type in rules.get('field_types', {}).items():
                if field in item:
                    actual_type = type(item[field]).__name__
                    if actual_type != expected_type:
                        item_issues.append(f"Field {field} type error: expected {expected_type}, actual {actual_type}")
            
            if not item_issues:
                valid_count += 1
            else:
                issues.append({
                    'index': i,
                    'item': item,
                    'issues': item_issues
                })
        
        return {
            'valid': len(issues) == 0,
            'valid_count': valid_count,
            'total_count': len(data),
            'issues': issues,
            'validity_rate': valid_count / len(data) if data else 0
        }
    except Exception as e:
        return {
            "status": 'error',
            "message": f"Data validation failed: {str(e)}"
        }

@data_processor_mcp.tool(
    name="cleaner",
    description="Clean data based on validation results, fix common data issues"
)
def data_cleaner(raw_data: List[Dict], issues: List[Dict]) -> Dict:
    """Clean data based on validation results"""
    try:
        cleaned_data = raw_data.copy()
        fixes_applied = 0
        
        for issue in issues:
            idx = issue['index']
            for problem in issue['issues']:
                if 'Missing required field' in problem:
                    field = problem.split(': ')[1]
                    cleaned_data[idx][field] = None
                    fixes_applied += 1
                elif 'type error' in problem:
                    field = problem.split(' ')[1]
                    original_value = cleaned_data[idx][field]
                    try:
                        if 'int' in problem:
                            cleaned_data[idx][field] = int(original_value)
                        elif 'float' in problem:
                            cleaned_data[idx][field] = float(original_value)
                        fixes_applied += 1
                    except:
                        cleaned_data[idx][field] = None
        
        return {
            'original_count': len(raw_data),
            'cleaned_count': len(cleaned_data),
            'cleaned_data': cleaned_data,
            'fixes_applied': fixes_applied
        }
    except Exception as e:
        return {
            "status": 'error',
            "message": f"Data cleaning failed: {str(e)}"
        }

@data_processor_mcp.tool(
    name="analyzer",
    description="Perform statistical analysis, calculate basic statistics and detect anomalies"
)
def stats_analyzer(data: List[Dict], metrics: List[str]) -> Dict:
    """Perform statistical analysis"""
    try:
        if not data:
            return {'count': 0, 'message': 'Empty dataset'}
        
        results = {'count': len(data)}
        
        # Identify numeric fields
        numeric_fields = []
        if data:
            numeric_fields = [k for k, v in data[0].items() 
                            if isinstance(v, (int, float)) and not k.startswith('_')]
        
        # Basic statistics
        for field in numeric_fields:
            field_results = {}
            values = [item.get(field) for item in data if item.get(field) is not None]
            values = [v for v in values if isinstance(v, (int, float))]
            
            if not values:
                continue
                
            if 'mean' in metrics:
                field_results['mean'] = statistics.mean(values)
            if 'median' in metrics:
                field_results['median'] = statistics.median(values)
            if 'std' in metrics and len(values) > 1:
                field_results['std'] = statistics.stdev(values)
            if 'min' in metrics:
                field_results['min'] = min(values)
            if 'max' in metrics:
                field_results['max'] = max(values)
            
            if field_results:
                results[field] = field_results
        
        # Anomaly detection
        anomalies = []
        for field in numeric_fields:
            values = [item.get(field) for item in data if item.get(field) is not None]
            values = [v for v in values if isinstance(v, (int, float))]
            
            if len(values) >= 3:
                q1 = statistics.quantiles(values, n=4)[0]
                q3 = statistics.quantiles(values, n=4)[2]
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                
                for i, value in enumerate(values):
                    if value < lower_bound or value > upper_bound:
                        anomalies.append({
                            'field': field,
                            'index': i,
                            'value': value,
                            'bounds': {'lower': lower_bound, 'upper': upper_bound}
                        })
        
        if anomalies:
            results['anomalies'] = anomalies
            results['anomaly_count'] = len(anomalies)
        
        return results
    except Exception as e:
        return {
            "status": 'error',
            "message": f"Statistical analysis failed: {str(e)}"
        }

# Main function to start the server
if __name__ == "__main__":
    import uvicorn
    import argparse
    
    parser = argparse.ArgumentParser(description="Start data processor MCP server")
    parser.add_argument("--port", type=int, default=8001, help="Server port")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Server host address")
    parser.add_argument("--transport", type=str, choices=['stdio', 'sse', 'streamable_http'], 
                       default='streamable_http', help="Transport protocol")
    
    args = parser.parse_args()
    
    if args.transport == 'streamable_http':
        app = data_processor_mcp.streamable_http_app()
        print(f"Starting data processor MCP server on {args.host}:{args.port}")
        uvicorn.run(app, host=args.host, port=args.port)
    elif args.transport == 'sse':
        app = data_processor_mcp.sse_app()
        print(f"Starting data processor MCP server on {args.host}:{args.port}")
        uvicorn.run(app, host=args.host, port=args.port)
    else:
        print("Starting data processor MCP server with stdio transport")
        import asyncio
        asyncio.run(data_processor_mcp.run_stdio_async())
