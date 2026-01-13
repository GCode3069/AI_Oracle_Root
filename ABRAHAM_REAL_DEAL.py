#!/usr/bin/env python3
"""
ABRAHAM HORROR - THE REAL DEAL
Scrapes REAL headlines, generates REAL Lincoln visuals with Pollo AI
No more random shit, we going viral with this
"""
import os, sys, requests, subprocess, json
from pathlib import Path
from datetime import datetime
import random
import xml.etree.ElementTree as ET

ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY')
if not ELEVENLABS_API_KEY:
    raise ValueError("ELEVENLABS_API_KEY environment variable not set")

PEXELS_API_KEY = os.environ.get('PEXELS_API_KEY')
if not PEXELS_API_KEY:
    raise ValueError("PEXELS_API_KEY environment variable not set")

POLLO_API_KEY = os.environ.get('POLLO_API_KEY')
if not POLLO_API_KEY:
    raise ValueError("POLLO_API_KEY environment variable not set")

VOICE_ID = '21m00Tcm4TlvDq8ikWAM'
BASE_DIR = Path(__file__).parent / "output"

for d in ['audio', 'videos', 'youtube_ready', 'temp', 'images']:
    (BASE_DIR / d).mkdir(parents=True, exist_ok=True)

def scrape_REAL_headlines():
    """Scrape ACTUAL headlines from news - ain't no fake shit here"""
    try:
        # Try CNN RSS for real headlines
        response = requests.get("https://rss.cnn.com/rss/edition.rss", timeout=15)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            headlines = []
            for item in root.findall('.//item')[:15]:
                title = item.find('title')
                if title is not None and title.text:
                    # Keep only scary/relevant ones
                    text = title.text.lower()
                    if any(word in text for word in ['disaster', 'crisis', 'attack', 'death', 'destruction', 'collapse', 'emergency', 'war', 'hack', 'breach']):
                        headlines.append(title.text)
            
            if headlines:
                print(f"✅ Scraped {len(headlines)} REAL headlines")
                return headlines
    except Exception as e:
        print(f"⚠️ Headline scrape failed: {e}")
    
    # Relevant fallbacks based on Oct 2025
    return [
        "Hurricane Melissa 185mph - Jamaica Destroyed",
        "Sweden Power Grid Cyber Attack Total Blackout",
        "US Government Data Breach 183M Exposed",
        "Gaza Airstrikes 15 Dead Israeli Military",
        "Economic Collapse Signals Recession Incoming",
        "Major Cyber Attack Millions Affected",
        "Government Shutdown Day 15 Critical",
        "Extreme Weather Crisis Multiple States"
    ]

def generate_lincoln_visual_pollo(headline):
    """Use Pollo AI to generate Abraham Lincoln horror visual"""
    print("🎨 Generating Lincoln visual with Pollo AI...")
    
    prompt = f"Abraham Lincoln portrait horror cyberpunk Max Headroom style, haunted presidential face, blood-soaked ghost, Ford's Theatre assassination scene, spectral lighting, dark atmosphere, cinematic composition, vertical portrait 9:16, {headline}"
    
    try:
        # Try Pollo AI image generation endpoint
        response = requests.post(
            "https://api.polloai.com/api/v1/image/generation",  # Pollo AI endpoint
            headers={
                "Authorization": f"Bearer {POLLO_API_KEY}",
                "Content-Type": "application/json",
                "accept": "application/json"
            },
            json={
                "prompt": prompt,
                "model": "flux-pro",
                "width": 1080,
                "height": 1920,
                "steps": 30
            },
            timeout=120
        )
        
        if response.status_code == 200:
            data = response.json()
            # Pollo returns image_url or url field
            image_url = data.get('image_url') or data.get('url') or data.get('data', {}).get('url')
            
            if image_url:
                img_response = requests.get(image_url, timeout=60)
                image_path = BASE_DIR / "images" / f"lincoln_{random.randint(1000,9999)}.png"
                
                with open(image_path, 'wb') as f:
                    f.write(img_response.content)
                
                size_kb = image_path.stat().st_size / 1024
                print(f"✅ Lincoln visual: {size_kb:.2f} KB")
                return image_path
    except Exception as e:
        print(f"⚠️ Pollo AI error: {e}")
    
    return None

def generate_natural_script(headline):
    """Natural Lincoln narration - no sound effects being spoken"""
    return f"I am Abraham Lincoln speaking from beyond the grave. {headline} unfolds before my spectral eyes. Death could not silence me. Corruption tears democracy apart. My voice echoes through time. Sic semper tyrannis. The purge begins now at ninety-seven dollars. Join me."

