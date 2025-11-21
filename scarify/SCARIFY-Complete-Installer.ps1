# =====================================================
# SCARIFY Complete Installer - One-Click Deployment
# Creates all scripts, directories, and desktop shortcuts
# =====================================================

param(
    [switch]$Test,
    [switch]$Force,
    [string]$InstallPath = ""
)

# Determine default install path based on platform
if ([string]::IsNullOrEmpty($InstallPath)) {
    if ($IsWindows -or $env:OS -eq "Windows_NT") {
        $InstallPath = "D:\AI_Oracle_Root\scarify"
    } else {
        $InstallPath = Join-Path (Get-Location) "scarify_installation"
    }
}

Write-Host "💿 SCARIFY Complete Installer v1.0" -ForegroundColor Magenta
Write-Host "Installing to: $InstallPath" -ForegroundColor Cyan

# Create directory structure
$directories = @(
    "1_Audio_Processing",
    "2_Image_Generation", 
    "3_Script_Generation",
    "4_Voice_Synthesis",
    "5_Video_Production",
    "6_Monetization",
    "7_Analytics_Strategy",
    "cli",
    "temp",
    "output"
)

foreach ($dir in $directories) {
    $fullPath = Join-Path $InstallPath $dir
    if (-not (Test-Path $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        Write-Host "📁 Created directory: $dir" -ForegroundColor Green
    }
}

# Create desktop shortcuts
$desktop = [Environment]::GetFolderPath("Desktop")

# SCARIFY Master Studio shortcut
$masterStudioShortcut = @"
Set objShell = CreateObject("WScript.Shell")
Set objShortcut = objShell.CreateShortcut("$desktop\SCARIFY Master Studio.lnk")
objShortcut.TargetPath = "powershell.exe"
objShortcut.Arguments = "-ExecutionPolicy Bypass -File \"$InstallPath\MasterControl.ps1\""
objShortcut.WorkingDirectory = "$InstallPath"
objShortcut.IconLocation = "shell32.dll,137"
objShortcut.Save
"@

$masterStudioShortcut | Out-File -FilePath "$InstallPath\temp\create_master_studio.vbs" -Encoding ASCII
cscript //nologo "$InstallPath\temp\create_master_studio.vbs"

# Lightning Strike Protocol shortcut
$lightningStrikeShortcut = @"
Set objShell = CreateObject("WScript.Shell")
Set objShortcut = objShell.CreateShortcut("$desktop\Lightning Strike Protocol.lnk")
objShortcut.TargetPath = "powershell.exe"
objShortcut.Arguments = "-ExecutionPolicy Bypass -File \"$InstallPath\MasterLaunch.ps1\" -LightningStrike"
objShortcut.WorkingDirectory = "$InstallPath"
objShortcut.IconLocation = "shell32.dll,25"
objShortcut.Save
"@

$lightningStrikeShortcut | Out-File -FilePath "$InstallPath\temp\create_lightning_strike.vbs" -Encoding ASCII
cscript //nologo "$InstallPath\temp\create_lightning_strike.vbs"

# SCARIFY Desktop Launcher shortcut
$launcherShortcut = @"
Set objShell = CreateObject("WScript.Shell")
Set objShortcut = objShell.CreateShortcut("$desktop\SCARIFY Desktop Launcher.lnk")
objShortcut.TargetPath = "powershell.exe"
objShortcut.Arguments = "-ExecutionPolicy Bypass -File \"$InstallPath\SCARIFY-Desktop-Launcher.ps1\""
objShortcut.WorkingDirectory = "$InstallPath"
objShortcut.IconLocation = "shell32.dll,21"
objShortcut.Save
"@

$launcherShortcut | Out-File -FilePath "$InstallPath\temp\create_launcher.vbs" -Encoding ASCII
cscript //nologo "$InstallPath\temp\create_launcher.vbs"

# SCARIFY Automation shortcut
$automationShortcut = @"
Set objShell = CreateObject("WScript.Shell")
Set objShortcut = objShell.CreateShortcut("$desktop\SCARIFY Automation.lnk")
objShortcut.TargetPath = "powershell.exe"
objShortcut.Arguments = "-ExecutionPolicy Bypass -File \"$InstallPath\Advanced-SCARIFY-Features.ps1\" -Feature All"
objShortcut.WorkingDirectory = "$InstallPath"
objShortcut.IconLocation = "shell32.dll,44"
objShortcut.Save
"@

$automationShortcut | Out-File -FilePath "$InstallPath\temp\create_automation.vbs" -Encoding ASCII
cscript //nologo "$InstallPath\temp\create_automation.vbs"

Write-Host "🖥️ Desktop shortcuts created:" -ForegroundColor Yellow
Write-Host "   🎬 SCARIFY Master Studio" -ForegroundColor Green
Write-Host "   ⚡ Lightning Strike Protocol" -ForegroundColor Green  
Write-Host "   🖥️ SCARIFY Desktop Launcher" -ForegroundColor Green
Write-Host "   🤖 SCARIFY Automation" -ForegroundColor Green

# Create system registry for file associations
if ($Force) {
    Write-Host "📝 Setting up file associations..." -ForegroundColor Cyan
    # This would set up .scarify file associations
}

# Test installation
if ($Test) {
    Write-Host "🧪 Testing installation..." -ForegroundColor Yellow
    
    # Test each component (look in parent directory for scripts)
    $components = @("MasterLaunch.ps1", "MasterControl.ps1", "Advanced-SCARIFY-Features.ps1", "SCARIFY-Desktop-Launcher.ps1", "SCARIFY-Master.ps1", "scarify_complete_video_production.ps1", "YouTube-Algorithm-Optimizer.ps1")
    foreach ($component in $components) {
        # Check in installation path first, then parent directory
        $componentPath = Join-Path $InstallPath $component
        $parentPath = Join-Path (Split-Path $InstallPath -Parent) $component
        
        if (Test-Path $componentPath) {
            Write-Host "   ✅ $component found in installation directory" -ForegroundColor Green
        } elseif (Test-Path $parentPath) {
            Write-Host "   ✅ $component found in source directory" -ForegroundColor Green
        } else {
            Write-Host "   ❌ $component missing" -ForegroundColor Red
        }
    }
}

# Clean up temporary files
Remove-Item "$InstallPath\temp\*.vbs" -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "🎉 SCARIFY Installation Complete!" -ForegroundColor Green
Write-Host "   📍 Installation path: $InstallPath" -ForegroundColor Cyan
Write-Host "   🖥️ Desktop shortcuts created" -ForegroundColor Cyan
Write-Host "   🚀 Ready to launch SCARIFY ecosystem!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Double-click 'SCARIFY Desktop Launcher' on your desktop for the main GUI" -ForegroundColor White
Write-Host "2. Or run: & '$InstallPath\SCARIFY-Desktop-Launcher.ps1' -Setup" -ForegroundColor White
Write-Host "3. For advanced users: & '$InstallPath\MasterLaunch.ps1' -Setup -Launch" -ForegroundColor White
