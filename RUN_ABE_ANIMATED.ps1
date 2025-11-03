# ═══════════════════════════════════════════════════════════════════════════
# ABRAHAM ANIMATED - COMPLETE ONE-FILE SOLUTION
# Everything in one script - no external files needed
# ═══════════════════════════════════════════════════════════════════════════

param([int]$Count = 10)

$ROOT = "F:\AI_Oracle_Root\scarify\abraham_horror"

Write-Host ""
Write-Host "🔥 ABRAHAM ANIMATED STUDIO - ONE-FILE DEPLOY 🔥" -ForegroundColor Red
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host ""

# Create directories
$dirs = @("audio", "videos", "uploaded", "temp")
foreach ($dir in $dirs) {
    $path = Join-Path $ROOT $dir
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
        Write-Host "📁 Created: $dir" -ForegroundColor Green
    }
}

# Install packages
Write-Host ""
Write-Host "📦 Installing Python packages..." -ForegroundColor Cyan
pip install --quiet requests beautifulsoup4 lxml 2>&1 | Out-Null
Write-Host "✅ Packages installed" -ForegroundColor Green

# Create Python script inline
Write-Host ""
Write-Host "📝 Creating generator..." -ForegroundColor Cyan

$pythonCode = @'
import os, sys, json, requests, subprocess, random, time
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

ELEVENLABS_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
BTC = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"

def scrape():
    try:
        r = requests.get("https://news.google.com/rss", timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'xml')
            return [item.title.text for item in soup.find_all('item')[:20] if item.title]
    except: pass
    return ["Trump Third Term", "Police Violence Continues", "Climate Summit Fails"]

def script(headline):
    hl = headline.lower()
    if "trump" in hl:
        return f"""Abraham Lincoln here. Dead since 1865.

{headline}.

Trump. Billionaire born with gold spoon convinced POOR people he's one of them. Con of the century.

I grew up in log cabin. ACTUAL poverty. Split rails. Read by candlelight. EARNED everything.

He inherited millions. Bankrupted casinos. You know how hard that is?

But YOU enable this. You worship a man who wouldn't piss on you if you were on fire.

He calls you poorly educated and you CHEER. You're not victims. You're VOLUNTEERS.

Rich around him? Senators? CEOs? You KNOW better. But you enable him because it's PROFITABLE.

You're ALL guilty. Rich manipulating. Poor believing. Elite enabling.

April 14 1865. Booth shot me. Nine hours dying. I saw YOU. I was WRONG.

Stop pointing fingers. Look in mirrors. Bitcoin {BTC}"""
    
    return f"""Abraham Lincoln here. Got shot at theater.

{headline}.

Who to blame? EVERYONE.

People with POWER doing NOTHING. People with MONEY hoarding it. People with PLATFORMS spreading lies.

YOU. You see problems but don't ACT. You see injustice and scroll past.

You have votes. Voices. CHOICES. But you choose NOTHING.

Rich exploiting. Middle enabling. Poor suffering. Media profiting. Politicians lying.

EVERYONE plays their part. Worst part? You'll watch this. Laugh. Share it. Then do NOTHING.

I died believing in human progress. I was wrong. You're ALL complicit.

Look in mirrors. Bitcoin {BTC}"""

def audio(text, out):
    print("    [AUDIO]")
    try:
        r = requests.post("https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB",
                         json={"text": text, "model_id": "eleven_multilingual_v2",
                               "voice_settings": {"stability": 0.4, "similarity_boost": 0.9, 
                                                "style": 0.8, "use_speaker_boost": True}},
                         headers={"xi-api-key": ELEVENLABS_KEY}, timeout=240)
        if r.status_code == 200:
            out.parent.mkdir(parents=True, exist_ok=True)
            with open(out, "wb") as f: f.write(r.content)
            return True
    except: pass
    return False

def video(audio_path, out):
    print("    [VIDEO]")
    try:
        img = BASE / "temp" / "lincoln.jpg"
        if not img.exists():
            img.parent.mkdir(exist_ok=True)
            data = requests.get("https://upload.wikimedia.org/wikipedia/commons/a/ab/Abraham_Lincoln_O-77_matte_collodion_print.jpg", timeout=30).content
            with open(img, "wb") as f: f.write(data)
        
        probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)],
                              capture_output=True, text=True)
        duration = float(probe.stdout.strip())
        
        subprocess.run([
            "ffmpeg", "-y", "-loop", "1", "-i", str(img), "-i", str(audio_path),
            "-filter_complex",
            "[0:v]scale=1080:1920,zoompan=z='if(lte(zoom,1.0),1.5,max(1.001,zoom-0.0015))':d=125:s=1080x1920,"
            "eq=contrast=1.5:brightness=-0.1:saturation=0.9,noise=alls=10:allf=t,format=yuv420p[v]",
            "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-c:a", "aac", "-b:a", "320k", "-t", str(duration), "-pix_fmt", "yuv420p", str(out)
        ], capture_output=True, timeout=600)
        
        return out.exists()
    except: pass
    return False

def gen():
    t = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"\n{'='*70}\nVIDEO {t}\n{'='*70}")
    
    h = random.choice(scrape())
    print(f"Headline: {h[:60]}")
    
    s = script(h)
    print(f"Script: {len(s)} chars")
    
    ap = BASE / f"audio/abe_{t}.mp3"
    if not audio(s, ap):
        print("❌ Audio failed")
        return None
    print("✅ Audio done")
    
    vp = BASE / f"videos/ABE_{t}.mp4"
    if not video(ap, vp):
        print("❌ Video failed")
        return None
    print("✅ Video done")
    
    up = BASE / "uploaded" / f"ABE_ANIMATED_{t}.mp4"
    up.parent.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy2(vp, up)
    
    mb = up.stat().st_size / (1024 * 1024)
    print(f"{'='*70}\n✅ SUCCESS: {up.name} ({mb:.1f}MB)\n{'='*70}")
    return str(up)

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    print(f"\n🔥 GENERATING {count} ANIMATED ABE VIDEOS 🔥\n")
    
    success = 0
    for i in range(count):
        if gen(): success += 1
        if i < count - 1:
            print("\nWaiting 20 seconds...\n")
            time.sleep(20)
    
    print(f"\n{'='*70}\n🎉 COMPLETE: {success}/{count}\n{'='*70}\n")
'@

$pyFile = Join-Path $ROOT "abe_animated.py"
$pythonCode | Set-Content -Path $pyFile -Encoding UTF8
Write-Host "✅ Generator created" -ForegroundColor Green

# Run it
Write-Host ""
Write-Host "🚀 GENERATING $Count VIDEOS..." -ForegroundColor Yellow
Write-Host ""

Set-Location $ROOT
python abe_animated.py $Count

# Show results
Write-Host ""
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host "📊 RESULTS" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Gray

$videos = Get-ChildItem (Join-Path $ROOT "uploaded") -Filter "*.mp4" -ErrorAction SilentlyContinue
if ($videos) {
    $totalSize = ($videos | Measure-Object -Property Length -Sum).Sum / 1MB
    Write-Host "✅ Generated: $($videos.Count) videos" -ForegroundColor Green
    Write-Host "💾 Total size: $([math]::Round($totalSize, 1)) MB" -ForegroundColor White
    Write-Host "📁 Location: uploaded\" -ForegroundColor Cyan
} else {
    Write-Host "⚠️  No videos found" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 DONE!" -ForegroundColor Green
Write-Host ""

# Open folder
Start-Process explorer.exe -ArgumentList (Join-Path $ROOT "uploaded")
