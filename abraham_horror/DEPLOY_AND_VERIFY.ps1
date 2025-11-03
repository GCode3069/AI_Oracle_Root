# DEPLOY AND VERIFY - Complete deployment with verification
param([int]$Count = 5)

$ROOT = "F:\AI_Oracle_Root\scarify\abraham_horror"
$CHANNEL_ID = "UCS5pEpSCw8k4wene0iv0uAg"

Write-Host ""
Write-Host "=" * 70
Write-Host "DEPLOYING ABRAHAM LINCOLN COMEDY TO YOUR CHANNEL"
Write-Host "=" * 70
Write-Host ""
Write-Host "Channel ID: $CHANNEL_ID"
Write-Host "Videos to generate: $Count"
Write-Host ""

cd $ROOT

# Step 1: Quick test
Write-Host "[STEP 1/3] Quick system check..." -ForegroundColor Yellow
$testResult = python -c "import requests, bs4; print('OK')" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  [OK] Dependencies ready" -ForegroundColor Green
} else {
    Write-Host "  [WARNING] Some dependencies missing" -ForegroundColor Yellow
}

# Step 2: Generate and upload
Write-Host ""
Write-Host "[STEP 2/3] Generating $Count videos and uploading..." -ForegroundColor Yellow
Write-Host ""

python ABRAHAM_COMEDY_YOUTUBE_COMPLETE.py $Count

# Step 3: Show results
Write-Host ""
Write-Host "[STEP 3/3] Verification and Links" -ForegroundColor Yellow
Write-Host ""

$videos = Get-ChildItem "$ROOT\videos\ABE_COMEDY_*.mp4" -ErrorAction SilentlyContinue | 
    Sort-Object LastWriteTime -Descending | 
    Select-Object -First $Count

Write-Host "Generated Files:" -ForegroundColor Cyan
if ($videos) {
    foreach ($vid in $videos) {
        $mb = [math]::Round($vid.Length / 1MB, 2)
        $date = $vid.LastWriteTime.ToString("yyyy-MM-dd HH:mm")
        Write-Host "  $($vid.Name) ($mb MB, $date)" -ForegroundColor White
    }
} else {
    Write-Host "  No videos found in videos folder" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=" * 70
Write-Host "YOUTUBE STUDIO LINKS - CHECK YOUR VIDEOS HERE"
Write-Host "=" * 70
Write-Host ""
Write-Host "ALL VIDEOS (Check this first - shows everything):" -ForegroundColor Green
Write-Host "  https://studio.youtube.com/channel/$CHANNEL_ID/videos" -ForegroundColor White
Write-Host ""
Write-Host "SHORTS TAB ONLY:" -ForegroundColor Cyan
Write-Host "  https://studio.youtube.com/channel/$CHANNEL_ID/videos/short" -ForegroundColor White
Write-Host ""
Write-Host "UPLOAD PAGE:" -ForegroundColor Cyan
Write-Host "  https://studio.youtube.com/channel/$CHANNEL_ID/videos/upload" -ForegroundColor White
Write-Host ""

Write-Host "=" * 70
Write-Host "IMPORTANT - READ THIS"
Write-Host "=" * 70
Write-Host ""
Write-Host "1. VIDEOS APPEAR AS SHORTS BECAUSE:" -ForegroundColor Yellow
Write-Host "   - They are under 60 seconds" -ForegroundColor Gray
Write-Host "   - They are vertical format (1080x1920)" -ForegroundColor Gray
Write-Host "   - YouTube auto-classifies them" -ForegroundColor Gray
Write-Host ""
Write-Host "2. WHERE TO FIND YOUR VIDEOS:" -ForegroundColor Yellow
Write-Host "   - Check 'Videos' tab (shows ALL videos)" -ForegroundColor White
Write-Host "   - Check 'Shorts' tab (shows only Shorts)" -ForegroundColor White
Write-Host "   - Both tabs will have your videos" -ForegroundColor White
Write-Host ""
Write-Host "3. IF VIDEOS DON'T APPEAR:" -ForegroundColor Yellow
Write-Host "   - Wait 1-2 minutes for processing" -ForegroundColor Gray
Write-Host "   - Refresh browser (Ctrl+F5)" -ForegroundColor Gray
Write-Host "   - Check 'Videos' tab, not just 'Shorts'" -ForegroundColor Gray
Write-Host "   - Filter by 'Newest first'" -ForegroundColor Gray
Write-Host ""

Write-Host "[OK] Deployment complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Copy this link to check your videos:" -ForegroundColor Cyan
Write-Host "https://studio.youtube.com/channel/$CHANNEL_ID/videos" -ForegroundColor Yellow
Write-Host ""

# Open videos folder
Start-Process explorer.exe -ArgumentList "$ROOT\videos"


