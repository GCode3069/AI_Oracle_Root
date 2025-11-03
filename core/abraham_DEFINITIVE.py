#!/usr/bin/env python3
"""
ABRAHAM HORROR - DEFINITIVE AUDIO FIX
This version GUARANTEES audio in output
Multiple verification layers
"""
import os, sys, json, requests, subprocess, random, time
from pathlib import Path
from datetime import datetime

# API KEYS
ELEVENLABS_API_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
PEXELS_API_KEY = "RgE9Mdn3ToSQhn2RiLJ4mPMISjjp587QKRG9uhpOrLVtkKPCibUPUDGh"
VOICE_ID = '21m00Tcm4TlvDq8ikWAM'  # Rachel - more natural
BASE_DIR = Path("F:/AI_Oracle_Root/scarify/abraham_horror")

def log(msg, level="INFO"):
    """Simple logging"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    symbols = {"INFO": "ℹ️", "OK": "✅", "ERROR": "❌", "WARN": "⚠️"}
    print(f"[{timestamp}] {symbols.get(level, 'ℹ️')} {msg}")

HEADLINES = [
    "Hurricane Melissa Catastrophe Jamaica 185mph Apocalypse",
    "Power Grid Cyber Attack Sweden Total Blackout",
    "US Government Data Breach FEMA CBP Exposed",
    "Gaza Airstrikes 15 Dead Israeli Military Action",
    "Flood Disaster Jamaica Bypass Bridges Destroyed"
]

def generate_script(headline):
    """Long horror script with Lincoln"""
    gore = random.choice([
        "derringer bullet tears through skull exploding brain matter across blood-soaked theatre walls",
        "lead ball shatters occiput spewing grey matter and bone fragments through presidential box",
        "assassin's shot tunnels through cerebral cortex spraying crimson life onto velvet seats"
    ])
    
    return f"""I am Abraham Lincoln. I watch from beyond death as your nation crumbles.

{headline}.

April 14th, 1865. Ford's Theatre. John Wilkes Booth's derringer fires. {gore}. As I bled out in that cursed box, I saw your future in my dying vision.

The corruption I fought against metastasizes through your veins like poison. Every lie you accept. Every freedom you surrender. Every tyranny you excuse.

{headline}. You think this is random? This is the evil I warned about. The darkness I died fighting. It returns stronger. Crueler. Unstoppable.

From my blood-soaked seat I speak truth: The Union I saved collapses from within. The democracy I preserved drowns in lies. The freedom I died for becomes chains.

You inherit the nightmare I saw in my last breath. The republic fractures. The dream dies. America burns.

Sic semper tyrannis. Thus always to tyrants.

But ask yourself: Who are the tyrants now?

