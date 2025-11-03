# ============================================================================
# TEST UPLOAD - Generate 1 video and upload directly to YouTube
# ============================================================================

$ROOT = "F:\AI_Oracle_Root\scarify\abraham_horror"

Write-Host ""
Write-Host "=" * 70
Write-Host "TEST UPLOAD - Generating 1 video and uploading to YouTube"
Write-Host "=" * 70
Write-Host ""
Write-Host "Channel: UCS5pEpSCw8k4wene0iv0uAg"
Write-Host "This will:"
Write-Host "  1. Scrape a real headline"
Write-Host "  2. Generate comedy script"
Write-Host "  3. Generate audio with Lincoln voice"
Write-Host "  4. Create professional video with B-roll"
Write-Host "  5. Upload directly to YouTube"
Write-Host ""
Write-Host "Starting in 3 seconds..."
Start-Sleep -Seconds 3

cd $ROOT

Write-Host ""
Write-Host "[TEST] Running professional generator..."
Write-Host ""

python ABRAHAM_PROFESSIONAL_UPGRADE.py 1

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=" * 70
    Write-Host "[SUCCESS] Test complete!"
    Write-Host "=" * 70
    Write-Host ""
    Write-Host "Check YouTube Studio:"
    Write-Host "  https://studio.youtube.com/channel/UCS5pEpSCw8k4wene0iv0uAg/videos" -ForegroundColor Yellow
    Write-Host ""
    
    # Show latest video file
    $latest = Get-ChildItem "$ROOT\videos\PRO_*.mp4" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($latest) {
        $mb = [math]::Round($latest.Length / 1MB, 2)
        Write-Host "Latest video: $($latest.Name) ($mb MB)" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "Video should appear in your YouTube Studio within 1-2 minutes."
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "=" * 70
    Write-Host "[ERROR] Test failed - check output above"
    Write-Host "=" * 70
    Write-Host ""
}


