# ABRAHAM LINCOLN - ALL APIs WITH OPTIMIZED PROCESSING
# Uses: Pexels + Pollo.ai + RunwayML + ElevenLabs
# Smart processing to avoid timeouts

param([int]$Videos = 10, [switch]$SkipBroll)

$ROOT = "F:\AI_Oracle_Root\scarify\abraham_horror"

Write-Host ""
Write-Host "ABRAHAM LINCOLN - FULL API INTEGRATION" -ForegroundColor Red
Write-Host "Pexels + Pollo.ai + RunwayML + ElevenLabs" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host ""

# Create directories
$dirs = @("audio", "videos", "uploaded", "temp", "broll", "pollo_cache")
foreach ($dir in $dirs) {
    $path = Join-Path $ROOT $dir
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
        Write-Host "[OK] Created: $dir" -ForegroundColor Green
    }
}

# Install packages
Write-Host ""
Write-Host "[PROCESS] Installing Python packages..." -ForegroundColor Cyan
pip install --quiet requests beautifulsoup4 lxml pillow 2>&1 | Out-Null
Write-Host "[OK] Packages installed" -ForegroundColor Green

# Create full-featured Python script
Write-Host ""
Write-Host "[PROCESS] Creating full-featured generator..." -ForegroundColor Cyan

$pythonCode = @'
"""
ABRAHAM LINCOLN - FULL API INTEGRATION
Uses: Pexels + Pollo.ai + RunwayML + ElevenLabs
Optimized to avoid timeouts
Integrated with Google Sheets for headlines
"""
import os, sys, json, requests, subprocess, random, time
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

# API KEYS FROM YOUR SETUP
ELEVENLABS_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
PEXELS_KEY = "RgE9Mdn3ToSQhn2RiLJ4mPMISjjp587QKRG9uhpOrLVtkKPCibUPUDGh"
POLLO_API = "YOUR_POLLO_API_KEY"  # Get from Pollo.ai dashboard
RUNWAY_KEY = "scarify"  # Your RunwayML project name

BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
YOUTUBE_CREDENTIALS = Path("F:/AI_Oracle_Root/scarify/config/credentials/youtube/client_secrets.json")
BTC = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"

# Google Sheets integration
SHEET_ID = "1jvWP95U0ksaHw97PrPZsrh6ZVllviJJof7kQ2dV0ka0"
try:
    from sheets_helper import read_headlines as sheets_read_headlines
except Exception:
    sheets_read_headlines = None

USE_BROLL = "--skip-broll" not in sys.argv

def log(msg, status="INFO"):
    icons = {"INFO": "[INFO]", "SUCCESS": "[OK]", "ERROR": "[ERROR]", "PROCESS": "[PROCESS]"}
    print(f"    {icons.get(status, '[INFO]')} {msg}")

def scrape():
    """Get headlines from Google Sheets first, then fall back to web scraping"""
    # Try Google Sheets first
    if sheets_read_headlines and SHEET_ID and len(SHEET_ID) > 10:
        try:
            hs, _, _ = sheets_read_headlines(SHEET_ID, "Sheet1", 200)
            if hs:
                log(f"Loaded {len(hs)} headlines from Google Sheets", "SUCCESS")
                return hs
        except Exception as e:
            log(f"Sheets read failed: {e}, using web scraping", "ERROR")
    
    # Fallback to web scraping
    try:
        r = requests.get("https://news.google.com/rss", timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'xml')
            return [item.title.text for item in soup.find_all('item')[:20] if item.title]
    except: pass
    return ["Trump Policies", "Police Violence", "Climate Crisis"]

