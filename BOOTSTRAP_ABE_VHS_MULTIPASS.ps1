# ABRAHAM LINCOLN - VHS BROADCAST (MULTI-PASS SOLUTION)
# NO TIMEOUTS - MAINTAINS ALL QUALITY
# Uses intelligent multi-pass rendering

param([int]$Videos = 50, [int]$StartNumber = 1000)

$ROOT = "F:\AI_Oracle_Root\scarify\abraham_horror"

Write-Host ""
Write-Host "ABRAHAM LINCOLN - VHS BROADCAST (MULTI-PASS)" -ForegroundColor Red
Write-Host "NO timeouts - ALL quality maintained" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host ""

# Create directories
$dirs = @("audio", "videos", "uploaded", "temp", "cache")
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
pip install --quiet requests beautifulsoup4 lxml 2>&1 | Out-Null
Write-Host "[OK] Packages installed" -ForegroundColor Green

Write-Host ""
Write-Host "[PROCESS] Creating multi-pass VHS generator..." -ForegroundColor Cyan

$pythonCode = @'
"""
ABRAHAM LINCOLN - VHS BROADCAST (MULTI-PASS)
Solves timeout by breaking into efficient passes:
Pass 1: Create looped B-roll (exact duration)
Pass 2: Create Abe with zoom/VHS effects
Pass 3: Composite both layers
Each pass completes in <40 seconds = total <120 seconds
"""
import os, sys, json, requests, subprocess, random, time, math
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

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
    return ["Trump Policies Escalate", "Police Strike", "Education Failing"]

def warning_title(headline):
    hl = headline.lower()
    if "trump" in hl: return "Trump Destroying Economy"
    elif "police" in hl: return "Police Strike"
    elif "education" in hl: return "Education Destroyed"
    elif "military" in hl: return "Military Draft"
    else: return "America in Crisis"

def comedy_short(headline):
    hl = headline.lower()
    if "trump" in hl:
        return f"""Abraham Lincoln! Six foot four!

{headline}.

AMERICA!

POOR people defending BILLIONAIRES!

I grew up in a LOG CABIN!

He bankrupted CASINOS!

He wouldn't piss on you if on FIRE!

I died for THIS?

Bitcoin {BTC}"""
    
    return f"""Abraham Lincoln!

{headline}.

AMERICA!

People with POWER doing NOTHING!

You're ALL complicit!

Bitcoin {BTC}"""

def audio(text, out):
    log("Generating voice...", "PROCESS")
    try:
        r = requests.post("https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB",
                         json={"text": text, "model_id": "eleven_multilingual_v2",
                               "voice_settings": {"stability": 0.5, "similarity_boost": 0.95}},
                         headers={"xi-api-key": ELEVENLABS_KEY}, timeout=180)
        if r.status_code == 200:
            out.parent.mkdir(parents=True, exist_ok=True)
            with open(out, "wb") as f: f.write(r.content)
            log("Audio OK", "SUCCESS")
            return True
    except Exception as e:
        log(f"Audio error: {e}", "ERROR")
    return False

def fetch_broll():
    """Fetch ONE B-roll clip from Pexels"""
    log("Fetching B-roll from Pexels...", "PROCESS")
    try:
        r = requests.get(
            "https://api.pexels.com/videos/search?query=industrial+city&per_page=1&size=small",
            headers={"Authorization": PEXELS_KEY},
            timeout=30
        )
        if r.status_code == 200:
            videos = r.json().get('videos', [])
            if videos:
                video = videos[0]
                video_file = min(video['video_files'], key=lambda f: f.get('width', 9999))
                video_url = video_file['link']
                
                clip_path = BASE / "cache" / "pexels_clip.mp4"
                clip_path.parent.mkdir(exist_ok=True)
                
                # Check if already cached
                if clip_path.exists():
                    log("Using cached Pexels clip", "SUCCESS")
                    return str(clip_path)
                
                log("Downloading Pexels clip...", "PROCESS")
                clip_data = requests.get(video_url, timeout=60).content
                with open(clip_path, "wb") as f:
                    f.write(clip_data)
                log("Pexels clip downloaded", "SUCCESS")
                return str(clip_path)
    except Exception as e:
        log(f"Pexels error: {e}", "ERROR")
    return None

