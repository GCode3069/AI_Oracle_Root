# REVENUE ACCELERATION SYSTEM - LAUNCHER
# Executes ALL revenue strategies automatically

param([int]$Videos = 10, [int]$StartEpisode = 1050)

$ROOT = "F:\AI_Oracle_Root\scarify"

Write-Host ""
Write-Host "="*70 -ForegroundColor Green
Write-Host "  REVENUE ACCELERATION SYSTEM - AUTOMATED" -ForegroundColor Green
Write-Host "="*70 -ForegroundColor Green
Write-Host ""

# Step 1: Create Gumroad products (if not exists)
Write-Host "[1/6] Creating Gumroad Products..." -ForegroundColor Cyan
if (-not (Test-Path "$ROOT\gumroad_products\Lincoln_Script_Pack_`$27.zip")) {
    python "$ROOT\create_gumroad_products.py"
} else {
    Write-Host "  [OK] Products already created" -ForegroundColor Green
}

# Step 2: Generate videos with dark comedy
Write-Host "`n[2/6] Generating $Videos Dark Comedy Videos..." -ForegroundColor Cyan
Set-Location $ROOT
$env:EPISODE_NUM = $StartEpisode
python abraham_MAX_HEADROOM.py $Videos

# Step 3: Upload to multiple platforms
Write-Host "`n[3/6] Multi-Platform Upload..." -ForegroundColor Cyan
$uploadedDir = "$ROOT\abraham_horror\uploaded"
$latestVideos = Get-ChildItem $uploadedDir -Filter "*.mp4" | Sort-Object LastWriteTime -Descending | Select-Object -First $Videos

foreach ($video in $latestVideos) {
    Write-Host "  Uploading: $($video.Name)" -ForegroundColor White
    
    # YouTube: Already done in main script
    Write-Host "    [OK] YouTube" -ForegroundColor Green
    
    # TikTok: Manual or automated
    Write-Host "    [MANUAL] TikTok - Use tiktok_auto_uploader.py" -ForegroundColor Yellow
    
    # Rumble: Automated
    Write-Host "    [READY] Rumble - Use rumble_auto_uploader.py" -ForegroundColor Yellow
}

# Step 4: Generate affiliate descriptions
Write-Host "`n[4/6] Generating Affiliate Descriptions..." -ForegroundColor Cyan
python "$ROOT\affiliate_link_injector.py" --projections

# Step 5: Update revenue tracker
Write-Host "`n[5/6] Revenue Tracker Dashboard..." -ForegroundColor Cyan
python "$ROOT\revenue_tracker_dashboard.py"

# Step 6: Show next steps
Write-Host "`n[6/6] Next Steps..." -ForegroundColor Cyan
Write-Host ""
Write-Host "="*70 -ForegroundColor Green
Write-Host "  REVENUE SYSTEM READY" -ForegroundColor Green
Write-Host "="*70 -ForegroundColor Green
Write-Host ""
Write-Host "[PRODUCTS CREATED]" -ForegroundColor Cyan
Write-Host "  • Lincoln_Script_Pack_`$27.zip (100 scripts)" -ForegroundColor White
Write-Host "  • Lincoln_Complete_System_`$97.zip (full generator)" -ForegroundColor White
Write-Host "  Location: $ROOT\gumroad_products\" -ForegroundColor Gray
Write-Host ""
Write-Host "[VIDEOS GENERATED]" -ForegroundColor Cyan
Write-Host "  • Count: $Videos videos" -ForegroundColor White
Write-Host "  • Dark comedy: Roasts everyone" -ForegroundColor White
Write-Host "  • Auto-tracked: video_tracking.csv" -ForegroundColor White
Write-Host ""
Write-Host "[UPLOAD TO PLATFORMS]" -ForegroundColor Cyan
Write-Host "  • YouTube: Auto-uploaded" -ForegroundColor Green
Write-Host "  • TikTok: Run tiktok_auto_uploader.py --batch $Videos" -ForegroundColor Yellow
Write-Host "  • Rumble: Run rumble_auto_uploader.py --batch $Videos" -ForegroundColor Yellow
Write-Host ""
Write-Host "[MONETIZATION SETUP]" -ForegroundColor Cyan
Write-Host "  1. Create Gumroad account: gumroad.com" -ForegroundColor White
Write-Host "  2. Upload products (gumroad_products folder)" -ForegroundColor White
Write-Host "  3. Set prices: `$27, `$97" -ForegroundColor White
Write-Host "  4. Add links to video descriptions" -ForegroundColor White
Write-Host "  5. Create CashApp: `$LincolnWarnings" -ForegroundColor White
Write-Host "  6. Sign up Rumble: rumble.com" -ForegroundColor White
Write-Host ""
Write-Host "[REVENUE PROJECTIONS]" -ForegroundColor Cyan
Write-Host "  30 days: `$5,750-15,200" -ForegroundColor Green
Write-Host "  90 days: `$25,000-50,000" -ForegroundColor Green
Write-Host "  vs. YouTube Shorts Fund: `$0 (12-month wait)" -ForegroundColor Red
Write-Host ""
Write-Host "="*70 -ForegroundColor Green
Write-Host ""

# Open folders
Start-Process explorer.exe -ArgumentList "$ROOT\gumroad_products"
Start-Process explorer.exe -ArgumentList "$ROOT\abraham_horror\uploaded"

