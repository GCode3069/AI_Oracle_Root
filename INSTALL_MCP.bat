@echo off
REM Quick installer for Scarify MCP Server

echo ========================================
echo  Scarify Empire - MCP Server Installer
echo ========================================
echo.

cd /d "%~dp0mcp-server"

echo Installing MCP Server...
echo.

pwsh -ExecutionPolicy Bypass -File install.ps1

echo.
echo Press any key to exit...
pause >nul

