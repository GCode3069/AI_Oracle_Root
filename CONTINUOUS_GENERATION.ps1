# CONTINUOUS_GENERATION.ps1
# Generates videos continuously for 72 hours

param(
    [int]$VideosPerBatch = 5,
    [int]$MinutesBetweenBatches = 10,
    [int]$TotalHours = 72
)

Write-Host "`n================================================================" -ForegroundColor Green
Write-Host "  CONTINUOUS VIDEO GENERATION - 72 HOURS" -ForegroundColor Green
Write-Host "================================================================`n" -ForegroundColor Green

Write-Host "SETTINGS:" -ForegroundColor Yellow
Write-Host "  Videos per batch: $VideosPerBatch" -ForegroundColor White
Write-Host "  Wait between batches: $MinutesBetweenBatches minutes" -ForegroundColor White
Write-Host "  Total duration: $TotalHours hours" -ForegroundColor White
Write-Host "  Estimated total videos: $($VideosPerBatch * ($TotalHours * 60 / $MinutesBetweenBatches))`n" -ForegroundColor White

$confirmation = Read-Host "Start continuous generation? (yes/no)"

if ($confirmation -ne "yes") {
    Write-Host "`nAborted." -ForegroundColor Yellow
    exit
}

$startTime = Get-Date
$endTime = $startTime.AddHours($TotalHours)
$batchCount = 0
$totalVideos = 0

Write-Host "`nSTARTED: $($startTime.ToString())" -ForegroundColor Green
Write-Host "WILL END: $($endTime.ToString())`n" -ForegroundColor Green

while ((Get-Date) -lt $endTime) {
    $batchCount++
    $currentTime = Get-Date
    $elapsed = $currentTime - $startTime
    $remaining = $endTime - $currentTime
    
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host "  BATCH #$batchCount" -ForegroundColor Cyan
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host "  Time: $($currentTime.ToString('HH:mm:ss'))" -ForegroundColor White
    Write-Host "  Elapsed: $($elapsed.ToString('hh\:mm\:ss'))" -ForegroundColor White
    Write-Host "  Remaining: $($remaining.ToString('hh\:mm\:ss'))" -ForegroundColor White
    Write-Host "  Total videos so far: $totalVideos`n" -ForegroundColor White
    
    # Generate batch
    Write-Host "Generating $VideosPerBatch videos..." -ForegroundColor Yellow
    python abraham_MAX_HEADROOM_ENHANCED.py $VideosPerBatch
    
    $totalVideos += $VideosPerBatch
    
    Write-Host "`nBatch #$batchCount complete. Total: $totalVideos videos`n" -ForegroundColor Green
    
    # Check if we should continue
    if ((Get-Date).AddMinutes($MinutesBetweenBatches) -ge $endTime) {
        Write-Host "Next batch would exceed time limit. Stopping.`n" -ForegroundColor Yellow
        break
    }
    
    # Wait
    Write-Host "Waiting $MinutesBetweenBatches minutes until next batch...`n" -ForegroundColor Gray
    Start-Sleep -Seconds ($MinutesBetweenBatches * 60)
}

$finalTime = Get-Date
$totalElapsed = $finalTime - $startTime

Write-Host "`n================================================================" -ForegroundColor Green
Write-Host "  CONTINUOUS GENERATION COMPLETE" -ForegroundColor Green
Write-Host "================================================================`n" -ForegroundColor Green

Write-Host "RESULTS:" -ForegroundColor Yellow
Write-Host "  Total batches: $batchCount" -ForegroundColor White
Write-Host "  Total videos: $totalVideos" -ForegroundColor White
Write-Host "  Duration: $($totalElapsed.ToString('hh\:mm\:ss'))" -ForegroundColor White
Write-Host "  Average: $([math]::Round($totalVideos / $totalElapsed.TotalHours, 1)) videos/hour`n" -ForegroundColor White

Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host "  1. Review uploads: python VIDEO_REVIEW_TRACKER.py --list" -ForegroundColor Cyan
Write-Host "  2. Check YouTube Studio: https://studio.youtube.com" -ForegroundColor Cyan
Write-Host "  3. Cross-post to other platforms" -ForegroundColor Cyan
Write-Host "  4. Monitor analytics and revenue`n" -ForegroundColor Cyan

Write-Host "================================================================`n" -ForegroundColor Green


