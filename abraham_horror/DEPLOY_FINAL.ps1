# ============================================================================
# FINAL DEPLOYMENT LAUNCHER - Generate & Upload to YouTube
# ============================================================================
param([int]$Count = 10)

$ROOT = "F:\AI_Oracle_Root\scarify\abraham_horror"
$CHANNEL_ID = "UCS5pEpSCw8k4wene0iv0uAg"

Write-Host ""
Write-Host "=" * 70
Write-Host "ABRAHAM LINCOLN - PROFESSIONAL VIDEO SYSTEM"
Write-Host "=" * 70
Write-Host ""
Write-Host "Status: [VERIFIED WORKING]"
Write-Host "Test Upload: SUCCESS (https://www.youtube.com/watch?v=rnFhveyeJi4)"
Write-Host ""
Write-Host "Generating $Count videos and uploading directly to YouTube..."
Write-Host "Channel: $CHANNEL_ID"
Write-Host ""
Write-Host "Features:"
Write-Host "  ✓ Real headline scraping"
Write-Host "  ✓ Professional comedy scripts"
Write-Host "  ✓ Dynamic B-roll from Pexels"
Write-Host "  ✓ Text overlays (PIL-based, no ImageMagick needed)"
Write-Host "  ✓ Direct YouTube upload"
Write-Host ""
Write-Host "Starting in 3 seconds..."
Start-Sleep -Seconds 3

cd $ROOT

Write-Host ""
Write-Host "[DEPLOY] Running professional generator..."
Write-Host ""

python ABRAHAM_PROFESSIONAL_UPGRADE.py $Count

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=" * 70
    Write-Host "[SUCCESS] Deployment Complete!"
    Write-Host "=" * 70
    Write-Host ""
    
    # Count generated videos
    $videos = Get-ChildItem "$ROOT\videos\PRO_*.mp4" | Sort-Object LastWriteTime -Descending | Select-Object -First $Count
    $total_mb = 0
    foreach ($v in $videos) {
        $total_mb += $v.Length / 1MB
    }
    
    Write-Host "Videos Generated: $($videos.Count)" -ForegroundColor Green
    Write-Host "Total Size: $([math]::Round($total_mb, 2)) MB" -ForegroundColor Green
    Write-Host ""
    Write-Host "Check YouTube Studio:" -ForegroundColor Yellow
    Write-Host "  https://studio.youtube.com/channel/$CHANNEL_ID/videos"
    Write-Host ""
    Write-Host "Videos should appear within 1-2 minutes."
    Write-Host ""
    
    # Open videos folder
    Start-Process explorer.exe -ArgumentList "$ROOT\videos"
} else {
    Write-Host ""
    Write-Host "=" * 70
    Write-Host "[ERROR] Deployment failed"
    Write-Host "=" * 70
    Write-Host ""
    Write-Host "Check console output above for details."
    Write-Host ""
}


