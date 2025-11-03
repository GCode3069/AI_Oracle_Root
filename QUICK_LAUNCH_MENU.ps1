# ============================================================================
# QUICK LAUNCH MENU - ALL INTEGRATED SYSTEMS
# ============================================================================

Write-Host ""
Write-Host "###############################################################################" -ForegroundColor Cyan
Write-Host "#                                                                             #" -ForegroundColor Cyan
Write-Host "#           🎯 SCARIFY - MULTI-STYLE GENERATION SYSTEM 🎯                    #" -ForegroundColor Cyan
Write-Host "#                                                                             #" -ForegroundColor Cyan
Write-Host "###############################################################################" -ForegroundColor Cyan
Write-Host ""
Write-Host "INTEGRATED SYSTEMS:" -ForegroundColor Yellow
Write-Host "  [OK] Multi-Style Script Generator (4 competitive styles)" -ForegroundColor Green
Write-Host "  [OK] Desktop Generator (GUI with style selection)" -ForegroundColor Green
Write-Host "  [OK] Mixed Batch Generator (50/30/15/5 optimal mix)" -ForegroundColor Green
Write-Host "  [OK] Production Pipeline (process JSON submissions)" -ForegroundColor Green
Write-Host ""
Write-Host "###############################################################################" -ForegroundColor Cyan
Write-Host "  SELECT GENERATION MODE:" -ForegroundColor Yellow
Write-Host "###############################################################################" -ForegroundColor Cyan
Write-Host ""
Write-Host "  [1] Desktop Generator (GUI) - Best for manual control" -ForegroundColor White
Write-Host "      → Visual interface" -ForegroundColor Gray
Write-Host "      → Select style, CTR level, batch count" -ForegroundColor Gray
Write-Host "      → Real-time progress display`n" -ForegroundColor Gray

Write-Host "  [2] Mixed Batch (20 videos) - Recommended for testing" -ForegroundColor White
Write-Host "      → 50% ChatGPT, 30% Cursor, 15% Opus, 5% Grok" -ForegroundColor Gray
Write-Host "      → Optimized revenue mix" -ForegroundColor Gray
Write-Host "      → Auto-upload to YouTube`n" -ForegroundColor Gray

Write-Host "  [3] Process Submissions (10 videos) - Use queued scripts" -ForegroundColor White
Write-Host "      → 5 ChatGPT scripts" -ForegroundColor Gray
Write-Host "      → 5 Grok scripts" -ForegroundColor Gray
Write-Host "      → Already validated and ready`n" -ForegroundColor Gray

Write-Host "  [4] Large Mixed Batch (100 videos) - Full production" -ForegroundColor White
Write-Host "      → Same optimal mix" -ForegroundColor Gray
Write-Host "      → Maximum revenue potential" -ForegroundColor Gray
Write-Host "      → 2-3 hour generation time`n" -ForegroundColor Gray

Write-Host "  [5] Test Multi-Style Generator - See all 4 styles" -ForegroundColor White
Write-Host "      → Demonstrates each competitive style" -ForegroundColor Gray
Write-Host "      → Same headline, different approaches" -ForegroundColor Gray
Write-Host "      → No video generation (just scripts)`n" -ForegroundColor Gray

Write-Host "  [0] Exit`n" -ForegroundColor Gray

Write-Host "###############################################################################" -ForegroundColor Cyan
Write-Host ""

$choice = Read-Host "Select option (0-5)"

switch ($choice) {
    "1" {
        Write-Host "`n[LAUNCHING DESKTOP GENERATOR...]`n" -ForegroundColor Green
        pythonw ABRAHAM_STUDIO_VHS.pyw
    }
    "2" {
        Write-Host "`n[MIXED BATCH: 20 videos]`n" -ForegroundColor Green
        Write-Host "Episode Range: #50000-50019" -ForegroundColor Cyan
        Write-Host "Mix: 10 ChatGPT, 6 Cursor, 3 Opus, 1 Grok`n" -ForegroundColor White
        python BATCH_MIXED_STRATEGY.py 20 --start 50000
    }
    "3" {
        Write-Host "`n[PROCESSING SUBMISSIONS: 10 videos]`n" -ForegroundColor Green
        Write-Host "Processing:" -ForegroundColor Cyan
        Write-Host "  → 5 ChatGPT videos (#30000-30004)" -ForegroundColor White
        Write-Host "  → 5 Grok videos (#60000-60004)`n" -ForegroundColor White
        python PRODUCTION_PIPELINE.py --all
    }
    "4" {
        Write-Host "`n[LARGE MIXED BATCH: 100 videos]`n" -ForegroundColor Green
        Write-Host "WARNING: This will take 2-3 hours" -ForegroundColor Yellow
        Write-Host "Episode Range: #50000-50099" -ForegroundColor Cyan
        Write-Host "Mix: 50 ChatGPT, 30 Cursor, 15 Opus, 5 Grok`n" -ForegroundColor White
        $confirm = Read-Host "Continue? (Y/N)"
        if ($confirm -eq "Y" -or $confirm -eq "y") {
            python BATCH_MIXED_STRATEGY.py 100 --start 50000
        } else {
            Write-Host "`nCancelled.`n" -ForegroundColor Yellow
        }
    }
    "5" {
        Write-Host "`n[TESTING MULTI-STYLE GENERATOR]`n" -ForegroundColor Green
        Write-Host "Generating scripts in all 4 styles...`n" -ForegroundColor Cyan
        python MULTI_STYLE_SCRIPT_GENERATOR.py
    }
    "0" {
        Write-Host "`nExiting...`n" -ForegroundColor Gray
    }
    default {
        Write-Host "`nInvalid option. Exiting.`n" -ForegroundColor Red
    }
}

Write-Host ""


