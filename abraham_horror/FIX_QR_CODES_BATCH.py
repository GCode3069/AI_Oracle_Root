"""
BATCH FIX QR CODES FOR EXISTING VIDEOS
Adds Bitcoin QR codes to videos missing them
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw
import qrcode

BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
BTC = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"

def create_bitcoin_qr(size=400):
    """Create high-quality Bitcoin QR code"""
    print("[QR] Generating Bitcoin QR code...")
    
    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=4,
    )
    qr.add_data(f"bitcoin:{BTC}")
    qr.make(fit=True)
    
    # Create QR image
    qr_img = qr.make_image(fill_color="white", back_color="black")
    qr_img = qr_img.resize((size, size), Image.NEAREST)
    
    # Add frame and text
    final = Image.new('RGB', (size, size+80), (0, 0, 0))
    final.paste(qr_img, (0, 0))
    
    draw = ImageDraw.Draw(final)
    draw.text((size//2, size+40), "SUPPORT TRUTH - SCAN FOR BITCOIN", 
              fill=(255, 255, 255), anchor="mm")
    
    qr_path = BASE / "temp" / "bitcoin_qr_overlay.png"
    qr_path.parent.mkdir(exist_ok=True, parents=True)
    final.save(qr_path)
    
    print(f"[QR] OK Created: {qr_path}")
    return str(qr_path)

def add_qr_to_video(video_path, qr_image_path, output_path=None):
    """Add QR code overlay to existing video using FFmpeg"""
    import subprocess
    
    if not output_path:
        output_path = video_path.parent / f"{video_path.stem}_QR{video_path.suffix}"
    
    print(f"[VIDEO] Adding QR to: {video_path.name}")
    
    # FFmpeg command to overlay QR code (bottom right corner)
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-i", str(qr_image_path),
        "-filter_complex",
        "[1:v]scale=300:-1[qr];[0:v][qr]overlay=W-w-20:H-h-20",
        "-c:a", "copy",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, timeout=300)
    
    if result.returncode == 0 and output_path.exists():
        print(f"[VIDEO] OK Created: {output_path.name}")
        return str(output_path)
    else:
        print(f"[VIDEO] FAILED: {result.stderr.decode()[:200]}")
        return None

def batch_fix_videos():
    """Fix all videos in uploaded/ folder"""
    print("\n" + "="*70)
    print("BATCH QR CODE FIX")
    print("="*70)
    
    # Create QR code
    qr_path = create_bitcoin_qr(400)
    
    # Find videos
    uploaded_dir = BASE / "uploaded"
    if not uploaded_dir.exists():
        print("[ERROR] No uploaded/ directory found!")
        return
    
    videos = list(uploaded_dir.glob("*.mp4"))
    print(f"\n[SCAN] Found {len(videos)} videos")
    
    # Process each video
    fixed_count = 0
    for video in videos:
        # Skip if already has _QR suffix
        if "_QR" in video.stem:
            print(f"[SKIP] Already has QR: {video.name}")
            continue
        
        output = add_qr_to_video(video, qr_path)
        if output:
            fixed_count += 1
    
    print("\n" + "="*70)
    print(f"✓ COMPLETE: Fixed {fixed_count}/{len(videos)} videos")
    print("="*70)
    print("\nℹ️  Original videos preserved")
    print("ℹ️  New videos have '_QR' suffix")
    print("\n📍 Location: abraham_horror/uploaded/")

if __name__ == "__main__":
    try:
        import qrcode
    except ImportError:
        print("[INSTALL] Installing qrcode library...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "qrcode[pil]"], capture_output=True)
    
    batch_fix_videos()

