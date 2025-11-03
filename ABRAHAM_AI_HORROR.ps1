# ============================================================================
# ABRAHAM AI HORROR GENERATOR - HALLOWEEN 2025
# Complete inline self-bootstrapping system
# Headlines → Lincoln Gore → Real Videos → YouTube Upload
# ============================================================================

param(
    [int]$Count = 5,
    [switch]$TestOnly,
    [string]$Method = "auto"
)

$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Red
Write-Host "║   🎃 ABRAHAM AI HORROR - HALLOWEEN 2025                 ║" -ForegroundColor Red
Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Red
Write-Host ""

# ============================================================================
# CONFIGURATION
# ============================================================================

$CONFIG = @{
    BASE_DIR = "F:\AI_Oracle_Root\scarify\abraham_horror"
    VOICE_ID = "7aavy6c5cYIloDVj2JvH"
    VERSION = "5.0-ABRAHAM"
}

# Create directories
$dirs = @("scripts", "audio", "videos", "youtube_ready")
foreach ($dir in $dirs) {
    $path = Join-Path $CONFIG.BASE_DIR $dir
    if (-not (Test-Path $path)) {
        New-Item -Path $path -ItemType Directory -Force | Out-Null
    }
}

# ============================================================================
# EMBEDDED PYTHON - COMPLETE WORKING SYSTEM
# ============================================================================

$PYTHON_SYSTEM = @'
import os, sys, json, random, requests, subprocess
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
VOICE_ID = '7aavy6c5cYIloDVj2JvH'
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY', '')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

# YouTube Uploader
try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    import pickle
    YOUTUBE_AVAILABLE = True
except ImportError:
    YOUTUBE_AVAILABLE = False

# Trending fear headlines
HEADLINES = [
            "Corrupt Government Officials at Record High - 69% Fear Level",
            "ICE Raids Spread Fear Across Communities - Families Hide",
            "Cyber-Terrorism Threats Surge - 55.9% Americans Terrified",
            "Economic Collapse Imminent - 58.2% Fear Total System Failure",
    "Trump Warns: Antifa Planning Coordinated Attack",
            "Government Shutdown Day 10 - No End in Sight",
    "Bitcoin Death Spiral - Crypto is Dead Say Experts",
    "Foreclosure Crisis Exploding - Housing Market Collapse"
        ]
        
# Gore elements
GORE = [
    "derringer tears through skull, blood floods theatre",
            "brain matter spatters velvet curtain",
            "bone fragments lodge in mahogany, ichor pools",
            "jaw unhinges, tongue lolls, death rattle echoes",
    "fingers probe wound, dislodge clot, cavity gapes"
        ]
    
def generate_script(headline):
    """Generate Lincoln horror script"""
    gore = random.choice(GORE)
    
    templates = [
        f"They shot me in Ford's Theatre. {gore}. I watch from shadows as America tears itself apart. {headline}. The corruption I fought has metastasized. Blood-soaked democracy, just as mine was blood-soaked. Every bullet echoes through my shattered skull. Sic semper tyrannis.",
        f"In death I see clearly. The theatre box drips with my essence. {gore}. {headline}. This is the America I bled for? A nation consumed by demons. My fingers trace the wound that ended me. Your fear feeds my torment. Sic semper tyrannis.",
        f"They call me the Great Emancipator. But who will free me? {gore}. Every night I replay the shot. {headline}. America has become the tyrant I fought. The theatre of democracy stages horror. My blood stains history you refuse to read. Sic semper tyrannis."
        ]
        
    return random.choice(templates)
        
def generate_audio(script, output_path):
    """Generate audio with ElevenLabs or gTTS"""
    
    if ELEVENLABS_API_KEY:
        try:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
            headers = {"Accept": "audio/mpeg", "xi-api-key": ELEVENLABS_API_KEY}
    
    data = {
                "text": script,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
                    "stability": 0.3,
                    "similarity_boost": 0.85,
                    "style": 0.8,
            "use_speaker_boost": True
        }
    }
    
        response = requests.post(url, json=data, headers=headers, timeout=120)
        
        if response.status_code == 200:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(response.content)
                print(f"   Audio: {output_path.name}")
                return True
        except Exception as e:
            print(f"   ElevenLabs failed: {e}")
    
    # Fallback to gTTS
    try:
        from gtts import gTTS
        tts = gTTS(text=script, lang='en', slow=True)
        tts.save(str(output_path))
        print(f"   Audio: {output_path.name} (gTTS)")
            return True
    except Exception as e:
        print(f"   Audio failed: {e}")
        return False

