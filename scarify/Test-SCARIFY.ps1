# SCARIFY Test Script
# GCode3069 | UTC: 2025-09-02 05:56:03

Set-Location $PSScriptRoot

Write-Host "===== SCARIFY System Test =====" -ForegroundColor Cyan
Write-Host "Current UTC time: $(Get-Date -AsUtc)" -ForegroundColor Gray
Write-Host "User: $env:USERNAME" -ForegroundColor Gray
Write-Host

try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python detected: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "✗ Python not found. Please install Python 3.8 or newer." -ForegroundColor Red
    exit
}

try {
    $ffmpegVersion = ffmpeg -version | Select-Object -First 1
    Write-Host "✓ FFmpeg detected: $ffmpegVersion" -ForegroundColor Green
}
catch {
    Write-Host "✗ FFmpeg not found. Please install FFmpeg." -ForegroundColor Red
    exit
}

if ($env:ELEVEN_LABS_API_KEY) {
    Write-Host "✓ ElevenLabs API key is set" -ForegroundColor Green
} else {
    Write-Host "✗ ElevenLabs API key is not set. Run Configure-ApiKeys.ps1 first." -ForegroundColor Red
}

Write-Host "`nTesting script generation..." -ForegroundColor Yellow
$outputScript = Join-Path $PSScriptRoot "Output/ShortsReady/test_script.json"
python cinematic_teaser.py -t "NightmareCity" -o $outputScript

if (Test-Path $outputScript) {
    Write-Host "✓ Script generation successful: $outputScript" -ForegroundColor Green

    Write-Host "`nTesting TTS generation..." -ForegroundColor Yellow
    $outputAudio = Join-Path $PSScriptRoot "Output/ShortsReady/test_audio.mp3"
    python tts_enhanced.py -i $outputScript -o $outputAudio --test

    if (Test-Path $outputAudio) {
        Write-Host "✓ TTS generation successful: $outputAudio" -ForegroundColor Green
    }
    else {
        Write-Host "✗ TTS generation failed" -ForegroundColor Red
    }
}
else {
    Write-Host "✗ Script generation failed" -ForegroundColor Red
}

Write-Host "`nSystem check complete. Fix any issues before proceeding." -ForegroundColor Cyan
