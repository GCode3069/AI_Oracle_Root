# LAUNCH ABRAHAM STUDIO - Desktop App
# One-click launch for batch horror video generation

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Red
Write-Host "║   🎃 ABRAHAM STUDIO - Desktop App Launcher              ║" -ForegroundColor Red
Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Red
Write-Host ""

$studioPath = Join-Path $PSScriptRoot "ABRAHAM_STUDIO.pyw"

if (-not (Test-Path $studioPath)) {
    Write-Host "❌ ABRAHAM_STUDIO.pyw not found!" -ForegroundColor Red
    exit 1
}

Write-Host "Launching ABRAHAM STUDIO..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Features:" -ForegroundColor Cyan
Write-Host "  ✓ Region-based headline selection" -ForegroundColor White
Write-Host "  ✓ Multi-language support (EN/ES/PT/DE)" -ForegroundColor White
Write-Host "  ✓ Batch generation (1-50 videos)" -ForegroundColor White
Write-Host "  ✓ Halloween 2025 optimization" -ForegroundColor White
Write-Host "  ✓ Direct YouTube upload support" -ForegroundColor White
Write-Host ""

# Launch
Start-Process pythonw.exe -ArgumentList $studioPath

Write-Host "✅ ABRAHAM STUDIO launched!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Tip: The app will open in a new window" -ForegroundColor Yellow
Write-Host ""

