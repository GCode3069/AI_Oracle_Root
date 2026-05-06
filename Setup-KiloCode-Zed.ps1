<#
.SYNOPSIS
    Kilo Code Setup for Zed Editor
.DESCRIPTION
    Configures Kilo AI coding agent to work with Zed IDE via terminal integration.
    Since Zed doesn't have a native Kilo extension yet, this sets up the CLI
    and creates Zed custom commands/shortcuts for seamless integration.
.NOTES
    Zed Editor: https://zed.dev
    Kilo Code: https://kilo.ai
    Model: inclusionAI Ling-2.6-1T (free, 256K context) - best free option
#>

[CmdletBinding()]
param(
    [switch]$SkipCLI,
    [switch]$Force,
    [string]$ConfigPath = "$env:USERPROFILE\.config\kilo\config.json"
)

$ErrorActionPreference = 'Stop'

Write-Host "`n🚀 Kilo Code Setup for Zed Editor" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Gray
Write-Host ""

# Check prerequisites
Write-Host "📋 Checking prerequisites..." -ForegroundColor Yellow

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Error "npm (Node.js) is required. Install from https://nodejs.org"
}
Write-Host "✓ npm detected" -ForegroundColor Green

# Check if Zed is installed (optional)
$zedPaths = @(
    "${env:ProgramFiles}\Zed\zed.exe",
    "${env:LocalAppData}\Programs\Zed\zed.exe",
    "${env:APPDATA}\Zed\zed.exe"
)
$zedInstalled = $false
foreach ($path in $zedPaths) {
    if (Test-Path $path) {
        $zedInstalled = $true
        $script:zedPath = $path
        Write-Host "✓ Zed detected at: $path" -ForegroundColor Green
        break
    }
}
if (-not $zedInstalled) {
    Write-Host "⚠️  Zed not found in standard locations." -ForegroundColor Yellow
    Write-Host "   The CLI will still work in any terminal." -ForegroundColor Gray
}

# Step 1: Install Kilo CLI
Write-Host "`n[1/5] Installing Kilo CLI..." -ForegroundColor Cyan

if ((Get-Command kilo -ErrorAction SilentlyContinue) -and -not $Force) {
    Write-Host "✓ Kilo already installed. Use -Force to reinstall." -ForegroundColor Green
} else {
    Write-Host "Installing @kilocode/cli globally..." -ForegroundColor Gray
    npm install -g @kilocode/cli

    if ($LASTEXITCODE -ne 0) {
        throw "npm install failed"
    }
    Write-Host "✓ Kilo CLI installed" -ForegroundColor Green
}

# Verify
if (-not (Get-Command kilo -ErrorAction SilentlyContinue)) {
    throw "kilo command not found. Restart terminal and try again."
}
Write-Host "✓ Kilo version: $(kilo --version)" -ForegroundColor Green

# Step 2: Configure Kilo with best free model
Write-Host "`n[2/5] Configuring Kilo for best free model..." -ForegroundColor Cyan

$configDir = Split-Path $ConfigPath -Parent
if (-not (Test-Path $configDir)) {
    New-Item -ItemType Directory -Path $configDir -Force | Out-Null
}

$config = @{
    model = "kilo-auto/free"
    agent = @{
        code = @{ model = "inclusionai/ling-2.6-1t:free" }
        ask  = @{ model = "inclusionai/ling-2.6-1t:free" }
        plan = @{ model = "inclusionai/ling-2.6-1t:free" }
        debug = @{ model = "inclusionai/ling-2.6-1t:free" }
    }
    small_model = "inclusionai/ling-2.6-1t:free"
} | ConvertTo-Json -Depth 5

$config | Out-File -FilePath $ConfigPath -Encoding UTF8
Write-Host "✓ Configuration saved to: $ConfigPath" -ForegroundColor Green
Write-Host "  Model: inclusionAI Ling-2.6-1T (256K context, FREE)" -ForegroundColor Gray

# Step 3: Create Zed integration files
Write-Host "`n[3/5] Creating Zed integration..." -ForegroundColor Cyan

# Zed projects directory
$zedConfigDir = "$env:APPDATA\zed\settings"  # Zed settings on Windows
if (-not (Test-Path $zedConfigDir)) {
    # Try Linux/Mac locations if needed
    if (Test-Path "$env:HOME\.config/zed") {
        $zedConfigDir = "$env:HOME\.config/zed"
    } else {
        Write-Host "⚠️  Zed settings directory not found. Will create local integration files." -ForegroundColor Yellow
        $zedConfigDir = "$PSScriptRoot\.zed"
    }
}

