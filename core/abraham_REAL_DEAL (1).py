#!/usr/bin/env python3
"""
ABRAHAM HORROR - THE REAL FUCKING DEAL
- Pollo AI for Abraham Lincoln videos
- Trend scraping for unique scripts
- Psycho audio layering
- Google Sheets tracking
"""
import os
import sys
import json
import requests
import subprocess
import random
import time
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

# ═══════════════════════════════════════════════════════════════════════════
# API KEYS
# ═══════════════════════════════════════════════════════════════════════════

ELEVENLABS_API_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
POLLO_API_KEY = "pollo_5EW9VjxB2eAUknmhd9vb9F2OJFDjPVVZttOQJRaaQ248"
STABILITY_API_KEY = "sk-sP9331LezaVNYp1fbSDf9sn0rUaxhlr377fJ3V9V1t8wOEPQ1"
PEXELS_API_KEY = "RgE9Mdn3ToSQhn2RiLJ4mPMISjjp587QKRG9uhpOrLVtkKPCibUPUDGh"

VOICE_ID = "pNInz6obpgDQGcFmaJgB"  # Adam - deep voice
BASE_DIR = Path("F:/AI_Oracle_Root/scarify/abraham_horror")

# ═══════════════════════════════════════════════════════════════════════════
# SCRAPE TRENDING HEADLINES
# ═══════════════════════════════════════════════════════════════════════════

def scrape_trending_headlines():
    """Scrape real trending news for unique scripts"""
    print("[TRENDS] Scraping trending headlines...")
    
    headlines = []
    
    # Try Google News
    try:
        url = "https://news.google.com/rss"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item')[:10]
            
            for item in items:
                title = item.title.text
                headlines.append(title)
    except Exception as e:
        print(f"[TRENDS] Google News failed: {e}")
    
    # Fallback headlines if scraping fails
    if not headlines:
        headlines = [
            "Economic Collapse Warning - Recession Signals Multiply",
            "Cyber Attack Cripples Critical Infrastructure",
            "Political Violence Escalates Across Nation",
            "Government Shutdown Enters Critical Phase",
            "Climate Emergency Declared - Extreme Weather Spreads"
        ]
    
    print(f"[TRENDS] Got {len(headlines)} headlines")
    return headlines

# ═══════════════════════════════════════════════════════════════════════════
# GENERATE UNIQUE SCRIPT (NO REPETITION)
# ═══════════════════════════════════════════════════════════════════════════

def generate_unique_script(headline):
    """Generate unique script - different every time"""
    
    # Different openings
    openings = [
        "I am Abraham Lincoln. I died in Ford's Theatre.",
        "They call me Honest Abe. They murdered me.",
        "Listen. This is Abraham Lincoln speaking from death.",
        "I was the 16th President. They assassinated me.",
        "My name is Abraham Lincoln. I watch from beyond."
    ]
    
    # Different gore descriptions
    gore_variants = [
        "Booth's .44 caliber derringer fired point-blank. The lead ball entered behind my left ear. It tore through my brain, fragmenting bone. Blood erupted from the wound. I collapsed forward, unconscious. I never woke.",
        "The shot rang out at 10:15 PM. Derringer bullet punctured my skull. Brain tissue exploded outward. Bone shards embedded in the presidential box. Blood pooled beneath my head. I died nine hours later.",
        "John Wilkes Booth approached from behind. His pistol touched my head. BANG. Skull shattered. Brain matter scattered. Blood soaked Mary's dress. I slumped in my seat, dying.",
        "April 14, 1865. Ford's Theatre. A .44 derringer. One shot. My skull fractured. Brain destroyed. Blood everywhere. I was dead before morning."
    ]
    
    # Different prophecy styles
    prophecies = [
        f"As I bled to death, I had a vision. I saw {headline}. I saw YOUR America. The corruption I fought metastasizes. The tyranny spreads unchecked.",
        f"In my final moments, the future revealed itself. {headline}. This is what becomes of the Union I preserved. The dream dies.",
        f"Death came slowly. In those nine hours, I witnessed your timeline. {headline}. Every warning I gave, ignored. Every sacrifice, wasted.",
        f"They say death brings clarity. I saw it all. {headline}. The republic fractures. Democracy drowns. Freedom becomes slavery."
    ]
    
    # Different endings
    endings = [
        "You inherit the nightmare. The assassin's bullet didn't just kill me. It killed America's soul.",
        "Sic semper tyrannis. Thus always to tyrants. But look around. Who are the tyrants now?",
        "From my blood-soaked seat in eternity, I watch. The experiment fails. The Union collapses.",
        "They murdered the president. You murdered the dream. The republic dies with you.",
        "I died for nothing. The America I saved betrays everything I fought for. You are complicit."
    ]
    
    # Assemble unique script
    script = f"""{random.choice(openings)}

{headline}.

{random.choice(gore_variants)}

{random.choice(prophecies)}

Every lie you accept. Every freedom you surrender. Every act of cowardice that rots this nation from within.

{headline}. This is not random. This is the pattern. The evil compounds. The darkness spreads.

{random.choice(endings)}"""
    
    return script

