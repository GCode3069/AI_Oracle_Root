#!/usr/bin/env python3
"""
BATCH FIX EXISTING VIDEOS
- Extract clean scripts from existing videos
- Re-generate audio with comedic voice (no video descriptions)
- Re-apply TV static effect
- Fix all videos in youtube_ready folder
"""
import os
import subprocess
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("F:/AI_Oracle_Root/scarify/abraham_studio")
YOUTUBE_DIR = BASE_DIR / "youtube_ready"
BACKUP_DIR = BASE_DIR / "backups"

# API Keys
ELEVENLABS_API_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"

def extract_audio_from_video(video_path):
    """Extract audio from video to get original script via transcription"""
    audio_path = video_path.with_suffix('.wav')
    
    cmd = [
        'ffmpeg', '-i', str(video_path),
        '-vn', '-acodec', 'pcm_s16le',
        '-ar', '44100', '-ac', '2',
        '-y', str(audio_path)
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, check=True, timeout=60)
        return audio_path
    except:
        return None

def clean_script(script_text):
    """Remove video description phrases from script"""
    if not script_text:
        return script_text
    
    # Remove common video description phrases
    video_description_phrases = [
        "tv static", "pop effect", "glitch", "zoom", "fade",
        "9:16", "1080x1920", "aspect ratio", "video quality",
        "visual effect", "static overlay", "noise", "distortion",
        "the video shows", "this video", "the image shows",
        "static tv", "television static", "screen effect"
    ]
    
    lines = script_text.split('\n')
    clean_lines = []
    
    for line in lines:
        line_lower = line.lower()
        # Skip lines that are clearly video descriptions
        if any(phrase in line_lower for phrase in video_description_phrases):
            continue
        # Remove phrases from within lines
        for phrase in video_description_phrases:
            line = line.replace(phrase, '')
            line = line.replace(phrase.capitalize(), '')
        clean_lines.append(line.strip())
    
    return ' '.join([l for l in clean_lines if l])

def regenerate_audio(script_text, output_path):
    """Regenerate audio with comedic voice settings"""
    import requests
    
    if not script_text or len(script_text) < 10:
        return False
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/7aavy6c5cYIloDVj2JvH"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    # COMEDIC SETTINGS
    data = {
        "text": script_text,
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
            return True
    except Exception as e:
        print(f"  Audio generation error: {e}")
    
    return False

def add_tv_static_effect(video_path):
    """Add TV static overlay to video"""
    static_temp = BASE_DIR / "temp_static_overlay.mp4"
    output_path = video_path.with_name(f"{video_path.stem}_fixed.mp4")
    
    try:
        # Create static noise overlay
        static_cmd = [
            'ffmpeg', '-f', 'lavfi', '-i', 'testsrc=duration=15:size=1080x1920:rate=30',
            '-f', 'lavfi', '-i', 'noise=alls=30:allf=t+u',
            '-filter_complex',
            '[0:v][1:v]blend=all_mode=screen:all_opacity=0.3[static]',
            '-map', '[static]', '-t', '15', '-pix_fmt', 'yuv420p', '-y', str(static_temp)
        ]
        
        subprocess.run(static_cmd, capture_output=True, check=True, timeout=30)
        
        # Overlay static on video
        overlay_cmd = [
            'ffmpeg', '-i', str(video_path),
            '-i', str(static_temp),
            '-filter_complex', '[0:v][1:v]blend=all_mode=screen:all_opacity=0.4[v]',
            '-map', '[v]', '-map', '0:a', '-c:v', 'libx264', '-c:a', 'copy',
            '-shortest', '-y', str(output_path)
        ]
        
        subprocess.run(overlay_cmd, capture_output=True, check=True, timeout=60)
        
        # Replace original
        video_path.unlink()
        output_path.rename(video_path)
        
        # Cleanup
        if static_temp.exists():
            static_temp.unlink()
        
        return True
    except Exception as e:
        print(f"  Static effect error: {e}")
        return False

def fix_video(video_path):
    """Fix a single video"""
    print(f"\n{'='*70}")
    print(f"FIXING: {video_path.name}")
    print(f"{'='*70}")
    
    # Step 1: Check for metadata JSON (might have clean script)
    json_path = video_path.with_suffix('.json')
    script = None
    
    if json_path.exists():
        try:
            with open(json_path, 'r') as f:
                metadata = json.load(f)
                script = metadata.get('description', '').split('\n')[1] if 'description' in metadata else None
                if script:
                    script = clean_script(script)
                    print(f"  Found script in metadata: {script[:80]}...")
        except:
            pass
    
    # Step 2: If no clean script, try to extract from audio (would need transcription)
    if not script:
        print("  WARNING: No script found. You'll need to manually provide scripts.")
        print("  Skipping audio regeneration for this video.")
    
    # Step 3: Regenerate audio if script available
    if script and len(script) > 10:
        audio_path = BASE_DIR / "audio" / f"fixed_{video_path.stem}.mp3"
        print(f"  Regenerating audio with clean script...")
        
        if regenerate_audio(script, audio_path):
            print(f"  ✅ Audio regenerated")
            
            # Replace audio in video
            print(f"  Replacing audio in video...")
            temp_video = video_path.with_name(f"{video_path.stem}_temp.mp4")
            
            cmd = [
                'ffmpeg', '-i', str(video_path),
                '-i', str(audio_path),
                '-c:v', 'copy', '-c:a', 'aac',
                '-map', '0:v:0', '-map', '1:a:0',
                '-shortest', '-y', str(temp_video)
            ]
            
            try:
                subprocess.run(cmd, capture_output=True, check=True, timeout=60)
                video_path.unlink()
                temp_video.rename(video_path)
                print(f"  ✅ Audio replaced")
            except Exception as e:
                print(f"  ⚠️ Audio replacement failed: {e}")
    
    # Step 4: Add TV static effect
    print(f"  Adding TV static effect...")
    if add_tv_static_effect(video_path):
        print(f"  ✅ TV static applied")
    else:
        print(f"  ⚠️ TV static skipped")
    
    print(f"  ✅ Video fixed: {video_path.name}")

def main():
    """Fix all videos in youtube_ready folder"""
    print("="*70)
    print("BATCH FIX EXISTING VIDEOS")
    print("="*70)
    print("\nThis will:")
    print("  1. Extract/clean scripts (remove video descriptions)")
    print("  2. Regenerate audio with comedic voice")
    print("  3. Add TV static effect")
    print("\nBacking up originals first...")
    
    # Create backup
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_subdir = BACKUP_DIR / f"backup_{backup_timestamp}"
    backup_subdir.mkdir()
    
    videos = list(YOUTUBE_DIR.glob('*.mp4'))
    
    if not videos:
        print(f"\n⚠️ No videos found in {YOUTUBE_DIR}")
        return
    
    print(f"\nFound {len(videos)} videos to fix")
    
    response = input("\nProceed? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled")
        return
    
    # Backup all videos
    print("\nBacking up...")
    for video in videos:
        backup_path = backup_subdir / video.name
        import shutil
        shutil.copy2(video, backup_path)
    
    print(f"✅ Backed up to: {backup_subdir}\n")
    
    # Fix each video
    for i, video in enumerate(videos, 1):
        print(f"\n[{i}/{len(videos)}]")
        try:
            fix_video(video)
        except Exception as e:
            print(f"  ❌ Error fixing {video.name}: {e}")
    
    print("\n" + "="*70)
    print("BATCH FIX COMPLETE")
    print("="*70)
    print(f"Fixed: {len(videos)} videos")
    print(f"Backups: {backup_subdir}")
    print("="*70)

if __name__ == "__main__":
    main()