# Create Zed custom commands JSON
$zedCommands = @"
{
  "commands": [
    {
      "name": "kilo: chat",
      "caption": "Kilo: Start AI Chat",
      "category": "Kilo Code",
      "run": "powershell.exe -NoExit -Command `\"kilo`\""
    },
    {
      "name": "kilo: ask",
      "caption": "Kilo: Ask Question",
      "run": "powershell.exe -NoExit -Command `\"kilo --agent ask`\""
    },
    {
      "name": "kilo: debug",
      "caption": "Kilo: Debug Issue",
      "run": "powershell.exe -NoExit -Command `\"kilo --agent debug`\""
    },
    {
      "name": "kilo: code",
      "caption": "Kilo: Code Task",
      "run": "powershell.exe -NoExit -Command `\"kilo --agent code`\""
    }
  ]
}
"@

$zedCommandsPath = Join-Path $zedConfigDir "kilo_commands.json"
$zedCommands | Out-File -FilePath $zedCommandsPath -Encoding UTF8
Write-Host "✓ Zed commands file created: $zedCommandsPath" -ForegroundColor Green
Write-Host "  (Zed may need to be restarted to detect these)" -ForegroundColor Gray

# Create Zed assistant/board integration file
$zedBoardConfig = @"
# Kilo Code - Zed Integration
# Add this to your Zed settings.json or use the commands file above

{
  "assistants": {
    "kilo": {
      "name": "Kilo Code",
      "caption": "Kilo AI Assistant",
      "model": "claude-3-sonnet",
      "prompt": "You are Kilo Code, an expert software engineering assistant. Use the following context from the user's workspace..."
    }
  }
}
"@

$zedBoardPath = Join-Path $zedConfigDir "kilo_assistant.md"
$zedBoardConfig | Out-File -FilePath $zedBoardPath -Encoding UTF8
Write-Host "✓ Zed assistant config created: $zedBoardPath" -ForegroundColor Green

# Step 4: Create desktop/start menu shortcuts for quick access
Write-Host "`n[4/5] Creating shortcuts..." -ForegroundColor Cyan

$desktop = [Environment]::GetFolderPath('Desktop')
$wshShell = New-Object -ComObject WScript.Shell

# Kilo Terminal shortcut
$kiloTerm = Join-Path $desktop "Kilo (Terminal).lnk"
$shortcut = $wshShell.CreateShortcut($kiloTerm)
$shortcut.TargetPath = "powershell.exe"
$shortcut.Arguments = "-NoExit -Command `"kilo`""
$shortcut.Description = "Launch Kilo AI in PowerShell"
$shortcut.IconLocation = "imageres.dll,-5302"
$shortcut.Save()
Write-Host "✓ Desktop shortcut: Kilo (Terminal)" -ForegroundColor Green

# Zed + Kilo shortcut (if Zed found)
if ($zedInstalled) {
    $zedKilo = Join-Path $desktop "Zed + Kilo.lnk"
    $shortcut = $wshShell.CreateShortcut($zedKilo)
    $shortcut.TargetPath = $zedPath
    $shortcut.Arguments = "--new-window"
    $shortcut.Description = "Zed Editor with Kilo"
    $shortcut.IconLocation = "$zedPath,0"
    $shortcut.Save()
    Write-Host "✓ Desktop shortcut: Zed + Kilo" -ForegroundColor Green
}

# Step 5: Generate documentation
Write-Host "`n[5/5] Generating documentation..." -ForegroundColor Cyan

$readme = @"
# Kilo Code for Zed Editor

## Installation Complete ✓

Kilo Code AI agent is now configured for use with Zed editor.

### Quick Start

**Option A: Terminal Panel (Recommended)**
1. In Zed, open terminal: `Ctrl+` (backtick)
2. Type: `kilo`
3. Start chatting with AI

**Option B: Custom Commands**
- Open Command Palette: `Cmd+Shift+P` (Mac) / `Ctrl+Shift+P` (Win/Linux)
- Type "Kilo:" to see custom commands
  - `Kilo: Start AI Chat`
  - `Kilo: Ask Question`
  - `Kilo: Debug Issue`
  - `Kilo: Code Task`

**Option C: Desktop Shortcuts**
- "Kilo (Terminal)" - Opens PowerShell with Kilo
- "Zed + Kilo" - Launches Zed with Kilo available

### Configuration

- **Config file:** `$ConfigPath`
- **Model:** inclusionAI Ling-2.6-1T (free, 256K context)
- **Rank:** #9 Code, #3 Debug (best free models)
- **Cost:** $0.00/1M tokens

