# Create Desktop Shortcut for SCARIFY Dashboard

$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ScriptPath = "F:\AI_Oracle_Root\scarify\LAUNCH_DASHBOARD.bat"
$ShortcutPath = Join-Path $DesktopPath "SCARIFY Empire.lnk"
$IconPath = "F:\AI_Oracle_Root\scarify\scarify_icon.ico"

$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $ScriptPath
$Shortcut.WorkingDirectory = "F:\AI_Oracle_Root\scarify"
$Shortcut.Description = "SCARIFY Empire Control Center - Manage video generation, uploads, and analytics"
$Shortcut.WindowStyle = 1

# Set icon if exists
if (Test-Path $IconPath) {
    $Shortcut.IconLocation = $IconPath
}

$Shortcut.Save()

Write-Host ""
Write-Host "====================================" -ForegroundColor Green
Write-Host "Desktop Shortcut Created!" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""
Write-Host "Shortcut Location: $ShortcutPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "Double-click 'SCARIFY Empire' on your desktop to launch!" -ForegroundColor Yellow
Write-Host ""
