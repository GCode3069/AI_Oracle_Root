# PROFESSIONAL ABRAHAM HORROR GENERATOR
# Real AI video, professional voice, live headlines

param([int]$Count = 1)

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Red
Write-Host "║   🎃 PROFESSIONAL ABRAHAM HORROR                        ║" -ForegroundColor Red
Write-Host "║   Real AI Video + Professional Voice                     ║" -ForegroundColor Red
Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Red
Write-Host ""

$script = Join-Path $PSScriptRoot "PROFESSIONAL_ABRAHAM.py"

Write-Host "🚀 Generating $Count professional video(s)..." -ForegroundColor Yellow
Write-Host ""

& python $script $Count

$exitCode = $LASTEXITCODE

if ($exitCode -eq 0) {
    Write-Host ""
    Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║   ✅ PROFESSIONAL VIDEOS READY                           ║" -ForegroundColor Green
    Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    
    $youtubeDir = "F:\AI_Oracle_Root\scarify\abraham_horror\youtube_ready"
    if (Test-Path $youtubeDir) {
        Write-Host "📁 Videos: $youtubeDir" -ForegroundColor Cyan
        Start-Process explorer.exe -ArgumentList $youtubeDir
    }
} else {
    Write-Host ""
    Write-Host "❌ Generation failed with code: $exitCode" -ForegroundColor Red
}

Write-Host ""

