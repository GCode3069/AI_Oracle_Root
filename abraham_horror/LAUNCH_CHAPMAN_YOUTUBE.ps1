# ═══════════════════════════════════════════════════════════════════════════
# CHAPMAN 2025 YOUTUBE AUTO-UPLOAD LAUNCHER
# Generates fear-targeted videos and auto-uploads to YouTube
# ═══════════════════════════════════════════════════════════════════════════

param([int]$Count = 5)

$ROOT = "F:\AI_Oracle_Root\scarify\abraham_horror"

Write-Host ""
Write-Host "🔥 CHAPMAN 2025 - YOUTUBE AUTO-UPLOAD" -ForegroundColor Red
Write-Host ("=" * 70) -ForegroundColor Gray
Write-Host ""
Write-Host "✅ Targets top fears (69%, 59%, 58%, 55%, 52%)" -ForegroundColor Green
Write-Host "✅ Uses your image generation API" -ForegroundColor Green
Write-Host "✅ Auto-uploads to YouTube channel" -ForegroundColor Green
Write-Host "✅ 15s Shorts optimized for viral" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install --quiet requests beautifulsoup4 PyYAML Pillow moviepy google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client 2>&1 | Out-Null

# Check image API config
Write-Host ""
Write-Host "⚠️  IMPORTANT: Configure your image API in CHAPMAN_2025_YOUTUBE_AUTO.py" -ForegroundColor Yellow
Write-Host "   - IMAGE_API_URL: Your API endpoint" -ForegroundColor Gray
Write-Host "   - IMAGE_API_KEY: Your API key" -ForegroundColor Gray
Write-Host ""

# Ensure directories
$dirs = @("audio", "videos", "temp", "images")
foreach ($dir in $dirs) {
    $path = Join-Path $ROOT $dir
    if (-not (Test-Path $path)) { 
        New-Item -ItemType Directory -Path $path -Force | Out-Null
    }
}

Write-Host "🚀 GENERATING $Count VIDEOS + AUTO-UPLOAD..." -ForegroundColor Yellow
Write-Host ""

Set-Location $ROOT
python CHAPMAN_2025_YOUTUBE_AUTO.py $Count

Write-Host ""
Write-Host "✅ COMPLETE!" -ForegroundColor Green
Write-Host ""
Start-Process explorer.exe -ArgumentList "$ROOT\videos"


