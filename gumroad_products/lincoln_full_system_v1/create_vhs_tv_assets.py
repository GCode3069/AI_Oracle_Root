#!/usr/bin/env python3
"""
CREATE VHS TV BROADCAST ASSETS
Generates reusable overlays: TV frame, scanlines, static
Based on authentic VHS reference images
"""
import os
from pathlib import Path
from PIL import Image, ImageDraw

BASE_DIR = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
ASSETS_DIR = BASE_DIR / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

def create_tv_frame_overlay():
    """Create vintage CRT TV frame overlay (like reference Image 3)"""
    frame_path = ASSETS_DIR / "tv_frame_1080x1920.png"
    
    if frame_path.exists():
        print(f"[OK] TV frame already exists: {frame_path}")
        return frame_path
    
    print("[PROCESS] Creating TV frame overlay...")
    
    # Create TV frame with rounded corners and vignette
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Outer TV bezel (thick black border - authentic 1980s CRT)
    border_width = 60
    bezel_color = (20, 20, 20, 255)  # Dark brown/black (Bakelite TV casing)
    
    draw.rectangle([0, 0, 1080, border_width], fill=bezel_color)  # Top
    draw.rectangle([0, 1920-border_width, 1080, 1920], fill=bezel_color)  # Bottom
    draw.rectangle([0, 0, border_width, 1920], fill=bezel_color)  # Left
    draw.rectangle([1080-border_width, 0, 1080, 1920], fill=bezel_color)  # Right
    
    # CRT screen vignette (darker at edges - phosphor fade characteristic)
    vignette = Image.new("L", (1080, 1920), 255)
    for y in range(1920):
        for x in range(1080):
            # Distance from center (radial gradient)
            dx = (x - 540) / 540
            dy = (y - 960) / 960
            dist = (dx*dx + dy*dy) ** 0.5
            darkness = int(255 * max(0, 1 - dist * 0.4))
            vignette.putpixel((x, y), darkness)
    
    # Convert to RGBA and composite
    vignette_rgba = Image.new("RGBA", (1080, 1920))
    for y in range(1920):
        for x in range(1080):
            val = vignette.getpixel((x, y))
            vignette_rgba.putpixel((x, y), (0, 0, 0, 255 - val))
    
    img = Image.alpha_composite(img, vignette_rgba)
    
    img.save(frame_path)
    print(f"[OK] TV frame created: {frame_path} ({frame_path.stat().st_size / 1024:.1f} KB)")
    return frame_path

def create_scanlines_overlay():
    """Create horizontal scan lines overlay (CRT raster effect)"""
    scanline_path = ASSETS_DIR / "scanlines_1080x1920.png"
    
    if scanline_path.exists():
        print(f"[OK] Scanlines already exist: {scanline_path}")
        return scanline_path
    
    print("[PROCESS] Creating scanlines overlay...")
    
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Thick scan lines every 2 pixels (visible CRT effect)
    for y in range(0, 1920, 2):
        draw.line([(0, y), (1080, y)], fill=(0, 0, 0, 60), width=1)
    
    img.save(scanline_path)
    print(f"[OK] Scanlines created: {scanline_path} ({scanline_path.stat().st_size / 1024:.1f} KB)")
    return scanline_path

def create_qr_code_overlay():
    """Create Bitcoin QR code overlay (persistent, reusable)"""
    qr_path = ASSETS_DIR / "bitcoin_qr_150x150.png"
    
    if qr_path.exists():
        print(f"[OK] QR code already exists: {qr_path}")
        return qr_path
    
    print("[PROCESS] Creating Bitcoin QR code...")
    
    try:
        import qrcode
        
        bitcoin_address = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )
        qr.add_data(f"bitcoin:{bitcoin_address}")
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="white", back_color="black")
        img = img.resize((150, 150))
        img.save(qr_path)
        
        print(f"[OK] QR code created: {qr_path} ({qr_path.stat().st_size / 1024:.1f} KB)")
        return qr_path
    except ImportError:
        print("[WARNING] qrcode library not installed, using FFmpeg fallback...")
        # Fallback: Create simple placeholder
        img = Image.new("RGB", (150, 150), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, 150, 150], outline=(0, 0, 0), width=5)
        draw.text((30, 65), "BTC", fill=(0, 0, 0))
        img.save(qr_path)
        print(f"[OK] QR placeholder created: {qr_path}")
        return qr_path

def main():
    """Create all VHS TV broadcast assets"""
    print("\n" + "="*70)
    print("  CREATING VHS TV BROADCAST ASSETS")
    print("="*70 + "\n")
    
    # Create all assets
    tv_frame = create_tv_frame_overlay()
    scanlines = create_scanlines_overlay()
    qr_code = create_qr_code_overlay()
    
    print("\n" + "="*70)
    print("  [OK] ALL ASSETS CREATED")
    print("="*70)
    print(f"\nLocation: {ASSETS_DIR}")
    print(f"  • tv_frame_1080x1920.png - Vintage CRT TV bezel")
    print(f"  • scanlines_1080x1920.png - CRT scan lines")
    print(f"  • bitcoin_qr_150x150.png - Bitcoin QR code")
    print("\nThese assets are reusable for all videos!")
    print("\n")

if __name__ == "__main__":
    main()

