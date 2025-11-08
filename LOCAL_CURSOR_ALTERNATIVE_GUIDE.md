# 🚀 AI Oracle IDE - Build Your Own Local Cursor Alternative

> **Turn your local machine into a powerful, independent AI coding assistant using 100% free, open-source tools**

[![Status](https://img.shields.io/badge/status-ready-brightgreen)]()
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-blue)]()
[![License](https://img.shields.io/badge/license-100%25%20Open%20Source-green)]()
[![Cost](https://img.shields.io/badge/cost-FREE-brightgreen)]()

---

## 🎯 What You're Building

A **complete, local AI coding environment** that rivals Cursor IDE with:

- ✅ **Local AI Models** - Run entirely on your machine
- ✅ **Code Completion** - Smart autocomplete like GitHub Copilot
- ✅ **AI Chat** - Conversation with AI about your code
- ✅ **Code Understanding** - Context-aware suggestions
- ✅ **MCP Integration** - Your existing MCP servers work perfectly!
- ✅ **Git Integration** - Built-in version control
- ✅ **Multi-Language** - Python, JS, TS, Go, Rust, and more
- ✅ **Extensions** - Thousands of free extensions
- ✅ **Terminal** - Integrated terminal
- ✅ **100% Free** - No subscriptions, no API costs

**Best Part:** It all runs locally. No internet required after initial setup!

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                   AI ORACLE IDE                          │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │         VSCodium (Open Source VS Code)         │    │
│  │  • Full VS Code features                       │    │
│  │  • No Microsoft telemetry                      │    │
│  │  • 100% open source                            │    │
│  └────────────────────────────────────────────────┘    │
│                         │                               │
│  ┌─────────────────────┴──────────────────────┐        │
│  │                                              │        │
│  ▼                                              ▼        │
│  ┌──────────────────────┐    ┌────────────────────┐    │
│  │  Continue.dev         │    │  Ollama + Models   │    │
│  │  • AI Chat            │◄───│  • CodeLlama       │    │
│  │  • Auto-complete      │    │  • DeepSeek Coder  │    │
│  │  │  • Refactoring     │    │  • Llama 3.2       │    │
│  │  • Context aware      │    │  • Qwen Coder      │    │
│  └──────────────────────┘    └────────────────────┘    │
│             │                                            │
│             ▼                                            │
│  ┌──────────────────────────────────────────────────┐  │
│  │          Your MCP Servers                         │  │
│  │  • Oracle MCP Server                              │  │
│  │  • Mobile MCP Bridge                              │  │
│  │  • Custom integrations                            │  │
│  └──────────────────────────────────────────────────┘  │
│             │                                            │
│             ▼                                            │
│  ┌──────────────────────────────────────────────────┐  │
│  │          Code Intelligence                        │  │
│  │  • LSP servers (auto-installed)                   │  │
│  │  • Tree-sitter (syntax)                           │  │
│  │  • IntelliSense                                   │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 Components Breakdown

### 1. **VSCodium** - The Editor
- **What**: 100% open-source VS Code (no Microsoft telemetry)
- **Why**: Best code editor, fully compatible with VS Code extensions
- **Cost**: FREE
- **Features**: Everything VS Code has, minus the tracking

### 2. **Ollama** - Local AI Runtime
- **What**: Run LLMs locally on your machine
- **Why**: No API costs, works offline, private
- **Cost**: FREE
- **Models Available**:
  - CodeLlama 13B - Fast, great for code
  - DeepSeek Coder 6.7B - Excellent code understanding
  - Llama 3.2 - General purpose
  - Qwen Coder - Specializes in multiple languages
  - Mistral 7B - Fast and efficient

### 3. **Continue.dev** - AI Integration
- **What**: Open-source Cursor alternative for VS Code
- **Why**: Connects VSCodium to local AI models
- **Cost**: FREE
- **Features**:
  - Tab autocomplete
  - AI chat panel
  - Code refactoring
  - Context-aware suggestions
  - Multi-model support

### 4. **MCP (Model Context Protocol)**
- **What**: You already have this!
- **Why**: Connect AI to your tools and data
- **Status**: ✅ Already configured
- **Integration**: Works seamlessly with Continue.dev

### 5. **Additional Tools**
- **Tree-sitter**: Syntax parsing (built-in)
- **LSP Servers**: Language intelligence (auto-installed)
- **Git**: Version control (built-in)
- **Extensions**: 1000s available for free

---

## 🚀 Quick Start (Choose Your Platform)

### **Windows** (10 minutes)
```powershell
# Run the automated installer
.\INSTALL_AI_ORACLE_IDE.ps1
```

### **Linux** (10 minutes)
```bash
# Run the automated installer
chmod +x INSTALL_AI_ORACLE_IDE.sh
./INSTALL_AI_ORACLE_IDE.sh
```

### **macOS** (10 minutes)
```bash
# Run the automated installer
chmod +x INSTALL_AI_ORACLE_IDE_MAC.sh
./INSTALL_AI_ORACLE_IDE_MAC.sh
```

**That's it!** The scripts install everything automatically.

---

## 📋 Manual Installation (If you prefer step-by-step)

### Step 1: Install VSCodium (5 min)

**Windows:**
```powershell
# Using winget
winget install VSCodium.VSCodium

# OR download from: https://vscodium.com
```

**Linux (Debian/Ubuntu):**
```bash
wget -qO - https://gitlab.com/paulcarroty/vscodium-deb-rpm-repo/raw/master/pub.gpg \
    | gpg --dearmor \
    | sudo dd of=/usr/share/keyrings/vscodium-archive-keyring.gpg

echo 'deb [ signed-by=/usr/share/keyrings/vscodium-archive-keyring.gpg ] https://download.vscodium.com/debs vscodium main' \
    | sudo tee /etc/apt/sources.list.d/vscodium.list

sudo apt update && sudo apt install codium
```

**Linux (Fedora):**
```bash
sudo dnf install vscodium
```

**macOS:**
```bash
brew install --cask vscodium
```

---

### Step 2: Install Ollama (3 min)

**Windows:**
```powershell
# Download and install from: https://ollama.ai/download
# OR use installer script (included)
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**macOS:**
```bash
brew install ollama
```

**Verify installation:**
```bash
ollama --version
```

---

### Step 3: Download AI Models (10-30 min depending on internet)

```bash
# Recommended starter models (choose based on your RAM)

# For 8GB RAM - Start with smallest
ollama pull deepseek-coder:1.3b

# For 16GB RAM - Great balance
ollama pull deepseek-coder:6.7b
ollama pull codellama:7b

# For 32GB+ RAM - Use larger models
ollama pull deepseek-coder:33b
ollama pull codellama:13b
ollama pull qwen:14b

# General purpose (always useful)
ollama pull llama3.2:3b
```

**Test a model:**
```bash
ollama run deepseek-coder:6.7b "Write a Python function to reverse a string"
```

---

### Step 4: Install Continue.dev Extension (2 min)

**In VSCodium:**
```
1. Open VSCodium
2. Click Extensions (Ctrl+Shift+X)
3. Search: "Continue"
4. Click "Install" on "Continue - AI Code Assistant"
5. Restart VSCodium
```

**OR via command line:**
```bash
# Windows
codium --install-extension continue.continue

# Linux/Mac
codium --install-extension continue.continue
```

---

### Step 5: Configure Continue.dev (5 min)

**Open Continue config:**
- Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
- Type: "Continue: Open config.json"
- Hit Enter

**Paste this configuration:**
```json
{
  "models": [
    {
      "title": "DeepSeek Coder",
      "provider": "ollama",
      "model": "deepseek-coder:6.7b",
      "apiBase": "http://localhost:11434"
    },
    {
      "title": "CodeLlama",
      "provider": "ollama",
      "model": "codellama:7b",
      "apiBase": "http://localhost:11434"
    },
    {
      "title": "Llama 3.2",
      "provider": "ollama",
      "model": "llama3.2:3b",
      "apiBase": "http://localhost:11434"
    }
  ],
  "tabAutocompleteModel": {
    "title": "DeepSeek Coder Autocomplete",
    "provider": "ollama",
    "model": "deepseek-coder:1.3b",
    "apiBase": "http://localhost:11434"
  },
  "embeddingsProvider": {
    "provider": "ollama",
    "model": "nomic-embed-text",
    "apiBase": "http://localhost:11434"
  },
  "contextProviders": [
    {
      "name": "code",
      "params": {}
    },
    {
      "name": "docs",
      "params": {}
    },
    {
      "name": "diff",
      "params": {}
    },
    {
      "name": "terminal",
      "params": {}
    },
    {
      "name": "problems",
      "params": {}
    },
    {
      "name": "folder",
      "params": {}
    },
    {
      "name": "codebase",
      "params": {}
    }
  ],
  "slashCommands": [
    {
      "name": "edit",
      "description": "Edit selected code"
    },
    {
      "name": "comment",
      "description": "Add comments to code"
    },
    {
      "name": "share",
      "description": "Share code context"
    },
    {
      "name": "cmd",
      "description": "Generate shell command"
    },
    {
      "name": "commit",
      "description": "Generate commit message"
    }
  ],
  "customCommands": [
    {
      "name": "test",
      "prompt": "Write unit tests for the selected code using the same framework as in the codebase",
      "description": "Generate unit tests"
    }
  ],
  "allowAnonymousTelemetry": false
}
```

**Download embedding model (for better context):**
```bash
ollama pull nomic-embed-text
```

---

### Step 6: Integrate Your MCP Servers (5 min)

You already have MCP servers! Let's connect them.

**Install MCP extension for VSCodium:**
```bash
codium --install-extension modelcontextprotocol.mcp
```

**Configure MCP in VSCodium:**

Create/edit: `~/.config/VSCodium/User/settings.json` (Linux/Mac)
Or: `%APPDATA%\VSCodium\User\settings.json` (Windows)

Add:
```json
{
  "mcp.servers": {
    "oracle": {
      "command": "node",
      "args": ["/home/user/AI_Oracle_Root/mcp_server/oracle_mcp_server.py"]
    },
    "mobile-bridge": {
      "command": "python3",
      "args": ["/home/user/AI_Oracle_Root/mcp_server/MOBILE_MCP_BRIDGE.py"]
    }
  }
}
```

---

## 🎨 Recommended Extensions

Install these for the complete experience:

```bash
# Essential
codium --install-extension continue.continue              # AI assistant
codium --install-extension ms-python.python               # Python
codium --install-extension dbaeumer.vscode-eslint         # JavaScript/TS
codium --install-extension esbenp.prettier-vscode         # Code formatter
codium --install-extension eamodio.gitlens                # Git supercharged

# Code Quality
codium --install-extension ms-python.pylint               # Python linting
codium --install-extension ms-python.black-formatter      # Python formatter
codium --install-extension streetsidesoftware.code-spell-checker  # Spell check

# Productivity
codium --install-extension usernamehw.errorlens           # Inline errors
codium --install-extension PKief.material-icon-theme      # Beautiful icons
codium --install-extension github.copilot-chat            # If you have Copilot

# AI Alternatives (choose one)
codium --install-extension tabnine.tabnine-vscode         # Tabnine (freemium)
codium --install-extension sourcegraph.cody-ai            # Cody (free tier)
```

---

## 🎯 Usage Guide

### **Tab Autocomplete**
Just start typing code - Continue.dev will suggest completions!

```python
def calculate_  # Press Tab to accept suggestion
```

### **AI Chat**
1. Press `Ctrl+L` (or `Cmd+L` on Mac) to open AI chat
2. Ask anything:
   - "Explain this function"
   - "Refactor this code to be more efficient"
   - "Add error handling"
   - "Write tests for this"

### **Inline Editing**
1. Select code
2. Press `Ctrl+I` (or `Cmd+I`)
3. Type what you want: "Add logging" or "Make this async"

### **Slash Commands**
In the chat, type `/` to see available commands:
- `/edit` - Edit selected code
- `/comment` - Add comments
- `/test` - Generate tests
- `/commit` - Generate commit message
- `/cmd` - Generate shell command

### **Context Providers**
Continue.dev automatically includes:
- Current file
- Recently edited files
- Terminal output
- Git diff
- Linter problems
- Entire codebase (with indexing)

---

## 🔧 Advanced Configuration

### **Increase Context Window**
For better code understanding, increase context:

```json
{
  "models": [
    {
      "title": "DeepSeek Coder (Large Context)",
      "provider": "ollama",
      "model": "deepseek-coder:6.7b",
      "apiBase": "http://localhost:11434",
      "contextLength": 16384
    }
  ]
}
```

### **Use Multiple Models**
Switch between models for different tasks:

```json
{
  "models": [
    {
      "title": "Fast (DeepSeek 1.3B)",
      "provider": "ollama",
      "model": "deepseek-coder:1.3b"
    },
    {
      "title": "Balanced (CodeLlama 7B)",
      "provider": "ollama",
      "model": "codellama:7b"
    },
    {
      "title": "Powerful (DeepSeek 33B)",
      "provider": "ollama",
      "model": "deepseek-coder:33b"
    }
  ]
}
```

### **Custom Prompts**
Add your own commands:

```json
{
  "customCommands": [
    {
      "name": "optimize",
      "prompt": "Optimize this code for performance and readability",
      "description": "Optimize code"
    },
    {
      "name": "security",
      "prompt": "Review this code for security vulnerabilities",
      "description": "Security audit"
    },
    {
      "name": "document",
      "prompt": "Add comprehensive documentation to this code",
      "description": "Add docs"
    }
  ]
}
```

---

## 💡 Pro Tips

### **1. Model Selection by Task**
- **Autocomplete**: Use smallest/fastest (1.3B)
- **Chat/Questions**: Use balanced (6.7B-7B)
- **Complex Refactoring**: Use largest (13B-33B)

### **2. Speed Up Responses**
- Keep Ollama running in background
- Use SSD for model storage
- Allocate more RAM to Ollama:
  ```bash
  # Set in environment
  export OLLAMA_MAX_LOADED_MODELS=2
  export OLLAMA_NUM_PARALLEL=4
  ```

### **3. Codebase Indexing**
Let Continue.dev index your codebase for better context:
```
1. Open Command Palette (Ctrl+Shift+P)
2. Type: "Continue: Index Codebase"
3. Wait for indexing to complete
4. Now AI understands your entire project!
```

### **4. Use @-mentions**
In chat, mention specific files:
```
@filename.py Explain how this module works
```

### **5. Terminal Integration**
Continue.dev can see terminal output:
```
Run command in terminal → Error appears → Ask AI: "Fix this error"
```

---

## 🆚 Comparison: AI Oracle IDE vs. Cursor

| Feature | AI Oracle IDE | Cursor |
|---------|---------------|---------|
| **Cost** | FREE | $20/month |
| **Privacy** | 100% Local | Cloud-based |
| **Speed** | Fast (local) | Network dependent |
| **Offline** | ✅ Yes | ❌ No |
| **Open Source** | ✅ Yes | ❌ No |
| **Models** | Any Ollama model | Claude/GPT-4 |
| **Customizable** | ✅ Fully | Limited |
| **MCP Support** | ✅ Yes | ✅ Yes |
| **Code Complete** | ✅ Yes | ✅ Yes |
| **AI Chat** | ✅ Yes | ✅ Yes |
| **Extensions** | 1000s | Limited |
| **Telemetry** | None | Yes |

**Winner**: AI Oracle IDE for privacy, cost, and control!

---

## 📊 Performance & Requirements

### **Minimum Requirements**
- **RAM**: 8GB (16GB recommended)
- **Storage**: 10GB free (for models)
- **CPU**: Modern quad-core
- **OS**: Windows 10+, Linux, macOS 10.15+

### **Recommended Setup**
- **RAM**: 16-32GB
- **Storage**: SSD with 50GB free
- **CPU**: 6+ cores
- **GPU**: Optional (speeds up inference)

### **Model Sizes**
| Model | Size | RAM Needed | Speed |
|-------|------|------------|-------|
| deepseek-coder:1.3b | 1.3GB | 4GB | Very Fast |
| codellama:7b | 3.8GB | 8GB | Fast |
| deepseek-coder:6.7b | 3.8GB | 8GB | Fast |
| codellama:13b | 7.4GB | 16GB | Medium |
| deepseek-coder:33b | 20GB | 32GB | Slower |

---

## 🐛 Troubleshooting

### **Ollama Not Starting**
```bash
# Check if running
systemctl status ollama  # Linux
netstat -an | grep 11434  # Check port

# Restart Ollama
systemctl restart ollama  # Linux
killall ollama && ollama serve  # Mac
```

### **Continue.dev Not Seeing Models**
1. Ensure Ollama is running: `ollama list`
2. Test API: `curl http://localhost:11434/api/tags`
3. Restart VSCodium
4. Check Continue config has correct API base

### **Slow Completions**
- Use smaller model for autocomplete (1.3B)
- Close other heavy applications
- Increase Ollama memory allocation
- Use GPU acceleration (if available)

### **MCP Servers Not Connecting**
1. Verify servers work standalone:
   ```bash
   node /path/to/mcp_server.js
   python3 /path/to/mcp_server.py
   ```
2. Check paths in VSCodium settings
3. Restart VSCodium
4. Check server logs

---

## 🔒 Privacy & Security

### **What Stays Local**
- ✅ All AI models
- ✅ All code
- ✅ All conversations
- ✅ All context
- ✅ All configurations

### **What Leaves Your Machine**
- ❌ Nothing (unless you configure external APIs)

### **Best Practices**
1. Keep Ollama updated: `ollama pull <model>` (checks for updates)
2. Review Continue.dev config
3. Disable telemetry (already done in config above)
4. Use `.gitignore` for sensitive files
5. Regular backups of configs

---

## 🚀 Next Steps

### **After Installation**
1. **Test Everything**:
   ```bash
   # Run test script
   ./TEST_AI_ORACLE_IDE.sh
   ```

2. **Open Sample Project**:
   ```bash
   codium /home/user/AI_Oracle_Root
   ```

3. **Try AI Features**:
   - Write a function and let AI autocomplete
   - Select code and ask AI to explain it
   - Generate tests with `/test`
   - Create commit messages with `/commit`

4. **Customize**:
   - Add more models
   - Create custom commands
   - Install more extensions
   - Configure keybindings

### **Daily Workflow**
```bash
# Morning: Start Ollama (if not auto-started)
systemctl start ollama  # Linux
# or just: ollama serve

# Open VSCodium
codium

# Code with AI assistance all day!

# Evening: (Ollama can run 24/7)
```

---

## 🎓 Learning Resources

### **Continue.dev**
- Docs: https://continue.dev/docs
- GitHub: https://github.com/continuedev/continue
- Discord: https://discord.gg/vapESyrFmJ

### **Ollama**
- Docs: https://ollama.ai/docs
- Models: https://ollama.ai/library
- GitHub: https://github.com/ollama/ollama

### **VSCodium**
- Website: https://vscodium.com
- Docs: Same as VS Code
- GitHub: https://github.com/VSCodium/vscodium

### **MCP (Model Context Protocol)**
- Docs: https://modelcontextprotocol.io
- GitHub: https://github.com/modelcontextprotocol

---

## 🤝 Contributing

### **Improve This Guide**
1. Fork the repo
2. Update documentation
3. Add examples
4. Submit PR

### **Share Your Setup**
- Post your custom configs
- Share useful commands
- Document workflows
- Help others

---

## 📜 License

This guide and all scripts are released under MIT License.

**All mentioned software**:
- VSCodium: MIT License
- Ollama: MIT License
- Continue.dev: Apache 2.0
- Models: Various open-source licenses

---

## 🎯 Quick Reference Card

### **Essential Commands**
```bash
# Ollama
ollama list                    # List installed models
ollama pull <model>            # Download model
ollama run <model> "prompt"    # Test model
ollama rm <model>              # Remove model

# VSCodium
codium <folder>                # Open folder
codium --install-extension     # Install extension
codium --list-extensions       # List installed

# Continue.dev (in VSCodium)
Ctrl+L                         # Open AI chat
Ctrl+I                         # Inline edit
Tab                            # Accept completion
/                              # Slash commands
```

### **Keyboard Shortcuts**
| Action | Windows/Linux | macOS |
|--------|---------------|-------|
| AI Chat | `Ctrl+L` | `Cmd+L` |
| Inline Edit | `Ctrl+I` | `Cmd+I` |
| Command Palette | `Ctrl+Shift+P` | `Cmd+Shift+P` |
| Accept Completion | `Tab` | `Tab` |
| Reject Completion | `Esc` | `Esc` |

---

## 🏆 Success Stories

After setting up AI Oracle IDE, you'll have:

- ✅ **Zero monthly costs** (vs $20-50/month for Cursor/Copilot)
- ✅ **Complete privacy** (code never leaves your machine)
- ✅ **Offline capability** (code anywhere, anytime)
- ✅ **Full control** (customize everything)
- ✅ **Open source** (audit, modify, improve)
- ✅ **MCP integration** (leverage your existing tools)

**Annual Savings**: $240-600 compared to paid alternatives!

---

## 📞 Support

- 📚 **Documentation**: This file + linked resources
- 💬 **Community**: Continue.dev Discord, Ollama Discord
- 🐛 **Issues**: GitHub issues in this repo
- 🆘 **Help**: Check troubleshooting section first

---

## 🎉 You're Ready!

Run the installer for your platform:

```bash
# Windows
.\INSTALL_AI_ORACLE_IDE.ps1

# Linux
./INSTALL_AI_ORACLE_IDE.sh

# macOS
./INSTALL_AI_ORACLE_IDE_MAC.sh
```

Then start coding with AI assistance - **100% free, 100% local, 100% open source!**

---

**Built with 💜 by the AI Oracle Team**

**Star ⭐ this repo if you love local AI!**

**Share this guide to help others break free from subscription hell!**
