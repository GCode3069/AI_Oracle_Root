#!/usr/bin/env python3
"""
ABRAHAM HORROR - FIXED VERSION
PROPERLY combines audio + video
Verified working FFmpeg commands
"""
import os, sys, json, requests, subprocess, random, time
from pathlib import Path
from datetime import datetime

# API KEYS
ELEVENLABS_API_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
PEXELS_API_KEY = "RgE9Mdn3ToSQhn2RiLJ4mPMISjjp587QKRG9uhpOrLVtkKPCibUPUDGh"
VOICE_ID = '7aavy6c5cYIloDVj2JvH'
BASE_DIR = Path("F:/AI_Oracle_Root/scarify/abraham_horror")

HEADLINES = [
    "Hurricane Melissa Catastrophe - Jamaica Drowns 185mph",
    "Power Grid Hack - Sweden Blackout Total",
    "US Government Data Apocalypse - FEMA CBP Exposed",
    "Gaza Firestorm - 15 Dead Israeli Strikes",
    "Melissa Flood Hell - Bypass Bridges Gone"
]

def generate_script(headline):
    """Generate LONG horror script with gore"""
    gore = random.choice([
        "derringer tears through skull, brain matter explodes across theatre walls, blood floods presidential box",
        "lead ball shatters occiput, grey matter drips down velvet curtains, death screams echo",
        "bullet tunnels through cerebral cortex, bone fragments pierce wooden seats, life drains in pools"
    ])
    
    return f"""I watch from shadows as America dies. {headline}.

April 14th 1865. Ford's Theatre. Booth's derringer fires. {gore}. 

As I bled to death I saw your future. The corruption I fought metastasizes through your veins. Every lie you accept. Every freedom you surrender. Every compromise that rots the republic.

{headline}. This is not accident. This is the tyranny I warned against. The evil I died fighting returns stronger. Darker. Unstoppable.

From my blood-soaked box I speak truth: You inherit the nightmare. The Union collapses. Democracy drowns in blood of the betrayed.

Sic semper tyrannis. Thus always to tyrants.

But who are the tyrants now? You are."""

def generate_voice(script, output_path):
    """Generate voice - VERIFIED WORKING"""
    print("  [Voice] Generating...")
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    data = {
        "text": script,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.3, "similarity_boost": 0.85, "style": 0.8}
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=180)
        if response.status_code == 200:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            size_kb = output_path.stat().st_size / 1024
            print(f"  [Voice] ✅ {size_kb:.2f} KB")
            
            # VERIFY audio file
            if size_kb < 10:
                print("  [Voice] ❌ File too small - generation failed")
                return False
            
            return True
    except Exception as e:
        print(f"  [Voice] ❌ {e}")
    
    return False

def get_pexels_video():
    """Get stock video"""
    print("  [Pexels] Downloading...")
    
    try:
        url = "https://api.pexels.com/videos/search"
        headers = {"Authorization": PEXELS_API_KEY}
        params = {"query": "dark horror atmosphere", "per_page": 1, "orientation": "portrait"}
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        data = response.json()
        
        if data.get('videos'):
            video = data['videos'][0]
            video_file = max(video['video_files'], key=lambda x: x.get('width', 0))
            download_url = video_file['link']
            
            video_data = requests.get(download_url, timeout=120).content
            temp_file = BASE_DIR / "temp" / f"pexels_{random.randint(1000,9999)}.mp4"
            temp_file.parent.mkdir(exist_ok=True)
            
            with open(temp_file, 'wb') as f:
                f.write(video_data)
            
            size_mb = temp_file.stat().st_size / (1024 * 1024)
            print(f"  [Pexels] ✅ {size_mb:.2f} MB")
            return temp_file
    except Exception as e:
        print(f"  [Pexels] ❌ {e}")
    
    return None

