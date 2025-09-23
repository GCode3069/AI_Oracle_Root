#!/usr/bin/env python3
"""
scarify_cli.py - Simple Typer CLI for SCARIFY AI Oracle Ecosystem
Fast, cost-effective solution using virtualenv
"""
import subprocess
import sys
from pathlib import Path
from typing import Optional
import typer

app = typer.Typer(help="SCARIFY AI Oracle Ecosystem CLI")
REPO_ROOT = Path(__file__).parent

@app.command()
def generate(
    duration: int = typer.Option(45, help="Video duration in seconds"),
    theme: str = typer.Option("tech_mystery", help="Content theme")
):
    """Generate a new SCARIFY deployment video"""
    typer.echo("🎬 Generating SCARIFY deployment video...")
    
    # Call your existing generator
    generator = REPO_ROOT / "SCARIFY_Deployment_Video_Generator.py"
    if generator.exists():
        result = subprocess.run([sys.executable, str(generator), str(duration), theme])
        if result.returncode == 0:
            typer.echo("✅ Video generated successfully!")
        else:
            typer.echo("❌ Generation failed")
            raise typer.Exit(code=1)
    else:
        typer.echo("⚠️  Generator script not found, creating sample video...")
        create_sample_video(duration)

def create_sample_video(duration: int):
    """Fallback sample video creation"""
    try:
        from moviepy.editor import ColorClip, AudioFileClip
        from gtts import gTTS
        import tempfile
        
        # Create simple video with text-to-speech
        tts = gTTS(f"SCARIFY Transmission. Duration {duration} seconds. AI Oracle Ecosystem active.")
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as audio_file:
            tts.save(audio_file.name)
        
        # Create color clip with audio
        video = ColorClip(size=(1920, 1080), color=(0, 0, 0), duration=duration)
        audio = AudioFileClip(audio_file.name)
        video = video.set_audio(audio)
        
        output_path = REPO_ROOT / "scarify" / "Output" / "YouTubeReady" / f"SCARIFY_Sample_{duration}s.mp4"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        video.write_videofile(str(output_path), fps=24)
        
        typer.echo(f"✅ Sample video created: {output_path}")
    except ImportError:
        typer.echo("❌ Required packages missing. Run: pip install moviepy gtts")

@app.command()
def upload(
    video_path: Optional[str] = typer.Argument(None, help="Path to video file"),
    title: Optional[str] = typer.Option(None, help="YouTube video title"),
    auto_find: bool = typer.Option(True, help="Auto-find latest generated video")
):
    """Upload video to YouTube"""
    
    # Find video file
    if video_path:
        video_file = Path(video_path)
    elif auto_find:
        output_dir = REPO_ROOT / "scarify" / "Output" / "YouTubeReady"
        videos = list(output_dir.glob("SCARIFY_*.mp4"))
        if not videos:
            typer.echo("❌ No SCARIFY videos found. Generate one first.")
            raise typer.Exit(code=1)
        video_file = max(videos, key=lambda p: p.stat().st_mtime)
        typer.echo(f"🔍 Found latest video: {video_file.name}")
    else:
        typer.echo("❌ No video specified")
        raise typer.Exit(code=1)
    
    if not video_file.exists():
        typer.echo(f"❌ Video not found: {video_file}")
        raise typer.Exit(code=1)
    
    # Use existing uploader or direct API
    uploader = REPO_ROOT / "youtube_uploader_wrapper.py"
    if uploader.exists():
        typer.echo("📤 Uploading via existing wrapper...")
        cmd = [sys.executable, str(uploader), str(video_file)]
        if title:
            cmd.append(title)
        subprocess.run(cmd)
    else:
        # Direct upload fallback
        direct_upload(video_file, title)

def direct_upload(video_path: Path, title: str = None):
    """Direct YouTube upload using API"""
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        
        SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
        
        # Authenticate
        flow = InstalledAppFlow.from_client_secrets_file(
            REPO_ROOT / 'credentials' / 'client_secrets.json', 
            SCOPES
        )
        creds = flow.run_local_server(port=0)
        
        # Build service
        youtube = build('youtube', 'v3', credentials=creds)
        
        # Create upload request
        if not title:
            title = f"SCARIFY Transmission {video_path.stem}"
        
        body = {
            'snippet': {
                'title': title,
                'description': 'AI Oracle Ecosystem - SCARIFY Transmission',
                'tags': ['AI', 'Oracle', 'SCARIFY', 'Transmission', 'Mystery'],
                'categoryId': '27'  # Education
            },
            'status': {
                'privacyStatus': 'unlisted',
                'selfDeclaredMadeForKids': False
            }
        }
        
        media = MediaFileUpload(str(video_path), chunksize=1024*1024, resumable=True)
        request = youtube.videos().insert(part='snippet,status', body=body, media_body=media)
        
        typer.echo("📤 Uploading...")
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                typer.echo(f"📊 Progress: {int(status.progress() * 100)}%")
        
        typer.echo(f"✅ Upload complete! Video ID: {response['id']}")
        typer.echo(f"🔗 https://youtube.com/watch?v={response['id']}")
        
    except Exception as e:
        typer.echo(f"❌ Upload failed: {e}")
        raise typer.Exit(code=1)

@app.command()
def lightning(
    input_video: str,
    autoupload: bool = typer.Option(False, help="Auto-upload to YouTube"),
    title: str = typer.Option("", help="YouTube title for auto-upload")
):
    """Run Lightning Strike pipeline"""
    ps_script = REPO_ROOT / "scarify" / "lightning_strike" / "SCARIFY-Lightning-Integration-YouTube.ps1"
    
    if not ps_script.exists():
        typer.echo("❌ Lightning Strike script not found")
        raise typer.Exit(code=1)
    
    cmd = [
        "powershell", "-ExecutionPolicy", "Bypass", 
        "-File", str(ps_script), 
        "-InputVideo", input_video
    ]
    
    if autoupload:
        cmd.append("-AutoUpload")
        if title:
            cmd.extend(["-YouTubeTitle", title])
    
    typer.echo("⚡ Running Lightning Strike...")
    subprocess.run(cmd)

@app.command()
def setup():
    """Setup YouTube API credentials""" 
    creds_dir = REPO_ROOT / "credentials"
    creds_dir.mkdir(exist_ok=True)
    
    typer.echo("🔐 YouTube API Setup Instructions:")
    typer.echo("1. Go to: https://console.cloud.google.com/")
    typer.echo("2. Create new project or select existing")
    typer.echo("3. Enable YouTube Data API v3")
    typer.echo("4. Create OAuth 2.0 Desktop credentials")
    typer.echo("5. Download client_secrets.json")
    typer.echo("6. Save to: credentials/client_secrets.json")
    typer.echo("")
    typer.echo("First upload will open browser for authentication.")

@app.command()
def status():
    """Show system status"""
    typer.echo("🔍 SCARIFY System Status:")
    
    # Check critical files
    files_to_check = [
        ("Generator", REPO_ROOT / "SCARIFY_Deployment_Video_Generator.py"),
        ("Uploader", REPO_ROOT / "youtube_uploader_wrapper.py"),
        ("Lightning Strike", REPO_ROOT / "scarify" / "lightning_strike" / "SCARIFY-Lightning-Integration-YouTube.ps1"),
        ("Credentials", REPO_ROOT / "credentials" / "client_secrets.json")
    ]
    
    for name, path in files_to_check:
        if path.exists():
            typer.echo(f"✅ {name}: Found")
        else:
            typer.echo(f"❌ {name}: Missing")

if __name__ == "__main__":
    app()