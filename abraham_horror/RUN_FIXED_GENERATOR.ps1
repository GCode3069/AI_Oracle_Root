# ═══════════════════════════════════════════════════════════════════════════
# RUN FIXED ABRAHAM LINCOLN GENERATOR
# ✅ No screen directions ✅ TV effect ✅ Proper male voice
# ═══════════════════════════════════════════════════════════════════════════

param([int]$Count = 50)

$ROOT = "F:\AI_Oracle_Root\scarify\abraham_horror"

Write-Host ""
Write-Host "🔥 ABRAHAM LINCOLN - FIXED GENERATOR" -ForegroundColor Red
Write-Host ("=" * 70) -ForegroundColor Gray
Write-Host ""
Write-Host "✅ No screen directions in audio" -ForegroundColor Green
Write-Host "✅ Abe visible speaking from staticky TV" -ForegroundColor Green
Write-Host "✅ Proper deep male Lincoln voice" -ForegroundColor Green
Write-Host ""

# Install dependencies
pip install --quiet requests beautifulsoup4 lxml Pillow moviepy numpy 2>&1 | Out-Null

# Ensure directories exist
$dirs = @("audio", "videos", "uploaded", "temp", "images")
foreach ($dir in $dirs) {
    $path = Join-Path $ROOT $dir
    if (-not (Test-Path $path)) { 
        New-Item -ItemType Directory -Path $path -Force | Out-Null
    }
}

# Check for Lincoln image
$lincolnImg = Join-Path $ROOT "images\lincoln_portrait.jpg"
if (-not (Test-Path $lincolnImg)) {
    Write-Host "⚠️  Warning: Lincoln portrait not found at:" -ForegroundColor Yellow
    Write-Host "   $lincolnImg" -ForegroundColor Gray
    Write-Host "   Placeholder will be used. Add real image for best results." -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "🚀 GENERATING $Count FIXED VIDEOS..." -ForegroundColor Yellow
Write-Host ""

Set-Location $ROOT
python abraham_LONG_RANTS_FIXED.py $Count

Write-Host ""
Write-Host "✅ COMPLETE!" -ForegroundColor Green
Write-Host ""
Start-Process explorer.exe -ArgumentList "$ROOT\uploaded"


