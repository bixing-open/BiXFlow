import time
import random
from datetime import datetime
from typing import Dict, List
from mcp.server.fastmcp import FastMCP

# Create monitoring and alerting MCP server instance
monitor_alert_mcp = FastMCP(
    name="monitor_alert_mcp",
    instructions="System monitoring and alerting service, providing API health checks, response time logging, and alert sending functions"
)

@monitor_alert_mcp.tool(
    name="api_checker",
    description="Check the health status and response time of API endpoints"
)
def api_checker(endpoint: str, timeout: int = 30, expected_status: int = 200) -> Dict:
    """Check API endpoint health status"""
    try:
        # Simulate API check
        time.sleep(0.1)
        
        is_healthy = random.random() > 0.15
        response_time = random.randint(50, 500)
        
        return {
            'endpoint': endpoint,
            'timestamp': datetime.now().isoformat(),
            'status': 'healthy' if is_healthy else 'unhealthy',
            'response_time_ms': response_time,
            'status_code': expected_status if is_healthy else random.choice([500, 503, 404])
        }
    except Exception as e:
        return {
            "status": 'error',
            "message": f"API check failed: {str(e)}"
        }

@monitor_alert_mcp.tool(
    name="response_logger",
    description="Record and analyze API response time metrics for monitoring"
)
def response_logger(endpoint: str, sample_count: int = 3) -> Dict:
    """Record API response time metrics"""
    try:
        response_times = []
        
        # Take multiple samples to get average response time
        for i in range(sample_count):
            start_time = time.time()
            time.sleep(random.uniform(0.02, 0.15))
            response_time = (time.time() - start_time) * 1000
            response_times.append(response_time)
        
        # Calculate statistics
        avg_response_time = round(sum(response_times) / len(response_times), 2)
        min_response_time = round(min(response_times), 2)
        max_response_time = round(max(response_times), 2)
        
        # Determine performance status
        performance_status = 'good'
        if avg_response_time > 1000:
            performance_status = 'poor'
        elif avg_response_time > 500:
            performance_status = 'warning'
        
        return {
            'endpoint': endpoint,
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'sample_count': sample_count,
                'avg_response_time': avg_response_time,
                'min_response_time': min_response_time,
                'max_response_time': max_response_time,
                'performance_status': performance_status,
                'success_rate': 100.0  # Since we're just timing, assume success
            },
            'detailed_results': [
                {
                    'request_id': i + 1,
                    'response_time_ms': round(response_times[i], 2)
                }
                for i in range(sample_count)
            ]
        }
    except Exception as e:
        return {
            "status": 'error',
            "message": f"Response logging failed: {str(e)}"
        }

@monitor_alert_mcp.tool(
    name="alert_sender",
    description="Send system alerts and notification messages"
)
def alert_sender(report: Dict, recipients: List[str], severity: str = "warning") -> Dict:
    """Send system alerts"""
    try:
        healthy_endpoints = report.get('system_status', {}).get('healthy_endpoints', 0)
        total_endpoints = report.get('system_status', {}).get('total_endpoints', 0)
        
        return {
            'alert_id': f"alert_{int(datetime.now().timestamp())}",
            'sent_at': datetime.now().isoformat(),
            'severity': severity,
            'recipients': recipients,
            'content': {
                'health_status': f"{healthy_endpoints}/{total_endpoints} endpoints healthy",
                'issues_count': len(report.get('identified_issues', [])),
                'recommendations': report.get('recommendations', [])
            },
            'delivery_status': 'simulated_success'
        }
    except Exception as e:
        return {
            "status": 'error',
            "message": f"Alert sending failed: {str(e)}"
        }

# Main function to start the server
if __name__ == "__main__":
    import uvicorn
    import argparse
    
    parser = argparse.ArgumentParser(description="Start monitor alert MCP server")
    parser.add_argument("--port", type=int, default=8002, help="Server port")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Server host address")
    parser.add_argument("--transport", type=str, choices=['stdio', 'sse', 'streamable_http'], 
                       default='streamable_http', help="Transport protocol")
    
    args = parser.parse_args()
    
    if args.transport == 'streamable_http':
        app = monitor_alert_mcp.streamable_http_app()
        print(f"Starting monitor alert MCP server on {args.host}:{args.port}")
        uvicorn.run(app, host=args.host, port=args.port)
    elif args.transport == 'sse':
        app = monitor_alert_mcp.sse_app()
        print(f"Starting monitor alert MCP server on {args.host}:{args.port}")
        uvicorn.run(app, host=args.host, port=args.port)
    else:
        print("Starting monitor alert MCP server with stdio transport")
        import asyncio
        asyncio.run(monitor_alert_mcp.run_stdio_async())
