# Kilo Code - Quick Reference Card

## Installation & Setup
```powershell
# Full installation
.\Setup-KiloCode.ps1

# Quick launcher menu
.\Start-KiloCode.bat
```

## Daily Use

### CLI Commands
```powershell
k                    # Start Kilo chat (shorthand)
kilo "task"         # One-off task
kilo --clear        # Clear history
kdebug "issue"      # Debug mode
kask "question"     # Ask mode (readonly)
kcode "implement"   # Code mode (default)
```

### Model Switching
```powershell
# Show available free models
.\Kilo-Utils.ps1 -ShowModels

# Change default model persistently
Set-KiloModel -Model ling-2.6-1t -Persist   # Best free (256K context)
Set-KiloModel -Model hy3 -Persist            # Configurable reasoning
Set-KiloModel -Model auto-free -Persist      # Auto-select best free

# Switch temporarily (per session)
kilo --model inclusionai/ling-2.6-1t:free "task"
```

### In-Chat Commands
```
/models              - Pick a model
/agents              - Switch agent mode
/clear               - Clear conversation
/approve             - Auto-approve next action
/code                - Switch to code agent
/debug               - Switch to debug agent
/ask                 - Switch to ask agent
/plan                - Switch to plan agent
/variant             - Select reasoning level
```

## Context Mentions

```
@file.ts             # Attach file
@folder/             # Attach folder (recursive)
@terminal            # Attach terminal output
@git-changes         # Attach uncommitted changes
@README.md           # Multiple files allowed
```

**Drag & Drop:** Drag files from Explorer into chat input

## Best Free Models (256K Context)

| Model | Rank | Use Case | Cost |
|-------|------|----------|------|
| Ling-2.6-1T | #9 Code / #3 Debug | General coding & debugging | FREE |
| Hy3 Preview | #17 Code | Configurable reasoning (low/high) | FREE |
| Nemotron 3 | #85 Code | Large 120B MoE model | FREE |
| Gemma 4 | N/A | Multimodal (image+text) | FREE |
| Step 3.5 Flash | #81 Code | Fast, low-cost paid option | $0.10/1M |

**Switch:** `/model inclusionai/ling-2.6-1t:free`

## zED Integration Hooks

### Project Context
```powershell
# Generate context file
New-KiloProjectContext -ProjectName "MyProject"

# Use with automatic context attachment
Invoke-KiloWithContext -Query "Refactor based on architecture"
```

### Diagnostics
```powershell
# Run full diagnostic
Test-KiloIntegration

# Check specific components
kilo --version
code --list-extensions | Select-String kilo
npm list -g @kilocode/cli
```

### Update
```powershell
# Update Kilo CLI
Update-Kilo

# Check for newer models
# Visit: https://kilo.ai/models
```

## VS Code Shortcuts

| Action | Shortcut |
|--------|----------|
| Open Kilo Chat | `Ctrl+Shift+P` → "Kilo: Focus" |
| Inline Chat | `Ctrl+Shift+I` |
| Inline Edit | Select code → `Cmd+.` (Mac) / `Ctrl+.` (Win) |
| Cycle Agents | `Cmd+.` (Mac) / `Ctrl+.` (Win/Linux) |
| Explain Code | Select code → Right-click → "Explain with Kilo" |
| Fix Error | Click lightbulb on error → "Fix with Kilo" |

## Agent Guide

### code (default)
- Full file read/write/edit
- Execute shell commands
- Run tests, git operations
- Best for: implementation, refactoring

### ask
- Read-only operations
- Explain code, search project
- No file modifications
- Best for: learning, investigation

### plan
- Design & architecture
- Creates files only in `.kilo/plans/`
- Strategic thinking
- Best for: system design, RFCs

### debug
- Systematic troubleshooting
- Full tool access
- Diagnostic-focused
- Best for: bugs, errors, crashes

**Switch:** Use dropdown or `/agents` command

## Advanced Usage

### Task Automation
```powershell
# Batch processing
Get-ChildItem -Recurse -Filter "*.py" | ForEach-Object {
    kilo "Add docstrings to $($_.FullName)"
}

# With approval
kilo run --auto "npm test && npm run build"
```

### Multi-File Context
```powershell
# Attach multiple files
kilo "Compare these implementations: @src/old.ts @src/new.ts"

# Attach entire directory (careful with size!)
kilo "Optimize all files in @src/utils/"
```

