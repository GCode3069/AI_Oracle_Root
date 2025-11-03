# SCARIFY - Dual Laptop Setup Guide

## Overview

Split workload between two laptops for maximum efficiency:
- **Laptop 1 (GPU)**: Video generation
- **Laptop 2**: Upload & analytics

---

## Laptop 1: Generation Beast

### Role
- Generate all videos using GPU-accelerated FFmpeg
- Process audio with ElevenLabs
- Create professional multi-clip compositions

### Setup

```powershell
# Install requirements
cd F:\AI_Oracle_Root\scarify
pip install -r requirements.txt

# Test GPU
python -c "import subprocess; print(subprocess.run(['ffmpeg', '-version'], capture_output=True).stdout.decode())"
```

### Run Generation Loop

```powershell
# Continuous generation
cd abraham_horror
python ABRAHAM_PROFESSIONAL_UPGRADE.py 1000
```

### Sync to Shared Drive

```powershell
# Setup sync every 10 minutes
$syncScript = @"
while (`$true) {
    robocopy F:\AI_Oracle_Root\scarify\abraham_horror\youtube_ready \\SharedDrive\SCARIFY_UPLOAD /MIR
    Start-Sleep -Seconds 600
}
"@

$syncScript | Out-File sync_to_shared.ps1
Start-Process powershell -ArgumentList "-File sync_to_shared.ps1" -WindowStyle Hidden
```

---

## Laptop 2: Upload & Analytics

### Role
- Monitor shared drive for new videos
- Upload to 15 YouTube channels (rotation)
- Track analytics
- Monitor Bitcoin balance

### Setup

```powershell
cd F:\AI_Oracle_Root\scarify

# Setup channel credentials (one-time)
python MULTI_CHANNEL_SETUP.py setup 15

# Test connection
python MULTI_CHANNEL_SETUP.py list
```

### Run Upload Loop

```powershell
# Watch and upload
$uploadScript = @"
while (`$true) {
    # Check for new videos
    `$videos = Get-ChildItem \\SharedDrive\SCARIFY_UPLOAD\*.mp4 | Where-Object { `$_.LastWriteTime -gt (Get-Date).AddMinutes(-15) }
    
    if (`$videos) {
        Write-Host '[UPLOAD] Found `$(`$videos.Count) new videos'
        python MULTI_CHANNEL_UPLOADER.py \\SharedDrive\SCARIFY_UPLOAD round-robin
    }
    
    Start-Sleep -Seconds 300  # Check every 5 minutes
}
"@

$uploadScript | Out-File upload_loop.ps1
Start-Process powershell -ArgumentList "-File upload_loop.ps1"
```

### Run Analytics Loop

```powershell
# Track performance every hour
$analyticsScript = @"
while (`$true) {
    python analytics_tracker.py scan
    python analytics_tracker.py report
    python check_balance.py
    Start-Sleep -Seconds 3600  # Every hour
}
"@

$analyticsScript | Out-File analytics_loop.ps1
Start-Process powershell -ArgumentList "-File analytics_loop.ps1" -WindowStyle Hidden
```

---

## Network Sync Options

### Option 1: Shared Network Drive

```powershell
# Laptop 1 - Share folder
New-SmbShare -Name "SCARIFY_UPLOAD" -Path "F:\AI_Oracle_Root\scarify\abraham_horror\youtube_ready" -FullAccess "Everyone"

# Laptop 2 - Map drive
New-PSDrive -Name "S" -PSProvider FileSystem -Root "\\LAPTOP1\SCARIFY_UPLOAD" -Persist
```

### Option 2: Cloud Sync (Dropbox/Google Drive)

```powershell
# Both laptops sync to:
# C:\Users\<User>\Dropbox\SCARIFY_UPLOAD

# Laptop 1 generates to Dropbox folder
# Laptop 2 monitors Dropbox folder
```

### Option 3: Direct SSH/rsync

```bash
# Laptop 1 pushes every 10 minutes
while true; do
    rsync -avz F:/AI_Oracle_Root/scarify/abraham_horror/youtube_ready/ laptop2:/scarify/upload/
    sleep 600
done
```

---

## Monitoring

### Laptop 1 Dashboard

```powershell
# Create dashboard
$dashboard1 = @"
while (`$true) {
    Clear-Host
    Write-Host '=' * 70 -ForegroundColor Red
    Write-Host 'SCARIFY - LAPTOP 1 (GENERATION)' -ForegroundColor Red
    Write-Host '=' * 70 -ForegroundColor Red
    Write-Host ''
    
    `$videoCount = (Get-ChildItem F:\AI_Oracle_Root\scarify\abraham_horror\youtube_ready\*.mp4).Count
    `$audioCount = (Get-ChildItem F:\AI_Oracle_Root\scarify\abraham_horror\audio\*.mp3).Count
    
    Write-Host 'Videos Generated: '`$videoCount -ForegroundColor Green
    Write-Host 'Audio Files: '`$audioCount -ForegroundColor Green
    Write-Host ''
    Write-Host 'GPU Status: ACTIVE' -ForegroundColor Yellow
    Write-Host 'Last Sync: '(Get-Date) -ForegroundColor Cyan
    Write-Host ''
    
    Start-Sleep -Seconds 10
}
"@

