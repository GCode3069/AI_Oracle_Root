# Kilo Code AI Agent - zED IDE Integration

## Overview

This directory contains the complete Kilo Code AI coding agent setup for the zED IDE environment. Kilo is a fully open-source, agentic engineering platform that provides AI-powered coding assistance with support for 500+ models through the Kilo Gateway.

## Files in This Package

| File | Purpose |
|------|---------|
| `Setup-KiloCode.ps1` | Main installation script - installs CLI, config, VS Code extension |
| `Kilo-Utils.ps1` | Daily utilities: model switching, diagnostics, project context |
| `Start-KiloCode.bat` | Interactive launcher menu for quick access |
| `KILO_QUICKSTART.md` | Generated usage guide post-installation |

## Quick Start

### One-Command Installation
```powershell
.\Setup-KiloCode.ps1
```

### Launch Kilo
```powershell
# CLI interface
kilo

# Or use the launcher
.\Start-KiloCode.bat
```

## Configuration Details

### Free Model Selection (256K Context)

Kilo has been configured with the **best free models** offering the **largest context windows** (256K tokens):

| Model | Context | Code Rank | Debug Rank | Cost |
|-------|---------|-----------|------------|------|
| inclusionAI Ling-2.6-1T | 262K | #9 | #3 | FREE |
| Tencent Hy3 Preview | 262K | #17 | #15 | FREE |
| NVIDIA Nemotron 3 Super | 262K | #85 | #71 | FREE |
| Google Gemma 4 26B | 262K | N/A | N/A | FREE |
| StepFun Step 3.5 Flash | 262K | #81 | N/A | $0.10/1M |

**Default:** `kilo-auto/free` (auto-selects best available free model)

### Configuration Location
- **Windows:** `%USERPROFILE%\.config\kilo\config.json`
- **Linux/Mac:** `~/.config/kilo/config.json`

### Key Settings in Config
```json
{
  "model": "kilo-auto/free",
  "agent": {
    "code": { "model": "inclusionai/ling-2.6-1t:free" },
    "debug": { "model": "inclusionai/ling-2.6-1t:free" }
  },
  "small_model": "inclusionai/ling-2.6-1t:free"
}
```

## Usage Patterns

### 1. CLI Usage
```powershell
# Start interactive session
kilo

# Clear history
kilo --clear

# Auto-approve mode (CI/CD)
kilo run --auto "fix all lint errors"

# With specific model
kilo --model inclusionai/ling-2.6-1t:free "explain this code"
```

### 2. VS Code Integration
- Open any project folder
- Click Kilo icon in left sidebar
- Type `@filename` to attach files
- Drag files into chat
- Use `/code`, `/debug`, `/ask` agents

### 3. Quick Commands (Aliases)
```powershell
k          # Short for kilo
kcode      # Force Ling-2.6-1T model
kauto      # Use auto-free tier
kdebug     # Debug agent mode
kask       # Ask agent mode (read-only)
```

## Agent Types

| Agent | Purpose | Tool Access |
|-------|---------|-------------|
| **code** (default) | Write/edit code | Full read/write/execute |
| **ask** | Answer questions | Read-only |
| **plan** | Architecture/design | Read + plan files |
| **debug** | Troubleshoot issues | Full access |

Switch with `/agents` or `Ctrl+.`

## Context Management

### Attaching Files
```
@path/to/file.ts          # Attach file content
@terminal                  # Attach terminal output
@git-changes              # Attach uncommitted changes
```

### Automatic Context
- Current editor tabs
- Project structure
- Git history (when relevant)

**Best Practice:** Just describe what you need - Kilo searches the codebase automatically.

## Free Model Benefits

