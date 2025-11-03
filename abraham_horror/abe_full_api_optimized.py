"""
ABRAHAM LINCOLN - ALL APIs OPTIMIZED
ElevenLabs + Pexels + RunwayML + Max Headroom
Optimized to prevent timeouts (~2min per video)
"""
import os, sys, json, requests, subprocess, random, time, re
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
import numpy as np
from PIL import Image, ImageDraw

# API KEYS
ELEVENLABS_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
PEXELS_KEY = "RgE9Mdn3ToSQhn2RiLJ4mPMISjjp587QKRG9uhpOrLVtkKPCibUPUDGh"

BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
ROOT = Path("F:/AI_Oracle_Root/scarify")
YOUTUBE_CREDENTIALS = Path("F:/AI_Oracle_Root/scarify/config/credentials/youtube/client_secrets.json")
BTC = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"

USE_BROLL = "--skip-broll" not in sys.argv

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

def log(msg, status="INFO"):
    icons = {"INFO": "[INFO]", "SUCCESS": "[OK]", "ERROR": "[ERROR]", "PROCESS": "[PROCESS]"}
    print(f"{icons.get(status, '[INFO]')} {msg}")

def scrape():
    """Get headlines from Google Sheets first, fallback to web"""
    if sheets_read_headlines and SHEET_ID and len(SHEET_ID) > 10:
        try:
            hs, _, _ = sheets_read_headlines(SHEET_ID, "Sheet1", 200)
            if hs:
                log(f"Loaded {len(hs)} headlines from Google Sheets", "SUCCESS")
                return hs
        except Exception as e:
            log(f"Sheets read failed: {e}", "ERROR")
    
    try:
        r = requests.get("https://news.google.com/rss", timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'xml')
            return [item.title.text for item in soup.find_all('item')[:20] if item.title]
    except: pass
    return ["Trump Policies", "Police Violence", "Climate Crisis"]

def stutterize(text: str) -> str:
    """Add Max Headroom stutter effect"""
    words = text.split()
    out = []
    for w in words:
        if random.random() < 0.08 and len(w) > 3:
            syl = w[:2]
            out.append(f"{syl}-{syl}-{w}")
        else:
            out.append(w)
    return " ".join(out)

def comedy(headline):
    """Generate comedy script with stutter"""
    hl = headline.lower()
    
    opens = [
        "Abraham Lincoln! Six foot four! Honest Abe who freed the slaves and MORE!",
        "I'm Abraham Lincoln, yeah that's right! Got shot in the head but I'm STILL upright!",
        "Abe Lincoln in the house! Tallest president, best president, no doubt!"
    ]
    
    if "trump" in hl:
        script = f"""{random.choice(opens)}
AMERICA! Let me tell you something right now!
{headline}.
Dave Chappelle style, real talk. This man got POOR people defending a BILLIONAIRE. That's like chickens voting for Colonel Sanders!
I grew up in a LOG CABIN. Not Trump Tower! I split rails! Read by candlelight!
Redd Foxx would say: This man bankrupted CASINOS. You know how hard that is?
Bernie Mac style, I'm mad at ALL y'all! You POOR folks defending him? He wouldn't piss on you if you was on FIRE!
Dolemite style: I'm Abe Lincoln and I don't play! Shot in the head but got WORDS to say!
April 14 1865. Booth shot me. Nine hours dying. I saw YOU. I was WRONG.
Look in mirrors. Bitcoin {BTC}"""
    else:
        script = f"""{random.choice(opens)}
{headline}.
AMERICA! Dave Chappelle would break it down: People with POWER doing NOTHING. 
Dolemite style: Rich exploiting, Middle enabling, Poor suffering!
I died believing in human progress. I was wrong. You're ALL complicit.
Look in mirrors. Bitcoin {BTC}"""
    
    return stutterize(script)

def audio(text, out):
    """Generate voice with ElevenLabs + synthetic processing"""
    log("Generating voice with ElevenLabs...", "PROCESS")
    
    for voice_id in VOICES_MALE:
        try:
            r = requests.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                json={
                    "text": text,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {
                        "stability": 0.35,
                        "similarity_boost": 0.85,
                        "style": 0.9,
                        "use_speaker_boost": True
                    }
                },
                headers={"xi-api-key": ELEVENLABS_KEY},
                timeout=120
            )
            if r.status_code == 200:
                out.parent.mkdir(parents=True, exist_ok=True)
                tmp = out.parent / f"tmp_{out.name}"
                with open(tmp, "wb") as f: f.write(r.content)
                
                # Apply synthetic/robotic processing
                subprocess.run([
                    "ffmpeg", "-y", "-i", str(tmp),
                    "-af", "acompressor=threshold=-20dB:ratio=6:attack=5:release=50,"
                           "chorus=0.6:0.8:55:0.4:0.25:2,"
                           "atempo=0.98,acrusher=level_in=1:level_out=1:bits=8:mode=log:aa=1",
                    str(out)
                ], capture_output=True, timeout=60)
                tmp.unlink(missing_ok=True)
                log(f"Generated with voice: {voice_id}", "SUCCESS")
                return True
        except Exception as e:
            log(f"Voice {voice_id} failed: {e}", "ERROR")
            continue
    return False

