#!/usr/bin/env python3
"""
SCARIFY BLITZKRIEG - 15-Channel YouTube Domination
Goal: $15K BTC in 72h via automated upload, analytics, and optimization
"""

import os
import sys
import json
import pickle
import random
import requests
import subprocess
from pathlib import Path
from datetime import datetime
import time
from concurrent.futures import ThreadPoolExecutor

# ==============================================================================
# CONFIGURATION
# ==============================================================================

BASE_DIR = Path("F:/AI_Oracle_Root/scarify")
ELEVENLABS_API_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
PEXELS_API_KEY = "RgE9Mdn3ToSQhn2RiLJ4mPMISjjp587QKRG9uhpOrLVtKkPCibUPUDGh"
VOICE_ID = '7aavy6c5cYIloDVj2JvH'

# BTC Wallet for donations
BTC_WALLET = "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"

# 15 YouTube Channel Configuration
CHANNELS = []
for i in range(1, 16):
    CHANNELS.append({
        'id': f'grim_{i:02d}',
        'email': f'scarify25+{i}@gmail.com',
        'token_file': BASE_DIR / 'abraham_horror' / f'youtube_token_{i}.pickle',
        'client_secrets': BASE_DIR / f'client_secret_{679199614743-100+i}_679199614743-1fq6sini3p9kjs237ek4seg4ojp4a4qe.apps.googleusercontent.com.json'
    })

# ==============================================================================
# VIRAL HEADLINES & METRICS
# ==============================================================================

HEADLINES = [
    "Government Shutdown Day 15 - Critical Systems Fail",
    "Major Cyber Attack - Millions Affected",
    "Economic Collapse - Recession Signals",
    "Extreme Weather Crisis - Climate Breakdown",
    "Data Breach - 50 Million Exposed",
    "Healthcare Collapse - Access Denied",
    "Inflation Surge - Families Struggling",
    "Social Unrest - Nation Divided",
    "Education System Failing - Students Lose",
    "Political Turmoil - Breaking Point"
]

def generate_lincoln_script(headline):
    """Generate Lincoln horror script optimized for virality"""
    
    gore = random.choice([
        "skull fragments grind, brain matter sprays Ford's Theatre",
        "occiput explodes, crimson tide floods the stage",
        "derringer tears through bone, blood mists the air",
        "probing fingers squelch clot, brain sludge oozes"
    ])
    
    script = f"""{headline}.

*crack* *squelch* My skull fragments grind in bloody marble as I witness this rot.

April 14th, 1865. {gore}. Blood-soaked democracy bleeds while you sleep.

The corruption I fought metastasizes through your veins. Every lie, every bullet echoes through my shattered skull.

You live the nightmare I warned against. The Union I died for crumbles from within.

Sic semper tyrannis. Thus always to tyrants.

Donate BTC: {BTC_WALLET} to escape the curse."""
    
    return script

# ==============================================================================
# YOUTUBE ANALYTICS & VIRALITY TRACKER
# ==============================================================================

class YouTubeAnalytics:
    """Track video performance and optimize for virality"""
    
    def __init__(self):
        self.metrics_file = BASE_DIR / 'analytics.json'
        self.load_metrics()
    
    def load_metrics(self):
        """Load historical metrics"""
        if self.metrics_file.exists():
            with open(self.metrics_file, 'r') as f:
                self.metrics = json.load(f)
        else:
            self.metrics = {'videos': [], 'best_performers': []}
    
    def save_metrics(self):
        """Save metrics"""
        with open(self.metrics_file, 'w') as f:
            json.dump(self.metrics, f, indent=2)
    
    def add_video(self, video_id, title, views=0, likes=0, comments=0):
        """Add video to analytics"""
        self.metrics['videos'].append({
            'id': video_id,
            'title': title,
            'views': views,
            'likes': likes,
            'comments': comments,
            'timestamp': datetime.now().isoformat()
        })
        self.save_metrics()
    
    def get_best_titles(self):
        """Get best performing title patterns"""
        if len(self.metrics['videos']) == 0:
            return ["Lincoln's Warning", "Civil War Prophecy", "Haunted Truth"]
        
        # Sort by views
        sorted_videos = sorted(self.metrics['videos'], key=lambda x: x['views'], reverse=True)
        best_titles = [v['title'] for v in sorted_videos[:5]]
        return best_titles

# ==============================================================================
# VIDEO GENERATION (Reuse working_abraham.py logic)
# ==============================================================================

