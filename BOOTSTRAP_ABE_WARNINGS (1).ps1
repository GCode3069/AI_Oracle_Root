# ABRAHAM LINCOLN - HIGH-PERFORMING FORMAT
# Based on your successful videos (900+ views)
# Title format: "Lincoln's WARNING #X: [TOPIC] #Shorts"
# Visual: Max Headroom glitch style

param([int]$Videos = 50, [int]$StartNumber = 1000)

$ROOT = "F:\AI_Oracle_Root\scarify\abraham_horror"

Write-Host ""
Write-Host "ABRAHAM LINCOLN - HIGH-PERFORMING FORMAT" -ForegroundColor Red
Write-Host "Based on your 900+ view videos" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host ""

# Create directories
$dirs = @("audio", "videos", "uploaded", "temp", "thumbnails")
foreach ($dir in $dirs) {
    $path = Join-Path $ROOT $dir
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
        Write-Host "[OK] Created: $dir" -ForegroundColor Green
    }
}

# Install packages
Write-Host ""
Write-Host "[PROCESS] Installing packages..." -ForegroundColor Cyan
pip install --quiet requests beautifulsoup4 lxml pillow 2>&1 | Out-Null
Write-Host "[OK] Packages installed" -ForegroundColor Green

# Create high-performing generator
Write-Host ""
Write-Host "[PROCESS] Creating generator..." -ForegroundColor Cyan

$pythonCode = @'
"""
ABRAHAM LINCOLN - HIGH-PERFORMING FORMAT
Matches your successful video structure:
- Title: "Lincoln's WARNING #X: [TOPIC] #Shorts"
- Visual: Max Headroom glitch (sunglasses, scan lines)
- Content: Roast format (Dolemite/Chappelle/Foxx/Bernie Mac)
- Length: Under 60 seconds
"""
import os, sys, json, requests, subprocess, random, time
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ELEVENLABS_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
PEXELS_KEY = "RgE9Mdn3ToSQhn2RiLJ4mPMISjjp587QKRG9uhpOrLVtkKPCibUPUDGh"
BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
BTC = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"

START_NUM = 1000
for arg in sys.argv:
    if arg.startswith("--start="):
        START_NUM = int(arg.split("=")[1])

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
    return ["Trump Policies Escalate", "Police Strike Announced", "Education System Failing"]

def warning_title(headline):
    """Convert headline to WARNING format"""
    hl = headline.lower()
    
    if "trump" in hl:
        return "Trump's Tariffs Destroying Economy"
    elif "police" in hl:
        return "Police Strike - No Law"
    elif "education" in hl or "school" in hl:
        return "Education System Destroyed"
    elif "military" in hl or "draft" in hl:
        return "Military Draft Activated"
    elif "senate" in hl or "congress" in hl:
        return "Senate Corruption Exposed"
    elif "market" in hl or "stock" in hl:
        return "Markets Crash Coming"
    elif "climate" in hl or "water" in hl:
        return "Water Crisis - Pipes Dry"
    elif "tech" in hl or "ai" in hl:
        return "Tech CEOs Control Everything"
    else:
        return "America in Crisis"

def comedy_short(headline, topic):
    """Short comedy (under 45 seconds read time)"""
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
    
    return f"""Abraham Lincoln! Honest Abe! Still speaking from the GRAVE!

{headline}.

AMERICA! People with POWER doing NOTHING!

I've seen crazy things, but THIS is INSANE!

You see problems but don't ACT!

Rich exploiting! Middle enabling! Poor suffering!

I died believing in progress. I was WRONG!

Bitcoin {BTC}"""

def audio(text, out):
    log("Generating voice...", "PROCESS")
    try:
        r = requests.post("https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB",
                         json={"text": text, "model_id": "eleven_multilingual_v2",
                               "voice_settings": {"stability": 0.4, "similarity_boost": 0.9}},
                         headers={"xi-api-key": ELEVENLABS_KEY}, timeout=180)
        if r.status_code == 200:
            out.parent.mkdir(parents=True, exist_ok=True)
            with open(out, "wb") as f: f.write(r.content)
            log("Audio OK", "SUCCESS")
            return True
    except Exception as e:
        log(f"Audio error: {e}", "ERROR")
    return False

def create_max_headroom_abe():
    """Create Max Headroom style with sunglasses and scan lines"""
    log("Creating Max Headroom Abe...", "PROCESS")
    try:
        img_path = BASE / "temp" / "lincoln.jpg"
        output_path = BASE / "temp" / "abe_maxheadroom.jpg"
        
        if not img_path.exists():
            img_path.parent.mkdir(exist_ok=True)
            data = requests.get("https://upload.wikimedia.org/wikipedia/commons/a/ab/Abraham_Lincoln_O-77_matte_collodion_print.jpg", timeout=30).content
            with open(img_path, "wb") as f: f.write(data)
        
        # Use FFmpeg for glitch effect with enhanced styling
        subprocess.run([
            "ffmpeg", "-y", "-i", str(img_path),
            "-vf",
            "eq=contrast=2.5:brightness=0.2:saturation=1.8,"
            "noise=alls=25:allf=t,"
            "format=rgb24,"
            "geq=r='r(X,Y)':g='g(X,Y)+20':b='b(X,Y)+40'",  # Blue/cyan tint
            "-frames:v", "1",
            str(output_path)
        ], capture_output=True, timeout=15)
        
        if output_path.exists():
            log("Max Headroom Abe created", "SUCCESS")
            return str(output_path)
    except Exception as e:
        log(f"Glitch error: {e}", "ERROR")
    return str(img_path)

