#!/usr/bin/env python3
import os
import sys
import json
import random
import time
from pathlib import Path
from datetime import datetime

# EMBEDDED API KEYS
os.environ['POLLO_API_KEY'] = 'pollo_5EW9VjxB2eAUknmhd9vb9F2OJFDjPVVZttOQJRaaQ248'
os.environ['ELEVENLABS_API_KEY'] = '3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa'
os.environ['STABILITY_API_KEY_1'] = 'sk-sP9******************pQi'
os.environ['STABILITY_API_KEY_2'] = 'sk-6JW******************P5m'

POLLO_API_KEY = os.getenv('POLLO_API_KEY')
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')

BASE_DIR = Path(r"F:\AI_Oracle_Root\scarify\abraham_studio")

# Fear headlines
HEADLINES = {
    'government': [
        "Corrupt Officials Hit 69% Fear - Government Rot Exposed",
        "ICE Raids Spread Terror - Communities Hide in Fear",
        "Shutdown Day 10 - Government Collapse Imminent",
        "Trump's Antifa Warning - Civil War Fears Mount"
    ],
    'economy': [
        "Economic Collapse - 58.2% Fear Total System Failure",
        "Bitcoin Death Spiral - Crypto is Dead Say Experts",
        "Foreclosure Crisis Exploding - Housing Market Collapse",
        "Markets Trading at Impossible Speeds - System Glitch"
    ],
    'cyber': [
        "Cyber-Terrorism Surge - 55.9% Americans Terrified",
        "Gmail Hack Exposes 183M - Your Data Leaked",
        "AI Systems Unauthorized Behavior - Machines Revolt",
        "Hospital Monitors Hacked - Lives at Risk"
    ]
}

LINCOLN_TEMPLATES = [
    """They shot me in Ford's Theatre. {gore}
I watch as {theme}.
Your systems fail as my brain failed.
Every glitch echoes my assassination.
Sic semper tyrannis.
$97 Purge Kit: ElevenLabs clone + Pollo gore.""",

    """The derringer's echo never fades. {gore}
{theme} - another bullet through democracy.
I bled for this Union. Now it bleeds from within.
Sic semper tyrannis.
Tools that bleed truth: $97 Kit.""",

    """In death, I see clearly. {gore}
{theme} is the wound that never heals.
The theatre box drips eternal warnings.
Sic semper tyrannis.
Clone the curse: $97."""
]

GORE = [
    "Derringer tears skull, blood floods stage",
    "Brain matter spatters velvet curtain",
    "Jaw unhinges, death rattle echoes",
    "Fingers probe wound, dislodge clot",
    "Skull fragments grind, copper stench"
]

def generate_script(category='government'):
    headline = random.choice(HEADLINES[category])
    template = random.choice(LINCOLN_TEMPLATES)
    gore = random.choice(GORE)
    
    if 'official' in headline.lower():
        theme = "corrupt officials feast on fear"
    elif 'bitcoin' in headline.lower():
        theme = "your digital gold turns to ash"
    elif 'cyber' in headline.lower():
        theme = "machines turn against masters"
    else:
        theme = "systems crumble like my skull"
    
    script = template.format(gore=gore, theme=theme)
    
    return {
        'headline': headline,
        'script': script,
        'category': category,
        'gore': gore
    }

def generate_voice(text, output_path):
    print("🎙️ Generating voice...")
    
    try:
        import requests
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/7aavy6c5cYIloDVj2JvH"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }
        
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.3,
                "similarity_boost": 0.85,
                "style": 0.8,
                "use_speaker_boost": True
            }
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=120)
        
        if response.status_code == 200:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print("   ✅ ElevenLabs voice")
            return True
        else:
            print(f"   ⚠️ ElevenLabs failed, using gTTS...")
            return generate_gtts(text, output_path)
    except Exception as e:
        print(f"   ⚠️ Using gTTS fallback...")
        return generate_gtts(text, output_path)

def generate_gtts(text, output_path):
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang='en', slow=False)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        tts.save(str(output_path))
        print("   ✅ gTTS voice")
        return True
    except:
        print("   Installing gTTS...")
        import subprocess
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'gtts', '--break-system-packages'], 
                      capture_output=True)
        from gtts import gTTS
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(str(output_path))
        print("   ✅ gTTS voice")
        return True

