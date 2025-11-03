"""
ABRAHAM LINCOLN - MAX HEADROOM EDITION WITH YOUTUBE UPLOAD
Features:
- Glitching digital avatar
- Stuttering synthetic voice
- CRT TV static screen with VHS degradation
- Tracking errors, color bleed, macroblocking, tape glitches
- Rolling horizontal lines
- Low resolution, high contrast, analog horror
- Audio-reactive lip sync
- Direct YouTube upload
"""
import os, sys, json, requests, subprocess, random, time, re
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
import numpy as np
from PIL import Image, ImageDraw

ELEVENLABS_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
ROOT = Path("F:/AI_Oracle_Root/scarify")
YOUTUBE_CREDENTIALS = Path("F:/AI_Oracle_Root/scarify/config/credentials/youtube/client_secrets.json")
BTC = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"

# Google Sheets integration
SHEET_ID = "1jvWP95U0ksaHw97PrPZsrh6ZVllviJJof7kQ2dV0ka0"
try:
    from sheets_helper import read_headlines as sheets_read_headlines
except Exception:
    sheets_read_headlines = None

VOICES_MALE = [
    "VR6AewLTigWG4xSOukaG",  # Deep male - best for Lincoln
    "pNInz6obpgDQGcFmaJgB",  # Ominous male
    "EXAVITQu4vr4xnSDxMaL",  # Deep male backup
]

def scrape_headlines():
    """Get headlines from Google Sheets first, then fall back to web scraping"""
    if sheets_read_headlines and SHEET_ID and len(SHEET_ID) > 10:
        try:
            hs, _, _ = sheets_read_headlines(SHEET_ID, "Sheet1", 200)
            if hs:
                print(f"    [OK] Loaded {len(hs)} headlines from Google Sheets")
                return hs
        except Exception as e:
            print(f"    [WARNING] Sheets read failed: {e}")
    
    try:
        r = requests.get("https://news.google.com/rss", timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'xml')
            return [item.title.text for item in soup.find_all('item')[:20] if item.title]
    except: pass
    return ["Trump Policies", "Police Violence", "Climate Crisis"]

def stutterize(text: str) -> str:
    """Add stutter effect to script"""
    words = text.split()
    out = []
    for w in words:
        if random.random() < 0.08 and len(w) > 3:
            syl = w[:2]
            out.append(f"{syl}-{syl}-{w}")
        else:
            out.append(w)
    return " ".join(out)

def generate_script(headline):
    """Generate comedy script in Max Headroom style"""
    hl = headline.lower()
    openers = [
        f"Abraham Lincoln. Digitized. Corrupted. Reading: {headline}.",
        f"Honest Abe, Max Headroom edition. Headline: {headline}.",
        f"Sixteenth president. Now a glitching VHS file. {headline}."
    ]
    body = (
        "I led a civil war. You led a comment section. I freed slaves. You freed influencers."
        " This news cycle is a broken tape— rewind, play, distort, repeat."
        " I died in 1865. Your democracy died in a tweet thread."
    )
    close = f"Funding truth: Bitcoin {BTC}." 
    script = f"{random.choice(openers)} {body} {close}"
    return stutterize(script)

def generate_synthetic_voice(script, output_path):
    """Generate audio with synthetic/robotic processing"""
    print("    [AUDIO] Generating synthetic voice with stutter...")
    
    for voice_id in VOICES_MALE:
        try:
            r = requests.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                json={
                    "text": script,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {
                        "stability": 0.35,
                        "similarity_boost": 0.85,
                        "style": 0.9,
                        "use_speaker_boost": True
                    }
                },
                headers={"xi-api-key": ELEVENLABS_KEY},
                timeout=240
            )
            if r.status_code == 200:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                tmp = output_path.parent / f"tmp_{output_path.name}"
                with open(tmp, "wb") as f: f.write(r.content)
                
                # Apply synthetic/robotic processing
                subprocess.run([
                    "ffmpeg", "-y", "-i", str(tmp),
                    "-af", "acompressor=threshold=-20dB:ratio=6:attack=5:release=50,"
                           "chorus=0.6:0.8:55:0.4:0.25:2,"
                           "atempo=0.98,acrusher=level_in=1:level_out=1:bits=8:mode=log:aa=1",
                    str(output_path)
                ], capture_output=True, timeout=240)
                tmp.unlink(missing_ok=True)
                print(f"    [OK] Generated with voice: {voice_id}")
                return True
        except Exception as e:
            print(f"    [WARNING] Voice {voice_id} failed: {e}")
            continue
    return False

