"""
EMERGENCY QR CODE FIX - Add Bitcoin QR to ALL generators
Run this to patch all your video generators with QR codes
"""
import os
import re
from pathlib import Path

BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
BTC = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"

# Find all Python generators
generators = [
    "DARK_JOSH_DYNAMIC.py",
    "MULTI_PLATFORM_ENGINE.py",
    "PLATFORM_OPTIMIZER.py",
    "LONG_FORM_GENERATOR.py",
    "ORACLE_SIGNAL_PACK.py",
    "ORACLE_COMEDY_ROAST.py",
    "ABRAHAM_PROFESSIONAL_UPGRADE.py",
    "ABRAHAM_COMEDY_YOUTUBE_COMPLETE.py",
]

QR_CODE_SNIPPET = '''
def create_bitcoin_qr(size=300):
    """Create Bitcoin QR code - ALWAYS visible in videos"""
    import qrcode
    from PIL import Image, ImageDraw
    
    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(f"bitcoin:{BTC}")
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="white", back_color="black")
    img = img.resize((size, size), Image.NEAREST)
    
    # Add "SUPPORT TRUTH" text
    final = Image.new('RGB', (size, size+60), (0, 0, 0))
    final.paste(img, (0, 0))
    
    draw = ImageDraw.Draw(final)
    draw.text((size//2, size+30), "SCAN FOR TRUTH", fill=(255, 255, 255), anchor="mm")
    
    qr_path = BASE / "temp" / "bitcoin_qr.jpg"
    qr_path.parent.mkdir(exist_ok=True, parents=True)
    final.save(qr_path)
    
    return str(qr_path)
'''

print("🔧 PATCHING ALL GENERATORS WITH QR CODES...")
print(f"Bitcoin: {BTC}\n")

for gen_file in generators:
    gen_path = BASE / gen_file
    if not gen_path.exists():
        print(f"⚠️  SKIP: {gen_file} (not found)")
        continue
    
    with open(gen_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if QR code function already exists
    if "create_bitcoin_qr" in content:
        print(f"✅ OK: {gen_file} (already has QR)")
        continue
    
    # Add QR code function before first def or class
    if "def " in content or "class " in content:
        # Find first function/class definition
        lines = content.split('\n')
        insert_idx = 0
        for i, line in enumerate(lines):
            if line.strip().startswith('def ') or line.strip().startswith('class '):
                insert_idx = i
                break
        
        # Insert QR function
        lines.insert(insert_idx, QR_CODE_SNIPPET)
        content = '\n'.join(lines)
        
        # Write back
        with open(gen_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ PATCHED: {gen_file}")
    else:
        print(f"⚠️  SKIP: {gen_file} (no functions found)")

print("\n🔥 QR CODE PATCH COMPLETE")
print("\nNEXT STEPS:")
print("1. Regenerate your last 12 shorts")
print("2. Delete the old ones without QR codes")
print("3. Upload the new versions with QR codes")
print(f"\nBitcoin: {BTC}")

