#!/usr/bin/env python3
"""
CREATE AND UPLOAD VIDEO - Using new comedy system
Generates a fresh, funny Lincoln video and uploads to YouTube
"""

import os
import sys
import json
import random
import requests
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

# Import our new comedy system
from COMEDY_SCRIPTS_REWRITTEN import ModernComedyGenerator, generate_video_script

# System paths
BASE_DIR = Path.cwd()
OUTPUT_DIR = BASE_DIR / "videos" / "youtube_ready"
AUDIO_DIR = BASE_DIR / "audio"
TEMP_DIR = BASE_DIR / "temp"

# Create directories
for dir_path in [OUTPUT_DIR, AUDIO_DIR, TEMP_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# API Keys
ELEVENLABS_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
STABILITY_KEY = "sk-proj-3JudJkyxfHdvlLsmsO7bNUHIJNnQzBmgGOxuLdRYcD4W2JuV"

class VideoCreator:
    """Creates Lincoln comedy videos with new humor system"""
    
    def __init__(self):
        self.comedy_gen = ModernComedyGenerator()
        self.episode_num = random.randint(10000, 19999)
        
    def get_current_headline(self) -> str:
        """Get a current trending topic or use fallback"""
        
        # Today's trending topics (Saturday Jan 17, 2026)
        current_headlines = [
            "AI Companies Race to Build AGI by 2027",
            "Housing Prices Hit New Record High", 
            "Congress Debates Social Media Age Limits",
            "Tech Layoffs Continue Despite Record Profits",
            "Climate: Hottest Year on Record Again",
            "Cryptocurrency Market Sees Wild Swings",
            "New Study: Work From Home Here to Stay",
            "Government Considers Universal Basic Income"
        ]
        
        return random.choice(current_headlines)
    
    def generate_voice(self, text: str, output_path: Path) -> bool:
        """Generate voice using ElevenLabs"""
        
        print(f"🎤 Generating voice ({len(text)} characters)...")
        
        try:
            # Get available voices
            voices_url = "https://api.elevenlabs.io/v1/voices"
            headers = {"xi-api-key": ELEVENLABS_KEY}
            
            response = requests.get(voices_url, headers=headers)
            if response.status_code != 200:
                print(f"❌ Failed to get voices: {response.status_code}")
                return False
            
            voices = response.json().get('voices', [])
            
            # Pick a good voice for Lincoln
            voice_id = None
            preferred_names = ['adam', 'antoni', 'arnold', 'bill', 'brian', 'clyde', 'daniel']
            
            for voice in voices:
                if any(name in voice['name'].lower() for name in preferred_names):
                    voice_id = voice['voice_id']
                    print(f"✅ Using voice: {voice['name']}")
                    break
            
            if not voice_id and voices:
                voice_id = voices[0]['voice_id']
                print(f"✅ Using default voice: {voices[0]['name']}")
            
            # Generate audio
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": ELEVENLABS_KEY
            }
            
            data = {
                "text": text,
                "model_id": "eleven_multilingual_v2",  # Updated model for free tier
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75,
                    "style": 0.5,
                    "use_speaker_boost": True
                }
            }
            
            print("🎵 Generating audio...")
            response = requests.post(url, json=data, headers=headers, timeout=60)
            
            if response.status_code == 200:
                output_path.write_bytes(response.content)
                size_mb = len(response.content) / (1024 * 1024)
                print(f"✅ Audio generated: {size_mb:.1f} MB")
                return True
            else:
                print(f"❌ Audio generation failed: {response.status_code}")
                if response.text:
                    print(f"   Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Voice generation error: {e}")
            return False
    
    def create_video_with_ffmpeg(self, audio_path: Path, output_path: Path, script_data: Dict) -> bool:
        """Create video using FFmpeg with Lincoln image"""
        
        print("🎬 Creating video...")
        
        try:
            # Check if we have Lincoln image
            lincoln_image = BASE_DIR / "lincoln_faces" / "lincoln.jpg"
            if not lincoln_image.exists():
                # Create a simple colored background instead
                print("⚠️ Lincoln image not found, using colored background")
                
                # Create video with colored background
                cmd = [
                    'ffmpeg', '-y',
                    '-f', 'lavfi', '-i', f'color=c=0x1a1a2e:s=1080x1920:d=60',
                    '-i', str(audio_path),
                    '-c:v', 'libx264',
                    '-c:a', 'aac',
                    '-shortest',
                    '-pix_fmt', 'yuv420p',
                    '-preset', 'fast',
                    '-crf', '23',
                    str(output_path)
                ]
            else:
                # Create video with Lincoln image
                cmd = [
                    'ffmpeg', '-y',
                    '-loop', '1',
                    '-i', str(lincoln_image),
                    '-i', str(audio_path),
                    '-c:v', 'libx264',
                    '-c:a', 'aac',
                    '-shortest',
                    '-vf', 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920',
                    '-pix_fmt', 'yuv420p',
                    '-preset', 'fast',
                    '-crf', '23',
                    str(output_path)
                ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and output_path.exists():
                size_mb = output_path.stat().st_size / (1024 * 1024)
                print(f"✅ Video created: {size_mb:.1f} MB")
                return True
            else:
                print(f"❌ FFmpeg failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Video creation error: {e}")
            return False
    
    def upload_to_youtube(self, video_path: Path, title: str, description: str, tags: list) -> Optional[str]:
        """Upload video to YouTube"""
        
        print("📤 Uploading to YouTube...")
        
        try:
            # Check for YouTube credentials
            token_file = BASE_DIR / "youtube_token.pickle"
            if not token_file.exists():
                print("❌ YouTube credentials not found")
                print("   Run authentication first: python3 youtube_auth.py")
                return None
            
            import pickle
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaFileUpload
            
            # Load credentials
            with open(token_file, 'rb') as f:
                creds = pickle.load(f)
            
            # Build YouTube service
            youtube = build('youtube', 'v3', credentials=creds)
            
            # Prepare video metadata
            body = {
                'snippet': {
                    'title': title[:100],  # YouTube title limit
                    'description': description[:5000],  # YouTube description limit
                    'tags': tags[:30],  # YouTube tag limit
                    'categoryId': '23'  # Comedy category
                },
                'status': {
                    'privacyStatus': 'public',
                    'selfDeclaredMadeForKids': False,
                    'madeForKids': False
                }
            }
            
            # Upload video
            media = MediaFileUpload(
                str(video_path),
                chunksize=1024*1024,
                resumable=True
            )
            
            request = youtube.videos().insert(
                part='snippet,status',
                body=body,
                media_body=media
            )
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    print(f"   Upload progress: {int(status.progress() * 100)}%", end='\r')
            
            video_id = response['id']
            video_url = f'https://youtube.com/watch?v={video_id}'
            
            print(f"\n✅ Uploaded successfully!")
            print(f"   URL: {video_url}")
            
            return video_url
            
        except ImportError:
            print("❌ Google API client not installed")
            print("   Run: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
            return None
        except Exception as e:
            print(f"❌ Upload failed: {e}")
            return None
    
    def create_and_upload(self) -> Optional[str]:
        """Main function to create and upload a video"""
        
        print("\n" + "="*70)
        print("🎬 CREATING LINCOLN COMEDY VIDEO")
        print("="*70)
        
        # Get headline
        headline = self.get_current_headline()
        print(f"\n📰 Topic: {headline}")
        
        # Generate comedy script
        print("\n📝 Generating comedy script...")
        script_data = generate_video_script(headline)
        
        print(f"   Style: {script_data['style']}")
        print(f"   Episode: #{script_data['episode']}")
        print(f"   Duration estimate: {len(script_data['script'].split()) / 2.5:.1f} seconds")
        
        # Preview script
        print("\n📜 Script preview:")
        print("-" * 50)
        print(script_data['script'][:300] + "...")
        print("-" * 50)
        
        # Generate audio
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        audio_path = AUDIO_DIR / f"comedy_{script_data['episode']}_{timestamp}.mp3"
        
        if not self.generate_voice(script_data['script'], audio_path):
            print("❌ Failed to generate audio")
            return None
        
        # Create video
        video_path = OUTPUT_DIR / f"LINCOLN_COMEDY_{script_data['episode']}_{timestamp}.mp4"
        
        if not self.create_video_with_ffmpeg(audio_path, video_path, script_data):
            print("❌ Failed to create video")
            return None
        
        # Prepare YouTube metadata
        description = f"""{script_data['script']}

🎭 ABRAHAM LINCOLN COMEDY - Episode #{script_data['episode']}
Comedy Style: {script_data['style'].replace('_', ' ').title()}

Created with modern AI comedy writing
Bitcoin: bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt

#comedy #shorts #lincolnreacts #funny #satire"""
        
        # Upload to YouTube
        video_url = self.upload_to_youtube(
            video_path,
            script_data['title'],
            description,
            script_data['tags']
        )
        
        if video_url:
            print("\n" + "="*70)
            print("✅ VIDEO SUCCESSFULLY CREATED AND UPLOADED!")
            print("="*70)
            print(f"\n📺 Watch at: {video_url}")
            print(f"📁 Local file: {video_path}")
            
            # Save metadata
            metadata = {
                'headline': headline,
                'title': script_data['title'],
                'episode': script_data['episode'],
                'style': script_data['style'],
                'url': video_url,
                'local_path': str(video_path),
                'timestamp': timestamp,
                'tags': script_data['tags']
            }
            
            metadata_file = OUTPUT_DIR / f"metadata_{script_data['episode']}.json"
            metadata_file.write_text(json.dumps(metadata, indent=2))
            
            return video_url
        else:
            print("\n⚠️ Video created but not uploaded")
            print(f"📁 Local file: {video_path}")
            return str(video_path)


if __name__ == "__main__":
    creator = VideoCreator()
    result = creator.create_and_upload()
    
    if result:
        print("\n🎉 Success! Video is ready.")
    else:
        print("\n❌ Failed to complete video creation.")