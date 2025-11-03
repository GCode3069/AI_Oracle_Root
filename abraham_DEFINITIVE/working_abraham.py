#!/usr/bin/env python3
import os, sys, requests, subprocess, json
from pathlib import Path
from datetime import datetime
import random

ELEVENLABS_API_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
# Better voices for Lincoln - more natural, less robotic
LINCOLN_VOICES = [
    '21m00Tcm4TlvDq8ikWAM',  # Rachel - clear, natural
    'AZnzlk1XvdvUeBnXmlld',  # Domi - energetic, expressive
    'pNInz6obpgDQGcFmaJgB',  # Adam - natural male voice
    'EXAVITQu4vr4xnSDxMaL',  # Bella - natural female voice
    'TxGEqnHWrfWFTfGW9XjX',  # Joshua - dramatic
]
VOICE_ID = LINCOLN_VOICES[0]  # Use Abraham by default
PEXELS_API_KEY = "RgE9Mdn3ToSQhn2RiLJ4mPMISjjp587QKRG9uhpOrLVtKkPCibUPUDGh"
POLLO_API_KEY = "pollo_5EW9VjxB2eAUknmhd9vb9F2OJFDjPVVZttOQJRaaQ248"
STABILITY_API_KEY = "sk-sP93JLezaVNYpifbSDf9sn0rUaxhir377fJJV9Vit0nOEPQ1"

BASE_DIR = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
for d in ['audio', 'videos', 'youtube_ready', 'temp']:
    (BASE_DIR / d).mkdir(parents=True, exist_ok=True)

def get_headlines():
    return ["Government Shutdown Day 15", "Major Cyber Attack", "Recession Signals", "Extreme Weather Spreads"]

def generate_script(headline):
    """Generate GRAPHIC Lincoln horror with gore"""
    gory_templates = [
        f"""{headline}.

*crack* *squelch* My skull fragments grind in bloody marble as I witness this rot.

Occiput explodes, bone shards paint the walls.

Sic semper tyrannis—I carve this curse into your nightmares.

The purge costs $97. Join me in the gory legacy, or bleed alone.

This is Abraham Lincoln's spectral butchery.""",
        
        f"""{headline}.

*gurgle* My jaw unhinges, arterial blood floods the theatre.

They thought I was dead. I'm not. I'm hunting.

Sic semper tyrannis—your corruption ends in blood-soaked justice.

$97 secures your place in the purge. Or face the derringer.

Lincoln's ghost demands your fear.""",
        
        f"""{headline}.

*probing fingers squelch in gray matter*

Brain matter sprays like election confetti across Ford's Theatre.

My derringer still speaks. My bones still rattle.

Sic semper tyrannis—pay $97 or pay with your skull.

This is Lincoln's curse. Your purge awaits."""
    ]
    
    import random
    return random.choice(gory_templates)

def generate_voice(script, output_path):
    """Generate voice with better settings for natural Lincoln sound"""
    print("Generating voice...")
    
    # Try different voices if one fails
    for voice_id in LINCOLN_VOICES:
        try:
            response = requests.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                json={
                    "text": script,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {
                        "stability": 0.5,  # Increased for more consistent pronunciation
                        "similarity_boost": 0.9,  # Higher for more voice-like quality
                        "style": 0.2,  # Subtle style
                        "use_speaker_boost": True  # Improve voice quality
                    }
                },
                headers={"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": ELEVENLABS_API_KEY},
                timeout=120
            )
            if response.status_code == 200:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                print(f"Voice OK ({voice_id}): {output_path.stat().st_size/1024:.2f} KB")
                return True
            print(f"Voice {voice_id} failed: {response.status_code}")
        except Exception as e:
            print(f"Voice {voice_id} error: {e}")
            continue
    
    print("All voices failed")
    return False

def get_stock_video(keyword):
    print(f"Getting stock video: {keyword}")
    try:
        response = requests.get("https://api.pexels.com/videos/search", headers={"Authorization": PEXELS_API_KEY}, params={"query": keyword, "per_page": 1}, timeout=30)
        print(f"Pexels API status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Pexels response: {data.keys()}")
            
            if data.get('videos'):
                videos = data['videos']
                print(f"Found {len(videos)} videos")
                
                video = videos[0]
                video_files = video.get('video_files', [])
                print(f"Found {len(video_files)} video files")
                
                if video_files:
                    video_file = max(video_files, key=lambda x: x.get('width',0)*x.get('height',0))
                    download_url = video_file.get('link')
                    print(f"Downloading from: {download_url}")
                    
                    vid_resp = requests.get(download_url, timeout=120)
                    print(f"Download status: {vid_resp.status_code}")
                    
                    temp_file = BASE_DIR / "temp" / f"stock_{random.randint(1000,9999)}.mp4"
                    temp_file.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(temp_file, 'wb') as f:
                        f.write(vid_resp.content)
                    
                    print(f"Saved stock video: {temp_file.name} ({temp_file.stat().st_size/1024:.2f} KB)")
                    return temp_file
    except Exception as e:
        print(f"Pexels error: {e}")
    
    print("No stock video available")
    return None

