# ═══════════════════════════════════════════════════════════════════════════
# ABRAHAM LINCOLN - ULTIMATE FINAL LAUNCHER
# Combines all features: Real Lincoln images + Max Headroom effects + Auto-upload
# ═══════════════════════════════════════════════════════════════════════════

param([int]$Count = 50)

$ErrorActionPreference = "Continue"
$ROOT = "F:\AI_Oracle_Root\scarify"
$SCRIPT = "ABRAHAM_ULTIMATE_FINAL.py"

Write-Host ""
Write-Host "🔥 ABRAHAM LINCOLN - ULTIMATE FINAL EDITION 🔥" -ForegroundColor Red
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host ""
Write-Host "FEATURES:" -ForegroundColor Cyan
Write-Host "  ✅ Real Lincoln images from Wikimedia" -ForegroundColor Green
Write-Host "  ✅ Max Headroom TV static effects" -ForegroundColor Green
Write-Host "  ✅ Chapman 2025 fear-based targeting" -ForegroundColor Green
Write-Host "  ✅ Auto-upload to YouTube" -ForegroundColor Green
Write-Host "  ✅ Bitcoin/Product integration" -ForegroundColor Green
Write-Host ""

# Check if Python file exists
$pyFile = Join-Path $ROOT $SCRIPT
if (-not (Test-Path $pyFile)) {
    Write-Host "❌ $SCRIPT not found!" -ForegroundColor Red
    Write-Host "Expected location: $pyFile" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

Write-Host "✅ Found: $SCRIPT" -ForegroundColor Green
Write-Host ""
Write-Host "📺 Generating $Count Max Headroom Abe Lincoln videos..." -ForegroundColor Yellow
Write-Host "   Each video will be auto-uploaded to YouTube" -ForegroundColor Cyan
Write-Host ""

# Change to root directory
Set-Location $ROOT

# Run the script
python $SCRIPT $Count

$exitCode = $LASTEXITCODE

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Gray
if ($exitCode -eq 0) {
    Write-Host "✅ GENERATION COMPLETE!" -ForegroundColor Green
} else {
    Write-Host "⚠️ Generation finished with exit code: $exitCode" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "CHECK OUTPUT:" -ForegroundColor Cyan
Write-Host "  Videos: abraham_horror\videos\" -ForegroundColor White
Write-Host "  Uploaded: abraham_horror\uploaded\" -ForegroundColor White
Write-Host "  YouTube: Check your channel for uploads" -ForegroundColor White
Write-Host ""

# Open output folder
$uploadFolder = Join-Path $ROOT "abraham_horror\uploaded"
if (Test-Path $uploadFolder) {
    Start-Process explorer.exe -ArgumentList $uploadFolder
}

Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

