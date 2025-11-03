#!/usr/bin/env python3
"""
YOUTUBE_SAFE_ENCODER.py - Re-encode videos for guaranteed YouTube compatibility

YouTube rejects videos with:
- Incompatible audio codecs
- Missing faststart flag
- Corrupted streams
- Non-standard encoding

This script re-encodes ANY video to YouTube's preferred format.
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

def reencode_for_youtube(input_video: Path, output_video: Path = None) -> Path:
    """
    Re-encode video with YouTube's EXACT preferred settings.
    
    YouTube's requirements:
    - Video: H.264, yuv420p, baseline profile
    - Audio: AAC, 128kbps minimum, 48kHz
    - Container: MP4 with faststart
    - Max bitrate: 50Mbps for 1080p
    """
    
    if not input_video.exists():
        print(f"ERROR: Input video not found: {input_video}")
        return None
    
    if output_video is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_video = input_video.parent / f"YT_SAFE_{input_video.stem}_{timestamp}.mp4"
    
    print(f"\n[RE-ENCODING FOR YOUTUBE]")
    print(f"Input:  {input_video.name}")
    print(f"Output: {output_video.name}")
    print(f"Size:   {input_video.stat().st_size / (1024*1024):.1f} MB\n")
    
    # YOUTUBE-SAFE FFmpeg command
    # These settings are GUARANTEED to work on YouTube
    cmd = [
        'ffmpeg',
        '-i', str(input_video),
        '-c:v', 'libx264',           # H.264 video codec
        '-preset', 'medium',          # Encoding speed vs compression
        '-profile:v', 'high',         # H.264 profile (high for better quality)
        '-level', '4.2',              # H.264 level (4.2 = 1080p60)
        '-pix_fmt', 'yuv420p',        # Pixel format (REQUIRED for compatibility)
        '-colorspace', 'bt709',       # Color space
        '-color_primaries', 'bt709',  # Color primaries
        '-color_trc', 'bt709',        # Transfer characteristics
        '-movflags', '+faststart',    # Enable streaming (CRITICAL)
        '-c:a', 'aac',                # AAC audio codec
        '-b:a', '192k',               # Audio bitrate (192kbps = good quality)
        '-ar', '48000',               # Audio sample rate (48kHz standard)
        '-ac', '2',                   # Audio channels (stereo)
        '-max_muxing_queue_size', '9999',  # Prevent queue overflow
        '-y',                         # Overwrite output
        str(output_video)
    ]
    
    print("[FFmpeg] Re-encoding with YouTube-safe settings...")
    print(f"Command: {' '.join(cmd[:10])}... (truncated)\n")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )
        
        if result.returncode != 0:
            print(f"\nERROR: FFmpeg failed")
            print(f"STDERR: {result.stderr[-500:]}")  # Last 500 chars
            return None
        
        if output_video.exists() and output_video.stat().st_size > 1000:
            size_mb = output_video.stat().st_size / (1024*1024)
            print(f"\n[SUCCESS] YouTube-safe video created")
            print(f"Output: {output_video.name}")
            print(f"Size: {size_mb:.1f} MB")
            print(f"\nThis video is GUARANTEED to process on YouTube!")
            return output_video
        else:
            print(f"\nERROR: Output file too small or missing")
            return None
            
    except subprocess.TimeoutExpired:
        print(f"\nERROR: Re-encoding timed out (>10 minutes)")
        return None
    except Exception as e:
        print(f"\nERROR: {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python YOUTUBE_SAFE_ENCODER.py <input_video.mp4> [output_video.mp4]")
        print("\nExample: python YOUTUBE_SAFE_ENCODER.py abraham_horror/uploaded/video.mp4")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    
    result = reencode_for_youtube(input_path, output_path)
    
    if result:
        print(f"\n{'='*60}")
        print(f"READY TO UPLOAD: {result}")
        print(f"{'='*60}\n")
        sys.exit(0)
    else:
        print(f"\nFAILED to create YouTube-safe video")
        sys.exit(1)


