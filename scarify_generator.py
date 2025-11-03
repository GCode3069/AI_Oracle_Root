#!/usr/bin/env python3
"""
SCARIFY Complete Video Generator - Embedded in Bootstrap
Generates videos with ElevenLabs voice + FFmpeg
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

# Configuration from PowerShell
VOICE_ID = '7aavy6c5cYIloDVj2JvH'
API_KEY = os.getenv('ELEVENLABS_API_KEY', '')
BASE_DIR = Path("F:/AI_Oracle_Root/scarify")

def setup_dirs():
    """Create all necessary directories"""
    dirs = [
        BASE_DIR / "audio",
        BASE_DIR / "videos/generated",
        BASE_DIR / "videos/youtube_ready",
        BASE_DIR / "temp",
        BASE_DIR / "logs"
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

def generate_voice(text, output_path):
    """Generate voice with ElevenLabs API"""
    if not API_KEY:
        print("❌ API key not set!")
        return False
    
    try:
        import requests
    except ImportError:
        print("Installing requests...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'requests', '--break-system-packages'], 
                      capture_output=True)
        import requests
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": API_KEY
    }
    
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.75,
            "style": 0.6,
            "use_speaker_boost": True
        }
    }
    
    print(f"🎙️ Generating voice...")
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=60)
        
        if response.status_code == 200:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            size_kb = output_path.stat().st_size / 1024
            print(f"✅ Voice generated: {size_kb:.2f} KB")
            return True
        else:
            print(f"❌ API Error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_video(audio_path, output_path):
    """Create video with FFmpeg"""
    
    # Check FFmpeg
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except:
        print("❌ FFmpeg not found!")
        return False
    
    print(f"🎬 Creating video...")
    
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
        duration = 30
    
    # Create video
    cmd = [
        'ffmpeg',
        '-f', 'lavfi',
        '-i', f'color=c=#0a0a0a:s=1920x1080:d={duration}',
        '-i', str(audio_path),
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
            print(f"✅ Video created: {size_mb:.2f} MB, {duration:.1f}s")
            return True
        else:
            print("❌ Video creation failed")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def prepare_for_youtube(video_path):
    """Copy to YouTube ready folder with metadata"""
    
    youtube_file = BASE_DIR / "videos/youtube_ready" / f"YT_{video_path.name}"
    
    import shutil
    shutil.copy2(video_path, youtube_file)
    
    metadata = {
        'title': f"SCARIFY Horror Story - {datetime.now().strftime('%Y-%m-%d')}",
        'description': "Dark psychological horror experience.\n\n#horror #scary #creepy #scarify",
        'tags': ['horror', 'scary', 'creepy', 'dark', 'scarify'],
        'voice_id': VOICE_ID,
        'created': datetime.now().isoformat()
    }
    
    metadata_file = youtube_file.with_suffix('.json')
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"📤 YouTube ready: {youtube_file}")
    return youtube_file

def test_voice(text=None):
    """Quick voice test"""
    
    if not text:
        text = "This is SCARIFY custom voice test. In the darkness, something awakens."
    
    setup_dirs()
    
    output = BASE_DIR / "temp" / f"test_{datetime.now().strftime('%H%M%S')}.mp3"
    
    if generate_voice(text, output):
        print(f"✅ Test complete: {output}")
        
        # Try to play
        try:
            if sys.platform == 'win32':
                os.startfile(str(output))
            else:
                subprocess.run(['xdg-open', str(output)])
        except:
            pass
        
        return True
    
    return False

def generate_complete_video(script=None):
    """Generate complete video: voice + video + YouTube prep"""
    
    if not script:
        script = """In the dead of night, when shadows come alive, 
there exists a place where reality bends. 
This is not a story for the faint of heart. 
What you're about to hear changed everything. 
Some say on quiet nights, you can still hear the echoes. 
But the truth is far worse than any rumor."""
    
    setup_dirs()
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Generate voice
    audio_file = BASE_DIR / "audio" / f"narration_{timestamp}.mp3"
    
    if not generate_voice(script, audio_file):
        return None
    
    # Create video
    video_file = BASE_DIR / "videos/generated" / f"SCARIFY_{timestamp}.mp4"
    
    if not create_video(audio_file, video_file):
        return None
    
    # Prepare for YouTube
    youtube_file = prepare_for_youtube(video_file)
    
    print(f"\n✅ COMPLETE!")
    print(f"   Video: {video_file}")
    print(f"   YouTube: {youtube_file}")
    
    return youtube_file

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: script.py [test|generate] [text/script]")
        sys.exit(1)
    
    action = sys.argv[1].lower()
    
    if action == 'test':
        text = sys.argv[2] if len(sys.argv) > 2 else None
        test_voice(text)
    
    elif action == 'generate':
        script = sys.argv[2] if len(sys.argv) > 2 else None
        generate_complete_video(script)
    
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)
