# ═══════════════════════════════════════════════════════════════════════════
# BATCH FIX ALL ABRAHAM LINCOLN VIDEOS
# Fixes screen directions, adds TV effect, proper voice
# ═══════════════════════════════════════════════════════════════════════════

$ROOT = "F:\AI_Oracle_Root\scarify\abraham_horror"

Write-Host ""
Write-Host "🔥 BATCH FIXING ALL ABRAHAM VIDEOS" -ForegroundColor Red
Write-Host ("=" * 70) -ForegroundColor Gray
Write-Host ""

Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install --quiet requests beautifulsoup4 lxml Pillow moviepy numpy 2>&1 | Out-Null

Write-Host ""
Write-Host "Running batch fix..." -ForegroundColor Yellow
Set-Location $ROOT
python FIX_ALL_VIDEOS.py

Write-Host ""
Write-Host "✅ BATCH FIX COMPLETE!" -ForegroundColor Green
Write-Host ""
Write-Host "Fixed videos are in: videos_fixed\" -ForegroundColor Cyan
Start-Process explorer.exe -ArgumentList "$ROOT\videos_fixed"


