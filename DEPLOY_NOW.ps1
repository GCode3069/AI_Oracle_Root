# ============================================================================
# SCARIFY ONE-LINER DEPLOYMENT
# Run this single command to deploy everything automatically
# ============================================================================

Write-Host @"

╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║     🔥 SCARIFY INSTANT DEPLOYMENT 🔥                                      ║
║                                                                            ║
║     This will automatically:                                               ║
║     ✅ Check prerequisites                                                 ║
║     ✅ Create directory structure                                          ║
║     ✅ Deploy all scripts                                                  ║
║     ✅ Install dependencies                                                ║
║     ✅ Generate 3 test videos                                              ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Cyan

Write-Host "Press Ctrl+C to cancel, or" -ForegroundColor Yellow
$countdown = 5
for ($i = $countdown; $i -gt 0; $i--) {
    Write-Host "  Starting in $i seconds..." -ForegroundColor Gray -NoNewline
    Start-Sleep -Seconds 1
    Write-Host "`r" -NoNewline
}
Write-Host "  🚀 Starting deployment now!                    " -ForegroundColor Green
Write-Host ""

# Execute the bootstrap
& "$PSScriptRoot\scarify_bootstrap.ps1" -VideoCount 3 -Archetype "Mystic"

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  ✅ DEPLOYMENT COMPLETE!                                                   ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "📹 Check your videos: explorer output\videos" -ForegroundColor White
Write-Host ""

