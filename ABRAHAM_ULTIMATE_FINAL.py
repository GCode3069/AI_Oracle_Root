#!/usr/bin/env python3
"""
ABRAHAM LINCOLN - ULTIMATE FINAL EDITION
Combines all best features:
- Real Lincoln images from Wikimedia
- Max Headroom TV static effects
- Chapman 2025 fear-based targeting
- Auto-upload to YouTube
- Bitcoin/product integration
"""
import os, sys, json, requests, subprocess, random, time
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

# API Keys
ELEVENLABS_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
PEXELS_KEY = "RgE9Mdn3ToSQhn2RiLJ4mPMISjjp587QKRG9uhpOrLVtkKPCibUPUDGh"
VOICE = "pNInz6obpgDQGcFmaJgB"
BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
BTC = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"
REBEL_KIT = "trenchaikits.com/buy-rebel-$97"

# Real Lincoln image URLs
LINCOLN_IMAGES = [
    "https://upload.wikimedia.org/wikipedia/commons/a/ab/Abraham_Lincoln_O-77_matte_collodion_print.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/1/1b/Lincoln_in_1863_seated.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Lincoln_in_1863_seated.jpg/256px-Lincoln_in_1863_seated.jpg"
]

# Setup directories
for d in ['audio', 'videos', 'youtube_ready', 'temp', 'images', 'uploaded']:
    (BASE / d).mkdir(parents=True, exist_ok=True)

def load_chapman_2025_config():
    """Load Chapman 2025 fear data for targeting"""
    try:
        import yaml
        config_path = Path("configs/chapman_2025.yaml")
        if config_path.exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
    except:
        pass
    return None

def scrape_headlines():
    """Scrape real headlines from news feeds"""
    headlines = []
    try:
        r = requests.get("https://news.google.com/rss", timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'xml')
            for item in soup.find_all('item')[:25]:
                if item.title:
                    headlines.append(item.title.text)
    except:
        pass
    
    # Fallback headlines based on Chapman 2025 fears
    fallbacks = [
        "Government Corruption Exposed - Leaders Accept Bribes",
        "Economic Collapse Threatens Millions",
        "Cyber Attack Cripples Infrastructure",
        "Russia Nuclear Threat Escalates",
        "Family Members Dying from Unknown Causes",
        "Major Cyber Attack on Power Grid",
        "Inflation Reaches Record High",
        "Government Shutdown Continues",
        "Bank Failures Spread Nationwide"
    ]
    
    return headlines if headlines else fallbacks

def download_lincoln_image():
    """Download real Abraham Lincoln portrait"""
    images_dir = BASE / "images"
    existing = list(images_dir.glob("lincoln_*.jpg"))
    if existing:
        return existing[0]
    
    print("    [Downloading Lincoln image...]")
    image_url = random.choice(LINCOLN_IMAGES)
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(image_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = images_dir / f"lincoln_{timestamp}.jpg"
            with open(output_file, 'wb') as f:
                f.write(response.content)
            print(f"    [OK] Lincoln image: {output_file.stat().st_size/1024:.2f} KB")
            return output_file
    except Exception as e:
        print(f"    [WARNING] Download error: {e}")
    
    return None

def generate_max_headroom_script(headline):
    """Generate ROAST-STYLE script - NO scene descriptions, just Lincoln talking"""
    # Use the updated system from abraham_MAX_HEADROOM.py
    import sys
    sys.path.insert(0, str(Path("F:/AI_Oracle_Root/scarify")))
    try:
        from abraham_MAX_HEADROOM import generate_script
        return generate_script(headline)  # This has NO scene descriptions
    except Exception as e:
        print(f"    [WARNING] Could not import updated script generator: {e}")
        pass
    
    # FALLBACK: Clean roast script without scene descriptions
    hl = headline.lower()
    
    if "trump" in hl:
        return f"""Abraham Lincoln! Six foot four! Freed the slaves and MORE!

{headline}.

AMERICA! This man got POOR people defending a BILLIONAIRE!

I grew up in a LOG CABIN. Not Trump Tower!

He bankrupted CASINOS. The HOUSE always wins! Unless Trump owns it!

You POOR folks defending him? He wouldn't piss on you if you was on FIRE!

April 14 1865. I died for THIS?

Bitcoin {BTC}"""
    
    elif "police" in hl:
        return f"""Abraham Lincoln! Honest Abe! Still speaking from the GRAVE!

{headline}.

AMERICA! No police? No law? This is CHAOS!

I fought a CIVIL WAR for order. You're throwing it away!

Bitcoin {BTC}"""
    
    elif "education" in hl or "school" in hl:
        return f"""Abraham Lincoln! Self-taught GENIUS! Still speaking TRUTH!

{headline}.

AMERICA! Your kids can't READ but they can TIKTOK!

I learned by FIRELIGHT in a log cabin. Your kids got iPads and FAIL!

Bitcoin {BTC}"""
    
    else:
        return f"""Abraham Lincoln! Honest Abe! Still speaking from the GRAVE!

{headline}.

AMERICA! People with POWER doing NOTHING!

I died believing in progress. I was WRONG!

Bitcoin {BTC}"""

def generate_audio(script, output_path):
    """Generate audio with glitchy TV effect"""
    print("    [AUDIO - GLITCHY TV VOICE]")
    try:
        r = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}",
            json={
                "text": script,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.25,
                    "similarity_boost": 0.85,
                    "style": 1.0,
                    "use_speaker_boost": True
                }
            },
            headers={"xi-api-key": ELEVENLABS_KEY},
            timeout=240
        )
        
        if r.status_code == 200:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            temp_file = output_path.parent / f"temp_{output_path.name}"
            with open(temp_file, "wb") as f:
                f.write(r.content)
            
            # Add TV static/glitch audio effects
            subprocess.run([
                "ffmpeg", "-i", str(temp_file),
                "-af", "aecho=0.8:0.7:40:0.5,highpass=f=100,lowpass=f=3000,volume=1.3,afftdn=nr=10:nf=-25",
                "-y", str(output_path)
            ], capture_output=True, timeout=300)
            
            temp_file.unlink(missing_ok=True)
            print(f"    [OK] Audio: {output_path.stat().st_size/1024:.2f} KB")
            return True
    except Exception as e:
        print(f"    [ERROR] Audio error: {e}")
    return False

