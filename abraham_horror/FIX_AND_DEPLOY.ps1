# ═══════════════════════════════════════════════════════════════════════════
# FIX & DEPLOY - Abraham Lincoln Comedy to YouTube
# Fixes: Upload to correct channel, ensure videos appear, test system
# ═══════════════════════════════════════════════════════════════════════════

param([int]$Count = 5)

$ROOT = "F:\AI_Oracle_Root\scarify\abraham_horror"
$YOUTUBE_CHANNEL = "UCS5pEpSCw8k4wene0iv0uAg"

Write-Host ""
Write-Host "🔧 FIXING & DEPLOYING COMEDY SYSTEM" -ForegroundColor Cyan
Write-Host ("=" * 70) -ForegroundColor Gray
Write-Host ""
Write-Host "Target Channel: $YOUTUBE_CHANNEL" -ForegroundColor Yellow
Write-Host "Studio URL: https://studio.youtube.com/channel/$YOUTUBE_CHANNEL/videos" -ForegroundColor Gray
Write-Host ""

# Test first
Write-Host "[STEP 1] Running system tests..." -ForegroundColor Yellow
cd $ROOT
python TEST_COMEDY_UPLOAD.py

Write-Host ""
Write-Host "[STEP 2] Generating $Count videos + uploading..." -ForegroundColor Yellow
Write-Host ""

# Generate and upload
python ABRAHAM_COMEDY_YOUTUBE_COMPLETE.py $Count

Write-Host ""
Write-Host "[STEP 3] Checking results..." -ForegroundColor Yellow
Write-Host ""

# Show generated videos
$videos = Get-ChildItem "$ROOT\videos\ABE_COMEDY_*.mp4" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First $Count

if ($videos) {
    Write-Host "✅ Generated Videos:" -ForegroundColor Green
    foreach ($vid in $videos) {
        $mb = [math]::Round($vid.Length / 1MB, 2)
        Write-Host "   📹 $($vid.Name) ($mb MB)" -ForegroundColor White
    }
} else {
    Write-Host "⚠️  No videos found in videos folder" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📊 UPLOAD STATUS:" -ForegroundColor Cyan
Write-Host "   Check YouTube Studio: https://studio.youtube.com/channel/$YOUTUBE_CHANNEL/videos" -ForegroundColor White
Write-Host "   Look in BOTH 'Shorts' tab AND 'Videos' tab" -ForegroundColor Yellow
Write-Host ""

Write-Host "🎯 WHY VIDEOS MIGHT NOT APPEAR:" -ForegroundColor Yellow
Write-Host "   1. Upload still processing (wait 1-2 minutes)" -ForegroundColor Gray
Write-Host "   2. Check 'Videos' tab, not just 'Shorts'" -ForegroundColor Gray
Write-Host "   3. Filter by date (newest first)" -ForegroundColor Gray
Write-Host "   4. YouTube API quota might be exceeded" -ForegroundColor Gray
Write-Host "   5. Need to refresh browser page" -ForegroundColor Gray
Write-Host ""

Write-Host "🔗 DIRECT LINKS:" -ForegroundColor Cyan
Write-Host "   All Videos:    https://studio.youtube.com/channel/$YOUTUBE_CHANNEL/videos" -ForegroundColor White
Write-Host "   Shorts Only:   https://studio.youtube.com/channel/$YOUTUBE_CHANNEL/videos/short" -ForegroundColor White
Write-Host "   Upload Page:   https://studio.youtube.com/channel/$YOUTUBE_CHANNEL/videos/upload" -ForegroundColor White
Write-Host ""

# Open videos folder
Start-Process explorer.exe -ArgumentList "$ROOT\videos"

Write-Host "✅ DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host ""


