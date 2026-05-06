# Kilo Code - zED IDE Integration Manifest

**Version:** 1.0.0
**Target:** zED IDE Environment
**Install Date:** 2026-05-06
**Primary Model:** inclusionAI Ling-2.6-1T (free, 256K context)
**Fallback Model:** kilo-auto/free

---

## Package Contents

| File | Size | Purpose |
|------|------|---------|
| `Setup-KiloCode.ps1` | 13 KB | Main installation script |
| `Kilo-Utils.ps1` | 12 KB | Daily utilities & helpers |
| `Start-KiloCode.bat` | 3 KB | Interactive launcher menu |
| `KILO_SETUP_README.md` | 8 KB | Comprehensive documentation |
| `KILO_QUICK_REFERENCE.md` | 7 KB | Quick reference card |
| `INTEGRATION_MANIFEST.md` | This | Integration metadata |

## System Requirements

| Component | Requirement |
|-----------|-------------|
| OS | Windows 10+ / PowerShell 5.1+ |
| Node.js | v18+ (for npm) |
| npm | Global package manager |
| VS Code | Optional (v1.70+) for IDE extension |
| Internet | Required for AI inference |

## Integration Points

### 1. VS Code Extension
- **Extension ID:** `kilocode.kilo-code`
- **Install Path:** `%USERPROFILE%\.vscode\extensions\`
- **Features:**
  - Sidebar chat panel
  - Inline completions
  - Code actions (lightbulb)
  - File drag & drop
  - MCP server support

### 2. CLI Global Installation
- **Package:** `@kilocode/cli`
- **npm Global Prefix:** `%APPDATA%\npm`
- **Binary:** `kilo.exe` in PATH
- **Config:** `%USERPROFILE%\.config\kilo\config.json`

### 3. MCP Server Integration
Workspace MCP servers detected in `./mcp_server/`:
- `oracle_mcp_server.py` - Oracle tools
- `Enable-VoiceControl.ps1` - Voice commands
- `Enable-CopilotVoice.ps1` - Copilot voice integration

Register in Kilo config under `mcp.servers` to enable.

### 4. Desktop Integration
Shortcuts created on desktop:
- "Kilo Code CLI" → PowerShell `kilo`
- "VS Code + Kilo" → VS Code (if installed)

### 5. Start Menu
- Programs → Kilo Code → Documentation
- Programs → Kilo Code → CLI Launcher

## Model Configuration

### Primary Model: inclusionAI Ling-2.6-1T (FREE) ⭐ RECOMMENDED
- **Provider:** inclusionAI via OpenRouter
- **Context Window:** 262,144 tokens (256K) ← Largest free context
- **Max Output:** 32,768 tokens
- **Pricing:** $0.00 / 1M tokens (completely free)
- **Kilo Leaderboard:** #9 Code mode, #3 Debug mode
- **Best For:** General coding, debugging, multi-file analysis

### Auto Fallback: kilo-auto/free
Automatically routes to best available free model if Ling-2.6-1T unavailable.

### Other Free Models (256K context)
1. **Tencent Hy3 Preview** - #17 Code rank, configurable reasoning levels
2. **NVIDIA Nemotron 3 Super** - #85 Code rank, 120B MoE architecture, 12B active
3. **Google Gemma 4 26B** - Multimodal (image + text), newest

### Paid Models (if you add API keys later)
| Model | Context | Strength | Cost |
|-------|---------|----------|------|
| Claude Opus 4.6 | 200K | Complex planning | $5.00/1M |
| GPT-5.4 | 922K input | Longest context | $2.50/1M |
| Claude Sonnet 4.6 | 200K | Balanced | $3.00/1M |

## Automated Installation Checks

The `Setup-KiloCode.ps1` script validates:
- [x] npm installed and available in PATH
- [x] Node.js version compatibility
- [x] Write permissions to `%USERPROFILE%\.config\`
- [x] VS Code detection (if present)
- [x] Existing Kilo installation (skip if found)
- [x] Network connectivity to kilo.ai

## Post-Installation Checklist

### Required
- [ ] Run `.\Setup-KiloCode.ps1` as Administrator
- [ ] Restart PowerShell to refresh PATH
- [ ] Test: `kilo --version`
- [ ] If VS Code installed: Verify extension with `code --list-extensions`

### Recommended
- [ ] Generate project context: `.\Kilo-Utils.ps1` → option 5
- [ ] Set preferred model (see Quick Reference)
- [ ] Join Kilo Discord: https://kilo.ai/discord
- [ ] Bookmark model leaderboard: https://kilo.ai/models

### Optional Enhancements
- [ ] Add Mistral API key for free autocomplete (BYOK method)
- [ ] Configure additional MCP servers from `./mcp_server/`
- [ ] Create custom agent rules in `.kilo/`
- [ ] Enable auto-approve for CI/CD with `kilo run --auto`

## Usage Workflow

### Typical Development Session
```
1. Open VS Code (or run .\Start-KiloCode.bat)
2. Kilo sidebar activates automatically
3. Attach relevant files: @src/MyComponent.tsx @tests/
4. Issue request: "Add comprehensive error handling"
5. Review AI changes, approve edits
6. Commit: git commit -m "feat: enhanced error handling"
```

### Complex Multi-Agent Workflow
```
Phase 1 - PLAN:   /plan → "Design scalable caching architecture"
Phase 2 - CODE:   /code → "Implement Redis cache layer"
Phase 3 - DEBUG:  /debug → "Diagnose memory leak in cache"
Phase 4 - ASK:    /ask → "Explain TTL eviction strategies"
```

## Quick Commands

```powershell
# Start interactive mode
kilo

