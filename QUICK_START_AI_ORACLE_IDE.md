# 🚀 AI Oracle IDE - Quick Start Guide

**Build your own local Cursor alternative in under 15 minutes!**

---

## 🎯 What Is This?

Turn your PC into a **powerful AI coding assistant** that:
- Runs **100% locally** (no cloud, no subscriptions)
- Uses **free, open-source** tools
- Provides **AI code completion** like GitHub Copilot
- Has **AI chat** for code help
- Works **offline** after setup
- Integrates with your **existing MCP servers**

**Total Cost**: $0
**Monthly Cost**: $0
**Privacy**: 100% (everything stays on your machine)

---

## ⚡ One-Command Installation

### Windows (PowerShell as Administrator)
```powershell
.\INSTALL_AI_ORACLE_IDE.ps1
```

### Linux
```bash
chmod +x INSTALL_AI_ORACLE_IDE.sh
./INSTALL_AI_ORACLE_IDE.sh
```

### macOS
```bash
chmod +x INSTALL_AI_ORACLE_IDE_MAC.sh
./INSTALL_AI_ORACLE_IDE_MAC.sh
```

**That's it!** The script installs everything automatically.

---

## 📦 What Gets Installed

1. **VSCodium** - Open-source VS Code (no Microsoft telemetry)
2. **Ollama** - Run AI models locally
3. **AI Models** - DeepSeek Coder, CodeLlama, Llama 3.2
4. **Continue.dev** - AI assistant extension (like Cursor)
5. **Extensions** - Python, ESLint, GitLens, etc.

**Download Size**: ~10-15GB (mostly AI models)
**Disk Space Needed**: ~20GB
**Installation Time**: 10-30 minutes (depends on internet)

---

## 🎮 How to Use After Installation

### Launch VSCodium
```bash
codium
```

Or find "VSCodium" in your applications menu.

### Open Your Project
```bash
codium /path/to/your/project
```

### AI Features

**1. AI Chat**
- Press `Ctrl+L` (Windows/Linux) or `Cmd+L` (Mac)
- Ask anything: "Explain this function", "Add error handling", etc.

**2. Auto-Complete**
- Just start typing code
- AI suggests completions
- Press `Tab` to accept

**3. Inline Editing**
- Select code
- Press `Ctrl+I` (Windows/Linux) or `Cmd+I` (Mac)
- Type what you want: "Add logging", "Make async", etc.

**4. Slash Commands**
In the AI chat, type `/` to see commands:
- `/edit` - Edit selected code
- `/comment` - Add comments
- `/test` - Generate tests
- `/commit` - Generate commit message
- `/cmd` - Generate shell command

---

## 💡 Quick Examples

### Example 1: Get Code Explanation
```
1. Select some code
2. Press Ctrl+L (AI chat)
3. Type: "Explain what this does"
4. AI explains it!
```

### Example 2: Auto-Complete
```python
def calculate_   # Just type this and pause
# AI suggests: calculate_fibonacci(n):
# Press Tab to accept!
```

### Example 3: Refactor Code
```
1. Select messy code
2. Press Ctrl+I (inline edit)
3. Type: "Refactor to be cleaner"
4. AI rewrites it!
```

### Example 4: Generate Tests
```
1. Select a function
2. Press Ctrl+L
3. Type: /test
4. AI generates unit tests!
```

---

## 🔧 System Requirements

**Minimum**:
- RAM: 8GB
- Storage: 20GB free
- CPU: Quad-core
- OS: Windows 10+, Linux, macOS 10.15+

**Recommended**:
- RAM: 16-32GB (better performance)
- Storage: 50GB free (SSD preferred)
- CPU: 6+ cores
- GPU: Optional (speeds up AI)

---

## 🆚 vs. Cursor IDE

| Feature | AI Oracle IDE | Cursor |
|---------|---------------|---------|
| Cost | **FREE** | $20/month |
| Privacy | **100% Local** | Cloud |
| Offline | **Yes** | No |
| Speed | Fast | Network dependent |
| Customizable | **Fully** | Limited |
| Models | Any | Claude/GPT-4 only |
| Open Source | **Yes** | No |

---

## 🎓 Learning Path

### Day 1: Setup & Basics
1. Run installer
2. Launch VSCodium
3. Try AI chat (Ctrl+L)
4. Try autocomplete

### Day 2: Daily Coding
1. Use AI for real project
2. Generate tests with `/test`
3. Get explanations for complex code
4. Use inline editing (Ctrl+I)

### Week 1: Advanced
1. Try different AI models
2. Create custom commands
3. Configure shortcuts
4. Integrate with MCP servers

---

## 🐛 Troubleshooting

### AI Not Responding?
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not, start it
ollama serve
```

### Slow Completions?
- Use smaller model for autocomplete
- Close other heavy apps
- Check Ollama is using correct model

### Can't Find VSCodium?
```bash
# Linux
which codium

# Windows
where codium

# Mac
which codium
```

If not found, add to PATH or reinstall.

---

## 📚 Full Documentation

For detailed docs, see:
- **LOCAL_CURSOR_ALTERNATIVE_GUIDE.md** - Complete guide
- **Continue.dev docs**: https://continue.dev/docs
- **Ollama docs**: https://ollama.ai/docs
- **VSCodium**: https://vscodium.com

---

## 🎯 Pro Tips

**1. Switch Models by Task**
- Autocomplete: Use fastest (1.3B model)
- Chat: Use balanced (6.7B model)
- Complex tasks: Use largest (13B+ model)

**2. Index Your Codebase**
- Command Palette (`Ctrl+Shift+P`)
- "Continue: Index Codebase"
- Now AI understands your whole project!

**3. Use @-mentions in Chat**
```
@filename.py Explain this module
@folder/ How does authentication work?
```

**4. Custom Commands**
Add your own shortcuts in Continue config!

**5. Keep Models Updated**
```bash
ollama pull deepseek-coder:6.7b
ollama pull codellama:7b
```

---

## 🔒 Privacy

**What Stays Local**:
- ✅ All AI models
- ✅ All your code
- ✅ All conversations
- ✅ All context
- ✅ Everything!

**What Leaves Your Machine**:
- ❌ Nothing

Unlike Cursor, GitHub Copilot, or ChatGPT - your code **never** leaves your computer!

---

## 💰 Cost Comparison

**AI Oracle IDE (This Setup)**:
- Installation: $0
- Monthly: $0
- Annual: $0
- **Total**: $0

**Cursor IDE**:
- Monthly: $20
- Annual: $240
- **Total**: $240/year

**GitHub Copilot**:
- Monthly: $10
- Annual: $100
- **Total**: $100/year

**Savings with AI Oracle IDE**: $100-240/year!

---

## 🚀 Next Steps

1. **Install** - Run the installer script
2. **Launch** - Open VSCodium
3. **Code** - Start using AI features
4. **Learn** - Read full guide for advanced features
5. **Customize** - Make it yours!

---

## 📞 Support

- **Issues**: Check troubleshooting section
- **Community**: Continue.dev Discord
- **Docs**: See full guide
- **Models**: Ollama library

---

## 🎉 You're Ready!

Run the installer and start coding with AI - **100% free, 100% local!**

**Questions?** Read the full guide: `LOCAL_CURSOR_ALTERNATIVE_GUIDE.md`

**Happy Coding! 🤖**
