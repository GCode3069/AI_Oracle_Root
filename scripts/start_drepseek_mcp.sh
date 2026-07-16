#!/bin/bash

# Drepseek MCP Start Script
# Quick script to start the Drepseek MCP server with proper environment

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Determine project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo ""
echo "🚀 Starting Drepseek MCP Server..."
echo ""

# Load environment variables
if [ -f ".env.drepseek" ]; then
    print_info "Loading environment from .env.drepseek"
    set -a
    source .env.drepseek
    set +a
    print_success "Environment loaded"
else
    print_warning ".env.drepseek not found, using default configuration"
fi

# Verify API key
if [ -z "$DREPSEEK_API_KEY" ] || [ "$DREPSEEK_API_KEY" = "your_api_key_here" ]; then
    echo ""
    print_warning "DREPSEEK_API_KEY is not set!"
    echo ""
    echo "Please set your API key:"
    echo "  1. Edit .env.drepseek and add your API key"
    echo "  2. Or export it: export DREPSEEK_API_KEY=your_key"
    echo ""
    exit 1
fi

# Create logs directory if it doesn't exist
mkdir -p logs

# Determine Python command
PYTHON_CMD=$(command -v python3 || command -v python)

# Check if server file exists
if [ ! -f "mcp_server/drepseek_mcp_server.py" ]; then
    print_warning "Server file not found!"
    exit 1
fi

# Start the server
print_info "Starting server at $(date)"
print_info "Log level: ${LOG_LEVEL:-info}"
print_info "Network: ${DREPSEEK_NETWORK:-mainnet}"
echo ""

# Run the server
$PYTHON_CMD mcp_server/drepseek_mcp_server.py

# This will only be reached if the server exits
echo ""
print_info "Server stopped at $(date)"