def create_video(stock_video, audio_path, output_path, headline):
    print("Creating video with MAXIMUM HORROR effects...")
    try:
        result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)], capture_output=True, text=True)
        duration = float(result.stdout.strip())
    except:
        duration = 30
    
    print(f"Duration: {duration}s")
    
    if not stock_video or not stock_video.exists():
        print("ERROR: No stock video")
        return False
    
    # Verify audio file exists
    if not audio_path.exists():
        print(f"ERROR: Audio file missing: {audio_path}")
        return False
    
    print(f"Using stock video: {stock_video}")
    print(f"Using audio: {audio_path}")
    
    # Create video with MAXIMUM HORROR EFFECTS:
    # - Blood-red color grading
    # - Multiple horror text overlays with effects
    # - Intense audio boost
    # - Glitch effects
    # - Lincoln-themed text
    
    video_filters = [
        # Color grading for blood-soaked horror
        "eq=contrast=1.6:brightness=-0.4:gamma=1.4",
        # Desaturate except red tones (blood effect)
        "hue=s=0.5",
        # Glitch effect
        "geq='if(gte(X,0),if(lte(X,10),p(X+10,Y),if(lte(X,W-10),p(X,Y),p(X-10,Y))),p(X,Y))'",
        # Main title with horror font (Arial Black as horror substitute)
        f"drawtext=text='ABRAHAM LINCOLN':font=Arial:fontcolor=darkred:fontsize=80:x=(w-text_w)/2:y=50:box=1:boxcolor=black@0.9:boxborderw=5",
        # Subtitle with gore theme
        f"drawtext=text='\\\'S SPECTRAL CURSE':font=Arial:fontcolor=red:fontsize=60:x=(w-text_w)/2:y=150:box=1:boxcolor=black@0.8:boxborderw=3",
        # Headline with intense styling
        f"drawtext=text='{headline}':font=Arial:fontcolor=white:fontsize=70:x=(w-text_w)/2:y=h-200:box=1:boxcolor=red@0.7:boxborderw=8",
        # Bottom tagline
        "drawtext=text='SIC SEMPER TYRANNIS':font=Arial:fontcolor=darkred:fontsize=50:x=(w-text_w)/2:y=h-100"
    ]
    
    video_filter = ','.join(video_filters)
    
    # Audio filter with aggressive boost MEABLE audio is audible
    audio_filter = "volume=3.0,loudnorm=I=-16:TP=-1.5:LRA=11"
    
    cmd = [
        'ffmpeg', '-i', str(stock_video), 
        '-i', str(audio_path),
        '-vf', video_filter,
        '-af', audio_filter,
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', 
        '-c:a', 'aac', '-b:a', '256k', '-ar', '44100',
        '-t', str(duration), '-shortest',
        '-map', '0:v:0', '-map', '1:a:0',  # Ensure audio is mapped
        '-y', str(output_path)
    ]
    
    print(f"Creating with MAXIMUM horror effects...")
    print(f"Audio boost: 3.0x volume")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if output_path.exists():
        print(f"SUCCESS - Video: {output_path.stat().st_size/1024/1024:.2f} MB")
        return True
    else:
        print(f"FAILED - ffmpeg error: {result.stderr}")
        return False

def upload_to_youtube(video_path, headline):
    """Upload video directly to YouTube"""
    
    print("Uploading to YouTube...")
    
    try:
        import pickle
        from googleapiclient.discovery import build
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.http import MediaFileUpload
        from google.auth.transport.requests import Request
    except ImportError:
        print("YouTube API packages not installed")
        return None
    
    # Check for credentials
    creds_file = Path("client_secret_679199614743-1fq6sini3p9kjs237ek4seg4ojp4a4qe.apps.googleusercontent.com.json")
    token_file = BASE_DIR / "youtube_token.pickle"
    
    if not creds_file.exists():
        print("YouTube credentials not found")
        return None
    
    try:
        # Load or get credentials
        creds = None
        if token_file.exists():
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(creds_file),
                    ['https://www.googleapis.com/auth/youtube.upload']
                )
                creds = flow.run_local_server(port=8080)
            
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        # Build service
        youtube = build('youtube', 'v3', credentials=creds)
        
        # Prepare metadata
        title = f"Lincoln's Warning: {headline[:50]} #Shorts"
        description = f"""{headline}

⚠️ LINCOLN'S WARNING

From Ford's Theatre, April 14, 1865...

Abraham Lincoln speaks from beyond the grave.

#Halloween2025 #AbrahamLincoln #Horror #Shorts #viral"""

        tags = ['abraham lincoln', 'halloween 2025', 'horror', 'shorts', 'viral']
        
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': '24'  # Entertainment
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
                print(f"Upload: {int(status.progress() * 100)}%", end='\r')
        
        print()
        video_id = response['id']
        video_url = f"https://youtube.com/watch?v={video_id}"
        
        print(f"UPLOADED: {video_url}")
        return video_url
        
    except Exception as e:
        print(f"Upload error: {e}")
        return None

def generate():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    print(f"\n{'='*60}\nABRAHAM HORROR VIDEO\n{'='*60}\n")
    
    headlines = get_headlines()
    headline = random.choice(headlines)
    print(f"Headline: {headline}\n")
    
    script = generate_script(headline)
    
    audio_path = BASE_DIR / f"audio/abraham_{timestamp}.mp3"
    if not generate_voice(script, audio_path):
        return None
    
    stock_video = get_stock_video("dark horror")
    
    video_path = BASE_DIR / f"videos/ABRAHAM_{timestamp}.mp4"
    if not create_video(stock_video, audio_path, video_path, headline):
        return None
    
    # Upload to YouTube
    youtube_url = upload_to_youtube(video_path, headline)
    
    youtube_dir = BASE_DIR / "youtube_ready"
    youtube_file = youtube_dir / f"ABRAHAM_{timestamp}.mp4"
    
    import shutil
    shutil.copy2(video_path, youtube_file)
    
    if youtube_url:
        print(f"\nREADY: {youtube_file.name}")
        print(f"UPLOADED: {youtube_url}\n")
    else:
        print(f"\nREADY: {youtube_file.name}\n")
    
    return str(youtube_file)

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    print(f"\nGenerating {count} video(s)...\n")
    
    for i in range(count):
        generate()
        if i < count - 1:
            import time
            time.sleep(5)

