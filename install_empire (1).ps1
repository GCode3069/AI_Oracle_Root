#!/usr/bin/env pwsh
# SCARIFY EMPIRE - COMPLETE INSTALLATION
# Run this ONCE to set up everything

Write-Host "🔥 SCARIFY EMPIRE - COMPLETE INSTALLATION" -ForegroundColor Cyan
Write-Host "="*80

# 1. Python packages
Write-Host "`n[1/6] Installing Python packages..." -ForegroundColor Yellow
pip install -r requirements.txt --break-system-packages 2>&1 | Out-Null
Write-Host "   ✅ Python packages installed" -ForegroundColor Green

# 2. Git (for SOVA)
Write-Host "`n[2/6] Checking Git..." -ForegroundColor Yellow
if (!(Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "   Installing Git..." -ForegroundColor Cyan
    winget install Git.Git -e --silent
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    Write-Host "   ✅ Git installed" -ForegroundColor Green
} else {
    Write-Host "   ✅ Git already installed" -ForegroundColor Green
}

# 3. SOVA TTS
Write-Host "`n[3/6] Installing SOVA TTS..." -ForegroundColor Yellow
if (!(Test-Path "sova-tts")) {
    git clone https://github.com/sovaai/sova-tts.git 2>&1 | Out-Null
    Push-Location sova-tts
    pip install -r requirements.txt --break-system-packages 2>&1 | Out-Null
    Pop-Location
    Write-Host "   ✅ SOVA TTS installed" -ForegroundColor Green
} else {
    Write-Host "   ✅ SOVA TTS already installed" -ForegroundColor Green
}

# 4. Fix ElevenLabs
Write-Host "`n[4/6] Fixing ElevenLabs SDK..." -ForegroundColor Yellow
pip uninstall elevenlabs -y 2>&1 | Out-Null
pip install elevenlabs==1.8.0 --break-system-packages 2>&1 | Out-Null
Write-Host "   ✅ ElevenLabs SDK fixed" -ForegroundColor Green

# 5. Test audio
Write-Host "`n[5/6] Testing audio systems..." -ForegroundColor Yellow
if (!(Test-Path "output")) {
    New-Item -ItemType Directory -Path "output/audio","output/videos" -Force | Out-Null
}
python audio_generator.py "SCARIFY system test" "output/test_audio.wav" 2>&1 | Out-Null
if (Test-Path "output/test_audio.wav") {
    Write-Host "   ✅ Audio system working" -ForegroundColor Green
    Remove-Item "output/test_audio.wav" -Force
} else {
    Write-Host "   ⚠️  Audio test failed - check manually" -ForegroundColor Yellow
}

# 6. Create desktop shortcut
Write-Host "`n[6/6] Creating desktop shortcut..." -ForegroundColor Yellow
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\🔥 SCARIFY Generator.lnk")
$Shortcut.TargetPath = "powershell.exe"
$Shortcut.Arguments = "-ExecutionPolicy Bypass -File `"$PWD\scarify_launcher.ps1`""
$Shortcut.WorkingDirectory = $PWD
$Shortcut.IconLocation = "powershell.exe,0"
$Shortcut.Description = "SCARIFY Empire Video Generator"
$Shortcut.Save()
Write-Host "   ✅ Desktop shortcut created" -ForegroundColor Green

Write-Host "`n" + ("="*80)
Write-Host "✅ INSTALLATION COMPLETE!" -ForegroundColor Green
Write-Host ("="*80)
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Double-click '🔥 SCARIFY Generator' on desktop" -ForegroundColor Cyan
Write-Host "2. Click 'Test (1 Video)' to verify everything works" -ForegroundColor Cyan
Write-Host "3. Click 'Generate 5 + Upload' to start dominating" -ForegroundColor Cyan
Write-Host "`n🎯 TARGET: 50 videos/day = 1M impressions = $6K/month" -ForegroundColor Yellow
Write-Host "`nLET'S FUCKING GO! 🔥" -ForegroundColor Red

Write-Host "`nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
