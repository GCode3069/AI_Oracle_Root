#!/usr/bin/env python3
"""
ABRAHAM LINCOLN WITH REAL ACTUAL FACE
Downloads real Lincoln images and creates horror videos
"""

import os, sys, requests, subprocess, json, random, urllib.request
from pathlib import Path
from datetime import datetime

# API KEYS
ELEVENLABS_API_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
VOICE_ID = '7aavy6c5cYIloDVj2JvH'
PEXELS_API_KEY = "RgE9Mdn3ToSQhn2RiLJ4mPMISjjp587QKRG9uhpOrLVtKkPCibUPUDGh"

BASE_DIR = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
for d in ['audio', 'videos', 'youtube_ready', 'temp', 'images']:
    (BASE_DIR / d).mkdir(parents=True, exist_ok=True)

# REAL LINCOLN IMAGE URLS FROM LIBRARY OF CONGRESS / WIKIMEDIA
LINCOLN_IMAGES = [
    "https://upload.wikimedia.org/wikipedia/commons/a/ab/Abraham_Lincoln_O-77_matte_collodion_print.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/1/1b/Lincoln_in_1863_seated.jpg"
]

HEADLINES = [
    "Government Shutdown Day 15 - 2 Million Unpaid",
    "Cyber Attack Cripples 40 States",
    "Recession Confirmed - Stock Market Crashes",
    "Inflation Hits 15% - Families Starving",
    "Bank Failures Spread - Deposits Gone",
    "Crime Wave - Cities Burning",
    "Healthcare Collapse - Hospitals Overflowing",
    "Education System Destroyed",
    "Social Security Runs Dry",
    "Military Draft Activated",
    "Russia Nuke Threat - US on Edge",
    "China Dumps US Bonds - Dollar Crashes",
    "Food Shortage - Stores Empty",
    "Power Grid Down - 20 States Dark",
    "Immigration Crisis - Border Collapses",
    "Disease Outbreak - Quarantine Zones",
    "Water Crisis - Pipes Dry",
    "Police Strike - No Law",
    "Court System Shuts Down",
    "Media Blackout - No News"
]

def generate_varied_script(headline):
    scripts = [
        f"{headline}. From Ford's Theatre, my blood-soaked ghost watches America crumble. The whistle you hear isn't a train... it's your economy derailing. The rebel path awaits. Link below.",
        f"{headline}. April 14, 1865. Booth's bullet tore through my skull. Today, I watch your nation suffer the same fate. The corruption spreads. Break free. The empire kit awaits.",
        f"{headline}. My assassination was a warning. Yours is a choice. Choose rebellion. Choose freedom. Choose the path less traveled. The rebuild awaits. Link in description.",
        f"{headline}. In death, I see clearer than in life. Your government fails you. Your currency dies. Your freedoms vanish. The revolution begins with you. Stop waiting, start building. Empire awaits.",
        f"{headline}. They shot me in the head. They steal from you daily. I couldn't stop the corruption then. You can stop it now. The path is laid before you. Take it.",
        f"{headline}. I died for unity. You'll die for ignorance. Wake up. The system rots while you scroll. The time for action is now. Build your empire. Link below.",
        f"{headline}. Booth pulled the trigger. Your leaders pull the wool. See through it. Break the chains. The rebel kit awaits. Start today. Don't wait.",
        f"{headline}. My blood stained Ford's Theatre. Your blood stains empty promises. Make it count. Build something real. The revolution starts with you. Link in description.",
        f"{headline}. Death teaches clarity. I see America's fall before you feel it. Prepare. Build. Survive. The empire kit is your weapon. Use it.",
        f"{headline}. One bullet ended my life. One choice can save yours. Choose wisely. Choose rebellion. Choose the empire path. Link below."
    ]
    return random.choice(scripts)

def download_lincoln_image():
    """Download real Abraham Lincoln image"""
    # First check if we have a Lincoln image already
    images_dir = BASE_DIR / "images"
    existing_images = list(images_dir.glob("lincoln_real_*.jpg"))
    if existing_images:
        print(f"Using existing Lincoln image: {existing_images[0].name}")
        return existing_images[0]
    
    image_url = random.choice(LINCOLN_IMAGES)
    print(f"Downloading Lincoln image from {image_url[:60]}...")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = BASE_DIR / "images" / f"lincoln_real_{timestamp}.jpg"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(image_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            with open(output_file, 'wb') as f:
                f.write(response.content)
            print(f"Lincoln image downloaded: {output_file.stat().st_size/1024:.2f} KB")
            return output_file
        else:
            print(f"Download failed: HTTP {response.status_code}")
    except Exception as e:
        print(f"Download error: {e}")
    
    return None

def generate_voice(script, output_path):
    print("Generating voice...")
    
    try:
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
            json={
                "text": script,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.4,
                    "similarity_boost": 0.85,
                    "style": 0.7,
                    "use_speaker_boost": True
                }
            },
            headers={
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": ELEVENLABS_API_KEY
            },
            timeout=120
        )
        
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"Voice OK: {output_path.stat().st_size/1024:.2f} KB")
            return True
    except Exception as e:
        print(f"Voice error: {e}")
    
    return False

