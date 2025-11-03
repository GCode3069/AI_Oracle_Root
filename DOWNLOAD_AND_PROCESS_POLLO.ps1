# DOWNLOAD_AND_PROCESS_POLLO.ps1
# Complete workflow to turn Pollo.ai video into Max Headroom masterpiece

param(
    [string]$PolloURL = "https://pollo.ai/v/cmhh8uasf0k5e13uu1ybs96c8",
    [string]$Script = "Government shutdown day 30. They vacation while you starve. Both parties feast while the people bleed. Classic theater. Now you see the scam. Bitcoin below.",
    [int]$Episode = 70000,
    [string]$Title = "Lincoln's WARNING #70000: Government Shutdown SCAM #Shorts"
)

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "  POLLO.AI + MAX HEADROOM INTEGRATION" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

$PolloDir = "F:\AI_Oracle_Root\scarify\pollo_videos"
New-Item -Path $PolloDir -ItemType Directory -Force | Out-Null

$PolloFile = "$PolloDir\pollo_source_$Episode.mp4"

Write-Host "STEP 1: DOWNLOAD POLLO.AI VIDEO" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Your Pollo.ai video: $PolloURL" -ForegroundColor White
Write-Host ""
Write-Host "  MANUAL DOWNLOAD REQUIRED:" -ForegroundColor Red
Write-Host "    1. Open: $PolloURL" -ForegroundColor Gray
Write-Host "    2. Click download/export button" -ForegroundColor Gray
Write-Host "    3. Save to: $PolloFile" -ForegroundColor Gray
Write-Host ""

# Check if already downloaded
if (Test-Path $PolloFile) {
    Write-Host "  ✅ Pollo video found: $PolloFile" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "STEP 2: ADD MAX HEADROOM EFFECTS" -ForegroundColor Yellow
    Write-Host ""
    
    python INTEGRATE_POLLO_VIDEO.py `
        --manual "$PolloFile" `
        --script "$Script" `
        --episode $Episode `
        --title "$Title"
    
} else {
    Write-Host "  ⏳ Waiting for manual download..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "AFTER DOWNLOADING:" -ForegroundColor Green
    Write-Host ""
    Write-Host "  Run this command:" -ForegroundColor White
    Write-Host ""
    Write-Host "  .\DOWNLOAD_AND_PROCESS_POLLO.ps1 ``" -ForegroundColor Cyan
    Write-Host "    -PolloURL '$PolloURL' ``" -ForegroundColor Cyan
    Write-Host "    -Script '$Script' ``" -ForegroundColor Cyan
    Write-Host "    -Episode $Episode ``" -ForegroundColor Cyan
    Write-Host "    -Title '$Title'" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  Or just:" -ForegroundColor White
    Write-Host ""
    Write-Host "  python INTEGRATE_POLLO_VIDEO.py --manual '$PolloFile' --script '$Script' --episode $Episode --title '$Title'" -ForegroundColor Cyan
    Write-Host ""
}

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "  WHAT YOU'LL GET:" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  ✅ Pollo.ai animated Lincoln (lip-sync!)" -ForegroundColor Green
Write-Host "  ✅ Max Headroom RGB split glitches" -ForegroundColor Green
Write-Host "  ✅ VHS scan lines + static" -ForegroundColor Green
Write-Host "  ✅ Our psychological audio (theta + gamma)" -ForegroundColor Green
Write-Host "  ✅ Cash App QR code overlay" -ForegroundColor Green
Write-Host "  ✅ 20-25 optimized YouTube tags" -ForegroundColor Green
Write-Host "  ✅ YouTube upload ready" -ForegroundColor Green
Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""


