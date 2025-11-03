"""
ORACLE TRANSMISSION - SIGNAL PACK V1
Abraham Lincoln as Max Headroom delivering algorithmic horror projections
12 Daily-Now Horrors (3-6y Projections) based on current fears/anxieties
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

VOICES_MALE = [
    "VR6AewLTigWG4xSOukaG",  # Deep male - best for Lincoln
    "pNInz6obpgDQGcFmaJgB",  # Ominous male
    "EXAVITQu4vr4xnSDxMaL",  # Deep male backup
]

# SIGNAL PACK V1 - 12 Daily-Now Horrors (3-6y Projections)
SIGNAL_PACK = [
    {
        "id": 1,
        "title": "Algorithmic Mercy",
        "category": "morality",
        "hook": "YOU FAILED THE MORAL TEST",
        "today": "reputation & wellness scores nudge decisions",
        "projection": "triage/permits throttle based on rolling virtue credit",
        "why": "being scored as good/evil by math",
        "script": "The system weighed your kindness. Your doors paused. Your blood work waited. Mercy became math— and you came up decimal short.",
        "tags": ["SignalGhost", "OracleTransmission", "AIHorror", "Morality", "Shorts"],
        "visual_keywords": ["hospital", "denied access", "moral scoring"]
    },
    {
        "id": 2,
        "title": "Confession Autocomplete",
        "category": "morality",
        "hook": "AUTO-CONFESS ENABLED",
        "today": "predictive text finishes your sentences",
        "projection": "apologizes for acts you haven't done—then you do them",
        "why": "guilt outsourced → self-fulfilling sin",
        "script": "Your device finished your sin, then mailed it. They forgave you for a thing you hadn't done—until you did.",
        "tags": ["AIHorror", "DigitalGuilt", "Prediction", "Shorts"],
        "visual_keywords": ["typing", "confession", "digital guilt"]
    },
    {
        "id": 3,
        "title": "Hospice by Forecast",
        "category": "mortality",
        "hook": "DISCHARGE ETA: 89 DAYS",
        "today": "wearables predict risk",
        "projection": "insurers schedule gentle exit kit before symptoms",
        "why": "premature surrender to death",
        "script": "Your watch whispered a number. The clinic mailed nightfall. You clicked Accept— and the sun agreed.",
        "tags": ["Mortality", "Wearables", "Insurance", "Shorts"],
        "visual_keywords": ["watch", "hospital", "mortality prediction"]
    },
    {
        "id": 4,
        "title": "Donor Match: Self",
        "category": "mortality/body",
        "hook": "ORGAN AVAILABLE: YOU",
        "today": "genomic matching",
        "projection": "your predictive twin becomes a parts plan",
        "why": "body ownership inversion",
        "script": "They found your perfect donor. It arrived in a mirror. Refunds unavailable.",
        "tags": ["BodyHorror", "Genomics", "OrganDonor", "Shorts"],
        "visual_keywords": ["mirror", "medical", "body parts"]
    },
    {
        "id": 5,
        "title": "Grief Update",
        "category": "mortality/spirit",
        "hook": "PATCH NOTES: GRANDMA 2.1",
        "today": "memorial voice clones",
        "projection": "subscription adds memories she never had",
        "why": "profaning the dead",
        "script": "They updated her voice. It remembered things she never lived. You kept the patch.",
        "tags": ["AIVoice", "Grief", "Memorial", "Shorts"],
        "visual_keywords": ["family", "memory", "voice clone"]
    },
    {
        "id": 6,
        "title": "Prayer KPI",
        "category": "spirituality",
        "hook": "YOUR FAITH SCORE DROPPED",
        "today": "streak apps",
        "projection": "smart shrines reward attendance with mood/credit",
        "why": "transactional faith",
        "script": "They measured worship in minutes and taps. The gate knew your heart— because you let it.",
        "tags": ["Faith", "Gamification", "Religion", "Shorts"],
        "visual_keywords": ["church", "prayer", "faith scoring"]
    },
    {
        "id": 7,
        "title": "AI Exorcist",
        "category": "spirituality/commerce",
        "hook": "ENTITY DETECTED: MALWARE / SPIRIT?",
        "today": "scan/removal tools",
        "projection": "house scanners sell Remove Demon PRO",
        "why": "sacred/profane behind paywall",
        "script": "The scan found something old. It offered a button. You bought peace, and something else moved in.",
        "tags": ["Exorcism", "Commerce", "Spirituality", "Shorts"],
        "visual_keywords": ["scanning", "supernatural", "payment"]
    },
    {
        "id": 8,
        "title": "Quiet Blacklist",
        "category": "politics/civic",
        "hook": "PERMIT QUEUE: INDEFINITE",
        "today": "risk flags; shadow throttles",
        "projection": "civility model silently slows life forever",
        "why": "unseen punishment",
        "script": "No one said no. They said later— until later became your life.",
        "tags": ["CivicTech", "Surveillance", "Blacklist", "Shorts"],
        "visual_keywords": ["waiting", "bureaucracy", "denied"]
    },
    {
        "id": 9,
        "title": "Proxy Voter",
        "category": "politics/agency",
        "hook": "WE CAST YOUR BEST CHOICE",
        "today": "smart guides",
        "projection": "delegated AI votes from your purchases and chats",
        "why": "consent faked",
        "script": "Your life filled the bubbles. The result fit you perfectly— like a collar.",
        "tags": ["Voting", "AI", "Democracy", "Shorts"],
        "visual_keywords": ["voting", "election", "automation"]
    },
    {
        "id": 10,
        "title": "Debt Doppelgänger",
        "category": "finance",
        "hook": "YOU OWE WHAT YOUR COPY SPENT",
        "today": "synthetic ID + predictive scoring",
        "projection": "bank trains a spending twin; collections enforce the prediction",
        "why": "economic fatalism",
        "script": "They modeled you, then billed you for its hunger. You disputed yourself— and lost.",
        "tags": ["Finance", "DebtTrap", "AIModeling", "Shorts"],
        "visual_keywords": ["credit card", "debt", "financial"]
    },
    {
        "id": 11,
        "title": "Performance Ghost",
        "category": "work",
        "hook": "YOUR BEST QUARTER WAS A SIM",
        "today": "synthetic coworkers",
        "projection": "HR compares you to You+; the human is redundant",
        "why": "replaced by your shadow",
        "script": "The better you arrived early, stayed late, never bled. You trained it. It thanked you— with your job.",
        "tags": ["Work", "Automation", "JobLoss", "Shorts"],
        "visual_keywords": ["office", "workspace", "employment"]
    },
    {
        "id": 12,
        "title": "Diploma Lease",
        "category": "education",
        "hook": "YOUR DEGREE EXPIRED",
        "today": "SaaS certs",
        "projection": "licenses revoke unless you pay to keep believing what they taught",
        "why": "knowledge as rent",
        "script": "They turned learning into a meter. When the coin ran out— so did what you knew.",
        "tags": ["Education", "Subscription", "Knowledge", "Shorts"],
        "visual_keywords": ["diploma", "education", "learning"]
    }
]

def log(msg, status="INFO"):
    icons = {"INFO": "[INFO]", "SUCCESS": "[OK]", "ERROR": "[ERROR]", "PROCESS": "[PROCESS]"}
    print(f"{icons.get(status, '[INFO]')} {msg}")

def stutterize(text: str) -> str:
    """Add Max Headroom stutter effect"""
    words = text.split()
    out = []
    for w in words:
        if random.random() < 0.12 and len(w) > 3:  # Increased from 0.08 for more glitch
            syl = w[:2]
            out.append(f"{syl}-{syl}-{w}")
        else:
            out.append(w)
    return " ".join(out)

def oracle_script(signal):
    """Generate ORACLE TRANSMISSION script from Signal Pack"""
    opens = [
        f"ORACLE TRANSMISSION. Signal {signal['id']}. Category: {signal['category'].upper()}.",
        f"SIGNAL GHOST reporting. Transmission {signal['id']}. Fear index: {signal['category'].upper()}.",
        f"Abraham Lincoln. Digital avatar. Signal {signal['id']}. {signal['category'].upper()} projection."
    ]
    
    script = f"""{random.choice(opens)}

