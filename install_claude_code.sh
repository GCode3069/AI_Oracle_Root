#!/bin/bash

# Claude Code Installation Script
# This script helps install Claude Code extension for VS Code/Cursor

set -e

echo "=== Claude Code Installation Script ==="
echo ""

# Check if we're in Cursor or VS Code environment
if command -v cursor &> /dev/null; then
    EDITOR="cursor"
    EDITOR_NAME="Cursor"
elif command -v code &> /dev/null; then
    EDITOR="code"
    EDITOR_NAME="VS Code"
else
    echo "⚠️  Neither Cursor nor VS Code CLI found in PATH"
    echo ""
    echo "You can still install Claude Code manually:"
    echo "1. Open Cursor/VS Code"
    echo "2. Press Ctrl+Shift+X to open Extensions"
    echo "3. Search for 'Claude Code' or 'Anthropic Claude'"
    echo "4. Click Install"
    echo ""
    echo "See CLAUDE_CODE_INSTALLATION.md for detailed instructions."
    exit 0
fi

echo "✓ Found $EDITOR_NAME CLI"
echo ""

# Try to install Claude Code extension
echo "Attempting to install Claude Code extension..."
echo ""

# Common extension IDs to try
EXTENSION_IDS=(
    "anthropic.claude-code"
    "Anthropic.claude-code"
    "anthropic.claude"
)

INSTALLED=false

for EXT_ID in "${EXTENSION_IDS[@]}"; do
    echo "Trying extension ID: $EXT_ID"
    if $EDITOR --install-extension "$EXT_ID" 2>&1; then
        echo "✓ Successfully installed: $EXT_ID"
        INSTALLED=true
        break
    else
        echo "  Not found, trying next..."
    fi
done

if [ "$INSTALLED" = false ]; then
    echo ""
    echo "⚠️  Could not install via CLI. Please install manually:"
    echo ""
    echo "1. Open $EDITOR_NAME"
    echo "2. Press Ctrl+Shift+X (or Cmd+Shift+X on Mac)"
    echo "3. Search for 'Claude Code' or 'Anthropic Claude'"
    echo "4. Click Install"
    echo ""
    echo "Or visit: https://marketplace.visualstudio.com/vscode"
    echo "and search for 'Claude Code'"
fi

echo ""
echo "=== Next Steps ==="
echo "1. After installation, authenticate with your Anthropic API key"
echo "2. Get your API key from: https://console.anthropic.com/"
echo "3. Use Command Palette (Ctrl+Shift+P) → 'Claude: Sign In'"
echo ""
echo "See CLAUDE_CODE_INSTALLATION.md for complete setup instructions."
