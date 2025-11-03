#!/usr/bin/env python3
"""
SCARIFY - Bitcoin QR Code Generator
Generates QR codes for Bitcoin donations to embed in videos
"""

import qrcode
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BTC_ADDRESS = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"
BASE_DIR = Path("F:/AI_Oracle_Root/scarify")
QR_DIR = BASE_DIR / "qr_codes"
QR_DIR.mkdir(exist_ok=True)

def generate_btc_qr(size=600, with_label=True):
    """Generate Bitcoin QR code"""
    
    print(f"Generating Bitcoin QR code...")
    print(f"Address: {BTC_ADDRESS}")
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    
    qr.add_data(f"bitcoin:{BTC_ADDRESS}")
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    
    if with_label:
        # Add label
        label_height = 100
        final_img = Image.new('RGB', (size, size + label_height), 'white')
        final_img.paste(img, (0, 0))
        
        # Draw text
        draw = ImageDraw.Draw(final_img)
        
        try:
            font_large = ImageFont.truetype("arial.ttf", 36)
            font_small = ImageFont.truetype("arial.ttf", 18)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Title
        title = "SUPPORT TRUTH"
        title_bbox = draw.textbbox((0, 0), title, font=font_large)
        title_width = title_bbox[2] - title_bbox[0]
        draw.text(((size - title_width) // 2, size + 10), title, fill="black", font=font_large)
        
        # Address
        addr_short = f"{BTC_ADDRESS[:20]}..."
        addr_bbox = draw.textbbox((0, 0), addr_short, font=font_small)
        addr_width = addr_bbox[2] - addr_bbox[0]
        draw.text(((size - addr_width) // 2, size + 60), addr_short, fill="gray", font=font_small)
        
        img = final_img
    
    # Save
    output_file = QR_DIR / "btc_qr_code.png"
    img.save(output_file)
    
    print(f"Saved: {output_file}")
    print(f"Size: {img.size}")
    
    return output_file

def generate_video_overlay_qr(size=400):
    """Generate smaller QR for video overlay"""
    
    print(f"Generating video overlay QR...")
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=2,
    )
    
    qr.add_data(f"bitcoin:{BTC_ADDRESS}")
    qr.make(fit=True)
    
    # Create with transparency
    img = qr.make_image(fill_color="white", back_color=(0, 0, 0, 0))
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    
    output_file = QR_DIR / "btc_qr_overlay.png"
    img.save(output_file)
    
    print(f"Saved: {output_file}")
    
    return output_file

def generate_all_variants():
    """Generate all QR code variants"""
    
    print(f"\n{'='*70}")
    print(f"SCARIFY - BTC QR CODE GENERATION")
    print(f"{'='*70}\n")
    
    variants = []
    
    # Standard QR with label
    variants.append(("Standard (with label)", generate_btc_qr(600, True)))
    
    # Large QR without label  
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=12, border=2)
    qr.add_data(f"bitcoin:{BTC_ADDRESS}")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((800, 800), Image.Resampling.LANCZOS)
    large_file = QR_DIR / "btc_qr_large.png"
    img.save(large_file)
    variants.append(("Large (800x800)", large_file))
    
    # Small for corners
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=6, border=1)
    qr.add_data(f"bitcoin:{BTC_ADDRESS}")
    qr.make(fit=True)
    img = qr.make_image(fill_color="white", back_color="black")
    img = img.resize((200, 200), Image.Resampling.LANCZOS)
    small_file = QR_DIR / "btc_qr_small.png"
    img.save(small_file)
    variants.append(("Small corner (200x200)", small_file))
    
    # Video overlay
    variants.append(("Video overlay (400x400)", generate_video_overlay_qr(400)))
    
    print(f"\n{'='*70}")
    print(f"QR CODES GENERATED")
    print(f"{'='*70}\n")
    
    for name, file in variants:
        print(f"[OK] {name}: {file}")
    
    print(f"\n{'='*70}")
    print(f"Bitcoin Address: {BTC_ADDRESS}")
    print(f"Output Directory: {QR_DIR}")
    print(f"{'='*70}\n")
    
    return variants

if __name__ == "__main__":
    generate_all_variants()