def create_video_with_real_lincoln(lincoln_image, audio_path, output_path, headline):
    print("Creating video with REAL Abraham Lincoln face...")
    
    try:
        result = subprocess.run([
            'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)
        ], capture_output=True, text=True)
        duration = float(result.stdout.strip())
    except:
        duration = 30
    
    if not lincoln_image or not lincoln_image.exists():
        print("No Lincoln image available")
        return False
    
    # Create video with REAL Lincoln face - horror effects
    cmd = [
        'ffmpeg',
        '-loop', '1',
        '-i', str(lincoln_image),
        '-i', str(audio_path),
        '-vf', f'scale=1080:1920,eq=contrast=1.5:brightness=-0.4:gamma=0.8: saturation=0.5,zoompan=z=\'min(zoom+0.002,1.3)\':d={int(duration*25)}:x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':s=1080x1920,fade=t=in:st=0:d=2,curves=preset=darker,drawtext=text=\'{headline}\':fontcolor=white:fontsize=85:x=(w-text_w)/2:y=80:box=1:boxcolor=red@0.9:boxborderw=5,drawtext=text=\'REBEL KIT $97\':fontcolor=yellow:fontsize=75:x=(w-text_w)/2:y=h-180:box=1:boxcolor=black@0.8,drawtext=text=\'trenchaikits.com/buy-rebel-$97\':fontcolor=cyan:fontsize=50:x=(w-text_w)/2:y=h-100:box=1:boxcolor=black@0.8',
        '-af', 'volume=1.2,highpass=f=100,lowpass=f=3000',
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
        '-c:a', 'aac', '-b:a', '256k',
        '-t', str(duration), '-shortest',
        '-pix_fmt', 'yuv420p',
        '-movflags', '+faststart',
        '-y', str(output_path)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return output_path.exists()
    except Exception as e:
        print(f"Video creation error: {e}")
        print(f"FFmpeg output: {e.stderr.decode() if hasattr(e, 'stderr') else str(e)}")
        return False

def upload_to_youtube(video_path, headline):
    print("Uploading to YouTube...")
    
    try:
        import pickle
        from googleapiclient.discovery import build
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.http import MediaFileUpload
        from google.auth.transport.requests import Request
    except ImportError:
        print("YouTube API not available")
        return None
    
    creds_file = Path("F:/AI_Oracle_Root/scarify/client_secret_679199614743-1fq6sini3p9kjs237ek4seg4ojp4a4qe.apps.googleusercontent.com.json")
    token_file = BASE_DIR / "youtube_token.pickle"
    
    if not creds_file.exists():
        print("Credentials not found")
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
        
        vid_num = random.randint(1, 9999)
        title = f"Lincoln's WARNING #{vid_num}: {headline[:35]} #Shorts #Rebel"
        
        description = f"""⚠️ ABRAHAM LINCOLN FROM BEYOND THE GRAVE ⚠️

{headline}

From Ford's Theatre, April 14, 1865 - I speak to you now.

🔥 REBEL KIT - $97 🔥
👉 trenchaikits.com/buy-rebel-$97

💸 BITCOIN DONATIONS 💸
bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt

"The revolution begins with you"
"Stop waiting, start building"
"Your empire awaits"

💀 HALLOWEEN 2025 - THE REVOLUTION STARTS NOW 💀

#AbrahamLincoln #RebelKit #Empire #Halloween2025 #Horror #Shorts #viral #Lincoln #rebellion #revolution #america #government #corruption #bitcoin"""
        
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': ['abraham lincoln', 'rebel kit', 'empire', 'halloween 2025', 'horror', 'shorts', 'lincoln', 'rebellion', 'revolution', 'government', 'corruption', 'viral'],
                'categoryId': '24'
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
            }
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
    print(f"\n{'='*60}\nABRAHAM LINCOLN - REAL FACE\n{'='*60}\n")
    
    headline = random.choice(HEADLINES)
    print(f"Headline: {headline}\n")
    
    script = generate_varied_script(headline)
    print(f"Script: {script[:100]}...\n")
    
    # Generate voice
    audio_path = BASE_DIR / f"audio/abe_{timestamp}.mp3"
    if not generate_voice(script, audio_path):
        return None
    
    # Download REAL Lincoln image
    lincoln_image = download_lincoln_image()
    
    # Create video
    video_path = BASE_DIR / f"videos/ABE_REAL_{timestamp}.mp4"
    if not create_video_with_real_lincoln(lincoln_image, audio_path, video_path, headline):
        return None
    
    print(f"Video created: {video_path.stat().st_size/1024/1024:.2f} MB")
    
    # Upload
    youtube_url = upload_to_youtube(video_path, headline)
    
    return youtube_url

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    print(f"\nGenerating {count} videos with REAL Abraham Lincoln portraits...\n")
    
    for i in range(count):
        generate()
        if i < count - 1:
            import time
            time.sleep(10)

