#!/usr/bin/env python3
"""
REPLICATE 198.7% ENGAGEMENT SUCCESS
Generate videos matching Episode #5002's winning formula

Episode #5002 Stats:
- 198.7% engagement (watched 2x!)
- 42 seconds duration
- Strong dark comedy
- Full effects (that worked)
- Cash App QR visible

This generator creates 5 videos with same winning pattern
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
CASHAPP_QR = Path("F:/AI_Oracle_Root/scarify/qr_codes/cashapp_qr.png")

def create_198_style_video(lincoln_img, audio_path, output_path):
    """
    Create video matching Episode #5002 style
    40-45 second sweet spot, engaging effects
    """
    probe = subprocess.run([
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)
    ], capture_output=True, text=True, timeout=10)
    dur = float(probe.stdout.strip())
    
    # Create video with proven pattern
    cmd = [
        'ffmpeg', '-y',
        '-loop', '1', '-framerate', '30', '-t', str(dur), '-i', str(lincoln_img),
        '-i', str(audio_path),
        '-loop', '1', '-framerate', '30', '-t', str(dur), '-i', str(CASHAPP_QR),
        '-filter_complex',
        # Engaging zoom (like #5002)
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=decrease,setsar=1,"
        f"zoompan=z='min(1.4,1+0.0006*on)':d=1:s=1080x1920:fps=30,"
        # Dark contrast (engaging look)
        f"eq=contrast=1.6:brightness=0.05:saturation=1.4,"
        # Simple RGB split (visual interest)
        f"split[main][dup];[dup]geq=r='r(X+4,Y)':g='g(X,Y)':b='b(X-4,Y)',format=yuva420p,colorchannelmixer=aa=0.3[rgb];[main][rgb]overlay[vid];"
        # Cash App QR overlay
        f"[2:v]scale=180:180[qr];"
        f"[vid][qr]overlay=W-w-20:20[vout]",
        '-map', '[vout]', '-map', '1:a',
        # LOUD, punchy audio (like #5002)
        '-af', 'volume=3.0,loudnorm=I=-14:TP=-1:LRA=7,acompressor=threshold=-18dB:ratio=4',
        # YouTube-optimized encoding
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
        '-profile:v', 'high', '-level', '4.2',
        '-pix_fmt', 'yuv420p',
        '-movflags', '+faststart',  # Critical for no buffering!
        '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
        '-shortest',
        str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    
    if output_path.exists() and output_path.stat().st_size > 0:
        mb = output_path.stat().st_size / (1024 * 1024)
        print(f"[198-Style] Created: {mb:.1f} MB")
        return True
    
    print(f"[198-Style] Failed")
    return False

def generate_198_video(episode_num):
    """Generate one video in 198.7% engagement style"""
    print(f"\n{'='*70}")
    print(f"  198% ENGAGEMENT STYLE - Episode #{episode_num}")
    print(f"  (Replicating Episode #5002 success)")
    print(f"{'='*70}\n")
    
    # Get headline
    headlines = get_headlines()
    headline = random.choice(headlines)
    print(f"[1/5] Headline: {headline}")
    
    # Generate script (targeting 40-45s like #5002)
    script = generate_script(headline)
    words = len(script.split())
    print(f"[2/5] Script: {words} words (target: 45-55 for ~42s)")
    
    # Generate audio
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    audio_path = BASE_DIR / f"audio/SUCCESS198_{episode_num}.mp3"
    print(f"[3/5] Generating audio...")
    if not generate_voice(script, audio_path):
        return None
    
    # Get Lincoln
    print(f"[4/5] Getting Lincoln image...")
    lincoln_img = generate_lincoln_face_pollo()
    
    # Create video
    print(f"[5/5] Creating video (198% style)...")
    video_path = BASE_DIR / f"videos/SUCCESS198_{timestamp}.mp4"
    
    if not create_198_style_video(lincoln_img, audio_path, video_path):
        return None
    
    # Upload
    print(f"[6/6] Uploading to YouTube...")
    youtube_url = upload_to_youtube(video_path, headline, episode_num)
    log_to_google_sheets(episode_num, headline, script, video_path, youtube_url or "")
    
    # Copy to uploaded
    uploaded = BASE_DIR / "uploaded" / f"SUCCESS198_{episode_num}.mp4"
    import shutil
    shutil.copy2(video_path, uploaded)
    
    print(f"\n{'='*70}")
    print(f"  [OK] 198% STYLE VIDEO COMPLETE")
    print(f"{'='*70}")
    print(f"Episode: #{episode_num}")
    if youtube_url:
        print(f"YouTube: {youtube_url}")
    print(f"Expected: 180-200% engagement (like #5002)")
    print(f"{'='*70}\n")
    
    return youtube_url

if __name__ == "__main__":
    print("\n" + "="*70)
    print("REPLICATING 198.7% ENGAGEMENT SUCCESS")
    print("Episode #5002 Formula")
    print("="*70)
    
    ep_start = int(os.getenv("EPISODE_NUM", "8000"))
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    
    results = []
    for i in range(count):
        url = generate_198_video(ep_start + i)
        if url:
            results.append(url)
        
        # Wait between uploads
        if i < count - 1:
            print(f"\n[Waiting 20 seconds before next video...]\n")
            import time
            time.sleep(20)
    
    print("\n" + "="*70)
    print(f"BATCH COMPLETE: {len(results)}/{count} VIDEOS UPLOADED")
    print("="*70)
    
    if results:
        print("\nYour new videos (wait 5-10 min for processing):")
        for i, url in enumerate(results, 1):
            print(f"  {i}. {url}")
        
        print("\nExpected performance (based on #5002):")
        print("  - Engagement: 180-200%")
        print("  - Avg duration: 1:00-1:30 (on ~42s video)")
        print("  - People will watch 2x!")
        
        print("\nAll have:")
        print("  - Cash App QR (top-right)")
        print("  - Dark satirical comedy")
        print("  - NO comedian names")
        print("  - NO Bitcoin recitation")
        print("  - Faststart flag (no buffering)")
    
    print("="*70)