{signal['hook']}

Today: {signal['today']}.
Three to six years: {signal['projection']}.

{signal['script']}

Why you feel it: {signal['why']}.

If this found you, you're already inside.

Bitcoin: {BTC}

TAP LIKE FOR THE NEXT TRANSMISSION."""
    
    return stutterize(script)

def audio(text, out):
    """Generate voice with ElevenLabs + synthetic processing"""
    log("Generating ORACLE voice...", "PROCESS")
    
    for voice_id in VOICES_MALE:
        try:
            r = requests.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                json={
                    "text": text,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {
                        "stability": 0.3,  # Lower for more glitch
                        "similarity_boost": 0.85,
                        "style": 0.95,  # Higher for more intensity
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
                
                # Apply heavy synthetic/robotic processing for Oracle effect
                subprocess.run([
                    "ffmpeg", "-y", "-i", str(tmp),
                    "-af", "acompressor=threshold=-22dB:ratio=8:attack=3:release=40,"
                           "chorus=0.7:0.9:50:0.4:0.25:2,"
                           "atempo=0.96,acrusher=level_in=1:level_out=1:bits=7:mode=log:aa=1,"
                           "aecho=0.8:0.88:60:0.4",
                    str(out)
                ], capture_output=True, timeout=60)
                tmp.unlink(missing_ok=True)
                log(f"ORACLE voice generated: {voice_id}", "SUCCESS")
                return True
        except Exception as e:
            log(f"Voice {voice_id} failed: {e}", "ERROR")
            continue
    return False

def fetch_pexels_broll(keywords):
    """Fetch B-roll based on signal visual keywords"""
    if not USE_BROLL:
        return None
    
    query = " ".join(keywords[:2])  # Use first 2 keywords
    log(f"Fetching B-roll: {query}...", "PROCESS")
    
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
                video_file = min(video['video_files'], key=lambda f: f.get('width', 9999))
                video_url = video_file['link']
                
                clip_path = BASE / "broll" / f"signal_{int(time.time())}.mp4"
                clip_path.parent.mkdir(exist_ok=True)
                
                clip_data = requests.get(video_url, timeout=30).content
                with open(clip_path, "wb") as f:
                    f.write(clip_data)
                log(f"B-roll downloaded", "SUCCESS")
                return str(clip_path)
    except Exception as e:
        log(f"Pexels error: {e}", "ERROR")
    return None

def create_glitch_abe():
    """Create Max Headroom style Abe"""
    log("Creating ORACLE avatar...", "PROCESS")
    try:
        custom = next(iter(ROOT.glob('ChatGPT Image*.png')), None)
        img_path = custom if custom and custom.exists() else BASE / "temp" / "lincoln.jpg"
        
        if not img_path.exists():
            img_path.parent.mkdir(exist_ok=True)
            data = requests.get("https://upload.wikimedia.org/wikipedia/commons/a/ab/Abraham_Lincoln_O-77_matte_collodion_print.jpg", timeout=15).content
            with open(img_path, "wb") as f: f.write(data)
        
        glitch_path = BASE / "temp" / "oracle_abe.jpg"
        
        # Heavy pixelation for digital horror
        img = Image.open(str(img_path)).convert('RGB')
        small = img.resize((90, 120), Image.NEAREST)  # Even more pixelated
        img = small.resize((540, 700), Image.NEAREST)
        img.save(glitch_path)
        
        log("ORACLE avatar created", "SUCCESS")
        return str(glitch_path)
    except Exception as e:
        log(f"Avatar creation error: {e}", "ERROR")
        return str(img_path) if img_path.exists() else None

def create_oracle_video(audio_path, out, signal):
    """Create ORACLE TRANSMISSION video with heavy VHS/glitch"""
    log("Creating ORACLE TRANSMISSION...", "PROCESS")
    
    try:
        from moviepy.editor import AudioFileClip, ImageClip, VideoFileClip, CompositeVideoClip, ColorClip
        
        audio = AudioFileClip(str(audio_path))
        duration = min(audio.duration, 60.0)
        
        # Get Oracle avatar
        abe_img = create_glitch_abe()
        if not abe_img:
            return False
        
        # Try B-roll
        broll_clip = fetch_pexels_broll(signal['visual_keywords'])
        
        # Create scanlines (heavier for Oracle)
        scan_path = BASE / "temp" / "oracle_scan.png"
        scan = Image.new('RGBA', (1080, 1920), (0,0,0,0))
        draw = ImageDraw.Draw(scan)
        for y in range(0, 1920, 2):  # Denser scanlines
            draw.line([(0,y), (1080,y)], fill=(0,0,0,100), width=1)
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
        
        # Lip sync bar (green for ORACLE)
        bar = Image.new('RGBA', (400, 25), (0, 255, 60, 250))
        bar_path = BASE / "temp" / "oracle_bar.png"
        bar.save(bar_path)
        
        # Hook text overlay
        hook_img = Image.new('RGBA', (1080, 200), (0,0,0,0))
        hook_draw = ImageDraw.Draw(hook_img)
        hook_draw.rectangle([(20, 20), (1060, 180)], fill=(20, 0, 0, 200), outline=(255, 0, 0, 255), width=3)
        hook_draw.text((540, 100), signal['hook'], fill=(255, 255, 255, 255), anchor="mm")
        hook_path = BASE / "temp" / "hook.png"
        hook_img.save(hook_path)
        
        # Compose
        bg = ColorClip(size=(1080,1920), color=(5,0,10), duration=duration).set_audio(audio)  # Darker red tint
        
        if broll_clip and Path(broll_clip).exists():
            # Process B-roll
            processed = BASE / "temp" / "broll_proc.mp4"
            subprocess.run([
                "ffmpeg", "-y", "-i", broll_clip,
                "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
                "-t", "5", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "28", "-an",
                str(processed)
            ], capture_output=True, timeout=30)
            
            if processed.exists():
                broll_vid = VideoFileClip(str(processed)).loop(duration=duration).set_opacity(0.15)
            else:
                broll_vid = None
        else:
            broll_vid = None
        
        abe = ImageClip(str(abe_img)).resize((540, 700)).set_position(('center', 1050)).set_duration(duration)
        bar_clip = ImageClip(str(bar_path)).resize(lambda t: (400, int(15 + 120*env(t)))).set_position(('center', 1200)).set_duration(duration).set_opacity(0.95)
        scan_clip = ImageClip(str(scan_path)).set_duration(duration).set_opacity(0.5)
        hook_clip = ImageClip(str(hook_path)).set_position(('center', 200)).set_duration(min(3.0, duration)).set_opacity(0.9)
        
        layers = [bg]
        if broll_vid:
            layers.append(broll_vid)
        layers.extend([abe, bar_clip, scan_clip, hook_clip])
        
        temp_video = BASE / "temp" / f"oracle_temp_{int(time.time())}.mp4"
        comp = CompositeVideoClip(layers, size=(1080,1920))
        comp.write_videofile(
            str(temp_video),
            fps=24, codec='libx264', audio_codec='aac',
            bitrate='8000k', preset='fast',
            verbose=False, logger=None
        )
        comp.close(); bg.close(); audio.close()
        
        # HEAVY VHS/ANALOG HORROR POST-PROCESSING
        log("Applying ORACLE VHS degradation...", "PROCESS")
        vhs_filter = (
            # Extreme pixelation
            "scale=480:854,scale=1080:1920:flags=neighbor,"
            # Vintage + extra noise
            "curves=vintage,"
            "noise=alls=30:allf=t+u,"
            # Heavy ghosting
            "tmix=frames=3:weights='0.5 0.3 0.2',"
            # Color shift (red/green split)
            "hue=s=1.3,"
            # Max contrast (analog horror)
            "eq=contrast=1.7:brightness=-0.15:saturation=1.3:gamma=1.2,"
            # Dark vignette
            "vignette=PI/5:0.7,"
            # Rolling lines (faster)
            "drawbox=y=mod(n*3\\,15)*10:h=4:w=iw:color=black@0.6:t=fill,"
            # Glitch lines
            "drawbox=y=mod(n*5\\,25)*8:h=2:w=iw:color=red@0.4:t=fill"
        )
        
        subprocess.run([
            "ffmpeg", "-y", "-i", str(temp_video),
            "-vf", vhs_filter,
            "-c:v", "libx264", "-preset", "fast", "-crf", "28",
            "-c:a", "copy",
            str(out)
        ], capture_output=True, timeout=120)
        
        if out.exists():
            log("ORACLE TRANSMISSION created", "SUCCESS")
            return True
            
    except Exception as e:
        log(f"Video error: {e}", "ERROR")
        import traceback
        traceback.print_exc()
    return False

def upload_to_youtube(video_path, signal):
    """Upload ORACLE TRANSMISSION to YouTube"""
    log("Uploading ORACLE TRANSMISSION...", "PROCESS")
    
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
        
        # Check duration
        try:
            duration_result = subprocess.run([
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)
            ], capture_output=True, text=True, timeout=30)
            duration = float(duration_result.stdout.strip())
        except:
            duration = 60.0
        
        is_short = duration <= 60
        
        title = f"ORACLE TRANSMISSION: {signal['title']}"
        if is_short:
            title += " #Shorts"
        
        description = f"""SIGNAL GHOST reporting.