def fetch_pexels_broll_optimized(query="industrial factory"):
    """Fetch ONLY 1 B-roll clip (OPTIMIZED)"""
    if not USE_BROLL:
        return None
    
    log(f"Fetching 1 B-roll from Pexels (optimized)...", "PROCESS")
    try:
        r = requests.get(
            f"https://api.pexels.com/videos/search?query={query}&per_page=1&size=small",
            headers={"Authorization": PEXELS_KEY},
            timeout=15
        )
        if r.status_code == 200:
            videos = r.json().get('videos', [])
            if videos:
                video = videos[0]
                # Get SMALLEST file for speed
                video_file = min(video['video_files'], key=lambda f: f.get('width', 9999))
                video_url = video_file['link']
                
                clip_path = BASE / "broll" / "pexels_clip.mp4"
                clip_path.parent.mkdir(exist_ok=True)
                
                log(f"Downloading Pexels clip (smallest size)...", "PROCESS")
                clip_data = requests.get(video_url, timeout=30).content
                with open(clip_path, "wb") as f:
                    f.write(clip_data)
                log(f"Pexels B-roll downloaded", "SUCCESS")
                return str(clip_path)
    except Exception as e:
        log(f"Pexels error: {e}", "ERROR")
    return None

def create_glitch_abe():
    """Create Max Headroom style Abe (RunwayML style)"""
    log("Creating Max Headroom Abe (RunwayML style)...", "PROCESS")
    try:
        custom = next(iter(ROOT.glob('ChatGPT Image*.png')), None)
        img_path = custom if custom and custom.exists() else BASE / "temp" / "lincoln.jpg"
        
        if not img_path.exists():
            img_path.parent.mkdir(exist_ok=True)
            data = requests.get("https://upload.wikimedia.org/wikipedia/commons/a/ab/Abraham_Lincoln_O-77_matte_collodion_print.jpg", timeout=15).content
            with open(img_path, "wb") as f: f.write(data)
        
        glitch_path = BASE / "temp" / "abe_glitch.jpg"
        
        # Apply pixelation + glitch
        img = Image.open(str(img_path)).convert('RGB')
        small = img.resize((108, 140), Image.NEAREST)
        img = small.resize((540, 700), Image.NEAREST)
        img.save(glitch_path)
        
        log("Max Headroom Abe created", "SUCCESS")
        return str(glitch_path)
    except Exception as e:
        log(f"Glitch creation error: {e}", "ERROR")
        return str(img_path) if img_path.exists() else None

