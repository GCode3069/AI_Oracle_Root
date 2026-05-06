<#
.SYNOPSIS
    Complete Kilo Code Setup & Integration for Development Environment
.DESCRIPTION
    Configures Kilo AI coding agent with optimal free models (largest context window)
    - Installs Kilo CLI globally
    - Configures Auto Free model routing
    - Sets up VS Code extension (if available)
    - Creates desktop/start menu shortcuts
    - Configures background task models
    - Validates installation
.NOTES
    File:      Install-KiloCode.ps1
    Author:    Kilo Integration Script
    Requires:  PowerShell 5.1+, Node.js/npm (for CLI install)
#>

#Requires -Version 5.1

[CmdletBinding()]
param(
    [switch]$SkipVS CodeExtension,
    [switch]$ForceInstall,
    [string]$CustomConfigPath = "$env:USERPROFILE\.config\kilo\config.json"
)

$ErrorActionPreference = 'Stop'
$Script:KilVersion = "latest"
$Script:KiloCLIPackage = "@kilocode/cli"
$Script:VSCodeExtensionId = "kilocode.kilo-code"

#region Helper Functions

function Write-KiloStatus {
    param(
        [string]$Message,
        [ValidateSet('Info','Success','Warning','Error')]
        [string]$Level = 'Info'
    )
    $timestamp = Get-Date -Format "HH:mm:ss"
    $prefix = "[$timestamp] [KILO]"

    switch ($Level) {
        'Success' { Write-Host "$prefix ✅ $Message" -ForegroundColor Green }
        'Warning' { Write-Host "$prefix ⚠️  $Message" -ForegroundColor Yellow }
        'Error'   { Write-Host "$prefix ❌ $Message" -ForegroundColor Red }
        default   { Write-Host "$prefix ℹ️  $Message" -ForegroundColor Cyan }
    }
}