Look in the mirror. You are."""

def generate_voice_VERIFIED(script, output_path):
    """Generate voice with MULTIPLE verifications"""
    log("Generating voice...", "INFO")
    
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
            "stability": 0.5,
            "similarity_boost": 0.9,
            "style": 0.8,
            "use_speaker_boost": True
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=180)
        
        if response.status_code != 200:
            log(f"ElevenLabs API error: {response.status_code}", "ERROR")
            log(f"Response: {response.text[:200]}", "ERROR")
            return False
        
        # Save audio
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        # VERIFICATION 1: File size
        size_kb = output_path.stat().st_size / 1024
        if size_kb < 10:
            log(f"Audio file too small: {size_kb:.2f} KB", "ERROR")
            return False
        
        # VERIFICATION 2: File format
        probe = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 
             'format=format_name,duration', '-of', 'json', str(output_path)],
            capture_output=True, text=True
        )
        
        if probe.returncode != 0:
            log("Audio file is corrupted", "ERROR")
            return False
        
        probe_data = json.loads(probe.stdout)
        duration = float(probe_data['format']['duration'])
        
        if duration < 1:
            log(f"Audio too short: {duration:.1f}s", "ERROR")
            return False
        
        log(f"Voice OK: {size_kb:.2f} KB, {duration:.1f}s", "OK")
        return True
        
    except Exception as e:
        log(f"Voice generation failed: {e}", "ERROR")
        return False

def get_pexels_video():
    """Download Pexels video"""
    log("Downloading Pexels video...", "INFO")
    
    try:
        url = "https://api.pexels.com/videos/search"
        headers = {"Authorization": PEXELS_API_KEY}
        params = {"query": "dark horror atmosphere", "per_page": 1, "orientation": "portrait"}
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        data = response.json()
        
        if not data.get('videos'):
            log("No videos found", "ERROR")
            return None
        
        video = data['videos'][0]
        video_file = max(video['video_files'], key=lambda x: x.get('width', 0))
        download_url = video_file['link']
        
        log(f"Downloading from Pexels...", "INFO")
        video_data = requests.get(download_url, timeout=120).content
        
        temp_file = BASE_DIR / "temp" / f"pexels_{random.randint(1000,9999)}.mp4"
        temp_file.parent.mkdir(exist_ok=True)
        
        with open(temp_file, 'wb') as f:
            f.write(video_data)
        
        size_mb = temp_file.stat().st_size / (1024 * 1024)
        log(f"Video OK: {size_mb:.2f} MB", "OK")
        
        return temp_file
        
    except Exception as e:
        log(f"Pexels download failed: {e}", "ERROR")
        return None

def compose_video_GUARANTEED_AUDIO(video_source, audio_path, output_path):
    """Compose video with GUARANTEED audio - triple verified"""
    log("Composing video with audio...", "INFO")
    
    # PRE-CHECK: Verify inputs exist
    if not video_source.exists():
        log(f"Video source missing: {video_source}", "ERROR")
        return False
    
    if not audio_path.exists():
        log(f"Audio source missing: {audio_path}", "ERROR")
        return False
    
    # Get audio duration
    try:
        probe = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)],
            capture_output=True, text=True, check=True
        )
        duration = float(probe.stdout.strip())
        log(f"Audio duration: {duration:.1f}s", "INFO")
    except Exception as e:
        log(f"Cannot read audio duration: {e}", "ERROR")
        return False
    
    # CRITICAL: FFmpeg command with EXPLICIT audio mapping
    cmd = [
        'ffmpeg',
        '-i', str(video_source),    # Input 0: video
        '-i', str(audio_path),       # Input 1: audio
        '-map', '0:v:0',             # EXPLICIT: map video from input 0
        '-map', '1:a:0',             # EXPLICIT: map audio from input 1
        '-vf', 'eq=contrast=1.3:brightness=-0.2,crop=1080:1920,scale=1080:1920',
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-c:a', 'aac',               # Audio codec
        '-b:a', '192k',              # Audio bitrate
        '-ar', '44100',              # Sample rate
        '-ac', '2',                  # Stereo
        '-t', str(duration),         # Duration from audio
        '-shortest',                 # Stop at shortest stream
        '-y',                        # Overwrite
        str(output_path)
    ]
    
    log(f"Running FFmpeg...", "INFO")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        if not output_path.exists():
            log("FFmpeg did not create output file", "ERROR")
            return False
        
        # VERIFICATION 1: File size
        size_mb = output_path.stat().st_size / (1024 * 1024)
        if size_mb < 1:
            log(f"Output too small: {size_mb:.2f} MB", "ERROR")
            return False
        
        # VERIFICATION 2: Audio stream exists
        probe = subprocess.run(
            ['ffprobe', '-v', 'error', '-select_streams', 'a:0',
             '-show_entries', 'stream=codec_type,codec_name',
             '-of', 'json', str(output_path)],
            capture_output=True, text=True
        )
        
        probe_data = json.loads(probe.stdout)
        
        if not probe_data.get('streams'):
            log("NO AUDIO STREAM IN OUTPUT!", "ERROR")
            log("This video will be SILENT on YouTube!", "ERROR")
            return False
        
        audio_codec = probe_data['streams'][0].get('codec_name')
        
        # VERIFICATION 3: Audio codec is correct
        if audio_codec != 'aac':
            log(f"Wrong audio codec: {audio_codec}", "WARN")
        
        log(f"Output OK: {size_mb:.2f} MB with {audio_codec} audio", "OK")
        
        # Cleanup
        video_source.unlink()
        
        return True
        
    except subprocess.CalledProcessError as e:
        log(f"FFmpeg failed: {e.stderr[:200]}", "ERROR")
        return False
    except Exception as e:
        log(f"Composition error: {e}", "ERROR")
        return False

def generate():
    """Generate complete video - GUARANTEED audio"""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    print("\n" + "="*70)
    print("ABRAHAM HORROR - DEFINITIVE AUDIO FIX")
    print("="*70 + "\n")
    
    # Headline
    headline = random.choice(HEADLINES)
    log(f"Headline: {headline}", "INFO")
    
    # Script
    script = generate_script(headline)
    log(f"Script: {len(script)} chars", "INFO")
    
    # Generate voice with verification
    audio_path = BASE_DIR / f"audio/abraham_{timestamp}.mp3"
    if not generate_voice_VERIFIED(script, audio_path):
        log("ABORT: Voice generation failed", "ERROR")
        return None
    
    # Download video
    video_source = get_pexels_video()
    if not video_source:
        log("ABORT: Video download failed", "ERROR")
        return None
    
    # Compose with GUARANTEED audio
    video_path = BASE_DIR / f"videos/ABRAHAM_{timestamp}.mp4"
    if not compose_video_GUARANTEED_AUDIO(video_source, audio_path, video_path):
        log("ABORT: Composition failed", "ERROR")
        return None
    
    # Copy to youtube_ready
    youtube_file = BASE_DIR / "youtube_ready" / f"ABRAHAM_{timestamp}.mp4"
    youtube_file.parent.mkdir(exist_ok=True)
    
    import shutil
    shutil.copy2(video_path, youtube_file)
    
    size_mb = youtube_file.stat().st_size / (1024 * 1024)
    
    # Save metadata
    metadata = {
        'timestamp': datetime.now().isoformat(),
        'headline': headline,
        'file_size_mb': round(size_mb, 2),
        'audio_verified': True,
        'file_path': str(youtube_file)
    }
    
    with open(youtube_file.with_suffix('.json'), 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("\n" + "="*70)
    print("SUCCESS - AUDIO VERIFIED")
    print("="*70)
    print(f"File: {youtube_file.name}")
    print(f"Size: {size_mb:.2f} MB")
    print("="*70 + "\n")
    
    return str(youtube_file)

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    
    print(f"\nGenerating {count} video(s) with GUARANTEED audio\n")
    
    success = 0
    failed = 0
    
    for i in range(count):
        log(f"Starting video {i+1}/{count}", "INFO")
        result = generate()
        
        if result:
            success += 1
            log(f"Video {i+1}/{count} SUCCESS", "OK")
        else:
            failed += 1
            log(f"Video {i+1}/{count} FAILED", "ERROR")
        
        if i < count - 1:
            log("Waiting 5 seconds...", "INFO")
            time.sleep(5)
    
    print(f"\n" + "="*70)
    print(f"COMPLETE: {success} success, {failed} failed")
    print("="*70 + "\n")
