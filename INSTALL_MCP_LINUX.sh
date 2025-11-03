#!/bin/bash
# Quick installer for Scarify MCP Server (Linux/Mac)

echo "========================================"
echo " Scarify Empire - MCP Server Installer"
echo "========================================"
echo ""

cd "$(dirname "$0")/mcp-server"

echo "Installing MCP Server..."
echo ""

bash install.sh

echo ""
read -p "Press Enter to exit..."

