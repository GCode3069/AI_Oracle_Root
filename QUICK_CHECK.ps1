# SCARIFY EMPIRE - Quick Status Check
# Run this anytime to see progress

$Host.UI.RawUI.WindowTitle = "SCARIFY - Empire Status"
Clear-Host

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "           SCARIFY EMPIRE - STATUS CHECK" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host "Timestamp: $timestamp" -ForegroundColor Gray
Write-Host ""

# Video Generation Status
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "VIDEO GENERATION:" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Cyan

$videoPath = "F:\AI_Oracle_Root\scarify\abraham_horror\youtube_ready"
if (Test-Path $videoPath) {
    $videoCount = (Get-ChildItem "$videoPath\*.mp4" -ErrorAction SilentlyContinue).Count
    Write-Host "Videos Generated: $videoCount" -ForegroundColor Green
    
    if ($videoCount -gt 0) {
        $latestVideo = Get-ChildItem "$videoPath\*.mp4" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
        Write-Host "Latest: $($latestVideo.Name)" -ForegroundColor Gray
        Write-Host "Time: $($latestVideo.LastWriteTime)" -ForegroundColor Gray
    }
} else {
    Write-Host "Video path not found" -ForegroundColor Red
}
Write-Host ""

# Upload Status
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "YOUTUBE UPLOADS:" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Cyan

$uploadResults = Get-ChildItem "F:\AI_Oracle_Root\scarify\upload_results_*.json" -ErrorAction SilentlyContinue
if ($uploadResults) {
    Write-Host "Upload batches: $($uploadResults.Count)" -ForegroundColor Green
    $latestUpload = $uploadResults | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    Write-Host "Latest: $($latestUpload.Name)" -ForegroundColor Gray
} else {
    Write-Host "No upload results yet" -ForegroundColor Yellow
}
Write-Host ""

# Process Status
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "RUNNING PROCESSES:" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Cyan

$pythonProcesses = Get-Process python -ErrorAction SilentlyContinue
if ($pythonProcesses) {
    Write-Host "Active Python processes: $($pythonProcesses.Count)" -ForegroundColor Green
    foreach ($proc in $pythonProcesses) {
        Write-Host "  PID: $($proc.Id) | CPU: $([math]::Round($proc.CPU, 2))s" -ForegroundColor Gray
    }
} else {
    Write-Host "No Python processes running" -ForegroundColor Yellow
}
Write-Host ""

# Bitcoin Status
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "BITCOIN:" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "Address: bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt" -ForegroundColor Cyan
Write-Host ""

# Analytics Status
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "ANALYTICS:" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Cyan

$analyticsFile = "F:\AI_Oracle_Root\scarify\analytics_data.json"
if (Test-Path $analyticsFile) {
    $analyticsData = Get-Content $analyticsFile -Raw | ConvertFrom-Json
    Write-Host "Data file exists - last updated: $((Get-Item $analyticsFile).LastWriteTime)" -ForegroundColor Green
} else {
    Write-Host "Analytics data not yet available" -ForegroundColor Yellow
}
Write-Host ""

# Quick Actions
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "QUICK ACTIONS:" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "[1] Check Bitcoin balance: python check_balance.py" -ForegroundColor White
Write-Host "[2] View analytics: python analytics_tracker.py report" -ForegroundColor White
Write-Host "[3] Open YouTube Studio: https://studio.youtube.com" -ForegroundColor White
Write-Host "[4] View videos: explorer abraham_horror\youtube_ready" -ForegroundColor White
Write-Host ""

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "           SYSTEM IS WORKING FOR YOU!" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