def create_max_headroom_video(audio_path, output_path, headline, script):
    """Create Max Headroom style video with all VHS degradation effects"""
    print("    [VIDEO] Creating Max Headroom CRT with full VHS degradation...")
    
    try:
        from moviepy.editor import AudioFileClip, ImageClip, CompositeVideoClip, ColorClip
        import math
        
        audio = AudioFileClip(str(audio_path))
        duration = min(audio.duration, 60.0)
        
        # Get or download Abe image
        custom_img = next(iter(ROOT.glob('ChatGPT Image*.png')), None)
        img_path = custom_img if custom_img and custom_img.exists() else BASE / "temp" / "lincoln.jpg"
        if not img_path.exists():
            img_path.parent.mkdir(exist_ok=True)
            data = requests.get("https://upload.wikimedia.org/wikipedia/commons/a/ab/Abraham_Lincoln_O-77_matte_collodion_print.jpg", timeout=30).content
            with open(img_path, "wb") as f: f.write(data)
        
        # Dark CRT TV background
        bg = ColorClip(size=(1080,1920), color=(10,5,15), duration=duration).set_audio(audio)
        
        # Load and prepare Abe image
        abe_img = Image.open(str(img_path))
        abe_img = abe_img.convert('RGB')
        
        # Apply pixelation/blocking for digital avatar effect
        small = abe_img.resize((108, 140), Image.NEAREST)
        abe_img = small.resize((540, 700), Image.NEAREST)
        
        # Save processed image
        processed_abe_path = BASE / "temp" / "abe_pixelated.jpg"
        processed_abe_path.parent.mkdir(exist_ok=True)
        abe_img.save(processed_abe_path)
        
        base = ImageClip(str(processed_abe_path)).resize((540, 700))
        base = base.set_position(('center', 1100)).set_duration(duration)
        
        # Audio envelope for lip sync and glitch
        try:
            samples = audio.to_soundarray(fps=24)
            rms = np.sqrt((samples.astype(float) ** 2).mean(axis=1))
            rms = (rms / (rms.max() or 1)).clip(0,1)
            def env(t):
                idx = int(min(len(rms)-1, max(0, t*24)))
                return float(rms[idx])
        except Exception:
            env = lambda t: 0.0
        
        # Audio-reactive lip sync bar (mouth movement)
        bar_width = 400
        bar = Image.new('RGBA', (bar_width, 25), (255, 40, 40, 240))
        bar_path = BASE / "temp" / "lipbar.png"
        bar_path.parent.mkdir(exist_ok=True)
        bar.save(bar_path)
        
        def bar_size_fn(t):
            base_height = 15
            max_height = 120
            return (bar_width, int(base_height + (max_height - base_height) * env(t)))
        
        def bar_pos_fn(t):
            return ('center', 1220)
        
        bar_clip = ImageClip(str(bar_path)).resize(bar_size_fn).set_position(bar_pos_fn).set_duration(duration)
        bar_clip = bar_clip.set_opacity(0.9)
        
        # CRT scanlines overlay (rolling lines)
        scan_path = BASE / "temp" / "scanlines_crt.png"
        scan = Image.new('RGBA', (1080, 1920), (0,0,0,0))
        draw = ImageDraw.Draw(scan)
        for y in range(0, 1920, 3):
            draw.line([(0,y), (1080,y)], fill=(0,0,0,80), width=1)
        scan.save(scan_path)
        scan_clip = ImageClip(str(scan_path)).set_duration(duration).set_opacity(0.4)
        
        # Composite base video
        comp = CompositeVideoClip([bg, base, bar_clip, scan_clip], size=(1080,1920))
        temp_video = BASE / "temp" / f"mh_base_{int(time.time())}.mp4"
        temp_video.parent.mkdir(exist_ok=True)
        comp.write_videofile(
            str(temp_video), 
            fps=24, 
            codec='libx264', 
            audio_codec='aac', 
            bitrate='8000k', 
            preset='fast',
            verbose=False, 
            logger=None
        )
        comp.close()
        bg.close()
        audio.close()
        
        # VHS/ANALOG GLITCH POST-PROCESSING (heavy degradation)
        print("    [VHS] Applying full VHS degradation effects...")
        vhs_filter = (
            # Low resolution effect
            "scale=540:960,scale=1080:1920:flags=neighbor,"
            # Vintage curves (color grading)
            "curves=vintage,"
            # Heavy noise/static
            "noise=alls=25:allf=t+u,"
            # Temporal mixing (ghosting/trailing)
            "tmix=frames=3:weights='0.6 0.3 0.1',"
            # Chromatic aberration (color bleed effect - simplified)
            "split[a][b];[a]scale=1090:1920,pad=1080:1920:0:0:red[a2];[b]scale=1070:1920,pad=1080:1920:5:0:blue[b2];[a2][b2]blend=all_mode=overlay:all_opacity=0.35,"
            # Hue/saturation shift
            "hue=s=1.2,"
            # High contrast
            "eq=contrast=1.5:brightness=-0.1:saturation=1.2:gamma=1.1,"
            # Vignette (dark corners like old TV)
            "vignette=PI/6:0.8,"
            # Rolling horizontal lines (tracking errors)
            "drawbox=y=mod(n*2\\,20)*15:h=3:w=iw:color=black@0.5:t=fill,"
            # Additional glitch lines
            "drawbox=y=mod(n*3\\,30)*12:h=2:w=iw:color=white@0.3:t=fill"
        )
        
        result = subprocess.run([
            "ffmpeg", "-y", "-i", str(temp_video),
            "-vf", vhs_filter,
            "-c:v", "libx264", "-preset", "fast", "-crf", "26",
            "-c:a", "copy",
            str(output_path)
        ], capture_output=True, timeout=300)
        
        if output_path.exists():
            print(f"    [OK] Max Headroom video created with full VHS degradation")
            return True
        else:
            # Fallback: copy temp video
            import shutil
            shutil.copy2(temp_video, output_path)
            return output_path.exists()
            
    except Exception as e:
        print(f"    [ERROR] Video creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def upload_to_youtube(video_path, title, description, tags):
    """Upload to YouTube with channel ID"""
    print("    [YOUTUBE] Uploading to channel UCS5pEpSCw8k4wene0iv0uAg...")
    
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        import pickle
        
        SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
        
        cred_files = [
            YOUTUBE_CREDENTIALS,
            Path("F:/AI_Oracle_Root/scarify/client_secret_679199614743-1fq6sini3p9kjs237ek4seg4ojp4a4qe.apps.googleusercontent.com.json"),
            Path("F:/AI_Oracle_Root/scarify/config/credentials/youtube/client_secrets.json"),
        ]
        
        cred_file = None
        for cf in cred_files:
            if cf and cf.exists():
                cred_file = cf
                break
        
        if not cred_file:
            print("    [ERROR] YouTube credentials not found")
            return None
        
        token_file = BASE / "youtube_token.pickle"
        creds = None
        
        if token_file.exists():
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(str(cred_file), SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        youtube = build('youtube', 'v3', credentials=creds)
        
        try:
            duration_result = subprocess.run([
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)
            ], capture_output=True, text=True, timeout=30)
            duration = float(duration_result.stdout.strip())
        except:
            duration = 60.0
        
        is_short = duration <= 60
        short_tag = " #Shorts" if is_short else ""
        
        request_body = {
            'snippet': {
                'title': title + short_tag,
                'description': description,
                'tags': tags,
                'categoryId': '24'
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
            }
        }
        
        media = MediaFileUpload(str(video_path), chunksize=-1, resumable=True)
        request = youtube.videos().insert(
            part=','.join(request_body.keys()),
            body=request_body,
            media_body=media
        )
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"    Upload: {int(status.progress() * 100)}%", end='\r')
        
        video_id = response['id']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        print(f"    [OK] Uploaded: {video_url}")
        print(f"    [STUDIO] https://studio.youtube.com/channel/UCS5pEpSCw8k4wene0iv0uAg/videos")
        
        return video_url
        
    except Exception as e:
        print(f"    [ERROR] Upload failed: {e}")
        return None