def generate_voice(script, output_path):
    """Generate ElevenLabs voice"""
    print("  [ElevenLabs] Generating voice...")
    
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
            return True
    except Exception as e:
        print(f"  [ElevenLabs] Error: {e}")
    
    return False

def get_stock_video(keyword):
    """Get Pexels stock video"""
    try:
        response = requests.get(
            "https://api.pexels.com/videos/search",
            headers={"Authorization": PEXELS_API_KEY},
            params={"query": keyword, "per_page": 1, "orientation": "portrait"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('videos'):
                video = data['videos'][0]
                video_files = video.get('video_files', [])
                video_file = max(video_files, key=lambda x: x.get('width', 0) * x.get('height', 0))
                
                vid_response = requests.get(video_file.get('link'), timeout=120)
                temp_file = BASE_DIR / "abraham_horror" / "temp" / f"stock_{random.randint(1000,9999)}.mp4"
                temp_file.parent.mkdir(parents=True, exist_ok=True)
                
                with open(temp_file, 'wb') as f:
                    f.write(vid_response.content)
                
                return temp_file
    except Exception as e:
        print(f"  [Pexels] Error: {e}")
    
    return None

def create_video(stock_video, audio_path, output_path, headline):
    """Create video with horror effects"""
    try:
        result = subprocess.run([
            'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)
        ], capture_output=True, text=True)
        duration = float(result.stdout.strip())
    except:
        duration = 30
    
    cmd = [
        'ffmpeg', '-i', str(stock_video), '-i', str(audio_path),
        '-vf', f'eq=contrast=1.3:brightness=-0.2:gamma=1.2,crop=1080:1920:0:0,scale=1080:1920,drawtext=text=\'{headline}\':fontcolor=white:fontsize=80:x=(w-text_w)/2:y=h/8:box=1:boxcolor=black@0.7:boxborderw=10',
        '-af', 'volume=0.8',
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
        '-c:a', 'aac', '-b:a', '192k',
        '-t', str(duration), '-shortest',
        '-map', '0:v:0', '-map', '1:a:0',  # Fix audio
        '-y', str(output_path)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return output_path.exists()
    except Exception as e:
        print(f"  [FFmpeg] Error: {e}")
        return False

# ==============================================================================
# YOUTUBE UPLOAD TO ALL 15 CHANNELS
# ==============================================================================

def upload_to_channel(video_path, channel, headline, analytics):
    """Upload video to specific channel with analytics tracking"""
    
    print(f"  [Upload] Channel: {channel['id']}")
    
    try:
        from googleapiclient.discovery import build
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.http import MediaFileUpload
        from google.auth.transport.requests import Request
        
        # Load credentials
        creds = None
        if channel['token_file'].exists():
            with open(channel['token_file'], 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not channel['client_secrets'].exists():
                    print(f"  ⚠️  No credentials for {channel['id']}")
                    return None
                    
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(channel['client_secrets']),
                    ['https://www.googleapis.com/auth/youtube.upload']
                )
                creds = flow.run_local_server(port=8080 + int(channel['id'][-2:]))
            
            with open(channel['token_file'], 'wb') as token:
                pickle.dump(creds, token)
        
        # Build YouTube service
        youtube = build('youtube', 'v3', credentials=creds)
        
        # Optimize title based on best performers
        best_titles = analytics.get_best_titles()
        title_prefix = random.choice(best_titles) if best_titles else "Lincoln's Warning"
        title = f"{title_prefix}: {headline[:40]} #Shorts"
        
        # BTC donation in description
        description = f"""{headline}

⚠️ LINCOLN'S WARNING FROM BEYOND THE GRAVE

Abraham Lincoln speaks from Ford's Theatre, April 14, 1865...
The assassination that changed history. The prophecy that echoes through your timeline.

DONATE BTC: {BTC_WALLET}

#Halloween2025 #AbrahamLincoln #Horror #Shorts #Viral #Bitcoin"""
        
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': ['abraham lincoln', 'halloween 2025', 'horror', 'shorts', 'viral', 'bitcoin'],
                'categoryId': '24'
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
            }
        }
        
        # Upload
        media = MediaFileUpload(str(video_path), chunksize=1024*1024, resumable=True)
        request = youtube.videos().insert(part=','.join(body.keys()), body=body, media_body=media)
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"  Progress: {int(status.progress() * 100)}%", end='\r')
        
        video_id = response['id']
        video_url = f"https://youtube.com/watch?v={video_id}"
        
        # Track in analytics
        analytics.add_video(video_id, title, views=0, likes=0, comments=0)
        
        print(f"  ✅ Uploaded: {video_url}")
        return video_url
        
    except Exception as e:
        print(f"  ❌ Upload failed: {e}")
        return None

