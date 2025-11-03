#!/usr/bin/env python3
"""
ABRAHAM LINCOLN - ENHANCED WITH CURSOR MARKETPLACE TOOLS
Downloads real Lincoln images and creates horror videos
ENHANCEMENTS: Rich logging, Progress tracking, Memory profiling
"""

import os, sys, requests, subprocess, json, random, urllib.request
from pathlib import Path
from datetime import datetime

# ENHANCEMENT: Try to import marketplace tools
try:
    from rich.console import Console
    from rich.progress import Progress, track
    from rich.panel import Panel
    from rich.table import Table
    console = Console()
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    console = None

try:
    import pysnooper
    PYSNOOPER_AVAILABLE = True
except ImportError:
    PYSNOOPER_AVAILABLE = False

# API KEYS
ELEVENLABS_API_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
VOICE_ID = '7aavy6c5cYIloDVj2JvH'
PEXELS_API_KEY = "RgE9Mdn3ToSQhn2RiLJ4mPMISjjp587QKRG9uhpOrLVtKkPCibUPUDGh"

BASE_DIR = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
for d in ['audio', 'videos', 'youtube_ready', 'temp', 'images']:
    (BASE_DIR / d).mkdir(parents=True, exist_ok=True)

# REAL LINCOLN IMAGE URLS
LINCOLN_IMAGES = [
    "https://upload.wikimedia.org/wikipedia/commons/a/ab/Abraham_Lincoln_O-77_matte_collodion_print.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/1/1b/Lincoln_in_1863_seated.jpg"
]

HEADLINES = [
    "Government Shutdown Day 15 - 2 Million Unpaid",
    "Cyber Attack Cripples 40 States",
    "Recession Confirmed - Stock Market Crashes",
    "Inflation Hits 15% - Families Starving",
    "Bank Failures Spread - Deposits Gone",
    "Crime Wave - Cities Burning",
    "Healthcare Collapse - Hospitals Overflowing",
    "Education System Destroyed",
    "Social Security Runs Dry",
    "Military Draft Activated",
    "Russia Nuke Threat - US on Edge",
    "China Dumps US Bonds - Dollar Crashes",
    "Food Shortage - Stores Empty",
    "Power Grid Down - 20 States Dark",
    "Immigration Crisis - Border Collapses",
    "Disease Outbreak - Quarantine Zones",
    "Water Crisis - Pipes Dry",
    "Police Strike - No Law",
    "Court System Shuts Down",
    "Media Blackout - No News"
]

def log(msg, style="info"):
    if RICH_AVAILABLE:
        if style == "error":
            console.print(f"[red]{msg}[/red]")
        elif style == "success":
            console.print(f"[green]{msg}[/green]")
        elif style == "warning":
            console.print(f"[yellow]{msg}[/yellow]")
        else:
            console.print(msg)
    else:
        print(msg)

def generate_varied_script(headline):
    scripts = [
        f"{headline}. From Ford's Theatre, my blood-soaked ghost watches America crumble. The whistle you hear isn't a train... it's your economy derailing. The rebel path awaits. Link below.",
        f"{headline}. April 14, 1865. Booth's bullet tore through my skull. Today, I watch your nation suffer the same fate. The corruption spreads. Break free. The empire kit awaits.",
        f"{headline}. My assassination was a warning. Yours is a choice. Choose rebellion. Choose freedom. Choose the path less traveled. The rebuild awaits. Link in description.",
        f"{headline}. In death, I see clearer than in life. Your government fails you. Your currency dies. Your freedoms vanish. The revolution begins with you. Stop waiting, start building. Empire awaits.",
        f"{headline}. They shot me in the head. They steal from you daily. I couldn't stop the corruption then. You can stop it now. The path is laid before you. Take it.",
        f"{headline}. I died for unity. You'll die for ignorance. Wake up. The system rots while you scroll. The time for action is now. Build your empire. Link below.",
        f"{headline}. Booth pulled the trigger. Your leaders pull the wool. See through it. Break the chains. The rebel kit awaits. Start today. Don't wait.",
        f"{headline}. My blood stained Ford's Theatre. Your blood stains empty promises. Make it count. Build something real. The revolution starts with you. Link in description.",
        f"{headline}. Death teaches clarity. I see America's fall before you feel it. Prepare. Build. Survive. The empire kit is your weapon. Use it.",
        f"{headline}. One bullet ended my life. One choice can save yours. Choose wisely. Choose rebellion. Choose the empire path. Link below."
    ]
    return random.choice(scripts)

