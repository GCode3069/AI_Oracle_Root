# Create Desktop Shortcut for Professional System
$desktop = [System.Environment]::GetFolderPath("Desktop")
$wshShell = New-Object -ComObject WScript.Shell
$shortcut = $wshShell.CreateShortcut("$desktop\Abraham Lincoln Professional Videos.lnk")

$shortcut.TargetPath = "F:\AI_Oracle_Root\scarify\abraham_horror\ABRAHAM_PRO_DESKTOP_LAUNCHER.bat"
$shortcut.WorkingDirectory = "F:\AI_Oracle_Root\scarify\abraham_horror"
$shortcut.IconLocation = "C:\Windows\System32\shell32.dll,27"
$shortcut.Description = "Generate professional Abraham Lincoln comedy videos (exceeds FarFromWeakFFW quality)"
$shortcut.Save()

Write-Host ""
Write-Host "Desktop shortcut created!" -ForegroundColor Green
Write-Host "  Location: $desktop\Abraham Lincoln Professional Videos.lnk" -ForegroundColor White
Write-Host ""
Write-Host "Double-click the shortcut on your desktop to generate videos!" -ForegroundColor Cyan
Write-Host ""