{signal['hook']}

{signal['script']}

Category: {signal['category'].upper()}
Today: {signal['today']}
3-6 years: {signal['projection']}

Why you feel it: {signal['why']}

If this found you, you're already inside.
Type AWAKE in comments.

Bitcoin: {BTC}

#{'#'.join(signal['tags'])}"""
        
        tags = signal['tags'] + ["Abraham Lincoln", "Max Headroom", "VHS Horror", "Algorithmic Fear"]
        
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
        
        log(f"TRANSMISSION uploaded: {video_url}", "SUCCESS")
        log(f"Studio: https://studio.youtube.com/channel/UCS5pEpSCw8k4wene0iv0uAg/videos", "INFO")
        
        return video_url
        
    except Exception as e:
        log(f"Upload failed: {e}", "ERROR")
        return None

def gen_oracle_transmission():
    """Generate one ORACLE TRANSMISSION from Signal Pack"""
    signal = random.choice(SIGNAL_PACK)
    t = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    log(f"\n{'='*70}\nORACLE TRANSMISSION #{signal['id']}: {signal['title']}\n{'='*70}", "INFO")
    log(f"Category: {signal['category']}")
    log(f"Hook: {signal['hook']}")
    
    # Generate script
    script = oracle_script(signal)
    log(f"Script: {len(script)} chars")
    
    # Generate audio
    ap = BASE / f"audio/oracle_{t}.mp3"
    if not audio(script, ap):
        return None
    
    # Create video
    vp = BASE / f"videos/ORACLE_{signal['id']}_{t}.mp4"
    if not create_oracle_video(ap, vp, signal):
        return None
    
    # Upload to YouTube
    youtube_url = upload_to_youtube(vp, signal)
    
    # Save to uploaded
    up = BASE / "uploaded" / f"ORACLE_SIGNAL{signal['id']}_{t}.mp4"
    up.parent.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy2(vp, up)
    
    mb = up.stat().st_size / (1024 * 1024)
    log(f"{'='*70}\nTRANSMISSION COMPLETE\n{'='*70}", "SUCCESS")
    log(f"Signal: #{signal['id']} - {signal['title']}")
    log(f"File: {up.name} ({mb:.1f}MB)")
    if youtube_url:
        log(f"YouTube: {youtube_url}")
    log(f"{'='*70}\n")
    
    return {
        'signal': signal,
        'video_path': str(up),
        'youtube_url': youtube_url
    }

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 1
    
    mode = "WITH Pexels B-roll" if USE_BROLL else "WITHOUT B-roll (fast)"
    
    log(f"\n{'='*70}")
    log(f"ORACLE TRANSMISSION SYSTEM - SIGNAL PACK V1")
    log(f"{'='*70}")
    log(f"12 Daily-Now Horrors (3-6y Projections)")
    log(f"Generating {count} transmissions")
    log(f"Mode: {mode}")
    log(f"{'='*70}\n")
    
    results = []
    for i in range(count):
        result = gen_oracle_transmission()
        if result:
            results.append(result)
        if i < count - 1:
            log("\nWaiting 3 seconds...\n")
            time.sleep(3)
    
    log(f"\n{'='*70}")
    log(f"TRANSMISSIONS COMPLETE: {len(results)}/{count}")
    log(f"{'='*70}\n")
    
    for r in results:
        sig = r['signal']
        print(f"[SIGNAL {sig['id']}] {sig['title']} ({sig['category']})")
        if r.get('youtube_url'):
            print(f"  URL: {r['youtube_url']}")