### System Prompt Customization
Create `.kilo/custom_instructions.md`:
```
You are an expert in:
- TypeScript/React
- Our codebase patterns (see @kilo_context.md)
- Performance optimization

Always write tests for new features.
```

## Troubleshooting

### CLI not found
```powershell
# Refresh PATH
$env:Path += ";${env:APPDATA}\npm"
# Restart PowerShell
```

### Extension not loading
1. `Ctrl+Shift+P` → "Developer: Reload Window"
2. Check logs: "View → Output → Extension Host"
3. Reinstall: `code --uninstall-extension kilocode.kilo-code`

### Rate limited
- Switch models: `/model tencent/hy3-preview:free`
- Wait 5-10 minutes
- Add API key for guaranteed access

### High memory
- Use auto-balanced tier: `Set-KiloModel -Model auto-balanced`
- Close other applications
- Reduce context window in settings

## Files Overview

```
zED-Workspace/
├── Setup-KiloCode.ps1      # Main installer
├── Kilo-Utils.ps1          # Utilities & helpers
├── Start-KiloCode.bat       # Interactive menu
├── KILO_SETUP_README.md    # Full documentation
├── KILO_QUICKSTART.md      # Quick start (generated)
├── kilo_context.md         # Project context (generated)
└── .config/kilo/
    └── config.json         # Kilo configuration
```

## Common Workflows

### New Feature
```
1. Plan:   kilo --agent plan "Design a notification system"
2. Code:   kilo --agent code "Implement notification system"
3. Debug:  kilo --agent debug "Fix race condition in notifications"
4. Ask:    kilo --agent ask "Why did we choose Redis?"
```

### Code Review
```
kilo "Review @src/auth.ts for security issues:
- Check for SQL injection
- Validate JWT handling
- Ensure proper authz"
```

### Refactoring
```
kilo "Refactor @legacy_module.py:
- Split into smaller functions
- Add type hints
- Update docstrings
- Preserve behavior"
```

### Debugging
```
1. Share error: "Fix this error: @error.log"
2. Attach code: "@problematic_file.cpp"
3. Run diagnostics: "What's causing the segfault?"
4. Apply fix: "Patch the issue"
```

## Config Locations

| Platform | Config Path |
|----------|-------------|
| Windows | `%USERPROFILE%\.config\kilo\config.json` |
| Linux | `~/.config/kilo/config.json` |
| Mac | `~/.config/kilo/config.json` |
| VS Code | Settings → Kilo Code |
| CLI | `kilo --config <path>` |

## Environment Variables

```powershell
# Override model
$env:KILO_MODEL = "inclusionai/ling-2.6-1t:free"

# Set default agent
$env:KILO_AGENT = "code"

# Custom config location
$env:KILO_CONFIG = "C:\path\to\custom-config.json"

# Debug logging
$env:KILO_DEBUG = "1"
```

## Performance Tips

1. **Use Ling-2.6-1T** for best free performance (256K, #9 rank)
2. **Attach only relevant files** - context is limited
3. **Batch tasks** - ask Kilo to create a script for repetitive work
4. **Use `--auto`** for CI/CD (no approvals)
5. **Clear history** with `kilo --clear` if context gets full

## Getting Help

```powershell
kilo --help                    # CLI help
.\Kilo-Utils.ps1               # Interactive menu
code --list-extensions         # Check VS Code extension
.\Kilo-Utils.ps1 -Diagnose     # Run diagnostics

# Online
https://kilo.ai/docs           # Official docs
https://kilo.ai/models         # Model leaderboard
https://kilo.ai/discord        # Discord community
```

## Cost Estimates (if using paid models)

| Model | Input Cost | Output Cost | 1M token session |
|-------|-----------|-------------|------------------|
| Claude Opus | $5.00 | $15.00 | $20.00 |
| Claude Sonnet | $3.00 | $15.00 | $18.00 |
| GPT-5.4 | $2.50 | $10.00 | $12.50 |
| Ling-2.6-1T | **$0.00** | **$0.00** | **$0.00** |
| Step 3.5 Flash | $0.10 | $0.30 | $0.40 |

**Annual savings with free model:** ~$5,000+ (based on 1M tokens/day)

---

**Setup Complete:** Run `.\Start-KiloCode.bat` to begin
