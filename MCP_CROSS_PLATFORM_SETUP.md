# 🌍 MCP Server - Cross-Platform Setup Guide

## Overview

The Scarify Empire MCP Server now supports **Windows, Linux, and macOS**!

---

## 🔧 Platform Detection

The server **automatically detects** your platform and adjusts:

- **Python Command**: `python` on Windows, `python3` on Linux/Mac
- **Project Root**: Auto-detected or use environment variable `SCARIFY_PROJECT_ROOT`
- **Paths**: All paths use Node.js `path.join()` for cross-platform compatibility

---

## 📦 Installation by Platform

### 🪟 Windows

**Method 1: Batch File (Easiest)**
```cmd
INSTALL_MCP.bat
```

**Method 2: Manual**
```powershell
cd mcp-server
npm install
npm run build
```

**Test:**
```cmd
TEST_MCP_SERVER.bat
```

---

### 🐧 Linux

**Method 1: Shell Script (Easiest)**
```bash
chmod +x INSTALL_MCP_LINUX.sh
./INSTALL_MCP_LINUX.sh
```

**Method 2: Manual**
```bash
cd mcp-server
npm install
npm run build
```

**Test:**
```bash
chmod +x TEST_MCP_SERVER_LINUX.sh
./TEST_MCP_SERVER_LINUX.sh
```

---

### 🍎 macOS

**Method 1: Shell Script (Easiest)**
```bash
chmod +x INSTALL_MCP_LINUX.sh
./INSTALL_MCP_LINUX.sh
```

**Method 2: Manual**
```bash
cd mcp-server
npm install
npm run build
```

**Test:**
```bash
chmod +x TEST_MCP_SERVER_LINUX.sh
./TEST_MCP_SERVER_LINUX.sh
```

---

## 🔌 Integration Configuration

### Windows - Claude Desktop

**Config File:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Example Config:**
```json
{
  "mcpServers": {
    "scarify-empire": {
      "command": "node",
      "args": [
        "F:\\AI_Oracle_Root\\scarify\\mcp-server\\dist\\index.js"
      ],
      "env": {
        "SCARIFY_PROJECT_ROOT": "F:\\AI_Oracle_Root\\scarify"
      }
    }
  }
}
```

---

### Linux - Claude Desktop

**Config File:**
```
~/.config/Claude/claude_desktop_config.json
```

**Example Config:**
```json
{
  "mcpServers": {
    "scarify-empire": {
      "command": "node",
      "args": [
        "/home/YOUR_USERNAME/scarify/mcp-server/dist/index.js"
      ],
      "env": {
        "SCARIFY_PROJECT_ROOT": "/home/YOUR_USERNAME/scarify"
      }
    }
  }
}
```

**Replace `YOUR_USERNAME` with your actual username!**

---

### macOS - Claude Desktop

**Config File:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Example Config:**
```json
{
  "mcpServers": {
    "scarify-empire": {
      "command": "node",
      "args": [
        "/Users/YOUR_USERNAME/scarify/mcp-server/dist/index.js"
      ],
      "env": {
        "SCARIFY_PROJECT_ROOT": "/Users/YOUR_USERNAME/scarify"
      }
    }
  }
}
```

**Replace `YOUR_USERNAME` with your actual username!**

---

## 🎯 Environment Variables

### Setting Project Root

The server looks for your Scarify project in this order:

1. **Environment Variable** `SCARIFY_PROJECT_ROOT` (highest priority)
2. **Default Windows**: `F:\AI_Oracle_Root\scarify`
3. **Default Linux/Mac**: `~/scarify`

### Setting the Variable

**Windows (PowerShell):**
```powershell
$env:SCARIFY_PROJECT_ROOT = "F:\AI_Oracle_Root\scarify"
```

**Windows (CMD):**
```cmd
set SCARIFY_PROJECT_ROOT=F:\AI_Oracle_Root\scarify
```

**Linux/Mac (Bash):**
```bash
export SCARIFY_PROJECT_ROOT=/home/youruser/scarify
```

**Permanent (Linux/Mac - add to ~/.bashrc or ~/.zshrc):**
```bash
echo 'export SCARIFY_PROJECT_ROOT=/home/youruser/scarify' >> ~/.bashrc
source ~/.bashrc
```

---

## 🧪 Testing

### Verify Installation

**All Platforms:**
```bash
cd mcp-server
npm start
```

**Expected Output:**
```
Scarify Empire MCP Server running on stdio
Platform: linux (or win32, darwin)
Python: python3 (or python)
Project Root: /path/to/your/scarify
```

Press `Ctrl+C` to stop.

---

### Quick Tests

**Windows:**
```cmd
TEST_MCP_SERVER.bat
```

**Linux/Mac:**
```bash
chmod +x TEST_MCP_SERVER_LINUX.sh
./TEST_MCP_SERVER_LINUX.sh
```

---

## 🔍 Platform-Specific Issues

### Windows

**Issue:** "python not found"
**Fix:** Install Python from https://python.org and ensure "Add to PATH" is checked

**Issue:** PowerShell scripts won't run
**Fix:** 
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### Linux

**Issue:** "python3 not found"
**Fix:**
```bash
sudo apt install python3 python3-pip  # Debian/Ubuntu
sudo yum install python3 python3-pip  # RedHat/CentOS
```

**Issue:** "npm not found"
**Fix:**
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

