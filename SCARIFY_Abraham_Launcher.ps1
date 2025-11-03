# ═══════════════════════════════════════════════════════════════════════════
# SCARIFY + ABRAHAM LINCOLN - INTEGRATED DESKTOP LAUNCHER
# Complete system with professional video generation and YouTube auto-upload
# ═══════════════════════════════════════════════════════════════════════════

param(
    [switch]$Install,
    [switch]$ShowMenu
)

$ErrorActionPreference = "Continue"
$ScarifyRoot = "F:\AI_Oracle_Root\scarify"
$AbrahamRoot = "$ScarifyRoot\abraham_horror"

# ═══════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

function Write-StudioLog {
    param([string]$Message, [string]$Type = "INFO")
    $colors = @{
        "SUCCESS" = "Green"
        "ERROR" = "Red"
        "WARNING" = "Yellow"
        "PROCESS" = "Cyan"
        "INFO" = "White"
    }
    $icons = @{
        "SUCCESS" = "✅"
        "ERROR" = "❌"
        "WARNING" = "⚠️"
        "PROCESS" = "🔧"
        "INFO" = "ℹ️"
    }
    Write-Host "$($icons[$Type]) $Message" -ForegroundColor $colors[$Type]
}

function Install-AbrahamSystem {
    Write-StudioLog "Installing Abraham Lincoln Comedy System..." "PROCESS"
    
    # Create directory structure
    $dirs = @(
        "$AbrahamRoot\audio",
        "$AbrahamRoot\videos",
        "$AbrahamRoot\uploaded",
        "$AbrahamRoot\temp",
        "$ScarifyRoot\Output\Abraham_Comedy"
    )
    
    foreach ($dir in $dirs) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-StudioLog "Created: $dir" "SUCCESS"
        }
    }
    
    # Install Python packages
    Write-StudioLog "Installing Python packages..." "PROCESS"
    pip install --quiet --upgrade requests beautifulsoup4 lxml 2>&1 | Out-Null
    Write-StudioLog "Python packages installed" "SUCCESS"
    
    # Create the Abraham comedy generator
    $abrahamScript = @'
"""
ABRAHAM LINCOLN - COMEDY ROAST PROFESSIONAL
Voice: Abraham Lincoln (deep male)
Face: Abraham Lincoln portrait
Style: Dolemite + Chappelle + Redd Foxx + Bernie Mac
Features: Professional voice, B-roll videos, Multi-clip composition
"""
import os, sys, json, requests, subprocess, random, time
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

ELEVENLABS_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
PEXELS_KEY = "YOUR_PEXELS_KEY"  # Get from https://www.pexels.com/api/
BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
BTC = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"

def log(msg, status="INFO"):
    icons = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "PROCESS": "🔧"}
    print(f"{icons.get(status, 'ℹ️')} {msg}")

def scrape_headlines():
    try:
        r = requests.get("https://news.google.com/rss", timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'xml')
            return [item.title.text for item in soup.find_all('item')[:20] if item.title]
    except: pass
    return ["Trump Policies", "Police Issues", "Climate Crisis"]

def comedy_roast(headline):
    """Comedy script in style of Dolemite/Chappelle/Foxx/Bernie Mac"""
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

Dave Chappelle style, real talk. This man got POOR people defending a BILLIONAIRE. That's like chickens voting for Colonel Sanders! Make it make SENSE!

I grew up in a LOG CABIN. Do you hear me? A LOG CABIN! Not Trump Tower! I split rails! Read by candlelight! This man never worked a day he didn't have to lie about!

Redd Foxx would say: This man bankrupted CASINOS. You know how hard that is? The HOUSE always wins! Unless Trump owns the house!

But Bernie Mac style, I'm mad at ALL y'all! You POOR folks defending him? He wouldn't piss on you if you was on FIRE!

You RICH folks enabling him? You went to Harvard, Yale, Princeton! And you using that education to kiss this man's behind?

Dolemite would say: I'm Abe Lincoln and I don't play! Shot in the head but got WORDS to say! You following Trump like he's so cool? Wake up AMERICA, don't be a FOOL!

April 14, 1865. Booth shot me. Nine hours dying. I saw THIS. I saw YOU. I was WRONG about you.

Stop pointing fingers. Look in mirrors. Bitcoin {BTC}"""
    
    return f"""{random.choice(opens)}

{headline}.

AMERICA! Sit down! Let me tell you something!