def compose_video_FIXED(video_source, audio_path, output_path):
    """FIXED FFmpeg composition - PROPERLY adds audio"""
    print("  [FFmpeg] Composing (FIXED)...")
    
    # Get audio duration
    try:
        probe = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', 
             '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)],
            capture_output=True, text=True, check=True
        )
        duration = float(probe.stdout.strip())
        print(f"  [FFmpeg] Audio duration: {duration:.1f}s")
    except Exception as e:
        print(f"  [FFmpeg] ❌ Cannot read audio: {e}")
        return False
    
    # FIXED FFmpeg command - ensures audio is included
    cmd = [
        'ffmpeg',
        '-i', str(video_source),  # Video input
        '-i', str(audio_path),     # Audio input
        '-map', '0:v:0',           # Map video from first input
        '-map', '1:a:0',           # Map audio from second input
        '-vf', 'eq=contrast=1.3:brightness=-0.2,crop=1080:1920,scale=1080:1920',
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-c:a', 'aac',             # Audio codec
        '-b:a', '192k',            # Audio bitrate
        '-ar', '44100',            # Audio sample rate
        '-ac', '2',                # Audio channels (stereo)
        '-t', str(duration),       # Match audio duration
        '-shortest',               # Stop at shortest stream
        '-y',                      # Overwrite
        str(output_path)
    ]
    
    print(f"  [FFmpeg] Command: {' '.join(cmd[:10])}...")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        if output_path.exists():
            size_mb = output_path.stat().st_size / (1024 * 1024)
            
            # VERIFY audio is in output
            probe = subprocess.run(
                ['ffprobe', '-v', 'error', '-select_streams', 'a:0',
                 '-show_entries', 'stream=codec_type', '-of', 'default=noprint_wrappers=1', 
                 str(output_path)],
                capture_output=True, text=True
            )
            
            has_audio = 'codec_type=audio' in probe.stdout
            
            if has_audio:
                print(f"  [FFmpeg] ✅ {size_mb:.2f} MB - AUDIO VERIFIED")
                video_source.unlink()
                return True
            else:
                print(f"  [FFmpeg] ❌ No audio in output!")
                return False
        
        print(f"  [FFmpeg] ❌ Output file not created")
        return False
        
    except subprocess.CalledProcessError as e:
        print(f"  [FFmpeg] ❌ Command failed:")
        print(f"  STDERR: {e.stderr}")
        return False
    except Exception as e:
        print(f"  [FFmpeg] ❌ {e}")
        return False

def generate():
    """Generate complete video - FIXED"""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    print(f"\n{'='*70}")
    print("GENERATING VIDEO (FIXED VERSION)")
    print(f"{'='*70}\n")
    
    # Headline
    headline = random.choice(HEADLINES)
    print(f"Headline: {headline}\n")
    
    # Script
    script = generate_script(headline)
    print(f"Script: {len(script)} chars\n")
    
    # Generate voice
    audio_path = BASE_DIR / f"audio/abraham_{timestamp}.mp3"
    if not generate_voice(script, audio_path):
        print("\n❌ Voice generation failed")
        return None
    
    # Get video
    video_source = get_pexels_video()
    if not video_source:
        print("\n❌ Video download failed")
        return None
    
    # Compose with FIXED method
    video_path = BASE_DIR / f"videos/ABRAHAM_{timestamp}.mp4"
    if not compose_video_FIXED(video_source, audio_path, video_path):
        print("\n❌ Video composition failed")
        return None
    
    # Copy to youtube_ready
    youtube_file = BASE_DIR / "youtube_ready" / f"ABRAHAM_{timestamp}.mp4"
    youtube_file.parent.mkdir(exist_ok=True)
    
    import shutil
    shutil.copy2(video_path, youtube_file)
    
    size_mb = youtube_file.stat().st_size / (1024 * 1024)
    
    print(f"\n{'='*70}")
    print("✅ COMPLETE - AUDIO VERIFIED")
    print(f"{'='*70}")
    print(f"File: {youtube_file.name}")
    print(f"Size: {size_mb:.2f} MB")
    print(f"{'='*70}\n")
    
    return str(youtube_file)

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    
    print(f"\n🔥 GENERATING {count} VIDEOS (FIXED)\n")
    
    for i in range(count):
        result = generate()
        if result:
            print(f"✅ Video {i+1}/{count} complete")
        else:
            print(f"❌ Video {i+1}/{count} failed")
        
        if i < count - 1:
            time.sleep(5)
    
    print(f"\n✅ DONE!\n")