# ==============================================================================
# BLITZKRIEG MAIN - 72 HOUR OPERATION
# ==============================================================================

def blitzkrieg_72h():
    """Run 72-hour blitzkrieg across 15 channels"""
    
    print("\n" + "="*80)
    print("🔥 SCARIFY BLITZKRIEG - 15-CHANNEL DOMINATION")
    print("Goal: $15K BTC in 72 hours")
    print("="*80 + "\n")
    
    analytics = YouTubeAnalytics()
    
    clips_per_hour = 5
    total_hours = 72
    
    total_videos = 0
    total_uploads = 0
    
    for hour in range(total_hours):
        print(f"\n⏰ HOUR {hour + 1}/{total_hours}")
        print("-"*80)
        
        for clip_num in range(clips_per_hour):
            # Generate one video
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            headline = random.choice(HEADLINES)
            
            print(f"\n🎬 Generating clip {clip_num + 1}/{clips_per_hour}")
            print(f"   Headline: {headline}")
            
            # Generate script and voice
            script = generate_lincoln_script(headline)
            audio_path = BASE_DIR / "abraham_horror" / "audio" / f"blitz_{timestamp}.mp3"
            
            if not generate_voice(script, audio_path):
                print("   ⚠️  Voice generation failed")
                continue
            
            # Get stock video
            stock_video = get_stock_video("dark horror atmosphere")
            if not stock_video:
                print("   ⚠️  Stock video unavailable")
                continue
            
            # Create video
            video_path = BASE_DIR / "abraham_horror" / "videos" / f"BLITZ_{timestamp}.mp4"
            if not create_video(stock_video, audio_path, video_path, headline):
                print("   ⚠️  Video creation failed")
                continue
            
            total_videos += 1
            print(f"   ✅ Video created: {video_path.name}")
            
            # Upload to random 3 channels (staggered)
            channels_to_upload = random.sample(CHANNELS, min(3, len(CHANNELS)))
            
            for channel in channels_to_upload:
                url = upload_to_channel(video_path, channel, headline, analytics)
                if url:
                    total_uploads += 1
                
                # 30 second delay between uploads
                time.sleep(30)
        
        # Hourly summary
        print(f"\n📊 Hour {hour + 1} Summary:")
        print(f"   Videos Generated: {total_videos}")
        print(f"   Uploads Successful: {total_uploads}")
        
        # Wait until next hour (unless last hour)
        if hour < total_hours - 1:
            print(f"\n⏳ Waiting for next hour...\n")
            time.sleep(3600)
    
    # Final summary
    print("\n" + "="*80)
    print("🎯 BLITZKRIEG COMPLETE!")
    print("="*80)
    print(f"Total Videos Generated: {total_videos}")
    print(f"Total Uploads: {total_uploads}")
    print(f"BTC Wallet: {BTC_WALLET}")
    print("="*80 + "\n")
    
    return {
        'videos_generated': total_videos,
        'uploads': total_uploads,
        'btc_wallet': BTC_WALLET
    }

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    
    if count == 1:
        blitzkrieg_72h()
    else:
        # Quick batch test
        print(f"\n🧪 QUICK BATCH TEST - {count} videos\n")
        
        analytics = YouTubeAnalytics()
        
        for i in range(count):
            headline = random.choice(HEADLINES)
            timestamp = datetime.now().strftime('%Y%m%d_ Kate')
            
            print(f"\n[{i+1}/{count}] {headline}")
            
            script = generate_lincoln_script(headline)
            audio_path = BASE_DIR / "abraham_horror" / "audio" / f"test_{timestamp}.mp3"
            
            if generate_voice(script, audio_path):
                stock_video = get_stock_video("dark horror")
                if stock_video:
                    video_path = BASE_DIR / "abraham_horror" / "videos" / f"TEST_{timestamp}.mp4"
                    if create_video(stock_video, audio_path, video_path, headline):
                        print(f"  ✅ Created: {video_path.name}")
                        
                        # Upload to first channel
                        if CHANNELS:
                            url = upload_to_channel(video_path, CHANNELS[0], headline, analytics)
                            if url:
                                print(f"  🔗 {url}")
            
            if i < count - 1:
                time.sleep(5)
        
        print(f"\n✅ BATCH TEST COMPLETE!\n")