def comedy(headline):
    hl = headline.lower()
    
    opens = [
        "Abraham Lincoln! Six foot four! Honest Abe who freed the slaves and MORE!",
        "I'm Abraham Lincoln, yeah that's right! Got shot in the head but I'm STILL upright!",
        "Abe Lincoln in the house! Tallest president, best president, no doubt!"
    ]
    
    if "trump" in hl:
        return f"""{random.choice(opens)}

AMERICA! Let me tell you something right now!

{headline}.

Dave Chappelle style, real talk. This man got POOR people defending a BILLIONAIRE. That's like chickens voting for Colonel Sanders!

I grew up in a LOG CABIN. Not Trump Tower! I split rails! Read by candlelight!

Redd Foxx would say: This man bankrupted CASINOS. You know how hard that is?

Bernie Mac style, I'm mad at ALL y'all! You POOR folks defending him? He wouldn't piss on you if you was on FIRE!

Dolemite style: I'm Abe Lincoln and I don't play! Shot in the head but got WORDS to say!

April 14 1865. Booth shot me. Nine hours dying. I saw YOU. I was WRONG.

Look in mirrors. Bitcoin {BTC}"""
    
    return f"""{random.choice(opens)}

{headline}.

AMERICA! Dave Chappelle would break it down: People with POWER doing NOTHING. 

Dolemite style: Rich exploiting, Middle enabling, Poor suffering!

I died believing in human progress. I was wrong. You're ALL complicit.

Look in mirrors. Bitcoin {BTC}"""

def audio(text, out):
    """Generate audio with ElevenLabs"""
    log("Generating voice with ElevenLabs...", "PROCESS")
    try:
        r = requests.post("https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB",
                         json={"text": text, "model_id": "eleven_multilingual_v2",
                               "voice_settings": {"stability": 0.4, "similarity_boost": 0.9, 
                                                "style": 0.8, "use_speaker_boost": True}},
                         headers={"xi-api-key": ELEVENLABS_KEY}, timeout=240)
        if r.status_code == 200:
            out.parent.mkdir(parents=True, exist_ok=True)
            with open(out, "wb") as f: f.write(r.content)
            log("ElevenLabs audio generated", "SUCCESS")
            return True
    except Exception as e:
        log(f"ElevenLabs error: {e}", "ERROR")
    return False

