# zED IDE - Kilo Code AI Integration

## Overview

Complete Kilo Code AI agent setup for the zED development environment. This package provides **free** AI coding assistance with the **largest available context window** (256K tokens) via inclusionAI Ling-2.6-1T model — ranked #9 for coding and #3 for debugging among all free models.

## Installation

```powershell
# One-line install (run as Administrator)
.\Setup-KiloCode.ps1

# Or use the interactive menu
.\Start-KiloCode.bat
```

After installation, restart PowerShell and run:
```powershell
kilo
```

## What's Included

### 📜 Scripts
- **Setup-KiloCode.ps1** - Automated installation (CLI, VS Code extension, config, shortcuts)
- **Kilo-Utils.ps1** - Daily utilities (model switching, diagnostics, project context)
- **Start-KiloCode.bat** - Interactive launcher menu

### 📚 Documentation
- **KILO_SETUP_README.md** - Comprehensive setup & usage guide
- **KILO_QUICK_REFERENCE.md** - One-page command cheat sheet
- **INTEGRATION_MANIFEST.md** - Technical integration details
- **KILO_INSTALLATION_SUMMARY.txt** - Visual summary & cost comparison

## Key Features

✅ **Completely Free** - Zero token costs, no subscriptions
✅ **256K Context** - Largest free context window available
✅ **Top-Ranked** - #9 coding, #3 debugging among free models
✅ **Full Integration** - VS Code, CLI, desktop shortcuts
✅ **MCP Ready** - Integrates with existing MCP servers
✅ **Yearly Savings** - $2,750 - $5,500+ vs paid models

## Model Comparison

| Model | Context | Code Rank | Cost | Annual (1M/day) |
|-------|---------|-----------|------|-----------------|
| inclusionAI Ling-2.6-1T | 256K | #9 | **FREE** | **$0** |
| Claude Opus 4.6 | 200K | #1 | $5.00/1M | $5,500 |
| GPT-5.4 | 922K | #3 | $2.50/1M | $2,750 |
| Step 3.5 Flash | 256K | #81 | $0.10/1M | $110 |

→ **We recommend Ling-2.6-1T for all daily coding tasks**

## Quick Commands

```powershell
k                  # Start Kilo chat
kcode              # Force Ling-2.6-1T (256K context)
kauto              # Use auto-free tier
kdebug "error"     # Debug agent
kask "question"    # Ask agent (readonly)

# Switch models in-chat
/model inclusionai/ling-2.6-1t:free
```

## Usage Examples

### Basic Coding
```powershell
kilo "Create a React component with TypeScript"
```

### File Context
```powershell
kilo "Add error handling to @src/utils.ts"
```

### Multi-file Analysis
```powershell
kilo "Review these files for security issues: @auth.ts @api/endpoints.ts"
```

### Debugging
```powershell
kdebug "Fix this error: [paste error message]"
```

## Integration Points

- **VS Code Extension** - Sidebar chat, inline completions, code actions
- **CLI Global** - `kilo` command available anywhere
- **Desktop Shortcuts** - Quick launch from desktop
- **MCP Servers** - Connects to `./mcp_server/` tools
- **Project Context** - Auto-generates `kilo_context.md` for better AI awareness

## File Locations

| Item | Path |
|------|------|
| Kilo config | `%USERPROFILE%\.config\kilo\config.json` |
| Desktop shortcuts | `%USERPROFILE%\Desktop\` |
| VS Code extension | `%USERPROFILE%\.vscode\extensions\kilocode.kilo-code` |
| Global CLI | `%APPDATA%\npm\node_modules\@kilocode\cli` |

## Support

- **Documentation:** https://kilo.ai/docs
- **Model Leaderboard:** https://kilo.ai/models (see live rankings)
- **Community:** https://kilo.ai/discord
- **Issues:** https://github.com/Kilo-Org/kilocode/issues

## Uninstall

```powershell
npm uninstall -g @kilocode/cli
Remove-Item $env:USERPROFILE\.config\kilo -Recurse -Force
code --uninstall-extension kilocode.kilo-code
```

---

**Status:** Ready for installation | Run `.\Setup-KiloCode.ps1` to begin