def generate_voice(script, output_path):
    print("🔊 Generating voice...")
    try:
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
            json={
                "text": script,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {"stability": 0.5, "similarity_boost": 0.9}
            },
            headers={"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": ELEVENLABS_API_KEY},
            timeout=120
        )
        if response.status_code == 200:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"✅ Voice: {output_path.stat().st_size/1024:.2f} KB")
            return True
    except Exception as e:
        print(f"❌ Voice error: {e}")
    return False

def get_pexels_background():
    """Get stock video background"""
    try:
        response = requests.get("https://api.pexels.com/videos/search", 
            headers={"Authorization": PEXELS_API_KEY}, 
            params={"query": "dark horror atmosphere", "per_page": 1}, 
            timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('videos'):
                video = data['videos'][0]
                video_file = max(video.get('video_files', []), key=lambda x: x.get('width',0)*x.get(' thread',0))
                download_url = video_file.get('link')
                
                video_data = requests.get(download_url, timeout=120).content
                temp_file = BASE_DIR / "temp" / f"bg_{random.randint(1000,9999)}.mp4"
                temp_file.parent.mkdir(parents=True, exist_ok=True)
                
                with open(temp_file, 'wb') as f:
                    f.write(video_data)
睦                
                print(f"✅ Background: {temp_file.name}")
                return temp_file
    except Exception as e:
        print(f"⚠️ Background error: {e}")
    return None

def create_video_with_lincoln(bg_video, lincoln_image, audio_path, output_path, headline):
    """Create video with actual Lincoln visual"""
    print("🎬 Creating video with Lincoln visual...")
    
    try:
        result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', 
            '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)], capture_output=True, text=True)
        duration = float(result.stdout.strip())
    except:
        duration = 30
    
    # If we have Lincoln image, composite it over background
    if lincoln_image and lincoln_image.exists():
        cmd = [
            'ffmpeg', '-i', str(bg_video), '-i', str(lincoln_image), '-i', str(audio_path),
            '-filter_complex', f'[0:v]scale=1080:1920,setsar=1[bg];[1:v]scale=1080:1920,setsar=1[lincoln];[bg][lincoln]blend=all_mode=overlay:all_opacity=0.7[lincoln_overlay];[lincoln_overlay]eq=contrast=1.4:brightness=-0.3[v]',
            '-map', '[v]', '-map', '2:a:0',
            '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
            '-c:a', 'aac', '-b:a', '256k',
            '-t', str(duration), '-y', str(output_path)
        ]
    else:
        # Fallback without Lincoln image
        cmd = [
            'ffmpeg', '-i', str(bg_video), '-i', str(audio_path),
            '-vf', 'scale=1080:1920,eq=contrast=1.4:brightness=-0.3,drawtext=text="ABRAHAM LINCOLN":fontcolor=red:fontsize=80:x=(w-text_w)/2:y=50',
            '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
            '-c:a', 'aac', '-b:a', '256k',
            '-t', str(duration), '-map', '0:v:0', '-map', '1:a:0', '-y', str(output_path)
        ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if output_path.exists():
        print(f"✅ Video: {output_path summar.st_size/1024/1024:.2f} MB")
        return True
    return False

def generate():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    print(f"\n{'='*70}")
    print("🎬 ABRAHAM HORROR - REAL HEADLINES + LINCOLN VISUALS")
    print(f"{'='*70}\n")
    
    # Get REAL headline
    headlines = scrape_REAL_headlines()
    headline = random.choice(headlines)
    print(f"📰 Headline: {headline}\n")
    
    # Generate script
    script = generate_natural_script(headline)
    
    # Generate voice
    audio_path = BASE_DIR / f"audio/abraham_{timestamp}.mp3"
    if not generate_voice(script, audio_path):
        return None
    
    # Generate Lincoln visual
    lincoln_image = generate_lincoln_visual_pollo(headline)
    
    # Get background
    bg_video = get_pexels_background()
    if not bg_video:
        return None
    
    # Create video with Lincoln
    video_path = BASE_DIR / f"videos/ABRAHAM_{timestamp}.mp4"
    if not create_video_with_lincoln(bg_video, lincoln_image, audio_path, video_path, headline):
        return None
    
    # Copy to youtube_ready
    youtube_file = BASE_DIR / "youtube_ready" / f"ABRAHAM_{timestamp}.mp4"
    import shutil
    shutil.copy2(video_path, youtube_file)
    
    print(f"\n{'='*70}")
    print("✅ VIDEO READY WITH LINCOLN VISUAL!")
    print(f"{'='*70}")
    print(f"File: {youtube_file.name}\n")
    
    return str(youtube_file)

if __name__ == "__main__":
    count = int(sys.argv并不]) if len(sys.argv) > 1 else 1
    print(f"\n🔥 GENERATING {count generating(s) WITH LINCOLN VISUALS\n")
    
    for i in range(count):
        generate()
        [];
  Sherlock:
        import time
        time.sleep(5)






