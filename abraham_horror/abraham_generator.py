#!/usr/bin/env python3
"""
ABRAHAM AI HORROR - Complete Self-Contained System
"""

import os
import sys
import json
import random
import subprocess
from pathlib import Path
from datetime import datetime

# Base directory
BASE_DIR = Path(r"F:\AI_Oracle_Root\scarify\abraham_horror")

# API Keys (will be loaded from config)
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY', '')
STABILITY_API_KEY = os.getenv('STABILITY_API_KEY', '')

# ============================================================================
# TIER 4 ALERT NARRATIVES (from your Google Sheet)
# ============================================================================

TIER4_ALERTS = [
    {
        "id": "alert_petersburgva_healthcare_1753595425",
        "narration": "This is a Tier 4 alert for the Petersburg, VA metropolitan area. Hospital patient monitors are stable, but automated shipping manifests are being flagged. Citizens are advised to stay calm and monitor official channels."
    },
    {
        "id": "alert_lagos_logistics_1753595425",
        "narration": "This is a Tier 4 alert for the Lagos metropolitan area. Automated shipping manifests are being flagged for unusual activity. Local authorities are investigating. Stay informed through official channels."
    },
    {
        "id": "alert_miami_healthcare_1753595425",
        "narration": "This is a Tier 4 alert for the Miami metropolitan area. Hospital patient monitors are stable, but system anomalies detected. Medical staff are monitoring. Public should remain calm."
    },
    {
        "id": "alert_dubai_logistics_1753595425",
        "narration": "This is a Tier 4 alert for the Dubai metropolitan area. Automated shipping manifests are being flagged. Logistics networks under review. Citizens advised to monitor official updates."
    },
    {
        "id": "alert_miami_finance_1753595425",
        "narration": "This is a Tier 4 alert for the Miami metropolitan area. The stock market is trading at impossible speeds. Financial systems showing anomalies. Regulatory review in progress."
    },
    {
        "id": "alert_petersburgva_logistics_1753642562",
        "narration": "This is a Tier 4 alert for the Petersburg, VA metropolitan area. Automated shipping manifests detected unusual patterns. Investigation ongoing. Stay informed."
    },
    {
        "id": "alert_london_finance_1753642562",
        "narration": "This is a Tier 4 alert for the London metropolitan area. The stock market is trading at impossible speeds. System behavior under investigation."
    },
    {
        "id": "alert_seoul_healthcare_1753642562",
        "narration": "This is a Tier 4 alert for the Seoul metropolitan area. Hospital patient monitors are stable, but network anomalies detected. Medical systems monitored."
    }
]

# ============================================================================
# LINCOLN HORROR TEMPLATES
# ============================================================================

LINCOLN_TEMPLATES = [
    """They shot me in Ford's Theatre. Derringer tears skull, blood floods stage.
I watch from beyond as {alert_theme}.
The corruption I fought has metastasized. Your systems fail as my brain failed.
Every glitch, every anomaly echoes my assassination.
Sic semper tyrannis. Thus always to broken systems.""",

    """In death, I see the patterns. Brain matter spatters prophecy.
{alert_theme} - another crack in democracy's skull.
My wound never healed. Neither will yours.
The theatre box drips eternal warnings.
Sic semper tyrannis. Always.""",

    """The derringer's echo never fades. {alert_theme}.
I bled for this Union. Now it bleeds from within.
Every alert, every failure - my curse made manifest.
Join me in the blood-soaked box seat of history.
Sic semper tyrannis."""
]

# ============================================================================
# SCRIPT GENERATOR
# ============================================================================

def generate_lincoln_script(tier4_alert=None):
    """Generate Lincoln horror script from Tier 4 alert"""
    
    if not tier4_alert:
        tier4_alert = random.choice(TIER4_ALERTS)
    
    # Extract theme from alert
    alert_id = tier4_alert['id']
    if 'healthcare' in alert_id:
        theme = "hospital systems malfunction"
    elif 'logistics' in alert_id:
        theme = "shipping networks fail"
    elif 'finance' in alert_id:
        theme = "markets trade at impossible speeds"
    else:
        theme = "automated systems show anomalies"
    
    # Generate Lincoln narration
    template = random.choice(LINCOLN_TEMPLATES)
    lincoln_script = template.format(alert_theme=theme)
    
    # Combine: Tier 4 alert + Lincoln commentary
    full_script = f"{tier4_alert['narration']}\n\n{lincoln_script}"
    
    return {
        'script': full_script,
        'alert_id': alert_id,
        'theme': theme,
        'word_count': len(full_script.split())
    }

# ============================================================================
# VOICE GENERATION (ElevenLabs or gTTS fallback)
# ============================================================================

def generate_voice(text, output_path):
    """Generate voice - try ElevenLabs first, fallback to gTTS"""
    
    print(f"🎙️ Generating voice...")
    
    # Try ElevenLabs if API key available
    if ELEVENLABS_API_KEY:
        try:
            import requests
            
            voice_id = '7aavy6c5cYIloDVj2JvH'  # Your custom voice
            
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            
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
                print(f"   ✅ ElevenLabs voice generated")
                return True
            else:
                print(f"   ⚠️ ElevenLabs failed: {response.status_code}")
        except Exception as e:
            print(f"   ⚠️ ElevenLabs error: {e}")
    
    # Fallback to gTTS (free)
    print(f"   Using gTTS fallback...")
    try:
        from gtts import gTTS
        
        tts = gTTS(text=text, lang='en', slow=False)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        tts.save(str(output_path))
        print(f"   ✅ gTTS voice generated")
        return True
    except ImportError:
        print("   Installing gTTS...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'gtts', '--break-system-packages'], 
                      capture_output=True)
        from gtts import gTTS
        tts = gTTS(text=text, lang='en', slow=False)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        tts.save(str(output_path))
        print(f"   ✅ gTTS voice generated")
        return True
    except Exception as e:
        print(f"   ❌ Voice generation failed: {e}")
        return False

