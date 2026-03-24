import json
import os
from datetime import datetime
from typing import Dict, List
from mcp.server.fastmcp import FastMCP
from BiXFlow import MCPClient

# Create report generation MCP server instance
report_generator_mcp = FastMCP(
    name="report_generator_mcp",
    instructions="Report generation service, providing data reports, health reports, and formatted output functions"
)

@report_generator_mcp.tool(
    name="comprehensive_analyzer",
    description="Execute comprehensive data analysis workflow, including data cleaning, analysis, and report generation"
)
async def comprehensive_analyzer(
    raw_data: List[Dict], 
    validation_rules: Dict = None,
    api_endpoints: List[str] = None
) -> Dict:
    """Execute comprehensive data analysis workflow"""
    try:
        # Get the directory where the current file is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        workflow_path = os.path.join(current_dir, "workflows", "comprehensive_analysis_workflow.yaml")
        
        # Check if workflow file exists
        if not os.path.exists(workflow_path):
            return {
                "status": 'error',
                "message": f"Workflow file does not exist: {workflow_path}"
            }
        
        # Create MCP client
        mcp_config = {
            "data_processor_mcp": {
                "url": "http://127.0.0.1:8001/mcp",
                "transport": "streamable_http"
            },
            "monitor_alert_mcp": {
                "url": "http://127.0.0.1:8002/mcp",
                "transport": "streamable_http"
            },
            "report_generator_mcp": {
                "url": "http://127.0.0.1:8003/mcp",
                "transport": "streamable_http"
            }
        }
        
        client = MCPClient(mcp_config)
        
        # Prepare workflow arguments
        workflow_args = {
            "raw_data": raw_data,
            "validation_rules": validation_rules or {},
            "api_endpoints": api_endpoints or []
        }
        
        # Execute workflow
        final_result = None
        error_occurred = False
        error_message = ""
        
        # Execute workflow asynchronously
        try:
            async for result in client.execute_workflow(workflow_path, workflow_args):
                if result['status'] == 'done':
                    final_result = result['data']
                elif result['status'] == 'error':
                    error_occurred = True
                    error_message = result['data']
        except Exception as e:
            error_occurred = True
            error_message = str(e)
        
        if error_occurred:
            return {
                "status": 'error',
                "message": f"Workflow execution failed: {error_message}"
            }
        
        return {
            "status": 'done',
            "data": final_result
        }
    except Exception as e:
        return {
            "status": 'error',
            "message": f"Comprehensive analysis failed: {str(e)}"
        }

@report_generator_mcp.tool(
    name="generator",
    description="Generate comprehensive analysis report, integrating validation, statistics, and monitoring data"
)
def report_generator(basic_stats: Dict, anomalies: Dict, validation_result: Dict) -> Dict:
    """Generate comprehensive analysis report"""
    try:
        report = {
            'report_id': f"report_{int(datetime.now().timestamp())}",
            'generated_at': datetime.now().isoformat(),
            'execution_summary': {
                'data_quality': validation_result.get('valid', False),
                'total_records': validation_result.get('total_count', 0),
                'valid_records': validation_result.get('valid_count', 0),
                'anomalies_detected': anomalies.get('anomaly_count', 0)
            },
            'statistical_insights': basic_stats,
            'anomaly_analysis': anomalies
        }
        
        # Generate quality score
        quality_score = 80
        if validation_result.get('valid', False):
            quality_score += 10
        if anomalies.get('anomaly_count', 0) == 0:
            quality_score += 10
        
        report['quality_assessment'] = {
            'overall_score': min(quality_score, 100),
            'rating': 'Excellent' if quality_score >= 90 else 'Good' if quality_score >= 80 else 'Average'
        }
        
        return report
    except Exception as e:
        return {
            "status": 'error',
            "message": f"Report generation failed: {str(e)}"
        }

