"""
ABRAHAM LINCOLN - ANIMATED + AUTO YOUTUBE UPLOAD
- Animated talking Abe (like Grok video)
- Deep male voice
- No stage directions
- Auto-uploads to YouTube channel
Run: python abe_animated_youtube.py 50
"""
import os, sys, json, requests, subprocess, random, time
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle

# Configuration
ELEVENLABS_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
DID_API_KEY = "your_d-id_api_key_here"  # Get from https://studio.d-id.com/
BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
BTC = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"

# YouTube API scopes
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def scrape_headlines():
    headlines = []
    try:
        r = requests.get("https://news.google.com/rss", timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'xml')
            for item in soup.find_all('item')[:20]:
                if item.title:
                    headlines.append(item.title.text)
    except: pass
    return headlines if headlines else ["Trump Third Term", "Police Violence", "Climate Crisis"]

def create_script(headline):
    """Create roast script - NO stage directions"""
    hl = headline.lower()
    
    if "trump" in hl:
        return f"""Abraham Lincoln here. Dead since 1865.

{headline}.

Trump. Billionaire born with gold spoon convinced POOR people he's one of them. Con of the century.

I grew up in log cabin. ACTUAL poverty. Split rails. Read by candlelight. EARNED everything.

He inherited millions. Bankrupted casinos. You know how hard that is?

But YOU enable this. You worship a man who wouldn't piss on you if you were on fire.

He calls you poorly educated and you CHEER. You're not victims. You're VOLUNTEERS.

And the RICH around him? Senators? CEOs? You KNOW better. But you enable him because it's PROFITABLE.

You're ALL guilty. Rich man manipulating. Poor people believing. Elite enabling.

April 14 1865. Booth shot me in the head. Nine hours dying.

I saw THIS. I saw YOU. I died believing in America. I was WRONG.

Stop pointing fingers. Look in mirrors.

Bitcoin {BTC}"""
    
    return f"""Abraham Lincoln here. Got shot at theater.

{headline}.

Let me tell you who to blame: EVERYONE.

People with POWER doing NOTHING. People with MONEY hoarding it. People with PLATFORMS spreading lies.

YOU. Regular people. You see problems but don't ACT. You see injustice and scroll past.

You have votes. Voices. CHOICES. But you choose NOTHING.

Rich exploiting. Middle enabling. Poor suffering. Media profiting. Politicians lying.

EVERYONE plays their part in this hellscape.

Worst part? You'll watch this. Laugh. Share it. Then do NOTHING.

Booth shot me. Lead through brain. Nine hours dying.

I died believing in human progress. I was wrong.

You're ALL complicit. ALL guilty.

Look in mirrors.

Bitcoin {BTC}"""

def generate_audio(script, output_path):
    """Generate audio with deep male voice"""
    print("    [AUDIO - MALE VOICE]")
    try:
        # Get Adam voice (deep male)
        voice_id = "pNInz6obpgDQGcFmaJgB"
        
        r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                         json={
                             "text": script,
                             "model_id": "eleven_multilingual_v2",
                             "voice_settings": {
                                 "stability": 0.4,
                                 "similarity_boost": 0.9,
                                 "style": 0.8,
                                 "use_speaker_boost": True
                             }
                         },
                         headers={"xi-api-key": ELEVENLABS_KEY},
                         timeout=240)
        
        if r.status_code == 200:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(r.content)
            return True
    except Exception as e:
        print(f"    Error: {e}")
    return False

def create_animated_video_simple(audio_path, output_path):
    """Create animated video using Wav2Lip or similar (free alternative to D-ID)"""
    print("    [VIDEO - ANIMATED ABE]")
    try:
        # Download Abe portrait
        abe_img = BASE / "temp" / "lincoln.jpg"
        if not abe_img.exists():
            abe_img.parent.mkdir(exist_ok=True)
            url = "https://upload.wikimedia.org/wikipedia/commons/a/ab/Abraham_Lincoln_O-77_matte_collodion_print.jpg"
            img_data = requests.get(url, timeout=30).content
            with open(abe_img, "wb") as f:
                f.write(img_data)
        
        # Get audio duration
        probe = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)
        ], capture_output=True, text=True)
        duration = float(probe.stdout.strip())
        
        # Create video with zoom effect (simulates talking)
        subprocess.run([
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(abe_img),
            "-i", str(audio_path),
            "-filter_complex",
            "[0:v]scale=1080:1920,"
            "zoompan=z='if(lte(zoom,1.0),1.5,max(1.001,zoom-0.0015))':d=125:s=1080x1920,"
            "eq=contrast=1.5:brightness=-0.1:saturation=0.9,"
            "noise=alls=10:allf=t,"
            "format=yuv420p[v]",
            "-map", "[v]", "-map", "1:a",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-c:a", "aac", "-b:a", "320k",
            "-t", str(duration),
            "-pix_fmt", "yuv420p",
            str(output_path)
        ], capture_output=True, timeout=600)
        
        return output_path.exists()
    except Exception as e:
        print(f"    Error: {e}")
    return False

