#!/usr/bin/env python3
import os, sys, requests, subprocess, json
from pathlib import Path
from datetime import datetime
import random

ELEVENLABS_API_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
LINCOLN_VOICES = [
    '21m00Tcm4TlvDq8ikWAM',
    'AZnzlk1XvdvUeBnXmlld',
    'pNInz6obpgDQGcFmaJgB',
]
VOICE_ID = LINCOLN_VOICES[0]
PEXELS_API_KEY = "RgE9Mdn3ToSQhn2RiLJ4mPMISjjp587QKRG9uhpOrLVtKkPCibUPUDGh"

BASE_DIR = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
for d in ['audio', 'videos', 'youtube_ready', 'temp']:
    (BASE_DIR / d).mkdir(parents=True, exist_ok=True)

def get_headlines():
    return ["Government Shutdown Day 15", "Major Cyber Attack", "Recession Signals"]

def generate_script(headline):
    return f"I am Abraham Lincoln speaking from death. {headline} unfolds before my eyes. Death could not silence me. My voice echoes through time. Sic semper tyrannis."

def generate_voice(script, output_path):
    print("Generating voice...")
    try:
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
            json={"text": script, "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.5}},
            headers={"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": ELEVENLABS_API_KEY},
            timeout=120
        )
        if response.status_code == 200:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"Voice OK: {output_path.stat().st_size/1024:.2f} KB")
            return True
    except Exception as e:
        print(f"Voice failed: {e}")
    return False

def get_stock_video(keyword):
    print(f"Getting stock video: {keyword}")
    try:
        response = requests.get("https://api.pexels.com/videos/search", headers={"Authorization": PEXELS_API_KEY}, params={"query": keyword, "per_page": 1}, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if data.get('videos'):
                videos = data['videos']
                video = videos[0]
                video_files = video.get('video_files', [])
                if video_files:
                    video_file = max(video_files, key=lambda x: x.get('width',0)*x.get('height',0))
                    download_url = video_file.get('link')
                    vid_resp = requests.get(download_url, timeout=120)
                    temp_file = BASE_DIR / "temp" / f"stock_{random.randint(1000,9999)}.mp4"
                    temp_file.parent.mkdir(parents=True, exist_ok=True)
                    with open(temp_file, 'wb') as f:
                        f.write(vid_resp.content)
                    print(f"Saved stock video: {temp_file.name}")
                    return temp_file
    except Exception as e:
        print(f"Pexels error: {e}")
    return None

def create_video(stock_video, audio_path, output_path, headline):
    print("Creating video...")
    try:
        result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)], capture_output=True, text=True)
        duration = float(result.stdout.strip())
    except:
        duration = 30
    
    if not stock_video or not audio_path.exists():
        return False
    
    cmd = [
        'ffmpeg', '-i', str(stock_video), '-i', str(audio_path),
        '-vf', 'eq=contrast=1.4:brightness=-0.3,drawtext=text="LINCOLN":fontcolor=red:fontsize=80:x=(w-text_w)/2:y=50',
        '-af', 'volume=3.0',
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
        '-c:a', 'aac', '-b:a', '256k',
        '-t', str(duration), '-shortest', '-map', '0:v:0', '-map', '1:a:0',
        '-y', str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return output_path.exists()

def upload_to_youtube(video_path, headline):
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
    
    creds_file = Path("client_secret_679199614743-1fq6sini3p9kjs237ek4seg4ojp4a4qe.apps.googleusercontent.com.json")
    token_file = BASE_DIR / "youtube_token.pickle"
    
    if not creds_file.exists():
        print("YouTube credentials not found")
        return None
    
    try:
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
        
        youtube = build('youtube', 'v3', credentials=creds)
        
        title = f"Lincoln's Warning: {headline[:50]} #Shorts"
        description = f"""{headline}

LINCOLN'S WARNING FROM BEYOND THE GRAVE

Abraham Lincoln speaks from Ford's Theatre, April 14, 1865...

#Halloween2025 #AbrahamLincoln #Horror #Shorts #viral"""
        
        tags = ['abraham lincoln', 'halloween 2025', 'horror', 'shorts', 'viral']
        
        body = {
            'snippet': {'title': title, 'description': description, 'tags': tags, 'categoryId': '24'},
            'status': {'privacyStatus': 'public', 'selfDeclaredMadeForKids': False}
        }
        
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
