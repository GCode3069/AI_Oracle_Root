#!/usr/bin/env python3
"""
Diagnose why YouTube video won't play
Check: Audio track, video track, codec, duration
"""
import subprocess
from pathlib import Path

def diagnose_video(video_path):
    """Check video file integrity"""
    print(f"\n{'='*70}")
    print(f"DIAGNOSING: {video_path.name}")
    print(f"{'='*70}\n")
    
    if not video_path.exists():
        print(f"[ERROR] File doesn't exist!")
        return
    
    # Check file size
    mb = video_path.stat().st_size / (1024 * 1024)
    print(f"[File Size] {mb:.2f} MB")
    
    # Check streams
    cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'stream=index,codec_name,codec_type,duration',
        '-of', 'json',
        str(video_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        import json
        data = json.loads(result.stdout)
        
        streams = data.get('streams', [])
        
        video_stream = None
        audio_stream = None
        
        for stream in streams:
            if stream['codec_type'] == 'video':
                video_stream = stream
            elif stream['codec_type'] == 'audio':
                audio_stream = stream
        
        print(f"[Video Stream]")
        if video_stream:
            print(f"  Codec: {video_stream.get('codec_name', 'Unknown')}")
            print(f"  Duration: {video_stream.get('duration', 'Unknown')}s")
            print(f"  Status: OK")
        else:
            print(f"  Status: MISSING!")
        
        print(f"\n[Audio Stream]")
        if audio_stream:
            print(f"  Codec: {audio_stream.get('codec_name', 'Unknown')}")
            print(f"  Duration: {audio_stream.get('duration', 'Unknown')}s")
            print(f"  Status: OK")
        else:
            print(f"  Status: MISSING! <-- THIS IS THE PROBLEM!")
        
        # Check for QR code in video
        print(f"\n[QR Code Check]")
        print(f"  Cannot detect visually without playing")
        print(f"  Recommendation: Play locally with VLC/ffplay")
        
        print(f"\n{'='*70}")
        print(f"DIAGNOSIS:")
        print(f"{'='*70}")
        
        if not audio_stream:
            print(f"[CRITICAL] NO AUDIO TRACK!")
            print(f"  This is why video won't play on YouTube")
            print(f"  Fix: Re-generate with proper audio mapping")
        
        if not video_stream:
            print(f"[CRITICAL] NO VIDEO TRACK!")
            print(f"  Complete corruption")
        
        if video_stream and audio_stream:
            print(f"[OK] Video has both tracks")
            print(f"  Issue may be:")
            print(f"    - Codec compatibility")
            print(f"    - Duration mismatch")
            print(f"    - YouTube processing delay")
        
        print(f"{'='*70}")
    
    else:
        print(f"[ERROR] ffprobe failed: {result.stderr}")

if __name__ == "__main__":
    import sys
    
    # Check latest uploaded videos
    uploaded_dir = Path("F:/AI_Oracle_Root/scarify/abraham_horror/uploaded")
    
    videos = sorted(uploaded_dir.glob("ULTRA_*.mp4"), key=lambda x: x.stat().st_mtime, reverse=True)[:5]
    
    for video in videos:
        diagnose_video(video)

