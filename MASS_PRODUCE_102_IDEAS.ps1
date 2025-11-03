# SCARIFY - Mass Production from 102 Horror Ideas
# Generates all 102 unique videos with Lincoln branding

param(
    [int]$BatchSize = 50,
    [int]$StartFrom = 1,
    [switch]$UploadImmediately
)

$ROOT = "F:\AI_Oracle_Root\scarify"
$ABRAHAM_DIR = "$ROOT\abraham_horror"

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Red
Write-Host "SCARIFY - 102 HORROR IDEAS MASS PRODUCTION" -ForegroundColor Red
Write-Host "=" * 70 -ForegroundColor Red
Write-Host ""
Write-Host "Batch Size: $BatchSize" -ForegroundColor Yellow
Write-Host "Starting From: ID $StartFrom" -ForegroundColor Yellow
Write-Host "Upload: $(if($UploadImmediately){'YES'}else{'NO'})" -ForegroundColor Yellow
Write-Host ""
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host ""

# Generate batch manifest
Write-Host "[1] Creating batch from horror ideas database..." -ForegroundColor Cyan
cd $ROOT
python GENERATE_FROM_IDEAS.py $BatchSize $StartFrom

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] Failed to create batch manifest" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[OK] Batch manifest created" -ForegroundColor Green
Write-Host ""

# Generate videos
Write-Host "[2] Generating $BatchSize professional videos..." -ForegroundColor Cyan
Write-Host ""

cd $ABRAHAM_DIR
python ABRAHAM_PROFESSIONAL_UPGRADE.py $BatchSize

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] Video generation failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[OK] Video generation complete" -ForegroundColor Green
Write-Host ""

# Upload if requested
if ($UploadImmediately) {
    Write-Host "[3] Uploading to 15 channels..." -ForegroundColor Cyan
    Write-Host ""
    
    cd $ROOT
    python MULTI_CHANNEL_UPLOADER.py "$ABRAHAM_DIR\youtube_ready" round-robin
    
    Write-Host ""
    Write-Host "[OK] Upload complete" -ForegroundColor Green
    Write-Host ""
}

# Summary
Write-Host ""
Write-Host "=" * 70 -ForegroundColor Green
Write-Host "PRODUCTION COMPLETE" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Green
Write-Host ""
Write-Host "Generated: $BatchSize videos" -ForegroundColor White
Write-Host "From Ideas: #$StartFrom to #$($StartFrom + $BatchSize - 1)" -ForegroundColor White
Write-Host "Location: $ABRAHAM_DIR\youtube_ready" -ForegroundColor White
Write-Host ""

if (-not $UploadImmediately) {
    Write-Host "NEXT STEP:" -ForegroundColor Yellow
    Write-Host "  Upload videos: python MULTI_CHANNEL_UPLOADER.py abraham_horror/youtube_ready round-robin" -ForegroundColor White
    Write-Host ""
}

Write-Host "Monitor:" -ForegroundColor Cyan
Write-Host "  python check_balance.py" -ForegroundColor White
Write-Host "  python analytics_tracker.py report" -ForegroundColor White
Write-Host ""
Write-Host "=" * 70 -ForegroundColor Green
Write-Host ""


