# Create Desktop Shortcut for Abraham Horror Generator

$shortcutPath = [Environment]::GetFolderPath("Desktop") + "\🎃 Abraham Horror Generator.lnk"
$targetPath = "powershell.exe"
$scriptPath = "F:\AI_Oracle_Root\scarify\abraham_horror\ABRAHAM_ULTIMATE.ps1"
$arguments = "-NoExit -ExecutionPolicy Bypass -File `"$scriptPath`" -Count 5"

$WScriptShell = New-Object -ComObject WScript.Shell
$shortcut = $WScriptShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $targetPath
$shortcut.Arguments = $arguments
$shortcut.WorkingDirectory = "F:\AI_Oracle_Root\scarify\abraham_horror"
$shortcut.IconLocation = "shell32.dll,238"
$shortcut.Description = "Generate Abraham Lincoln Horror Videos"
$shortcut.Save()

Write-Host "✅ Desktop shortcut created!" -ForegroundColor Green
Write-Host "🎃 Double-click 'Abraham Horror Generator' on your desktop!" -ForegroundColor Cyan
