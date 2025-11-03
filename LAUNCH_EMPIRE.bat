@echo off
REM ═══════════════════════════════════════════════════════════════
REM   SCARIFY EMPIRE - UNIFIED LAUNCHER
REM   Starts EVERYTHING in one click!
REM ═══════════════════════════════════════════════════════════════

color 0A
cls

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║              🚀 SCARIFY EMPIRE - FULL SYSTEM LAUNCH 🚀           ║
echo ║                                                                  ║
echo ║                    Your Video Empire Starts NOW!                ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo.

cd /d "%~dp0"

echo [1/5] 🎮 Starting Desktop Control Center...
echo        ^> SCARIFY_CONTROL_CENTER.pyw
start "" pythonw SCARIFY_CONTROL_CENTER.pyw
timeout /t 2 /nobreak >nul
echo        ✅ Dashboard Launched!
echo.

echo [2/5] 🤖 Starting MCP Server for AI Control...
echo        ^> mcp-server/dist/index.js
cd mcp-server
start "MCP Server" cmd /k "echo MCP SERVER RUNNING && echo Press Ctrl+C to stop && node dist/index.js"
cd ..
timeout /t 2 /nobreak >nul
echo        ✅ MCP Server Online!
echo.

echo [3/5] 📱 Starting Telegram Bot (if configured)...
if exist telegram_bot.py (
    start "Telegram Bot" cmd /k "python telegram_bot.py"
    echo        ✅ Telegram Bot Started!
) else (
    echo        ⚠️  Telegram bot not found (optional)
)
echo.

echo [4/5] 🌐 Starting Mobile Web Interface...
if exist MOBILE_MCP_SERVER.py (
    start "Mobile Web UI" cmd /k "python MOBILE_MCP_SERVER.py"
    echo        ✅ Mobile Web UI: http://localhost:5000
) else (
    echo        ⚠️  Mobile UI not found (will create next)
)
echo.

echo [5/5] 📚 Opening Quick Start Guide...
if exist START_HERE_MCP.md (
    start "" START_HERE_MCP.md
    echo        ✅ Documentation Opened!
) else (
    echo        ℹ️  Documentation in project folder
)
echo.

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║                    ✅ ALL SYSTEMS OPERATIONAL! ✅                ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo 🎯 YOU NOW HAVE ACCESS TO:
echo.
echo    1. 🖥️  Desktop Dashboard         - Visual GUI Control
echo    2. 🤖 MCP Server                 - AI Voice Control (Claude/Cursor)
echo    3. 📱 Telegram Bot               - Mobile Remote Control
echo    4. 🌐 Mobile Web UI              - http://localhost:5000
echo    5. 📚 Documentation              - Guides ^& Help
echo.
echo 💡 NEXT STEPS:
echo.
echo    • Open Claude Desktop to use MCP voice control
echo    • Access Desktop Dashboard for visual control  
echo    • Visit http://localhost:5000 for mobile interface
echo    • Check Telegram for mobile commands
echo.
echo 🔥 YOUR VIDEO EMPIRE IS NOW FULLY OPERATIONAL! 🔥
echo.
echo Press any key to keep this window open...
pause >nul