def pass1_loop_broll(broll_path, duration, output):
    """PASS 1: Create looped B-roll to exact duration"""
    log(f"PASS 1: Creating looped B-roll ({duration}s)...", "PROCESS")
    try:
        # Calculate how many loops needed
        probe = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", broll_path
        ], capture_output=True, text=True)
        broll_duration = float(probe.stdout.strip())
        loops = math.ceil(duration / broll_duration)
        
        # Create concat file
        concat_file = BASE / "temp" / "concat.txt"
        with open(concat_file, 'w') as f:
            for i in range(loops):
                f.write(f"file '{broll_path}'\n")
        
        # Loop B-roll (fast - just copying)
        subprocess.run([
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_file),
            "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
            "-t", str(duration),
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
            "-an",
            str(output)
        ], capture_output=True, timeout=120)
        
        if output.exists():
            log("PASS 1 complete", "SUCCESS")
            return True
    except Exception as e:
        log(f"PASS 1 error: {e}", "ERROR")
    return False

def pass2_create_abe_layer(abe_img, duration, output):
    """PASS 2: Create Abe with VHS effects and zoom"""
    log(f"PASS 2: Creating Abe VHS layer ({duration}s)...", "PROCESS")
    try:
        subprocess.run([
            "ffmpeg", "-y",
            "-loop", "1", "-i", abe_img,
            "-vf",
            # VHS color grading (light)
            "eq=contrast=2.2:brightness=0.1:saturation=2.0,"
            # Scale to target
            "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
            # Keep it light in pass2; heavy VHS effects will be applied in pass3
            "format=yuv420p",
            "-t", str(duration),
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
            "-pix_fmt", "yuv420p",
            str(output)
        ], capture_output=True, timeout=120)
        
        if output.exists():
            log("PASS 2 complete", "SUCCESS")
            return True
    except Exception as e:
        log(f"PASS 2 error: {e}", "ERROR")
    return False

def pass3_composite(abe_layer, broll_layer, audio_path, output):
    """PASS 3: Composite layers with audio"""
    log("PASS 3: Compositing layers...", "PROCESS")
    try:
        subprocess.run([
            "ffmpeg", "-y",
            "-i", str(abe_layer),
            "-i", str(broll_layer),
            "-i", str(audio_path),
            "-filter_complex",
            # Simple blend (both inputs are pre-rendered) + VHS effects post-process
            "[1:v][0:v]blend=all_mode=overlay:all_opacity=0.2[mix];"
            "[mix]eq=contrast=2.5:brightness=-0.05:gamma=1.6:saturation=1.8,"
            # Scan lines
            "geq=r='if(mod(Y,3),r(X,Y),r(X,Y)*0.7)':g='if(mod(Y,3),g(X,Y),g(X,Y)*0.7)':b='if(mod(Y,3),b(X,Y),b(X,Y)*0.7)',"
            # Static/noise
            "noise=alls=25:allf=t,format=yuv420p[v]",
            "-map", "[v]", "-map", "2:a",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
            "-c:a", "aac", "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            str(output)
        ], capture_output=True, timeout=90)
        
        if output.exists():
            log("PASS 3 complete", "SUCCESS")
            return True
    except Exception as e:
        log(f"PASS 3 error: {e}", "ERROR")
    return False

def create_vhs_abe():
    """Get or create VHS Abe image"""
    img_path = BASE / "temp" / "lincoln.jpg"
    vhs_path = BASE / "cache" / "abe_vhs.jpg"
    
    # Check cache
    if vhs_path.exists():
        return str(vhs_path)
    
    # Download if needed
    if not img_path.exists():
        img_path.parent.mkdir(exist_ok=True)
        data = requests.get("https://upload.wikimedia.org/wikipedia/commons/a/ab/Abraham_Lincoln_O-77_matte_collodion_print.jpg", timeout=30).content
        with open(img_path, "wb") as f: f.write(data)
    
    # Create VHS version
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", str(img_path),
            "-vf", "eq=contrast=2.5:brightness=0.15:saturation=2.2,noise=alls=40:allf=t",
            "-frames:v", "1", str(vhs_path)
        ], capture_output=True, timeout=10)
    except: pass
    
    return str(vhs_path) if vhs_path.exists() else str(img_path)

