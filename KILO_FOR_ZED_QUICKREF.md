# Kilo Code for Zed Editor - Quick Reference

## Installation
```powershell
.\Setup-KiloCode-Zed.ps1
```
Then restart Zed.

## Launch Methods

### Method 1: Terminal Panel (Recommended)
1. In Zed: `Ctrl+` (backtick) to open terminal
2. Type: `kilo`
3. Chat with AI directly in terminal

### Method 2: Command Palette
1. `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Win/Linux)
2. Type "Kilo:"
3. Select:
   - **Kilo: Start AI Chat** - Full chat interface
   - **Kilo: Ask Question** - Q&A mode (read-only)
   - **Kilo: Debug Issue** - Debug mode
   - **Kilo: Code Task** - Coding mode

### Method 3: Desktop Shortcuts
- **Kilo (Terminal).lnk** - Opens PowerShell with Kilo
- **Zed + Kilo.lnk** - Launches Zed editor

## Quick Commands

### In Kilo Terminal
```powershell
# Start chatting
kilo "Create a React component"

# Attach files
@src/App.tsx "Add error handling"

# Multiple files
@auth.ts @api.ts "Review for security issues"

# Switch agents
/code   # Full read/write (default)
/ask    # Read-only Q&A
/debug  # Systematic troubleshooting
/plan   # Architecture/design

# Switch models
/model inclusionai/ling-2.6-1t:free    # Best free (256K)
/model tencent/hy3-preview:free        # Alternative free
/model stepfun/step-3.5-flash          # Cheap option

# Other
/clear            # Clear conversation history
/help             # Show all commands
```

### PowerShell Aliases (defined in Kilo-Utils.ps1)
```powershell
k          # = kilo (shortest)
kcode      # Force Ling-2.6-1T model
kauto      # Use auto-free tier
kdebug     # Debug agent mode
kask       # Ask agent (read-only)
```

## Best Free Models for Zed

| Rank | Model | Context | Use Case | Cost |
|------|-------|---------|----------|------|
| #9 | inclusionAI Ling-2.6-1T ⭐ | 256K | General coding & debugging | FREE |
| #17 | Tencent Hy3 Preview | 256K | Configurable reasoning | FREE |
| #85 | NVIDIA Nemotron 3 Super | 256K | Large MoE model | FREE |
| #81 | StepFun Step 3.5 Flash | 256K | Fast, cheap | $0.10/1M |

## Zed-Specific Workflow

### Split Terminal + Editor
```
┌─────────────────────────────────────┐
│  Editor (left)   │  Terminal (right)│
│                  │  kilo            │
│  @file.ts        │  > Add feature X  │
│                  │                  │
└─────────────────────────────────────┘
```

1. Open file in editor
2. Open terminal: `Ctrl+`
3. Run `kilo`
4. Type: `@current-file "your request"`

### Multi-File Context
```
kilo "Compare these implementations:
@src/old_parser.ts
@src/new_parser.ts
@tests/parser.test.ts"

# Kilo reads all 3 files + their relationships
```

### Debug Workflow
```
1. Copy error from Zed Problems panel
2. In terminal: kdebug "paste error here"
3. Attach relevant file: @problematic.rs
4. Kilo diagnoses and suggests fix
5. Apply changes in editor
```

## Configuration Files

| File | Location | Purpose |
|------|----------|---------|
| Kilo config | `%USERPROFILE%\.config\kilo\config.json` | Model selection, agents |
| Zed commands | `%APPDATA%\zed\settings\kilo_commands.json` | Custom palette commands |
| Project context | `./kilo_context.md` | Project metadata (auto-gen) |

## Customization

### Change Default Model
Edit `%USERPROFILE%\.config\kilo\config.json`:
```json
{
  "model": "inclusionai/ling-2.6-1t:free"
}
```

Or in-chat: `/model inclusionai/ling-2.6-1t:free`

### Add Project Context
```powershell
.\Kilo-Utils.ps1 -NewContext
```
Creates `kilo_context.md` with project overview.

### Zed Settings Integration
Add to `settings.json` (Zed):
```json
{
  "commands": [
    {
      "name": "kilo: quick fix",
      "caption": "Kilo: Quick Fix Selection",
      "run": "powershell.exe -Command \"kilo --agent code 'Fix selected code'\""
    }
  ]
}
```

## Troubleshooting Zed

**Kilo not in Command Palette:**
- Restart Zed (it loads commands on startup)
- Check: `%APPDATA%\zed\settings\kilo_commands.json` exists
- In Zed: `Ctrl+Shift+P` → "Zed: Reload Window"

**Terminal says 'kilo' not found:**
- Close and reopen terminal panel
- Or run: `refreshenv` (if using Chocolatey)
- Restart Zed (inherits PATH from shell)

**File attachments not working:**
- Use absolute paths or ensure file is saved
- Type full path: `@C:\path\to\file.ts`
- Or drag file into terminal (Zed supports this)

**High memory usage:**
- 256K context is large but powerful
- Close unused Zed tabs/terminals
- Switch to `kilo-auto/balanced` for smaller models

## Keyboard Shortcuts

| Action | Zed Shortcut |
|--------|--------------|
| Open terminal | `Ctrl+` |
| Command palette | `Ctrl+Shift+P` |
| Quick open file | `Ctrl+P` |
| Toggle sidebar | `Ctrl+B` |
| Split terminal | `Ctrl+Shift+` |

## Productivity Tips

1. **Terminal panes:** `Cmd+K` then `→` to split, run Kilo in right pane
2. **Quick file attach:** Type `@` then filename (autocomplete works)
3. **Session persistence:** Kilo context resets on `kilo` re-run; use `/clear` manually
4. **Batch operations:** Ask Kilo to create scripts, then run them
5. **Learn shortcuts:** Zed's command palette is fast - bind Kilo to a key

## Cost Breakdown

Using Ling-2.6-1T (free):
- **Daily:** $0.00
- **Monthly:** $0.00
- **Yearly:** $0.00

vs Paid alternatives:
- Claude Opus: $5,500/year (1M tokens/day)
- GPT-5.4: $2,750/year (1M tokens/day)

**Savings:** $2,750 - $5,500/year

## Getting Help

- **Kilo Docs:** https://kilo.ai/docs
- **Model Leaderboard:** https://kilo.ai/models
- **Zed Docs:** https://zed.dev/docs
- **Discord:** https://kilo.ai/discord
- **Local Guide:** `KILO_FOR_ZED.md`

## Uninstall

```powershell
npm uninstall -g @kilocode/cli
Remove-Item $env:USERPROFILE\.config\kilo -Recurse -Force
Remove-Item "$env:APPDATA\zed\settings\kilo_*" -Force
Remove-Item "$env:USERPROFILE\Desktop\Kilo*" -Force
```

---

**Ready:** After running `Setup-KiloCode-Zed.ps1`, restart Zed and press `Ctrl+Shift+P` → "Kilo: Start AI Chat"