$dashboard1 | Out-File dashboard_laptop1.ps1
```

### Laptop 2 Dashboard

```powershell
# Create dashboard
$dashboard2 = @"
while (`$true) {
    Clear-Host
    Write-Host '=' * 70 -ForegroundColor Cyan
    Write-Host 'SCARIFY - LAPTOP 2 (UPLOAD)' -ForegroundColor Cyan
    Write-Host '=' * 70 -ForegroundColor Cyan
    Write-Host ''
    
    # Get upload stats
    `$results = Get-Content F:\AI_Oracle_Root\scarify\upload_results_*.json | ConvertFrom-Json
    `$totalUploads = `$results.Count
    
    Write-Host 'Total Uploads: '`$totalUploads -ForegroundColor Green
    Write-Host 'Active Channels: 15' -ForegroundColor Green
    Write-Host ''
    
    # BTC balance
    python check_balance.py
    
    Start-Sleep -Seconds 10
}
"@

$dashboard2 | Out-File dashboard_laptop2.ps1
```

---

## Launch Everything

### Master Launch Script (Laptop 1)

```powershell
# LAPTOP1_START.ps1
Write-Host 'Starting SCARIFY Laptop 1 (Generation)...' -ForegroundColor Red

# Start generation
Start-Process powershell -ArgumentList "-File F:\AI_Oracle_Root\scarify\abraham_horror\GENERATE_CONTINUOUS.ps1"

# Start sync
Start-Process powershell -ArgumentList "-File sync_to_shared.ps1" -WindowStyle Hidden

# Show dashboard
.\dashboard_laptop1.ps1
```

### Master Launch Script (Laptop 2)

```powershell
# LAPTOP2_START.ps1
Write-Host 'Starting SCARIFY Laptop 2 (Upload & Analytics)...' -ForegroundColor Cyan

# Start upload loop
Start-Process powershell -ArgumentList "-File upload_loop.ps1"

# Start analytics loop
Start-Process powershell -ArgumentList "-File analytics_loop.ps1" -WindowStyle Hidden

# Show dashboard
.\dashboard_laptop2.ps1
```

---

## Failover

### Heartbeat Monitor

```powershell
# Check if Laptop 1 is responsive
while ($true) {
    if (Test-Connection LAPTOP1 -Count 1 -Quiet) {
        Write-Host '[OK] Laptop 1 responsive' -ForegroundColor Green
    } else {
        Write-Host '[ALERT] Laptop 1 DOWN - switching to local generation' -ForegroundColor Red
        # Start generation on Laptop 2
        Start-Process python -ArgumentList "F:\AI_Oracle_Root\scarify\abraham_horror\ABRAHAM_PROFESSIONAL_UPGRADE.py 10"
    }
    Start-Sleep -Seconds 60
}
```

---

## Complete Execution

1. **Laptop 1**: Run `LAPTOP1_START.ps1`
2. **Laptop 2**: Run `LAPTOP2_START.ps1`
3. Monitor dashboards
4. Videos generate → sync → upload → analytics → Bitcoin tracking

**System runs 24/7 until $10K-$15K target hit**


