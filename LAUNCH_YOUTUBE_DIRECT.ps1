# ABRAHAM HORROR - DIRECT YOUTUBE UPLOAD LAUNCHER
# Generates videos and uploads directly to YouTube via terminal

param(
    [int]$Count = 1,
    [switch]$Test
)

$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host "="*70 -ForegroundColor Cyan
Write-Host " ABRAHAM HORROR - DIRECT YOUTUBE UPLOAD" -ForegroundColor Yellow
Write-Host "="*70 -ForegroundColor Cyan
Write-Host ""

Set-Location "F:\AI_Oracle_Root\scarify"

# Check if working_abraham.py exists
if (-not (Test-Path "working_abraham.py")) {
    Write-Host "ERROR: working_abraham.py not found!" -ForegroundColor Red
    exit 1
}

Write-Host "Processing $Count video(s)..." -ForegroundColor Green
Write-Host ""

# Run the generator
python working_abraham.py $Count

# Check for errors
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Generation failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "="*70 -ForegroundColor Green
Write-Host " COMPLETE!" -ForegroundColor Yellow
Write-Host "="*70 -ForegroundColor Green
Write-Host ""
Write-Host "Videos uploaded to YouTube channel" -ForegroundColor Cyan
Write-Host ""

# Open YouTube Studio
Start-Process "https://studio.youtube.com"

exit 0

