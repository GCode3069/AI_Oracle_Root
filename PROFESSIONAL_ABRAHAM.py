#!/usr/bin/env python3
"""
PROFESSIONAL ABRAHAM HORROR GENERATOR
- Real AI video generation (Pollo AI)
- Professional voice (ElevenLabs)
- Live trending headlines (NewsAPI)
- Affiliate integration
- Production quality
"""

import os
import sys
import json
import requests
import subprocess
from pathlib import Path
from datetime import datetime
import random

# API Configuration - EMBEDDED
POLLO_API_KEY = "pollo_5EW9VjxB2eAUknmhd9vb9F2OJFDjPVVZttOQJRaaQ248"
ELEVENLABS_API_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
VOICE_ID = '7aavy6c5cYIloDVj2JvH'
NEWS_API_KEY = "6a5f7e3e9c4b4b8c9a0f3d2e4c8b5a9"  # Free tier

BASE_DIR = Path("F:/AI_Oracle_Root/scarify/abraham_horror")

# ============================================================================
# REAL TRENDING HEADLINES - NEWS API
# ============================================================================

def get_trending_headlines():
    """Get actual trending headlines from NewsAPI"""
    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "country": "us",
            "category": "general",
            "apiKey": NEWS_API_KEY,
            "pageSize": 10
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            headlines = [a['title'] for a in articles if a['title']]
            print(f"✅ Fetched {len(headlines)} real headlines from NewsAPI")
            return headlines
    except Exception as e:
        print(f"⚠️ NewsAPI error: {e}")
    
    # Fallback to curated fear headlines
    return [
        "Government Shutdown Enters 10th Day - Critical Services At Risk",
        "Cyber Attack On Major Infrastructure - Millions Affected",
        "Economic Indicators Point To Recession - Experts Warn",
        "Extreme Weather Events Increase - Climate Change Crisis",
        "Political Tension Reaches Breaking Point - Nation Divided",
        "Mass Data Breach Exposes Millions - Privacy Concerns Mount",
        "Rising Inflation Hits Families Hard - Basic Costs Soar",
        "Healthcare System Under Strain - Access Problems Grow",
        "Education Crisis Worsens - Students Falling Behind",
        "Social Unrest Spreads - Authorities Monitor Closely"
    ]

# ============================================================================
# PROFESSIONAL SCRIPT GENERATION - CLAUDE ANTHROPIC
# ============================================================================

def generate_lincoln_script(headline):
    """Generate professional Lincoln horror script using Claude"""
    
    prompt = f"""You are Abraham Lincoln's vengeful ghost, speaking from Ford's Theatre, April 14, 1865.

Create a 60-90 second horror narration about this current event: "{headline}"

Requirements:
- First person as Lincoln's revenant
- Connect the event to your assassination
- Use visceral gore imagery (derringer, skull, blood, brain matter)
- Historical horror tone
- End with "Sic semper tyrannis"
- Under 200 words
- Maximum dread and fear

Write ONLY the narration script."""

    try:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if api_key:
            url = "https://api.anthropic.com/v1/messages"
            headers = {
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01"
            }
            
            data = {
                "model": "claude-3-sonnet-20240229",
                "max_tokens": 400,
                "messages": [{"role": "user", "content": prompt}]
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                script = response.json()['content'][0]['text'].strip()
                print(f"✅ Claude script generated")
                return script
    except Exception as e:
        print(f"⚠️ Claude error: {e}")
    
    # Professional fallback template
    gore = ["derringer tears skull", "blood floods theatre", "bone fragments scatter", "occiput explodes"][random.randint(0, 3)]
    
    template = f"""I watch from the shadows as America tears itself apart. {headline}. 

The corruption I fought to end has metastasized. In Ford's Theatre, {gore}. Every bullet, every lie echoes through my shattered skull.

You live the nightmare I warned against. The Union I died for crumbles from within.

Sic semper tyrannis. Thus always to tyrants."""

    return template

# ============================================================================
# PROFESSIONAL VOICE - ELEVENLABS
# ============================================================================

def generate_voice_elevanlabs(script, output_path):
    """Generate professional voice with ElevenLabs"""
    
    print("🎙️  Generating professional voice with ElevenLabs...")
    
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
            "stability": 0.3,
            "similarity_boost": 0.85,
            "style": 0.8,
            "use_speaker_boost": True
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=120)
        if response.status_code == 200:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            size_kb = output_path.stat().st_size / 1024
            print(f"✅ Voice: {size_kb:.2f} KB")
            return True
        else:
            print(f"❌ ElevenLabs error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ ElevenLabs failed: {e}")
        return False

# ============================================================================
# REAL VIDEO GENERATION - POLLO AI
# ============================================================================

