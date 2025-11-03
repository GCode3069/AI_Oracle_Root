#!/bin/bash
# ═══════════════════════════════════════════════════════════════
#   SCARIFY EMPIRE - Desktop Launcher Creator (Linux)
#   Creates .desktop files for GNOME, KDE, etc.
# ═══════════════════════════════════════════════════════════════

clear

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║         🖥️  SCARIFY EMPIRE - DESKTOP LAUNCHER CREATOR 🖥️        ║"
echo "║                                                                  ║"
echo "║           Creating beautiful desktop launchers...                ║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
DESKTOP_DIR="$HOME/Desktop"
APPLICATIONS_DIR="$HOME/.local/share/applications"

# Create applications directory if it doesn't exist
mkdir -p "$APPLICATIONS_DIR"

# Function to create .desktop file
create_desktop_launcher() {
    local name="$1"
    local exec_cmd="$2"
    local comment="$3"
    local icon="$4"
    local filename="$5"
    
    echo "[*] Creating: $name"
    
    cat > "$DESKTOP_DIR/$filename" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=$name
Comment=$comment
Exec=$exec_cmd
Path=$PROJECT_ROOT
Icon=$icon
Terminal=false
Categories=Development;Utility;
EOF
    
    # Make executable
    chmod +x "$DESKTOP_DIR/$filename"
    
    # Also create in applications menu
    cp "$DESKTOP_DIR/$filename" "$APPLICATIONS_DIR/"
    
    echo "    ✅ Created: $filename"
}

# Main Empire Launcher
create_desktop_launcher \
    "🚀 Launch Scarify Empire" \
    "$PROJECT_ROOT/LAUNCH_EMPIRE.sh" \
    "Start the complete Scarify Empire system" \
    "applications-multimedia" \
    "scarify-empire.desktop"

# Desktop Dashboard
create_desktop_launcher \
    "🖥️ Scarify Control Center" \
    "python3 $PROJECT_ROOT/SCARIFY_CONTROL_CENTER.pyw" \
    "Open Scarify Empire Desktop Dashboard (18 tabs)" \
    "preferences-desktop" \
    "scarify-dashboard.desktop"

# Mobile Web UI
create_desktop_launcher \
    "📱 Mobile Web Interface" \
    "x-terminal-emulator -e python3 $PROJECT_ROOT/MOBILE_MCP_SERVER.py" \
    "Start Scarify Mobile Web UI (http://localhost:5000)" \
    "applications-internet" \
    "scarify-mobile.desktop"

# MCP Server
create_desktop_launcher \
    "🤖 MCP Server" \
    "x-terminal-emulator -e bash -c 'cd $PROJECT_ROOT/mcp-server && npm start; exec bash'" \
    "Start MCP Server for Claude/Cursor AI control" \
    "applications-system" \
    "scarify-mcp.desktop"

# Self Deploy Agent
create_desktop_launcher \
    "🔧 Self Deploy Agent" \
    "x-terminal-emulator -e python3 $PROJECT_ROOT/SELF_DEPLOY.py" \
    "Run Scarify Empire self-deployment agent" \
    "system-software-install" \
    "scarify-deploy.desktop"

# GitHub Sync
create_desktop_launcher \
    "📤 Sync to GitHub" \
    "x-terminal-emulator -e $PROJECT_ROOT/SYNC_TO_GITHUB.sh" \
    "Sync all changes to GitHub repository" \
    "folder-publicshare" \
    "scarify-github.desktop"

# Project Folder
create_desktop_launcher \
    "📁 Scarify Folder" \
    "xdg-open $PROJECT_ROOT" \
    "Open Scarify Empire project folder" \
    "folder" \
    "scarify-folder.desktop"

# Documentation
create_desktop_launcher \
    "📚 Scarify Docs" \
    "xdg-open $PROJECT_ROOT/🚀_START_HERE_MASTER_GUIDE.md" \
    "Open Scarify Empire documentation" \
    "text-x-generic" \
    "scarify-docs.desktop"

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║                 ✅ DESKTOP LAUNCHERS CREATED! ✅                 ║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "🎯 Created on your desktop:"
echo ""
echo "   🚀 Launch Scarify Empire    - Starts everything!"
echo "   🖥️  Scarify Control Center   - Desktop dashboard only"
echo "   📱 Mobile Web Interface     - Mobile UI server"
echo "   🤖 MCP Server               - AI voice control"
echo "   🔧 Self Deploy Agent        - Auto-deployment"
echo "   📤 Sync to GitHub           - GitHub sync"
echo "   📁 Scarify Folder           - Project folder"
echo "   📚 Scarify Docs             - Documentation"
echo ""
echo "💡 TIP: Double-click any launcher to run!"
echo ""
echo "🔥 Your desktop is now a command center! 🔥"
echo ""

