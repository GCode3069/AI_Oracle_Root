#!/usr/bin/env pwsh
# ═══════════════════════════════════════════════════════════════
#   SCARIFY EMPIRE - Desktop Shortcut Creator
#   Creates beautiful desktop shortcuts for all systems!
# ═══════════════════════════════════════════════════════════════

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                                  ║" -ForegroundColor Cyan
Write-Host "║         🖥️  SCARIFY EMPIRE - DESKTOP LAUNCHER CREATOR 🖥️        ║" -ForegroundColor Cyan
Write-Host "║                                                                  ║" -ForegroundColor Cyan
Write-Host "║           Creating beautiful desktop shortcuts...                ║" -ForegroundColor Cyan
Write-Host "║                                                                  ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$ProjectRoot = $PSScriptRoot
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$WScriptShell = New-Object -ComObject WScript.Shell

function Create-Shortcut {
    param(
        [string]$Name,
        [string]$TargetPath,
        [string]$Arguments = "",
        [string]$Description,
        [string]$IconPath = "",
        [string]$WorkingDirectory = ""
    )
    
    Write-Host "[*] Creating: $Name" -ForegroundColor Yellow
    
    $ShortcutPath = Join-Path $DesktopPath "$Name.lnk"
    $Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)
    $Shortcut.TargetPath = $TargetPath
    
    if ($Arguments) { $Shortcut.Arguments = $Arguments }
    if ($Description) { $Shortcut.Description = $Description }
    if ($IconPath) { $Shortcut.IconLocation = $IconPath }
    if ($WorkingDirectory) { 
        $Shortcut.WorkingDirectory = $WorkingDirectory 
    } else {
        $Shortcut.WorkingDirectory = $ProjectRoot
    }
    
    $Shortcut.Save()
    Write-Host "    ✅ Created: $ShortcutPath" -ForegroundColor Green
}

# Main Empire Launcher
Create-Shortcut `
    -Name "Launch Scarify Empire" `
    -TargetPath "$ProjectRoot\LAUNCH_EMPIRE.bat" `
    -Description "Start the complete Scarify Empire system (Desktop + MCP + Mobile + Telegram)" `
    -WorkingDirectory $ProjectRoot

# Desktop Dashboard Only
Create-Shortcut `
    -Name "Scarify Control Center" `
    -TargetPath "pythonw.exe" `
    -Arguments "`"$ProjectRoot\SCARIFY_CONTROL_CENTER.pyw`"" `
    -Description "Open Scarify Empire Desktop Dashboard (18 tabs)" `
    -WorkingDirectory $ProjectRoot

# Mobile Web UI
Create-Shortcut `
    -Name "Mobile Web Interface" `
    -TargetPath "python.exe" `
    -Arguments "`"$ProjectRoot\MOBILE_MCP_SERVER.py`"" `
    -Description "Start Scarify Mobile Web UI (http://localhost:5000)" `
    -WorkingDirectory $ProjectRoot

# MCP Server
Create-Shortcut `
    -Name "MCP Server (AI Control)" `
    -TargetPath "cmd.exe" `
    -Arguments "/k cd /d `"$ProjectRoot\mcp-server`" && node dist\index.js" `
    -Description "Start MCP Server for Claude/Cursor AI control" `
    -WorkingDirectory "$ProjectRoot\mcp-server"

# Self Deploy Agent
Create-Shortcut `
    -Name "Self Deploy Agent" `
    -TargetPath "python.exe" `
    -Arguments "`"$ProjectRoot\SELF_DEPLOY.py`"" `
    -Description "Run Scarify Empire self-deployment agent (5 modes)" `
    -WorkingDirectory $ProjectRoot

# GitHub Sync
Create-Shortcut `
    -Name "Sync to GitHub" `
    -TargetPath "$ProjectRoot\SYNC_TO_GITHUB.bat" `
    -Description "Sync all changes to GitHub repository" `
    -WorkingDirectory $ProjectRoot

# Quick Actions
Create-Shortcut `
    -Name "Generate 10 Videos" `
    -TargetPath "cmd.exe" `
    -Arguments "/k python `"$ProjectRoot\abraham_horror\ABRAHAM_PROFESSIONAL_UPGRADE.py`" 10" `
    -Description "Quick generate 10 Abraham Lincoln videos" `
    -WorkingDirectory "$ProjectRoot\abraham_horror"

Create-Shortcut `
    -Name "Upload All Videos" `
    -TargetPath "cmd.exe" `
    -Arguments "/k python `"$ProjectRoot\MULTI_CHANNEL_UPLOADER.py`" abraham_horror/youtube_ready round-robin" `
    -Description "Upload all ready videos to YouTube channels" `
    -WorkingDirectory $ProjectRoot

Create-Shortcut `
    -Name "Check Bitcoin Balance" `
    -TargetPath "cmd.exe" `
    -Arguments "/k python `"$ProjectRoot\check_balance.py`"" `
    -Description "Check Bitcoin donation balance" `
    -WorkingDirectory $ProjectRoot

# Project Folder
Create-Shortcut `
    -Name "Scarify Project Folder" `
    -TargetPath "explorer.exe" `
    -Arguments "`"$ProjectRoot`"" `
    -Description "Open Scarify Empire project folder"

# Documentation
Create-Shortcut `
    -Name "Scarify Documentation" `
    -TargetPath "notepad.exe" `
    -Arguments "`"$ProjectRoot\README.md`"" `
    -Description "Open Scarify Empire documentation"

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                                                                  ║" -ForegroundColor Green
Write-Host "║                 ✅ DESKTOP SHORTCUTS CREATED! ✅                 ║" -ForegroundColor Green
Write-Host "║                                                                  ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "🎯 Created on your desktop:" -ForegroundColor Cyan
Write-Host ""
Write-Host "   🚀 Launch Scarify Empire       - Starts everything!" -ForegroundColor White
Write-Host "   🖥️  Scarify Control Center      - Desktop dashboard only" -ForegroundColor White
Write-Host "   📱 Mobile Web Interface        - Mobile UI server" -ForegroundColor White
Write-Host "   🤖 MCP Server (AI Control)     - AI voice control" -ForegroundColor White
Write-Host "   🔧 Self Deploy Agent           - Auto-deployment" -ForegroundColor White
Write-Host "   📤 Sync to GitHub              - GitHub sync" -ForegroundColor White
Write-Host "   🎬 Generate 10 Videos          - Quick generation" -ForegroundColor White
Write-Host "   📤 Upload All Videos           - Quick upload" -ForegroundColor White
Write-Host "   💰 Check Bitcoin Balance       - Revenue check" -ForegroundColor White
Write-Host "   📁 Open Scarify Folder         - Project folder" -ForegroundColor White
Write-Host "   📚 Scarify Documentation       - Master guide" -ForegroundColor White
Write-Host ""
Write-Host "💡 TIP: Double-click any shortcut to run!" -ForegroundColor Yellow
Write-Host ""
Write-Host "🔥 Your desktop is now a command center! 🔥" -ForegroundColor Magenta
Write-Host ""