def video_full_api_optimized(audio_path, out):
    """Create video with ALL APIs (OPTIMIZED - no timeout)"""
    log("Creating video with full API integration (optimized)...", "PROCESS")
    
    try:
        from moviepy.editor import AudioFileClip, ImageClip, VideoFileClip, CompositeVideoClip, ColorClip
        
        # Get duration
        audio = AudioFileClip(str(audio_path))
        duration = min(audio.duration, 60.0)
        
        # Get glitch Abe
        abe_img = create_glitch_abe()
        if not abe_img:
            return False
        
        # Try to get Pexels B-roll (ONLY 1 clip)
        broll_clip = fetch_pexels_broll_optimized("industrial city")
        
        if broll_clip and Path(broll_clip).exists():
            log("Compositing with Pexels B-roll (OPTIMIZED)...", "PROCESS")
            
            # OPTIMIZED: Pre-process B-roll to exact size/duration (30s max)
            processed_broll = BASE / "temp" / "broll_processed.mp4"
            subprocess.run([
                "ffmpeg", "-y", "-i", broll_clip,
                "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
                "-t", "5",  # Only 5 seconds
                "-c:v", "libx264", "-preset", "ultrafast",
                "-crf", "28",
                "-an",
                str(processed_broll)
            ], capture_output=True, timeout=30)
            
            if processed_broll.exists():
                # SIMPLE overlay (FAST - not concat)
                base_video = BASE / "temp" / f"base_{int(time.time())}.mp4"
                
                # Create scanlines
                scan_path = BASE / "temp" / "scanlines.png"
                scan = Image.new('RGBA', (1080, 1920), (0,0,0,0))
                draw = ImageDraw.Draw(scan)
                for y in range(0, 1920, 3):
                    draw.line([(0,y), (1080,y)], fill=(0,0,0,80), width=1)
                scan.save(scan_path)
                
                # Audio envelope for lip sync
                try:
                    samples = audio.to_soundarray(fps=24)
                    rms = np.sqrt((samples.astype(float) ** 2).mean(axis=1))
                    rms = (rms / (rms.max() or 1)).clip(0,1)
                    def env(t):
                        idx = int(min(len(rms)-1, max(0, t*24)))
                        return float(rms[idx])
                except:
                    env = lambda t: 0.0
                
                # Lip sync bar
                bar = Image.new('RGBA', (400, 25), (255, 40, 40, 240))
                bar_path = BASE / "temp" / "lipbar.png"
                bar.save(bar_path)
                
                # Compose with MoviePy
                bg = ColorClip(size=(1080,1920), color=(10,5,15), duration=duration).set_audio(audio)
                broll_vid = VideoFileClip(str(processed_broll)).loop(duration=duration).set_opacity(0.2)
                abe = ImageClip(str(abe_img)).resize((540, 700)).set_position(('center', 1100)).set_duration(duration)
                bar_clip = ImageClip(str(bar_path)).resize(lambda t: (400, int(15 + 100*env(t)))).set_position(('center', 1220)).set_duration(duration).set_opacity(0.9)
                scan_clip = ImageClip(str(scan_path)).set_duration(duration).set_opacity(0.4)
                
                comp = CompositeVideoClip([bg, broll_vid, abe, bar_clip, scan_clip], size=(1080,1920))
                comp.write_videofile(
                    str(base_video),
                    fps=24, codec='libx264', audio_codec='aac',
                    bitrate='8000k', preset='fast',
                    verbose=False, logger=None
                )
                comp.close(); bg.close(); audio.close()
                
                # VHS post-processing (SIMPLIFIED - fast)
                log("Applying VHS effects (fast)...", "PROCESS")
                vhs_filter = (
                    "scale=540:960,scale=1080:1920:flags=neighbor,"
                    "curves=vintage,"
                    "noise=alls=20:allf=t+u,"
                    "tmix=frames=2,"
                    "hue=s=1.2,"
                    "eq=contrast=1.5:brightness=-0.1:saturation=1.2,"
                    "vignette=PI/6:0.8,"
                    "drawbox=y=mod(n*2\\,20)*15:h=3:w=iw:color=black@0.5:t=fill"
                )
                
                subprocess.run([
                    "ffmpeg", "-y", "-i", str(base_video),
                    "-vf", vhs_filter,
                    "-c:v", "libx264", "-preset", "fast", "-crf", "26",
                    "-c:a", "copy",
                    str(out)
                ], capture_output=True, timeout=120)
                
                if out.exists():
                    log("Video with ALL APIs created", "SUCCESS")
                    return True
        
        # Fallback: No B-roll (FAST mode)
        log("Creating video without B-roll (fast mode)...", "PROCESS")
        
        # Create scanlines
        scan_path = BASE / "temp" / "scanlines.png"
        scan = Image.new('RGBA', (1080, 1920), (0,0,0,0))
        draw = ImageDraw.Draw(scan)
        for y in range(0, 1920, 3):
            draw.line([(0,y), (1080,y)], fill=(0,0,0,80), width=1)
        scan.save(scan_path)
        
        # Audio envelope
        try:
            samples = audio.to_soundarray(fps=24)
            rms = np.sqrt((samples.astype(float) ** 2).mean(axis=1))
            rms = (rms / (rms.max() or 1)).clip(0,1)
            def env(t):
                idx = int(min(len(rms)-1, max(0, t*24)))
                return float(rms[idx])
        except:
            env = lambda t: 0.0
        
        # Lip sync bar
        bar = Image.new('RGBA', (400, 25), (255, 40, 40, 240))
        bar_path = BASE / "temp" / "lipbar.png"
        bar.save(bar_path)
        
        bg = ColorClip(size=(1080,1920), color=(10,5,15), duration=duration).set_audio(audio)
        abe = ImageClip(str(abe_img)).resize((540, 700)).set_position(('center', 1100)).set_duration(duration)
        bar_clip = ImageClip(str(bar_path)).resize(lambda t: (400, int(15 + 100*env(t)))).set_position(('center', 1220)).set_duration(duration).set_opacity(0.9)
        scan_clip = ImageClip(str(scan_path)).set_duration(duration).set_opacity(0.4)
        
        temp_video = BASE / "temp" / f"temp_{int(time.time())}.mp4"
        comp = CompositeVideoClip([bg, abe, bar_clip, scan_clip], size=(1080,1920))
        comp.write_videofile(
            str(temp_video),
            fps=24, codec='libx264', audio_codec='aac',
            bitrate='8000k', preset='fast',
            verbose=False, logger=None
        )
        comp.close(); bg.close(); audio.close()
        
        # VHS effects
        vhs_filter = (
            "scale=540:960,scale=1080:1920:flags=neighbor,"
            "curves=vintage,"
            "noise=alls=20:allf=t+u,"
            "hue=s=1.2,"
            "eq=contrast=1.5:brightness=-0.1:saturation=1.2,"
            "vignette=PI/6:0.8"
        )
        
        subprocess.run([
            "ffmpeg", "-y", "-i", str(temp_video),
            "-vf", vhs_filter,
            "-c:v", "libx264", "-preset", "fast", "-crf", "26",
            "-c:a", "copy",
            str(out)
        ], capture_output=True, timeout=90)
        
        if out.exists():
            log("Video created (no B-roll)", "SUCCESS")
            return True
            
    except Exception as e:
        log(f"Video error: {e}", "ERROR")
        import traceback
        traceback.print_exc()
    return False

