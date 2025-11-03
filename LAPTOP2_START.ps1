# SCARIFY - LAPTOP 2 UPLOAD & ANALYTICS SYSTEM
# Monitors for new videos and uploads across 15 channels

$ROOT = "F:\AI_Oracle_Root\scarify"
$WATCH_DIR = "$ROOT\abraham_horror\youtube_ready"  # Change to shared drive if using network sync

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "SCARIFY - LAPTOP 2 (UPLOAD & ANALYTICS)" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Check channels configured
Write-Host "[1] Checking YouTube channels..." -ForegroundColor Green
cd $ROOT

$channelsFile = "$ROOT\channels\channels_master.json"
if (Test-Path $channelsFile) {
    $channelData = Get-Content $channelsFile | ConvertFrom-Json
    $channelCount = $channelData.channels.Count
    Write-Host "[OK] $channelCount channels configured" -ForegroundColor Green
} else {
    Write-Host "[WARNING] No channels configured!" -ForegroundColor Yellow
    Write-Host "Run: python MULTI_CHANNEL_SETUP.py setup 15" -ForegroundColor Yellow
    $setup = Read-Host "Setup channels now? (y/n)"
    if ($setup -eq 'y') {
        python MULTI_CHANNEL_SETUP.py setup 15
    }
}

Write-Host ""

# Start upload loop
Write-Host "[2] Starting upload monitor..." -ForegroundColor Green

$uploadScript = @"
`$ROOT = '$ROOT'
`$WATCH_DIR = '$WATCH_DIR'

while (`$true) {
    Write-Host ''
    Write-Host '[UPLOAD] Checking for new videos...' -ForegroundColor Cyan
    Write-Host '[WATCH] '`$WATCH_DIR -ForegroundColor Gray
    
    `$newVideos = Get-ChildItem `$WATCH_DIR\*.mp4 -ErrorAction SilentlyContinue | 
                 Where-Object { `$_.LastWriteTime -gt (Get-Date).AddMinutes(-30) }
    
    if (`$newVideos) {
        Write-Host '[FOUND] '`$newVideos.Count' new videos' -ForegroundColor Yellow
        
        cd `$ROOT
        python MULTI_CHANNEL_UPLOADER.py `$WATCH_DIR round-robin
        
        Write-Host '[OK] Upload batch complete' -ForegroundColor Green
    } else {
        Write-Host '[IDLE] No new videos' -ForegroundColor Gray
    }
    
    Start-Sleep -Seconds 300  # Check every 5 minutes
}
"@

$uploadScript | Out-File "$ROOT\upload_monitor.ps1"
Start-Process powershell -ArgumentList "-NoExit -File $ROOT\upload_monitor.ps1" -WindowStyle Normal

Write-Host "[OK] Upload monitor started" -ForegroundColor Green
Write-Host ""

# Start analytics loop
Write-Host "[3] Starting analytics tracker..." -ForegroundColor Green

$analyticsScript = @"
`$ROOT = '$ROOT'
cd `$ROOT

while (`$true) {
    Write-Host ''
    Write-Host '=' * 70 -ForegroundColor Magenta
    Write-Host 'ANALYTICS UPDATE' -ForegroundColor Magenta
    Write-Host '=' * 70 -ForegroundColor Magenta
    
    python analytics_tracker.py scan
    python analytics_tracker.py report
    
    Write-Host ''
    Write-Host 'BTC BALANCE CHECK' -ForegroundColor Yellow
    python check_balance.py
    
    Write-Host ''
    Write-Host 'Next update in 1 hour...' -ForegroundColor Gray
    Start-Sleep -Seconds 3600  # Every hour
}
"@

$analyticsScript | Out-File "$ROOT\analytics_monitor.ps1"
Start-Process powershell -ArgumentList "-NoExit -File $ROOT\analytics_monitor.ps1" -WindowStyle Minimized

Write-Host "[OK] Analytics tracker started" -ForegroundColor Green
Write-Host ""

Write-Host "=" * 70 -ForegroundColor Green
Write-Host "LAPTOP 2 OPERATIONAL" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Green
Write-Host ""
Write-Host "Upload monitor: Running (visible window)" -ForegroundColor White
Write-Host "Analytics tracker: Running (minimized)" -ForegroundColor White
Write-Host ""
Write-Host "All processes active. Monitoring revenue target..." -ForegroundColor Cyan
Write-Host ""

# Dashboard
while ($true) {
    Clear-Host
    Write-Host "=" * 70 -ForegroundColor Cyan
    Write-Host "LAPTOP 2 - UPLOAD & ANALYTICS DASHBOARD" -ForegroundColor Cyan
    Write-Host "=" * 70 -ForegroundColor Cyan
    Write-Host ""
    
    # Upload stats
    $resultFiles = Get-ChildItem "$ROOT\upload_results_*.json" -ErrorAction SilentlyContinue
    if ($resultFiles) {
        $totalUploads = 0
        foreach ($file in $resultFiles) {
            $data = Get-Content $file | ConvertFrom-Json
            $totalUploads += $data.Count
        }
        Write-Host "Total Uploads: $totalUploads" -ForegroundColor Green
    } else {
        Write-Host "Total Uploads: 0" -ForegroundColor Yellow
    }
    
    Write-Host "Active Channels: $channelCount" -ForegroundColor Green
    Write-Host ""
    
    # BTC status
    Write-Host "Bitcoin: bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt" -ForegroundColor Yellow
    Write-Host "Target: `$10,000 - `$15,000" -ForegroundColor Yellow
    Write-Host ""
    
    Write-Host "Last Updated: $(Get-Date)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "=" * 70 -ForegroundColor Cyan
    
    Start-Sleep -Seconds 60
}


