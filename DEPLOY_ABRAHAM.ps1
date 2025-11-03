# ============================================================================
# ABRAHAM HORROR - SELF-DEPLOYING BOOTSTRAP
# Generates REAL videos with actual content (not black screens)
# Uses: Pexels stock footage + ElevenLabs professional voice
# ============================================================================

param([int]$Count = 1)

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Red
Write-Host "║   🎃 ABRAHAM HORROR - SELF-DEPLOYING                      ║" -ForegroundColor Red
Write-Host "║   Real Videos, Professional Voice, No Black Screens       ║" -ForegroundColor Red
Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Red
Write-Host ""

# Configuration
$BASE_DIR = "F:\AI_Oracle_Root\scarify\abraham_horror"

# Embedded Python generator with REAL video generation
$PYTHON_GEN = @'
import os, sys, requests, subprocess, json
from pathlib import Path
from datetime import datetime
import random

# API Keys - EMBEDDED
ELEVENLABS_API_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
VOICE_ID = '7aavy6c5cYIloDVj2JvH'
PEXELS_API_KEY = "dLdEZyJRQJvV3xltfZMJ0lNJJZfN6ldbJnAUxJRbgwaRRqVcTUxnQMJf"

BASE_DIR = Path("F:/AI_Oracle_Root/scarify/abraham_horror")

# Create directories
for d in ['audio', 'videos', 'youtube_ready', 'temp']:
    (BASE_DIR / d).mkdir(parents=True, exist_ok=True)

def get_headlines():
    return [
        "Government Shutdown Day 15 - Critical Services Failing",
        "Major Cyber Attack - Millions Data Breached",  
        "Recession Signals - Economic Collapse Looms",
        "Extreme Weather Spreads - Climate Crisis",
        "Nation Divided - Political Turmoil",
        "50 Million Data Breached - Privacy Gone",
        "Inflation Crushes Families - Survival Hard",
        "Healthcare Collapsing - Access Denied",
        "Education Crisis - Students Failing",
        "Social Unrest - Authority Alert"
    ]

def generate_script(headline):
    gore = ["derringer tears skull, blood floods", "bone shards grind brain", "occiput explodes, crimson tide", "probing fingers squelch clot"][random.randint(0,3)]
    return f"""I watch from shadows as America tears apart. {headline}.

Ford's Theatre, April 14th, {gore}. Blood-soaked democracy bleeds while you sleep.

Corruption metastasizes. Every lie echoes through my shattered skull.

You live the nightmare I warned against. The Union I died for crumbles.

Sic semper tyrannis. Thus always to tyrants."""

def generate_voice(script, output_path):
    print("🎙️  Generating professional voice with ElevenLabs...")
    try:
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
            json={"text": script, "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.3, "similarity_boost": 0.85, "style": 0.8, "use_speaker_boost": True}},
            headers={"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": ELEVENLABS_API_KEY},
            timeout=120
        )
        if response.status_code == 200:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"✅ Voice: {output_path.stat().st_size/1024:.2f} KB")
            return True
        print(f"❌ ElevenLabs: {response.status_code}")
    except Exception as e:
        print(f"❌ Voice failed: {e}")
    return False

def get_stock_video(keyword):
    print(f"🎬 Fetching REAL stock video: {keyword}...")
    try:
        response = requests.get(
            "https://api.pexels.com/videos/search",
            headers={"Authorization": PEXELS_API_KEY},
            params={"query": keyword, "per_page": 1, "orientation": "portrait"},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('videos'):
                video_file = max(data['videos'][0].get('video_files', []), key=lambda x: x.get('width',0)*x.get('height',0))
                vid_resp = requests.get(video_file.get('link'), timeout=120)
                temp_file = BASE_DIR / "temp" / f"stock_{random.randint(1000,9999)}.mp4"
                temp_file.parent.mkdir(parents=True, exist_ok=True)
                with open(temp_file, 'wb') as f:
                    f.write(vid_resp.content)
                print(f"✅ Stock video: {temp_file.name}")
                return temp_file
    except Exception as e:
        print(f"⚠️ Pexels error: {e}")
    return None

def create_video(stock_video, audio_path, output_path, headline):
    print("🎬 Creating professional video with REAL footage...")
    try:
        result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)], capture_output=True, text=True)
        duration = float(result.stdout.strip())
    except:
        duration = 30
    
    if stock_video and stock_video.exists():
        cmd = ['ffmpeg', '-i', str(stock_video), '-i', str(audio_path), '-vf', f'eq=contrast=1.3:brightness=-0.2:gamma=1.2,crop=1080:1920:0:0,scale=1080:1920,drawtext=text=\'{headline}\':fontcolor=white:fontsize=80:x=(w-text_w)/2:y=h/8:box=1:boxcolor=black@0.7:boxborderw=10', '-af', 'volume=0.8', '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-c:a', 'aac', '-b:a', '192k', '-t', str(duration), '-y', str(output_path)]
        subprocess.run(cmd, capture_output=True)
        
        if output_path.exists():
            print(f"✅ Video: {output_path.stat().st_size/1024/1024:.2f} MB")
            return True
    
    print("❌ Video creation failed")
    return False

