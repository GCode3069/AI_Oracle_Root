# Create Updated Desktop Shortcut - Points to Latest Working Launcher
$desktop = [System.Environment]::GetFolderPath("Desktop")
$wshShell = New-Object -ComObject WScript.Shell

# Remove old shortcut if exists
$oldShortcut = "$desktop\Abraham Lincoln Professional Videos.lnk"
if (Test-Path $oldShortcut) {
    Remove-Item $oldShortcut -Force
}

# Create new shortcut pointing to START_HERE.bat (the working launcher)
$shortcut = $wshShell.CreateShortcut("$desktop\Abraham Lincoln Videos.lnk")

$shortcut.TargetPath = "F:\AI_Oracle_Root\scarify\abraham_horror\START_HERE.bat"
$shortcut.WorkingDirectory = "F:\AI_Oracle_Root\scarify\abraham_horror"
$shortcut.IconLocation = "C:\Windows\System32\shell32.dll,27"
$shortcut.Description = "Generate & Upload Abraham Lincoln Professional Videos to YouTube"
$shortcut.Arguments = ""
$shortcut.Save()

Write-Host ""
Write-Host "Desktop shortcut created/updated!" -ForegroundColor Green
Write-Host "  Location: $desktop\Abraham Lincoln Videos.lnk" -ForegroundColor White
Write-Host ""
Write-Host "Double-click the shortcut on your desktop to generate 10 videos!" -ForegroundColor Cyan
Write-Host ""


