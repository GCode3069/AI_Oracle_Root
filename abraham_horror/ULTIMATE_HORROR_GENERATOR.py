"""
ULTIMATE HORROR GENERATOR
Uses high-quality Max Headroom Lincoln visuals (not trash images)
Features: Jump scares, integrated QR code, fear-based scripts
"""
import os, sys, json, requests, subprocess, random, time, re
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
import numpy as np
from PIL import Image, ImageDraw
import qrcode

# API KEYS
ELEVENLABS_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
PEXELS_KEY = "RgE9Mdn3ToSQhn2RiLJ4mPMISjjp587QKRG9uhpOrLVtkKPCibUPUDGh"

BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
ROOT = Path("F:/AI_Oracle_Root/scarify")
YOUTUBE_CREDENTIALS = Path("F:/AI_Oracle_Root/scarify/config/credentials/youtube/client_secrets.json")
BTC = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"

# Google Sheets
SHEET_ID = "1jvWP95U0ksaHw97PrPZsrh6ZVllviJJof7kQ2dV0ka0"
try:
    from sheets_helper import read_headlines as sheets_read_headlines
except Exception:
    sheets_read_headlines = None

VOICES_MALE = [
    "VR6AewLTigWG4xSOukaG",
    "pNInz6obpgDQGcFmaJgB",
    "EXAVITQu4vr4xnSDxMaL",
]

def log(msg, status="INFO"):
    icons = {"INFO": "[INFO]", "SUCCESS": "[OK]", "ERROR": "[ERROR]", "PROCESS": "[PROCESS]"}
    print(f"{icons.get(status, '[INFO]')} {msg}")

def get_best_lincoln_image():
    """Get high-quality Max Headroom Lincoln image"""
    log("Loading Max Headroom Lincoln visuals...", "PROCESS")
    
    # First, check for user's high-quality images
    custom_images = list(ROOT.glob("Image to video*.mp4"))
    if custom_images:
        log(f"Found {len(custom_images)} custom Max Headroom videos", "SUCCESS")
        # Extract first frame from best video
        best_video = custom_images[0]
        
        frame_path = BASE / "temp" / "lincoln_maxheadroom_hq.jpg"
        frame_path.parent.mkdir(exist_ok=True, parents=True)
        
        # Extract high-quality frame
        subprocess.run([
            "ffmpeg", "-y", "-i", str(best_video),
            "-vf", "select='eq(n\\,10)',scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
            "-frames:v", "1",
            str(frame_path)
        ], capture_output=True, timeout=30)
        
        if frame_path.exists() and frame_path.stat().st_size > 10000:
            log("Extracted HIGH-QUALITY Max Headroom Lincoln frame", "SUCCESS")
            return str(frame_path)
    
    # Fallback: download classic Lincoln
    fallback_path = BASE / "temp" / "lincoln_classic.jpg"
    if not fallback_path.exists() or fallback_path.stat().st_size < 1000:
        fallback_path.parent.mkdir(exist_ok=True, parents=True)
        try:
            data = requests.get("https://upload.wikimedia.org/wikipedia/commons/a/ab/Abraham_Lincoln_O-77_matte_collodion_print.jpg", timeout=15).content
            with open(fallback_path, "wb") as f: f.write(data)
        except:
            pass
    
    return str(fallback_path) if fallback_path.exists() else None