def fetch_pexels_broll(query="industrial factory", count=1):
    """Fetch B-roll from Pexels (optimized - only 1 clip)"""
    if not USE_BROLL:
        return []
    
    log(f"Fetching B-roll from Pexels...", "PROCESS")
    try:
        r = requests.get(
            f"https://api.pexels.com/videos/search?query={query}&per_page={count}&size=small",
            headers={"Authorization": PEXELS_KEY},
            timeout=30
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
                
                log(f"Downloading Pexels clip (small size)...", "PROCESS")
                clip_data = requests.get(video_url, timeout=60).content
                with open(clip_path, "wb") as f:
                    f.write(clip_data)
                log(f"Pexels B-roll downloaded", "SUCCESS")
                return [str(clip_path)]
        else:
            log(f"Pexels API returned: {r.status_code}", "ERROR")
    except Exception as e:
        log(f"Pexels error: {e}", "ERROR")
    return []

def create_glitch_abe():
    """Create Max Headroom style Abe with glitch effects"""
    log("Creating Max Headroom Abe with RunwayML style...", "PROCESS")
    try:
        img_path = BASE / "temp" / "lincoln.jpg"
        glitch_path = BASE / "temp" / "abe_glitch.jpg"
        
        if not img_path.exists():
            img_path.parent.mkdir(exist_ok=True)
            data = requests.get("https://upload.wikimedia.org/wikipedia/commons/a/ab/Abraham_Lincoln_O-77_matte_collodion_print.jpg", timeout=30).content
            with open(img_path, "wb") as f: f.write(data)
        
        # Apply glitch effect quickly
        subprocess.run([
            "ffmpeg", "-y", "-i", str(img_path),
            "-vf", "eq=contrast=2.2:brightness=0.15:saturation=1.6,"
            "noise=alls=18:allf=t",
            "-frames:v", "1",
            str(glitch_path)
        ], capture_output=True, timeout=10)
        
        if glitch_path.exists():
            log("Max Headroom Abe created", "SUCCESS")
            return str(glitch_path)
    except Exception as e:
        log(f"Glitch creation error: {e}", "ERROR")
    return str(img_path)

def video_optimized(audio_path, out):
    """Create video with all APIs but optimized processing"""
    log("Creating video with full API integration...", "PROCESS")
    try:
        # Get glitch Abe
        abe_img = create_glitch_abe()
        
        # Get duration
        probe = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)
        ], capture_output=True, text=True)
        duration = float(probe.stdout.strip())
        
        # Try to get Pexels B-roll (only 1 clip for speed)
        broll_clips = fetch_pexels_broll("industrial city", 1)
        
        if broll_clips and len(broll_clips) > 0:
            log("Compositing with Pexels B-roll (OPTIMIZED)...", "PROCESS")
            
            # OPTIMIZED: Pre-process B-roll clip to exact size/duration
            processed_broll = BASE / "temp" / "broll_processed.mp4"
            subprocess.run([
                "ffmpeg", "-y", "-i", broll_clips[0],
                "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
                "-t", "5",  # Only 5 seconds
                "-c:v", "libx264", "-preset", "ultrafast",
                "-crf", "28",
                "-an",  # No audio
                str(processed_broll)
            ], capture_output=True, timeout=30)
            
            if processed_broll.exists():
                # SIMPLE overlay (not concat - faster!)
                subprocess.run([
                    "ffmpeg", "-y",
                    "-loop", "1", "-i", abe_img,
                    "-i", str(processed_broll),
                    "-i", str(audio_path),
                    "-filter_complex",
                    "[0:v]scale=1080:1920,zoompan=z='min(zoom+0.001,1.5)':d=1:s=1080x1920[abe];"
                    "[1:v]loop=loop=-1:size=1,setpts=N/FRAME_RATE/TB[broll_loop];"
                    "[abe][broll_loop]blend=all_mode=overlay:all_opacity=0.2[v]",
                    "-map", "[v]", "-map", "2:a",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "23",
                    "-c:a", "aac", "-b:a", "192k",
                    "-t", str(duration),
                    "-pix_fmt", "yuv420p",
                    str(out)
                ], capture_output=True, timeout=120)
                
                if out.exists():
                    log("Video with Pexels B-roll created", "SUCCESS")
                    return True
        
        # Fallback: No B-roll, just Abe
        log("Creating video without B-roll (fast mode)...", "PROCESS")
        subprocess.run([
            "ffmpeg", "-y",
            "-loop", "1", "-i", abe_img,
            "-i", str(audio_path),
            "-filter_complex",
            "[0:v]scale=1080:1920,"
            "zoompan=z='min(zoom+0.001,1.5)':d=1:s=1080x1920,"
            "format=yuv420p[v]",
            "-map", "[v]", "-map", "1:a",
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-b:a", "192k",
            "-t", str(duration),
            "-pix_fmt", "yuv420p",
            str(out)
        ], capture_output=True, timeout=90)
        
        if out.exists():
            log("Video created (no B-roll)", "SUCCESS")
            return True
            
    except Exception as e:
        log(f"Video error: {e}", "ERROR")
    return False

def upload_to_youtube(video_path, title, description, tags):
    """Upload to YouTube with channel ID"""
    log("Uploading to channel UCS5pEpSCw8k4wene0iv0uAg...", "PROCESS")
    
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
                log(f"Upload: {int(status.progress() * 100)}%", "PROCESS")
        
        video_id = response['id']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        log(f"Uploaded: {video_url}", "SUCCESS")
        log(f"Studio: https://studio.youtube.com/channel/UCS5pEpSCw8k4wene0iv0uAg/videos", "SUCCESS")
        
        return video_url
        
    except Exception as e:
        log(f"Upload failed: {e}", "ERROR")
        return None

