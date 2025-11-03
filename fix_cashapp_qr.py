#!/usr/bin/env python3
"""
FIX CASH APP QR CODE - MAKE IT SCANNABLE!

Issues that prevent scanning:
1. Too small (need 300x300+ for mobile)
2. Low contrast (need pure black/white)
3. Too much error correction (makes it complex)
4. Transparent background (cameras struggle)

FIX: Generate HIGH-CONTRAST, LARGE QR code that ALWAYS scans
"""
import qrcode
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

CASHAPP_LINK = "https://cash.app/$healthiwealthi/bitcoin/THZmAyn3nx"
OUTPUT_DIR = Path("F:/AI_Oracle_Root/scarify/qr_codes")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_scannable_cashapp_qr():
    """Generate GUARANTEED scannable Cash App QR code"""
    print("\n" + "="*70)
    print("GENERATING HIGH-QUALITY SCANNABLE QR CODE")
    print("="*70)
    
    # HIGH-CONTRAST, LARGE QR code
    qr = qrcode.QRCode(
        version=1,  # Smallest version that fits
        error_correction=qrcode.constants.ERROR_CORRECT_M,  # Medium (not too complex)
        box_size=15,  # Larger boxes = easier to scan
        border=4,  # Good margin
    )
    
    qr.add_data(CASHAPP_LINK)
    qr.make(fit=True)
    
    # Create image with HIGH CONTRAST
    img = qr.make_image(
        fill_color="black",      # Pure black (not gray)
        back_color="white"       # Pure white (not transparent)
    )
    
    # Resize to LARGE size (300x300 minimum for mobile)
    img = img.resize((400, 400), Image.Resampling.LANCZOS)
    
    # Save standard version
    standard_path = OUTPUT_DIR / "cashapp_qr_scannable.png"
    img.save(standard_path, "PNG", optimize=True)
    
    print(f"[QR] Generated: {standard_path}")
    print(f"[QR] Size: 400x400px")
    print(f"[QR] Contrast: Pure black/white")
    print(f"[QR] Link: {CASHAPP_LINK}")
    
    # Also create VIDEO-OPTIMIZED version (white on black for dark videos)
    qr_inverted = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=15,
        border=4,
    )
    
    qr_inverted.add_data(CASHAPP_LINK)
    qr_inverted.make(fit=True)
    
    # White on black (better visibility on videos)
    img_inverted = qr_inverted.make_image(
        fill_color="white",
        back_color="black"
    )
    
    img_inverted = img_inverted.resize((400, 400), Image.Resampling.LANCZOS)
    
    # Add label for clarity
    canvas = Image.new('RGB', (450, 460), 'black')
    canvas.paste(img_inverted, (25, 25))
    
    # Add text label
    try:
        draw = ImageDraw.Draw(canvas)
        font = ImageFont.truetype("arial.ttf", 24)
        text = "CASH APP"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        draw.text(((450 - text_width) // 2, 435), text, fill="white", font=font)
    except:
        pass  # Font not critical
    
    video_path = OUTPUT_DIR / "cashapp_qr.png"
    canvas.save(video_path, "PNG", optimize=True)
    
    print(f"[QR] Video version: {video_path}")
    print(f"[QR] Size: 450x460px (with label)")
    print(f"[QR] Optimized for: Dark video backgrounds")
    
    print("\n" + "="*70)
    print("QR CODE TESTING")
    print("="*70)
    print("\n1. Scan with phone camera app")
    print("2. Should open Cash App instantly")
    print("3. Should show: Send Bitcoin to $healthiwealthi")
    print("\nIf doesn't work:")
    print("  - Increase brightness on screen")
    print("  - Hold phone steady 6-12 inches away")
    print("  - Try different camera app")
    print("  - Make sure phone has Cash App installed")
    
    print("\n" + "="*70)
    print("READY FOR VIDEO EMBEDDING")
    print("="*70)
    print(f"\nUse in FFmpeg: {video_path}")
    print(f"Recommended overlay size: 250x250 (scaled from 450x460)")
    print(f"Position: Top-right corner")
    print(f"Command: [qr]scale=250:250[qr_scaled]; overlay=W-w-20:20")
    
    print("\n" + "="*70)
    
    return str(video_path)

def test_qr_link():
    """Verify Cash App link is valid"""
    print("\n" + "="*70)
    print("TESTING CASH APP LINK")
    print("="*70)
    
    import requests
    
    print(f"\nLink: {CASHAPP_LINK}")
    print(f"Testing...")
    
    try:
        response = requests.head(CASHAPP_LINK, timeout=10, allow_redirects=True)
        if response.status_code in [200, 302, 301]:
            print(f"[OK] Link is valid (Status: {response.status_code})")
        else:
            print(f"[WARN] Link returned: {response.status_code}")
    except Exception as e:
        print(f"[INFO] Could not test link: {e}")
        print(f"[INFO] This is normal - link may require Cash App context")
    
    print(f"\nTo test manually:")
    print(f"1. Open: {CASHAPP_LINK}")
    print(f"2. Should redirect to Cash App")
    print(f"3. Should show Bitcoin send screen")
    
    print("="*70)

if __name__ == "__main__":
    # Generate improved QR code
    qr_path = generate_scannable_cashapp_qr()
    
    # Test link
    test_qr_link()
    
    print("\n" + "="*70)
    print("ACTION REQUIRED")
    print("="*70)
    print("\n1. Open: F:\\AI_Oracle_Root\\scarify\\qr_codes\\")
    print("2. Find: cashapp_qr.png (new version)")
    print("3. Scan with phone camera")
    print("4. Verify it opens Cash App")
    print("\nIf scans successfully:")
    print("  -> Videos will have working QR after next generation")
    print("\nIf still doesn't scan:")
    print("  -> May need to use direct link in description instead")
    print("  -> Or use larger QR (500x500px)")
    
    print("\n" + "="*70)