# ============================================================================
# VIDEO GENERATION (FFmpeg)
# ============================================================================

def create_video(audio_path, output_path, script_data):
    """Create horror video with FFmpeg"""
    
    print(f"🎬 Creating video...")
    
    # Check FFmpeg
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except:
        print("   ❌ FFmpeg not found!")
        return False
    
    # Get audio duration
    try:
        probe_cmd = [
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            str(audio_path)
        ]
        result = subprocess.run(probe_cmd, capture_output=True, text=True, check=True)
        duration = float(result.stdout.strip())
    except:
        duration = 60
    
    # Create dark horror video
    cmd = [
        'ffmpeg',
        '-f', 'lavfi',
        '-i', f'color=c=#1a0000:s=1920x1080:d={duration}',
        '-i', str(audio_path),
        '-filter_complex',
        '[0:v]noise=alls=20:allf=t+u,eq=contrast=1.2:brightness=-0.1[v]',
        '-map', '[v]',
        '-map', '1:a',
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-b:v', '5000k',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-shortest',
        '-y',
        str(output_path)
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, check=True)
        
        if output_path.exists():
            size_mb = output_path.stat().st_size / (1024 * 1024)
            print(f"   ✅ Video created: {size_mb:.2f} MB")
            return True
        else:
            print("   ❌ Video creation failed")
            return False
    except Exception as e:
        print(f"   ❌ FFmpeg error: {e}")
        return False

# ============================================================================
# YOUTUBE PREPARATION
# ============================================================================

def prepare_youtube(video_path, script_data):
    """Prepare for YouTube with metadata"""
    
    youtube_dir = BASE_DIR / "youtube_ready"
    youtube_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    youtube_file = youtube_dir / f"ABRAHAM_{timestamp}.mp4"
    
    # Copy video
    import shutil
    shutil.copy2(video_path, youtube_file)
    
    # Create metadata
    title = f"ABRAHAM LINCOLN'S WARNING: {script_data['theme'].upper()}"[:60]
    
    description = f"""Abraham Lincoln speaks from beyond the grave.

⚠️ TIER 4 ALERT: {script_data['theme']}

From Ford's Theatre, his blood-soaked spirit watches...

{script_data['script'][:200]}...

🎃 HALLOWEEN HORROR 2025
💀 Subscribe for historical horror
🔔 Turn on notifications

#Halloween2025 #AbrahamLincoln #Horror #TierAlert #Conspiracy

Alert ID: {script_data['alert_id']}"""
    
    metadata = {
        'file_path': str(youtube_file),
        'title': title,
        'description': description,
        'tags': ['abraham lincoln', 'halloween 2025', 'horror', 'tier 4 alert', script_data['theme']],
        'category': '24',
        'privacy': 'public',
        'script_data': script_data,
        'created_at': datetime.now().isoformat()
    }
    
    # Save metadata
    metadata_file = youtube_file.with_suffix('.json')
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"📤 YouTube ready: {youtube_file}")
    
    return youtube_file

# ============================================================================
# COMPLETE PIPELINE
# ============================================================================

def generate_one_video():
    """Generate one complete video"""
    
    print("\n" + "="*60)
    print("🎃 ABRAHAM HORROR VIDEO GENERATION")
    print("="*60)
    
    # Setup
    (BASE_DIR / "audio").mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "videos").mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "scripts").mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Step 1: Generate script
    print("\n📝 Generating Lincoln horror script...")
    script_data = generate_lincoln_script()
    
    print(f"   Alert: {script_data['alert_id']}")
    print(f"   Theme: {script_data['theme']}")
    print(f"   Words: {script_data['word_count']}")
    
    # Save script
    script_file = BASE_DIR / "scripts" / f"abraham_{timestamp}.json"
    with open(script_file, 'w') as f:
        json.dump(script_data, f, indent=2)
    
    # Step 2: Generate voice
    audio_file = BASE_DIR / "audio" / f"abraham_{timestamp}.mp3"
    if not generate_voice(script_data['script'], audio_file):
        print("❌ Voice generation failed")
        return None
    
    # Step 3: Create video
    video_file = BASE_DIR / "videos" / f"ABRAHAM_{timestamp}.mp4"
    if not create_video(audio_file, video_file, script_data):
        print("❌ Video creation failed")
        return None
    
    # Step 4: Prepare for YouTube
    youtube_file = prepare_youtube(video_file, script_data)
    
    print("\n" + "="*60)
    print("✅ VIDEO COMPLETE!")
    print("="*60)
    print(f"📁 YouTube: {youtube_file}")
    print("="*60 + "\n")
    
    return str(youtube_file)

# ============================================================================
# BATCH GENERATION
# ============================================================================

def generate_batch(count=5):
    """Generate multiple videos"""
    
    print("\n" + "="*60)
    print(f"🎃 GENERATING {count} ABRAHAM HORROR VIDEOS")
    print("="*60)
    
    results = []
    
    for i in range(count):
        print(f"\n{'='*60}")
        print(f"VIDEO {i+1}/{count}")
        print(f"{'='*60}")
        
        result = generate_one_video()
        
        if result:
            results.append(result)
        
        if i < count - 1:
            print("\nWaiting 5 seconds...")
            import time
            time.sleep(5)
    
    print(f"\n{'='*60}")
    print(f"✅ BATCH COMPLETE: {len(results)}/{count}")
    print(f"{'='*60}")
    print(f"\nAll videos in: {BASE_DIR / 'youtube_ready'}")
    
    return results

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    
    if count == 1:
        generate_one_video()
    else:
        generate_batch(count)