function Test-CommandExists {
    param([string]$Command)
    try {
        $null = Get-Command $Command -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

function Ensure-Directory {
    param([string]$Path)
    if (-not (Test-Path $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
        Write-KiloStatus "Created directory: $Path" 'Info'
    }
}

#endregion

#region Main Installation

try {
    Write-KiloStatus "====================================" 'Info'
    Write-KiloStatus "KILO CODE SETUP INITIATED" 'Info'
    Write-KiloStatus "====================================" 'Info'
    Write-KiloStatus "Target IDE: zED Development Environment" 'Info'
    Write-KiloStatus "Optimizing for: Largest free context (256K tokens)" 'Info'
    Write-KiloStatus ""

    # Check prerequisites
    Write-KiloStatus "Checking prerequisites..." 'Info'

    if (-not (Test-CommandExists 'npm')) {
        throw "npm (Node.js) is required. Install from https://nodejs.org/"
    }
    Write-KiloStatus "✓ npm detected" 'Success'

    # Check for VS Code
    $vscodePaths = @(
        "${env:ProgramFiles}\Microsoft VS Code\Code.exe",
        "${env:ProgramFiles(x86)}\Microsoft VS Code\Code.exe",
        "${env:LocalAppData}\Programs\Microsoft VS Code\Code.exe"
    )
    $vscodeInstalled = $false
    foreach ($path in $vscodePaths) {
        if (Test-Path $path) {
            $vscodeInstalled = $true
            $script:vscodePath = $path
            Write-KiloStatus "✓ VS Code detected at: $path" 'Success'
            break
        }
    }

    if (-not $vscodeInstalled) {
        Write-KiloStatus "⚠️  VS Code not found. CLI-only installation." 'Warning'
    }

    # Step 1: Install Kilo CLI
    Write-KiloStatus ""
    Write-KiloStatus "STEP 1: Installing Kilo CLI..." 'Info'

    # Check if already installed
    $kiloInstalled = Test-CommandExists 'kilo'

    if ($kiloInstalled -and -not $ForceInstall) {
        Write-KiloStatus "✓ Kilo CLI already installed" 'Success'
        $currentVersion = (kilo --version 2>$null) -replace 'v',''
        Write-KiloStatus "  Current version: $currentVersion" 'Info'
    } else {
        Write-KiloStatus "Installing $KiloCLIPackage globally via npm..." 'Info'
        npm install -g $KiloCLIPackage

        if ($LASTEXITCODE -eq 0) {
            Write-KiloStatus "✓ Kilo CLI installed successfully" 'Success'
        } else {
            throw "npm install failed with exit code $LASTEXITCODE"
        }
    }

    # Verify installation
    if (-not (Test-CommandExists 'kilo')) {
        throw "kilo command not found after installation. Check npm global path."
    }
    Write-KiloStatus "✓ Kilo CLI is ready" 'Success'

    # Step 2: Configure Kilo with optimal free model settings
    Write-KiloStatus ""
    Write-KiloStatus "STEP 2: Configuring Kilo for optimal free usage..." 'Info'

    Ensure-Directory (Split-Path $CustomConfigPath -Parent)

    $config = @{
        # Use Auto Free tier for automatic best free model routing
        model = "kilo-auto/free"

        # Explicitly set the free Ling-2.6-1T for largest context (256K)
        # This was identified as the best free model with most context
        agent = @{
            code = @{
                model = "inclusionai/ling-2.6-1t:free"
            }
            ask = @{
                model = "inclusionai/ling-2.6-1t:free"
            }
            plan = @{
                model = "inclusionai/ling-2.6-1t:free"
            }
            debug = @{
                model = "inclusionai/ling-2.6-1t:free"
            }
        }

        # Background tasks (session titles, etc.) - use free model
        small_model = "inclusionai/ling-2.6-1t:free"

        # Autocomplete - use free Mistral Codestral via BYOK recommendation
        # User should add their own key later
        inline_completions = @{
            provider = "kilo"  # Change to "mistral" after adding BYOK key
        }

        # MCP server configuration (if applicable)
        mcp = @{
            enabled = $true
        }
    } | ConvertTo-Json -Depth 5

    $config | Out-File -FilePath $CustomConfigPath -Encoding UTF8
    Write-KiloStatus "✓ Configuration saved to: $CustomConfigPath" 'Success'

    # Step 3: VS Code Extension Installation
    Write-KiloStatus ""
    Write-KiloStatus "STEP 3: VS Code Extension Setup" 'Info'

    if ($vscodeInstalled -and -not $SkipVS CodeExtension) {
        try {
            # Check if extension is already installed
            $extensionsOutput = & $vscodePath --list-extensions 2>$null
            if ($extensionsOutput -match [regex]::Escape($VSCodeExtensionId)) {
                Write-KiloStatus "✓ Kilo Code extension already installed" 'Success'
            } else {
                Write-KiloStatus "Installing Kilo Code VS Code extension..." 'Info'
                & $vscodePath --install-extension $VSCodeExtensionId --force

                if ($LASTEXITCODE -eq 0) {
                    Write-KiloStatus "✓ VS Code extension installed" 'Success'
                } else {
                    Write-KiloStatus "⚠️  Extension install may have failed (exit: $LASTEXITCODE)" 'Warning'
                }
            }
        } catch {
            Write-KiloStatus "⚠️  Could not install VS Code extension: $_" 'Warning'
        }
    } elseif ($SkipVS CodeExtension) {
        Write-KiloStatus "⏭️  Skipping VS Code extension (--SkipVS CodeExtension)" 'Info'
    } else {
        Write-KiloStatus "⚠️  VS Code not available - skipping extension" 'Warning'
    }

    # Step 4: Create desktop shortcuts
    Write-KiloStatus ""
    Write-KiloStatus "STEP 4: Creating shortcuts..." 'Info'

    $desktopPath = [Environment]::GetFolderPath('Desktop')
    $startMenuPath = "${env:ProgramData}\Microsoft\Windows\Start Menu\Programs"

    # Kilo CLI launcher shortcut
    $kiloShortcutPath = Join-Path $desktopPath "Kilo Code CLI.lnk"
    $wshShell = New-Object -ComObject WScript.Shell
    $shortcut = $wshShell.CreateShortcut($kiloShortcutPath)
    $shortcut.TargetPath = "powershell.exe"
    $shortcut.Arguments = "-NoExit -Command `"kilo`""
    $shortcut.Description = "Launch Kilo Code AI Agent (CLI)"
    $shortcut.IconLocation = "imageres.dll,-5302"  # Terminal icon
    $shortcut.Save()
    Write-KiloStatus "✓ Desktop shortcut created: Kilo Code CLI" 'Success'

    # VS Code with Kilo shortcut (if VS Code installed)
    if ($vscodeInstalled) {
        $vscodeKiloShortcut = Join-Path $desktopPath "VS Code + Kilo.lnk"
        $shortcut = $wshShell.CreateShortcut($vscodeKiloShortcut)
        $shortcut.TargetPath = $vscodePath
        $shortcut.Arguments = "--new-window"
        $shortcut.Description = "VS Code with Kilo AI Extension"
        $shortcut.IconLocation = "${env:ProgramFiles}\Microsoft VS Code\Code.exe,0"
        $shortcut.Save()
        Write-KiloStatus "✓ Desktop shortcut created: VS Code + Kilo" 'Success'
    }

    # Step 5: Create usage documentation
    Write-KiloStatus ""
    Write-KiloStatus "STEP 5: Generating usage documentation..." 'Info'

    $usageDoc = @"
# Kilo Code - Quick Start Guide

## Installation Complete ✓

Kilo Code has been configured with:
- **Model:** inclusionAI Ling-2.6-1T (free) - 256K context window
- **Auto-tier:** kilo-auto/free (auto-selects best free model)
- **CLI:** Installed globally via npm

## Quick Commands

### Start Kilo CLI
```powershell
kilo
```

### Use in VS Code
1. Open VS Code
2. Click Kilo icon in sidebar (or Ctrl+Shift+P → "Kilo: Focus on Kilo View")
3. Start chatting with AI

### Recommended Free Models (256K context)
- `inclusionai/ling-2.6-1t:free` - BEST #9 Code rank, #3 Debug rank
- `tencent/hy3-preview:free` - #17 Code, configurable reasoning levels
- `nvidia/nemotron-3-super-120b-a12b:free` - 120B MoE, 256K context
- `stepfun/step-3.5-flash` - $0.10/1M tokens, strong performance

## Configuration

Config file: $CustomConfigPath

To switch models in chat:
- Type `/models` to open model picker
- Filter with `free` or `256K`
- Select desired model

## Autocomplete (Free)
For completely free inline completions:
1. Get Mistral API key from https://console.mistral.ai
2. In Kilo Settings → Providers → Add "mistral" API key
3. Set inline_completions.provider = "mistral"

## Integration Tips
- Use `@` to mention files and attach context
- Drag & drop files into chat
- Use `/code` agent for coding tasks (default)
- Use `/debug` for troubleshooting
- Check leaderboard: https://kilo.ai/models

## Next Steps
1. Run `kilo` to test
2. Open a project and try: "Create a new feature"
3. Check MCP servers: `.\mcp_server\` (if available)

---
Installation: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
"@

    $docsPath = Join-Path (Split-Path $CustomConfigPath -Parent) "KILO_QUICKSTART.md"
    $usageDoc | Out-File -FilePath $docsPath -Encoding UTF8
    Write-KiloStatus "✓ Documentation saved: $docsPath" 'Success'

    # Step 6: Validate installation
    Write-KiloStatus ""
    Write-KiloStatus "STEP 6: Validating installation..." 'Info'

    $kiloVersion = kilo --version 2>$null
    if ($kiloVersion) {
        Write-KiloStatus "✓ Kilo version: $kiloVersion" 'Success'
    } else {
        Write-KiloStatus "⚠️  Could not verify version (may need restart)" 'Warning'
    }

    # Summary
    Write-KiloStatus ""
    Write-KiloStatus "====================================" 'Info'
    Write-KiloStatus "KILO SETUP COMPLETE" 'Success'
    Write-KiloStatus "====================================" 'Info'
    Write-KiloStatus ""
    Write-KiloStatus "INSTALLATION SUMMARY:" 'Info'
    Write-KiloStatus "  • Kilo CLI: Installed globally" 'Info'
    Write-KiloStatus "  • Model Config: inclusionAI Ling-2.6-1T (256K context, free)" 'Info'
    Write-KiloStatus "  • Auto Free tier: Enabled for fallback" 'Info'
    Write-KiloStatus "  • VS Code Extension: $(
        if ($vscodeInstalled -and -not $SkipVS CodeExtension) { 'Installed' }
        elseif ($SkipVS CodeExtension) { 'Skipped' }
        else { 'Not available' }
    )" 'Info'
    Write-KiloStatus "  • Shortcuts: Desktop created" 'Info'
    Write-KiloStatus "  • Documentation: $docsPath" 'Info'
    Write-KiloStatus ""
    Write-KiloStatus "NEXT STEPS:" 'Info'
    Write-KiloStatus "  1. Restart PowerShell (refresh PATH)" 'Info'
    Write-KiloStatus "  2. Run: kilo" 'Info'
    Write-KiloStatus "  3. In VS Code: Click Kilo sidebar icon" 'Info'
    Write-KiloStatus "  4. Type: 'Hello with my 256K context free model!'" 'Info'
    Write-KiloStatus ""
    Write-KiloStatus "For help: kilo --help or https://kilo.ai/docs" 'Info'

} catch {
    Write-KiloStatus "INSTALLATION FAILED: $_" 'Error'
    Write-KiloStatus "Check prerequisites and try again." 'Info'
    exit 1
}

#endregion
