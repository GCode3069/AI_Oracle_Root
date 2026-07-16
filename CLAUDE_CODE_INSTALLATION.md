# Claude Code Installation Guide

## Overview
Claude Code is an extension/tool from Anthropic that provides AI-powered coding assistance. This guide will help you install it in your development environment.

## Installation Methods

### Method 1: Install via VS Code/Cursor Extension Marketplace (Recommended)

1. **Open Cursor/VS Code**
   - If you're using Cursor, it should already be open
   - If using VS Code, launch it

2. **Open Extensions View**
   - Press `Ctrl+Shift+X` (Linux/Windows) or `Cmd+Shift+X` (Mac)
   - Or click the Extensions icon in the sidebar

3. **Search for Claude Code**
   - Type "Claude Code" or "Anthropic Claude" in the search box
   - Look for the official Anthropic extension

4. **Install**
   - Click "Install" on the Claude Code extension
   - Wait for installation to complete
   - You may need to reload the window

### Method 2: Install via Command Line (if VS Code CLI is available)

If you have VS Code CLI installed:

```bash
code --install-extension anthropic.claude-code
```

Or for Cursor:

```bash
cursor --install-extension anthropic.claude-code
```

### Method 3: Manual Installation

1. **Download the Extension**
   - Visit the VS Code Marketplace: https://marketplace.visualstudio.com/
   - Search for "Claude Code" or "Anthropic Claude"
   - Download the `.vsix` file

2. **Install from VSIX**
   - In VS Code/Cursor, go to Extensions view
   - Click the `...` menu (top right)
   - Select "Install from VSIX..."
   - Choose the downloaded `.vsix` file

### Method 4: Install VS Code First (if not installed)

If VS Code is not installed on your system:

**For Linux (Ubuntu/Debian):**
```bash
# Download and install VS Code
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt update
sudo apt install code
```

**For Linux (using snap):**
```bash
sudo snap install code --classic
```

**For other distributions:**
- Visit: https://code.visualstudio.com/download
- Download the appropriate package for your Linux distribution

## Post-Installation Setup

### 1. Authenticate with Anthropic

After installation, you'll need to authenticate:

1. Open Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`)
2. Type "Claude: Sign In" or "Claude: Authenticate"
3. Follow the authentication flow
4. You may need an Anthropic API key

### 2. Get Your Anthropic API Key

1. Visit: https://console.anthropic.com/
2. Sign in or create an account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (you'll need it for authentication)

### 3. Configure the Extension

1. Open Settings (`Ctrl+,` or `Cmd+,`)
2. Search for "Claude" or "Anthropic"
3. Configure any necessary settings:
   - API endpoint (if using custom endpoint)
   - Model preferences
   - Other extension-specific settings

## Verification

To verify Claude Code is installed and working:

1. Open any code file
2. Look for Claude Code features in the editor
3. Try using the command palette to access Claude Code commands
4. Check the status bar for Claude Code indicators

## Troubleshooting

### Extension Not Found
- Make sure you're searching in the correct marketplace
- Check if you're behind a firewall/proxy
- Try the manual installation method

### Authentication Issues
- Verify your API key is correct
- Check your internet connection
- Ensure you have API access enabled in your Anthropic account

### Extension Not Working
- Reload the window (`Ctrl+Shift+P` → "Reload Window")
- Check the Output panel for error messages
- Verify VS Code/Cursor is up to date

## Additional Resources

- Official Documentation: https://docs.anthropic.com/
- VS Code Marketplace: https://marketplace.visualstudio.com/
- Anthropic Console: https://console.anthropic.com/

## Notes

- Claude Code may require a paid Anthropic API plan depending on usage
- Some features may require specific VS Code/Cursor versions
- Check the extension's documentation for model-specific requirements