@report_generator_mcp.tool(
    name="health_reporter",
    description="Generate system health status report"
)
def health_reporter(status_results: list[Dict], performance_data: Dict) -> Dict:
    """Generate system health status report"""
    try:
        healthy_endpoints = sum(1 for result in status_results 
                              if result.get('status') == 'healthy')
        total_endpoints = len(status_results) if status_results else 0
        
        # Analyze performance issues
        performance_issues = []
        avg_response_time = performance_data.get('summary', {}).get('avg_response_time', 0)
        performance_status = performance_data.get('summary', {}).get('performance_status', 'good')
        
        # Check response time issues
        if avg_response_time > 1000:
            performance_issues.append(f"Response time too high: {avg_response_time}ms")
        elif avg_response_time > 500:
            performance_issues.append(f"Response time elevated: {avg_response_time}ms")
        
        # Check performance status
        if performance_status == 'poor':
            performance_issues.append("Poor performance detected")
        elif performance_status == 'warning':
            performance_issues.append("Performance degradation warning")
        
        # Check if we have response data
        if not performance_data or not performance_data.get('summary'):
            performance_issues.append("No response time data available")
        
        return {
            'report_type': 'health_monitoring',
            'timestamp': datetime.now().isoformat(),
            'system_status': {
                'total_endpoints': total_endpoints,
                'healthy_endpoints': healthy_endpoints,
                'availability_rate': round(healthy_endpoints / total_endpoints * 100, 2) if total_endpoints > 0 else 0,
                'overall_health': 'Healthy' if healthy_endpoints == total_endpoints and not performance_issues else 'Warning'
            },
            'performance_metrics': performance_data.get('summary', {}),
            'identified_issues': performance_issues,
            'recommendations': [
                'All endpoints running normally' if healthy_endpoints == total_endpoints else f'{total_endpoints - healthy_endpoints} endpoints need attention',
                'Performance metrics within normal range' if not performance_issues else f'Performance {performance_status} - needs attention' if performance_status != 'good' else 'Performance needs optimization'
            ]
        }
    except Exception as e:
        return {
            "status": 'error',
            "message": f"Health report generation failed: {str(e)}"
        }

@report_generator_mcp.tool(
    name="formatter",
    description="Format report data into specified format"
)
def report_formatter(report_data: Dict, format: str = "markdown") -> Dict:
    """Format report data"""
    try:
        if format == "json":
            return {
                'format': 'json',
                'content': json.dumps(report_data, indent=2, ensure_ascii=False)
            }
        elif format == "markdown":
            markdown_content = f"# Analysis Report\n\n"
            markdown_content += f"**Generated at:** {report_data.get('generated_at', 'N/A')}\n\n"
            
            if 'execution_summary' in report_data:
                summary = report_data['execution_summary']
                markdown_content += f"## Execution Summary\n\n"
                markdown_content += f"- Total records: {summary.get('total_records', 0)}\n"
                markdown_content += f"- Valid records: {summary.get('valid_records', 0)}\n"
                markdown_content += f"- Data quality: {'✅ Good' if summary.get('data_quality') else '⚠️ Needs improvement'}\n"
                markdown_content += f"- Anomalies detected: {summary.get('anomalies_detected', 0)}\n\n"
            
            if 'quality_assessment' in report_data:
                assessment = report_data['quality_assessment']
                markdown_content += f"## Quality Assessment\n\n"
                markdown_content += f"**Overall score:** {assessment.get('overall_score', 0)}/100 ({assessment.get('rating', 'N/A')})\n\n"
            
            return {
                'format': 'markdown',
                'content': markdown_content
            }
        else:
            return {
                'format': 'raw',
                'content': report_data
            }
    except Exception as e:
        return {
            "status": 'error',
            "message": f"Report formatting failed: {str(e)}"
        }

# Main function to start the server
if __name__ == "__main__":
    import uvicorn
    import argparse
    
    parser = argparse.ArgumentParser(description="Start report generator MCP server")
    parser.add_argument("--port", type=int, default=8003, help="Server port")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Server host address")
    parser.add_argument("--transport", type=str, choices=['stdio', 'sse', 'streamable_http'], 
                       default='streamable_http', help="Transport protocol")
    
    args = parser.parse_args()
    
    if args.transport == 'streamable_http':
        app = report_generator_mcp.streamable_http_app()
        print(f"Starting report generator MCP server on {args.host}:{args.port}")
        uvicorn.run(app, host=args.host, port=args.port)
    elif args.transport == 'sse':
        app = report_generator_mcp.sse_app()
        print(f"Starting report generator MCP server on {args.host}:{args.port}")
        uvicorn.run(app, host=args.host, port=args.port)
    else:
        print("Starting report generator MCP server with stdio transport")
        import asyncio
        asyncio.run(report_generator_mcp.run_stdio_async())
