# ABRAHAM HORROR - WORKING FINAL
# Generates REAL videos with professional voice
# AUTO-UPLOADS TO YOUTUBE

param([int]$Count = 1, [switch]$SkipUpload)

Write-Host ""
Write-Host "ABRAHAM HORROR - GENERATING $Count VIDEO(S)" -ForegroundColor Red
Write-Host ""

$BASE_DIR = "F:\AI_Oracle_Root\scarify\abraham_horror"

# Create directories
foreach ($dir in @("audio", "videos", "youtube_ready")) {
    $path = Join-Path $BASE_DIR $dir
    if (-not (Test-Path $path)) {
        New-Item -Path $path -ItemType Directory -Force | Out-Null
    }
}

# Run Python generator
python working_abraham.py $Count

Write-Host ""
Write-Host "COMPLETE!" -ForegroundColor Green
Write-Host ""
Write-Host "Videos in: $BASE_DIR\youtube_ready" -ForegroundColor Cyan
Write-Host ""
Write-Host "Double-click to open folder..." -ForegroundColor Yellow

Start-Sleep -Seconds 2
Start-Process explorer.exe -ArgumentList "$BASE_DIR\youtube_ready"

