@echo off
REM Quick test launcher for Scarify MCP Server

echo ========================================
echo  Scarify Empire - MCP Server Test
echo ========================================
echo.

cd /d "%~dp0mcp-server"

echo Testing MCP Server...
echo.

pwsh -ExecutionPolicy Bypass -File test-server.ps1

echo.
echo Press any key to exit...
pause >nul