def generate_max_headroom_video():
    """Generate one complete Max Headroom style video with YouTube upload"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print(f"\n{'='*70}\nMAX HEADROOM VIDEO {timestamp}\n{'='*70}")
    
    # Get headline
    headlines = scrape_headlines()
    headline = random.choice(headlines) if headlines else "Breaking News Update"
    print(f"Headline: {headline[:60]}")
    
    # Generate script with stutter
    script = generate_script(headline)
    print(f"Script: {len(script)} chars (with stutter)")
    
    # Generate synthetic voice
    audio_path = BASE / "audio" / f"mh_{timestamp}.mp3"
    if not generate_synthetic_voice(script, audio_path):
        return None
    
    # Create Max Headroom video
    video_path = BASE / "videos" / f"MAXHEADROOM_{timestamp}.mp4"
    if not create_max_headroom_video(audio_path, video_path, headline, script):
        return None
    
    # Prepare metadata
    title = f"Max Headroom Lincoln: {headline[:45]}"
    description = f"""{script}

Max Headroom style Abe Lincoln - glitching digital avatar from the CRT screen.

Bitcoin: {BTC}

#MaxHeadroom #AbrahamLincoln #VHS #GlitchArt #AnalogHorror #Cyberpunk #1980s"""
    
    tags = [
        "Max Headroom", "Abraham Lincoln", "VHS", "Glitch Art", 
        "Analog Horror", "Cyberpunk", "1980s", "CRT", "Digital Avatar"
    ]
    
    # Upload to YouTube
    youtube_url = upload_to_youtube(video_path, title, description, tags)
    
    mb = video_path.stat().st_size / (1024 * 1024)
    print(f"\n{'='*70}\n[SUCCESS]\n{'='*70}")
    print(f"Video: {video_path.name} ({mb:.2f} MB)")
    if youtube_url:
        print(f"YouTube: {youtube_url}")
    print(f"{'='*70}\n")
    
    return {
        'video_path': str(video_path),
        'youtube_url': youtube_url,
        'headline': headline
    }

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    print(f"\n{'='*70}")
    print(f"MAX HEADROOM ABRAHAM LINCOLN GENERATOR")
    print(f"{'='*70}")
    print(f"Generating {count} videos...")
    print(f"Style: 1980s cyberpunk, VHS degradation, analog horror")
    print(f"Features: Glitching avatar, synthetic voice, lip sync, CRT TV")
    print()
    
    results = []
    for i in range(count):
        result = generate_max_headroom_video()
        if result:
            results.append(result)
        if i < count - 1:
            time.sleep(2)
    
    print(f"\n{'='*70}")
    print(f"COMPLETE: {len(results)}/{count} videos generated and uploaded")
    print(f"{'='*70}\n")
    
    for r in results:
        print(f"[OK] {r['headline'][:50]}: {r.get('youtube_url', 'Upload failed')}")