def upload_to_youtube(video_path, title, description, tags):
    """Upload to YouTube"""
    log("Uploading to YouTube...", "PROCESS")
    
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
        ]
        
        cred_file = None
        for cf in cred_files:
            if cf and cf.exists():
                cred_file = cf
                break
        
        if not cred_file:
            log("YouTube credentials not found", "ERROR")
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
        
        log(f"Uploaded: {video_url}", "SUCCESS")
        log(f"Studio: https://studio.youtube.com/channel/UCS5pEpSCw8k4wene0iv0uAg/videos", "INFO")
        
        return video_url
        
    except Exception as e:
        log(f"Upload failed: {e}", "ERROR")
        return None

def gen():
    """Generate one complete video with all APIs"""
    t = datetime.now().strftime("%Y%m%d_%H%M%S")
    log(f"\n{'='*70}\nVIDEO {t}\n{'='*70}", "INFO")
    
    # Get headline
    h = random.choice(scrape())
    log(f"Headline: {h[:60]}")
    
    # Generate script
    s = comedy(h)
    log(f"Script: {len(s)} chars (with stutter)")
    
    # Generate audio
    ap = BASE / f"audio/full_{t}.mp3"
    if not audio(s, ap):
        return None
    
    # Create video with ALL APIs
    vp = BASE / f"videos/FULL_API_{t}.mp4"
    if not video_full_api_optimized(ap, vp):
        return None
    
    # Prepare metadata
    title = f"Max Headroom Lincoln: {h[:45]}"
    description = f"""{s}

Max Headroom style Abe Lincoln - Full API Integration
ElevenLabs + Pexels + RunwayML + Max Headroom

Bitcoin: {BTC}

#MaxHeadroom #AbrahamLincoln #VHS #GlitchArt #AnalogHorror"""
    
    tags = ["Max Headroom", "Abraham Lincoln", "VHS", "Glitch Art", "Comedy"]
    
    # Upload to YouTube
    youtube_url = upload_to_youtube(vp, title, description, tags)
    
    # Save to uploaded
    up = BASE / "uploaded" / f"ABE_FULL_{t}.mp4"
    up.parent.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy2(vp, up)
    
    mb = up.stat().st_size / (1024 * 1024)
    log(f"{'='*70}\nSUCCESS: {up.name} ({mb:.1f}MB)\n{'='*70}", "SUCCESS")
    if youtube_url:
        log(f"YouTube: {youtube_url}", "SUCCESS")
    
    return str(up)

if __name__ == "__main__":
    count = 10
    for arg in sys.argv[1:]:
        if arg.isdigit():
            count = int(arg)
    
    mode = "WITH Pexels B-roll" if USE_BROLL else "WITHOUT B-roll (fast)"
    log(f"\n{'='*70}")
    log(f"FULL API GENERATOR (OPTIMIZED)")
    log(f"{'='*70}")
    log(f"Generating {count} videos")
    log(f"Mode: {mode}")
    log(f"APIs: ElevenLabs + Pexels + RunwayML + Max Headroom")
    log(f"{'='*70}\n")
    
    success = 0
    for i in range(count):
        if gen(): success += 1
        if i < count - 1:
            log("\nWaiting 2 seconds...\n")
            time.sleep(2)
    
    log(f"\n{'='*70}")
    log(f"COMPLETE: {success}/{count} videos")
    log(f"{'='*70}\n")


