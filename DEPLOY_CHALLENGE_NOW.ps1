# ============================================================================
# DEPLOY CHALLENGE - CTR MASTER + BATTLE ROYALE
# ============================================================================

param(
    [int]$Round = 1,
    [int]$VideosPerRound = 5,
    [int]$StartEpisode = 20000,
    [switch]$FullCompetition
)

Write-Host ""
Write-Host "###############################################################################" -ForegroundColor Magenta
Write-Host "#                                                                             #" -ForegroundColor Magenta
Write-Host "#         🏆 BATTLE ROYALE + CTR MASTER DEPLOYMENT 🏆                        #" -ForegroundColor Magenta
Write-Host "#                                                                             #" -ForegroundColor Magenta
Write-Host "###############################################################################" -ForegroundColor Magenta
Write-Host ""

if ($FullCompetition) {
    Write-Host "MODE: Full Competition (12 Rounds)" -ForegroundColor Yellow
    Write-Host "  Total Videos: $($VideosPerRound * 12)" -ForegroundColor White
    Write-Host "  Target Revenue: `$3,690 in 72 hours" -ForegroundColor Cyan
} else {
    Write-Host "MODE: Single Round #$Round" -ForegroundColor Yellow
    Write-Host "  Videos: $VideosPerRound" -ForegroundColor White
}

Write-Host ""
Write-Host "OPTIMIZATION:" -ForegroundColor Yellow
Write-Host "  [OK] CTR-optimized titles (8-15% target)" -ForegroundColor Green
Write-Host "  [OK] Shock hooks (0-3s)" -ForegroundColor Green
Write-Host "  [OK] 12-15 second format" -ForegroundColor Green
Write-Host "  [OK] Cash App QR monetization" -ForegroundColor Green
Write-Host "  [OK] Battle tracking enabled" -ForegroundColor Green
Write-Host ""

Write-Host "STARTING FROM: Episode #$StartEpisode" -ForegroundColor Cyan
Write-Host ""

Write-Host "###############################################################################" -ForegroundColor Magenta
Write-Host ""

# Change to project directory
Set-Location F:\AI_Oracle_Root\scarify

# Set episode number
$env:EPISODE_NUM = $StartEpisode

# Run the integrated system
Write-Host "[LAUNCHING...]`n" -ForegroundColor Green

if ($FullCompetition) {
    # Full competition
    python BATTLE_CTR_INTEGRATION.py --llm "CTR_Master" --full --videos $VideosPerRound --start $StartEpisode
} else {
    # Single round
    python BATTLE_CTR_INTEGRATION.py --llm "CTR_Master" --round $Round --videos $VideosPerRound --start $StartEpisode
}

Write-Host ""
Write-Host "###############################################################################" -ForegroundColor Magenta
Write-Host "#                                                                             #" -ForegroundColor Magenta
Write-Host "#                          ✅ DEPLOYMENT COMPLETE ✅                          #" -ForegroundColor Magenta
Write-Host "#                                                                             #" -ForegroundColor Magenta
Write-Host "###############################################################################" -ForegroundColor Magenta
Write-Host ""

# Show battle tracker status
Write-Host "CHECKING BATTLE STANDINGS...`n" -ForegroundColor Cyan

if (Test-Path "battle_data.json") {
    $battleData = Get-Content "battle_data.json" -Raw | ConvertFrom-Json
    
    Write-Host "CURRENT STANDINGS:" -ForegroundColor Yellow
    Write-Host ""
    
    $sorted = $battleData.llms.PSObject.Properties | Sort-Object {$_.Value.total_revenue} -Descending
    
    $rank = 1
    foreach ($llm in $sorted) {
        $name = $llm.Name
        $data = $llm.Value
        $revenue = $data.total_revenue
        $videos = $data.videos_generated
        $errors = $data.error_count
        
        Write-Host "  #$rank $name" -ForegroundColor $(if ($rank -eq 1) { 'Green' } else { 'White' })
        Write-Host "      Revenue: `$$([math]::Round($revenue, 2))" -ForegroundColor Cyan
        Write-Host "      Videos: $videos" -ForegroundColor White
        Write-Host "      Errors: $errors" -ForegroundColor $(if ($errors -gt 50) { 'Red' } else { 'White' })
        Write-Host ""
        
        $rank++
    }
}

Write-Host "###############################################################################" -ForegroundColor Magenta
Write-Host ""
Write-Host "VIDEOS UPLOADED TO:" -ForegroundColor Yellow
Write-Host "  YouTube: https://studio.youtube.com" -ForegroundColor Cyan
Write-Host ""
Write-Host "CHECK CTR IN 24-48 HOURS:" -ForegroundColor Yellow
Write-Host "  YouTube Studio > Analytics > Reach > CTR" -ForegroundColor Cyan
Write-Host "  Target: 8%+ (excellent), 15%+ (viral)" -ForegroundColor White
Write-Host ""
Write-Host "###############################################################################" -ForegroundColor Magenta
Write-Host ""


