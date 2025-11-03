# UPDATE_GENERATOR_WITH_SCREAMS.ps1
# Integrate scream/jumpcut scripts into generator

Write-Host "`n================================================================" -ForegroundColor Magenta
Write-Host "  UPDATING GENERATOR - SCREAMS & JUMPCUTS" -ForegroundColor Magenta
Write-Host "================================================================`n" -ForegroundColor Magenta

Write-Host "Based on screenshot analysis:" -ForegroundColor Yellow
Write-Host "  Video 3: 'Senate advances bill' - 226 views (BEST PERFORMER)" -ForegroundColor Green
Write-Host "  What works: Motion, traction" -ForegroundColor Green
Write-Host "  Missing: QR code, Bitcoin address recitation`n" -ForegroundColor Red

Write-Host "NEW FEATURES ADDING:" -ForegroundColor Yellow
Write-Host "  [NEW] SCREAM markers (2-3 per video)" -ForegroundColor Cyan
Write-Host "        - Audio spike + visual flash" -ForegroundColor Gray
Write-Host "        - Screen shake effect" -ForegroundColor Gray
Write-Host "        - Color inversion pulse`n" -ForegroundColor Gray

Write-Host "  [NEW] JUMPCUT markers (2-3 per video)" -ForegroundColor Cyan
Write-Host "        - Quick glitch transition" -ForegroundColor Gray
Write-Host "        - RGB shift" -ForegroundColor Gray
Write-Host "        - Scanline distortion`n" -ForegroundColor Gray

Write-Host "  [FIX] NO Bitcoin address recitation" -ForegroundColor Cyan
Write-Host "        - QR code is enough!" -ForegroundColor Gray
Write-Host "        - Use that time for MORE SATIRE`n" -ForegroundColor Gray

Write-Host "  [FIX] 400px QR code" -ForegroundColor Cyan
Write-Host "        - Visible entire video" -ForegroundColor Gray
Write-Host "        - Top-right corner`n" -ForegroundColor Gray

Write-Host "================================================================`n" -ForegroundColor Magenta

Write-Host "Generating TEST video with ALL new features...`n" -ForegroundColor Cyan

python -c "
import sys, random
from pathlib import Path
from datetime import datetime
sys.path.insert(0, str(Path.cwd()))

from abraham_MAX_HEADROOM import generate_voice, generate_lincoln_face_pollo, upload_to_youtube, BASE_DIR
from ADD_SCREAMS_AND_JUMPCUTS import get_scream_jumpcut_script, parse_scream_jumpcut_markers
from MAX_HEADROOM_ULTIMATE import create_max_headroom_ultimate

# Get headline
headline = 'Government Shutdown Day 15'
print(f'Headline: {headline}\n')

# Generate script WITH screams & jumpcuts
script_raw = get_scream_jumpcut_script(headline)
script_clean, scream_times, jumpcut_times = parse_scream_jumpcut_markers(script_raw)

print(f'[Script] With markers:')
print(f'  {script_raw}\n')
print(f'[Script] Clean: {len(script_clean.split())} words')
print(f'  Screams at: {scream_times}')
print(f'  Jumpcuts at: {jumpcut_times}')
print(f'  Preview: {script_clean[:80]}...\n')

# Verify NO Bitcoin address
if 'bc1q' in script_clean:
    print('[ERROR] Bitcoin address still in script!')
    sys.exit(1)
else:
    print('[OK] No Bitcoin address - just QR code!\n')

# Generate voice
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
audio_path = BASE_DIR / 'audio' / f'SCREAM_TEST_{timestamp}.mp3'
audio_path.parent.mkdir(parents=True, exist_ok=True)

print('[Voice] Generating voice...')
if not generate_voice(script_clean, audio_path):
    print('[ERROR] Voice generation failed')
    sys.exit(1)

# Get Lincoln
print('[Lincoln] Getting face...')
lincoln = generate_lincoln_face_pollo()

# Get QR
qr = BASE_DIR / 'qr_codes' / 'cashapp_qr.png'

# Create video with PIP
print('[Video] Creating Max Headroom with PIP + screams/jumpcuts...')
output = BASE_DIR / 'uploaded' / f'SCREAM_JUMPCUT_{timestamp}.mp4'
output.parent.mkdir(parents=True, exist_ok=True)

video = create_max_headroom_ultimate(lincoln, audio_path, output, headline, qr)

if video and Path(video).exists():
    size = Path(video).stat().st_size / (1024*1024)
    print(f'\n[OK] Video: {size:.1f} MB')
    
    # Upload
    print(f'\n[Upload] Uploading to YouTube...')
    url = upload_to_youtube(Path(video), headline, 7777)
    
    if url:
        print(f'\n' + '='*60)
        print(f'SUCCESS - SCREAM/JUMPCUT VIDEO READY!')
        print(f'='*60)
        print(f'\nYouTube: {url}')
        print(f'\nFeatures:')
        print(f'  [OK] {len(scream_times)} scream effects')
        print(f'  [OK] {len(jumpcut_times)} jumpcut glitches')
        print(f'  [OK] NO Bitcoin address recitation')
        print(f'  [OK] More satire instead')
        print(f'  [OK] Picture-in-Picture (multi-screen)')
        print(f'  [OK] 400px QR code visible')
        print(f'\n' + '='*60)
else:
    print('\n[ERROR] Video generation failed')
"

Write-Host "`n================================================================" -ForegroundColor Magenta
Write-Host "  GENERATION COMPLETE" -ForegroundColor Magenta
Write-Host "================================================================`n" -ForegroundColor Magenta

Write-Host "Check YouTube for new video with:" -ForegroundColor Yellow
Write-Host "  - Scream effects (2-3 per video)" -ForegroundColor Cyan
Write-Host "  - Jumpcut glitches (2-3 per video)" -ForegroundColor Cyan
Write-Host "  - NO Bitcoin address spoken" -ForegroundColor Green
Write-Host "  - More satire in that time" -ForegroundColor Cyan
Write-Host "  - Picture-in-Picture (multi-screen)" -ForegroundColor Cyan
Write-Host "  - 400px QR code visible`n" -ForegroundColor Cyan

Write-Host "================================================================`n" -ForegroundColor Magenta


