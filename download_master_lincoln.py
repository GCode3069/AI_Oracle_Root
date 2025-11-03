#!/usr/bin/env python3
"""
Download and prepare the MASTER Abraham Lincoln image for the project
This is the best quality image optimized for Max Headroom VHS effects
"""
import requests
from pathlib import Path
import subprocess

# Best Lincoln image for Max Headroom VHS effects
# O-77 matte collodion print - Library of Congress, excellent quality, formal pose
MASTER_LINCOLN_URL = "https://upload.wikimedia.org/wikipedia/commons/a/ab/Abraham_Lincoln_O-77_matte_collodion_print.jpg"

# Alternative high-quality options
ALTERNATIVE_URLS = [
    "https://upload.wikimedia.org/wikipedia/commons/1/1b/Abraham_Lincoln_November_1863.jpg",  # Gardner 1863
    "https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Abraham_Lincoln_head_on_shoulders_photo_portrait.jpg/800px-Abraham_Lincoln_head_on_shoulders_photo_portrait.jpg",  # Head and shoulders
]

BASE_DIR = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
LINCOLN_DIR = BASE_DIR / "lincoln_faces"
LINCOLN_DIR.mkdir(parents=True, exist_ok=True)

def download_image(url, output_path):
    """Download image from URL"""
    try:
        print(f"Downloading from: {url}")
        # Add user agent to avoid 403 errors
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=30, stream=True, headers=headers)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Verify file size
        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"[OK] Downloaded: {output_path.name} ({size_mb:.2f} MB)")
        return True
    except Exception as e:
        print(f"[ERROR] Download failed: {e}")
        return False

def optimize_image_for_vhs(input_path, output_path):
    """Optimize image for VHS Max Headroom effects (square crop, centered face)"""
    try:
        print(f"Optimizing image for VHS effects...")
        # Use FFmpeg to create optimized version:
        # 1. Ensure minimum 1080x1080 (square for TV screen)
        # 2. Center crop face
        # 3. Enhance contrast slightly for VHS effects
        
        cmd = [
            'ffmpeg', '-y',
            '-i', str(input_path),
            '-vf',
            # Scale to at least 1080 height, maintain aspect
            'scale=1080:1080:force_original_aspect_ratio=increase,'
            # Crop to square, center face
            'crop=1080:1080:0:(ih-oh)/2,'
            # Enhance for VHS (slight contrast boost)
            'eq=contrast=1.1:brightness=0.05',
            '-frames:v', '1',
            str(output_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if output_path.exists():
            size_mb = output_path.stat().st_size / (1024 * 1024)
            print(f"[OK] Optimized: {output_path.name} ({size_mb:.2f} MB, 1080x1080)")
            return True
        else:
            print(f"[WARNING] Optimization failed, using original")
            return False
    except Exception as e:
        print(f"[WARNING] Optimization error: {e}, using original")
        return False

def main():
    print("\n" + "="*70)
    print("  DOWNLOADING MASTER ABRAHAM LINCOLN IMAGE")
    print("="*70 + "\n")
    
    # Primary master image
    master_path = LINCOLN_DIR / "lincoln_master.jpg"
    master_optimized = LINCOLN_DIR / "lincoln_master_optimized.jpg"
    
    # Download master image
    if not master_path.exists():
        if download_image(MASTER_LINCOLN_URL, master_path):
            print(f"[OK] Master image saved: {master_path}")
        else:
            # Try alternatives
            print("Trying alternative sources...")
            for alt_url in ALTERNATIVE_URLS:
                if download_image(alt_url, master_path):
                    break
    else:
        print(f"[OK] Master image already exists: {master_path}")
    
    # Optimize for VHS effects
    if master_path.exists():
        optimize_image_for_vhs(master_path, master_optimized)
    
    # Also create a backup as "lincoln.jpg" (commonly used name)
    if master_path.exists():
        import shutil
        backup_path = LINCOLN_DIR / "lincoln.jpg"
        if not backup_path.exists():
            shutil.copy2(master_path, backup_path)
            print(f"[OK] Created backup: {backup_path}")
    
    # Create optimized backup
    if master_optimized.exists():
        import shutil
        optimized_backup = LINCOLN_DIR / "lincoln_optimized.jpg"
        if not optimized_backup.exists():
            shutil.copy2(master_optimized, optimized_backup)
            print(f"[OK] Created optimized backup: {optimized_backup}")
    
    print("\n" + "="*70)
    print("  [OK] MASTER LINCOLN IMAGE READY")
    print("="*70)
    print(f"\nLocation: {LINCOLN_DIR}")
    print(f"Master: lincoln_master.jpg")
    print(f"Optimized: lincoln_master_optimized.jpg (1080x1080, VHS-ready)")
    print(f"\nAll effects will use this image:")
    print(f"  - VHS TV broadcast effects")
    print(f"  - Lip-sync (D-ID/Wav2Lip)")
    print(f"  - Jumpscare effects")
    print(f"  - Bitcoin QR code overlay")
    print(f"  - Psychological audio layers")
    print("\n")

if __name__ == "__main__":
    main()

