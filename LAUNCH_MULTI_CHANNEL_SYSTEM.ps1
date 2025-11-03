# SCARIFY - MULTI-CHANNEL LAUNCH SYSTEM
# Automates the entire 15-channel operation

param(
    [int]$VideoCount = 50,
    [switch]$TestMode,
    [switch]$SetupChannels
)

$ROOT = "F:\AI_Oracle_Root\scarify"
$ABRAHAM_DIR = "$ROOT\abraham_horror"

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Red
Write-Host "SCARIFY - MULTI-CHANNEL SYSTEM" -ForegroundColor Red
Write-Host "=" * 70 -ForegroundColor Red
Write-Host ""

# Step 1: Setup channels if requested
if ($SetupChannels) {
    Write-Host "[STEP 1] CHANNEL SETUP" -ForegroundColor Cyan
    Write-Host "Setting up 15 YouTube channels..." -ForegroundColor Yellow
    Write-Host "You'll need to log in 15 times with different accounts" -ForegroundColor Yellow
    Write-Host ""
    
    $confirm = Read-Host "Continue with channel setup? (y/n)"
    if ($confirm -eq 'y') {
        python "$ROOT\MULTI_CHANNEL_SETUP.py" setup 15
    } else {
        Write-Host "Skipping channel setup" -ForegroundColor Yellow
    }
    Write-Host ""
}

# Step 2: Generate videos
Write-Host "[STEP 2] VIDEO GENERATION" -ForegroundColor Cyan
Write-Host "Generating $VideoCount professional videos..." -ForegroundColor Yellow
Write-Host ""

cd $ABRAHAM_DIR

if ($TestMode) {
    Write-Host "[TEST MODE] Generating 3 test videos..." -ForegroundColor Yellow
    python "ABRAHAM_PROFESSIONAL_UPGRADE.py" 3
} else {
    python "ABRAHAM_PROFESSIONAL_UPGRADE.py" $VideoCount
}

Write-Host ""
Write-Host "[OK] Video generation complete" -ForegroundColor Green
Write-Host ""

# Step 3: Distribute across channels
Write-Host "[STEP 3] MULTI-CHANNEL DISTRIBUTION" -ForegroundColor Cyan
Write-Host "Uploading to 15 channels..." -ForegroundColor Yellow
Write-Host ""

cd $ROOT

if ($TestMode) {
    Write-Host "[TEST MODE] Simulating uploads..." -ForegroundColor Yellow
    python "MULTI_CHANNEL_UPLOADER.py" "$ABRAHAM_DIR\youtube_ready" round-robin --test
} else {
    python "MULTI_CHANNEL_UPLOADER.py" "$ABRAHAM_DIR\youtube_ready" round-robin
}

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Green
Write-Host "SCARIFY SYSTEM OPERATIONAL" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Green
Write-Host ""
Write-Host "Videos Generated: $VideoCount" -ForegroundColor White
Write-Host "Channels Active: 15" -ForegroundColor White
Write-Host "Distribution: Round-robin" -ForegroundColor White
Write-Host ""
Write-Host "Monitor results in:" -ForegroundColor Cyan
Write-Host "  $ROOT\upload_results_*.json" -ForegroundColor White
Write-Host ""
Write-Host "Bitcoin: bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt" -ForegroundColor Yellow
Write-Host "Product: https://trenchaikits.com/buy-rebel-`$97" -ForegroundColor Yellow
Write-Host ""


