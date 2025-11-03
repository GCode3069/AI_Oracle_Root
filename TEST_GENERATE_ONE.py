#!/usr/bin/env python3
"""
Test generate ONE video to check quality
"""
import os
import sys
import subprocess
from pathlib import Path

BASE_DIR = Path("F:/AI_Oracle_Root/scarify/abraham_studio")
sys.path.insert(0, str(Path(__file__).parent))

# Import the studio functions
import random
import requests
from datetime import datetime

# API Keys
ELEVENLABS_API_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
STABILITY_API_KEY = "sk-sP9EO0Ybb3L7SfGbpEtfrmOIhXVf8DdK9eSaTSBuTcNhjpQi"

def generate_clean_script(headline):
    """Generate clean comedic script"""
    openings = [
        "Now hold up, hold up. Let me tell y'all something real quick.",
        "Aight, look here. I'm watching this mess unfold and I got thoughts.",
        "You know what? I'm dead, but this here got me spinning in my grave."
    ]
    
    observations = [
        "This is wild, man. Straight wild.",
        "Y'all really out here doing the most, huh?",
        "I'm telling you, this country done lost its mind."
    ]
    
    rants = [
        "Sic semper tyrannis. That means thus always to tyrants, in case y'all forgot.",
        "I'm Abe Lincoln, man. The real Abe. And I'm telling you, this ain't it."
    ]
    
    opening = random.choice(openings)
    observation = random.choice(observations)
    rant = random.choice(rants)
    
    script = f"{opening} {headline}. {observation} {rant}"
    
    # Clean script - remove video description phrases
    video_description_phrases = [
        "tv static", "pop effect", "glitch", "zoom", "fade",
        "9:16", "1080x1920", "aspect ratio", "video quality",
        "visual effect", "static overlay", "noise", "distortion"
    ]
    
    words = script.split()
    clean_words = [w for w in words if not any(phrase in w.lower() for phrase in video_description_phrases)]
    script = " ".join(clean_words)
    
    return script

def generate_audio(script, output_path):
    """Generate audio with comedic voice"""
    print(f"\n[Audio] Generating voice...")
    print(f"Script: {script}")
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/7aavy6c5cYIloDVj2JvH"
    
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
            "similarity_boost": 0.8,
            "style": 0.95,
            "use_speaker_boost": True
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=120)
        
        if response.status_code == 200:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"[Audio] SUCCESS: {output_path.name}")
            return True
        else:
            print(f"[Audio] FAILED: {response.status_code}")
            return False
    except Exception as e:
        print(f"[Audio] ERROR: {e}")
        return False

def generate_video(headline, audio_path, output_path):
    """Generate video with Abe's face on TV static"""
    print(f"\n[Video] Generating visual...")
    
    # FALLBACK: Use existing Abe image or create simple background
    print(f"[Video] Using fallback visual (no API needed)...")
    
    # Check for existing Abe image
    abe_image = Path("assets") / "lincoln_portrait.jpg"
    if not abe_image.exists():
        # Create simple test image with FFmpeg
        image_path = output_path.with_suffix('.jpg')
        cmd = [
            'ffmpeg', '-f', 'lavfi', '-i', 'color=c=black:size=1080x1920',
            '-vf', "drawtext=text='ABRAHAM LINCOLN':fontcolor=white:fontsize=80:x=(w-text_w)/2:y=(h-text_h)/2",
            '-frames:v', '1', '-y', str(image_path)
        ]
        subprocess.run(cmd, capture_output=True, check=True, timeout=30)
        print(f"[Video] Created test image")
    else:
        image_path = abe_image
    
    try:
        
        # Step 2: Create base video with zoom
        print(f"[Video] Creating video with zoom...")
        cmd = [
            'ffmpeg', '-loop', '1', '-i', str(image_path),
            '-i', str(audio_path),
            '-t', '15',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-vf', 'scale=1080:1920,zoompan=z=\'min(zoom+0.0015,1.5)\':d=360:s=1080x1920',
            '-c:a', 'aac',
            '-shortest', '-y', str(output_path)
        ]
        
        subprocess.run(cmd, capture_output=True, check=True, timeout=60)
        print(f"[Video] Base video created")
        
        # Step 3: Add TV static (try, don't fail if it doesn't work)
        try:
            print(f"[Video] Adding TV static effect...")
            static_temp = BASE_DIR / "temp_static.mp4"
            final_output = output_path.with_name(f"{output_path.stem}_final.mp4")
            
            # Create static
            static_cmd = [
                'ffmpeg', '-f', 'lavfi', '-i', 'testsrc=duration=15:size=1080x1920:rate=30',
                '-f', 'lavfi', '-i', 'noise=alls=30:allf=t+u',
                '-filter_complex',
                '[0:v][1:v]blend=all_mode=screen:all_opacity=0.3[static]',
                '-map', '[static]', '-t', '15', '-pix_fmt', 'yuv420p', '-y', str(static_temp)
            ]
            
            subprocess.run(static_cmd, capture_output=True, check=True, timeout=30)
            
            # Overlay
            overlay_cmd = [
                'ffmpeg', '-i', str(output_path),
                '-i', str(static_temp),
                '-filter_complex', '[0:v][1:v]blend=all_mode=screen:all_opacity=0.4[v]',
                '-map', '[v]', '-map', '0:a', '-c:v', 'libx264', '-c:a', 'copy',
                '-shortest', '-y', str(final_output)
            ]
            
            subprocess.run(overlay_cmd, capture_output=True, check=True, timeout=30)
            
            # Replace
            output_path.unlink()
            final_output.rename(output_path)
            
            if static_temp.exists():
                static_temp.unlink()
            
            print(f"[Video] TV static added")
        except Exception as e:
            print(f"[Video] Static effect skipped: {e}")
        
        # Cleanup
        image_path.unlink()
        
        print(f"[Video] SUCCESS: {output_path.name}")
        return True
        
    except Exception as e:
        print(f"[Video] ERROR: {e}")
        return False

def main():
    """Test generate 1 video"""
    print("="*70)
    print("TEST GENERATION - ONE VIDEO")
    print("="*70)
    
    # Setup
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "audio").mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "videos").mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "youtube_ready").mkdir(parents=True, exist_ok=True)
    
    # Generate
    headline = "Corrupt Government Officials - 69% Fear"
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    print(f"\nHeadline: {headline}")
    print(f"Timestamp: {timestamp}")
    
    # Script
    script = generate_clean_script(headline)
    print(f"Script ({len(script)} chars): {script}")
    
    # Audio
    audio_path = BASE_DIR / "audio" / f"test_{timestamp}.mp3"
    if not generate_audio(script, audio_path):
        print("\nFAILED: Audio generation")
        return
    
    # Video
    video_path = BASE_DIR / "videos" / f"TEST_{timestamp}.mp4"
    if not generate_video(headline, audio_path, video_path):
        print("\nFAILED: Video generation")
        return
    
    # Copy to youtube_ready
    youtube_path = BASE_DIR / "youtube_ready" / f"TEST_{timestamp}.mp4"
    import shutil
    shutil.copy2(video_path, youtube_path)
    
    print("\n" + "="*70)
    print("SUCCESS - VIDEO READY")
    print("="*70)
    print(f"Output: {youtube_path}")
    print(f"Size: {youtube_path.stat().st_size / 1_000_000:.2f}MB")
    print("="*70)
    
    # Open folder
    if sys.platform == 'win32':
        os.startfile(BASE_DIR / "youtube_ready")

if __name__ == "__main__":
    main()

