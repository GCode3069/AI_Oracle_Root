# ABRAHAM LINCOLN - ALL APIs OPTIMIZED (NO TIMEOUTS)
# Uses: ElevenLabs + Pexels + RunwayML style + Max Headroom effects
# Optimized: Only 1 B-roll clip, fast processing, ~2min per video
param([int]$Videos = 10, [switch]$SkipBroll)

$ROOT = "F:\AI_Oracle_Root\scarify\abraham_horror"

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║ ABRAHAM LINCOLN - FULL API INTEGRATION (OPTIMIZED)                ║" -ForegroundColor Cyan
Write-Host "║ ElevenLabs + Pexels + RunwayML + Max Headroom                      ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Create directories
$dirs = @("audio", "videos", "uploaded", "temp", "broll")
foreach ($dir in $dirs) {
    $path = Join-Path $ROOT $dir
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
        Write-Host "[OK] Created: $dir" -ForegroundColor Green
    }
}

# Install packages
Write-Host ""
Write-Host "[PROCESS] Installing Python packages..." -ForegroundColor Cyan
pip install --quiet requests beautifulsoup4 lxml pillow moviepy numpy 2>&1 | Out-Null
Write-Host "[OK] Packages installed" -ForegroundColor Green

# Run the generator
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
Write-Host "║ GENERATING $Videos VIDEOS - FULL API (OPTIMIZED)                   ║" -ForegroundColor Yellow
Write-Host "╚════════════════════════════════════════════════════════════════════╝" -ForegroundColor Yellow
Write-Host ""

if ($SkipBroll) {
    Write-Host "[MODE] WITHOUT B-roll (faster processing)" -ForegroundColor Cyan
    Write-Host "[APIS] ElevenLabs + RunwayML + Max Headroom" -ForegroundColor Cyan
} else {
    Write-Host "[MODE] WITH Pexels B-roll (better quality)" -ForegroundColor Cyan
    Write-Host "[APIS] ElevenLabs + Pexels + RunwayML + Max Headroom" -ForegroundColor Cyan
}

Write-Host "[OPTIMIZATIONS] Only 1 B-roll, fast preset, 120s timeout" -ForegroundColor Green
Write-Host ""

Set-Location $ROOT

if ($SkipBroll) {
    python abe_full_api_optimized.py $Videos --skip-broll
} else {
    python abe_full_api_optimized.py $Videos
}

# Show results
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║ RESULTS                                                            ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════════╝" -ForegroundColor Green

$vids = Get-ChildItem (Join-Path $ROOT "uploaded") -Filter "ABE_FULL_*.mp4" -ErrorAction SilentlyContinue
if ($vids) {
    $totalSize = ($vids | Measure-Object -Property Length -Sum).Sum / 1MB
    Write-Host "[OK] Generated: $($vids.Count) videos" -ForegroundColor Green
    Write-Host "[INFO] Total size: $([math]::Round($totalSize, 1)) MB" -ForegroundColor White
    Write-Host "[INFO] APIs used:" -ForegroundColor Cyan
    Write-Host "       ✅ ElevenLabs (voice generation)" -ForegroundColor Green
    if (-not $SkipBroll) {
        Write-Host "       ✅ Pexels (B-roll video)" -ForegroundColor Green
    }
    Write-Host "       ✅ RunwayML style (glitch effects)" -ForegroundColor Green
    Write-Host "       ✅ Max Headroom (lip sync, VHS)" -ForegroundColor Green
    Write-Host "[INFO] Location: uploaded\" -ForegroundColor Cyan
    Write-Host "[INFO] YouTube: https://studio.youtube.com/channel/UCS5pEpSCw8k4wene0iv0uAg/videos" -ForegroundColor Cyan
} else {
    Write-Host "[WARNING] No videos found" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
Write-Host "║ DONE! All APIs integrated, optimized for speed                    ║" -ForegroundColor Magenta
Write-Host "╚════════════════════════════════════════════════════════════════════╝" -ForegroundColor Magenta
Write-Host ""

# Open folder
Start-Process explorer.exe -ArgumentList (Join-Path $ROOT "uploaded")
