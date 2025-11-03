# GENERATE_ULTIMATE_VIDEO.ps1
# Quick launcher for ultimate combined video

Write-Host "`n================================================================" -ForegroundColor Magenta
Write-Host "  ULTIMATE COMBINED VIDEO GENERATOR" -ForegroundColor Magenta
Write-Host "================================================================`n" -ForegroundColor Magenta

Write-Host "This will create a video combining:" -ForegroundColor Yellow
Write-Host "  [OK] Glitchy jumpcut Lincoln (Video 1 style)" -ForegroundColor Green
Write-Host "  [OK] Max Headroom effects" -ForegroundColor Green
Write-Host "  [OK] 400px QR code (VISIBLE)" -ForegroundColor Green
Write-Host "  [OK] Jumpscare effects (enhanced)" -ForegroundColor Green
Write-Host "  [OK] Psychological audio (6/40/60 Hz)" -ForegroundColor Green
Write-Host "  [OK] VHS glitch effects" -ForegroundColor Green
Write-Host "  [OK] All neuro-optimizations`n" -ForegroundColor Green

Write-Host "REFERENCE VIDEOS:" -ForegroundColor Yellow
Write-Host "  Video 1: https://www.youtube.com/watch?v=1cF8DwthSJc" -ForegroundColor White
Write-Host "           (Good glitchy jumpcut, missing QR)" -ForegroundColor Gray
Write-Host "  Video 2: https://www.youtube.com/shorts/fhkTwie5poc" -ForegroundColor White
Write-Host "           (Other good elements)`n" -ForegroundColor Gray

Write-Host "OUTPUT:" -ForegroundColor Yellow
Write-Host "  - New video with BEST of both" -ForegroundColor White
Write-Host "  - QR code fixed (400px)" -ForegroundColor White
Write-Host "  - Maximum glitch effects" -ForegroundColor White
Write-Host "  - Auto-uploaded to YouTube`n" -ForegroundColor White

Write-Host "================================================================`n" -ForegroundColor Magenta

Write-Host "Generating ultimate video...`n" -ForegroundColor Cyan

# Generate with all features enabled
$env:USE_LIPSYNC="false"  # Disable for speed
$env:USE_JUMPSCARE="true"  # Enable for glitch
$env:EPISODE_NUM="9999"  # Special episode number

python abraham_MAX_HEADROOM.py 1

Write-Host "`n================================================================" -ForegroundColor Magenta
Write-Host "  GENERATION COMPLETE" -ForegroundColor Magenta
Write-Host "================================================================`n" -ForegroundColor Magenta

Write-Host "Check YouTube Studio for the new video!" -ForegroundColor Yellow
Write-Host "  https://studio.youtube.com`n" -ForegroundColor Cyan

Write-Host "VERIFY:" -ForegroundColor Yellow
Write-Host "  - QR code visible in top-right (400px)" -ForegroundColor Cyan
Write-Host "  - Glitchy jumpcut effects present" -ForegroundColor Cyan
Write-Host "  - Max Headroom style aesthetic" -ForegroundColor Cyan
Write-Host "  - Jumpscare effects synced" -ForegroundColor Cyan
Write-Host "  - All features working`n" -ForegroundColor Cyan

Write-Host "================================================================`n" -ForegroundColor Magenta

# Track the upload
python VIDEO_REVIEW_TRACKER.py --last