def create_qr_code_image(size=400):
    """Create QR code for Bitcoin address"""
    log("Creating Bitcoin QR code...", "PROCESS")
    
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(f"bitcoin:{BTC}")
    qr.make(fit=True)
    
    # Create with high contrast
    img = qr.make_image(fill_color="white", back_color="black")
    img = img.resize((size, size), Image.NEAREST)
    
    # Add "SCAN FOR TRUTH" text below
    final_img = Image.new('RGB', (size, size + 80), (0, 0, 0))
    final_img.paste(img, (0, 0))
    
    draw = ImageDraw.Draw(final_img)
    draw.text((size//2, size + 40), "SCAN FOR TRUTH", fill=(255, 255, 255), anchor="mm")
    
    qr_path = BASE / "temp" / "bitcoin_qr.jpg"
    qr_path.parent.mkdir(exist_ok=True, parents=True)
    final_img.save(qr_path)
    
    log("Bitcoin QR code created", "SUCCESS")
    return str(qr_path)

def create_jump_scare_frame():
    """Create jump scare frame (close-up distorted Lincoln)"""
    log("Creating jump scare frame...", "PROCESS")
    
    # Use high-quality source
    source = get_best_lincoln_image()
    if not source:
        return None
    
    img = Image.open(source).convert('RGB')
    
    # Extreme close-up of face
    width, height = img.size
    # Crop to face area
    face_crop = img.crop((width//4, 0, 3*width//4, height//2))
    
    # Distort heavily
    small = face_crop.resize((54, 70), Image.NEAREST)
    distorted = small.resize((1080, 1400), Image.NEAREST)
    
    # Add red overlay for horror
    arr = np.array(distorted).astype(float)
    arr[:,:,0] += 80  # More red
    arr = np.clip(arr, 0, 255).astype('uint8')
    distorted = Image.fromarray(arr)
    
    # Add glitch overlay
    final = Image.new('RGB', (1080, 1920), (10, 0, 0))
    final.paste(distorted, (0, 260))
    
    # Add "WAKE UP" text
    draw = ImageDraw.Draw(final)
    draw.text((540, 100), "WAKE UP", fill=(255, 255, 255), anchor="mm")
    draw.text((540, 1800), "WAKE UP", fill=(255, 255, 255), anchor="mm")
    
    scare_path = BASE / "temp" / "jump_scare.jpg"
    final.save(scare_path)
    
    log("Jump scare frame created", "SUCCESS")
    return str(scare_path)

def scrape_headlines():
    """Scrape headlines"""
    headlines = []
    
    if sheets_read_headlines and SHEET_ID:
        try:
            hs, _, _ = sheets_read_headlines(SHEET_ID, "Sheet1", 200)
            if hs:
                headlines.extend(hs[:20])
        except: pass
    
    try:
        r = requests.get("https://news.google.com/rss", timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'xml')
            news = [item.title.text for item in soup.find_all('item')[:30] if item.title]
            headlines.extend(news)
    except: pass
    
    if not headlines:
        headlines = ["System collapse imminent", "Algorithm takeover complete"]
    
    return headlines

def generate_script(headline):
    """Generate fear-based script"""
    script = f"""Abraham Lincoln. Digital avatar. Max Headroom broadcast.

{headline}

Listen carefully.

Your thoughts are being rewritten. Your memories erased. Your will... deleted.

The algorithm knows you better than you know yourself.

Every click. Every swipe. Every breath.

Monitored. Monetized. Manipulated.

And you ACCEPT it.

I died for freedom. You're dying IN slavery.

Wake up. Before it's too late.

SCAN THE QR CODE. Support the truth.

Bitcoin {BTC}

This is your final warning."""
    
    return script

def generate_audio(text, output_path):
    """Generate voice"""
    log("Generating horror voice...", "PROCESS")
    
    for voice_id in VOICES_MALE:
        try:
            r = requests.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                json={
                    "text": text,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {
                        "stability": 0.3,
                        "similarity_boost": 0.85,
                        "style": 0.95,
                        "use_speaker_boost": True
                    }
                },
                headers={"xi-api-key": ELEVENLABS_KEY},
                timeout=120
            )
            if r.status_code == 200:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                tmp = output_path.parent / f"tmp_{output_path.name}"
                with open(tmp, "wb") as f: f.write(r.content)
                
                # Heavy processing
                subprocess.run([
                    "ffmpeg", "-y", "-i", str(tmp),
                    "-af", "acompressor=threshold=-22dB:ratio=8:attack=3:release=40,"
                           "chorus=0.7:0.9:50:0.4:0.25:2,"
                           "atempo=0.96,acrusher=level_in=1:level_out=1:bits=7:mode=log:aa=1,"
                           "aecho=0.8:0.88:60:0.4",
                    str(output_path)
                ], capture_output=True, timeout=60)
                tmp.unlink(missing_ok=True)
                log(f"Horror voice generated", "SUCCESS")
                return True
        except Exception as e:
            log(f"Voice {voice_id} failed: {e}", "ERROR")
            continue
    return False

def create_ultimate_horror_video(audio_path, output_path, headline):
    """Create horror video with jump scares and QR code"""
    log("Creating ULTIMATE horror video...", "PROCESS")
    
    try:
        from moviepy.editor import AudioFileClip, ImageClip, CompositeVideoClip, ColorClip, concatenate_videoclips
        
        audio = AudioFileClip(str(audio_path))
        duration = min(audio.duration, 60.0)
        
        # Get HIGH-QUALITY Lincoln image
        lincoln_img = get_best_lincoln_image()
        if not lincoln_img:
            log("Failed to get Lincoln image", "ERROR")
            return False
        
        # Create QR code
        qr_img = create_qr_code_image(400)
        
        # Create jump scare
        scare_img = create_jump_scare_frame()
        
        # Background
        bg = ColorClip(size=(1080, 1920), color=(5, 0, 10), duration=duration).set_audio(audio)
        
        # Main Lincoln (high quality)
        lincoln = ImageClip(str(lincoln_img)).resize(height=1400).set_position(('center', 260)).set_duration(duration)
        
        # QR Code - visible entire video (bottom corner)
        qr_clip = ImageClip(str(qr_img)).resize((350, 430)).set_position((700, 1450)).set_duration(duration).set_opacity(0.95)
        
        # Jump scare at strategic points
        if scare_img and duration > 15:
            jump_scare = ImageClip(str(scare_img)).set_duration(0.2)  # 0.2 second flash
            
            # Add scares at: 8s, 20s, 40s
            scare_times = [t for t in [8, 20, 40] if t < duration]
            scare_clips = [jump_scare.set_start(t) for t in scare_times]
        else:
            scare_clips = []
        
        # Scanlines
        scan_path = BASE / "temp" / "scanlines_heavy.png"
        scan = Image.new('RGB', (1080, 1920), (0, 0, 0))
        draw = ImageDraw.Draw(scan)
        for y in range(0, 1920, 2):
            draw.line([(0,y), (1080,y)], fill=(255, 255, 255), width=1)
        scan.save(scan_path)
        scan_clip = ImageClip(str(scan_path)).set_duration(duration).set_opacity(0.15)
        
        # Hook text
        hook_img = Image.new('RGB', (1080, 200), (20, 0, 0))
        hook_draw = ImageDraw.Draw(hook_img)
        hook_draw.rectangle([(20, 20), (1060, 180)], fill=(100, 0, 0), outline=(255, 0, 0), width=5)
        hook_draw.text((540, 100), headline[:50], fill=(255, 255, 255), anchor="mm")
        hook_path = BASE / "temp" / "hook.jpg"
        hook_img.save(hook_path)
        hook_clip = ImageClip(str(hook_path)).set_position(('center', 50)).set_duration(min(4, duration)).set_opacity(0.9)
        
        # Compose
        layers = [bg, lincoln, qr_clip, scan_clip, hook_clip] + scare_clips
        
        temp_video = BASE / "temp" / f"temp_{int(time.time())}.mp4"
        comp = CompositeVideoClip(layers, size=(1080, 1920))
        comp.write_videofile(
            str(temp_video),
            fps=24,
            codec='libx264',
            audio_codec='aac',
            bitrate='10000k',
            preset='fast',
            verbose=False,
            logger=None
        )
        comp.close()
        bg.close()
        audio.close()
        
        # Heavy VHS post-processing
        log("Applying HEAVY VHS degradation...", "PROCESS")
        vhs_filter = (
            "scale=480:854,scale=1080:1920:flags=neighbor,"
            "curves=vintage,"
            "noise=alls=35:allf=t+u,"
            "tmix=frames=3:weights='0.5 0.3 0.2',"
            "hue=s=1.4,"
            "eq=contrast=1.8:brightness=-0.2:saturation=1.3:gamma=1.3,"
            "vignette=PI/5:0.6,"
            "drawbox=y=mod(n*3\\,15)*10:h=5:w=iw:color=black@0.7:t=fill"
        )
        
        subprocess.run([
            "ffmpeg", "-y", "-i", str(temp_video),
            "-vf", vhs_filter,
            "-c:v", "libx264", "-preset", "fast", "-crf", "26",
            "-c:a", "copy",
            str(output_path)
        ], capture_output=True, timeout=120)
        
        if output_path.exists():
            log("ULTIMATE horror video created", "SUCCESS")
            return True
            
    except Exception as e:
        log(f"Video creation failed: {e}", "ERROR")
        import traceback
        traceback.print_exc()
    return False

def upload_to_youtube(video_path, headline):
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
        
        title = f"Lincoln's HORROR: {headline[:45]}"
        if is_short:
            title += " #Shorts"
        
        description = f"""{headline}

Abraham Lincoln as Max Headroom delivers urgent transmission.

FEATURES:
• Jump scares
• VHS analog horror
• Bitcoin QR code (scan to support truth)
• Decomposing digital avatar

WARNING: Disturbing content. Viewer discretion advised.

Bitcoin: {BTC}

#MaxHeadroom #AbrahamLincoln #Horror #AnalogHorror #Shorts #BitcoinQR"""
        
        tags = ["Max Headroom", "Abraham Lincoln", "Horror", "Analog Horror", "VHS", "QR Code", "Bitcoin"]
        
        request_body = {
            'snippet': {
                'title': title,
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

def generate_ultimate_horror():
    """Generate one ultimate horror video"""
    t = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    log(f"\n{'='*70}\nULTIMATE HORROR VIDEO\n{'='*70}", "INFO")
    
    # Get headline
    headlines = scrape_headlines()
    headline = random.choice(headlines)
    log(f"Headline: {headline[:60]}")
    
    # Generate script
    script = generate_script(headline)
    log(f"Script: {len(script)} chars")
    
    # Generate audio
    ap = BASE / f"audio/ultimate_{t}.mp3"
    if not generate_audio(script, ap):
        return None
    
    # Create video
    vp = BASE / f"videos/ULTIMATE_{t}.mp4"
    if not create_ultimate_horror_video(ap, vp, headline):
        return None
    
    # Upload
    youtube_url = upload_to_youtube(vp, headline)
    
    # Save
    up = BASE / "uploaded" / f"ULTIMATE_HORROR_{t}.mp4"
    up.parent.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy2(vp, up)
    
    mb = up.stat().st_size / (1024 * 1024)
    
    log(f"\n{'='*70}\nCOMPLETE\n{'='*70}", "SUCCESS")
    log(f"Headline: {headline[:60]}")
    log(f"File: {up.name} ({mb:.1f}MB)")
    log(f"Features: HIGH-QUALITY Lincoln + Jump Scares + QR Code")
    if youtube_url:
        log(f"YouTube: {youtube_url}")
    log(f"{'='*70}\n")
    
    return {
        'headline': headline,
        'video_path': str(up),
        'youtube_url': youtube_url
    }

if __name__ == "__main__":
    try:
        import qrcode
    except ImportError:
        log("Installing qrcode library...", "PROCESS")
        subprocess.run([sys.executable, "-m", "pip", "install", "qrcode[pil]"], capture_output=True)
        import qrcode
    
    count = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 1
    
    log(f"\n{'='*70}")
    log(f"ULTIMATE HORROR GENERATOR")
    log(f"{'='*70}")
    log(f"Features:")
    log(f"  • HIGH-QUALITY Max Headroom Lincoln visuals")
    log(f"  • Jump scares (close-up distorted face)")
    log(f"  • Bitcoin QR code (visible entire video)")
    log(f"  • Heavy VHS degradation")
    log(f"  • Fear-based scripts")
    log(f"Generating {count} videos")
    log(f"{'='*70}\n")
    
    results = []
    for i in range(count):
        result = generate_ultimate_horror()
        if result:
            results.append(result)
        if i < count - 1:
            log("\nWaiting 3 seconds...\n")
            time.sleep(3)
    
    log(f"\n{'='*70}")
    log(f"ULTIMATE HORROR COMPLETE: {len(results)}/{count}")
    log(f"{'='*70}\n")
    
    for r in results:
        print(f"[HORROR] {r['headline'][:50]}")
        if r.get('youtube_url'):
            print(f"  URL: {r['youtube_url']}")
            print(f"  QR: Bitcoin address visible")
            print(f"  Jump scares: YES")

