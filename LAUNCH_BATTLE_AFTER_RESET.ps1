# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  🏆 LLM BATTLE ROYALE - POST-RESET LAUNCHER                          ║
# ║  Elimination Rounds + Cash App QR + Algorithm Hack Immunity          ║
# ╚═══════════════════════════════════════════════════════════════════════╝

<#
.SYNOPSIS
    Launch LLM Battle Royale competition after laptop reset

.DESCRIPTION
    Complete launcher for elimination rounds battle system:
    - 12 rounds x 6 hours = 72 hours
    - Lowest earner eliminated each round
    - Algorithm hack immunity (most creative gets saved)
    - Cash App QR code mandatory in all videos
    - Top 3 finale for highest total revenue

.PARAMETER LLMName
    Your LLM competitor name (e.g., "Claude-Sonnet-4")

.PARAMETER RoundDuration
    Duration per round in hours (default: 6)

.PARAMETER VideoCount
    Number of videos to generate (default: 50)

.PARAMETER TestMode
    Run in test mode (no actual competition, just verify systems)

.EXAMPLE
    .\LAUNCH_BATTLE_AFTER_RESET.ps1 -LLMName "Claude-Sonnet-4" -VideoCount 50

.EXAMPLE
    .\LAUNCH_BATTLE_AFTER_RESET.ps1 -TestMode
#>

param(
    [string]$LLMName = "Claude-Sonnet-4",
    [int]$RoundDuration = 6,
    [int]$VideoCount = 50,
    [switch]$TestMode = $false
)

$ErrorActionPreference = "Continue"
$Root = "F:\AI_Oracle_Root\scarify"

# ============================================================================
# DISPLAY BANNER
# ============================================================================

function Show-BattleBanner {
    Clear-Host
    Write-Host ""
    Write-Host "╔═══════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║                                                                       ║" -ForegroundColor Cyan
    Write-Host "║              🏆 LLM BATTLE ROYALE - ELIMINATION ROUNDS 🏆            ║" -ForegroundColor Cyan
    Write-Host "║                                                                       ║" -ForegroundColor Cyan
    Write-Host "╚═══════════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  Competitor: $LLMName" -ForegroundColor Yellow
    Write-Host "  Format: 12 rounds x $RoundDuration hours = 72 hours total" -ForegroundColor White
    Write-Host "  Rule: Lowest earner eliminated each round" -ForegroundColor White
    Write-Host "  Exception: Algorithm hack immunity saves you" -ForegroundColor Green
    Write-Host "  Revenue: Cash App QR mandatory in all videos" -ForegroundColor Cyan
    Write-Host ""
}

# ============================================================================
# PRE-FLIGHT CHECKS
# ============================================================================

function Test-SystemReady {
    Write-Host "[STEP 1: PRE-FLIGHT CHECKS]" -ForegroundColor Cyan
    Write-Host ""
    
    $allGood = $true
    
    # Check Python
    Write-Host "  Checking Python..." -NoNewline
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python 3") {
            Write-Host " [OK] $pythonVersion" -ForegroundColor Green
        } else {
            Write-Host " [FAIL] Python 3 required" -ForegroundColor Red
            $allGood = $false
        }
    } catch {
        Write-Host " [FAIL] Python not found" -ForegroundColor Red
        $allGood = $false
    }
    
    # Check FFmpeg
    Write-Host "  Checking FFmpeg..." -NoNewline
    try {
        $ffmpegVersion = ffmpeg -version 2>&1 | Select-Object -First 1
        if ($ffmpegVersion -match "ffmpeg version") {
            Write-Host " [OK]" -ForegroundColor Green
        } else {
            Write-Host " [FAIL]" -ForegroundColor Red
            $allGood = $false
        }
    } catch {
        Write-Host " [FAIL] FFmpeg not found" -ForegroundColor Red
        $allGood = $false
    }
    
    # Check Cash App QR
    Write-Host "  Checking Cash App QR..." -NoNewline
    $qrPath = Join-Path $Root "qr_codes\cashapp_qr.png"
    if (Test-Path $qrPath) {
        Write-Host " [OK]" -ForegroundColor Green
    } else {
        Write-Host " [MISSING] Generating..." -ForegroundColor Yellow
        Set-Location $Root
        python fix_cashapp_qr_600.py
        if (Test-Path $qrPath) {
            Write-Host "  Cash App QR generated [OK]" -ForegroundColor Green
        } else {
            Write-Host "  Cash App QR generation [FAIL]" -ForegroundColor Red
            $allGood = $false
        }
    }
    
    # Check main generator
    Write-Host "  Checking video generator..." -NoNewline
    $generatorPath = Join-Path $Root "abraham_MAX_HEADROOM.py"
    if (Test-Path $generatorPath) {
        Write-Host " [OK]" -ForegroundColor Green
    } else {
        Write-Host " [FAIL] abraham_MAX_HEADROOM.py missing" -ForegroundColor Red
        $allGood = $false
    }
    
    # Check battle tracker
    Write-Host "  Checking battle tracker..." -NoNewline
    $trackerPath = Join-Path $Root "BATTLE_TRACKER_ELIMINATION_ROUNDS.py"
    if (Test-Path $trackerPath) {
        Write-Host " [OK]" -ForegroundColor Green
    } else {
        Write-Host " [FAIL] BATTLE_TRACKER_ELIMINATION_ROUNDS.py missing" -ForegroundColor Red
        $allGood = $false
    }
    
    Write-Host ""
    return $allGood
}