def create_video(audio_path, output_path, headline):
    """Create video with FFmpeg"""
    
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True)
    except:
        print("FFmpeg not found!")
        return False
    
    # Get duration
    try:
        probe = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)], capture_output=True, text=True)
        duration = float(probe.stdout.strip())
    except:
        duration = 60.0
    
    # Create video
    cmd = [
        'ffmpeg',
        '-f', 'lavfi',
        '-i', f'color=c=#1a0000:s=1920x1080:d={duration}',
        '-i', str(audio_path),
        '-vf', f'drawtext=text=\'{headline}\':fontcolor=white:fontsize=70:x=(w-text_w)/2:y=200',
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-b:v', '5000k',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-shortest',
        '-y',
        str(output_path)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        if output_path.exists():
            size_mb = output_path.stat().st_size / (1024 * 1024)
            print(f"   Video: {output_path.name} ({size_mb:.2f}MB)")
            return True
    except Exception as e:
        print(f"   Video failed: {e}")
        return False

def upload_to_youtube(video_path, headline):
    """Upload video directly to YouTube"""
    
    if not YOUTUBE_AVAILABLE:
        print("   YouTube uploader not available - saving locally")
        return prepare_youtube(video_path, headline)
    
    print(f"   Uploading to YouTube...")
    
    # Check for credentials
    credentials_file = Path("F:/AI_Oracle_Root/scarify/client_secret_679199614743-1fq6sini3p9kjs237ek4seg4ojp4a4qe.apps.googleusercontent.com.json")
    token_file = BASE_DIR / "youtube_token.pickle"
    
    if not credentials_file.exists():
        print("   No YouTube credentials - saving locally")
        return prepare_youtube(video_path, headline)
    
    try:
        # Load or get credentials
        creds = None
        if token_file.exists():
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                from google.auth.transport.requests import Request
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(credentials_file),
                    ['https://www.googleapis.com/auth/youtube.upload']
                )
                creds = flow.run_local_server(port=8080)
            
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        # Build service
        youtube = build('youtube', 'v3', credentials=creds)
        
        # Prepare metadata
        title = f"ABRAHAM LINCOLN'S WARNING: {headline[:40]} #Shorts"
        description = f"""Abraham Lincoln speaks from beyond the grave about {headline.lower()}.

⚠️ Lincoln's ghost has a message for America.

From Ford's Theatre, April 14, 1865, his blood-soaked spirit watches...

🎃 HALLOWEEN HORROR 2025
💀 Subscribe for more historical horror
👻 Share if this gave you chills

#Halloween2025 #AbrahamLincoln #Horror #PoliticalHorror #ScaryStories #Shorts"""
        
        tags = ['abraham lincoln', 'halloween 2025', 'horror', 'political horror', 'scary stories', 'shorts']
        
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': '24'  # Entertainment
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
            }
        }
        
        # Upload
        media = MediaFileUpload(str(video_path), chunksize=1024*1024, resumable=True)
        request = youtube.videos().insert(part=','.join(body.keys()), body=body, media_body=media)
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"   Upload progress: {int(status.progress() * 100)}%", end='\r')
        
        print()
        video_id = response['id']
        video_url = f"https://youtube.com/watch?v={video_id}"
        
        print(f"   ✅ UPLOADED: {video_url}")
        return video_url
        
    except Exception as e:
        print(f"   Upload failed: {e} - saving locally")
        return prepare_youtube(video_path, headline)

def prepare_youtube(video_path, headline):
    """Prepare for YouTube (local save)"""
    youtube_dir = BASE_DIR / "youtube_ready"
    youtube_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    youtube_file = youtube_dir / f"ABRAHAM_{timestamp}.mp4"
    
    import shutil
    shutil.copy2(video_path, youtube_file)
    
    metadata = {
        'file_path': str(youtube_file),
        'title': f"ABRAHAM LINCOLN'S WARNING: {headline[:40]}",
        'description': f"Abraham Lincoln speaks from beyond the grave about {headline.lower()}.\n\n⚠️ Lincoln's ghost has a message for America.\n\nFrom Ford's Theatre, April 14, 1865, his blood-soaked spirit watches...\n\n🎃 HALLOWEEN HORROR 2025\n#Halloween2025 #AbrahamLincoln #Horror #PoliticalHorror",
        'tags': ['abraham lincoln', 'halloween 2025', 'horror', 'political horror', 'scary stories'],
        'category': '24',
        'privacy': 'public',
        'created_at': datetime.now().isoformat()
    }
    
    metadata_file = youtube_file.with_suffix('.json')
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"   Saved: {youtube_file.name}")
    return youtube_file

