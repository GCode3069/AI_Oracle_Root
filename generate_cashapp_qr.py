#!/usr/bin/env python3
"""
Generate Cash App QR Code for video overlay
Easier for mobile users than Bitcoin address QR
"""
import qrcode
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Your Cash App Bitcoin link
CASHAPP_LINK = "https://cash.app/launch/bitcoin/$healthiwealthi/THZmAyn3nx"
BITCOIN_ADDRESS = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"

BASE_DIR = Path("F:/AI_Oracle_Root/scarify")
QR_DIR = BASE_DIR / "qr_codes"
QR_DIR.mkdir(parents=True, exist_ok=True)

def generate_cashapp_qr():
    """Generate Cash App QR code"""
    print("\n[CashApp QR] Generating...")
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2
    )
    qr.add_data(CASHAPP_LINK)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="white", back_color="transparent")
    
    # Resize to standard size
    img = img.resize((200, 200), Image.Resampling.LANCZOS)
    
    # Save
    output_path = QR_DIR / "cashapp_qr.png"
    img.save(output_path, "PNG")
    
    print(f"[CashApp QR] Saved: {output_path}")
    print(f"[CashApp QR] Link: {CASHAPP_LINK}")
    return str(output_path)

def generate_bitcoin_qr():
    """Generate Bitcoin address QR code"""
    print("\n[Bitcoin QR] Generating...")
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2
    )
    qr.add_data(f"bitcoin:{BITCOIN_ADDRESS}")
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="white", back_color="transparent")
    
    # Resize
    img = img.resize((200, 200), Image.Resampling.LANCZOS)
    
    # Save
    output_path = QR_DIR / "bitcoin_qr.png"
    img.save(output_path, "PNG")
    
    print(f"[Bitcoin QR] Saved: {output_path}")
    print(f"[Bitcoin QR] Address: {BITCOIN_ADDRESS}")
    return str(output_path)

def generate_dual_qr():
    """Generate side-by-side QR codes (Bitcoin + Cash App)"""
    print("\n[Dual QR] Generating side-by-side...")
    
    # Generate both QR codes
    bitcoin_qr = generate_bitcoin_qr()
    cashapp_qr = generate_cashapp_qr()
    
    # Load both
    btc_img = Image.open(bitcoin_qr)
    cash_img = Image.open(cashapp_qr)
    
    # Create canvas
    width = 450
    height = 250
    canvas = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    
    # Paste QR codes side by side
    canvas.paste(btc_img, (10, 25))
    canvas.paste(cash_img, (240, 25))
    
    # Add labels (if font available)
    try:
        draw = ImageDraw.Draw(canvas)
        font = ImageFont.truetype("arial.ttf", 16)
        draw.text((50, 5), "BTC", fill="white", font=font)
        draw.text((270, 5), "CASH", fill="white", font=font)
    except:
        pass
    
    # Save
    output_path = QR_DIR / "dual_payment_qr.png"
    canvas.save(output_path, "PNG")
    
    print(f"[Dual QR] Saved: {output_path}")
    return str(output_path)

def generate_all_qr_codes():
    """Generate all QR code variants"""
    print("\n" + "="*70)
    print("GENERATING PAYMENT QR CODES")
    print("="*70)
    
    # Individual QR codes
    bitcoin_qr = generate_bitcoin_qr()
    cashapp_qr = generate_cashapp_qr()
    
    # Dual QR code
    dual_qr = generate_dual_qr()
    
    print("\n" + "="*70)
    print("GENERATED:")
    print("="*70)
    print(f"1. Bitcoin QR: {bitcoin_qr}")
    print(f"2. Cash App QR: {cashapp_qr}")
    print(f"3. Dual QR: {dual_qr}")
    print("\n" + "="*70)
    print("USAGE:")
    print("="*70)
    print("Option A: Use Cash App QR (easier for mobile)")
    print("Option B: Use Bitcoin QR (direct wallet)")
    print("Option C: Use Dual QR (both options)")
    print("\nRecommended: Cash App QR (more user-friendly!)")
    print("="*70)

if __name__ == "__main__":
    generate_all_qr_codes()