# ============================================================================
# INITIALIZE BATTLE TRACKER
# ============================================================================

function Initialize-BattleTracker {
    param([string]$Name)
    
    Write-Host "[STEP 2: INITIALIZE BATTLE TRACKER]" -ForegroundColor Cyan
    Write-Host ""
    
    Set-Location $Root
    
    Write-Host "  Creating tracker for: $Name" -ForegroundColor White
    
    $initScript = @"
from BATTLE_TRACKER_ELIMINATION_ROUNDS import EliminationRoundTracker
import sys

try:
    tracker = EliminationRoundTracker('$Name', 'battle_elim_001')
    tracker.print_overall_status()
    print('\n[OK] Battle tracker initialized')
    print(f'Tracker file: {tracker.tracking_file}')
    sys.exit(0)
except Exception as e:
    print(f'\n[ERROR] Failed to initialize tracker: {e}')
    sys.exit(1)
"@
    
    $initScript | Out-File -FilePath "temp_init_tracker.py" -Encoding UTF8
    
    $result = python temp_init_tracker.py
    Write-Host $result
    
    Remove-Item "temp_init_tracker.py" -ErrorAction SilentlyContinue
    
    Write-Host ""
}

# ============================================================================
# VERIFY CASH APP QR
# ============================================================================

function Test-CashAppQR {
    Write-Host "[STEP 3: CASH APP QR VERIFICATION]" -ForegroundColor Cyan
    Write-Host ""
    
    $qrPath = Join-Path $Root "qr_codes\cashapp_qr.png"
    
    if (Test-Path $qrPath) {
        $qr = Get-Item $qrPath
        Write-Host "  File: $($qr.Name)" -ForegroundColor White
        Write-Host "  Size: $($qr.Length) bytes" -ForegroundColor White
        Write-Host "  Link: https://cash.app/`$healthiwealthi/bitcoin/THZmAyn3nx" -ForegroundColor Cyan
        Write-Host ""
        
        Write-Host "  [OPENING QR CODE FOR SCAN TEST]" -ForegroundColor Yellow
        Start-Process $qr.FullName
        Write-Host ""
        Write-Host "  ACTION REQUIRED:" -ForegroundColor Yellow
        Write-Host "    1. QR code should be open on screen" -ForegroundColor White
        Write-Host "    2. Scan with phone camera app" -ForegroundColor White
        Write-Host "    3. Should show: 'Open Cash App'" -ForegroundColor White
        Write-Host "    4. Should load: Send Bitcoin to `$healthiwealthi" -ForegroundColor White
        Write-Host ""
        
        $scanResult = Read-Host "  Did QR code scan successfully? (Y/N)"
        
        if ($scanResult -eq "Y" -or $scanResult -eq "y") {
            Write-Host "  [OK] QR code verified" -ForegroundColor Green
            return $true
        } else {
            Write-Host "  [WARNING] QR code may need regeneration" -ForegroundColor Yellow
            Write-Host "  Run: python fix_cashapp_qr_600.py" -ForegroundColor Yellow
            return $false
        }
    } else {
        Write-Host "  [ERROR] QR code file not found" -ForegroundColor Red
        return $false
    }
}

# ============================================================================
# GENERATE TEST VIDEO
# ============================================================================

