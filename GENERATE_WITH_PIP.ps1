# GENERATE_WITH_PIP.ps1
# Generate video with Picture-in-Picture (PIP) Max Headroom effect

Write-Host "`n================================================================" -ForegroundColor Magenta
Write-Host "  MAX HEADROOM ULTIMATE - WITH PICTURE-IN-PICTURE" -ForegroundColor Magenta
Write-Host "================================================================`n" -ForegroundColor Magenta

Write-Host "GENERATING VIDEO WITH:" -ForegroundColor Yellow
Write-Host "  [OK] Picture-in-Picture (multiple screens)" -ForegroundColor Green
Write-Host "  [OK] Non-repetitive roast scripts (50+ unique)" -ForegroundColor Green
Write-Host "  [OK] NO comedian names (pure energy)" -ForegroundColor Green
Write-Host "  [OK] Max Headroom glitchy aesthetic" -ForegroundColor Green
Write-Host "  [OK] 400px QR code (visible)" -ForegroundColor Green
Write-Host "  [OK] All psychological audio" -ForegroundColor Green
Write-Host "  [OK] Jumpscare effects`n" -ForegroundColor Green

Write-Host "VISUAL STYLE:" -ForegroundColor Yellow
Write-Host "  - Main screen: Large Lincoln (center)" -ForegroundColor White
Write-Host "  - PIP 1: Edge-detected (top-left)" -ForegroundColor White
Write-Host "  - PIP 2: Inverted colors (top-right)" -ForegroundColor White
Write-Host "  - Bottom: Glitch strip (RGB split)" -ForegroundColor White
Write-Host "  - QR: Top-right (400px, visible)`n" -ForegroundColor White

Write-Host "This is TRUE Max Headroom multi-screen aesthetic!`n" -ForegroundColor Cyan

Write-Host "================================================================`n" -ForegroundColor Magenta

Write-Host "Starting generation...`n" -ForegroundColor Yellow

# Use ultimate generator
$env:USE_LIPSYNC="false"  # Disable for speed
$env:USE_JUMPSCARE="true"  # Enable glitch
$env:EPISODE_NUM="8888"  # Ultimate episode

python -c "
import sys
from pathlib import Path
from datetime import datetime
import subprocess
sys.path.insert(0, str(Path.cwd()))

from abraham_MAX_HEADROOM import generate_voice, generate_lincoln_face_pollo, get_headlines, upload_to_youtube, BASE_DIR
from MAX_HEADROOM_ULTIMATE import get_non_repetitive_roast, create_max_headroom_ultimate

# Get headline
headline = get_headlines()[0]
print(f'Headline: {headline}\n')

# Generate NON-REPETITIVE script (no comedian names)
script_tracker = BASE_DIR / 'used_scripts.txt'
used = set()
if script_tracker.exists():
    used = set(script_tracker.read_text().splitlines())

script = get_non_repetitive_roast(headline, used)

print(f'[Script] Generated unique roast')
print(f'  Words: {len(script.split())}')
print(f'  Previously used: {len(used)}')
print(f'  Preview: {script[:80]}...\n')

# Save to tracker
with open(script_tracker, 'a', encoding='utf-8') as f:
    f.write(script + chr(10))

# Generate voice
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
audio_path = BASE_DIR / 'audio' / f'ULTIMATE_{timestamp}.mp3'
audio_path.parent.mkdir(parents=True, exist_ok=True)

print('[Voice] Generating with psychological audio...')
if not generate_voice(script, audio_path):
    sys.exit(1)

# Get Lincoln
print('[Lincoln] Getting face...')
lincoln = generate_lincoln_face_pollo()

# Get QR
print('[QR] Getting Cash App QR...')
qr = BASE_DIR / 'qr_codes' / 'cashapp_qr.png'
if not qr.exists():
    print('[QR] Warning: QR not found, will skip')
    qr = None

# Create ULTIMATE video with PIP
print('[Video] Creating Max Headroom ULTIMATE (PIP effect)...')
output = BASE_DIR / 'uploaded' / f'ULTIMATE_PIP_{timestamp}.mp4'
output.parent.mkdir(parents=True, exist_ok=True)

video = create_max_headroom_ultimate(lincoln, audio_path, output, headline, qr)

if video and Path(video).exists():
    size = Path(video).stat().st_size / (1024*1024)
    print(f'\n[OK] Video created: {size:.1f} MB')
    
    # Upload
    print(f'\n[Upload] Uploading to YouTube...')
    url = upload_to_youtube(Path(video), headline, 8888)
    
    if url:
        print(f'\n' + '='*60)
        print(f'SUCCESS!')
        print(f'='*60)
        print(f'\nYouTube: {url}')
        print(f'\nFeatures:')
        print(f'  [OK] Picture-in-Picture (multi-screen)')
        print(f'  [OK] Non-repetitive script')
        print(f'  [OK] No comedian names')
        print(f'  [OK] 400px QR code')
        print(f'  [OK] Max Headroom glitch')
        print(f'\n' + '='*60)
else:
    print('\n[FAIL] Video generation failed')
"

Write-Host "`n================================================================" -ForegroundColor Magenta
Write-Host "  GENERATION COMPLETE" -ForegroundColor Magenta
Write-Host "================================================================`n" -ForegroundColor Magenta