def generate_video_pollo(prompt, audio_path, output_path):
    print("🎬 Pollo AI video generation...")
    
    if not POLLO_API_KEY:
        print("   ❌ No Pollo key!")
        return False
    
    try:
        import requests
        import subprocess
        
        # Generate video
        url = "https://api.pollo.ai/v1/video/generate"
        
        headers = {
            "Authorization": f"Bearer {POLLO_API_KEY}",
            "Content-Type": "application/json"
        }
        
        enhanced_prompt = f"{prompt}. Dark horror aesthetic, blood red lighting, nightmare quality, vertical 9:16 format"
        
        data = {
            "prompt": enhanced_prompt,
            "duration": 15,
            "aspect_ratio": "9:16"
        }
        
        print("   🔄 Requesting video from Pollo AI...")
        response = requests.post(url, json=data, headers=headers, timeout=180)
        
        if response.status_code == 200:
            result = response.json()
            
            # Get video URL
            if 'video_url' in result:
                video_url = result['video_url']
            elif 'url' in result:
                video_url = result['url']
            elif 'output' in result:
                video_url = result['output']
            else:
                print(f"   ⚠️ Response: {result}")
                return False
            
            print(f"   📥 Downloading video...")
            video_response = requests.get(video_url, timeout=180)
            
            # Save silent video
            silent_video = output_path.with_suffix('.silent.mp4')
            silent_video.parent.mkdir(parents=True, exist_ok=True)
            with open(silent_video, 'wb') as f:
                f.write(video_response.content)
            
            print(f"   🎵 Merging audio...")
            
            # Merge audio
            cmd = [
                'ffmpeg',
                '-i', str(silent_video),
                '-i', str(audio_path),
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-shortest',
                '-y',
                str(output_path)
            ]
            
            subprocess.run(cmd, capture_output=True, check=True)
            
            # Cleanup
            silent_video.unlink()
            
            print(f"   ✅ Video ready")
            return True
        else:
            print(f"   ❌ Pollo error: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def generate_metadata(script_data):
    headline = script_data['headline']
    
    title = f"LINCOLN'S WARNING: {headline.upper()}"[:60]
    
    description = f"""Abraham Lincoln speaks from beyond the grave.

⚠️ WARNING: {headline}

{script_data['script'][:250]}...

🔥 PURGE KIT ($97):
• ElevenLabs Voice Clone: https://elevenlabs.io/?ref=scarify
• Pollo AI Video Gen: https://pollo.ai/?ref=scarify
• Writesonic Scripts: https://writesonic.com/?ref=scarify

🎃 HALLOWEEN HORROR 2025
💀 Subscribe for more
🔔 Turn on notifications

#Halloween2025 #AbrahamLincoln #Horror #Conspiracy #{script_data['category'].title()}"""
    
    tags = [
        'abraham lincoln',
        'halloween 2025',
        'horror',
        'scary',
        script_data['category'],
        'conspiracy',
        'viral horror',
        'historical',
        'scarify'
    ]
    
    return {
        'title': title,
        'description': description,
        'tags': tags
    }

def generate_one_video(category='government'):
    print("\n" + "="*60)
    print("🎃 VIDEO GENERATION")
    print("="*60)
    
    (BASE_DIR / "audio").mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "videos").mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "youtube_ready").mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Generate script
    print("\n📝 Script generation...")
    script_data = generate_script(category)
    print(f"   Headline: {script_data['headline'][:50]}...")
    
    # Generate voice
    audio_file = BASE_DIR / "audio" / f"abraham_{timestamp}.mp3"
    if not generate_voice(script_data['script'], audio_file):
        print("❌ Voice failed")
        return None
    
    # Generate video
    video_prompt = f"Abraham Lincoln ghost, {script_data['gore']}, dark horror nightmare"
    video_file = BASE_DIR / "videos" / f"ABRAHAM_{timestamp}.mp4"
    
    if not generate_video_pollo(video_prompt, audio_file, video_file):
        print("❌ Video failed")
        return None
    
    # Prepare for YouTube
    youtube_file = BASE_DIR / "youtube_ready" / f"ABRAHAM_{timestamp}.mp4"
    import shutil
    shutil.copy2(video_file, youtube_file)
    
    metadata = generate_metadata(script_data)
    metadata_file = youtube_file.with_suffix('.json')
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("\n" + "="*60)
    print("✅ VIDEO COMPLETE")
    print("="*60)
    print(f"📁 {youtube_file.name}")
    
    return str(youtube_file)

def generate_batch(count=10):
    print("\n" + "="*60)
    print(f"🎃 GENERATING {count} VIDEOS")
    print("="*60)
    
    results = []
    categories = list(HEADLINES.keys())
    
    for i in range(count):
        print(f"\n{'='*60}")
        print(f"VIDEO {i+1}/{count}")
        print(f"{'='*60}")
        
        cat = categories[i % len(categories)]
        result = generate_one_video(cat)
        
        if result:
            results.append(result)
        
        if i < count - 1:
            print("\nWaiting 5 seconds...")
            time.sleep(5)
    
    print(f"\n{'='*60}")
    print(f"✅ BATCH COMPLETE: {len(results)}/{count}")
    print(f"{'='*60}")
    
    return results

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    
    if count == 1:
        generate_one_video()
    else:
        generate_batch(count)