function New-TestVideo {
    Write-Host "[STEP 4: GENERATE TEST VIDEO]" -ForegroundColor Cyan
    Write-Host ""
    
    Set-Location $Root
    
    Write-Host "  Generating test video with Cash App QR..." -ForegroundColor White
    Write-Host "  Episode: #TEST_001" -ForegroundColor Gray
    Write-Host ""
    
    $env:EPISODE_NUM = "99999"
    
    python abraham_MAX_HEADROOM.py 1
    
    # Find latest video
    $latestVideo = Get-ChildItem "abraham_horror\uploaded\*.mp4" -ErrorAction SilentlyContinue | 
                   Sort-Object LastWriteTime -Descending | 
                   Select-Object -First 1
    
    if ($latestVideo) {
        Write-Host ""
        Write-Host "  [OK] Test video generated" -ForegroundColor Green
        Write-Host "  File: $($latestVideo.Name)" -ForegroundColor White
        Write-Host "  Size: $([math]::Round($latestVideo.Length/1MB, 1)) MB" -ForegroundColor White
        Write-Host "  Path: $($latestVideo.FullName)" -ForegroundColor Gray
        Write-Host ""
        
        Write-Host "  [OPENING VIDEO FOR VERIFICATION]" -ForegroundColor Yellow
        Start-Process $latestVideo.FullName
        Write-Host ""
        Write-Host "  ACTION REQUIRED:" -ForegroundColor Yellow
        Write-Host "    1. Video should be playing" -ForegroundColor White
        Write-Host "    2. Verify Cash App QR visible in top-right corner" -ForegroundColor White
        Write-Host "    3. QR should be 250x250px, white on black" -ForegroundColor White
        Write-Host "    4. Try scanning QR from video with phone" -ForegroundColor White
        Write-Host ""
        
        $videoOk = Read-Host "  Is video quality acceptable? (Y/N)"
        
        return ($videoOk -eq "Y" -or $videoOk -eq "y")
    } else {
        Write-Host "  [ERROR] Test video generation failed" -ForegroundColor Red
        return $false
    }
}

# ============================================================================
# START COMPETITION
# ============================================================================

function Start-BattleCompetition {
    param(
        [string]$Name,
        [int]$Videos
    )
    
    Write-Host "[STEP 5: START BATTLE COMPETITION]" -ForegroundColor Cyan
    Write-Host ""
    
    Write-Host "╔═══════════════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
    Write-Host "║                    BATTLE ROYALE - STARTING NOW                       ║" -ForegroundColor Magenta
    Write-Host "╚═══════════════════════════════════════════════════════════════════════╝" -ForegroundColor Magenta
    Write-Host ""
    Write-Host "  Competitor: $Name" -ForegroundColor Yellow
    Write-Host "  Videos to Generate: $Videos" -ForegroundColor White
    Write-Host "  Competition Format: 12 elimination rounds" -ForegroundColor White
    Write-Host "  Victory Condition: Highest total revenue" -ForegroundColor Green
    Write-Host "  Special Rule: Algorithm hack immunity" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  [CRITICAL RULES]" -ForegroundColor Yellow
    Write-Host "    • Lowest earner eliminated each round" -ForegroundColor White
    Write-Host "    • Cash App QR mandatory in ALL videos" -ForegroundColor White
    Write-Host "    • Most creative algo hack gets immunity" -ForegroundColor White
    Write-Host "    • Errors reduce revenue (not elimination)" -ForegroundColor White
    Write-Host "    • Top 3 compete in finale rounds" -ForegroundColor White
    Write-Host ""
    
    $ready = Read-Host "  Ready to start competition? (Y/N)"
    
    if ($ready -ne "Y" -and $ready -ne "y") {
        Write-Host ""
        Write-Host "  [CANCELLED] Competition not started" -ForegroundColor Yellow
        Write-Host ""
        return
    }
    
    Write-Host ""
    Write-Host "  [LAUNCHING COMPETITION]" -ForegroundColor Green
    Write-Host ""
    
    Set-Location $Root
    
    # Start generating videos with battle tracking
    $env:LLM_NAME = $Name
    $env:COMPETITION_ID = "battle_elim_001"
    
    Write-Host "  Generating $Videos videos with battle tracking..." -ForegroundColor White
    Write-Host ""
    
    # Run main generation loop
    for ($i = 1; $i -le $Videos; $i++) {
        $episode = 10000 + $i
        $env:EPISODE_NUM = $episode
        
        Write-Host "  [$i/$Videos] Generating Episode #$episode..." -ForegroundColor Cyan
        
        python abraham_MAX_HEADROOM.py 1
        
        # Every 10 videos, show tracker status
        if ($i % 10 -eq 0) {
            Write-Host ""
            Write-Host "  [PROGRESS UPDATE - $i/$Videos videos complete]" -ForegroundColor Yellow
            
            $statusScript = @"
from BATTLE_TRACKER_ELIMINATION_ROUNDS import EliminationRoundTracker
tracker = EliminationRoundTracker.load('$Name', 'battle_elim_001')
tracker.print_overall_status()
"@
            $statusScript | python
            
            Write-Host ""
        }
    }
    
    Write-Host ""
    Write-Host "╔═══════════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║                 BATTLE COMPETITION - GENERATION COMPLETE              ║" -ForegroundColor Green
    Write-Host "╚═══════════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    Write-Host "  Videos Generated: $Videos" -ForegroundColor White
    Write-Host "  Competitor: $Name" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  [NEXT STEPS]" -ForegroundColor Cyan
    Write-Host "    1. Monitor round revenue (every 6 hours)" -ForegroundColor White
    Write-Host "    2. Track elimination risk" -ForegroundColor White
    Write-Host "    3. Log algorithm hacks for immunity" -ForegroundColor White
    Write-Host "    4. Document all Cash App donations" -ForegroundColor White
    Write-Host "    5. Prepare for round-end eliminations" -ForegroundColor White
    Write-Host ""
}

