# ABRAHAM LINCOLN - VHS TV BROADCAST STYLE
# Max Headroom broadcasting from old staticky TV screen
# VHS tracking errors, scan lines, color bleeding, interference

param([int]$Videos = 50, [int]$StartNumber = 1000)

$ROOT = "F:\AI_Oracle_Root\scarify"

Write-Host ""
Write-Host "ABRAHAM LINCOLN - VHS TV BROADCAST" -ForegroundColor Red
Write-Host "Max Headroom style - Broadcasting from old TV" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host ""

# Create directories
$dirs = @("audio", "videos", "uploaded", "temp", "assets")
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
pip install --quiet requests beautifulsoup4 lxml pillow numpy 2>&1 | Out-Null
Write-Host "[OK] Packages installed" -ForegroundColor Green

# Create VHS broadcast generator
Write-Host ""
Write-Host "[PROCESS] Creating VHS broadcast generator..." -ForegroundColor Cyan

$pythonCode = @'
"""
ABRAHAM LINCOLN - VHS TV BROADCAST
Max Headroom style - Broadcasting from old staticky TV screen
VHS artifacts: tracking errors, scan lines, color bleeding, interference
"""
import os, sys, json, requests, subprocess, random, time
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

ELEVENLABS_KEY = os.getenv("ELEVENLABS_API_KEY", "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa")
BASE = Path("F:/AI_Oracle_Root/scarify")
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
    hl = headline.lower()
    if "trump" in hl: return "Trump's Tariffs Destroying Economy"
    elif "police" in hl: return "Police Strike - No Law"
    elif "education" in hl or "school" in hl: return "Education System Destroyed"
    elif "military" in hl or "draft" in hl: return "Military Draft Activated"
    elif "senate" in hl or "congress" in hl: return "Senate Corruption Exposed"
    else: return "America in Crisis"

def comedy_short(headline):
    hl = headline.lower()
    
    if "trump" in hl:
        return f"""Abraham Lincoln! Six foot four!

{headline}.

AMERICA!

This man got POOR people defending a BILLIONAIRE!

I grew up in a LOG CABIN. Not Trump Tower!

He bankrupted CASINOS. You know how hard that is?

You POOR folks? He wouldn't piss on you if you was on FIRE!

April 14 1865. I died for THIS?

Look in mirrors.

Bitcoin {BTC}"""
    
    return f"""Abraham Lincoln! Honest Abe!

{headline}.

AMERICA! People with POWER doing NOTHING!

I died believing in progress. You're ALL complicit!

Look in mirrors.

Bitcoin {BTC}"""

def audio(text, out):
    log("Generating broadcast voice...", "PROCESS")
    try:
        r = requests.post("https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB",
                         json={
                             "text": text,
                             "model_id": "eleven_multilingual_v2",
                             "voice_settings": {
                                 "stability": 0.5,
                                 "similarity_boost": 0.95,
                                 "style": 0.7
                             }
                         },
                         headers={"xi-api-key": ELEVENLABS_KEY}, timeout=180)
        if r.status_code == 200:
            out.parent.mkdir(parents=True, exist_ok=True)
            with open(out, "wb") as f: f.write(r.content)
            log("Audio OK", "SUCCESS")
            return True
    except Exception as e:
        log(f"Audio error: {e}", "ERROR")
    return False

def create_vhs_abe():
    """Create Max Headroom Abe for VHS TV broadcast"""
    log("Creating VHS broadcast Abe...", "PROCESS")
    try:
        img_path = BASE / "temp" / "lincoln.jpg"
        output_path = BASE / "temp" / "abe_vhs.jpg"
        
        if not img_path.exists():
            img_path.parent.mkdir(exist_ok=True)
            data = requests.get("https://upload.wikimedia.org/wikipedia/commons/a/ab/Abraham_Lincoln_O-77_matte_collodion_print.jpg", timeout=30).content
            with open(img_path, "wb") as f: f.write(data)
        
        # Create VHS broadcast look
        subprocess.run([
            "ffmpeg", "-y", "-i", str(img_path),
            "-vf",
            # VHS color grading: oversaturated, cyan-magenta shift
            "eq=contrast=2.5:brightness=0.15:saturation=2.2,"
            # Color bleeding (VHS characteristic)
            "colorchannelmixer=rr=0.9:rg=0.1:rb=0.0:gr=0.0:gg=0.95:gb=0.15:br=0.0:bg=0.1:bb=1.0,"
            # Add grain/noise (VHS static)
            "noise=alls=40:allf=t+u,"
            # Slight blur (VHS softness)
            "boxblur=1:1",
            "-frames:v", "1",
            str(output_path)
        ], capture_output=True, timeout=15)
        
        if output_path.exists():
            log("VHS Abe created", "SUCCESS")
            return str(output_path)
    except Exception as e:
        log(f"VHS Abe error: {e}", "ERROR")
    return str(img_path)

