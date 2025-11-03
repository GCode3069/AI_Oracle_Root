# DEPLOY NOW - Abraham Lincoln Comedy to YouTube
# Quick deployment script with status reporting

param([int]$Count = 5)

$ROOT = "F:\AI_Oracle_Root\scarify\abraham_horror"
$CHANNEL_ID = "UCS5pEpSCw8k4wene0iv0uAg"

Write-Host ""
Write-Host "=" * 70
Write-Host "DEPLOYING ABRAHAM LINCOLN COMEDY TO YOUTUBE"
Write-Host "=" * 70
Write-Host ""
Write-Host "Channel: $CHANNEL_ID"
Write-Host "Count: $Count videos"
Write-Host ""

cd $ROOT

Write-Host "[1/3] Testing system..."
python TEST_COMEDY_UPLOAD.py

Write-Host ""
Write-Host "[2/3] Generating and uploading $Count videos..."
Write-Host ""

python ABRAHAM_COMEDY_YOUTUBE_COMPLETE.py $Count

Write-Host ""
Write-Host "[3/3] Results Summary"
Write-Host ""

$videos = Get-ChildItem "$ROOT\videos\ABE_COMEDY_*.mp4" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First $Count

Write-Host "Generated Videos:" -ForegroundColor Cyan
if ($videos) {
    foreach ($vid in $videos) {
        $mb = [math]::Round($vid.Length / 1MB, 2)
        Write-Host "  $($vid.Name) ($mb MB)" -ForegroundColor White
    }
} else {
    Write-Host "  No videos found" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "YOUTUBE STUDIO LINKS:" -ForegroundColor Cyan
Write-Host "  All Videos: https://studio.youtube.com/channel/$CHANNEL_ID/videos" -ForegroundColor White
Write-Host "  Shorts: https://studio.youtube.com/channel/$CHANNEL_ID/videos/short" -ForegroundColor White
Write-Host "  Upload: https://studio.youtube.com/channel/$CHANNEL_ID/videos/upload" -ForegroundColor White
Write-Host ""
Write-Host "IMPORTANT:" -ForegroundColor Yellow
Write-Host "  - Check BOTH 'Videos' tab AND 'Shorts' tab" -ForegroundColor White
Write-Host "  - Refresh browser (Ctrl+F5) if videos don't appear" -ForegroundColor White
Write-Host "  - Wait 1-2 minutes for YouTube processing" -ForegroundColor White
Write-Host ""
Write-Host "Ready!" -ForegroundColor Green