# ============================================================================
# TEST MODE
# ============================================================================

function Start-TestMode {
    Write-Host "[TEST MODE - SYSTEM VERIFICATION ONLY]" -ForegroundColor Yellow
    Write-Host ""
    
    # Run all checks
    $systemOk = Test-SystemReady
    
    if (-not $systemOk) {
        Write-Host "[FAIL] System not ready for competition" -ForegroundColor Red
        Write-Host "Fix errors above before launching battle" -ForegroundColor Yellow
        return
    }
    
    Initialize-BattleTracker -Name "TEST_LLM"
    
    $qrOk = Test-CashAppQR
    
    if ($qrOk) {
        Write-Host "[STEP 4: SKIPPED IN TEST MODE]" -ForegroundColor Gray
        Write-Host "  To generate test video, run without -TestMode" -ForegroundColor Gray
        Write-Host ""
    }
    
    Write-Host "╔═══════════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║                     TEST MODE - VERIFICATION COMPLETE                 ║" -ForegroundColor Green
    Write-Host "╚═══════════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    Write-Host "  System Status: READY FOR COMPETITION" -ForegroundColor Green
    Write-Host ""
    Write-Host "  To start actual competition:" -ForegroundColor Cyan
    Write-Host "    .\LAUNCH_BATTLE_AFTER_RESET.ps1 -LLMName 'YourName' -VideoCount 50" -ForegroundColor White
    Write-Host ""
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

Set-Location $Root

Show-BattleBanner

if ($TestMode) {
    Start-TestMode
} else {
    # Full competition launch
    $systemOk = Test-SystemReady
    
    if (-not $systemOk) {
        Write-Host "[FAIL] System not ready" -ForegroundColor Red
        Write-Host "Run in test mode first: -TestMode" -ForegroundColor Yellow
        Write-Host ""
        exit 1
    }
    
    Initialize-BattleTracker -Name $LLMName
    
    $qrOk = Test-CashAppQR
    
    if (-not $qrOk) {
        Write-Host "[WARNING] QR code verification failed" -ForegroundColor Yellow
        $continue = Read-Host "Continue anyway? (Y/N)"
        if ($continue -ne "Y" -and $continue -ne "y") {
            Write-Host "[CANCELLED]" -ForegroundColor Yellow
            exit 1
        }
    }
    
    $videoOk = New-TestVideo
    
    if (-not $videoOk) {
        Write-Host "[WARNING] Test video verification failed" -ForegroundColor Yellow
        $continue = Read-Host "Continue with full generation anyway? (Y/N)"
        if ($continue -ne "Y" -and $continue -ne "y") {
            Write-Host "[CANCELLED]" -ForegroundColor Yellow
            exit 1
        }
    }
    
    Start-BattleCompetition -Name $LLMName -Videos $VideoCount
}

Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")