def create_vhs_broadcast(audio_path, out, episode_num, topic):
    """Create VHS TV broadcast video with all authentic effects"""
    log("Creating VHS TV broadcast...", "PROCESS")
    try:
        abe_img = create_vhs_abe()
        
        # Get duration
        probe = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)
        ], capture_output=True, text=True)
        duration = float(probe.stdout.strip())
        
        # Create VHS broadcast with ALL effects
        subprocess.run([
            "ffmpeg", "-y",
            "-loop", "1", "-i", abe_img,
            "-i", str(audio_path),
            "-filter_complex",
            # Scale to vintage TV resolution first
            "[0:v]scale=720:480,"
            # Then scale up to 1080x1920 (creates pixelation)
            "scale=1080:1920:flags=neighbor,"
            # Slow zoom (Max Headroom style)
            "zoompan=z='min(zoom+0.0008,1.5)':d=1:s=1080x1920,"
            # SCAN LINES (horizontal lines across screen)
            "geq="
            "r='if(mod(Y,4),r(X,Y),r(X,Y)*0.7)':"
            "g='if(mod(Y,4),g(X,Y),g(X,Y)*0.7)':"
            "b='if(mod(Y,4),b(X,Y),b(X,Y)*0.7)',"
            # VHS TRACKING ERRORS (horizontal displacement)
            "geq="
            "r='r(X+2*sin(Y*0.1+T*5),Y)':"
            "g='g(X+2*sin(Y*0.1+T*5),Y)':"
            "b='b(X+2*sin(Y*0.1+T*5),Y)',"
            # RGB SPLIT (chromatic aberration)
            "split=3[r][g][b];"
            "[r]lutrgb=r=255:g=0:b=0,crop=iw-4:ih:4:0[r_split];"
            "[g]lutrgb=r=0:g=255:b=0[g_split];"
            "[b]lutrgb=r=0:g=0:b=255,crop=iw-4:ih:0:0[b_split];"
            "[r_split][g_split]blend=all_mode=addition[rg];"
            "[rg][b_split]blend=all_mode=addition,"
            # VERTICAL HOLD GLITCH (occasional screen roll)
            "geq=r='r(X,Y+2*sin(T*2))':g='g(X,Y+2*sin(T*2))':b='b(X,Y+2*sin(T*2))',"
            # VHS INTERFERENCE (random flicker)
            "noise=alls=15:allf=t,"
            # TV VIGNETTE (darker edges like CRT)
            "vignette=angle=PI/4:mode=backward,"
            # Final format
            "format=yuv420p[v]",
            "-map", "[v]", "-map", "1:a",
            # Add slight audio distortion (VHS audio)
            "-af", "highpass=f=100,lowpass=f=8000,acompressor=threshold=-20dB:ratio=4:attack=5:release=50",
            "-c:v", "libx264", "-preset", "medium", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k",
            "-t", str(duration),
            "-pix_fmt", "yuv420p",
            str(out)
        ], capture_output=True, timeout=180)
        
        if out.exists():
            log("VHS broadcast created", "SUCCESS")
            return True
    except subprocess.TimeoutExpired:
        log("Timeout - trying simpler VHS version...", "ERROR")
        # Fallback: simpler VHS effect
        try:
            subprocess.run([
                "ffmpeg", "-y",
                "-loop", "1", "-i", abe_img,
                "-i", str(audio_path),
                "-filter_complex",
                "[0:v]scale=1080:1920,"
                "zoompan=z='min(zoom+0.0008,1.5)':d=1:s=1080x1920,"
                # Basic scan lines
                "geq=r='if(mod(Y,3),r(X,Y),r(X,Y)*0.6)':g='if(mod(Y,3),g(X,Y),g(X,Y)*0.6)':b='if(mod(Y,3),b(X,Y),b(X,Y)*0.6)',"
                # Noise
                "noise=alls=25:allf=t,"
                "format=yuv420p[v]",
                "-map", "[v]", "-map", "1:a",
                "-c:v", "libx264", "-preset", "fast", "-crf", "25",
                "-c:a", "aac", "-b:a", "128k",
                "-t", str(duration),
                str(out)
            ], capture_output=True, timeout=90)
            
            if out.exists():
                log("Simple VHS created", "SUCCESS")
                return True
        except: pass
    except Exception as e:
        log(f"VHS error: {e}", "ERROR")
    return False

