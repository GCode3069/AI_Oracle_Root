# GENERATE_10_VIDEOS_BATCH.ps1
# Generate 10 videos in proven clean style with darker scripts

param(
    [int]$Count = 10,
    [int]$StartEpisode = 5000
)

Write-Host "`n================================================================" -ForegroundColor Green
Write-Host "  BATCH GENERATION - 10 VIDEOS IN PROVEN STYLE" -ForegroundColor Green
Write-Host "================================================================`n" -ForegroundColor Green

Write-Host "GENERATING: $Count videos" -ForegroundColor Yellow
Write-Host "STARTING AT: Episode #$StartEpisode" -ForegroundColor White
Write-Host "STYLE: Clean professional (NOT messy)" -ForegroundColor Cyan
Write-Host "SCRIPTS: Darker ethical satire (100+ unique)" -ForegroundColor Cyan
Write-Host "FEATURES: All optimizations included`n" -ForegroundColor Cyan

Write-Host "Each video will have:" -ForegroundColor Yellow
Write-Host "  [OK] Clean single screen (not messy PIP)" -ForegroundColor Green
Write-Host "  [OK] 400px QR code (visible)" -ForegroundColor Green
Write-Host "  [OK] Darker satirical script (unique)" -ForegroundColor Green
Write-Host "  [OK] NO Bitcoin address recitation" -ForegroundColor Green
Write-Host "  [OK] NO comedian names" -ForegroundColor Green
Write-Host "  [OK] Psychological audio (6/40/60 Hz)" -ForegroundColor Green
Write-Host "  [OK] Max Headroom glitch aesthetic" -ForegroundColor Green
Write-Host "  [OK] YouTube-safe encoding`n" -ForegroundColor Green

Write-Host "================================================================`n" -ForegroundColor Green

$confirmation = Read-Host "Start batch generation? (yes/no)"

if ($confirmation -ne "yes") {
    Write-Host "`nAborted." -ForegroundColor Yellow
    exit
}

$startTime = Get-Date
$successCount = 0
$failCount = 0

for ($i = 0; $i -lt $Count; $i++) {
    $episodeNum = $StartEpisode + $i
    $currentNum = $i + 1
    
    Write-Host "`n[$currentNum/$Count] Generating Episode #$episodeNum..." -ForegroundColor Cyan
    Write-Host "================================================================" -ForegroundColor Gray
    
    # Generate video using clean style with darker scripts
    $env:EPISODE_NUM = $episodeNum
    
    python -c "
import sys, random
from pathlib import Path
from datetime import datetime
sys.path.insert(0, str(Path.cwd()))

from abraham_MAX_HEADROOM import generate_voice, generate_lincoln_face_pollo, get_headlines, upload_to_youtube, BASE_DIR
from DARKER_ETHICAL_SCRIPTS import get_darker_roast
from CLEAN_UP_MESSY_VISUALS import create_clean_max_headroom

# Get headline
headline = get_headlines()[0]
print(f'Headline: {headline}')

# Generate DARKER script
script = get_darker_roast(headline)
print(f'Script: {len(script.split())} words')
print(f'Preview: {script[:80]}...\n')

# Generate voice
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
audio_path = BASE_DIR / 'audio' / f'BATCH_{$episodeNum}_{timestamp}.mp3'
audio_path.parent.mkdir(parents=True, exist_ok=True)

if generate_voice(script, audio_path):
    lincoln = generate_lincoln_face_pollo()
    qr = BASE_DIR / 'qr_codes' / 'cashapp_qr.png'
    
    output = BASE_DIR / 'uploaded' / f'BATCH_{$episodeNum}_{timestamp}.mp4'
    output.parent.mkdir(parents=True, exist_ok=True)
    
    video = create_clean_max_headroom(lincoln, audio_path, output, qr)
    
    if video and Path(video).exists():
        url = upload_to_youtube(Path(video), headline, $episodeNum)
        if url:
            print(f'\n[OK] Episode #{$episodeNum}: {url}')
            exit(0)

exit(1)
"
    
    if ($LASTEXITCODE -eq 0) {
        $successCount++
        Write-Host "[SUCCESS] Episode #$episodeNum completed" -ForegroundColor Green
    } else {
        $failCount++
        Write-Host "[FAIL] Episode #$episodeNum failed" -ForegroundColor Red
    }
    
    # Brief pause between videos
    if ($i -lt ($Count - 1)) {
        Write-Host "Waiting 30 seconds before next video..." -ForegroundColor Gray
        Start-Sleep -Seconds 30
    }
}

$endTime = Get-Date
$duration = $endTime - $startTime

Write-Host "`n================================================================" -ForegroundColor Green
Write-Host "  BATCH GENERATION COMPLETE" -ForegroundColor Green
Write-Host "================================================================`n" -ForegroundColor Green

Write-Host "RESULTS:" -ForegroundColor Yellow
Write-Host "  Success: $successCount videos" -ForegroundColor Green
Write-Host "  Failed: $failCount videos" -ForegroundColor $(if ($failCount -gt 0) {'Red'} else {'Green'})
Write-Host "  Duration: $($duration.ToString('hh\:mm\:ss'))" -ForegroundColor White
Write-Host "  Average: $([math]::Round($successCount / $duration.TotalMinutes, 1)) videos/minute`n" -ForegroundColor White

Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host "  1. Check YouTube Studio for all uploads" -ForegroundColor Cyan
Write-Host "  2. Review video tracking: python VIDEO_REVIEW_TRACKER.py --list" -ForegroundColor Cyan
Write-Host "  3. Cross-post to other platforms" -ForegroundColor Cyan
Write-Host "  4. Monitor performance in 24-48 hours`n" -ForegroundColor Cyan

Write-Host "================================================================`n" -ForegroundColor Green