def generate():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    print(f"\n{'='*60}\nABRAHAM HORROR VIDEO\n{'='*60}\n")
    
    headlines = get_headlines()
    headline = random.choice(headlines)
    print(f"📰 {headline}\n")
    
    script = generate_script(headline)
    print(f"📝 Script: {len(script)} chars\n")
    
    audio_path = BASE_DIR / f"audio/abraham_{timestamp}.mp3"
    if not generate_voice(script, audio_path):
        return None
    
    stock_video = get_stock_video("dark horror atmosphere")
    
    video_path = BASE_DIR / f"videos/ABRAHAM_{timestamp}.mp4"
    if not create_video(stock_video, audio_path, video_path, headline):
        return None
    
    youtube_dir = BASE_DIR / "youtube_ready"
    youtube_dir.mkdir(parents=True, exist_ok=True)
    youtube_file = youtube_dir / f"ABRAHAM_{timestamp}.mp4"
    
    import shutil
    shutil.copy2(video_path, youtube_file)
    
    metadata = {
        'file_path': str(youtube_file),
        'headline': headline,
        'title': f"Lincoln's Warning: {headline[:50]} #Shorts",
        'description': f"""{headline}

⚠️ LINCOLN'S WARNING

From Ford's Theatre, April 14, 1865...

#Halloween2025 #AbrahamLincoln #Horror #Shorts""",
        'created_at': datetime.now().isoformat()
    }
    
    metadata_file = youtube_file.with_suffix('.json')
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n✅ READY: {youtube_file.name}\n")
    return str(youtube_file)

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║   🎃 ABRAHAM HORROR - REAL VIDEOS                         ║
    ║   Pexels + ElevenLabs + No Black Screens                 ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    print(f"Generating {count} video(s)...\n")
    
    results = []
    for i in range(count):
        result = generate()
        if result:
            results.append(result)
        if i < count - 1:
            print("Waiting 5 seconds...\n")
            import time
            time.sleep(5)
    
    print(f"COMPLETE: {len(results)}/{count}\n")
'@

# Deploy and run
Write-Host "[1/3] Deploying generator..." -ForegroundColor Yellow

$pythonScript = Join-Path $BASE_DIR "abraham_generator.py"
$pythonScript | Split-Path | ForEach-Object { New-Item -Path $_ -ItemType Directory -Force | Out-Null }
$PYTHON_GEN | Out-File -FilePath $pythonScript -Encoding UTF8

Write-Host "✅ Generator deployed" -ForegroundColor Green
Write-Host ""

Write-Host "[2/3] Generating $Count video(s)..." -ForegroundColor Yellow
Write-Host ""

& python $pythonScript $Count

Write-Host ""
Write-Host "[3/3] Results" -ForegroundColor Yellow
Write-Host ""

$youtubeDir = Join-Path $BASE_DIR "youtube_ready"
if (Test-Path $youtubeDir) {
    $videos = Get-ChildItem -Path $youtubeDir -Filter "*.mp4" | Sort-Object LastWriteTime -Descending | Select-Object -First $Count
    
    if ($videos) {
        Write-Host "✅ Generated Videos:" -ForegroundColor Green
        foreach ($video in $videos) {
            $sizeMB = [math]::Round($video.Length / 1MB, 2)
            Write-Host "  ✓ $($video.Name) (${sizeMB}MB)" -ForegroundColor White
        }
        
        Write-Host ""
        Start-Process explorer.exe -ArgumentList $youtubeDir
    }
}

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║   ✅ READY TO UPLOAD                                    ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "📁 Upload from: $youtubeDir" -ForegroundColor Cyan
Write-Host ""