def generate_video():
    """Complete pipeline"""
    
    print("\n" + "="*60)
    print("ABRAHAM HORROR VIDEO")
    print("="*60)
    
    headline = random.choice(HEADLINES)
    script = generate_script(headline)
    
    print(f"Headline: {headline}")
    print(f"Script: {len(script)} chars\n")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Audio
    audio_path = BASE_DIR / "audio" / f"abraham_{timestamp}.mp3"
    if not generate_audio(script, audio_path):
        return None
    
    # Video
    video_path = BASE_DIR / "videos" / f"ABRAHAM_{timestamp}.mp4"
    if not create_video(audio_path, video_path, headline):
        return None
    
    # YouTube Upload or Save
    youtube_file = upload_to_youtube(video_path, headline)
    
    # Save script
    script_file = BASE_DIR / "scripts" / f"abraham_{timestamp}.txt"
    with open(script_file, 'w') as f:
        f.write(f"HEADLINE: {headline}\n\nSCRIPT:\n{script}")
    
    print("\n" + "="*60)
    print("VIDEO GENERATED")
    print("="*60)
    print(f"Video: {youtube_file.name}")
    print(f"Location: {youtube_file}")
    print("="*60 + "\n")
    
    return str(youtube_file)

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    
    print("\n" + "="*60)
    print("ABRAHAM AI HORROR - HALLOWEEN 2025")
    print("="*60)
    print(f"Generating {count} video(s)...\n")
    
    results = []
    for i in range(count):
        result = generate_video()
        if result:
            results.append(result)
        if i < count - 1:
            print("Waiting 5 seconds...\n")
            import time
            time.sleep(5)
    
    print("="*60)
    print(f"COMPLETE: {len(results)}/{count} videos")
    print("="*60)
    print(f"\nVideos: {BASE_DIR / 'youtube_ready'}\n")
'@

# ============================================================================
# DEPLOY AND RUN
# ============================================================================

Write-Host "[STEP 1/3] Deploying Python system..." -ForegroundColor Yellow
    
    $pythonScript = Join-Path $CONFIG.BASE_DIR "abraham_generator.py"
$PYTHON_SYSTEM | Out-File -FilePath $pythonScript -Encoding UTF8
    
Write-Host "✅ Python system deployed" -ForegroundColor Green
    Write-Host ""
    
Write-Host "[STEP 2/3] Generating $Count video(s)..." -ForegroundColor Yellow
    Write-Host ""
    
& python $pythonScript $Count

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "[STEP 3/3] Results" -ForegroundColor Yellow
    
    $youtubeDir = Join-Path $CONFIG.BASE_DIR "youtube_ready"
    $videos = Get-ChildItem -Path $youtubeDir -Filter "*.mp4" | Sort-Object LastWriteTime -Descending | Select-Object -First $Count
    
    if ($videos) {
    Write-Host ""
        Write-Host "Generated Videos:" -ForegroundColor Green
        foreach ($video in $videos) {
            $sizeMB = [math]::Round($video.Length / 1MB, 2)
            Write-Host "  ✓ $($video.Name) (${sizeMB}MB)" -ForegroundColor White
        }
        Write-Host ""
        Write-Host "Location: $youtubeDir" -ForegroundColor Cyan
        
        Start-Process explorer.exe -ArgumentList $youtubeDir
    }
}

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║   ✅ ABRAHAM AI HALLOWEEN SERIES READY                  ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Upload videos to YouTube Shorts" -ForegroundColor White
Write-Host "2. Post to X/Twitter with #Halloween2025" -ForegroundColor White
Write-Host "3. Add Gumroad CTAs in descriptions" -ForegroundColor White
Write-Host "4. Track performance" -ForegroundColor White
Write-Host ""
