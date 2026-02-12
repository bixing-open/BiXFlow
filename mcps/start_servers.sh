#!/bin/bash

# Script to start MCP servers in batch

# Get the absolute path of the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Server list (using relative paths)
declare -A SERVERS
SERVERS["data_processor_mcp"]="8001:data_processor_mcp/server.py"
SERVERS["monitor_alert_mcp"]="8002:monitor_alert_mcp/server.py"
SERVERS["report_generator_mcp"]="8003:report_generator_mcp/server.py"
SERVERS["excel_processor_mcp"]="8004:excel_processor_mcp/server.py"

PIDS_FILE="/tmp/mcp_server_pids"
SUCCESS_SERVERS=()

# Cleanup function
cleanup() {
    echo -e "\n\n${YELLOW}🛑 Received stop signal, shutting down servers...${NC}"
    
    if [[ -f "$PIDS_FILE" ]]; then
        while IFS= read -r pid; do
            if kill -0 "$pid" 2>/dev/null; then
                kill "$pid"
                echo -e "${GREEN}Stopped PID: $pid${NC}"
            fi
        done < "$PIDS_FILE"
        rm -f "$PIDS_FILE"
    fi
    
    echo -e "${GREEN}✅ All servers stopped${NC}"
    exit 0
}

# Register cleanup function
trap cleanup SIGINT SIGTERM

# Main function
main() {
    echo "" > "$PIDS_FILE"
    
    # Start all servers
    for name in "${!SERVERS[@]}"; do
        IFS=':' read -r port relative_file <<< "${SERVERS[$name]}"
        # Build the complete absolute path
        file="${SCRIPT_DIR}/${relative_file}"
        
        if [[ -f "$file" ]]; then
            echo -e "${YELLOW}🚀 Starting ${name} server (port: ${port})...${NC}"
            
            python "$file" \
                --port "$port" \
                --host "127.0.0.1" \
                --transport "streamable_http" \
                > "/tmp/${name}.log" 2>&1 &
            
            pid=$!
            
            # Wait for server to start
            sleep 3
            
            if kill -0 "$pid" 2>/dev/null; then
                echo "$pid" >> "$PIDS_FILE"
                echo -e "${GREEN}✅ ${name} server started (PID: $pid)${NC}"
                # Record successfully started server
                SUCCESS_SERVERS+=("$name:$port")
            else
                echo -e "${RED}❌ ${name} server failed to start${NC}"
                echo "Please check /tmp/${name}.log for details"
            fi
        else
            echo -e "${RED}❌ File not found: $file${NC}"
        fi
    done
    
    # Display information based on actual startup results
    echo
    echo "=================================================="
    if [ ${#SUCCESS_SERVERS[@]} -gt 0 ]; then
        echo "Successfully started MCP servers:"
        counter=1
        for server in "${SUCCESS_SERVERS[@]}"; do
            IFS=':' read -r name port <<< "$server"
            case $name in
                "data_processor_mcp")
                    echo "  $counter. Data Processing Service: http://localhost:$port"
                    ;;
                "monitor_alert_mcp")
                    echo "  $counter. Monitoring Alert Service: http://localhost:$port"
                    ;;
                "report_generator_mcp")
                    echo "  $counter. Report Generation Service: http://localhost:$port"
                    ;;
                "excel_processor_mcp")
                    echo "  $counter. Excel Processing Service: http://localhost:$port"
                    ;;
            esac
            ((counter++))
        done
    else
        echo "No servers started successfully"
    fi
    echo
    echo "Configuration file path: ${SCRIPT_DIR}/mcp_servers_setting.json"
    echo "=================================================="
    echo
    echo "Press Ctrl+C to stop all servers..."
    
    # Keep main process running
    while true; do
        sleep 1
    done
}

# Run main function
main