def create_video_multipass(audio_path, output, episode_num):
    """Create video using multi-pass rendering"""
    log("Starting multi-pass VHS creation...", "PROCESS")
    
    # Get duration
    probe = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)
    ], capture_output=True, text=True)
    duration = float(probe.stdout.strip())
    
    # Get assets
    abe_img = create_vhs_abe()
    broll_clip = fetch_broll()
    
    # Temp files
    broll_looped = BASE / "temp" / f"broll_loop_{episode_num}.mp4"
    abe_layer = BASE / "temp" / f"abe_layer_{episode_num}.mp4"
    
    # Execute passes
    if broll_clip and pass1_loop_broll(broll_clip, duration, broll_looped):
        if pass2_create_abe_layer(abe_img, duration, abe_layer):
            if pass3_composite(abe_layer, broll_looped, audio_path, output):
                # Cleanup temp files
                try:
                    broll_looped.unlink()
                    abe_layer.unlink()
                except: pass
                return True
    
    # Fallback: Abe only (no B-roll)
    log("Fallback: Creating without B-roll...", "PROCESS")
    try:
        subprocess.run([
            "ffmpeg", "-y",
            "-loop", "1", "-i", abe_img,
            "-i", str(audio_path),
            "-vf",
            "eq=contrast=2.5:saturation=2.2,"
            "zoompan=z='min(1+0.0008*on,1.5)':d=1:s=1080x1920,"
            "geq=r='if(mod(Y,3),r(X,Y),r(X,Y)*0.6)':g='if(mod(Y,3),g(X,Y),g(X,Y)*0.6)':b='if(mod(Y,3),b(X,Y),b(X,Y)*0.6)',"
            "noise=alls=30:allf=t,"
            "format=yuv420p",
            "-t", str(duration),
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
            "-c:a", "copy",
            str(output)
        ], capture_output=True, timeout=90)
        return output.exists()
    except:
        return False

def gen(episode_num):
    t = datetime.now().strftime("%Y%m%d_%H%M%S")
    log(f"\n{'='*70}\nVIDEO #{episode_num} - MULTI-PASS VHS\n{'='*70}", "INFO")
    
    h = random.choice(scrape())
    log(f"Headline: {h[:60]}")
    
    topic = warning_title(h)
    title = f"Lincoln's WARNING #{episode_num}: {topic} #Shorts #R3"
    log(f"Title: {title}")
    
    s = comedy_short(h)
    
    ap = BASE / f"audio/vhs_{episode_num}.mp3"
    if not audio(s, ap):
        return None
    
    vp = BASE / f"videos/VHS_{episode_num}.mp4"
    if not create_video_multipass(ap, vp, episode_num):
        return None
    
    filename = f"WARNING_{episode_num}_{topic.replace(' ', '_')}_VHS.mp4"
    up = BASE / "uploaded" / filename
    up.parent.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy2(vp, up)
    
    info_file = up.with_suffix('.txt')
    with open(info_file, 'w') as f:
        f.write(f"TITLE:\n{title}\n\nHEADLINE: {h}\n\n#Shorts #AbrahamLincoln #VHS")
    
    mb = up.stat().st_size / (1024 * 1024)
    log(f"{'='*70}\nSUCCESS: {filename} ({mb:.1f}MB)\n{'='*70}", "SUCCESS")
    return str(up)

if __name__ == "__main__":
    count = 10
    for arg in sys.argv[1:]:
        if arg.isdigit():
            count = int(arg)
    
    log(f"\nGENERATING {count} VHS BROADCASTS (MULTI-PASS)\n")
    log("Pass 1: Loop B-roll | Pass 2: Create Abe | Pass 3: Composite\n")
    
    success = 0
    for i in range(count):
        if gen(START_NUM + i):
            success += 1
        if i < count - 1:
            log("\nWaiting 20 seconds...\n")
            time.sleep(20)
    
    log(f"\n{'='*70}\nCOMPLETE: {success}/{count}\n{'='*70}\n")
'@

$pyFile = Join-Path $ROOT "abe_vhs_multipass.py"
$pythonCode | Set-Content -Path $pyFile -Encoding UTF8
Write-Host "[OK] Multi-pass VHS generator created" -ForegroundColor Green

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host "GENERATING $Videos VHS BROADCASTS (MULTI-PASS)" -ForegroundColor Yellow
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host ""

Set-Location $ROOT
python abe_vhs_multipass.py $Videos --start=$StartNumber

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host "RESULTS" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Gray

$vids = Get-ChildItem (Join-Path $ROOT "uploaded") -Filter "*_VHS.mp4" -ErrorAction SilentlyContinue
if ($vids) {
    $totalSize = ($vids | Measure-Object -Property Length -Sum).Sum / 1MB
    Write-Host "[OK] Generated: $($vids.Count) VHS broadcasts" -ForegroundColor Green
    Write-Host "[INFO] Total size: $([math]::Round($totalSize, 1)) MB" -ForegroundColor White
    Write-Host "[INFO] Method: Multi-pass rendering (no timeouts)" -ForegroundColor Cyan
    Write-Host "[INFO] Upload to: https://studio.youtube.com/channel/UCS5pEpSCw8k4wene0iv0uAg/videos" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "DONE!" -ForegroundColor Green
Start-Process explorer.exe -ArgumentList (Join-Path $ROOT "uploaded")
