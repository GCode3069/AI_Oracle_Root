#!/usr/bin/env python3
"""
ABRAHAM LINCOLN - WITH ACTUAL FACE GENERATED
Uses Stability AI to create real Lincoln visuals, Pollo AI for video, ElevenLabs for voice
NO MORE BORING DARK BACKGROUNDS
"""

import os, sys, requests, subprocess, json, random
from pathlib import Path
from datetime import datetime

# API KEYS
STABILITY_API_KEY = "sk-sP93JLezaVNYpifbSDf9sn0rUaxhir377fJJV9Vit0nOEPQ1"
ELEVENLABS_API_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
POLLO_API_KEY = "pollo_5EW9VjxB2eAUknmhd9vb9F2OJFDjPVVZttOQJRaaQ248"
VOICE_ID = '7aavy6c5cYIloDVj2JvH'
PEXELS_API_KEY = "RgE9Mdn3ToSQhn2RiLJ4mPMISjjp587QKRG9uhpOrLVtKkPCibUPUDGh"

BASE_DIR = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
for d in ['audio', 'videos', 'youtube_ready', 'temp', 'images']:
    (BASE_DIR / d).mkdir(parents=True, exist_ok=True)

# ==============================================================================
# LINCOLN VISUAL GENERATION - ACTUAL FACES
# ==============================================================================

LINCOLN_VISUAL_PROMPTS = [
    "Abraham Lincoln portrait, haunted, ghostly face emerging from darkness, blood-soaked beard, hollow eyes, Ford's Theatre background, cinematic horror lighting, 1800s photography style, monochromatic with red blood accents, ultra realistic, 4k",
    "Abraham Lincoln's skull, cracked open, brain visible, derringer pistol, Victorian horror aesthetic, bone fragments, blood dripping, gothic dark atmosphere, ultra detailed, cinematic, 4k",
    "Abraham Lincoln's ghostly face, crying blood, presidential coat torn, Ford's Theatre stage behind, April 14 1865, horror cinematography, desaturated colors with red highlights, photorealistic, 4k",
    "Abraham Lincoln portrait, face partially decomposed, maggots, eyes missing, Presidential box at Ford's Theatre in background, blood-stained clothing, horror macabre, detailed gore, cinematic lighting, 4k",
    "Abraham Lincoln's corpse, sitting in theatre seat, head wound visible, John Wilkes Booth shadow in background, candlelight, Victorian horror, detailed gore, blood-soaked, realistic, 4k"
]

def generate_lincoln_face():
    """Generate actual Abraham Lincoln face using Stability AI"""
    print("Generating Abraham Lincoln face...")
    
    prompt = random.choice(LINCOLN_VISUAL_PROMPTS)
    
    try:
        response = requests.post(
            "https://api.stability.ai/v2beta/stable-image/generate/sd3",
            headers={
                "Authorization": f"Bearer {STABILITY_API_KEY}",
                "Accept": "image/*"
            },
            files={"none": ""},
            data={
                "prompt": prompt,
                "model": "sd3.5-large-turbo",
                "aspect_ratio": "9:16",
                "output_format": "png",
                "seed": random.randint(0, 999999999),
                "negative_prompt": "cartoon, anime, painting, illustration, low quality, blurry"
            },
            timeout=120
        )
        
        if response.status_code == 200:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = BASE_DIR / "images" / f"lincoln_face_{timestamp}.png"
            with open(output_file, 'wb') as f:
                f.write(response.content)
            print(f"Lincoln face generated: {output_file.stat().st_size/1024:.2f} KB")
            return output_file
        else:
            print(f"Stability API error: {response.status_code}")
    except Exception as e:
        print(f"Stability AI error: {e}")
    
    return None

# ==============================================================================
# VARIED HEADLINES & SCRIPTS
# ==============================================================================

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
    "Military Draft Activated"
]

def generate_varied_script(headline):
    """Generate unique script for each video"""
    
    scripts = [
        f"{headline}. From Ford's Theatre, my blood-soaked ghost watches America crumble. The whistle you hear isn't a train... it's your economy derailing. The rebel path awaits. Link below.",
        
        f"{headline}. April 14, 1865. Booth's bullet tore through my skull. Today, I watch your nation suffer the same fate. The corruption spreads. Break free. The empire kit awaits.",
        
        f"{headline}. My assassination was a warning. Yours is a choice. Choose rebellion. Choose freedom. Choose the path less traveled. The rebuild awaits. Link in description.",
        
        f"{headline}. In death, I see clearer than in life. Your government fails you. Your currency dies. Your freedoms vanish. The revolution begins with you. Stop waiting, start building. Empire awaits.",
        
        f"{headline}. They shot me in the head. They steal from you daily. I couldn't stop the corruption then. You can stop it now. The path is laid before you. Take it."
    ]
    
    return random.choice(scripts)

# ==============================================================================
# VOICE GENERATION
# ==============================================================================

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

# ==============================================================================
# VIDEO GENERATION WITH LINCOLN FACE
# ==============================================================================

