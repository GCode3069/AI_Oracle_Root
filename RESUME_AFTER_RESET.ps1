# RESUME AFTER RESET - ONE COMMAND TO CONTINUE
# Run this after laptop reset to verify everything works

Write-Host "`n" -NoNewline
Write-Host "================================================================================" -ForegroundColor Green
Write-Host "  SCARIFY - RESUME AFTER RESET" -ForegroundColor Yellow
Write-Host "================================================================================" -ForegroundColor Green
Write-Host ""

# Navigate to project
Set-Location "F:\AI_Oracle_Root\scarify"

Write-Host "[1/4] Checking repository..." -ForegroundColor Cyan
if (Test-Path "abraham_MAX_HEADROOM.py") {
    Write-Host "  [OK] Main system present" -ForegroundColor Green
} else {
    Write-Host "  [ERROR] Files missing!" -ForegroundColor Red
    exit 1
}

Write-Host "`n[2/4] Checking latest videos on YouTube..." -ForegroundColor Cyan
Write-Host "  Episode #7000: https://youtube.com/watch?v=LlXKY4SNiUo" -ForegroundColor White
Write-Host "  Episode #5002: https://youtube.com/watch?v=qvoL9BgsVWQ (198% engagement!)" -ForegroundColor White
Write-Host "  Check these for:" -ForegroundColor Yellow
Write-Host "    - Video plays (no buffering)" -ForegroundColor White
Write-Host "    - Audio works" -ForegroundColor White
Write-Host "    - Cash App QR visible (top-right)" -ForegroundColor White

Write-Host "`n[3/4] Testing generator..." -ForegroundColor Cyan
$env:EPISODE_NUM="8100"
Write-Host "  Generating test video (Episode #8100)..." -ForegroundColor White

python VERIFIED_WORKING_GENERATOR.py

Write-Host "`n[4/4] Status check..." -ForegroundColor Cyan

if (Test-Path "abraham_horror\uploaded\VERIFIED_8100.mp4") {
    Write-Host "  [OK] Generator working!" -ForegroundColor Green
    Write-Host "`n[SUCCESS] System operational after reset!" -ForegroundColor Green
    Write-Host "`nNext steps:" -ForegroundColor Yellow
    Write-Host "  1. Wait 5-10 min for YouTube processing" -ForegroundColor White
    Write-Host "  2. Check videos play without buffering" -ForegroundColor White
    Write-Host "  3. If working, generate more:" -ForegroundColor White
    Write-Host "     python REPLICATE_198_PERCENT_SUCCESS.py 10" -ForegroundColor Cyan
} else {
    Write-Host "  [WARN] Generator may have issues" -ForegroundColor Yellow
}

Write-Host "`n" -NoNewline
Write-Host "================================================================================" -ForegroundColor Green
Write-Host ""