def gen(episode_num):
    t = datetime.now().strftime("%Y%m%d_%H%M%S")
    log(f"\n{'='*70}\nVIDEO #{episode_num} - VHS BROADCAST\n{'='*70}", "INFO")
    
    h = random.choice(scrape())
    log(f"Headline: {h[:60]}")
    
    topic = warning_title(h)
    title = f"Lincoln's WARNING #{episode_num}: {topic} #Shorts #R3"
    log(f"Title: {title}")
    
    s = comedy_short(h)
    log(f"Script: {len(s)} chars")
    
    ap = BASE / f"audio/vhs_{episode_num}.mp3"
    if not audio(s, ap):
        return None
    
    vp = BASE / f"videos/VHS_{episode_num}.mp4"
    if not create_vhs_broadcast(ap, vp, episode_num, topic):
        return None
    
    filename = f"WARNING_{episode_num}_{topic.replace(' ', '_')}_VHS.mp4"
    up = BASE / "uploaded" / filename
    up.parent.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy2(vp, up)
    
    # Save upload info
    info_file = up.with_suffix('.txt')
    with open(info_file, 'w') as f:
        f.write(f"TITLE:\n{title}\n\n")
        f.write(f"DESCRIPTION:\n")
        f.write(f"Abraham Lincoln broadcasts from beyond the grave.\n")
        f.write(f"VHS broadcast intercepted from 1865.\n\n")
        f.write(f"Headline: {h}\n\n")
        f.write(f"HASHTAGS:\n#Shorts #AbrahamLincoln #VHS #MaxHeadroom #Retro")
    
    mb = up.stat().st_size / (1024 * 1024)
    log(f"{'='*70}\nSUCCESS: {filename} ({mb:.1f}MB)\n{'='*70}", "SUCCESS")
    return str(up)

if __name__ == "__main__":
    count = 10
    for arg in sys.argv[1:]:
        if arg.isdigit():
            count = int(arg)
    
    log(f"\nGENERATING {count} VHS BROADCAST VIDEOS\n")
    log("Style: Max Headroom broadcasting from old TV\n")
    log("Effects: Scan lines, tracking errors, RGB split, interference\n")
    
    success = 0
    for i in range(count):
        if gen(START_NUM + i):
            success += 1
        if i < count - 1:
            log("\nWaiting 20 seconds...\n")
            time.sleep(20)
    
    log(f"\n{'='*70}\nCOMPLETE: {success}/{count} VHS BROADCASTS\n{'='*70}\n")
'@

$pyFile = Join-Path $ROOT "abe_vhs_broadcast.py"
$pythonCode | Set-Content -Path $pyFile -Encoding UTF8
Write-Host "[OK] VHS broadcast generator created" -ForegroundColor Green

# Run it
Write-Host ""
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host "GENERATING $Videos VHS BROADCASTS" -ForegroundColor Yellow
Write-Host "Max Headroom style from old TV screen" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host ""

Set-Location $ROOT
python abe_vhs_broadcast.py $Videos --start=$StartNumber

# Show results
Write-Host ""
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host "RESULTS" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Gray

$vids = Get-ChildItem (Join-Path $ROOT "uploaded") -Filter "*_VHS.mp4" -ErrorAction SilentlyContinue
if ($vids) {
    $totalSize = ($vids | Measure-Object -Property Length -Sum).Sum / 1MB
    Write-Host "[OK] Generated: $($vids.Count) VHS broadcasts" -ForegroundColor Green
    Write-Host "[INFO] Total size: $([math]::Round($totalSize, 1)) MB" -ForegroundColor White
    Write-Host "[INFO] Effects: Scan lines, tracking, RGB split, static" -ForegroundColor Cyan
    Write-Host "[INFO] Location: uploaded\" -ForegroundColor Cyan
    Write-Host "[INFO] Upload to: https://studio.youtube.com/channel/UCS5pEpSCw8k4wene0iv0uAg/videos" -ForegroundColor Cyan
} else {
    Write-Host "[WARNING] No videos found" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "DONE!" -ForegroundColor Green
Write-Host ""

Start-Process explorer.exe -ArgumentList (Join-Path $ROOT "uploaded")
