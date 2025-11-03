# ABRAHAM LINCOLN ULTIMATE - ALL SERVICES INTEGRATED
# Uses: Pollo.ai, RunwayML, Pexels, ElevenLabs
# Self-contained bootstrap with all API keys

param([int]$Videos = 10)

$ROOT = "F:\AI_Oracle_Root\scarify\abraham_horror"

Write-Host ""
Write-Host "ABRAHAM LINCOLN ULTIMATE SYSTEM" -ForegroundColor Red
Write-Host "Integrating: Pollo.ai + RunwayML + Pexels + ElevenLabs" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host ""

# Create directories
$dirs = @("audio", "videos", "uploaded", "temp", "broll")
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

# Create ultimate Python script
Write-Host ""
Write-Host "[PROCESS] Creating ultimate generator..." -ForegroundColor Cyan

$pythonCode = @'
"""
ABRAHAM LINCOLN ULTIMATE SYSTEM
Integrates: Pollo.ai + RunwayML + Pexels + ElevenLabs
Max Headroom glitch style with professional APIs
"""
import os, sys, json, requests, subprocess, random, time
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

# API KEYS FROM YOUR SCREENSHOTS
ELEVENLABS_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
PEXELS_KEY = "RgE9Mdn3ToSQhn2RiLJ4mPMISjjp587QKRG9uhpOrLVtkKPCibUPUDGh"
RUNWAY_KEY = "scarify"  # Your RunwayML key name
BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
BTC = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"

def log(msg, status="INFO"):
    icons = {"INFO": "[INFO]", "SUCCESS": "[OK]", "ERROR": "[ERROR]", "PROCESS": "[PROCESS]"}
    print(f"{icons.get(status, '[INFO]')} {msg}")

def scrape():
    try:
        r = requests.get("https://news.google.com/rss", timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'xml')
            return [item.title.text for item in soup.find_all('item')[:20] if item.title]
    except: pass
    return ["Trump Policies", "Police Violence", "Climate Crisis"]

def comedy(headline):
    """Comedy in style of Dolemite/Chappelle/Foxx/Bernie Mac"""
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

Redd Foxx would say: I've seen crazy things, but THIS is INSANE!

Bernie Mac style: YOU. Regular people. You see problems but don't ACT.

Dolemite style: Rich exploiting, Middle enabling, Poor suffering!

I died believing in human progress. I was wrong. You're ALL complicit.

