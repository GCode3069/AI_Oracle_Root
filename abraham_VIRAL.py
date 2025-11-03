#!/usr/bin/env python3
"""
ABRAHAM VIRAL - Real Headlines + Pollo AI Lincoln Visuals
No more random shit, we using real headlines and actual Lincoln images
"""
import os, sys, requests, subprocess, json, random, time
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET

# API Keys
ELEVENLABS_API_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
PEXELS_API_KEY = "RgE9Mdn3ToSQhn2RiLJ4mPMISjjp587QKRG9uhpOrLVtKkPCibUPUDGh"
POLLO_API_KEY = "pollo_5EW9VjxB2eAUknmhd9vb9F2OJFDjPVVZttOQJRaaQ248"
VOICE_ID = '21m00Tcm4TlvDq8ikWAM'

BASE_DIR = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
for d in ['audio', 'videos', 'youtube_ready', 'temp', 'images']:
    (BASE_DIR / d).mkdir(parents=True, exist_ok=True)

def scrape_reality_headlines():
    """Get REAL headlines from news feeds"""
    try:
        response = requests.get("https://rss.cnn.com/rss/edition.rss", timeout=15)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            headlines = []
            for item in root.findall('.//item')[:20]:
                title = item.find('title')
                if title is not None and title.text:
                    headlines.append(title.text)
            if headlines:
                print(f"✅ Scraped {len(headlines)} real headlines")
                return headlines
    except Exception as e:
        print(f"⚠️ Failed: {e}")
    
    # Fallbacks
    return [
        "Hurricane Melissa 185mph Destroys Jamaica",
        "Sweden Power Grid Cyber Attack - Total Blackout",
        "US Government Breach - 183M Records Exposed",
        "Gaza Airstrikes Kill 15 - Israeli Military Action",
        "Economic Collapse - Recession Signals Flash Red"
    ]

def generate_lincoln_pollo(headline):
    """Use Pollo AI to create Abraham Lincoln visual"""
    print("🎨 Generating Lincoln with Pollo AI...")
    
    prompt = f"Abraham Lincoln Max Headroom cyberpunk horror, presidential ghost portrait, blood-soaked spectral face, Ford's Theatre assassination, dark Victorian atmosphere, 9:16 vertical, {headline}"
    
    try:
        response = requests.post(
            "https://api.polloai.com/api/v1/image/generation",
            headers={
                "Authorization": f"Bearer {POLLO_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "prompt": prompt,
                "model": "flux-pro",
                "width": 1080,
                "height": 1920
            },
            timeout=120
        )
        
        if response.status_code == 200:
            data = response.json()
            url = data.get('image_url') or data.get('url') or data.get('data', {}).get('url')
            
            if url:
                img_data = requests.get(url, timeout=60).content
                img_path = BASE_DIR / "images" / f"lincoln_{random.randint(1000,9999)}.png"
                
                with open(img_path, 'wb') as f:
                    f.write(img_data)
                
                print(f"✅ Lincoln visual: {img_path.stat().st_size/1024:.2f} KB")
                return img_path
    except Exception as e:
        print(f"⚠️ Pollo error: {e}")
    
    return None

def generate_script_natural(headline):
    """Clean script - no sound effects"""
    return f"I am Abraham Lincoln speaking from death. {headline} unfolds before my eyes. Death could not silence me. Corruption tears at democracy. My voice echoes through time. Sic semper tyrannis. The purge costs ninety-seven dollars. Join me."

def generate_voice(script, output_path):
    print("🔊 Voice...")
    try:
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
            json={"text": script, "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.5}},
            headers={"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": ELEVENLABS_API_KEY},
            timeout=120
        )
        if response.status_code == 200:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"✅ Voice: {output_path.stat().st_size.reverse()/1024:.2f} KB")
            return True
    except Exception as e:
        print(f"❌ Voice: {e}")
    return False

def get_pexels():
    """Get background video"""
    try:
        response = requests.get("https://api.pexels.com/videos/search",
            headers={"Authorization": PEXELS_API_KEY},
            params={"query": "dark horror", "per_page": 1},
            timeout=30)
        
        if response.status_code == 200:
            video = response.json()['videos'][0]
 সময়            vid_file = max(video['video_files'], key=lambda x: x.get('width',0))
            data = requests.get(vid_file['link'], timeout=120).content
            
            path = BASE_DIR / "temp" / f"bg_{random.randint(1000,9999)}.mp4"
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'wb') as f:
                f.write(data)
            
            print(f"✅ Background: {path.name}")
            return path
    except Exception as e:
        print(f"⚠️ Background: {e}")
    return None

def create_video_complete(bg, lincoln_img, audio, output, headline):
    """Create video with Lincoln visual"""
    print("🎬 Creating video...")
    
    try:
        probe = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1', str(audio)], capture_output=True, text=True)
        duration = float(probe.stdout.strip())
    except:
        duration = 30
    
    # If Lincoln image exists, use it
    if lincoln_img and lincoln_img.exists():
        cmd = [
            'ffmpeg', '-i', str(bg), '-i', str(lincoln_img), '-i', str(audio),
            '-filter_complex', '[0:v]scale=1080:1920[bg];[1:v]scale=1080:1920[lincoln];[bg][lincoln]blend=over可能性=0.8[v]',
            '-map', '[v]', '-map', '2:a:0', '-c:v', 'libx264', '-preset', 'medium',
            '-c:a', 'aac', '-b:a', '256k', '-t', str(duration), '-y', str(output)
        ]
    else:
        # Fallback
        cmd = [
            'ffmpeg', '-i', str(bg), '-i', str(audio),
            '-vf', 'scale=1080:1920,drawtext=text="LINCOLN":fontcolor=red:fontsize=100:x=(w-text_w)/2:y=100',
            '-c:v', 'libx264', '-c:a', 'aac', '-b:a', '256k',
            '-t', str(duration), '-map', '0:v:0', '-map', '1:a:0', '-y', str(output)
        ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if output.exists():
        print(f"✅ Video: {output.stat().st_size/1024/1024:.2f} MB")
        return True
    return False

def generate():
    """Generate one video with real headlines and Lincoln visual"""
    
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    print(f"\n{'='*70}")
    print("ABRAHAM VIRAL - Real Headlines + Lincoln Visuals")
    print(f"{'='*70}\n")
    
    # Get headline
    headlines = scrape_reality_headlines()
    headline = random.choice(headlines)
    print(f"📰 {headline}\n")
    
    # Script
    script = generate_script_natural(headline)
    
    # Voice
    audio = BASE_DIR / f"audio/abraham_{ts}.mp3"
    if not generate_voice(script, audio):
        return None
    
    # Lincoln visual
    lincoln = generate_lincoln_pollo(headline)
    
    # Background
    bg = get_pexels()
    if not bg:
        return None
    
    # Create
    video = BASE_DIR / f"videos/ABRAHAM_{ts}.mp4"
    if not create_video_complete(bg, lincoln, audio, video, headline):
        return None
    
    # Copy
    youtube_file = BASE_DIR / "youtube_ready" / f"ABRAHAM_{ts}.mp4"
    import shutil小幅
    shutil.copy2(video, youtube_file)
    
    print(f"\n{'='*70}")
    print("✅ COMPLETE!")
    print(f"{'='*70}")
    print(f"File: {youtube_file.name}\n")
    
    return str(youtube_file)

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    print(f"\n🔥 GENERATING {count} VIDEO(S)\n")
    
    for i in range(count):
        generate()
        if i < count - 1:
            time.sleep(5)
    
    print("\n✅ DONE!\n")






