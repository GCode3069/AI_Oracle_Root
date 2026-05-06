<#
.SYNOPSIS
    Kilo Code Daily Operations & Integration Utilities
.DESCRIPTION
    Helper functions for using Kilo AI within the zED workspace environment.
    Includes project-aware commands, quick task runners, and integration hooks.
.NOTES
    Companion script to Setup-KiloCode.ps1
#>

[CmdletBinding()]
param()

$script:WorkspaceRoot = $PSScriptRoot
$script:KiloConfig = "$env:USERPROFILE\.config\kilo\config.json"
$script:ProjectContextFile = "kilo_context.md"

#region Utility Functions

function Invoke-KiloTask {
    <#
    .SYNOPSIS
        Run a Kilo task with automatic context awareness
    #>
    param(
        [Parameter(Mandatory=$true)]
        [string]$Task,

        [string]$Model = "kilo-auto/free",

        [switch]$NoContext,

        [switch]$AutoApprove
    )

    Write-Host "🤖 Kilo Task: $Task" -ForegroundColor Cyan

    # Build context from current workspace
    $contextArgs = @()
    if (-not $NoContext) {
        $contextArgs = @("@current-workspace")
    }

    # Build command
    $cmd = "kilo"
    if ($AutoApprove) {
        $cmd = "kilo --auto"
    }

    # Write task file for reference
    $taskLog = @{
        timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        task = $Task
        model = $Model
        context = $contextArgs
    } | ConvertTo-Json -Depth 3

    $taskLog | Out-File -FilePath "kilo_task_log.json" -Append -Encoding UTF8

    # Execute
    Write-Host "   Model: $Model" -ForegroundColor Gray
    Write-Host "   Context: $($contextArgs -join ', ')" -ForegroundColor Gray
    Write-Host "   Executing..." -ForegroundColor Yellow

    # Pass to Kilo
    & $cmd $Task
}

