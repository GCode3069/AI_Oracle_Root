# ABRAHAM STUDIO - LAUNCHER (STAYS OPEN)
# Launches GUI and keeps PowerShell window visible

$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Red
Write-Host "║   🎃 ABRAHAM STUDIO - LAUNCHER                          ║" -ForegroundColor Red
Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Red
Write-Host ""

$studioPath = "F:\AI_Oracle_Root\scarify\abraham_studio\ABRAHAM_STUDIO.pyw"

# Check if file exists
if (-not (Test-Path $studioPath)) {
    Write-Host "❌ ABRAHAM_STUDIO.pyw not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Expected location:" -ForegroundColor Yellow
    Write-Host "   $studioPath" -ForegroundColor White
    Write-Host ""
    Write-Host "📥 Please download ABRAHAM_STUDIO.pyw from outputs and place it here:" -ForegroundColor Cyan
    Write-Host "   F:\AI_Oracle_Root\scarify\abraham_studio\" -ForegroundColor White
    Write-Host ""
    Write-Host "Press any key to exit..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host "🚀 Launching ABRAHAM STUDIO..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Features:" -ForegroundColor Cyan
Write-Host "  ✓ Region selection (10 regions)" -ForegroundColor White
Write-Host "  ✓ Multi-language (EN/ES/PT/DE)" -ForegroundColor White
Write-Host "  ✓ Batch control (1-50 videos)" -ForegroundColor White
Write-Host "  ✓ Real stock footage (Pexels)" -ForegroundColor White
Write-Host "  ✓ Professional voice (ElevenLabs)" -ForegroundColor White
Write-Host "  ✓ Adult gore mode" -ForegroundColor White
Write-Host "  ✓ Progress tracking" -ForegroundColor White
Write-Host ""

# Launch the app
try {
    $process = Start-Process -FilePath "pythonw.exe" -ArgumentList "`"$studioPath`"" -PassThru
    
    Start-Sleep -Seconds 2
    
    Write-Host "✅ ABRAHAM STUDIO launched!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📝 The desktop app window should now be open" -ForegroundColor Cyan
    Write-Host "💰 Target: $15,000 from Halloween campaign" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "🎃 HOW TO USE:" -ForegroundColor Red
    Write-Host "   1. Select your region" -ForegroundColor White
    Write-Host "   2. Set batch count (e.g., 10)" -ForegroundColor White
    Write-Host "   3. Click 'GENERATE VIDEOS'" -ForegroundColor White
    Write-Host "   4. Wait for completion" -ForegroundColor White
    Write-Host "   5. Upload from youtube_ready folder" -ForegroundColor White
    Write-Host ""
    Write-Host "⏳ Keep this PowerShell window open while the app is running..." -ForegroundColor Magenta
    Write-Host ""
    Write-Host "Press any key to close this launcher window..." -ForegroundColor Gray
    
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    
} catch {
    Write-Host "❌ Failed to launch: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Try running directly:" -ForegroundColor Yellow
    Write-Host "   python $studioPath" -ForegroundColor White
    Write-Host ""
    Write-Host "Press any key to exit..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}
