# Create Desktop Shortcut for SCARIFY Launcher
# Run this script to create a desktop shortcut

$ShortcutName = "SCARIFY Generator.lnk"
$LauncherPath = Join-Path $PSScriptRoot "scarify_launcher.ps1"
$IconPath = "C:\Windows\System32\shell32.dll"  # Default video icon
$IconIndex = 165  # Video camera icon

# Get Desktop path
$Desktop = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $Desktop $ShortcutName

# Check if launcher exists
if (-not (Test-Path $LauncherPath)) {
    Write-Host "❌ ERROR: scarify_launcher.ps1 not found at: $LauncherPath"
    Write-Host "Make sure this script is in the same folder as scarify_launcher.ps1"
    pause
    exit 1
}

Write-Host "🔧 Creating desktop shortcut..."
Write-Host "   From: $LauncherPath"
Write-Host "   To: $ShortcutPath"

try {
    # Create WScript Shell object
    $WshShell = New-Object -ComObject WScript.Shell
    
    # Create shortcut
    $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
    $Shortcut.TargetPath = "powershell.exe"
    $Shortcut.Arguments = "-ExecutionPolicy Bypass -WindowStyle Hidden -File `"$LauncherPath`""
    $Shortcut.WorkingDirectory = $PSScriptRoot
    $Shortcut.Description = "SCARIFY YouTube Shorts Video Generator"
    $Shortcut.IconLocation = "$IconPath,$IconIndex"
    $Shortcut.Save()
    
    Write-Host "✅ Shortcut created successfully!"
    Write-Host ""
    Write-Host "You can now double-click the 'SCARIFY Generator' icon on your desktop."
    Write-Host ""
    
    # Ask if user wants to open the launcher now
    $Response = Read-Host "Launch SCARIFY now? (y/n)"
    if ($Response -eq 'y' -or $Response -eq 'Y') {
        Write-Host "🚀 Starting SCARIFY..."
        & powershell.exe -ExecutionPolicy Bypass -File "$LauncherPath"
    }
    
} catch {
    Write-Host "❌ ERROR creating shortcut: $($_.Exception.Message)"
    pause
    exit 1
}

Write-Host ""
Write-Host "✅ Setup complete!"
pause


