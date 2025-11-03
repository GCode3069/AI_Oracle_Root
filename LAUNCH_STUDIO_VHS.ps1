# LAUNCH ABRAHAM STUDIO - VHS TV BROADCAST DESKTOP GENERATOR

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "  📺 ABRAHAM STUDIO - VHS TV BROADCAST GENERATOR" -ForegroundColor Red
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""
Write-Host "  🎬 Max Headroom Style" -ForegroundColor White
Write-Host "  📺 Full VHS TV Effects" -ForegroundColor White
Write-Host "  🧠 Psychological Audio (Secret Sauce)" -ForegroundColor White
Write-Host "  🔢 Episode Numbering" -ForegroundColor White
Write-Host "  ⚡ Batch Generation" -ForegroundColor White
Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

$ROOT = "F:\AI_Oracle_Root\scarify"

# Check if Python is available
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Install Python 3.8+`n" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit
}

# Check if script exists
$scriptPath = Join-Path $ROOT "ABRAHAM_STUDIO_VHS.pyw"
if (-not (Test-Path $scriptPath)) {
    Write-Host "❌ Script not found: $scriptPath`n" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit
}

Write-Host "✅ Script found" -ForegroundColor Green
Write-Host "🚀 Launching desktop generator...`n" -ForegroundColor Cyan

# Launch the GUI
Set-Location $ROOT
Start-Process python -ArgumentList $scriptPath -WindowStyle Hidden

Start-Sleep -Seconds 2

Write-Host "✅ Desktop generator launched!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 INSTRUCTIONS:" -ForegroundColor Yellow
Write-Host "  1. Set batch count (how many videos to generate)" -ForegroundColor White
Write-Host "  2. Set starting episode number (e.g., 1000)" -ForegroundColor White
Write-Host "  3. Enable/disable psychological audio" -ForegroundColor White
Write-Host "  4. Click 'GENERATE VHS BROADCASTS'" -ForegroundColor White
Write-Host "  5. Videos will be saved to videos\youtube_ready\" -ForegroundColor White
Write-Host ""
Write-Host "💡 TIP: Use 'TEST SINGLE' to generate one video first" -ForegroundColor Cyan
Write-Host ""

