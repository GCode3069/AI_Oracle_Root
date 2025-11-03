#!/usr/bin/env python3
"""
CLEAN_UP_MESSY_VISUALS.py - Fix "looks a mess" issue

Current problem:
- Too many visual elements competing
- PIP windows too cluttered
- Glitch effects too intense
- Overall chaotic, not stylish

Solution:
- Simplify to 1 main screen only (or 1 main + 1 small PIP max)
- Reduce glitch intensity
- Clean up composition
- Keep Max Headroom vibe but make it CLEAN
"""

import subprocess
from pathlib import Path

def create_clean_max_headroom(lincoln_image, audio_path, output_path, qr_path=None):
    """
    Create CLEAN Max Headroom video (not messy)
    
    Single main screen with:
    - Lincoln face (prominent, centered)
    - Subtle glitch (not overwhelming)
    - Clean scan lines
    - QR code (visible but not intrusive)
    - Professional composition
    """
    
    print("[Clean Max Headroom] Creating professional glitchy broadcast...")
    
    # Get audio duration
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)],
            capture_output=True, text=True
        )
        duration = float(result.stdout.strip())
    except:
        duration = 30
    
    # CLEAN filter chain - simpler, professional
    filter_chain = [
        # Base: Scale and pad Lincoln
        "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease",
        "pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black",
        
        # Subtle glitch (not overwhelming)
        "noise=alls=3:allf=t",  # Very light noise
        
        # Clean scan lines
        "split[a][b]",
        "[b]geq=lum='p(X,Y)':cb=128:cr=128,drawgrid=width=iw:height=2:t=1:c=black@0.1[scanlines]",
        "[a][scanlines]overlay",
        
        # Subtle RGB shift (not extreme)
        "split[orig][shift]",
        "[shift]rgbashift=rh=2:gh=-2:bh=2[rgb]",
        "[orig][rgb]blend=all_mode=screen:all_opacity=0.3",
        
        # Cyan tint (Max Headroom signature, but clean)
        "eq=contrast=1.3:saturation=1.2,colorbalance=rm=-0.1:gm=0.05:bm=0.1",
        
        # Slight vignette (focus on center)
        "vignette=angle=PI/4:mode=forward",
        
        # Output
        "format=yuv420p[vbase]"
    ]
    
    # Join filter
    vf = ','.join(filter_chain)
    
    # Build FFmpeg command
    ffmpeg_inputs = [
        'ffmpeg',
        '-loop', '1', '-t', str(duration), '-i', str(lincoln_image),
        '-i', str(audio_path)
    ]
    
    # Add QR if available
    if qr_path and qr_path.exists():
        ffmpeg_inputs.extend(['-loop', '1', '-t', str(duration), '-i', str(qr_path)])
        # Add QR overlay to clean filter
        vf += ",[2:v]scale=400:400[qr],[vbase][qr]overlay=W-420:20[vfinal]"
        map_video = '[vfinal]'
    else:
        map_video = '[vbase]'
    
    cmd = ffmpeg_inputs + [
        '-filter_complex', vf,
        '-map', map_video,
        '-map', '1:a:0',
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '20',
        '-profile:v', 'high',
        '-level', '4.2',
        '-pix_fmt', 'yuv420p',
        '-colorspace', 'bt709',
        '-color_primaries', 'bt709',
        '-color_trc', 'bt709',
        '-movflags', '+faststart',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-ar', '48000',
        '-shortest',
        '-y', str(output_path)
    ]
    
    print("[FFmpeg] Rendering CLEAN composition...")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        if result.returncode != 0:
            print(f"[Error] {result.stderr[-500:]}")
            return None
        
        if output_path.exists() and output_path.stat().st_size > 1000:
            size_mb = output_path.stat().st_size / (1024*1024)
            print(f"[Success] Clean Max Headroom: {size_mb:.1f} MB")
            print(f"  - Single main screen (not messy)")
            print(f"  - Subtle glitch (not overwhelming)")
            print(f"  - Professional composition")
            return output_path
    except Exception as e:
        print(f"[Error] {e}")
    
    return None

if __name__ == "__main__":
    print("""
CLEAN MAX HEADROOM vs MESSY PIP

MESSY (Current):
  - 3 screens competing for attention
  - RGB glitch strip at bottom
  - Too many effects
  - Chaotic, hard to watch

CLEAN (New):
  - 1 main screen (Lincoln prominent)
  - Subtle glitch effects
  - Clean scan lines
  - Professional composition
  - QR code visible but not intrusive
  
  Still Max Headroom aesthetic, but CLEAN not MESSY!
""")