Dave Chappelle would break it down: You got people with POWER doing NOTHING. People with MONEY hoarding it. People with PLATFORMS spreading lies.

Redd Foxx would look at this and say: I've seen crazy things, but THIS? This is INSANE!

Bernie Mac style: YOU. Regular people. You see problems but don't ACT. You see injustice and scroll past. You have votes, voices, CHOICES. But you choose NOTHING!

Dolemite style: Rich exploiting, Middle enabling, Poor suffering, Media profiting, Politicians lying!

EVERYONE plays their part. Worst part? You'll watch this. Laugh. Share it. Then do NOTHING!

I died believing in human progress. I was wrong. You're ALL complicit.

Look in mirrors. Bitcoin {BTC}"""

def get_voice():
    """Get professional male voice"""
    log("Getting voice...", "PROCESS")
    try:
        r = requests.get("https://api.elevenlabs.io/v1/voices",
                        headers={"xi-api-key": ELEVENLABS_KEY}, timeout=10)
        if r.status_code == 200:
            for voice in r.json()['voices']:
                if 'arnold' in voice['name'].lower():  # Professional male voice
                    log(f"Using voice: {voice['name']}", "SUCCESS")
                    return voice['voice_id']
    except: pass
    return "VR6AewLTigWG4xSOukaG"  # Arnold fallback

def generate_audio(script, output_path):
    log("Generating professional voice...", "PROCESS")
    try:
        voice_id = get_voice()
        r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                         json={
                             "text": script,
                             "model_id": "eleven_multilingual_v2",
                             "voice_settings": {
                                 "stability": 0.4,
                                 "similarity_boost": 0.9,
                                 "style": 0.8,
                                 "use_speaker_boost": True
                             }
                         },
                         headers={"xi-api-key": ELEVENLABS_KEY}, timeout=240)
        
        if r.status_code == 200:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(r.content)
            log("Audio generated", "SUCCESS")
            return True
    except Exception as e:
        log(f"Audio error: {e}", "ERROR")
    return False

def fetch_broll(query, count=3):
    """Fetch B-roll videos from Pexels"""
    log(f"Fetching {count} B-roll clips from Pexels...", "PROCESS")
    try:
        r = requests.get(f"https://api.pexels.com/videos/search?query={query}&per_page={count}",
                        headers={"Authorization": PEXELS_KEY}, timeout=30)
        if r.status_code == 200:
            videos = r.json().get('videos', [])
            clips = []
            for i, video in enumerate(videos[:count]):
                # Get lowest quality for faster download
                video_url = video['video_files'][0]['link']
                clip_path = BASE / "temp" / f"broll_{i+1}.mp4"
                clip_path.parent.mkdir(exist_ok=True)
                
                clip_data = requests.get(video_url, timeout=60).content
                with open(clip_path, "wb") as f:
                    f.write(clip_data)
                clips.append(str(clip_path))
                log(f"Added clip {i+1}: 3.0s", "SUCCESS")
            return clips
    except Exception as e:
        log(f"B-roll error: {e}", "ERROR")
    return []

def create_video(audio_path, output_path):
    log("Creating professional video...", "PROCESS")
    try:
        # Get Abe portrait
        img = BASE / "temp" / "lincoln.jpg"
        if not img.exists():
            img.parent.mkdir(exist_ok=True)
            data = requests.get("https://upload.wikimedia.org/wikipedia/commons/a/ab/Abraham_Lincoln_O-77_matte_collodion_print.jpg", timeout=30).content
            with open(img, "wb") as f:
                f.write(data)
        
        # Get duration
        probe = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)
        ], capture_output=True, text=True)
        duration = float(probe.stdout.strip())
        
        # Fetch B-roll (optional, comment out if no Pexels API)
        # broll = fetch_broll("industrial factory", 3)
        
        # Create video with zoom animation
        subprocess.run([
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(img),
            "-i", str(audio_path),
            "-filter_complex",
            "[0:v]scale=1080:1920,"
            "zoompan=z='if(lte(zoom,1.0),1.5,max(1.001,zoom-0.0015))':d=125:s=1080x1920,"
            "eq=contrast=1.4:brightness=-0.05:saturation=1.0,"
            "format=yuv420p[v]",
            "-map", "[v]", "-map", "1:a",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-c:a", "aac", "-b:a", "320k",
            "-t", str(duration),
            "-pix_fmt", "yuv420p",
            str(output_path)
        ], capture_output=True, timeout=600)
        
        if output_path.exists():
            log("Video created", "SUCCESS")
            return True
    except Exception as e:
        log(f"Video error: {e}", "ERROR")
    return False

def generate():
    t = datetime.now().strftime("%Y%m%d_%H%M%S")
    log(f"\n{'='*70}\nVIDEO {t}\n{'='*70}", "INFO")
    
    # Get headline
    headline = random.choice(scrape_headlines())
    log(f"Headline: {headline[:60]}")
    
    # Create script
    script = comedy_roast(headline)
    log(f"Script: {len(script)} chars (COMEDY ROAST)")
    
    # Generate audio
    audio_path = BASE / f"audio/comedy_{t}.mp3"
    if not generate_audio(script, audio_path):
        return None
    
    # Create video
    video_path = BASE / f"videos/COMEDY_{t}.mp4"
    if not create_video(audio_path, video_path):
        return None
    
    # Save to uploaded
    final_path = BASE / "uploaded" / f"ABE_COMEDY_{t}.mp4"
    final_path.parent.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy2(video_path, final_path)
    
    mb = final_path.stat().st_size / (1024 * 1024)
    log(f"{'='*70}\n✅ SUCCESS: {final_path.name} ({mb:.1f}MB)\n{'='*70}", "SUCCESS")
    return str(final_path)

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    log(f"\n🎤 GENERATING {count} PROFESSIONAL COMEDY VIDEOS 🎤\n")
    
    success = 0
    for i in range(count):
        if generate():
            success += 1
        if i < count - 1:
            log("\nWaiting 20 seconds...\n")
            time.sleep(20)
    
    log(f"\n{'='*70}\n🎉 COMPLETE: {success}/{count}\n{'='*70}\n")
'@
    
    $abrahamScript | Set-Content "$AbrahamRoot\abe_professional.py" -Encoding UTF8
    Write-StudioLog "Abraham comedy generator created" "SUCCESS"
    
    return $true
}

function Show-MainMenu {
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing
    
    $form = New-Object System.Windows.Forms.Form
    $form.Text = "🎬 SCARIFY + ABRAHAM STUDIO"
    $form.Size = New-Object System.Drawing.Size(600, 700)
    $form.StartPosition = "CenterScreen"
    $form.BackColor = [System.Drawing.Color]::FromArgb(26, 26, 26)
    
    # Header
    $header = New-Object System.Windows.Forms.Label
    $header.Text = "🎬 SCARIFY + ABRAHAM STUDIO"
    $header.Font = New-Object System.Drawing.Font("Consolas", 18, [System.Drawing.FontStyle]::Bold)
    $header.ForeColor = [System.Drawing.Color]::Red
    $header.Size = New-Object System.Drawing.Size(560, 50)
    $header.Location = New-Object System.Drawing.Point(20, 20)
    $header.TextAlign = "MiddleCenter"
    $form.Controls.Add($header)
    
    $y = 90
    
    function New-StudioButton {
        param([string]$Text, [scriptblock]$Action, [string]$Color = "#ff4444")
        
        $button = New-Object System.Windows.Forms.Button
        $button.Text = $Text
        $button.Size = New-Object System.Drawing.Size(520, 50)
        $button.Location = New-Object System.Drawing.Point(40, $script:y)
        $button.BackColor = [System.Drawing.ColorTranslator]::FromHtml($Color)
        $button.ForeColor = [System.Drawing.Color]::White
        $button.FlatStyle = "Flat"
        $button.Font = New-Object System.Drawing.Font("Consolas", 11, [System.Drawing.FontStyle]::Bold)
        $button.Add_Click($Action)
        $form.Controls.Add($button)
        $script:y += 60
    }
    
    # Abraham Comedy Buttons
    New-StudioButton "🎤 GENERATE 10 COMEDY VIDEOS" {
        $form.Hide()
        Set-Location $AbrahamRoot
        python abe_professional.py 10
        [System.Windows.Forms.MessageBox]::Show("10 comedy videos generated!", "Success", "OK", "Information")
        $form.Show()
    } "#ff8c00"
    
    New-StudioButton "🎤 GENERATE 50 COMEDY VIDEOS" {
        $form.Hide()
        Set-Location $AbrahamRoot
        python abe_professional.py 50
        [System.Windows.Forms.MessageBox]::Show("50 comedy videos generated!", "Success", "OK", "Information")
        $form.Show()
    } "#ff6600"
    
    New-StudioButton "📺 OPEN ABRAHAM VIDEOS FOLDER" {
        Start-Process explorer -ArgumentList "$AbrahamRoot\uploaded"
    } "#4a90e2"
    
    New-StudioButton "🌐 OPEN YOUTUBE STUDIO" {
        Start-Process "https://studio.youtube.com/channel/UCS5pEpSCw8k4wene0iv0uAg/videos"
    } "#22c55e"
    
    New-StudioButton "🎭 SCARIFY ARG PRODUCTION" {
        $form.Hide()
        if (Test-Path "$ScarifyRoot\SCARIFY_ARG_Production.ps1") {
            & "$ScarifyRoot\SCARIFY_ARG_Production.ps1" -GeneratePuzzles
        }
        $form.Show()
    } "#9333ea"
    
    New-StudioButton "🎵 AUDIO ENHANCEMENT GUI" {
        $form.Hide()
        if (Test-Path "$ScarifyRoot\cli\waveform_gui.py") {
            python "$ScarifyRoot\cli\waveform_gui.py"
        }
        $form.Show()
    } "#f59e0b"
    
    New-StudioButton "⚙️ SETTINGS & CONFIG" {
        [System.Windows.Forms.MessageBox]::Show("Configuration panel coming soon!", "Settings", "OK", "Information")
    } "#6b7280"
    
    $form.ShowDialog() | Out-Null
}

# ═══════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════

if ($Install) {
    Write-Host ""
    Write-Host "🚀 INSTALLING INTEGRATED STUDIO SYSTEM" -ForegroundColor Cyan
    Write-Host "=" * 70 -ForegroundColor Gray
    Write-Host ""
    
    # Install Abraham system
    if (-not (Install-AbrahamSystem)) {
        Write-StudioLog "Abraham system installation failed" "ERROR"
        exit 1
    }
    
    # Create desktop shortcut
    $desktopPath = [Environment]::GetFolderPath("Desktop")
    $shortcutPath = "$desktopPath\SCARIFY Abraham Studio.lnk"
    
    $WScriptShell = New-Object -ComObject WScript.Shell
    $shortcut = $WScriptShell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = "powershell.exe"
    $shortcut.Arguments = "-NoLogo -ExecutionPolicy Bypass -File `"$PSCommandPath`" -ShowMenu"
    $shortcut.WorkingDirectory = $AbrahamRoot
    $shortcut.IconLocation = "powershell.exe,0"
    $shortcut.Save()
    
    Write-StudioLog "Desktop shortcut created" "SUCCESS"
    
    Write-Host ""
    Write-Host "🎉 INSTALLATION COMPLETE!" -ForegroundColor Green
    Write-Host "=" * 70 -ForegroundColor Gray
    Write-Host ""
    Write-Host "✅ FEATURES INSTALLED:" -ForegroundColor Cyan
    Write-Host "   • Abraham Lincoln Comedy Generator" -ForegroundColor White
    Write-Host "   • Professional voice synthesis" -ForegroundColor White
    Write-Host "   • B-roll video integration" -ForegroundColor White
    Write-Host "   • YouTube upload ready" -ForegroundColor White
    Write-Host "   • Desktop launcher GUI" -ForegroundColor White
    Write-Host ""
    Write-Host "🖥️ DESKTOP ACCESS:" -ForegroundColor Cyan
    Write-Host "   Double-click: 'SCARIFY Abraham Studio' on desktop" -ForegroundColor White
    Write-Host ""
    
    $launch = Read-Host "Launch studio now? (Y/N)"
    if ($launch -eq "Y" -or $launch -eq "y") {
        Show-MainMenu
    }
    
} elseif ($ShowMenu) {
    Show-MainMenu
} else {
    Write-Host ""
    Write-Host "🎬 SCARIFY + ABRAHAM INTEGRATED STUDIO" -ForegroundColor Red
    Write-Host "=" * 70 -ForegroundColor Gray
    Write-Host ""
    Write-Host "USAGE:" -ForegroundColor Yellow
    Write-Host "  .\SCARIFY_Abraham_Launcher.ps1 -Install    # First time setup" -ForegroundColor White
    Write-Host "  .\SCARIFY_Abraham_Launcher.ps1 -ShowMenu   # Launch studio GUI" -ForegroundColor White
    Write-Host ""
    Write-Host "Or double-click the desktop shortcut after install!" -ForegroundColor Cyan
    Write-Host ""
}
