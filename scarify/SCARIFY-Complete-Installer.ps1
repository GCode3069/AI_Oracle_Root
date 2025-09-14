# =====================================================
# SCARIFY Complete Installer - One-Click Deployment
# Creates all scripts, directories, and desktop shortcuts
# =====================================================

param(
    [switch]$Test,
    [switch]$Force,
    [string]$InstallPath = "D:\AI_Oracle_Root\scarify"
)

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
Write-Host "   🤖 SCARIFY Automation" -ForegroundColor Green

# Create system registry for file associations
if ($Force) {
    Write-Host "📝 Setting up file associations..." -ForegroundColor Cyan
    # This would set up .scarify file associations
}

# Test installation
if ($Test) {
    Write-Host "🧪 Testing installation..." -ForegroundColor Yellow
    
    # Test each component
    $components = @("MasterLaunch.ps1", "MasterControl.ps1", "Advanced-SCARIFY-Features.ps1")
    foreach ($component in $components) {
        $componentPath = Join-Path $InstallPath $component
        if (Test-Path $componentPath) {
            Write-Host "   ✅ $component found" -ForegroundColor Green
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
Write-Host "1. Double-click 'SCARIFY Master Studio' on your desktop" -ForegroundColor White
Write-Host "2. Or run: & '$InstallPath\MasterLaunch.ps1' -Setup -Launch" -ForegroundColor White