**Issue:** Permission denied
**Fix:**
```bash
chmod +x INSTALL_MCP_LINUX.sh
chmod +x TEST_MCP_SERVER_LINUX.sh
chmod +x mcp-server/install.sh
chmod +x mcp-server/test-server.sh
```

---

### macOS

**Issue:** "python3 not found"
**Fix:**
```bash
brew install python3
```

**Issue:** "npm not found"
**Fix:**
```bash
brew install node
```

**Issue:** "command not found: node"
**Fix:** Ensure Node.js is in PATH:
```bash
export PATH="/usr/local/bin:$PATH"
```

---

## 📁 Directory Structure (Cross-Platform)

```
scarify/                          # Your project root
├── mcp-server/                   # MCP Server
│   ├── src/
│   │   └── index.ts              # Cross-platform source
│   ├── dist/
│   │   └── index.js              # Compiled (all platforms)
│   ├── config-examples/          # Platform-specific configs
│   │   ├── claude-desktop-windows.json
│   │   ├── claude-desktop-linux.json
│   │   └── claude-desktop-mac.json
│   ├── install.sh                # Linux/Mac installer
│   ├── install.ps1               # Windows installer
│   ├── test-server.sh            # Linux/Mac tester
│   └── test-server.ps1           # Windows tester
│
├── INSTALL_MCP.bat               # Windows quick install
├── INSTALL_MCP_LINUX.sh          # Linux/Mac quick install
├── TEST_MCP_SERVER.bat           # Windows quick test
└── TEST_MCP_SERVER_LINUX.sh      # Linux/Mac quick test
```

---

## 🚀 Platform-Specific Features

### Windows
- ✅ PowerShell scripts
- ✅ Batch files for one-click install
- ✅ `python` command
- ✅ Windows paths with backslashes

### Linux
- ✅ Bash scripts
- ✅ `python3` command
- ✅ Unix paths with forward slashes
- ✅ Systemd integration (optional)

### macOS
- ✅ Bash scripts
- ✅ `python3` command
- ✅ Unix paths
- ✅ Homebrew-friendly

---

## 🔄 Auto-Detection Logic

The server automatically detects:

```typescript
// Platform detection
const platform = os.platform();
// 'win32' = Windows
// 'linux' = Linux
// 'darwin' = macOS

// Python command
const PYTHON_CMD = platform === 'win32' ? 'python' : 'python3';

// Project root
const PROJECT_ROOT = process.env.SCARIFY_PROJECT_ROOT || 
  (platform === 'win32' 
    ? 'F:\\AI_Oracle_Root\\scarify' 
    : path.join(os.homedir(), 'scarify'));
```

---

## 📝 Configuration Examples

Ready-to-use configs are in `mcp-server/config-examples/`:

- `claude-desktop-windows.json` - Windows paths
- `claude-desktop-linux.json` - Linux paths
- `claude-desktop-mac.json` - macOS paths

**Just copy the relevant one and update YOUR_USERNAME!**

---

## 🎯 Quick Start by Platform

### Windows Quick Start
1. Run `INSTALL_MCP.bat`
2. Edit `%APPDATA%\Claude\claude_desktop_config.json`
3. Paste config from `mcp-server/config-examples/claude-desktop-windows.json`
4. Restart Claude Desktop
5. Test: "Show system status"

### Linux Quick Start
1. Run `chmod +x INSTALL_MCP_LINUX.sh && ./INSTALL_MCP_LINUX.sh`
2. Edit `~/.config/Claude/claude_desktop_config.json`
3. Paste config from `mcp-server/config-examples/claude-desktop-linux.json`
4. Update YOUR_USERNAME to your actual username
5. Restart Claude Desktop
6. Test: "Show system status"

### macOS Quick Start
1. Run `chmod +x INSTALL_MCP_LINUX.sh && ./INSTALL_MCP_LINUX.sh`
2. Edit `~/Library/Application Support/Claude/claude_desktop_config.json`
3. Paste config from `mcp-server/config-examples/claude-desktop-mac.json`
4. Update YOUR_USERNAME to your actual username
5. Restart Claude Desktop
6. Test: "Show system status"

---

## 🆘 Troubleshooting by Platform

### Windows
```powershell
# Check Node.js
node --version

# Check Python
python --version

# Check npm
npm --version

# Rebuild
cd mcp-server
npm run build
```

### Linux/Mac
```bash
# Check Node.js
node --version

# Check Python
python3 --version

# Check npm
npm --version

# Rebuild
cd mcp-server
npm run build
```

---

## ✅ Verification Checklist

- [ ] Node.js installed (v18+)
- [ ] Python installed (3.8+)
- [ ] npm installed
- [ ] MCP server built (`mcp-server/dist/index.js` exists)
- [ ] Project root configured (environment variable or default)
- [ ] Claude Desktop config updated
- [ ] Server starts without errors
- [ ] AI assistant can see tools

---

## 🌟 Success Indicators

When working correctly, you should see:

```
Scarify Empire MCP Server running on stdio
Platform: [your-platform]
Python: [python-command]
Project Root: [your-path]
```

And in Claude/Cursor, you can say:
- "Show system status" ✅
- "List all videos" ✅
- "Generate videos" ✅

---

## 📚 Additional Resources

- **Main Setup Guide**: `MCP_SERVER_SETUP.md`
- **Usage Examples**: `MCP_USAGE_EXAMPLES.md`
- **Quick Reference**: `MCP_QUICK_REFERENCE.txt`
- **Installation Summary**: `MCP_INSTALLATION_SUMMARY.txt`

---

**The MCP server is now truly cross-platform! 🌍**