def create_video_with_lincoln_face(lincoln_image, audio_path, output_path, headline):
    """Create video with actual Lincoln face overlay"""
    
    print("Creating video with Lincoln face overlay...")
    
    try:
        result = subprocess.run([
            'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)
        ], capture_output=True, text=True)
        duration = float(result.stdout.strip())
    except:
        duration = 30
    
    if not lincoln_image or not lincoln_image.exists():
        print("No Lincoln image, using stock video")
        return get_stock_video_fallback(audio_path, output_path, headline, duration)
    
    # Create video with Lincoln face overlay on dark background
    cmd = [
        'ffmpeg',
        '-loop', '1',
        '-i', str(lincoln_image),
        '-i', str(audio_path),
        '-vf', f'scale=1080:1920,eq=contrast=1.3:brightness=-0.2:gamma=1.1,zoompan=z=\'min(zoom+0.001,1.2)\':d={int(duration*25)}:x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':s=1080x1920,drawtext=text=\'{headline}\':fontcolor=white:fontsize=80:x=(w-text_w)/2:y=100:box=1:boxcolor=black@0.8,drawtext=text=\'REBEL KIT $97\':fontcolor=yellow:fontsize=70:x=(w-text_w)/2:y=750:box=1:boxcolor=black@0.8',
        '-af', 'volume=0.8',
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
        '-c:a', 'aac', '-b:a', '192k',
        '-t', str(duration), '-shortest',
        '-pix_fmt', 'yuv420p',
        '-y', str(output_path)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return output_path.exists()
    except Exception as e:
        print(f"Video creation error: {e}")
        return False

def get_stock_video_fallback(audio_path, output_path, headline, duration):
    """Fallback to stock video if Lincoln generation fails"""
    
    try:
        response = requests.get(
            "https://api.pexels.com/videos/search",
            headers={"Authorization": PEXELS_API_KEY},
            params={"query": "abraham lincoln memorial", "per_page": 1},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('videos'):
                video = data['videos'][0]
                video_files = video.get('video_files', [])
                if video_files:
                    video_file = max(video_files, key=lambda x: x.get('width', 0))
                    vid_resp = requests.get(video_file.get('link'), timeout=120)
                    temp_file = BASE_DIR / "temp" / f"stock_{random.randint(1000,9999)}.mp4"
                    with open(temp_file, 'wb') as f:
                        f.write(vid_resp.content)
                    
                    cmd = [
                        'ffmpeg', '-i', str(temp_file), '-i', str(audio_path),
                        '-vf', f'eq=contrast=1.3:brightness=-0.2,drawtext=text=\'{headline}\':fontcolor=white:fontsize=80:x=(w-text_w)/2:y=100:box=1:boxcolor=black@0.8',
                        '-af', 'volume=0.8',
                        '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
                        '-c:a', 'aac', '-b:a', '192k',
                        '-t', str(duration), '-shortest',
                        '-map', '0:v:0', '-map', '1:a:0',
                        '-y', str(output_path)
                    ]
                    
                    subprocess.run(cmd, capture_output=True)
                    return output_path.exists()
    except Exception as e:
        print(f"Fallback error: {e}")
    
    return False

# ==============================================================================
# YOUTUBE UPLOAD
# ==============================================================================

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
        
        # Unique title for each video
        title = f"Lincoln's Warning #{random.randint(1,1000)}: {headline[:40]} #Shorts"
        
        description = f"""{headline}

⚠️ ABRAHAM LINCOLN FROM BEYOND THE GRAVE

Ford's Theatre, April 14, 1865. The assassination that changed history.

🔥 REBEL KIT - $97
trenchaikits.com/buy-rebel-$97

"The revolution begins with you"
"Stop waiting, start building"  
"Your empire awaits"

#Halloween2025 #AbrahamLincoln #Horror #Shorts #Rebel #Empire #viral #Lincoln"""
        
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': ['abraham lincoln', 'rebel kit', 'empire', 'halloween 2025', 'horror', 'shorts', 'lincoln'],
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

# ==============================================================================
# MAIN GENERATOR
# ==============================================================================

def generate():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    print(f"\n{'='*60}\nABRAHAM LINCOLN - ACTUAL FACE\n{'='*60}\n")
    
    headline = random.choice(HEADLINES)
    print(f"Headline: {headline}\n")
    
    script = generate_varied_script(headline)
    print(f"Script: {script[:80]}...\n")
    
    # Generate voice
    audio_path = BASE_DIR / f"audio/abe_{timestamp}.mp3"
    if not generate_voice(script, audio_path):
        return None
    
    # Generate Lincoln face
    lincoln_face = generate_lincoln_face()
    
    # Create video
    video_path = BASE_DIR / f"videos/ABE_{timestamp}.mp4"
    if not create_video_with_lincoln_face(lincoln_face, audio_path, video_path, headline):
        return None
    
    print(f"Video created: {video_path.stat().st_size/1024/1024:.2f} MB")
    
    # Upload
    youtube_url = upload_to_youtube(video_path, headline)
    
    return youtube_url

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    print(f"\nGenerating {count} videos with REAL Abraham Lincoln faces...\n")
    
    for i in range(count):
        generate()
        if i < count - 1:
            import time
            time.sleep(5)

