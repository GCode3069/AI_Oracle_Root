# GENERATE.PS1 - WORKING LINCOLN HORROR GENERATOR
# NO API KEYS REQUIRED - GENERATES REAL VIDEOS

param([int]$Count = 1)

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Red
Write-Host "║   🩸 LINCOLN HORROR GENERATOR - WORKING                  ║" -ForegroundColor Red
Write-Host "║   NO API KEYS NEEDED                                     ║" -ForegroundColor Red
Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Red
Write-Host ""

$ErrorActionPreference = "Continue"

# Check Python
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found!" -ForegroundColor Red
    exit 1
}

# Run the working generator
$script = Join-Path $PSScriptRoot "WORKING_GENERATOR.py"

Write-Host "🚀 Generating $Count video(s)..." -ForegroundColor Yellow
Write-Host ""

& python $script $Count

$exitCode = $LASTEXITCODE

if ($exitCode -eq 0) {
    Write-Host ""
    Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║   ✅ GENERATION COMPLETE                                ║" -ForegroundColor Green
    Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    Write-Host "📁 Videos: F:\AI_Oracle_Root\scarify\output\videos" -ForegroundColor Cyan
    Write-Host "📄 Scripts: F:\AI_Oracle_Root\scarify\output\scripts" -ForegroundColor Cyan
    Write-Host "🎵 Audio: F:\AI_Oracle_Root\scarify\output\audio" -ForegroundColor Cyan
    Write-Host ""
    
    # Open folder
    Start-Process explorer.exe -ArgumentList "F:\AI_Oracle_Root\scarify\output\videos"
} else {
    Write-Host ""
    Write-Host "❌ Generation failed with code: $exitCode" -ForegroundColor Red
}

Write-Host ""

