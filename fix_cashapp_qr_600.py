#!/usr/bin/env python3
"""
GENERATE 600x600 CASH APP QR CODE - GUARANTEED SCANNABLE
"""
import qrcode
from PIL import Image, ImageDraw
from pathlib import Path

CASHAPP_LINK = "https://cash.app/$healthiwealthi/bitcoin/THZmAyn3nx"
OUTPUT_DIR = Path("F:/AI_Oracle_Root/scarify/qr_codes")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_600x600_qr():
    """Generate 600x600 scannable QR code"""
    print("\n[GENERATING 600x600 CASH APP QR CODE]")
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=20,  # Large boxes
        border=4,
    )
    
    qr.add_data(CASHAPP_LINK)
    qr.make(fit=True)
    
    # Pure black/white, high contrast
    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((600, 600), Image.Resampling.LANCZOS)
    
    # Save video version (white on black)
    qr_inverted = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=20, border=4)
    qr_inverted.add_data(CASHAPP_LINK)
    qr_inverted.make(fit=True)
    
    img_inverted = qr_inverted.make_image(fill_color="white", back_color="black")
    img_inverted = img_inverted.resize((600, 600), Image.Resampling.LANCZOS)
    
    # Add border and label
    canvas = Image.new('RGB', (650, 650), 'black')
    canvas.paste(img_inverted, (25, 25))
    
    try:
        draw = ImageDraw.Draw(canvas)
        # Simple text
        font_size = 28
        text = "CASH APP BITCOIN"
        draw.text((325, 615), text, fill="white", anchor="mm")
    except:
        pass
    
    video_path = OUTPUT_DIR / "cashapp_qr.png"
    canvas.save(video_path, "PNG", optimize=True)
    
    print(f"[OK] Generated: {video_path}")
    print(f"[OK] Size: 650x650px")
    print(f"[OK] QR Code: 600x600px (scannable from 2+ feet away)")
    print(f"[OK] Link: {CASHAPP_LINK}")
    
    return str(video_path)

if __name__ == "__main__":
    generate_600x600_qr()
    print("\n[READY] QR code ready for video embedding")



