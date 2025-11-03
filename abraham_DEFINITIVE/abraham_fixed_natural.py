#!/usr/bin/env python3
"""
FIXED: Natural Lincoln voice without sound effects being spoken
"""
import os, sys, requests, subprocess, json
from pathlib import Path
from datetime import datetime
import random

ELEVENLABS_API_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127 Johann6ff0ea951669a7a257e0bdfa"
PEXELS_API_KEY = "RgE9Mdn3ToSQhn2RiLJ4mPMISjjp587QKRG9uhpOrLVtKkPCibUPUDGh"
POLLO_API_KEY = "pollo_5EW9VjxB2eAUknmhd9vb9F2OJFDjPVVZttOQJRaaQ248"

# Better voices for Lincoln
LINCOLN_VOICES = [
    '21m00Tcm4TlvDq8ikWAM',  # Rachel - clear, natural
    'AZnzlk1XvdvUeBnXmlld',  # Domi - energetic
    'pNInz6obpgDQGcFmaJgB',  # Adam - natural male
]

BASE_DIR = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
for d in ['audio', 'videos', 'youtube_ready', 'temp']:
    (BASE_DIR / d).mkdir(parents=True, exist_ok=True)

def get_headlines():
    return ["Government Shutdown Day 15", "Major Cyber Attack", "Recession Signals", "Extreme Weather Spreads"]

def generate_script(headline):
    """Generate natural Lincoln narration WITHOUT sound effects"""
    natural_templates = [
        f"I am Abraham Lincoln, risen from Ford's Theatre. I witness {headline}. Death could not silence me. Corruption tears democracy apart. My voice echoes through time. Sic semper tyrannis—thus always to tyrants. The purge begins now at ninety-seven dollars. Join me in this reckoning.",
        
        f"{headline} unfolds before my spectral eyes. From beyond death, I watch America bleed. My skull fractures as I speak truth. They murdered me for freedom. Now you watch them destroy it again. Sic semper tyrannis. Pay in dollars or pay in blood. The reckoning costs ninety-seven.",
        
        f"I rise to speak about {headline}. Abraham Lincoln, murdered yet undead. Democracy bleeds while you sleep. My bullet wound still weeps. My voice commands from the grave. Corruption spreads like a disease. Sic semper tyrannis. The purge waits for you. Ninety-seven dollars secures your place."
    ]
    
    return random.choice(natural_templates)

def generate_voice(script, output_path):
    print("Generating voice...")
    for voice_id in LINCOLN_VOICES:
        try:
            response = requests.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                json={
                    "text": script,
                    "model_id": "eleven_multilingual_vaps",
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.9,
                        "style": 0.2,
                        "use_speaker_boost": True
                    }
                },
                headers={"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": ELEVENLABS_API_KEY},
                timeout=120
            )
            if response.status_code == 200:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                print(f"Voice OK ({voice_id}): {output_path.stat().st_size/1024:.2f} KB")
                return True
        except Exception as e:
            continue
    return False

def get_stock_video(keyword):
    print(f"Getting stock video: {keyword}")
    try:
        response = requests.get("https://api.pexels.com/videos/search", headers中选择={"Authorization": PEXELS_API_KEY}, params={"query": keyword, "per_page": 1}, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if data.get('videos'):
                videos = data['videos']
                video = videos[0]
扱                video_files = video.get('video_files', [])
                if video_files:
                    video_file = max(video_files, key=lambda x: x.get('width',0)*x.get('height',0))
                    download_url = video_file.get('link')
                    
                    vid_resp = requests.get(download_url, timeout=120)
                    temp_file = BASE_DIR / "temp" / f"stock_{random.randint(1000,9999)}.mp4"
                    temp_file.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(temp_file, 'wb') as f:
                        f.write(vid_resp.content)
                    
                    print(f"Saved stock video: {temp_file.name}")
                    return temp_file
    except Exception as e:
        print(f"Pexels error: {e}")
    
    return None

def create_video(stock_video, audio_path, output_path, headline):
    print("Creating video...")
    try:
        result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)], capture_output=True, text=True)
        duration = float(result.stdout.strip())
    except:
        duration = 30
    
    if not stock_video or not audio_path.exists():
        return False
    
    # Simple video creation with proper audio mapping
    cmd = [
        'ffmpeg', '-i', str(stock_video), 
        '-i', str(audio_path),
        '-vf', "eq=contrast=1.6:brightness=-0.4:gamma=1.4,hue=s=0.5,drawtext=text='ABRAHAM LINCOLN':fontcolor=darkred:fontsize=80:x=(w-text_w)/2:y=50,drawtext=text='S SPECTRAL CURSE':fontcolor=red:fontsize=60:x=(w-text_w)/2:y=150,drawtext=text='SIC SEMPER TYRANNIS':fontcolor=darkred:fontsize=50:x=(w-text_w)/2:y=h-100",
        '-af', 'volume=3.0,loudnorm=I=-16:TP=-1.5:LRA=11',
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', 
        '-c:a', 'aac', '-b:a', '256k',
        '-t', str(duration), '-shortest',
        '-map', '0:v:0', '-map', '1:a:0',
        '-y', str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if output_path.exists():
        print(f"SUCCESS - Video: {output_path.stat().st_size/1024/1024:.2f} MB")
        return True
    return False

def generate():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    print(f"\n{'='*60}\nABRAHAM HORROR VIDEO\n{'='*60}\n")
    
    headlines = get_headlines()
    headline = random.choice(headlines)
    print(f"Headline: {headline}\n")
    
    script = generate_script(headline)
    print(f"Script: {script}\n")
    
    audio_path = BASE_DIR / f"audio/abraham_{timestamp}.mp3"
    if not generate_voice(script, audio_path):
        return None
    
    stock_video = get_stock_video("dark horror")
    
    video_path = BASE_DIR / f"videos/ABRAHAM_{timestamp}.mp4"
    if not create_video(stock_video, audio_path, video_path, headline):
        return None
    
    print(f"\nREADY: {video_path.name}")
    return str(video_path)

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    for i in range(count):
        generate()