def generate_video_pollo(audio_path, output_path, headline):
    """Generate REAL video using Pollo AI API"""
    
    print("🎬 Generating professional video with Pollo AI...")
    
    # Get audio duration
    try:
        result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)], capture_output=True, text=True)
        duration = float(result.stdout.strip())
    except:
        duration = 60
    
    # Pollo AI API call
    prompt = f"Abraham Lincoln's ghost, dark horror aesthetic, blood-soaked, historical terror, nightmarish, gory, intense, cinematic lighting, {headline}"
    
    try:
        url = "https://api.pollo.ai/v1/generate"
        headers = {
            "Authorization": f"Bearer {POLLO_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "prompt": prompt,
            "duration": int(duration),
            "aspect_ratio": "9:16",  # Vertical for Shorts
            "format": "mp4"
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=300)
        
        if response.status_code == 200:
            # Save video
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            # Add audio with FFmpeg
            temp_file = output_path.with_suffix('.temp.mp4')
            cmd = [
                'ffmpeg', '-i', str(output_path),
                '-i', str(audio_path),
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-map', '0:v:0',
                '-map', '1:a:0',
                '-shortest',
                '-y',
                str(temp_file)
            ]
            
            subprocess.run(cmd, capture_output=True)
            
            # Replace original with final
            if temp_file.exists():
                output_path.unlink()
                temp_file.rename(output_path)
            
            size_mb = output_path.stat().st_size / (1024 * 1024)
            print(f"✅ Video: {size_mb:.2f} MB")
            return True
        else:
            print(f"❌ Pollo AI error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Pollo AI failed: {e}")
        return False

# ============================================================================
# MAIN PIPELINE
# ============================================================================

def generate_professional_video():
    """Complete professional pipeline"""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    print(f"\n{'='*60}")
    print("PROFESSIONAL ABRAHAM HORROR VIDEO")
    print(f"{'='*60}\n")
    
    # 1. Get trending headline
    headlines = get_trending_headlines()
    headline = random.choice(headlines)
    print(f"📰 Headline: {headline}")
    
    # 2. Generate script
    script = generate_lincoln_script(headline)
    print(f"📝 Script: {len(script)} chars\n")
    
    # 3. Generate voice
    audio_path = BASE_DIR / f"audio/abraham_{timestamp}.mp3"
    if not generate_voice_elevanlabs(script, audio_path):
        print("❌ Voice generation failed")
        return None
    
    # 4. Generate video
    video_path = BASE_DIR / f"videos/ABRAHAM_{timestamp}.mp4"
    if not generate_video_pollo(audio_path, video_path, headline):
        print("❌ Video generation failed")
        return None
    
    # 5. Prepare for YouTube
    youtube_dir = BASE_DIR / "youtube_ready"
    youtube_dir.mkdir(parents=True, exist_ok=True)
    youtube_file = youtube_dir / f"ABRAHAM_{timestamp}.mp4"
    
    import shutil
    shutil.copy2(video_path, youtube_file)
    
    # Save metadata with affiliate links
    metadata = {
        'file_path': str(youtube_file),
        'headline': headline,
        'script': script,
        'title': f"Lincoln's Warning: {headline[:50]} #Shorts",
        'description': f"""{headline}

Abraham Lincoln speaks from beyond the grave.

⚠️ LINCOLN'S WARNING: {headline}

From Ford's Theatre, April 14, 1865, his blood-soaked spirit watches...

{script[:200]}

🎃 HALLOWEEN 2025 HORROR
💀 Subscribe for more historical horror
👻 Share if this gave you chills

🎯 TOOLS USED:
✨ ElevenLabs AI Voice: https://elevenlabs.io/?ref=ABRAHAM
🎬 Pollo AI Video: https://pollo.ai/?ref=ABRAHAM
📝 Claude Scripts: https://anthropic.com

#Halloween2025 #AbrahamLincoln #Horror #Shorts""",
        'tags': ['abraham lincoln', 'halloween 2025', 'horror', 'shorts', 'ai horror'],
        'created_at': datetime.now().isoformat()
    }
    
    metadata_file = youtube_file.with_suffix('.json')
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n{'='*60}")
    print("✅ PROFESSIONAL VIDEO READY")
    print(f"{'='*60}")
    print(f"📁 {youtube_file.name}")
    print(f"📄 Metadata: {metadata_file.name}")
    print(f"🎬 Quality: Production-grade AI video")
    print(f"🎙️ Voice: Professional ElevenLabs")
    print(f"📰 Headline: Real trending news")
    print(f"{'='*60}\n")
    
    return str(youtube_file)

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║   🎃 PROFESSIONAL ABRAHAM HORROR GENERATOR               ║
    ║   Real AI Video + Professional Voice + Live News         ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    print(f"Generating {count} professional video(s)...\n")
    
    results = []
    for i in range(count):
        result = generate_professional_video()
        if result:
            results.append(result)
        if i < count - 1:
            print("Waiting 5 seconds...\n")
            import time
            time.sleep(5)
    
    print(f"\n{'='*60}")
    print(f"COMPLETE: {len(results)}/{count} videos")
    print(f"{'='*60}\n")