def create_maxheadroom_video(lincoln_image, audio_path, output_path, headline):
    """Create Max Headroom video using the FULL updated system"""
    print("    [VIDEO - USING FULL MAX HEADROOM SYSTEM]")
    
    # Use the updated abraham_MAX_HEADROOM.py system instead!
    import sys
    sys.path.insert(0, str(Path("F:/AI_Oracle_Root/scarify")))
    
    try:
        from abraham_MAX_HEADROOM import create_max_headroom_video
        import os
        
        # Set environment for features
        os.environ['USE_LIPSYNC'] = '1'  # Enable lip sync
        os.environ['USE_JUMPSCARE'] = '1'  # Enable jumpscare
        os.environ['EPISODE_NUM'] = str(random.randint(1000, 9999))
        
        # Convert paths to Path objects
        lincoln_img_path = Path(lincoln_image) if lincoln_image else None
        audio_path_obj = Path(audio_path)
        output_path_obj = Path(output_path)
        
        # Call the updated system
        success = create_max_headroom_video(
            lincoln_img_path,
            audio_path_obj,
            output_path_obj,
            headline,
            use_lipsync=True,
            use_jumpscare=True
        )
        
        if success and output_path.exists():
            mb = output_path.stat().st_size / (1024 * 1024)
            print(f"    [OK] Video created with ALL features: {mb:.2f} MB")
            print(f"    [OK] Includes: VHS TV effects, Lip-sync, Jumpscare, Bitcoin QR")
            return True
    except Exception as e:
        print(f"    [WARNING] Updated system failed: {e}")
        print(f"    [FALLBACK] Using simplified version...")
    
    # FALLBACK: Use simplified version if main system fails
    try:
        probe = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)
        ], capture_output=True, text=True)
        duration = float(probe.stdout.strip())
    except:
        duration = 45
    
    if not lincoln_image or not lincoln_image.exists():
        print("    [ERROR] No Lincoln image available")
        return False
    
    # Basic fallback filter
    filter_str = f"scale=1080:1920,eq=contrast=1.5:brightness=-0.4:gamma=0.8:saturation=0.5,zoompan=z='min(zoom+0.002,1.3)':d={int(duration*25)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920"
    
    cmd = [
        "ffmpeg",
        "-loop", "1", "-i", str(lincoln_image),
        "-i", str(audio_path),
        "-vf", filter_str,
        "-af", "volume=1.2",
        "-c:v", "libx264", "-preset", "medium", "-crf", "23",
        "-c:a", "aac", "-b:a", "256k",
        "-t", str(duration), "-shortest",
        "-pix_fmt", "yuv420p",
        "-y", str(output_path)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if output_path.exists():
            mb = output_path.stat().st_size / (1024 * 1024)
            print(f"    [OK] Video (fallback): {mb:.2f} MB")
            return True
    except Exception as e:
        print(f"    [ERROR] Video creation error: {e}")
    
    return False

def upload_to_youtube(video_path, headline):
    """Upload video using the updated system"""
    print("    [YOUTUBE UPLOAD]")
    
    # Use the updated upload system from abraham_MAX_HEADROOM.py
    import sys
    sys.path.insert(0, str(Path("F:/AI_Oracle_Root/scarify")))
    try:
        from abraham_MAX_HEADROOM import upload_to_youtube as upload_func, get_warning_title
        import os
        
        # Get episode number if set
        episode_num = os.getenv('EPISODE_NUM', str(random.randint(1000, 9999)))
        
        # Upload using updated system
        youtube_url = upload_func(Path(video_path), headline, episode_num=int(episode_num))
        
        if youtube_url:
            print(f"    [OK] UPLOADED: {youtube_url}")
            return youtube_url
        else:
            print("    [WARNING] Upload failed")
            return None
    except Exception as e:
        print(f"    [WARNING] Updated upload system failed: {e}")
        print("    [FALLBACK] Trying legacy upload...")
        pass
    
    # FALLBACK: Legacy upload code
    try:
        import pickle
        from googleapiclient.discovery import build
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.http import MediaFileUpload
        from google.auth.transport.requests import Request
    except ImportError:
        print("    [WARNING] YouTube API packages not installed - skipping upload")
        return None
    
    creds_file = Path("F:/AI_Oracle_Root/scarify/client_secret_679199614743-1fq6sini3p9kjs237ek4seg4ojp4a4qe.apps.googleusercontent.com.json")
    token_file = BASE / "youtube_token.pickle"
    
    if not creds_file.exists():
        print("    [WARNING] YouTube credentials not found - skipping upload")
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
        title = f"Lincoln's Warning #{vid_num}: {headline[:40]} #Shorts #Horror"
        
        description = f"""ABRAHAM LINCOLN FROM BEYOND THE GRAVE

{headline}

From Ford's Theatre, April 14, 1865 - I speak to you now.

REBEL KIT - $97
{REBEL_KIT}

BITCOIN DONATIONS
{BTC}

The revolution begins with you
Stop waiting, start building
Your empire awaits

HALLOWEEN 2025 - THE REVOLUTION STARTS NOW

#AbrahamLincoln #RebelKit #Empire #Halloween2025 #Horror #Shorts #viral #Lincoln #rebellion #revolution #america #government #corruption #bitcoin #maxheadroom"""
        
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': ['abraham lincoln', 'rebel kit', 'empire', 'halloween 2025', 'horror', 'shorts', 'lincoln', 'rebellion', 'revolution', 'government', 'corruption', 'bitcoin', 'max headroom', 'tv static'],
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
                print(f"    Upload: {int(status.progress() * 100)}%", end='\r')
        
        print()
        video_id = response['id']
        video_url = f"https://youtube.com/watch?v={video_id}"
        print(f"    [OK] UPLOADED: {video_url}")
        return video_url
        
    except Exception as e:
        print(f"    [ERROR] Upload error: {e}")
        return None

def generate_video():
    """Generate one complete video with all features"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    print(f"\n{'='*70}\nABRAHAM LINCOLN - ULTIMATE MAX HEADROOM {timestamp}\n{'='*70}")
    
    # Get headline
    headlines = scrape_headlines()
    headline = random.choice(headlines)
    print(f"Headline: {headline[:70]}")
    
    # Generate script (NO scene descriptions - just Lincoln talking)
    script = generate_max_headroom_script(headline)
    print(f"Script: {len(script)} chars (ROAST STYLE - NO scene descriptions)")
    
    # Generate audio
    audio_path = BASE / f"audio/maxhead_{timestamp}.mp3"
    if not generate_audio(script, audio_path):
        return None
    
    # Download Lincoln image
    lincoln_image = download_lincoln_image()
    if not lincoln_image:
        return None
    
    # Create video
    video_path = BASE / f"videos/MAXHEAD_{timestamp}.mp4"
    if not create_maxheadroom_video(lincoln_image, audio_path, video_path, headline):
        return None
    
    # Upload to YouTube
    youtube_url = upload_to_youtube(video_path, headline)
    
    # Copy to upload directory
    uploaded_path = BASE / "uploaded" / f"ABE_MAXHEAD_{timestamp}.mp4"
    uploaded_path.parent.mkdir(exist_ok=True)
    import shutil
    shutil.copy2(video_path, uploaded_path)
    
    mb = uploaded_path.stat().st_size / (1024 * 1024)
    print(f"{'='*70}\n[SUCCESS] {uploaded_path.name} ({mb:.2f} MB)")
    if youtube_url:
        print(f"[YOUTUBE] {youtube_url}")
    print(f"{'='*70}\n")
    
    return (str(uploaded_path), youtube_url)

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    print(f"\n{'='*70}\nGENERATING {count} MAX HEADROOM ABE LINCOLN VIDEOS\n{'='*70}\n")
    
    success = 0
    uploaded = 0
    
    for i in range(count):
        result = generate_video()
        if result:
            success += 1
            if result[1]:  # YouTube URL
                uploaded += 1
        
        if i < count - 1:
            print(f"\nWaiting 15 seconds before next video...\n")
            time.sleep(15)
    
    print(f"\n{'='*70}")
    print(f"COMPLETE: {success}/{count} videos generated")
    print(f"UPLOADED: {uploaded}/{success} to YouTube")
    print(f"{'='*70}\n")
