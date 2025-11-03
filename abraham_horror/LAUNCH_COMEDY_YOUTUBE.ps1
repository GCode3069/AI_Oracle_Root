# ═══════════════════════════════════════════════════════════════════════════
# ABRAHAM LINCOLN COMEDY - YOUTUBE AUTO-UPLOAD
# ✅ Abe visible on TV screen ✅ Male voice ✅ Comedy styles ✅ Auto-upload
# ═══════════════════════════════════════════════════════════════════════════

param([int]$Count = 10)

$ROOT = "F:\AI_Oracle_Root\scarify\abraham_horror"

Write-Host ""
Write-Host "🔥 ABRAHAM LINCOLN COMEDY - YOUTUBE AUTO-UPLOAD" -ForegroundColor Red
Write-Host ("=" * 70) -ForegroundColor Gray
Write-Host ""
Write-Host "✅ Abe visible speaking from TV screen" -ForegroundColor Green
Write-Host "✅ Proper MALE voice (Chappelle, Carlin, Pryor style)" -ForegroundColor Green
Write-Host "✅ Dark satirical takes on current events" -ForegroundColor Green
Write-Host "✅ Auto-uploads to YouTube" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install --quiet requests beautifulsoup4 lxml PyYAML Pillow moviepy google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client 2>&1 | Out-Null

# Ensure directories
$dirs = @("audio", "videos", "temp", "images", "uploads")
foreach ($dir in $dirs) {
    $path = Join-Path $ROOT $dir
    if (-not (Test-Path $path)) { 
        New-Item -ItemType Directory -Path $path -Force | Out-Null
    }
}

# Check for Lincoln image
$lincolnImg = Join-Path $ROOT "images\lincoln_portrait.jpg"
if (-not (Test-Path $lincolnImg)) {
    Write-Host "⚠️  Note: Add Lincoln portrait for best visual results" -ForegroundColor Yellow
    Write-Host "   Location: $lincolnImg" -ForegroundColor Gray
    Write-Host "   Placeholder will be used if missing" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "🚀 GENERATING $Count COMEDY VIDEOS + AUTO-UPLOAD..." -ForegroundColor Yellow
Write-Host ""

Set-Location $ROOT
python ABRAHAM_COMEDY_YOUTUBE_COMPLETE.py $Count

Write-Host ""
Write-Host "✅ COMPLETE!" -ForegroundColor Green
Write-Host ""
Start-Process explorer.exe -ArgumentList "$ROOT\videos"


