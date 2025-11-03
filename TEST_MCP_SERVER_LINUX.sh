#!/bin/bash
# Quick test launcher for Scarify MCP Server (Linux/Mac)

echo "========================================"
echo " Scarify Empire - MCP Server Test"
echo "========================================"
echo ""

cd "$(dirname "$0")/mcp-server"

echo "Testing MCP Server..."
echo ""

bash test-server.sh

echo ""
read -p "Press Enter to exit..."