# One-off task with specific model
kilo --model inclusionai/ling-2.6-1t:free "task description"

# Clear conversation history
kilo --clear

# Debug mode
kdebug "error message"

# Auto-approve (CI/CD)
kilo run --auto "npm test && npm run build"
```

**Aliases defined in Kilo-Utils.ps1:**
- `k` = `kilo`
- `kcode` = force Ling-2.6-1T model
- `kauto` = auto-free tier
- `kdebug` = debug agent
- `kask` = ask agent

## Troubleshooting Matrix

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| `kilo: command not found` | PATH not refreshed | Restart PowerShell / reopen terminal |
| Extension not loading | VS Code needs reload | `Ctrl+Shift+P` → "Developer: Reload Window" |
| Rate limit errors | Free model usage cap | Switch to another free model via `/model` |
| High memory usage | Large context window | Use `kilo-auto/balanced` or close tabs |
| No inline completions | Provider misconfigured | Check Settings → Kilo → Inline Completions |
| Context full | Token limit exceeded | Use `/clear` or start new session |

## Uninstall

```powershell
# Remove CLI
npm uninstall -g @kilocode/cli

# Remove config
Remove-Item $env:USERPROFILE\.config\kilo -Recurse -Force

# Remove VS Code extension
code --uninstall-extension kilocode.kilo-code

# Remove desktop shortcuts
Remove-Item "$env:USERPROFILE\Desktop\Kilo Code CLI.lnk" -Force

# Delete integration files (this package)
# Remove all .ps1, .bat, .md files from this directory
```

## Support Resources

| Resource | Purpose |
|----------|---------|
| Official Docs | https://kilo.ai/docs |
| Model Leaderboard | https://kilo.ai/models (live rankings) |
| Discord Community | https://kilo.ai/discord |
| GitHub Issues | https://github.com/Kilo-Org/kilocode/issues |
| VS Code Marketplace | https://marketplace.visualstudio.com/items?itemName=kilocode.kilo-code |

## Version History

- **v1.0.0** (2026-05-06) - Initial zED IDE integration package

## License

Kilo Code is released under the MIT License.
See the LICENSE file in the Kilo repository.

---

**Status:** ✅ Ready for Installation

**Installation Command:**
```powershell
.\Setup-KiloCode.ps1
```

**Quick Launch:**
```powershell
.\Start-KiloCode.bat
# or
kilo
```

**Need Help?** See `KILO_QUICK_REFERENCE.md` for command cheat sheet