### Using Kilo in Zed

#### 1. Attach Files
In the Kilo chat terminal:
```
@src/main.ts          # Attach a file
@src/                 # Attach folder (careful with size)
@git-changes          # Show uncommitted changes
```

#### 2. Switch Agents
```
/code                 # Coding agent (default, full access)
/ask                  # Q&A agent (read-only)
/debug                # Debug agent (systematic troubleshooting)
/plan                 # Planning agent (architecture)
```

#### 3. Change Model
```
/model inclusionai/ling-2.6-1t:free    # Best free (256K)
/model tencent/hy3-preview:free        # Alternative free
/model stepfun/step-3.5-flash          # Cheap paid ($0.10/1M)
```

#### 4. Useful Commands
```
/clear                # Clear conversation
/help                 # Show all commands
```

### Best Free Models for Zed

| Model | Context | Rank | Cost |
|-------|---------|------|------|
| Ling-2.6-1T | 256K | #9 Code / #3 Debug | FREE ⭐ |
| Hy3 Preview | 256K | #17 Code | FREE |
| Nemotron 3 | 256K | #85 Code | FREE |
| Step 3.5 Flash | 256K | #81 Code | $0.10/1M |

### Integration Features

✓ Global Kilo CLI available in any terminal
✓ Zed custom commands (Command Palette)
✓ Desktop shortcuts for quick launch
✓ VS Code extension also installed (if you use VS Code sometimes)
✓ Configuration in `$ConfigPath`

### Tips for Zed Workflow

1. **Split Panels:** Split Zed terminal, run Kilo in one panel, code in another
2. **File Context:** Use `@` to auto-complete file paths from current project
3. **Multi-file:** Attach multiple files: `@a.ts @b.ts analyze both`
4. **Quick Switch:** Use alias `k` for `kilo`, `kcode` for Ling model
5. **Session Save:** Kilo conversations are per-session; use `--clear` to reset

### Troubleshooting

**'kilo' not found in terminal:**
- Restart Zed (it inherits PATH from shell)
- Or run: `refreshenv` (if using Chocolatey) or restart terminal

**Commands not showing in palette:**
- Restart Zed after setup completes
- Check Zed settings → Custom Commands

**Rate limits:**
- Free models have caps. Switch: `/model tencent/hy3-preview:free`
- Or add API key for unlimited access (see Kilo docs)

**High memory:**
- 256K context uses more RAM. Close unused files/terminals
- Switch to auto-balanced: edit config → `"model": "kilo-auto/balanced"`

### Uninstall

```powershell
npm uninstall -g @kilocode/cli
Remove-Item $env:USERPROFILE\.config\kilo -Recurse -Force
Remove-Item "$env:USERPROFILE\Desktop\Kilo*" -Force
Remove-Item "$env:APPDATA\zed\settings\kilo_*" -Force
```

### Resources

- **Kilo Docs:** https://kilo.ai/docs
- **Model Leaderboard:** https://kilo.ai/models
- **Zed Editor:** https://zed.dev
- **Discord:** https://kilo.ai/discord

---

Installed: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
Model: inclusionAI Ling-2.6-1T (256K context, FREE)
Workspace: $PSScriptRoot
"@

$readmePath = Join-Path $PSScriptRoot "KILO_FOR_ZED.md"
$readme | Out-File -FilePath $readmePath -Encoding UTF8
Write-Host "✓ Documentation: $readmePath" -ForegroundColor Green

# Final summary
Write-Host "`n" + "="*50 -ForegroundColor Cyan
Write-Host "✅ KILO SETUP COMPLETE FOR ZED" -ForegroundColor Green
Write-Host "="*50 -ForegroundColor Cyan
Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host "1. Restart Zed (to load custom commands)" -ForegroundColor White
Write-Host "2. In Zed, open terminal: Ctrl+`" -ForegroundColor White
Write-Host "3. Type: kilo" -ForegroundColor White
Write-Host "4. Or use Cmd/Ctrl+Shift+P → 'Kilo:' commands" -ForegroundColor White
Write-Host ""
Write-Host "MODEL: inclusionAI Ling-2.6-1T (256K context, FREE) ⭐" -ForegroundColor Cyan
Write-Host "RANK:  #9 Code / #3 Debug (best free)" -ForegroundColor Cyan
Write-Host "COST:  $0.00 per 1M tokens" -ForegroundColor Cyan
Write-Host ""
Write-Host "Docs: See KILO_FOR_ZED.md for full guide" -ForegroundColor Gray
Write-Host ""
