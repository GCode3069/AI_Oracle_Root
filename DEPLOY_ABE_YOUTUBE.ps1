# ═══════════════════════════════════════════════════════════════════════════
# ABRAHAM STUDIO - COMPLETE AUTO-DEPLOY TO YOUTUBE
# Downloads files, sets up everything, generates & uploads videos
# ═══════════════════════════════════════════════════════════════════════════

param([int]$Count = 10)

$ErrorActionPreference = "Continue"
$ROOT = "F:\AI_Oracle_Root\scarify\abraham_horror"

Write-Host ""
Write-Host "🔥 ABRAHAM ANIMATED STUDIO - AUTO YOUTUBE DEPLOY 🔥" -ForegroundColor Red
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host ""

# Create directories
Write-Host "📁 Creating directories..." -ForegroundColor Cyan
$dirs = @("audio", "videos", "uploaded", "temp")
foreach ($dir in $dirs) {
    $path = Join-Path $ROOT $dir
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
    }
}
Write-Host "✅ Directories ready" -ForegroundColor Green

# Install Python packages
Write-Host ""
Write-Host "📦 Installing packages..." -ForegroundColor Cyan
pip install --quiet --upgrade requests beautifulsoup4 lxml google-api-python-client google-auth-oauthlib google-auth-httplib2 2>&1 | Out-Null
Write-Host "✅ Packages installed" -ForegroundColor Green

# Check if abe_animated_youtube.py exists
$scriptFile = Join-Path $ROOT "abe_animated_youtube.py"
if (-not (Test-Path $scriptFile)) {
    Write-Host ""
    Write-Host "❌ abe_animated_youtube.py not found!" -ForegroundColor Red
    Write-Host "📥 Download it from Claude and put it here:" -ForegroundColor Yellow
    Write-Host "   $ROOT\abe_animated_youtube.py" -ForegroundColor White
    Write-Host ""
    exit 1
}

# Check YouTube credentials
$clientSecrets = Join-Path $ROOT "client_secrets.json"
if (-not (Test-Path $clientSecrets)) {
    Write-Host ""
    Write-Host "⚠️  YOUTUBE API NOT CONFIGURED" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📺 TO ENABLE AUTO-UPLOAD:" -ForegroundColor Cyan
    Write-Host "   1. Run: .\SETUP_YOUTUBE_API.ps1" -ForegroundColor White
    Write-Host "   2. Follow the 5-step setup" -ForegroundColor White
    Write-Host "   3. Download client_secrets.json" -ForegroundColor White
    Write-Host "   4. Run this script again" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 OR SKIP YOUTUBE:" -ForegroundColor Yellow
    Write-Host "   - Videos will save to 'uploaded' folder" -ForegroundColor White
    Write-Host "   - Manually upload them later" -ForegroundColor White
    Write-Host ""
    
    $continue = Read-Host "Continue without YouTube auto-upload? (Y/N)"
    if ($continue -ne "Y" -and $continue -ne "y") {
        Write-Host "❌ Cancelled" -ForegroundColor Red
        exit 0
    }
}

# Display configuration
Write-Host ""
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host "🎯 CONFIGURATION" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host "📂 Location: $ROOT" -ForegroundColor White
Write-Host "📊 Videos to generate: $Count" -ForegroundColor White
Write-Host "🎤 Voice: Deep male (Adam)" -ForegroundColor White
Write-Host "📺 Animation: Zoom effect (like Grok)" -ForegroundColor White

if (Test-Path $clientSecrets) {
    Write-Host "📤 YouTube: AUTO-UPLOAD ENABLED ✅" -ForegroundColor Green
} else {
    Write-Host "📤 YouTube: Manual upload (auto-upload not configured)" -ForegroundColor Yellow
}

Write-Host "=" * 70 -ForegroundColor Gray
Write-Host ""

# Confirm
$confirm = Read-Host "Generate $Count videos now? (Y/N)"
if ($confirm -ne "Y" -and $confirm -ne "y") {
    Write-Host "❌ Cancelled" -ForegroundColor Red
    exit 0
}

# Run generation
Write-Host ""
Write-Host "🚀 STARTING GENERATION..." -ForegroundColor Yellow
Write-Host ""

Set-Location $ROOT
python abe_animated_youtube.py $Count

# Check results
Write-Host ""
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host "📊 RESULTS" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Gray

$uploadedVideos = Get-ChildItem (Join-Path $ROOT "uploaded") -Filter "*.mp4" -ErrorAction SilentlyContinue
if ($uploadedVideos) {
    $totalSize = ($uploadedVideos | Measure-Object -Property Length -Sum).Sum / 1MB
    Write-Host "✅ Generated: $($uploadedVideos.Count) videos" -ForegroundColor Green
    Write-Host "💾 Total size: $([math]::Round($totalSize, 1)) MB" -ForegroundColor White
    Write-Host ""
    Write-Host "📁 Location: $ROOT\uploaded\" -ForegroundColor Cyan
    
    if (Test-Path $clientSecrets) {
        Write-Host "📺 Check uploads: https://studio.youtube.com/channel/UCS5pEpSCw8k4wene0iv0uAg/videos" -ForegroundColor Cyan
    }
} else {
    Write-Host "⚠️  No videos found - check errors above" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host ""

# Open folder
Start-Process explorer.exe -ArgumentList (Join-Path $ROOT "uploaded")