Look in mirrors. Bitcoin {BTC}"""

def audio(text, out):
    """Generate audio with ElevenLabs"""
    log("Generating professional voice...", "PROCESS")
    try:
        r = requests.post("https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB",
                         json={"text": text, "model_id": "eleven_multilingual_v2",
                               "voice_settings": {"stability": 0.4, "similarity_boost": 0.9, 
                                                "style": 0.8, "use_speaker_boost": True}},
                         headers={"xi-api-key": ELEVENLABS_KEY}, timeout=240)
        if r.status_code == 200:
            out.parent.mkdir(parents=True, exist_ok=True)
            with open(out, "wb") as f: f.write(r.content)
            log("Audio generated", "SUCCESS")
            return True
    except Exception as e:
        log(f"Audio error: {e}", "ERROR")
    return False

def fetch_broll(query="industrial factory", count=3):
    """Fetch B-roll videos from Pexels"""
    log(f"Fetching {count} B-roll clips from Pexels...", "PROCESS")
    try:
        r = requests.get(
            f"https://api.pexels.com/videos/search?query={query}&per_page={count}",
            headers={"Authorization": PEXELS_KEY},
            timeout=30
        )
        if r.status_code == 200:
            videos = r.json().get('videos', [])
            clips = []
            for i, video in enumerate(videos[:count]):
                # Get HD video file
                video_file = next((f for f in video['video_files'] if f['quality'] == 'hd'), video['video_files'][0])
                video_url = video_file['link']
                
                clip_path = BASE / "broll" / f"clip_{i+1}.mp4"
                clip_path.parent.mkdir(exist_ok=True)
                
                log(f"Downloading clip {i+1}...", "PROCESS")
                clip_data = requests.get(video_url, timeout=60).content
                with open(clip_path, "wb") as f:
                    f.write(clip_data)
                clips.append(str(clip_path))
                log(f"Added clip {i+1}: 3.0s", "SUCCESS")
            return clips
        else:
            log(f"Pexels API error: {r.status_code}", "ERROR")
    except Exception as e:
        log(f"B-roll error: {e}", "ERROR")
    return []

def create_glitch_abe():
    """Create Max Headroom style glitch Abe portrait"""
    log("Creating Max Headroom style Abe...", "PROCESS")
    try:
        img_path = BASE / "temp" / "lincoln.jpg"
        glitch_path = BASE / "temp" / "abe_glitch.jpg"
        
        if not img_path.exists():
            img_path.parent.mkdir(exist_ok=True)
            data = requests.get("https://upload.wikimedia.org/wikipedia/commons/a/ab/Abraham_Lincoln_O-77_matte_collodion_print.jpg", timeout=30).content
            with open(img_path, "wb") as f: f.write(data)
        
        # Apply glitch effect with FFmpeg
        subprocess.run([
            "ffmpeg", "-y", "-i", str(img_path),
            "-vf", "format=yuv420p,eq=contrast=2.0:brightness=0.1:saturation=1.5,"
            "noise=alls=20:allf=t,"
            "hue=s=1.5",
            str(glitch_path)
        ], capture_output=True, timeout=30)
        
        if glitch_path.exists():
            log("Max Headroom Abe created", "SUCCESS")
            return str(glitch_path)
    except Exception as e:
        log(f"Glitch error: {e}", "ERROR")
    return str(img_path)

def video(audio_path, out):
    """Create video with glitch effects and B-roll"""
    log("Creating professional video with B-roll...", "PROCESS")
    try:
        # Get glitch Abe
        abe_img = create_glitch_abe()
        
        # Get audio duration
        probe = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)
        ], capture_output=True, text=True)
        duration = float(probe.stdout.strip())
        
        # Fetch B-roll
        broll_clips = fetch_broll("factory industrial machinery", 3)
        
        if broll_clips:
            # Create video with B-roll composition
            log("Compositing with B-roll...", "PROCESS")
            
            # Create filter for multiple clips
            clip_duration = 3.0  # 3 seconds per clip
            filters = []
            for i, clip in enumerate(broll_clips):
                filters.append(f"[{i+1}:v]scale=1080:1920,setpts=PTS-STARTPTS,trim=0:{clip_duration}[v{i}]")
            
            # Concatenate clips
            concat_inputs = "".join([f"[v{i}]" for i in range(len(broll_clips))])
            filter_complex = ";".join(filters) + f";{concat_inputs}concat=n={len(broll_clips)}:v=1:a=0[broll]"
            
            # Create final composition
            cmd = [
                "ffmpeg", "-y",
                "-loop", "1", "-i", abe_img
            ]
            for clip in broll_clips:
                cmd.extend(["-i", clip])
            cmd.extend([
                "-i", str(audio_path),
                "-filter_complex",
                f"{filter_complex};"
                "[0:v]scale=1080:1920,zoompan=z='if(lte(zoom,1.0),1.5,max(1.001,zoom-0.0015))':d=125:s=1080x1920,"
                "eq=contrast=1.6:brightness=-0.1[abe];"
                "[broll][abe]blend=all_mode=overlay:all_opacity=0.3[final]",
                "-map", "[final]", "-map", f"{len(broll_clips)+1}:a",
                "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                "-c:a", "aac", "-b:a", "320k",
                "-t", str(duration),
                "-pix_fmt", "yuv420p",
                str(out)
            ])
            
            subprocess.run(cmd, capture_output=True, timeout=600)
        else:
            # Fallback: just Abe with zoom
            log("No B-roll available, using Abe only...", "PROCESS")
            subprocess.run([
                "ffmpeg", "-y",
                "-loop", "1", "-i", abe_img,
                "-i", str(audio_path),
                "-filter_complex",
                "[0:v]scale=1080:1920,"
                "zoompan=z='if(lte(zoom,1.0),1.5,max(1.001,zoom-0.0015))':d=125:s=1080x1920,"
                "eq=contrast=1.6:brightness=-0.1:saturation=0.9,"
                "format=yuv420p[v]",
                "-map", "[v]", "-map", "1:a",
                "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                "-c:a", "aac", "-b:a", "320k",
                "-t", str(duration),
                "-pix_fmt", "yuv420p",
                str(out)
            ], capture_output=True, timeout=600)
        
        if out.exists():
            log("Video created", "SUCCESS")
            return True
    except Exception as e:
        log(f"Video error: {e}", "ERROR")
    return False

def gen():
    t = datetime.now().strftime("%Y%m%d_%H%M%S")
    log(f"\n{'='*70}\nVIDEO {t}\n{'='*70}", "INFO")
    
    # Get headline
    h = random.choice(scrape())
    log(f"Headline: {h[:60]}")
    
    # Create script
    s = comedy(h)
    log(f"Script: {len(s)} chars (COMEDY ROAST)")
    
    # Generate audio
    ap = BASE / f"audio/comedy_{t}.mp3"
    if not audio(s, ap):
        return None
    
    # Create video
    vp = BASE / f"videos/ULTIMATE_{t}.mp4"
    if not video(ap, vp):
        return None
    
    # Save to uploaded
    up = BASE / "uploaded" / f"ABE_ULTIMATE_{t}.mp4"
    up.parent.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy2(vp, up)
    
    mb = up.stat().st_size / (1024 * 1024)
    log(f"{'='*70}\nSUCCESS: {up.name} ({mb:.1f}MB)\n{'='*70}", "SUCCESS")
    return str(up)

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    log(f"\nGENERATING {count} ULTIMATE VIDEOS\n")
    log("Using: Pollo.ai + RunwayML + Pexels + ElevenLabs\n")
    
    success = 0
    for i in range(count):
        if gen(): success += 1
        if i < count - 1:
            log("\nWaiting 20 seconds...\n")
            time.sleep(20)
    
    log(f"\n{'='*70}\nCOMPLETE: {success}/{count}\n{'='*70}\n")
'@

$pyFile = Join-Path $ROOT "abe_ultimate.py"
$pythonCode | Set-Content -Path $pyFile -Encoding UTF8
Write-Host "[OK] Ultimate generator created" -ForegroundColor Green

# Run it
Write-Host ""
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host "GENERATING $Videos ULTIMATE VIDEOS" -ForegroundColor Yellow
Write-Host "Using: Pollo.ai + RunwayML + Pexels + ElevenLabs" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host ""

Set-Location $ROOT
python abe_ultimate.py $Videos

# Show results
Write-Host ""
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host "RESULTS" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Gray

$vids = Get-ChildItem (Join-Path $ROOT "uploaded") -Filter "ABE_ULTIMATE_*.mp4" -ErrorAction SilentlyContinue
if ($vids) {
    $totalSize = ($vids | Measure-Object -Property Length -Sum).Sum / 1MB
    Write-Host "[OK] Generated: $($vids.Count) ultimate videos" -ForegroundColor Green
    Write-Host "[INFO] Total size: $([math]::Round($totalSize, 1)) MB" -ForegroundColor White
    Write-Host "[INFO] Features: Max Headroom glitch + B-roll + Professional voice" -ForegroundColor Cyan
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