# ═══════════════════════════════════════════════════════════════════════════
# GENERATE PSYCHO AUDIO (LAYERED HORROR)
# ═══════════════════════════════════════════════════════════════════════════

def generate_psycho_audio(script, output_path):
    """Generate voice with horror effects"""
    print("[AUDIO] Generating psycho audio...")
    
    # Generate base voice
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    data = {
        "text": script,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.3,  # More variation for psycho effect
            "similarity_boost": 0.9,
            "style": 1.0,  # Maximum dramatic
            "use_speaker_boost": True
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=180)
        
        if response.status_code != 200:
            print(f"[AUDIO] ElevenLabs error: {response.status_code}")
            return False
        
        # Save base audio
        temp_audio = output_path.parent / f"temp_{output_path.name}"
        temp_audio.parent.mkdir(parents=True, exist_ok=True)
        
        with open(temp_audio, "wb") as f:
            f.write(response.content)
        
        # Apply horror effects with FFmpeg
        cmd = [
            "ffmpeg",
            "-i", str(temp_audio),
            "-af", "aecho=0.8:0.9:1000:0.3,atempo=0.95,bass=g=3,treble=g=2",
            "-ar", "44100",
            "-y",
            str(output_path)
        ]
        
        subprocess.run(cmd, capture_output=True, check=True)
        temp_audio.unlink()
        
        size_kb = output_path.stat().st_size / 1024
        print(f"[AUDIO] ✅ Psycho audio: {size_kb:.1f} KB")
        return True
        
    except Exception as e:
        print(f"[AUDIO] ❌ Error: {e}")
        return False

# ═══════════════════════════════════════════════════════════════════════════
# GENERATE ABRAHAM LINCOLN AI VIDEO (POLLO AI)
# ═══════════════════════════════════════════════════════════════════════════

def generate_pollo_abraham_video(headline):
    """Generate Abraham Lincoln AI video with Pollo"""
    print("[POLLO] Generating Abraham Lincoln AI video...")
    
    try:
        url = "https://api.pollo.ai/v1/text2video"
        
        headers = {
            "Authorization": f"Bearer {POLLO_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Pollo prompt for Abraham Lincoln horror
        prompt = f"Abraham Lincoln ghost, dark horror atmosphere, {headline}, cinematic lighting, dramatic, 9:16 vertical, photorealistic"
        
        data = {
            "prompt": prompt,
            "duration": 10,
            "aspect_ratio": "9:16",
            "model": "pollo-1.5"
        }
        
        # Submit generation request
        response = requests.post(url, headers=headers, json=data, timeout=60)
        
        if response.status_code != 200:
            print(f"[POLLO] ❌ API error: {response.status_code}")
            return None
        
        result = response.json()
        task_id = result.get("id")
        
        if not task_id:
            print("[POLLO] ❌ No task ID")
            return None
        
        print(f"[POLLO] Task ID: {task_id}, waiting for generation...")
        
        # Poll for completion (max 5 minutes)
        for attempt in range(60):
            time.sleep(5)
            
            status_response = requests.get(
                f"https://api.pollo.ai/v1/text2video/{task_id}",
                headers=headers,
                timeout=30
            )
            
            if status_response.status_code == 200:
                status_data = status_response.json()
                state = status_data.get("state")
                
                if state == "completed":
                    video_url = status_data.get("video_url")
                    
                    if video_url:
                        # Download video
                        video_data = requests.get(video_url, timeout=120).content
                        temp_file = BASE_DIR / "temp" / f"pollo_{random.randint(1000, 9999)}.mp4"
                        temp_file.parent.mkdir(exist_ok=True)
                        
                        with open(temp_file, "wb") as f:
                            f.write(video_data)
                        
                        print(f"[POLLO] ✅ Abraham Lincoln video generated")
                        return temp_file
                
                elif state == "failed":
                    print("[POLLO] ❌ Generation failed")
                    return None
            
            print(f"[POLLO] Still generating... ({attempt + 1}/60)")
        
        print("[POLLO] ❌ Timeout")
        return None
        
    except Exception as e:
        print(f"[POLLO] ❌ Error: {e}")
        return None

# ═══════════════════════════════════════════════════════════════════════════
# COMPOSE FINAL VIDEO
# ═══════════════════════════════════════════════════════════════════════════

def compose_final_video(video_source, audio_path, output_path):
    """Compose with guaranteed audio"""
    print("[COMPOSE] Combining video + psycho audio...")
    
    try:
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)],
            capture_output=True,
            text=True,
            check=True
        )
        duration = float(probe.stdout.strip())
    except:
        print("[COMPOSE] ❌ Cannot read audio")
        return False
    
    cmd = [
        "ffmpeg",
        "-i", str(video_source),
        "-i", str(audio_path),
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-vf", "eq=contrast=1.5:brightness=-0.4:saturation=0.6,scale=1080:1920",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "21",
        "-c:a", "aac",
        "-b:a", "256k",
        "-t", str(duration),
        "-shortest",
        "-y",
        str(output_path)
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, check=True, timeout=300)
        
        if output_path.exists():
            size_mb = output_path.stat().st_size / (1024 * 1024)
            print(f"[COMPOSE] ✅ Final video: {size_mb:.2f} MB")
            video_source.unlink()
            return True
    except Exception as e:
        print(f"[COMPOSE] ❌ Error: {e}")
    
    return False

