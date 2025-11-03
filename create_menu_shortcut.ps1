# Create Desktop Shortcut for SCARIFY Menu
# This creates a shortcut for the main menu that lets users choose between dashboard and simple launcher

$Desktop = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $Desktop "SCARIFY Generator.lnk"
$TargetPath = "F:\AI_Oracle_Root\scarify\scarify_menu.ps1"

Write-Host ""
Write-Host "Creating SCARIFY Menu shortcut..." -ForegroundColor Cyan
Write-Host "   From: $TargetPath"
Write-Host "   To: $ShortcutPath"

try {
    # Create WScript.Shell object
    $WshShell = New-Object -ComObject WScript.Shell
    
    # Create shortcut
    $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
    $Shortcut.TargetPath = "powershell.exe"
    $Shortcut.Arguments = "-ExecutionPolicy Bypass -File `"$TargetPath`""
    $Shortcut.WorkingDirectory = "F:\AI_Oracle_Root\scarify"
    $Shortcut.Description = "SCARIFY Generator - YouTube Shorts Empire"
    $Shortcut.IconLocation = "powershell.exe,0"
    
    # Save shortcut
    $Shortcut.Save()
    
    Write-Host "✅ Menu shortcut created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now double-click the 'SCARIFY Generator' icon on your desktop." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Menu options:" -ForegroundColor Cyan
    Write-Host "  🚀 FULL DASHBOARD - Advanced control center" -ForegroundColor White
    Write-Host "  ⚡ SIMPLE LAUNCHER - Quick generation buttons" -ForegroundColor White
    Write-Host ""
    Write-Host "Dashboard features:" -ForegroundColor Cyan
    Write-Host "  • Batch operations (1, 5, 10, 20, 50 videos)" -ForegroundColor White
    Write-Host "  • Custom batch sizes" -ForegroundColor White
    Write-Host "  • Real-time monitoring" -ForegroundColor White
    Write-Host "  • YouTube authentication testing" -ForegroundColor White
    Write-Host "  • Statistics tracking" -ForegroundColor White
    Write-Host "  • System controls" -ForegroundColor White
    
} catch {
    Write-Host "❌ Error creating shortcut: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host ""

pause
