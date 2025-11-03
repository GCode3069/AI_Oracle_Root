#!/usr/bin/env python3
"""
FAST GENERATOR - SIMPLIFIED FOR SPEED
No lip-sync, simpler effects, NO TIMEOUTS
Generates in <60s GUARANTEED

For speed priority over maximum effects
"""
import os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from abraham_MAX_HEADROOM import (
    generate_script,
    generate_voice,
    generate_lincoln_face_pollo,
    upload_to_youtube,
    get_headlines,
    log_to_google_sheets,
    generate_bitcoin_qr,
    BITCOIN_ADDRESS,
    CASHAPP_LINK
)
import subprocess, random
from datetime import datetime

BASE_DIR = Path("F:/AI_Oracle_Root/scarify/abraham_horror")

def create_fast_video(lincoln_image, audio_path, output_path, headline):
    """
    FAST video creation - simplified effects, NO TIMEOUTS
    Target: <60 seconds processing
    """
    print(f"[Fast] Creating video (simplified, fast)...")
    
    # Get audio duration
    probe = subprocess.run([
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)
    ], capture_output=True, text=True)
    duration = float(probe.stdout.strip())
    
    # Get QR code
    qr_path = BASE_DIR / "qr_codes" / "cashapp_qr.png"
    if not qr_path.exists():
        qr_path = generate_bitcoin_qr()
    
    # SIMPLIFIED FFmpeg - fewer effects, faster render
    cmd = [
        'ffmpeg', '-y',
        '-loop', '1', '-t', str(duration), '-i', str(lincoln_image),
        '-i', str(audio_path),
        '-loop', '1', '-t', str(duration), '-i', str(qr_path),
        '-filter_complex',
        f"[0:v]scale=900:900:force_original_aspect_ratio=decrease,zoompan=z='1.0+0.3*on/({duration}*30)':d=1:x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):s=1080x1920[face];"
        f"[face]eq=contrast=1.8:brightness=0.1:saturation=1.5[face_eq];"
        f"[face_eq]geq=r='r(X+3,Y)':g='g(X,Y)':b='b(X-3,Y)'[rgb];"  # Simple RGB split
        f"[rgb]drawtext=text='ABRAHAM LINCOLN':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=30[title];"
        f"[2:v]scale=150:150[qr];"
        f"[title][qr]overlay=W-w-20:20[final]",
        '-map', '[final]',
        '-map', '1:a',
        '-af', 'volume=2.5,loudnorm=I=-14:TP=-1:LRA=7',
        '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '22',
        '-c:a', 'aac', '-b:a', '192k',
        '-shortest',
        str(output_path)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if output_path.exists() and output_path.stat().st_size > 0:
            mb = output_path.stat().st_size / (1024 * 1024)
            print(f"[Fast] OK: {mb:.1f} MB")
            return True
        else:
            print(f"[Fast] Failed")
            if result.stderr:
                print(f"[Debug] {result.stderr[:500]}")
            return False
    except subprocess.TimeoutExpired:
        print(f"[Fast] Even simplified version timed out!")
        return False
    except Exception as e:
        print(f"[Fast] Error: {e}")
        return False

def generate_fast_video(episode_num):
    """Generate video FAST - under 60s total"""
    print(f"\n{'='*70}")
    print(f"  FAST GENERATOR - Episode #{episode_num}")
    print(f"  (Simplified effects for SPEED)")
    print(f"{'='*70}\n")
    
    # Get headline
    headlines = get_headlines()
    headline = random.choice(headlines)
    print(f"[1/5] Headline: {headline}")
    
    # Generate script
    script = generate_script(headline)
    print(f"[2/5] Script: {len(script.split())} words")
    
    # Generate audio
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    audio_path = BASE_DIR / f"audio/FAST_{episode_num}.mp3"
    print(f"[3/5] Generating audio...")
    if not generate_voice(script, audio_path):
        return None
    
    # Get Lincoln image
    print(f"[4/5] Getting Lincoln image...")
    lincoln_image = generate_lincoln_face_pollo()
    
    # Create video FAST
    print(f"[5/5] Creating video (fast mode)...")
    video_path = BASE_DIR / f"videos/FAST_{timestamp}.mp4"
    
    if not create_fast_video(lincoln_image, audio_path, video_path, headline):
        return None
    
    # Upload
    print(f"[6/6] Uploading to YouTube...")
    youtube_url = upload_to_youtube(video_path, headline, episode_num)
    
    # Track
    log_to_google_sheets(episode_num, headline, script, video_path, youtube_url or "")
    
    # Copy to uploaded
    uploaded_path = BASE_DIR / "uploaded" / f"FAST_{episode_num}.mp4"
    import shutil
    shutil.copy2(video_path, uploaded_path)
    
    print(f"\n{'='*70}")
    print(f"  [OK] FAST VIDEO COMPLETE")
    print(f"{'='*70}")
    print(f"File: {uploaded_path.name}")
    if youtube_url:
        print(f"YouTube: {youtube_url}")
    print(f"{'='*70}\n")
    
    return str(uploaded_path)

if __name__ == "__main__":
    start_ep = int(os.getenv("EPISODE_NUM", "5010"))
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    
    for i in range(count):
        generate_fast_video(start_ep + i)

