#!/usr/bin/env pwsh
# Place the Visual GUI Launcher on Desktop

$ProjectRoot = $PSScriptRoot
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$WScriptShell = New-Object -ComObject WScript.Shell

Write-Host ""
Write-Host "Creating Visual Launcher shortcut on desktop..." -ForegroundColor Cyan
Write-Host ""

# Create shortcut for GUI Launcher
$ShortcutPath = Join-Path $DesktopPath "Scarify Empire Launcher.lnk"
$Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "pythonw.exe"
$Shortcut.Arguments = "`"$ProjectRoot\DESKTOP_LAUNCHER.pyw`""
$Shortcut.WorkingDirectory = $ProjectRoot
$Shortcut.Description = "Scarify Empire Visual Launcher - Click to open command center"
$Shortcut.Save()

Write-Host "✅ Created: Scarify Empire Launcher.lnk" -ForegroundColor Green
Write-Host ""
Write-Host "Location: $DesktopPath" -ForegroundColor Yellow
Write-Host ""
Write-Host "Double-click 'Scarify Empire Launcher' on your desktop to open!" -ForegroundColor Cyan
Write-Host ""

