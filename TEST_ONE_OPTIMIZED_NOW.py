#!/usr/bin/env python3
"""
TEST_ONE_OPTIMIZED_NOW.py
Generate 1 FULLY OPTIMIZED video with ALL features for quality check
"""

import sys
from pathlib import Path
from datetime import datetime

# Add to path
sys.path.insert(0, str(Path.cwd()))

from abraham_MAX_HEADROOM import (
    generate_voice, generate_lincoln_face_pollo, 
    create_max_headroom_video, upload_to_youtube,
    get_headlines, BASE_DIR
)
from FEAR_OPTIMIZED_SCRIPTS import get_unique_script
from YOUTUBE_TAG_OPTIMIZATION import generate_optimized_tags

def main():
    print("\n" + "="*80)
    print("  GENERATING 1 FULLY OPTIMIZED VIDEO - QUALITY TEST")
    print("="*80 + "\n")
    
    # Get headline
    headlines = get_headlines()
    if not headlines:
        print("[!] Failed to get headlines")
        return
    
    headline = headlines[0]
    print(f"[1/6] Headline: {headline}\n")
    
    # Get fear-optimized script
    used_hashes = set()
    script, script_hash = get_unique_script(used_hashes)
    print(f"[2/6] Fear-optimized script generated")
    print(f"      {script[:100]}...\n")
    
    # Generate voice with binaural beats
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    audio_path = BASE_DIR / 'audio' / f'TEST_OPTIMIZED_{timestamp}.mp3'
    audio_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"[3/6] Generating voice with psychological audio...")
    print(f"      - Binaural beats: 200Hz L / 208Hz R = 8Hz theta")
    print(f"      - Theta waves: 6Hz")
    print(f"      - Gamma spikes: 40Hz")
    print(f"      - Subliminal: 17Hz")
    
    if not generate_voice(script, audio_path):
        print("[!] Voice generation failed")
        return
    
    print(f"      [OK] Voice + psychological audio ready\n")
    
    # Get Lincoln image
    print(f"[4/6] Getting Lincoln image...")
    lincoln = generate_lincoln_face_pollo()
    if not lincoln:
        print("[!] Failed to get Lincoln image")
        return
    print(f"      [OK] {lincoln}\n")
    
    # Create video with ALL effects
    print(f"[5/6] Creating video with ALL features:")
    print(f"      - Max Headroom glitch effects")
    print(f"      - VHS aesthetic (scan lines, RGB split)")
    print(f"      - Lip sync")
    print(f"      - Jumpscare")
    print(f"      - Cash App QR code")
    print(f"      - Binaural beats mixed in audio")
    
    video_out = BASE_DIR / 'uploaded' / f'TEST_OPTIMIZED_{timestamp}.mp4'
    video_out.parent.mkdir(parents=True, exist_ok=True)
    
    video = create_max_headroom_video(
        lincoln_image=lincoln,
        audio_path=audio_path,
        output_path=video_out,
        headline=headline,
        use_lipsync=True,
        use_jumpscare=True
    )
    
    if not video:
        print("      [!] Video creation failed")
        return
    
    size_mb = Path(video).stat().st_size / (1024*1024)
    print(f"      [OK] Video created: {Path(video).name} ({size_mb:.1f}MB)\n")
    
    # Generate optimized tags
    print(f"[6/6] Generating 24 optimized YouTube tags...")
    tags = generate_optimized_tags(headline, script)
    print(f"      [OK] Tags: {', '.join(tags[:5])}... (+{len(tags)-5} more)\n")
    
    # Upload to YouTube
    print(f"[UPLOAD] Uploading to YouTube with:")
    print(f"         - Title: Lincoln's WARNING - {headline[:40]}...")
    print(f"         - 24 optimized tags")
    print(f"         - Category: Entertainment")
    print(f"         - Privacy: Public")
    
    episode = 99999  # Test episode number
    url = upload_to_youtube(Path(video), headline, episode)
    
    print("\n" + "="*80)
    print("  QUALITY TEST COMPLETE!")
    print("="*80 + "\n")
    
    if url:
        print(f"✅ YouTube URL: {url}")
        print(f"\nCheck this video for:")
        print(f"  1. Visual quality (Max Headroom effects, VHS aesthetic)")
        print(f"  2. Audio quality (voice clear, binaural undertones present)")
        print(f"  3. QR code visible")
        print(f"  4. Tags showing in YouTube Studio (24 tags)")
        print(f"  5. Overall engagement factor (would you stop scrolling?)")
    else:
        print(f"❌ Upload failed - check output above")
        print(f"\nBut video is saved locally: {video}")
        print(f"You can manually upload to test quality")
    
    print(f"\n" + "="*80)
    print(f"Video file: {video}")
    print(f"Ready for mass generation? This is the quality level.")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()

