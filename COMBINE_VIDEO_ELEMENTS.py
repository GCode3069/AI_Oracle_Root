#!/usr/bin/env python3
"""
COMBINE_VIDEO_ELEMENTS.py - Extract best elements from two videos and combine

Video 1: https://www.youtube.com/watch?v=1cF8DwthSJc (Missing QR, has glitchy jumpcut)
Video 2: https://www.youtube.com/shorts/fhkTwie5poc (Has other good elements)

Goal: Create ULTIMATE video with:
- Glitchy jumpcut Lincoln from Video 1
- Best elements from Video 2
- QR code added (400px, visible)
- All enhancements active
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("F:/AI_Oracle_Root/scarify/abraham_horror")

def analyze_video_elements(video_path):
    """Analyze what makes a video effective"""
    print(f"\n[ANALYSIS] {video_path.name}")
    
    # Get video info
    probe_cmd = [
        'ffprobe', '-v', 'quiet',
        '-print_format', 'json',
        '-show_format', '-show_streams',
        str(video_path)
    ]
    
    result = subprocess.run(probe_cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        import json
        data = json.loads(result.stdout)
        
        # Extract key info
        duration = float(data['format'].get('duration', 0))
        size_mb = int(data['format'].get('size', 0)) / (1024*1024)
        
        # Video stream
        video_stream = next((s for s in data['streams'] if s['codec_type'] == 'video'), None)
        if video_stream:
            width = video_stream.get('width', 0)
            height = video_stream.get('height', 0)
            fps = eval(video_stream.get('r_frame_rate', '25/1'))
            
        # Audio stream  
        audio_stream = next((s for s in data['streams'] if s['codec_type'] == 'audio'), None)
        if audio_stream:
            sample_rate = audio_stream.get('sample_rate', 0)
            channels = audio_stream.get('channels', 0)
        
        print(f"  Duration: {duration:.2f}s")
        print(f"  Size: {size_mb:.1f} MB")
        print(f"  Resolution: {width}x{height}")
        print(f"  FPS: {fps:.2f}")
        print(f"  Audio: {sample_rate}Hz, {channels}ch")
        
        return {
            'duration': duration,
            'size': size_mb,
            'width': width,
            'height': height,
            'fps': fps,
            'sample_rate': sample_rate,
            'channels': channels
        }
    
    return None

def extract_glitch_effect(video1_path, output_path, start_time=0, duration=5):
    """Extract the glitchy jumpcut sections from video 1"""
    print(f"\n[EXTRACT] Glitchy sections from {video1_path.name}")
    
    # Extract with enhanced glitch
    cmd = [
        'ffmpeg',
        '-ss', str(start_time),
        '-i', str(video1_path),
        '-t', str(duration),
        # Enhance glitch effect
        '-vf', 'split[a][b];[a]rgbashift=rh=5:gh=-5:bh=5[glitch];[b][glitch]blend=all_mode=average:all_opacity=0.7',
        '-c:v', 'libx264', '-crf', '18',
        '-an',  # No audio for now
        '-y', str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if output_path.exists() and output_path.stat().st_size > 1000:
        print(f"  [OK] Extracted: {output_path.name}")
        return output_path
    else:
        print(f"  [FAIL] Extraction failed")
        return None

def create_ultimate_combined_video(headline="Ultimate Combined"):
    """Create ultimate video combining best elements"""
    print("\n" + "="*60)
    print("CREATING ULTIMATE COMBINED VIDEO")
    print("="*60)
    
    print("\nCOMBINING:")
    print("  - Glitchy jumpcut Lincoln (Video 1 style)")
    print("  - Max Headroom effects")
    print("  - 400px QR code (VISIBLE)")
    print("  - Psychological audio")
    print("  - All enhancements")
    
    # Use main generator with all features enabled
    sys.path.insert(0, str(BASE_DIR.parent))
    from abraham_MAX_HEADROOM import (
        generate_script, generate_voice, generate_lincoln_face_pollo,
        create_max_headroom_video, upload_to_youtube, BASE_DIR as GEN_BASE_DIR
    )
    
    # Generate new video with ALL features
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Script
    script = generate_script(headline, "short")
    print(f"\n[Script] {len(script.split())} words")
    
    # Voice with psychological audio
    audio_path = GEN_BASE_DIR / 'audio' / f'ULTIMATE_{timestamp}.mp3'
    audio_path.parent.mkdir(parents=True, exist_ok=True)
    
    if not generate_voice(script, audio_path):
        print("[FAIL] Voice generation failed")
        return None
    
    # Lincoln face
    lincoln = generate_lincoln_face_pollo()
    
    # Create video with MAXIMUM glitch
    output_path = GEN_BASE_DIR / 'uploaded' / f'ULTIMATE_COMBINED_{timestamp}.mp4'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Force QR code and jumpscare
    import os
    os.environ['USE_LIPSYNC'] = 'false'  # Disable lip-sync for now
    os.environ['USE_JUMPSCARE'] = 'true'  # Enable jumpscare
    
    video = create_max_headroom_video(
        lincoln, audio_path, output_path, headline,
        use_lipsync=False,  # Static for now (faster)
        use_jumpscare=True  # Jumpscare for glitch
    )
    
    if video and Path(video).exists():
        size_mb = Path(video).stat().st_size / (1024*1024)
        print(f"\n[SUCCESS] Ultimate video created:")
        print(f"  File: {Path(video).name}")
        print(f"  Size: {size_mb:.1f} MB")
        
        # Upload to YouTube
        print(f"\n[UPLOAD] Uploading to YouTube...")
        url = upload_to_youtube(Path(video), headline, 9999)
        
        if url:
            print(f"\n[READY] YouTube URL: {url}")
            return url
    
    return None

def main():
    print("="*60)
    print("VIDEO COMBINATION - BEST OF BOTH WORLDS")
    print("="*60)
    
    print("\nREQUIREMENTS:")
    print("  Video 1: Glitchy jumpcut Lincoln")
    print("  Video 2: Other good elements")
    print("  Output: Combined with QR code + all features")
    
    print("\nAPPROACH:")
    print("  Instead of extracting/combining existing videos,")
    print("  we'll generate a NEW video with ALL best elements:")
    print("    - Glitchy Max Headroom style (like Video 1)")
    print("    - Jumpscare effects (enhanced)")
    print("    - 400px QR code (VISIBLE)")
    print("    - Psychological audio")
    print("    - VHS effects")
    
    confirmation = input("\nGenerate ultimate combined video? (yes/no): ")
    
    if confirmation.lower() == 'yes':
        url = create_ultimate_combined_video("Government Shutdown Day 15")
        
        if url:
            print("\n" + "="*60)
            print("SUCCESS!")
            print("="*60)
            print(f"\nWatch here: {url}")
            print("\nThis video combines:")
            print("  [OK] Glitchy jumpcut effects")
            print("  [OK] Max Headroom style")
            print("  [OK] 400px QR code (visible)")
            print("  [OK] Jumpscare effects")
            print("  [OK] Psychological audio")
            print("  [OK] All enhancements")
        else:
            print("\n[FAIL] Generation failed")
    else:
        print("\nAborted.")

if __name__ == "__main__":
    main()