function Get-KiloBestModel {
    <#
    .SYNOPSIS
        Show top free models with context sizes
    #>
    Write-Host "`n🏆 BEST FREE KILO MODELS (with context size)" -ForegroundColor Cyan
    Write-Host "=" * 60 -ForegroundColor Gray

    $models = @(
        @{ Name="inclusionAI Ling-2.6-1T"; Context="256K"; Rank="#9 Code / #3 Debug"; Free=$true; Notes="BEST OVERALL" },
        @{ Name="Tencent Hy3 preview"; Context="256K"; Rank="#17 Code"; Free=$true; Notes="Configurable reasoning" },
        @{ Name="NVIDIA Nemotron 3 Super"; Context="256K"; Rank="#85 Code"; Free=$true; Notes="120B MoE, 12B active" },
        @{ Name="Google Gemma 4 26B"; Context="256K"; Rank="N/A"; Free=$true; Notes="Multimodal" },
        @{ Name="StepFun Step 3.5 Flash"; Context="256K"; Rank="#81 Code"; Free=$false; Notes="$0.10/1M tokens" },
        @{ Name="Poolside Laguna M.1"; Context="128K"; Rank="#30 Code"; Free=$true; Notes="Coding specialized" },
        @{ Name="Qwen 3.6 Plus"; Context="?; Rank="#42 Code"; Free=$false; Notes="Pay per use" }
    )

    $models | Format-Table -AutoSize -Property @{Label="Model";Expression={$_.Name}}, `
                                            @{Label="Context";Expression={$_.Context}}, `
                                            @{Label="Rank";Expression={$_.Rank}}, `
                                            @{Label="Free?";Expression={if($_.Free){'✓'}else{'$'}}}, `
                                            @{Label="Notes";Expression={$_.Notes}}
}

function Set-KiloModel {
    <#
    .SYNOPSIS
        Switch Kilo to a specific model with validation
    #>
    param(
        [Parameter(Mandatory=$true)]
        [ValidateSet('ling-2.6-1t','hy3','nemotron','gemma','step','laguna','auto-free','auto-balanced')]
        [string]$Model,

        [switch]$Persist
    )

    $modelMap = @{
        'ling-2.6-1t' = 'inclusionai/ling-2.6-1t:free'
        'hy3' = 'tencent/hy3-preview:free'
        'nemotron' = 'nvidia/nemotron-3-super-120b-a12b:free'
        'gemma' = 'google/gemma-4-26b-a4b-it:free'
        'step' = 'stepfun/step-3.5-flash'
        'laguna' = 'poolside/laguna-m.1:free'
        'auto-free' = 'kilo-auto/free'
        'auto-balanced' = 'kilo-auto/balanced'
    }

    $selectedModel = $modelMap[$Model]
    Write-Host "🎯 Switching Kilo to: $selectedModel" -ForegroundColor Cyan

    if ($Persist) {
        # Update config
        if (Test-Path $script:KiloConfig) {
            $config = Get-Content $script:KiloConfig | ConvertFrom-Json
            $config.model = $selectedModel
            $config | ConvertTo-Json -Depth 5 | Out-File -FilePath $script:KiloConfig -Encoding UTF8
            Write-Host "✓ Persisted to config" -ForegroundColor Green
        }
    }

    Write-Host "✓ Model set. Start a new Kilo session to apply." -ForegroundColor Green
}

function New-KiloProjectContext {
    <#
    .SYNOPSIS
        Generate a context file for the current project
    #>
    param(
        [string]$ProjectName = (Split-Path (Get-Location) -Leaf),

        [string]$OutputFile = "kilo_context.md"
    )

    Write-Host "📋 Generating project context for Kilo..." -ForegroundColor Cyan

    $context = @"
# Project: $ProjectName

**Generated:** $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

## Overview
<!-- Add project description here -->

## Key Files
"@

    # Auto-detect important files
    $importantExtensions = @('*.py','*.js','*.ts','*.ps1','*.md','*.json','*.yaml','*.yml')
    $keyFiles = @()

    foreach ($ext in $importantExtensions) {
        $files = Get-ChildItem -Path . -Recurse -Filter $ext -File -ErrorAction SilentlyContinue |
                 Select-Object -First 20
        foreach ($f in $files) {
            $keyFiles += $f.FullName
        }
    }

    if ($keyFiles.Count -gt 0) {
        $context += "`n### File Inventory`n"
        $keyFiles | ForEach-Object {
            $relPath = $_ -replace [regex]::Escape((Get-Location).Path + '\'), ''
            $context += "- `$relPath`n"
        }
    }

    $context += "`n## Architecture Notes`n<!-- Add architecture details -->`n"
    $context += "`n## Dependencies`n<!-- List key dependencies -->`n"
    $context += "`n## Known Issues`n<!-- List known problems -->`n"

    $context | Out-File -FilePath $OutputFile -Encoding UTF8
    Write-Host "✓ Context file created: $OutputFile" -ForegroundColor Green
    Write-Host "  Edit this file and reference it in Kilo chats with @kilo_context.md" -ForegroundColor Gray
}

function Invoke-KiloWithContext {
    <#
    .SYNOPSIS
        Run Kilo with project-specific context automatically attached
    #>
    param(
        [Parameter(Mandatory=$true)]
        [string]$Query
    )

    # Build context mentions
    $mentions = @()

    # Add project context if exists
    if (Test-Path $script:ProjectContextFile) {
        $mentions += "@$script:ProjectContextFile"
    }

    # Add README if exists
    if (Test-Path "README.md") {
        $mentions += "@README.md"
    }

    # Add any *.plan.md or *.spec files
    $planFiles = Get-ChildItem -Path . -Filter "*.plan.md" -File -ErrorAction SilentlyContinue
    foreach ($pf in $planFiles) {
        $mentions += "@$($pf.Name)"
    }

    $contextStr = $mentions -join ' '
    $fullQuery = "$Query $contextStr"

    Write-Host "🧠 Querying Kilo with context..." -ForegroundColor Cyan
    Write-Host "   Context files: $($mentions -join ', ')" -ForegroundColor Gray

    kilo $fullQuery
}

function Test-KiloIntegration {
    <#
    .SYNOPSIS
        Run diagnostics on Kilo installation
    #>
    Write-Host "`n🔧 Kilo Integration Diagnostics" -ForegroundColor Cyan
    Write-Host "=" * 50 -ForegroundColor Gray

    # Check CLI
    Write-Host "`n1. CLI Installation" -ForegroundColor Yellow
    if (Test-CommandExists 'kilo') {
        $version = kilo --version 2>&1
        Write-Host "   ✓ Kilo installed: $version" -ForegroundColor Green
    } else {
        Write-Host "   ✗ Kilo not found in PATH" -ForegroundColor Red
    }

    # Check config
    Write-Host "`n2. Configuration" -ForegroundColor Yellow
    if (Test-Path $script:KiloConfig) {
        $config = Get-Content $script:KiloConfig | ConvertFrom-Json
        Write-Host "   ✓ Config exists: $script:KiloConfig" -ForegroundColor Green
        Write-Host "   Model: $($config.model)" -ForegroundColor Gray

        if ($config.agent.code.model) {
            Write-Host "   Code agent: $($config.agent.code.model)" -ForegroundColor Gray
        }
    } else {
        Write-Host "   ✗ Config not found" -ForegroundColor Red
    }

    # Check VS Code
    Write-Host "`n3. VS Code Integration" -ForegroundColor Yellow
    $vscode = Get-Command code -ErrorAction SilentlyContinue
    if ($vscode) {
        Write-Host "   ✓ VS Code CLI detected" -ForegroundColor Green
        $extensions = code --list-extensions 2>&1 | Where-Object { $_ -match 'kilocode' }
        if ($extensions) {
            Write-Host "   ✓ Kilo extension installed" -ForegroundColor Green
        } else {
            Write-Host "   ✗ Kilo extension NOT installed" -ForegroundColor Red
        }
    } else {
        Write-Host "   ⚠ VS Code not in PATH (normal if using launcher)" -ForegroundColor Yellow
    }

    # Check npm global prefix
    Write-Host "`n4. npm Global Packages" -ForegroundColor Yellow
    $npmRoot = npm root -g 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   npm global: $npmRoot" -ForegroundColor Gray
        $kiloPath = Join-Path $npmRoot "node_modules\$KiloCLIPackage"
        if (Test-Path $kiloPath) {
            Write-Host "   ✓ Kilo package exists in node_modules" -ForegroundColor Green
        }
    }

    # Network test
    Write-Host "`n5. Connectivity" -ForegroundColor Yellow
    try {
        $response = Invoke-WebRequest -Uri "https://kilo.ai" -Method Head -TimeoutSec 5 -ErrorAction Stop
        Write-Host "   ✓ Kilo AI reachable (HTTP $($response.StatusCode))" -ForegroundColor Green
    } catch {
        Write-Host "   ⚠ Cannot reach Kilo AI: $_" -ForegroundColor Yellow
    }

    Write-Host "`n✅ Diagnostics complete" -ForegroundColor Cyan
}

function Update-Kilo {
    <#
    .SYNOPSIS
        Update Kilo CLI to latest version
    #>
    Write-Host "🔄 Updating Kilo CLI..." -ForegroundColor Cyan

    npm update -g $KiloCLIPackage

    if ($LASTEXITCODE -eq 0) {
        $newVersion = (kilo --version 2>$null)
        Write-Host "✓ Updated successfully: $newVersion" -ForegroundColor Green
    } else {
        Write-Host "✗ Update failed" -ForegroundColor Red
    }
}

#endregion

#region Quick-Access Aliases

# Create convenient shortcuts
function k { kilo @args }
function kc { kilo --clear @args }
function kcode { kilo --model "inclusionai/ling-2.6-1t:free" @args }
function kauto { kilo --model "kilo-auto/free" @args }
function kdebug { kilo --agent debug @args }
function kask { kilo --agent ask @args }

#endregion

#region Interactive Mode

if ($MyInvocation.InvocationName -eq '&') {
    # Script run directly - show menu
    Write-Host "`n🎯 Kilo Code Utilities - Select an option:" -ForegroundColor Cyan
    Write-Host ""

    $options = @(
        @{Num=1; Text="Run Kilo CLI"; Action={ kilo } },
        @{Num=2; Text="Diagnose Installation"; Action={ Test-KiloIntegration } },
        @{Num=3; Text="Switch Model (Ling-2.6-1T)"; Action={ Set-KiloModel -Model 'ling-2.6-1t' -Persist } },
        @{Num=4; Text="Switch Model (Auto Free)"; Action={ Set-KiloModel -Model 'auto-free' -Persist } },
        @{Num=5; Text="Create Project Context"; Action={ New-KiloProjectContext } },
        @{Num=6; Text="Update Kilo CLI"; Action={ Update-Kilo } },
        @{Num=7; Text="Show All Free Models"; Action={ Get-KiloBestModel } },
        @{Num=8; Text="Exit"; Action={ exit } }
    )

    while ($true) {
        Write-Host "" -ForegroundColor Gray
        foreach ($opt in $options) {
            Write-Host "  [$($opt.Num)] $($opt.Text)" -ForegroundColor White
        }

        $choice = Read-Host "`nSelect option (1-$($options.Count))"
        $selected = $options | Where-Object { $_.Num -eq [int]$choice }

        if ($selected) {
            & $selected.Action
            if ($selected.Text -ne "Exit") {
                Write-Host "`nPress any key to continue..." -ForegroundColor Gray
                $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            }
        } else {
            Write-Host "Invalid choice" -ForegroundColor Red
        }
    }
}

#endregion