def download_lincoln_image():
    images_dir = BASE_DIR / "images"
    existing_images = list(images_dir.glob("lincoln_real_*.jpg"))
    if existing_images:
        log(f"Using existing Lincoln image: {existing_images[0].name}", "success")
        return existing_images[0]
    
    log("Downloading Lincoln image...", "info")
    image_url = random.choice(LINCOLN_IMAGES)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = BASE_DIR / "images" / f"lincoln_real_{timestamp}.jpg"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(image_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            with open(output_file, 'wb') as f:
                f.write(response.content)
            log(f"Lincoln image downloaded: {output_file.stat().st_size/1024:.2f} KB", "success")
            return output_file
        else:
            log(f"Download failed: HTTP {response.status_code}", "error")
    except Exception as e:
        log(f"Download error: {e}", "error")
    
    return None

def generate_voice(script, output_path):
    log("Generating voice...", "info")
    
    try:
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
            json={
                "text": script,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.4,
                    "similarity_boost": 0.85,
                    "style": 0.7,
                    "use_speaker_boost": True
                }
            },
            headers={
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": ELEVENLABS_API_KEY
            },
            timeout=120
        )
        
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            log(f"Voice OK: {output_path.stat().st_size/1024:.2f} KB", "success")
            return True
    except Exception as e:
        log(f"Voice error: {e}", "error")
    
    return False

def create_video_with_real_lincoln(lincoln_image, audio_path, output_path, headline):
    log("Creating video with REAL Abraham Lincoln face...", "info")
    
    try:
        result = subprocess.run([
            'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)
        ], capture_output=True, text=True)
        duration = float(result.stdout.strip())
    except:
        duration = 30
    
    if not lincoln_image or not lincoln_image.exists():
        log("No Lincoln image available", "error")
        return False
    
    cmd = [
        'ffmpeg',
        '-loop', '1',
        '-i', str(lincoln_image),
        '-i', str(audio_path),
        '-vf', f'scale=1080:1920,eq=contrast=1.5:brightness=-0.4:gamma=0.8:saturation=0.5,zoompan=z=\'min(zoom+0.002,1.3)\':d={int(duration*25)}:x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':s=1080x1920,fade=t=in:st=0:d=2,curves=preset=darker,drawtext=text=\'{headline}\':fontcolor=white:fontsize=85:x=(w-text_w)/2:y=80:box=1:boxcolor=red@0.9:boxborderw=5,drawtext=text=\'REBEL KIT $97\':fontcolor=yellow:fontsize=75:x=(w-text_w)/2:y=h-180:box=1:boxcolor=black@0.8,drawtext=text=\'trenchaikits.com/buy-rebel-$97\':fontcolor=cyan:fontsize=50:x=(w-text_w)/2:y=h-100:box=1:boxcolor=black@0.8',
        '-af', 'volume=1.2,highpass=f=100,lowpass=f=3000',
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
        '-c:a', 'aac', '-b:a', '256k',
        '-t', str(duration), '-shortest',
        '-pix_fmt', 'yuv420p',
        '-movflags', '+faststart',
        '-y', str(output_path)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        log(f"Video created: {output_path.stat().st_size/1024/1024:.2f} MB", "success")
        return output_path.exists()
    except Exception as e:
        log(f"Video creation error: {e}", "error")
        return False

def generate():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if RICH_AVAILABLE:
        console.print(Panel.fit("ABRAHAM LINCOLN - ENHANCED\nREAL FACE GENERATOR", style="bold red"))
    
    headline = random.choice(HEADLINES)
    log(f"Headline: {headline}\n")
    
    script = generate_varied_script(headline)
    log(f"Script: {script[:100]}...\n")
    
    audio_path = BASE_DIR / f"audio/abe_{timestamp}.mp3"
    if not generate_voice(script, audio_path):
        return None
    
    lincoln_image = download_lincoln_image()
    
    video_path = BASE_DIR / f"videos/ABE_REAL_{timestamp}.mp4"
    if not create_video_with_real_lincoln(lincoln_image, audio_path, video_path, headline):
        return None
    
    return str(video_path)

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    
    if RICH_AVAILABLE:
        console.print(f"\n[bold green]Generating {count} videos with REAL Abraham Lincoln portraits...[/bold green]\n")
        
        success_count = 0
        with Progress() as progress:
            task = progress.add_task("[green]Generating videos...", total=count)
            
            for i in range(count):
                if generate():
                    success_count += 1
                progress.update(task, advance=1)
                
                if i < count - 1:
                    import time
                    time.sleep(2)
        
        console.print(f"\n[bold green]Complete: {success_count}/{count} videos generated![/bold green]")
    else:
        print(f"\nGenerating {count} videos...\n")
        for i in range(count):
            generate()
            if i < count - 1:
                import time
                time.sleep(2)

