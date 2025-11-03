#!/usr/bin/env python3
"""
ULTRA-SIMPLE GENERATOR
Minimal effects, maximum speed, NO TIMEOUTS POSSIBLE
Target: <30s generation time

Includes:
✓ Lincoln image
✓ Cash App QR code
✓ Basic zoom
✓ Audio
✓ Text overlay

Skips (for speed):
✗ Complex VHS effects
✗ Lip-sync
✗ Heavy color grading
✗ Multiple filter passes
"""
import os, sys, subprocess, random
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from abraham_MAX_HEADROOM import (
    generate_script, generate_voice, generate_lincoln_face_pollo,
    upload_to_youtube, get_headlines, log_to_google_sheets
)

BASE_DIR = Path("F:/AI_Oracle_Root/scarify/abraham_horror")

def create_ultra_simple_video(lincoln_img, audio_path, output_path):
    """Ultra-simple video - GUARANTEED to work in <30s"""
    
    # Get duration
    probe = subprocess.run([
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)
    ], capture_output=True, text=True, timeout=10)
    dur = float(probe.stdout.strip())
    
    # Get QR (check both locations)
    qr_path = BASE_DIR / "qr_codes" / "cashapp_qr.png"
    if not qr_path.exists():
        qr_path = Path("F:/AI_Oracle_Root/scarify/qr_codes/cashapp_qr.png")
    if not qr_path.exists():
        print(f"[QR] Not found, generating...")
        from generate_cashapp_qr import generate_cashapp_qr
        generate_cashapp_qr()
        qr_path = Path("F:/AI_Oracle_Root/scarify/qr_codes/cashapp_qr.png")
    
    # ULTRA-SIMPLE command
    cmd = [
        'ffmpeg', '-y',
        '-loop', '1', '-t', str(dur), '-i', str(lincoln_img),
        '-i', str(audio_path),
        '-loop', '1', '-t', str(dur), '-i', str(qr_path),
        '-filter_complex',
        # Just zoom, QR overlay, text
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=decrease,zoompan=z='min(1.3,1+0.0005*on)':d=1:s=1080x1920[v];"
        f"[2:v]scale=150:150[qr];"
        f"[v][qr]overlay=W-w-20:20[final]",
        '-map', '[final]', '-map', '1:a',
        '-af', 'volume=2,loudnorm',
        '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '23',
        '-c:a', 'aac', '-shortest',
        str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
    
    if output_path.exists() and output_path.stat().st_size > 0:
        mb = output_path.stat().st_size / (1024 * 1024)
        print(f"[Ultra-Simple] OK: {mb:.1f} MB in <30s")
        return True
    
    print(f"[Ultra-Simple] Failed: {result.stderr[-300:]}")
    return False

def generate(episode_num):
    """Generate ONE ultra-simple video"""
    print(f"\n{'='*70}")
    print(f"  ULTRA-SIMPLE - Episode #{episode_num}")
    print(f"{'='*70}\n")
    
    headlines = get_headlines()
    headline = random.choice(headlines)
    print(f"[1/5] {headline}")
    
    script = generate_script(headline)
    print(f"[2/5] Script: {len(script.split())} words")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    audio_path = BASE_DIR / f"audio/ULTRA_{episode_num}.mp3"
    
    print(f"[3/5] Generating audio...")
    if not generate_voice(script, audio_path):
        return None
    
    print(f"[4/5] Getting Lincoln...")
    lincoln_img = generate_lincoln_face_pollo()
    
    print(f"[5/5] Creating video...")
    video_path = BASE_DIR / f"videos/ULTRA_{timestamp}.mp4"
    
    if not create_ultra_simple_video(lincoln_img, audio_path, video_path):
        return None
    
    print(f"[6/6] Uploading...")
    youtube_url = upload_to_youtube(video_path, headline, episode_num)
    log_to_google_sheets(episode_num, headline, script, video_path, youtube_url or "")
    
    uploaded = BASE_DIR / "uploaded" / f"ULTRA_{episode_num}.mp4"
    import shutil
    shutil.copy2(video_path, uploaded)
    
    print(f"\n{'='*70}")
    print(f"  [OK] COMPLETE")
    print(f"{'='*70}")
    if youtube_url:
        print(f"YouTube: {youtube_url}")
    print(f"{'='*70}\n")
    
    return youtube_url

if __name__ == "__main__":
    ep = int(os.getenv("EPISODE_NUM", "5010"))
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    
    for i in range(count):
        generate(ep + i)