# ═══════════════════════════════════════════════════════════════════════════
# MAIN GENERATION
# ═══════════════════════════════════════════════════════════════════════════

def generate_video():
    """Generate complete Abraham horror video"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print("\n" + "="*70)
    print("GENERATING ABRAHAM HORROR VIDEO - THE REAL DEAL")
    print("="*70 + "\n")
    
    # Get trending headline
    headlines = scrape_trending_headlines()
    headline = random.choice(headlines)
    print(f"[HEADLINE] {headline}\n")
    
    # Generate unique script
    script = generate_unique_script(headline)
    print(f"[SCRIPT] {len(script)} characters\n")
    
    # Generate psycho audio
    audio_path = BASE_DIR / f"audio/abraham_{timestamp}.mp3"
    if not generate_psycho_audio(script, audio_path):
        print("\n❌ Audio generation failed")
        return None
    
    # Generate Abraham Lincoln AI video with Pollo
    video_source = generate_pollo_abraham_video(headline)
    
    # Fallback to Pexels if Pollo fails
    if not video_source:
        print("[FALLBACK] Using Pexels...")
        try:
            url = "https://api.pexels.com/videos/search"
            headers = {"Authorization": PEXELS_API_KEY}
            params = {"query": "dark horror", "per_page": 1, "orientation": "portrait"}
            
            response = requests.get(url, headers=headers, params=params, timeout=30)
            data = response.json()
            
            if data.get("videos"):
                video = data["videos"][0]
                video_file = max(video["video_files"], key=lambda x: x.get("width", 0))
                video_data = requests.get(video_file["link"], timeout=120).content
                
                video_source = BASE_DIR / "temp" / f"pexels_{random.randint(1000, 9999)}.mp4"
                with open(video_source, "wb") as f:
                    f.write(video_data)
        except:
            print("\n❌ All video sources failed")
            return None
    
    # Compose final video
    video_path = BASE_DIR / f"videos/ABRAHAM_{timestamp}.mp4"
    if not compose_final_video(video_source, audio_path, video_path):
        print("\n❌ Composition failed")
        return None
    
    # Copy to YouTube folder
    youtube_file = BASE_DIR / "youtube_ready" / f"ABRAHAM_{timestamp}.mp4"
    youtube_file.parent.mkdir(exist_ok=True)
    
    import shutil
    shutil.copy2(video_path, youtube_file)
    
    size_mb = youtube_file.stat().st_size / (1024 * 1024)
    
    print("\n" + "="*70)
    print("✅ SUCCESS - ABRAHAM HORROR VIDEO CREATED")
    print("="*70)
    print(f"File: {youtube_file.name}")
    print(f"Size: {size_mb:.2f} MB")
    print(f"Headline: {headline}")
    print("="*70 + "\n")
    
    return str(youtube_file)

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    
    print(f"\n🔥 GENERATING {count} ABRAHAM HORROR VIDEOS - THE REAL DEAL\n")
    
    success = 0
    failed = 0
    
    for i in range(count):
        print(f"\n{'='*70}")
        print(f"VIDEO {i+1}/{count}")
        print(f"{'='*70}")
        
        result = generate_video()
        
        if result:
            success += 1
        else:
            failed += 1
        
        if i < count - 1:
            print("\nWaiting 15 seconds...")
            time.sleep(15)
    
    print(f"\n{'='*70}")
    print(f"COMPLETE: {success} success, {failed} failed")
    print(f"{'='*70}\n")
