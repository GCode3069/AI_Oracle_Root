# SCARIFY - LAPTOP 1 GENERATION SYSTEM
# Continuous video generation with sync

param([int]$TargetVideos = 500)

$ROOT = "F:\AI_Oracle_Root\scarify"
$ABRAHAM = "$ROOT\abraham_horror"

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Red
Write-Host "SCARIFY - LAPTOP 1 (GENERATION BEAST)" -ForegroundColor Red
Write-Host "=" * 70 -ForegroundColor Red
Write-Host ""
Write-Host "Target: $TargetVideos videos" -ForegroundColor Yellow
Write-Host "Output: $ABRAHAM\youtube_ready" -ForegroundColor Cyan
Write-Host ""

# Start generation
Write-Host "[1] Starting video generation..." -ForegroundColor Green
cd $ABRAHAM

Start-Process powershell -ArgumentList @"
-NoExit
-Command Write-Host 'GENERATION ACTIVE' -ForegroundColor Red; python 'ABRAHAM_PROFESSIONAL_UPGRADE.py' $TargetVideos
"@

Write-Host "[OK] Generation process started" -ForegroundColor Green
Write-Host ""

# Setup file sync (if shared drive available)
$sharedDrive = "\\LAPTOP2\SCARIFY_UPLOAD"
if (Test-Path $sharedDrive -ErrorAction SilentlyContinue) {
    Write-Host "[2] Starting sync to shared drive..." -ForegroundColor Green
    
    $syncScript = @"
while (`$true) {
    `$source = 'F:\AI_Oracle_Root\scarify\abraham_horror\youtube_ready'
    `$dest = '\\LAPTOP2\SCARIFY_UPLOAD'
    
    robocopy `$source `$dest *.mp4 *.json /MIR /R:3 /W:5 /LOG+:sync_log.txt
    
    Write-Host '[SYNC] Complete - '(Get-Date) -ForegroundColor Cyan
    Start-Sleep -Seconds 600  # Every 10 minutes
}
"@
    
    $syncScript | Out-File "$ROOT\sync_laptop1.ps1"
    Start-Process powershell -ArgumentList "-File $ROOT\sync_laptop1.ps1" -WindowStyle Minimized
    
    Write-Host "[OK] Sync process started" -ForegroundColor Green
} else {
    Write-Host "[SKIP] Shared drive not available - files saved locally" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Green
Write-Host "LAPTOP 1 OPERATIONAL" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Green
Write-Host ""
Write-Host "Generation running in background window" -ForegroundColor White
Write-Host "Videos saved to: $ABRAHAM\youtube_ready" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

# Monitor status
while ($true) {
    Clear-Host
    Write-Host "=" * 70 -ForegroundColor Red
    Write-Host "LAPTOP 1 - GENERATION STATUS" -ForegroundColor Red
    Write-Host "=" * 70 -ForegroundColor Red
    Write-Host ""
    
    $videoCount = (Get-ChildItem "$ABRAHAM\youtube_ready\*.mp4" -ErrorAction SilentlyContinue).Count
    $audioCount = (Get-ChildItem "$ABRAHAM\audio\*.mp3" -ErrorAction SilentlyContinue).Count
    
    Write-Host "Videos Generated: $videoCount / $TargetVideos" -ForegroundColor Green
    Write-Host "Audio Files: $audioCount" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Last Updated: $(Get-Date)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "=" * 70 -ForegroundColor Red
    
    if ($videoCount -ge $TargetVideos) {
        Write-Host ""
        Write-Host "TARGET REACHED!" -ForegroundColor Green
        Write-Host ""
        break
    }
    
    Start-Sleep -Seconds 30
}


