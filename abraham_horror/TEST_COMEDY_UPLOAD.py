"""
TEST SCRIPT - Quick test of comedy generator and YouTube upload
"""
import sys
from pathlib import Path

BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")

print("TESTING ABRAHAM LINCOLN COMEDY SYSTEM")
print("=" * 70)
print()

# Test 1: Check all dependencies
print("[TEST 1] Checking dependencies...")
try:
    import requests
    from bs4 import BeautifulSoup
    from moviepy.editor import AudioFileClip, ImageClip, CompositeVideoClip
    from PIL import Image
    import numpy as np
    print("✅ All dependencies installed")
except ImportError as e:
    print(f"❌ Missing: {e}")
    print("Run: pip install requests beautifulsoup4 moviepy Pillow numpy")
    sys.exit(1)

# Test 2: Check YouTube credentials
print("\n[TEST 2] Checking YouTube credentials...")
youtube_creds = Path("F:/AI_Oracle_Root/scarify/config/credentials/youtube/client_secrets.json")
if youtube_creds.exists():
    print("✅ YouTube credentials found")
else:
    print("⚠️  YouTube credentials missing - uploads will fail")
    print(f"   Expected: {youtube_creds}")

# Test 3: Check for Lincoln image
print("\n[TEST 3] Checking Lincoln images...")
images_dir = BASE / "images"
if images_dir.exists():
    lincoln_images = list(images_dir.glob("*lincoln*.jpg")) + list(images_dir.glob("*lincoln*.png"))
    if lincoln_images:
        print(f"✅ Found {len(lincoln_images)} Lincoln image(s):")
        for img in lincoln_images[:3]:
            print(f"   - {img.name}")
    else:
        print("⚠️  No Lincoln images - placeholder will be used")
else:
    print("⚠️  Images directory missing - will be created")

# Test 4: Check ElevenLabs API
print("\n[TEST 4] Testing ElevenLabs API...")
try:
    import requests
    ELEVENLABS_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
    r = requests.get(
        "https://api.elevenlabs.io/v1/voices",
        headers={"xi-api-key": ELEVENLABS_KEY},
        timeout=10
    )
    if r.status_code == 200:
        voices = r.json().get('voices', [])
        print(f"✅ ElevenLabs API working ({len(voices)} voices available)")
        
        # Check for male voices
        male_voices = []
        for voice in voices:
            if voice['voice_id'] in ["VR6AewLTigWG4xSOukaG", "pNInz6obpgDQGcFmaJgB", "EXAVITQu4vr4xnSDxMaL"]:
                male_voices.append(voice['name'])
        if male_voices:
            print(f"✅ Male voices found: {', '.join(male_voices)}")
    else:
        print(f"❌ ElevenLabs API error: {r.status_code}")
except Exception as e:
    print(f"❌ ElevenLabs test failed: {e}")

# Test 5: Check FFmpeg
print("\n[TEST 5] Checking FFmpeg...")
try:
    import subprocess
    result = subprocess.run(["ffmpeg", "-version"], capture_output=True, timeout=5)
    if result.returncode == 0:
        version_line = result.stdout.decode().split('\n')[0]
        print(f"✅ FFmpeg available: {version_line}")
    else:
        print("⚠️  FFmpeg not working properly")
except:
    print("⚠️  FFmpeg not found - video creation may fail")

# Test 6: Generate test video
print("\n[TEST 6] Generating test video...")
print("   This will create 1 test comedy video and attempt upload")
response = input("   Continue? (y/n): ")

if response.lower() == 'y':
    print()
    print("=" * 70)
    print("RUNNING COMEDY GENERATOR...")
    print("=" * 70)
    print()
    
    import subprocess
    result = subprocess.run(
        [sys.executable, str(BASE / "ABRAHAM_COMEDY_YOUTUBE_COMPLETE.py"), "1"],
        cwd=str(BASE),
        timeout=600
    )
    
    if result.returncode == 0:
        print("\n✅ Test complete! Check output above for results.")
    else:
        print(f"\n[ERROR] Test failed with exit code: {result.returncode}")
else:
    print("   Test skipped")

print("\n" + "=" * 70)
print("TEST SUMMARY")
print("=" * 70)
print("\nNext steps:")
print("1. If all tests pass, run: .\\LAUNCH_COMEDY_YOUTUBE.ps1 -Count 10")
print("2. Check YouTube Studio: https://studio.youtube.com/channel/UCS5pEpSCw8k4wene0iv0uAg/videos")
print("3. Videos should appear in both 'Shorts' AND 'Videos' tabs")
print("\nIf videos don't appear:")
print("- Check youtube_token.pickle exists and is valid")
print("- Re-run auth: Delete youtube_token.pickle and regenerate")
print("- Check YouTube API quota: https://console.cloud.google.com/apis/api/youtube.googleapis.com/quotas")