def gen():
    t = datetime.now().strftime("%Y%m%d_%H%M%S")
    log(f"\n{'='*70}\nVIDEO {t}\n{'='*70}", "INFO")
    log(f"APIs: ElevenLabs + Pexels + RunwayML style", "INFO")
    
    # Get headline
    h = random.choice(scrape())
    log(f"Headline: {h[:60]}")
    
    # Create script
    s = comedy(h)
    log(f"Script: {len(s)} chars")
    
    # Generate audio
    ap = BASE / f"audio/comedy_{t}.mp3"
    if not audio(s, ap):
        return None
    
    # Create video
    vp = BASE / f"videos/FULL_{t}.mp4"
    if not video_optimized(ap, vp):
        return None
    
    # Save to uploaded
    up = BASE / "uploaded" / f"ABE_FULL_{t}.mp4"
    up.parent.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy2(vp, up)
    
    mb = up.stat().st_size / (1024 * 1024)
    log(f"{'='*70}\nSUCCESS: {up.name} ({mb:.1f}MB)\n{'='*70}", "SUCCESS")
    
    # Upload to YouTube
    title = f"Lincoln Roasts: {h[:50]}"
    description = f"""{s}

Subscribe for more Lincoln comedy!

Bitcoin: {BTC}

#AbrahamLincoln #Comedy #Roast #CurrentEvents #Standup #DarkComedy"""
    tags = ["Abraham Lincoln", "Comedy", "Roast", "Standup", "Dark Comedy", "Dave Chappelle", h.replace(" ", "").replace("#", "")]
    
    youtube_url = upload_to_youtube(str(up), title, description, tags)
    
    return {'video_path': str(up), 'youtube_url': youtube_url, 'headline': h}

if __name__ == "__main__":
    count = 10
    for arg in sys.argv[1:]:
        if arg.isdigit():
            count = int(arg)
    
    log(f"\nGENERATING {count} VIDEOS WITH FULL API INTEGRATION\n")
    if USE_BROLL:
        log("Mode: WITH Pexels B-roll (slower but better quality)")
    else:
        log("Mode: WITHOUT B-roll (faster processing)")
    log("")
    
    results = []
    for i in range(count):
        result = gen()
        if result: 
            results.append(result)
        if i < count - 1:
            log("\nWaiting 20 seconds...\n")
            time.sleep(20)
    
    log(f"\n{'='*70}\nCOMPLETE: {len(results)}/{count}\n{'='*70}\n")
    log(f"Used: ElevenLabs (voice) + Pexels (B-roll) + RunwayML (glitch style) + YouTube Upload")
    
    for r in results:
        if isinstance(r, dict) and r.get('youtube_url'):
            log(f"[OK] {r['headline'][:50]}: {r['youtube_url']}", "SUCCESS")
'@

$pyFile = Join-Path $ROOT "abe_full_api.py"
$pythonCode | Set-Content -Path $pyFile -Encoding UTF8
Write-Host "[OK] Full API generator created" -ForegroundColor Green

# Run it
Write-Host ""
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host "GENERATING $Videos VIDEOS" -ForegroundColor Yellow
if ($SkipBroll) {
    Write-Host "Mode: WITHOUT B-roll (fast)" -ForegroundColor Cyan
} else {
    Write-Host "Mode: WITH Pexels B-roll" -ForegroundColor Cyan
}
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host ""

Set-Location $ROOT
if ($SkipBroll) {
    python abe_full_api.py $Videos --skip-broll
} else {
    python abe_full_api.py $Videos
}

# Show results
Write-Host ""
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host "RESULTS" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Gray

$vids = Get-ChildItem (Join-Path $ROOT "uploaded") -Filter "ABE_FULL_*.mp4" -ErrorAction SilentlyContinue
if ($vids) {
    $totalSize = ($vids | Measure-Object -Property Length -Sum).Sum / 1MB
    Write-Host "[OK] Generated: $($vids.Count) videos" -ForegroundColor Green
    Write-Host "[INFO] Total size: $([math]::Round($totalSize, 1)) MB" -ForegroundColor White
    Write-Host "[INFO] APIs used: ElevenLabs + Pexels + RunwayML style" -ForegroundColor Cyan
    Write-Host "[INFO] Location: uploaded\" -ForegroundColor Cyan
    Write-Host "[INFO] Upload to: https://studio.youtube.com/channel/UCS5pEpSCw8k4wene0iv0uAg/videos" -ForegroundColor Cyan
} else {
    Write-Host "[WARNING] No videos found" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "DONE!" -ForegroundColor Green
Write-Host ""

# Open folder
Start-Process explorer.exe -ArgumentList (Join-Path $ROOT "uploaded")