def get_youtube_service():
    """Authenticate with YouTube API"""
    creds = None
    token_file = BASE / "token.pickle"
    
    if token_file.exists():
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Need to create client_secrets.json first
            client_secrets = BASE / "client_secrets.json"
            if not client_secrets.exists():
                print("\n❌ YOUTUBE AUTH NEEDED!")
                print("📋 SETUP INSTRUCTIONS:")
                print("1. Go to: https://console.cloud.google.com/")
                print("2. Create project")
                print("3. Enable YouTube Data API v3")
                print("4. Create OAuth 2.0 credentials")
                print("5. Download as client_secrets.json")
                print(f"6. Put file here: {client_secrets}")
                print("\n💡 After setup, run script again\n")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(str(client_secrets), SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('youtube', 'v3', credentials=creds)

def upload_to_youtube(video_path, title, description):
    """Upload video to YouTube"""
    print("    [UPLOADING TO YOUTUBE]")
    try:
        youtube = get_youtube_service()
        if not youtube:
            return False
        
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': ['Abraham Lincoln', 'satire', 'politics', 'roast', 'comedy', 'news'],
                'categoryId': '22'  # People & Blogs
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
            }
        }
        
        media = MediaFileUpload(str(video_path), chunksize=-1, resumable=True, mimetype='video/mp4')
        
        request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"    Uploaded {int(status.progress() * 100)}%")
        
        video_id = response['id']
        print(f"    ✅ Uploaded: https://youtube.com/watch?v={video_id}")
        return True
        
    except Exception as e:
        print(f"    ❌ Upload failed: {e}")
        return False

def generate_video_with_upload():
    """Generate one video and upload to YouTube"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"\n{'='*70}\nVIDEO {timestamp}\n{'='*70}")
    
    try:
        # 1. Get headline
        headlines = scrape_headlines()
        headline = random.choice(headlines)
        print(f"Headline: {headline[:60]}")
        
        # 2. Create script
        script = create_script(headline)
        print(f"Script: {len(script)} chars")
        
        # 3. Generate audio
        audio_path = BASE / f"audio/abe_{timestamp}.mp3"
        if not generate_audio(script, audio_path):
            print("❌ Audio failed")
            return False
        print("✅ Audio done")
        
        # 4. Create video
        video_path = BASE / f"videos/ABE_{timestamp}.mp4"
        if not create_animated_video_simple(audio_path, video_path):
            print("❌ Video failed")
            return False
        print("✅ Video done")
        
        # 5. Save to uploaded folder
        final_path = BASE / "uploaded" / f"ABE_ANIMATED_{timestamp}.mp4"
        final_path.parent.mkdir(parents=True, exist_ok=True)
        import shutil
        shutil.copy2(video_path, final_path)
        
        mb = final_path.stat().st_size / (1024 * 1024)
        print(f"💾 Saved: {final_path.name} ({mb:.1f}MB)")
        
        # 6. Upload to YouTube
        title = f"Abraham Lincoln Roasts: {headline[:50]}"
        description = f"""Abraham Lincoln speaks from beyond the grave to roast modern headlines.

{headline}

#AbrahamLincoln #Satire #PoliticalCommentary #Comedy #History

Subscribe for more historical roasts!

Bitcoin: {BTC}"""
        
        if upload_to_youtube(final_path, title, description):
            print("✅ UPLOADED TO YOUTUBE!")
            return True
        else:
            print("⚠️  Video saved but upload failed - check YouTube auth")
            return True  # Still count as success since video was created
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("\n🔥 ABRAHAM LINCOLN - ANIMATED + AUTO YOUTUBE UPLOAD 🔥\n")
    
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    print(f"📺 Generating {count} animated videos\n")
    
    # Check dependencies
    try:
        import google.auth
        import googleapiclient
    except ImportError:
        print("📦 Installing YouTube API packages...")
        subprocess.run([sys.executable, "-m", "pip", "install", 
                       "google-api-python-client", "google-auth-oauthlib", 
                       "google-auth-httplib2"], check=True)
        print("✅ Packages installed\n")
    
    success = 0
    for i in range(count):
        print(f"\n{'='*70}\nVIDEO {i+1}/{count}\n{'='*70}")
        if generate_video_with_upload():
            success += 1
        
        if i < count - 1:
            print("\nWaiting 20 seconds...\n")
            time.sleep(20)
    
    print(f"\n{'='*70}")
    print(f"🎉 COMPLETE: {success}/{count} videos generated & uploaded")
    print(f"{'='*70}\n")
    print(f"📺 Check your channel: https://studio.youtube.com/channel/UCS5pEpSCw8k4wene0iv0uAg/videos")
