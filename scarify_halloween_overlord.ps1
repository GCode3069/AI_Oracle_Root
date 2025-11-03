# SCARIFY Halloween Overlord - Unified Execution Script
# Combines EMPIRE FORGE 2.0 + 15-Channel Psychological Operation
# $10K revenue target in 72 hours

param(
    [switch]$TestMode = $false,
    [switch]$GenOnly = $false,
    [int]$Duration = 72
)

$ErrorActionPreference = "Continue"

Write-Host "🔥 SCARIFY HALLOWEEN OVERLORD - UNIFIED EXECUTION" -ForegroundColor Red
Write-Host "="*80

# Configuration
$baseDir = $PSScriptRoot
$outputDir = Join-Path $baseDir "outputs"
$logFile = Join-Path $outputDir "overlord_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"

# Ensure output directory exists
New-Item -ItemType Directory -Path $outputDir -Force | Out-Null

function Log-Message {
    param([string]$msg)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "$timestamp - $msg"
    Add-Content -Path $logFile -Value $logEntry
    Write-Host "📝 $msg"
}

Log-Message "Starting SCARIFY Halloween Overlord"
Log-Message "Test Mode: $TestMode"
Log-Message "Generation Only: $GenOnly"
Log-Message "Duration: $Duration hours"

# Phase 1: Environment Check
Write-Host "`n▶ PHASE 1: Environment Check" -ForegroundColor Yellow
Log-Message "Checking dependencies..."

# Check Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "   ❌ Python not found" -ForegroundColor Red
    Log-Message "ERROR: Python not installed"
    exit 1
}
Write-Host "   ✅ Python found" -ForegroundColor Green

# Check FFmpeg
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
    Write-Host "   ⚠️  FFmpeg not found (optional)" -ForegroundColor Yellow
    Log-Message "WARNING: FFmpeg not installed"
} else {
    Write-Host "   ✅ FFmpeg found" -ForegroundColor Green
}

# Install Python dependencies
Write-Host "`n▶ Installing Python dependencies..." -ForegroundColor Yellow
$requirements = @(
    "moviepy",
    "pyyaml",
    "google-api-python-client",
    "google-auth-oauthlib",
    "google-auth-httplib2"
)

foreach ($pkg in $requirements) {
    Write-Host "   Installing $pkg..." -NoNewline
    python -m pip install $pkg -q 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host " ✅" -ForegroundColor Green
    } else {
        Write-Host " ⚠️" -ForegroundColor Yellow
    }
}

# Phase 2: Configuration Setup
Write-Host "`n▶ PHASE 2: Configuration Setup" -ForegroundColor Yellow

# Check configuration files
$configFiles = @(
    "configs/chapman_2025.yaml",
    "accounts/channels.yaml"
)

foreach ($file in $configFiles) {
    $filePath = Join-Path $baseDir $file
    if (Test-Path $filePath) {
        Write-Host "   ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $file missing" -ForegroundColor Red
        Log-Message "ERROR: Missing configuration file: $file"
    }
}

# Phase 3: Asset Preparation
Write-Host "`n▶ PHASE 3: Asset Preparation" -ForegroundColor Yellow

# Create placeholder audio if needed
$audioDir = Join-Path $baseDir "audio"
$rattlePath = Join-Path $audioDir "heartbeat_rattle.wav"

if (-not (Test-Path $rattlePath)) {
    Write-Host "   📝 Creating placeholder audio..." -ForegroundColor Yellow
    Log-Message "Creating placeholder audio file"
    
    # Create silent audio placeholder using Python
    $pythonScript = @"
from moviepy.editor import AudioClip
import numpy as np

def make_frame(t):
    # Generate low frequency rumble
    freq = 4  # 4Hz theta
    return np.array([np.sin(2 * np.pi * freq * t)] * 2) * 0.3

audio = AudioClip(make_frame, duration=10.0, fps=44100)
audio.write_audiofile('$($rattlePath.Replace('\', '/'))', fps=44100, verbose=False, logger=None)
"@
    
    $pythonScript | python 2>&1 | Out-Null
    
    if (Test-Path $rattlePath) {
        Write-Host "   ✅ Audio placeholder created" -ForegroundColor Green
    }
}

# Phase 4: Test Generation
if ($TestMode) {
    Write-Host "`n▶ PHASE 4: Test Generation" -ForegroundColor Yellow
    Log-Message "Running test generation..."
    
    $scriptPath = Join-Path $baseDir "scripts\scarify_blitz.py"
    
    Write-Host "   🎬 Generating test clip..." -ForegroundColor Cyan
    python $scriptPath --test --fear corrupt_gov
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Test generation complete" -ForegroundColor Green
        Log-Message "Test generation successful"
    } else {
        Write-Host "   ❌ Test generation failed" -ForegroundColor Red
        Log-Message "ERROR: Test generation failed"
    }
    
    Write-Host "`n🎯 TEST MODE COMPLETE" -ForegroundColor Green
    Write-Host "📁 Output: $outputDir"
    Write-Host "📝 Log: $logFile"
    exit 0
}

# Phase 5: Full Blitzkrieg Execution
Write-Host "`n▶ PHASE 5: Blitzkrieg Execution" -ForegroundColor Yellow
Log-Message "Starting 72-hour blitzkrieg operation..."

$scriptPath = Join-Path $baseDir "scripts\scarify_blitz.py"

if ($GenOnly) {
    Write-Host "   🎬 Generation Only Mode" -ForegroundColor Cyan
    python $scriptPath --gen-only --fear corrupt_gov
} else {
    Write-Host "   🚀 Full Blitzkrieg Mode" -ForegroundColor Cyan
    Write-Host "   Duration: $Duration hours" -ForegroundColor Cyan
    Write-Host "   Target: $10K revenue" -ForegroundColor Cyan
    
    python $scriptPath --duration $Duration
}

# Phase 6: Summary
Write-Host "`n" + "="*80
Write-Host "🎯 SCARIFY HALLOWEEN OVERLORD EXECUTION COMPLETE" -ForegroundColor Green
Write-Host "="*80
Write-Host "📁 Output Directory: $outputDir"
Write-Host "📝 Log File: $logFile"
Write-Host "🔗 Next Steps:"
Write-Host "   1. Review generated clips in outputs/"
Write-Host "   2. Configure YouTube OAuth tokens for upload"
Write-Host "   3. Monitor analytics dashboard"
Write-Host "   4. Scale based on performance"
Write-Host "="*80

Log-Message "Overlord execution complete"

