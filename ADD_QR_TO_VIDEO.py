#!/usr/bin/env python3
"""
ADD QR CODE TO VIDEO - Match Video 2 Style
Adds Bitcoin/CashApp QR code overlay to videos that are missing it

Usage: python ADD_QR_TO_VIDEO.py "video_file.mp4"
"""

import sys
from pathlib import Path
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
import qrcode
from PIL import Image, ImageDraw, ImageFont
import subprocess

# Configuration
PROJECT_ROOT = Path("F:/AI_Oracle_Root/scarify")
QR_DIR = PROJECT_ROOT / "qr_codes"
QR_DIR.mkdir(exist_ok=True)

# Bitcoin address for QR code
BTC_ADDRESS = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"
CASHAPP_LINK = "https://cash.app/$healthiwealthi"

def generate_video_qr_styled(style="video2"):
    """
    Generate QR code matching Video 2's style
    
    Video 2 style:
    - White QR code on black/dark background
    - Small size (200-300px)
    - Top-right or bottom-right corner
    - High contrast for visibility
    """
    print(f"\nGenerating QR code (Video 2 style)...")
    
    # Create QR code - high error correction for video compression
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=2,
    )
    
    # Add Bitcoin address
    qr.add_data(f"bitcoin:{BTC_ADDRESS}")
    qr.make(fit=True)
    
    # Create QR image - WHITE on BLACK (Video 2 style)
    qr_img = qr.make_image(
        fill_color="white",      # White QR pattern
        back_color="black"       # Black background
    )
    
    # Resize to 250x250 (good size for corner overlay)
    qr_img = qr_img.resize((250, 250), Image.Resampling.LANCZOS)
    
    # Add subtle border/frame for better visibility
    canvas_size = 270  # 250 + 10px border on each side
    canvas = Image.new('RGBA', (canvas_size, canvas_size), (0, 0, 0, 200))  # Semi-transparent black
    canvas.paste(qr_img, (10, 10))
    
    # Add small text label (optional)
    try:
        draw = ImageDraw.Draw(canvas)
        font = ImageFont.truetype("arial.ttf", 16)
        text = "SUPPORT"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        draw.text(((canvas_size - text_width) // 2, 5), text, fill="white", font=font)
    except:
        pass  # Font optional
    
    # Save
    output_path = QR_DIR / "video2_style_qr.png"
    canvas.save(output_path, "PNG")
    
    print(f"   [OK] QR code generated: {output_path}")
    print(f"   [OK] Size: {canvas_size}x{canvas_size}px")
    print(f"   [OK] Style: White on black (Video 2 match)")
    print(f"   [OK] Address: {BTC_ADDRESS[:20]}...")
    
    return output_path

def add_qr_to_video(input_video, output_video=None, position="bottom-right"):
    """
    Add QR code overlay to video matching Video 2 style
    
    Args:
        input_video: Path to input video (Video 1)
        output_video: Path to save output (auto-generated if None)
        position: Where to place QR ("top-right", "bottom-right", "bottom-left", "top-left")
    """
    print(f"\n{'='*70}")
    print(f"🎬 ADDING QR CODE TO VIDEO")
    print(f"{'='*70}\n")
    
    input_path = Path(input_video)
    if not input_path.exists():
        print(f"❌ Error: Video not found: {input_video}")
        return None
    
    # Generate output filename if not provided
    if output_video is None:
        output_video = input_path.parent / f"{input_path.stem}_with_qr{input_path.suffix}"
    
    print(f"📥 Input:  {input_path.name}")
    print(f"📤 Output: {Path(output_video).name}")
    print(f"📍 Position: {position}")
    
    try:
        # Generate QR code
        qr_path = generate_video_qr_styled()
        
        # Load video
        print(f"\n🎥 Loading video...")
        video = VideoFileClip(str(input_path))
        print(f"   ✅ Duration: {video.duration:.1f}s")
        print(f"   ✅ Size: {video.size}")
        print(f"   ✅ FPS: {video.fps}")
        
        # Load QR code as image clip
        qr_clip = ImageClip(str(qr_path))
        qr_clip = qr_clip.set_duration(video.duration)
        
        # Position QR code
        qr_size = 270  # QR image size
        margin = 20    # Margin from edge
        
        positions = {
            "top-right": (video.w - qr_size - margin, margin),
            "bottom-right": (video.w - qr_size - margin, video.h - qr_size - margin),
            "top-left": (margin, margin),
            "bottom-left": (margin, video.h - qr_size - margin)
        }
        
        qr_position = positions.get(position, positions["bottom-right"])
        qr_clip = qr_clip.set_position(qr_position)
        
        print(f"\n🎨 Compositing QR code...")
        print(f"   📍 Position: {position} at ({qr_position[0]}, {qr_position[1]})")
        
        # Composite video with QR overlay
        final_video = CompositeVideoClip([video, qr_clip])
        
        # Write output
        print(f"\n💾 Rendering video...")
        print(f"   (This may take a few minutes...)")
        
        final_video.write_videofile(
            str(output_video),
            codec='libx264',
            audio_codec='aac',
            fps=video.fps,
            preset='medium',
            bitrate='5000k',
            logger=None  # Suppress moviepy progress
        )
        
        # Cleanup
        video.close()
        final_video.close()
        
        print(f"\n{'='*70}")
        print(f"✅ SUCCESS! QR CODE ADDED!")
        print(f"{'='*70}\n")
        print(f"📹 Original: {input_path}")
        print(f"📹 Updated:  {output_video}")
        print(f"\n💡 Next steps:")
        print(f"   1. Preview the video to verify QR placement")
        print(f"   2. Scan QR with phone to test functionality")
        print(f"   3. Upload to YouTube if satisfied")
        print(f"   4. Delete original if you want to replace it")
        print(f"\n{'='*70}\n")
        
        return output_video
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def batch_add_qr(video_dir, output_dir=None):
    """Add QR code to all videos in directory"""
    print(f"\n{'='*70}")
    print(f"📁 BATCH QR CODE ADDITION")
    print(f"{'='*70}\n")
    
    video_dir = Path(video_dir)
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = video_dir / "with_qr"
        output_dir.mkdir(exist_ok=True)
    
    videos = list(video_dir.glob("*.mp4"))
    print(f"Found {len(videos)} videos in {video_dir}")
    
    results = []
    for i, video in enumerate(videos, 1):
        print(f"\n[{i}/{len(videos)}] Processing: {video.name}")
        
        output_path = output_dir / f"{video.stem}_qr.mp4"
        result = add_qr_to_video(str(video), str(output_path))
        
        if result:
            results.append(result)
            print(f"   ✅ Saved: {output_path.name}")
        else:
            print(f"   ❌ Failed: {video.name}")
    
    print(f"\n{'='*70}")
    print(f"✅ BATCH COMPLETE!")
    print(f"{'='*70}\n")
    print(f"Processed: {len(results)}/{len(videos)} videos")
    print(f"Output: {output_dir}")
    print(f"\n{'='*70}\n")
    
    return results

def main():
    """Main entry point"""
    print(f"\n{'='*70}")
    print(f"SCARIFY - QR CODE VIDEO FIXER")
    print(f"Add QR codes to videos matching Video 2 style")
    print(f"{'='*70}\n")
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Single video:  python ADD_QR_TO_VIDEO.py 'video.mp4'")
        print("  Batch mode:    python ADD_QR_TO_VIDEO.py 'video_folder/'")
        print("")
        print("Examples:")
        print("  python ADD_QR_TO_VIDEO.py \"Lincoln's DEEP DIVE_ Military Draft Return _ No. 23 USC Avoids Nebraska's U.mp4\"")
        print("  python ADD_QR_TO_VIDEO.py abraham_horror/youtube_ready/")
        print("")
        
        # Interactive mode
        video_path = input("Enter video file path (or press Enter to exit): ").strip('"')
        if not video_path:
            sys.exit(0)
    else:
        video_path = sys.argv[1].strip('"')
    
    video_path = Path(video_path)
    
    # Check if it's a directory (batch mode) or file (single mode)
    if video_path.is_dir():
        batch_add_qr(video_path)
    elif video_path.is_file():
        add_qr_to_video(str(video_path))
    else:
        print(f"❌ Error: Not found: {video_path}")
        sys.exit(1)

if __name__ == "__main__":
    main()