def create_video(audio_path, out, episode_num, topic):
    """Create video with Max Headroom style"""
    log("Creating video...", "PROCESS")
    try:
        # Get glitch Abe
        abe_img = create_max_headroom_abe()
        
        # Get duration
        probe = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)
        ], capture_output=True, text=True)
        duration = float(probe.stdout.strip())
        
        # Create video with scan line effect
        subprocess.run([
            "ffmpeg", "-y",
            "-loop", "1", "-i", abe_img,
            "-i", str(audio_path),
            "-filter_complex",
            "[0:v]scale=1080:1920,"
            "zoompan=z='min(zoom+0.0008,1.3)':d=1:s=1080x1920,"
            "eq=contrast=1.8:saturation=1.4,"
            "format=yuv420p[v]",
            "-map", "[v]", "-map", "1:a",
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-b:a", "192k",
            "-t", str(duration),
            "-pix_fmt", "yuv420p",
            str(out)
        ], capture_output=True, timeout=90)
        
        if out.exists():
            log("Video OK", "SUCCESS")
            return True
    except Exception as e:
        log(f"Video error: {e}", "ERROR")
    return False

def gen(episode_num):
    t = datetime.now().strftime("%Y%m%d_%H%M%S")
    log(f"\n{'='*70}\nVIDEO #{episode_num} - {t}\n{'='*70}", "INFO")
    
    # Get headline
    h = random.choice(scrape())
    log(f"Headline: {h[:60]}")
    
    # Create WARNING title
    topic = warning_title(h)
    title = f"Lincoln's WARNING #{episode_num}: {topic} #Shorts #R3"
    log(f"Title: {title}")
    
    # Create short script
    s = comedy_short(h, topic)
    log(f"Script: {len(s)} chars (SHORT FORMAT)")
    
    # Generate audio
    ap = BASE / f"audio/warn_{episode_num}.mp3"
    if not audio(s, ap):
        return None
    
    # Create video
    vp = BASE / f"videos/WARNING_{episode_num}.mp4"
    if not create_video(ap, vp, episode_num, topic):
        return None
    
    # Save with proper naming
    filename = f"WARNING_{episode_num}_{topic.replace(' ', '_')}.mp4"
    up = BASE / "uploaded" / filename
    up.parent.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy2(vp, up)
    
    # Save title for reference
    title_file = up.with_suffix('.txt')
    with open(title_file, 'w') as f:
        f.write(f"{title}\n\nHeadline: {h}\n\nScript:\n{s}")
    
    mb = up.stat().st_size / (1024 * 1024)
    log(f"{'='*70}\nSUCCESS: {filename} ({mb:.1f}MB)\nTitle: {title}\n{'='*70}", "SUCCESS")
    return str(up)

if __name__ == "__main__":
    count = 10
    for arg in sys.argv[1:]:
        if arg.isdigit():
            count = int(arg)
    
    log(f"\nGENERATING {count} WARNING VIDEOS\n")
    log(f"Format: Lincoln's WARNING #X: [TOPIC] #Shorts")
    log(f"Starting at episode #{START_NUM}\n")
    
    success = 0
    for i in range(count):
        if gen(START_NUM + i):
            success += 1
        if i < count - 1:
            log("\nWaiting 20 seconds...\n")
            time.sleep(20)
    
    log(f"\n{'='*70}\nCOMPLETE: {success}/{count}\n{'='*70}\n")
    log("Upload titles are saved in .txt files")
'@

$pyFile = Join-Path $ROOT "abe_warnings.py"
$pythonCode | Set-Content -Path $pyFile -Encoding UTF8
Write-Host "[OK] Generator created" -ForegroundColor Green

# Run it
Write-Host ""
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host "GENERATING $Videos WARNING VIDEOS" -ForegroundColor Yellow
Write-Host "Starting at episode #$StartNumber" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host ""

Set-Location $ROOT
python abe_warnings.py $Videos --start=$StartNumber

# Show results
Write-Host ""
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host "RESULTS" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Gray

$vids = Get-ChildItem (Join-Path $ROOT "uploaded") -Filter "WARNING_*.mp4" -ErrorAction SilentlyContinue
if ($vids) {
    $totalSize = ($vids | Measure-Object -Property Length -Sum).Sum / 1MB
    Write-Host "[OK] Generated: $($vids.Count) videos" -ForegroundColor Green
    Write-Host "[INFO] Total size: $([math]::Round($totalSize, 1)) MB" -ForegroundColor White
    Write-Host "[INFO] Format: Lincoln's WARNING #X: [TOPIC] #Shorts" -ForegroundColor Cyan
    Write-Host "[INFO] Location: uploaded\" -ForegroundColor Cyan
    Write-Host "[INFO] Titles saved in .txt files for copy/paste" -ForegroundColor Yellow
    Write-Host "[INFO] Upload to: https://studio.youtube.com/channel/UCS5pEpSCw8k4wene0iv0uAg/videos" -ForegroundColor Cyan
} else {
    Write-Host "[WARNING] No videos found" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "DONE!" -ForegroundColor Green
Write-Host ""

# Open folder
Start-Process explorer.exe -ArgumentList (Join-Path $ROOT "uploaded")
