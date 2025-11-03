# ═══════════════════════════════════════════════════════════════════════════
# ABE LINCOLN MAX HEADROOM - SIMPLE LAUNCHER
# Just run this file - it does everything
# ═══════════════════════════════════════════════════════════════════════════

param([int]$Count = 50)

$ErrorActionPreference = "Stop"
$ROOT = "F:\AI_Oracle_Root\scarify\abraham_horror"

Write-Host ""
Write-Host "📺 ABE LINCOLN - MAX HEADROOM EDITION 📺" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host ""

# Check if Python file exists
$pyFile = Join-Path $ROOT "abe_maxheadroom.py"
if (-not (Test-Path $pyFile)) {
    Write-Host "❌ abe_maxheadroom.py not found!" -ForegroundColor Red
    Write-Host "Expected location: $pyFile" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Download it from Claude and put it in:" -ForegroundColor Yellow
    Write-Host "  F:\AI_Oracle_Root\scarify\abraham_horror\" -ForegroundColor White
    Write-Host ""
    exit 1
}

Write-Host "✅ Found: abe_maxheadroom.py" -ForegroundColor Green
Write-Host ""

# Run it
Write-Host "🚀 Generating $Count Max Headroom videos..." -ForegroundColor Yellow
Write-Host ""

Set-Location $ROOT
python abe_maxheadroom.py $Count

Write-Host ""
Write-Host "✅ DONE!" -ForegroundColor Green
Write-Host ""
Write-Host "Videos saved to: uploaded\" -ForegroundColor Cyan

Start-Process explorer.exe -ArgumentList (Join-Path $ROOT "uploaded")
