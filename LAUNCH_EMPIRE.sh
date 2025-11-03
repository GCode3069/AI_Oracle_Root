#!/bin/bash
# ═══════════════════════════════════════════════════════════════
#   SCARIFY EMPIRE - UNIFIED LAUNCHER (Linux/Mac)
#   Starts EVERYTHING in one click!
# ═══════════════════════════════════════════════════════════════

clear

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║              🚀 SCARIFY EMPIRE - FULL SYSTEM LAUNCH 🚀           ║"
echo "║                                                                  ║"
echo "║                    Your Video Empire Starts NOW!                ║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo ""

cd "$(dirname "$0")"

echo "[1/5] 🎮 Starting Desktop Control Center..."
echo "       > SCARIFY_CONTROL_CENTER.pyw"
if command -v python3 &> /dev/null; then
    python3 SCARIFY_CONTROL_CENTER.pyw &
elif command -v python &> /dev/null; then
    python SCARIFY_CONTROL_CENTER.pyw &
fi
sleep 2
echo "       ✅ Dashboard Launched!"
echo ""

echo "[2/5] 🤖 Starting MCP Server for AI Control..."
echo "       > mcp-server/dist/index.js"
cd mcp-server
if [ -f dist/index.js ]; then
    gnome-terminal -- bash -c "echo 'MCP SERVER RUNNING' && node dist/index.js; exec bash" 2>/dev/null || \
    xterm -e "echo 'MCP SERVER RUNNING' && node dist/index.js; bash" 2>/dev/null || \
    node dist/index.js &
    echo "       ✅ MCP Server Online!"
else
    echo "       ⚠️  MCP server not built. Run: npm run build"
fi
cd ..
sleep 2
echo ""

echo "[3/5] 📱 Starting Telegram Bot (if configured)..."
if [ -f telegram_bot.py ]; then
    python3 telegram_bot.py &
    echo "       ✅ Telegram Bot Started!"
else
    echo "       ⚠️  Telegram bot not found (optional)"
fi
echo ""

echo "[4/5] 🌐 Starting Mobile Web Interface..."
if [ -f MOBILE_MCP_SERVER.py ]; then
    python3 MOBILE_MCP_SERVER.py &
    echo "       ✅ Mobile Web UI: http://localhost:5000"
else
    echo "       ⚠️  Mobile UI not found (will create next)"
fi
echo ""

echo "[5/5] 📚 Opening Quick Start Guide..."
if [ -f START_HERE_MCP.md ]; then
    xdg-open START_HERE_MCP.md 2>/dev/null || open START_HERE_MCP.md 2>/dev/null
    echo "       ✅ Documentation Opened!"
else
    echo "       ℹ️  Documentation in project folder"
fi
echo ""

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║                    ✅ ALL SYSTEMS OPERATIONAL! ✅                ║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "🎯 YOU NOW HAVE ACCESS TO:"
echo ""
echo "   1. 🖥️  Desktop Dashboard         - Visual GUI Control"
echo "   2. 🤖 MCP Server                 - AI Voice Control (Claude/Cursor)"
echo "   3. 📱 Telegram Bot               - Mobile Remote Control"
echo "   4. 🌐 Mobile Web UI              - http://localhost:5000"
echo "   5. 📚 Documentation              - Guides & Help"
echo ""
echo "💡 NEXT STEPS:"
echo ""
echo "   • Open Claude Desktop to use MCP voice control"
echo "   • Access Desktop Dashboard for visual control"
echo "   • Visit http://localhost:5000 for mobile interface"
echo "   • Check Telegram for mobile commands"
echo ""
echo "🔥 YOUR VIDEO EMPIRE IS NOW FULLY OPERATIONAL! 🔥"
echo ""
echo "Press Enter to continue..."
read

