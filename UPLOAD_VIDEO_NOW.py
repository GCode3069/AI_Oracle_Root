#!/usr/bin/env python3
"""
UPLOAD VIDEO NOW - Creates and uploads a comedy video using existing systems
Uses the new comedy scripts with existing video generation infrastructure
"""

import os
import sys
import json
import random
import subprocess
from pathlib import Path
from datetime import datetime

# Add path for imports
sys.path.insert(0, str(Path.cwd()))

# Import our new comedy system
from COMEDY_SCRIPTS_REWRITTEN import ModernComedyGenerator, generate_video_script

# Import existing video creation system
try:
    from abraham_MAX_HEADROOM import generate_voice, generate_lincoln_face_pollo, BASE_DIR
except:
    BASE_DIR = Path.cwd()

def create_quick_video():
    """Create a video using existing infrastructure"""
    
    print("\n" + "="*70)
    print("🎬 CREATING LINCOLN COMEDY VIDEO - QUICK METHOD")
    print("="*70)
    
    # Current trending topics
    headlines = [
        "Tech Companies Announce More Layoffs",
        "Housing Market Reaches New Heights",
        "Congress Still Arguing About Everything",
        "AI Taking Over But Not Really",
        "Climate Change: We're Still Surprised",
        "Social Media Makes Everyone Angry"
    ]
    
    headline = random.choice(headlines)
    print(f"\n📰 Topic: {headline}")
    
    # Generate comedy script with new system
    print("\n📝 Generating ACTUALLY FUNNY script...")
    comedy_gen = ModernComedyGenerator()
    
    # Pick a random style for variety
    styles = ['observational', 'absurdist', 'dry_wit', 'relatable', 'deadpan']
    style = random.choice(styles)
    
    script, used_style = comedy_gen.generate(headline, style, word_limit=100)
    
    episode = random.randint(20000, 29999)
    title = f"Lincoln Comedy #{episode}: {headline[:30]} #Shorts"
    
    print(f"   Style: {used_style}")
    print(f"   Episode: #{episode}")
    print(f"   Words: {len(script.split())}")
    
    # Preview
    print("\n📜 Script:")
    print("-" * 50)
    print(script)
    print("-" * 50)
    
    # Create output directories
    output_dir = Path.cwd() / "videos" / "youtube_ready"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Use FFmpeg to create a simple video
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = output_dir / f"LINCOLN_COMEDY_{episode}_{timestamp}.mp4"
    
    print("\n🎬 Creating video with FFmpeg...")
    
    # Create a simple text-to-speech using espeak (available on Linux)
    audio_file = output_dir / f"temp_audio_{episode}.wav"
    
    # Try to generate audio with espeak
    try:
        cmd = ['espeak', '-w', str(audio_file), '-s', '150', '-p', '30', script]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Audio generated with espeak")
        else:
            print("⚠️ espeak failed, creating silent video")
            # Create silent audio
            cmd = [
                'ffmpeg', '-y',
                '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono',
                '-t', '30',
                str(audio_file)
            ]
            subprocess.run(cmd, capture_output=True)
    except:
        print("⚠️ Audio generation skipped")
        audio_file = None
    
    # Create video with colored background
    if audio_file and audio_file.exists():
        cmd = [
            'ffmpeg', '-y',
            '-f', 'lavfi', '-i', 'color=c=0x1a1a2e:s=1080x1920:d=30',
            '-i', str(audio_file),
            '-vf', f"drawtext=text='{title}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=100," + 
                   f"drawtext=text='Style\\: {used_style}':fontcolor=yellow:fontsize=36:x=(w-text_w)/2:y=200",
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-shortest',
            '-pix_fmt', 'yuv420p',
            str(output_file)
        ]
    else:
        # Video without audio
        cmd = [
            'ffmpeg', '-y',
            '-f', 'lavfi', '-i', 'color=c=0x1a1a2e:s=1080x1920:d=30',
            '-vf', f"drawtext=text='{title}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=100," + 
                   f"drawtext=text='Style\\: {used_style}':fontcolor=yellow:fontsize=36:x=(w-text_w)/2:y=200",
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            str(output_file)
        ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0 and output_file.exists():
        size_mb = output_file.stat().st_size / (1024 * 1024)
        print(f"✅ Video created: {size_mb:.1f} MB")
        print(f"📁 Location: {output_file}")
        
        # Clean up temp audio
        if audio_file and audio_file.exists():
            audio_file.unlink()
        
        # Save metadata
        metadata = {
            'headline': headline,
            'title': title,
            'episode': episode,
            'style': used_style,
            'script': script,
            'file': str(output_file),
            'timestamp': timestamp
        }
        
        metadata_file = output_dir / f"metadata_{episode}_{timestamp}.json"
        metadata_file.write_text(json.dumps(metadata, indent=2))
        
        # Try to upload with existing system
        try:
            print("\n📤 Attempting YouTube upload...")
            
            import pickle
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaFileUpload
            
            token_file = Path.cwd() / "youtube_token.pickle"
            
            if token_file.exists():
                with open(token_file, 'rb') as f:
                    creds = pickle.load(f)
                
                youtube = build('youtube', 'v3', credentials=creds)
                
                # YouTube metadata
                description = f"""{script}

🎭 ABRAHAM LINCOLN COMEDY - Episode #{episode}
Comedy Style: {used_style.replace('_', ' ').title()}
Topic: {headline}

New comedy system with actually funny scripts!
Bitcoin: bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt

#comedy #shorts #lincolnreacts #funny #{used_style.replace('_', '')}"""
                
                body = {
                    'snippet': {
                        'title': title,
                        'description': description,
                        'tags': ['comedy', 'shorts', 'lincoln', 'funny', used_style, 'abrahamlincoln'],
                        'categoryId': '23'
                    },
                    'status': {
                        'privacyStatus': 'public',
                        'selfDeclaredMadeForKids': False
                    }
                }
                
                media = MediaFileUpload(str(output_file), chunksize=1024*1024, resumable=True)
                request = youtube.videos().insert(part='snippet,status', body=body, media_body=media)
                
                print("   Uploading to YouTube...")
                response = None
                while response is None:
                    status, response = request.next_chunk()
                    if status:
                        print(f"   Progress: {int(status.progress() * 100)}%", end='\r')
                
                video_id = response['id']
                video_url = f'https://youtube.com/watch?v={video_id}'
                
                print(f"\n✅ UPLOADED SUCCESSFULLY!")
                print(f"📺 Watch at: {video_url}")
                
                return video_url
            else:
                print("❌ YouTube credentials not found")
                print("   Video saved locally: " + str(output_file))
                
        except Exception as e:
            print(f"⚠️ Upload failed: {e}")
            print(f"   Video saved locally: {output_file}")
        
        return str(output_file)
    else:
        print(f"❌ Video creation failed")
        if result.stderr:
            print(f"   Error: {result.stderr[:200]}")
        return None


if __name__ == "__main__":
    print("""
    🎬 QUICK VIDEO CREATOR
    ======================
    Creates comedy video with:
    - New actually funny scripts
    - Multiple comedy styles
    - Simple video generation
    - YouTube upload support
    """)
    
    result = create_quick_video()
    
    if result:
        print("\n" + "="*70)
        print("✅ SUCCESS!")
        print("="*70)
        if result.startswith('http'):
            print(f"🌐 Video URL: {result}")
        else:
            print(f"📁 Video file: {result}")
            print("\nTo upload manually:")
            print("1. Go to YouTube Studio")
            print("2. Click 'Create' → 'Upload videos'")
            print("3. Select the file above")
    else:
        print("\n❌ Video creation failed")