### Why Ling-2.6-1T?
- **Largest context** (256K tokens) among free models
- **Highest ranked** free model for coding (#9) and debugging (#3)
- **Zero cost** - completely free
- **Fast inference** - instant (instruct-tuned)
- **Production ready** - real-world agent optimized

### Cost Comparison
```
Claude Opus 4.6:  $5.00/1M tokens (top-tier paid)
GPT-5.4:         $2.50/1M tokens
Step 3.5 Flash:  $0.10/1M tokens (efficient paid)
Ling-2.6-1T:     $0.00/1M tokens (free, 256K context)
```

**Savings:** $0 - $5 per 1M tokens depending on usage.

## VS Code Setup Details

### Extension Features
- Inline chat (Ctrl+Shift+I)
- Code completions (Tab)
- Code actions (lightbulb menu)
- File mentions with `@`
- Agent switching dropdown

### Keyboard Shortcuts
- `Ctrl+Shift+P` → "Kilo: Focus on Kilo View"
- `Ctrl+Shift+I` → Inline chat
- `Cmd+.` (Mac) / `Ctrl+.` (Win/Linux) → Cycle agents
- `Cmd+Shift+I` / `Ctrl+Shift+I` → Inline edit

### Settings Sync
Kilo config syncs across VS Code, JetBrains, and CLI via the `~/.config/kilo/` directory.

## Advanced Configuration

### Using Your Own API Keys (BYOK)
For guaranteed availability and privacy:

1. **Mistral (Codestral)** - Free autocomplete
   ```
   Settings → Providers → Add "mistral"
   API Key: https://console.mistral.ai
   ```

2. **Anthropic/OpenAI** - Premium models with your credits
   ```
   Add provider key → Select premium model
   ```

### Custom Models
```json
{
  "model": "custom",
  "custom_models": {
    "my-finetuned": {
      "provider": "openrouter",
      "model_id": "my-org/my-model-v1"
    }
  }
}
```

### MCP Servers
Kilo can connect to Model Context Protocol servers in `./mcp_server/`:

```json
{
  "mcp": {
    "servers": {
      "local-tools": {
        "command": "python",
        "args": ["mcp_server/oracle_mcp_server.py"]
      }
    }
  }
}
```

## Troubleshooting

### CLI Not Found After Install
```powershell
# Restart PowerShell to refresh PATH
# Or manually:
$env:Path += ";${env:APPDATA}\npm"
```

### Rate Limits on Free Models
Free models have usage caps. If rate-limited:
1. Switch to another free model: `/model tencent/hy3-preview:free`
2. Wait a few minutes
3. Consider adding a paid provider key for premium models

### VS Code Extension Not Loading
1. Reload VS Code window (`Ctrl+R` or `Cmd+R`)
2. Check Extension view for Kilo Code
3. Run `Developer: Show Logs` → "Extension Host"
4. Reinstall: `code --uninstall-extension kilocode.kilo-code`

### High Memory Usage
Free models have larger context but higher memory:
- Close other applications
- Use smaller context if possible
- Switch to `kilo-auto/balanced` tier for more efficient models

## Integration with zED Workspace

### Existing Environment
This Kilo setup integrates with your existing:
- MCP servers in `./mcp_server/`
- Python virtual environment (`scarify_venv/`)
- Project scripts in root
- GitHub workflows

### Recommended Workflow
1. **Plan:** `kilo --agent plan "Design feature X"`
2. **Code:** `kilo --agent code "Implement feature X"`
3. **Debug:** `kilo --agent debug "Fix error in Y"`
4. **Learn:** `kilo --agent ask "Explain Z architecture"`

### Project Context File
The `kilo_context.md` file (auto-generated) contains:
- Project overview
- Key file inventory
- Architecture notes
- Dependencies
- Known issues

Reference with `@kilo_context.md` in chats.

## Performance Tips

### Best Free Model Matrix

| Task | Recommended Model |
|------|-------------------|
| Code generation | Ling-2.6-1T (#9) |
| Debugging | Ling-2.6-1T (#3 debug) |
| General questions | Ling-2.6-1T or Hy3 |
| Long files (1MB+) | Any 256K model |
| Fast & cheap | Step 3.5 Flash ($0.10) |
| Complex planning | Switch to auto-tier or premium |

### Prompt Engineering for 256K Context
Kilo can handle massive context. Use it:
```
Here's the full codebase. Find all security issues:

@path/to/large/file1.ts
@path/to/large/file2.ts
@path/to/large/file3.ts
```

### Batch Operations
Use CLI scripts for automation:
```powershell
# Process multiple files
Get-ChildItem -Path . -Filter "*.py" -Recurse | ForEach-Object {
    kilo "Add type hints to $($_.FullName)"
}
```

## Support & Resources

- **Documentation:** https://kilo.ai/docs
- **Model Leaderboard:** https://kilo.ai/models (live rankings)
- **Discord Community:** https://kilo.ai/discord
- **GitHub:** https://github.com/Kilo-Org/kilocode
- **Report Issues:** https://github.com/Kilo-Org/kilocode/issues

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `KILO_MODEL` | Override default model |
| `KILO_AGENT` | Default agent (code/ask/plan/debug) |
| `KILO_CONFIG` | Custom config path |

Example:
```powershell
$env:KILO_MODEL = "inclusionai/ling-2.6-1t:free"
kilo "Refactor this"
```

## Uninstall

```powershell
# Remove CLI
npm uninstall -g @kilocode/cli

# Remove config
Remove-Item "$env:USERPROFILE\.config\kilo" -Recurse -Force

# Remove VS Code extension
code --uninstall-extension kilocode.kilo-code
```

## License

Kilo Code is MIT Licensed. See LICENSE file in repository.

---

**Installation Date:** $(Get-Date -Format 'yyyy-MM-dd')
**Workspace:** zED IDE Environment
**Optimized for:** Largest free context (256K tokens)
**Primary Model:** inclusionAI Ling-2.6-1T (free)
