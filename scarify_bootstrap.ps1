<#
================================================================================
    SCARIFY BOOTSTRAP - SELF-DEPLOYING SYSTEM
    Single-file deployment with everything inline
    No external dependencies required
================================================================================
#>

param(
    [int]$VideoCount = 1,
    [switch]$FullDeploy,
    [switch]$QuickTest,
    [string]$Archetype = "Mystic"
)

$ErrorActionPreference = "Continue"
$ProgressPreference = "SilentlyContinue"

# ============================================================================
# CONFIGURATION
# ============================================================================

$SCARIFY_ROOT = $PSScriptRoot
if ([string]::IsNullOrEmpty($SCARIFY_ROOT)) {
    $SCARIFY_ROOT = "F:\AI_Oracle_Root\scarify"
}

$CONFIG = @{
    ProjectName = "SCARIFY Auto-Deploy System"
    Version = "2.0-Bootstrap"
    Root = $SCARIFY_ROOT
    OutputDir = Join-Path $SCARIFY_ROOT "output"
    VideosDir = Join-Path $SCARIFY_ROOT "output\videos"
    AudioDir = Join-Path $SCARIFY_ROOT "output\audio"
    ScriptsDir = Join-Path $SCARIFY_ROOT "output\scripts"
    VenvDir = Join-Path $SCARIFY_ROOT "scarify_venv"
    LogFile = Join-Path $SCARIFY_ROOT "logs\bootstrap_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
}

# ============================================================================
# LOGGING
# ============================================================================

function Write-Log {
    param(
        [string]$Message,
        [string]$Level = "INFO",
        [ConsoleColor]$Color = "White"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    
    Write-Host $logMessage -ForegroundColor $Color
    
    if (Test-Path (Split-Path $CONFIG.LogFile)) {
        Add-Content -Path $CONFIG.LogFile -Value $logMessage -ErrorAction SilentlyContinue
    }
}

# ============================================================================
# HEADER
# ============================================================================

Clear-Host
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "    🔥 SCARIFY BOOTSTRAP - SELF-DEPLOYING SYSTEM 🔥" -ForegroundColor Red
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Log "Initializing SCARIFY Bootstrap v2.0" "INIT" Cyan
Write-Log "Root Directory: $($CONFIG.Root)" "INFO" White

# ============================================================================
# STEP 1: ENVIRONMENT CHECK
# ============================================================================

Write-Host "`n[STEP 1/6] Checking Prerequisites..." -ForegroundColor Yellow
Write-Log "Checking system prerequisites" "CHECK" Yellow

# Check Python
$pythonExists = $false
$pythonPath = $null

try {
    $pythonCmd = Get-Command python -ErrorAction Stop
    $pythonVersion = & python --version 2>&1
    $pythonPath = $pythonCmd.Source
    $pythonExists = $true
    Write-Log "✅ Python found: $pythonVersion at $pythonPath" "SUCCESS" Green
} catch {
    Write-Log "❌ Python not found - will attempt to use system Python" "WARN" Yellow
}

# Check ffmpeg
$ffmpegExists = $false
try {
    $ffmpegCmd = Get-Command ffmpeg -ErrorAction Stop
    $ffmpegVersion = & ffmpeg -version 2>&1 | Select-Object -First 1
    $ffmpegExists = $true
    Write-Log "✅ FFmpeg found: $ffmpegVersion" "SUCCESS" Green
} catch {
    Write-Log "⚠️  FFmpeg not found - video processing may be limited" "WARN" Yellow
}

# Check internet connectivity
try {
    $null = Test-Connection -ComputerName "8.8.8.8" -Count 1 -Quiet
    Write-Log "✅ Internet connectivity verified" "SUCCESS" Green
} catch {
    Write-Log "⚠️  No internet connection - some features may be limited" "WARN" Yellow
}

# ============================================================================
# STEP 2: CREATE DIRECTORY STRUCTURE
# ============================================================================

Write-Host "`n[STEP 2/6] Creating Directory Structure..." -ForegroundColor Yellow
Write-Log "Creating directory structure" "SETUP" Yellow

$directories = @(
    $CONFIG.OutputDir,
    $CONFIG.VideosDir,
    $CONFIG.AudioDir,
    $CONFIG.ScriptsDir,
    (Join-Path $SCARIFY_ROOT "logs"),
    (Join-Path $SCARIFY_ROOT "config"),
    (Join-Path $SCARIFY_ROOT "assets"),
    (Join-Path $SCARIFY_ROOT "assets\b-roll"),
    (Join-Path $SCARIFY_ROOT "temp")
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Log "Created: $dir" "CREATE" Green
    } else {
        Write-Log "Exists: $dir" "INFO" Gray
    }
}

# ============================================================================
# STEP 3: DEPLOY INLINE PYTHON SCRIPTS
# ============================================================================

Write-Host "`n[STEP 3/6] Deploying Inline Scripts..." -ForegroundColor Yellow
Write-Log "Creating embedded Python scripts" "DEPLOY" Yellow

# -------------------- MAIN GENERATOR SCRIPT --------------------
$PYTHON_GENERATOR = @'
"""
SCARIFY Video Generator - Inline Bootstrap Version
Generates videos with TTS audio and visual content
"""

import os
import sys
import json
import random
from datetime import datetime
from pathlib import Path

print("🚀 SCARIFY Video Generator v2.0")
print("=" * 50)

# ============================================================================
# CONFIGURATION
# ============================================================================

ROOT_DIR = Path(__file__).parent
OUTPUT_DIR = ROOT_DIR / "output"
VIDEOS_DIR = OUTPUT_DIR / "videos"
AUDIO_DIR = OUTPUT_DIR / "audio"
SCRIPTS_DIR = OUTPUT_DIR / "scripts"

# Ensure directories exist
for directory in [OUTPUT_DIR, VIDEOS_DIR, AUDIO_DIR, SCRIPTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# ============================================================================
# CONTENT ARCHETYPES
# ============================================================================

ARCHETYPES = {
    "Rebel": {
        "themes": [
            "Breaking free from conventional thinking",
            "Revolutionary ideas that challenge the status quo",
            "Question everything, accept nothing at face value",
            "Forge your own path, reject the herd mentality",
            "True freedom comes from independent thought"
        ],
        "colors": [(220, 20, 60), (139, 0, 0), (178, 34, 34)],
        "fonts": ["Arial-Bold", "Impact"],
        "style": "gritty, urban, revolutionary"
    },
    "Mystic": {
        "themes": [
            "Exploring consciousness beyond physical reality",
            "Journey into mystical dimensions and spiritual awakening",
            "Ancient wisdom for modern spiritual seekers",
            "Unlock the mysteries of the universe within",
            "Transcend the material, embrace the ethereal"
        ],
        "colors": [(75, 0, 130), (138, 43, 226), (147, 112, 219)],
        "fonts": ["Arial", "Georgia"],
        "style": "ethereal, mystical, cosmic"
    },
    "Sage": {
        "themes": [
            "Wisdom in the information age",
            "Cutting through noise to find timeless truths",
            "Practical insights for modern life challenges",
            "Ancient philosophy meets contemporary reality",
            "Knowledge is power, wisdom is freedom"
        ],
        "colors": [(70, 130, 180), (100, 149, 237), (65, 105, 225)],
        "fonts": ["Arial", "Times New Roman"],
        "style": "contemplative, intellectual, serene"
    },
    "Hero": {
        "themes": [
            "Rise above your limitations",
            "Every hero's journey starts with a single step",
            "Courage is not absence of fear, but action despite it",
            "Transform your trials into triumphs",
            "Become the hero of your own story"
        ],
        "colors": [(255, 215, 0), (255, 140, 0), (255, 69, 0)],
        "fonts": ["Arial-Bold", "Impact"],
        "style": "heroic, inspirational, dynamic"
    },
    "Guardian": {
        "themes": [
            "Protect what matters most",
            "Strength in service, power in protection",
            "Stand firm against chaos",
            "Vigilance is the price of safety",
            "Guard the vulnerable, defend the weak"
        ],
        "colors": [(34, 139, 34), (0, 100, 0), (85, 107, 47)],
        "fonts": ["Arial-Bold", "Georgia"],
        "style": "protective, strong, steadfast"
    }
}

# ============================================================================
# AUDIO GENERATION (FREE TTS)
# ============================================================================

def generate_audio_gtts(text, archetype="Mystic"):
    """Generate audio using Google Text-to-Speech (free)"""
    try:
        from gtts import gTTS
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        audio_file = AUDIO_DIR / f"tts_{archetype}_{timestamp}.mp3"
        
        print(f"🎵 Generating audio with gTTS...")
        print(f"   Text length: {len(text)} characters")
        
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(str(audio_file))
        
        if audio_file.exists():
            size = audio_file.stat().st_size
            print(f"✅ Audio created: {audio_file.name} ({size:,} bytes)")
            return str(audio_file)
        else:
            print("❌ Audio file not created")
            return None
            
    except ImportError:
        print("⚠️  gTTS not installed, attempting to install...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "gtts"])
            from gtts import gTTS
            return generate_audio_gtts(text, archetype)
        except:
            print("❌ Failed to install gTTS")
            return None
    except Exception as e:
        print(f"❌ Audio generation failed: {e}")
        return None

# ============================================================================
# VIDEO GENERATION (MOVIEPY)
# ============================================================================

def generate_video_moviepy(script_text, audio_file, archetype="Mystic"):
    """Generate video using MoviePy with text overlays"""
    try:
        from moviepy.editor import (
            ColorClip, TextClip, CompositeVideoClip, 
            AudioFileClip, concatenate_videoclips
        )
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        video_file = VIDEOS_DIR / f"scarify_{archetype}_{timestamp}.mp4"
        
        print(f"🎬 Generating video with MoviePy...")
        
        # Get archetype config
        arch_config = ARCHETYPES.get(archetype, ARCHETYPES["Mystic"])
        bg_color = random.choice(arch_config["colors"])
        
        # Get audio duration if available
        duration = 15  # default
        if audio_file and os.path.exists(audio_file):
            try:
                audio_clip = AudioFileClip(audio_file)
                duration = max(audio_clip.duration, 10)
            except:
                pass
        
        # Create background
        bg_clip = ColorClip(
            size=(1080, 1920), 
            color=bg_color, 
            duration=duration
        )
        
        # Split text into words for better display
        words = script_text.split()[:15]  # First 15 words
        display_text = " ".join(words)
        if len(words) >= 15:
            display_text += "..."
        
        # Create title text
        try:
            title_clip = TextClip(
                display_text,
                fontsize=60,
                color='white',
                font='Arial-Bold',
                size=(980, None),
                method='caption',
                align='center'
            )
            title_clip = title_clip.set_position('center').set_duration(duration)
            
            # Create archetype badge
            badge_clip = TextClip(
                f"⚡ {archetype.upper()} ⚡",
                fontsize=40,
                color='yellow',
                font='Arial-Bold'
            )
            badge_clip = badge_clip.set_position(('center', 200)).set_duration(duration)
            
            # Composite video
            video = CompositeVideoClip([bg_clip, title_clip, badge_clip])
            
        except Exception as e:
            print(f"⚠️  Text overlay failed: {e}")
            video = bg_clip
        
        # Add audio if available
        if audio_file and os.path.exists(audio_file):
            try:
                audio = AudioFileClip(audio_file)
                video = video.set_audio(audio)
                print("✅ Audio added to video")
            except Exception as e:
                print(f"⚠️  Could not add audio: {e}")
        
        # Export video
        print("📦 Rendering video...")
        video.write_videofile(
            str(video_file),
            fps=24,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None
        )
        
        if video_file.exists():
            size = video_file.stat().st_size
            print(f"✅ Video created: {video_file.name} ({size:,} bytes)")
            return str(video_file)
        else:
            print("❌ Video file not created")
            return None
            
    except ImportError as e:
        print(f"⚠️  MoviePy not installed: {e}")
        print("   Attempting to install...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy"])
            return generate_video_moviepy(script_text, audio_file, archetype)
        except:
            print("❌ Failed to install MoviePy")
            return None
    except Exception as e:
        print(f"❌ Video generation failed: {e}")
        import traceback
        traceback.print_exc()
        return None

# ============================================================================
# SIMPLE FALLBACK VIDEO (NO DEPENDENCIES)
# ============================================================================

def generate_simple_video(script_text, archetype="Mystic"):
    """Generate a simple MP4 using ffmpeg directly (no Python deps)"""
    try:
        import subprocess
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        video_file = VIDEOS_DIR / f"scarify_simple_{archetype}_{timestamp}.mp4"
        
        arch_config = ARCHETYPES.get(archetype, ARCHETYPES["Mystic"])
        color = random.choice(arch_config["colors"])
        color_hex = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
        
        print(f"🎬 Generating simple video with ffmpeg...")
        
        # Create color video with ffmpeg
        cmd = [
            "ffmpeg", "-f", "lavfi",
            "-i", f"color=c={color_hex}:s=1080x1920:d=15",
            "-vf", f"drawtext=text='{archetype.upper()}':fontcolor=white:fontsize=80:x=(w-text_w)/2:y=(h-text_h)/2",
            "-c:v", "libx264", "-t", "15", "-pix_fmt", "yuv420p",
            "-y", str(video_file)
        ]
        
        subprocess.run(cmd, capture_output=True, check=True)
        
        if video_file.exists():
            print(f"✅ Simple video created: {video_file.name}")
            return str(video_file)
        
        return None
        
    except Exception as e:
        print(f"❌ Simple video generation failed: {e}")
        return None

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def create_content(archetype="Mystic"):
    """Generate script content for archetype"""
    arch_data = ARCHETYPES.get(archetype, ARCHETYPES["Mystic"])
    theme = random.choice(arch_data["themes"])
    
    script = f"{theme} Discover deeper truths and expand your consciousness. " \
             f"This is your invitation to explore beyond the ordinary. " \
             f"Join the journey. Transform your reality."
    
    return script

def main():
    print("\n" + "="*50)
    print("Starting Video Generation Process")
    print("="*50 + "\n")
    
    # Parse command line arguments
    archetype = "Mystic"
    count = 1
    
    if len(sys.argv) > 1:
        archetype = sys.argv[1]
    if len(sys.argv) > 2:
        try:
            count = int(sys.argv[2])
        except:
            count = 1
    
    print(f"🎯 Archetype: {archetype}")
    print(f"🎯 Video Count: {count}")
    print()
    
    success_count = 0
    
    for i in range(count):
        if count > 1:
            print(f"\n{'='*50}")
            print(f"VIDEO {i+1}/{count}")
            print(f"{'='*50}\n")
        
        # Generate script
        script = create_content(archetype)
        print(f"📝 Script: {script[:100]}...")
        
        # Save script
        script_file = SCRIPTS_DIR / f"script_{archetype}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        script_file.write_text(script, encoding='utf-8')
        print(f"💾 Script saved: {script_file.name}")
        
        # Generate audio
        audio_file = generate_audio_gtts(script, archetype)
        
        # Generate video
        if audio_file:
            video_file = generate_video_moviepy(script, audio_file, archetype)
        else:
            print("⚠️  No audio, trying simple video...")
            video_file = generate_simple_video(script, archetype)
        
        if video_file:
            success_count += 1
            print(f"\n✅ VIDEO {i+1} COMPLETE!")
            print(f"   📹 {os.path.basename(video_file)}")
        else:
            print(f"\n❌ VIDEO {i+1} FAILED")
    
    # Summary
    print(f"\n{'='*50}")
    print(f"🎉 GENERATION COMPLETE")
    print(f"{'='*50}")
    print(f"✅ Success: {success_count}/{count}")
    print(f"📁 Output: {VIDEOS_DIR}")
    print()

if __name__ == "__main__":
    main()
'@

$generatorPath = Join-Path $SCARIFY_ROOT "scarify_bootstrap_generator.py"
$PYTHON_GENERATOR | Out-File -FilePath $generatorPath -Encoding UTF8
Write-Log "Created: scarify_bootstrap_generator.py" "CREATE" Green

# -------------------- REQUIREMENTS FILE --------------------
$REQUIREMENTS = @"
# SCARIFY Bootstrap Requirements
requests>=2.31.0
gtts>=2.4.0
moviepy>=1.0.3
Pillow>=10.0.0
numpy>=1.24.0
imageio>=2.31.0
imageio-ffmpeg>=0.4.9
"@

$requirementsPath = Join-Path $SCARIFY_ROOT "requirements_bootstrap.txt"
$REQUIREMENTS | Out-File -FilePath $requirementsPath -Encoding UTF8
Write-Log "Created: requirements_bootstrap.txt" "CREATE" Green

# ============================================================================
# STEP 4: INSTALL PYTHON DEPENDENCIES
# ============================================================================

Write-Host "`n[STEP 4/6] Installing Python Dependencies..." -ForegroundColor Yellow
Write-Log "Installing Python packages" "INSTALL" Yellow

if ($pythonExists) {
    try {
        Write-Log "Installing packages from requirements..." "INFO" White
        $installOutput = & python -m pip install -r $requirementsPath 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Log "✅ Dependencies installed successfully" "SUCCESS" Green
        } else {
            Write-Log "⚠️  Some packages may have failed to install" "WARN" Yellow
            Write-Log "Output: $installOutput" "DEBUG" Gray
        }
    } catch {
        Write-Log "⚠️  Dependency installation encountered issues: $_" "WARN" Yellow
    }
} else {
    Write-Log "⚠️  Python not available, skipping dependency installation" "WARN" Yellow
}

# ============================================================================
# STEP 5: CREATE CONFIGURATION FILES
# ============================================================================

Write-Host "`n[STEP 5/6] Creating Configuration..." -ForegroundColor Yellow
Write-Log "Creating configuration files" "CONFIG" Yellow

$configData = @{
    project_name = "SCARIFY Bootstrap"
    version = "2.0"
    root = $CONFIG.Root
    paths = @{
        output = $CONFIG.OutputDir
        videos = $CONFIG.VideosDir
        audio = $CONFIG.AudioDir
        scripts = $CONFIG.ScriptsDir
    }
    archetypes = @("Rebel", "Mystic", "Sage", "Hero", "Guardian")
    default_archetype = $Archetype
    video_settings = @{
        resolution = @{width = 1080; height = 1920}
        fps = 24
        duration = 15
    }
    deployed = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
} | ConvertTo-Json -Depth 10

$configPath = Join-Path $SCARIFY_ROOT "config\bootstrap_config.json"
New-Item -ItemType Directory -Path (Split-Path $configPath) -Force | Out-Null
$configData | Out-File -FilePath $configPath -Encoding UTF8
Write-Log "Created: bootstrap_config.json" "CREATE" Green

# ============================================================================
# STEP 6: GENERATE TEST VIDEO
# ============================================================================

if (-not $QuickTest) {
    Write-Host "`n[STEP 6/6] Generating Test Video..." -ForegroundColor Yellow
    Write-Log "Generating test video" "GENERATE" Yellow
    
    if ($pythonExists) {
        try {
            $args = @($generatorPath, $Archetype, $VideoCount)
            
            Write-Log "Running: python $($args -join ' ')" "INFO" White
            
            $process = Start-Process -FilePath "python" `
                                    -ArgumentList $args `
                                    -WorkingDirectory $SCARIFY_ROOT `
                                    -NoNewWindow `
                                    -Wait `
                                    -PassThru
            
            if ($process.ExitCode -eq 0) {
                Write-Log "✅ Video generation completed" "SUCCESS" Green
                
                # Check for generated videos
                $videos = Get-ChildItem -Path $CONFIG.VideosDir -Filter "*.mp4" -ErrorAction SilentlyContinue
                if ($videos) {
                    Write-Log "📹 Generated videos:" "INFO" Cyan
                    foreach ($video in $videos) {
                        $sizeMB = [math]::Round($video.Length / 1MB, 2)
                        Write-Log "   - $($video.Name) (${sizeMB}MB)" "INFO" White
                    }
                }
            } else {
                Write-Log "⚠️  Video generation returned exit code: $($process.ExitCode)" "WARN" Yellow
            }
        } catch {
            Write-Log "❌ Video generation failed: $_" "ERROR" Red
        }
    } else {
        Write-Log "⚠️  Python not available, skipping video generation" "WARN" Yellow
    }
} else {
    Write-Log "Quick test mode - skipping video generation" "INFO" Yellow
}

# ============================================================================
# DEPLOYMENT SUMMARY
# ============================================================================

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "    ✅ SCARIFY BOOTSTRAP DEPLOYMENT COMPLETE" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Log "Deployment Summary:" "SUMMARY" Cyan
Write-Log "  📁 Root: $($CONFIG.Root)" "INFO" White
Write-Log "  📹 Videos: $($CONFIG.VideosDir)" "INFO" White
Write-Log "  🎵 Audio: $($CONFIG.AudioDir)" "INFO" White
Write-Log "  📝 Scripts: $($CONFIG.ScriptsDir)" "INFO" White
Write-Log "  📊 Logs: $($CONFIG.LogFile)" "INFO" White
Write-Host ""

# Show next steps
Write-Host "🚀 NEXT STEPS:" -ForegroundColor Yellow
Write-Host "  1. Generate videos: python scarify_bootstrap_generator.py Mystic 5" -ForegroundColor White
Write-Host "  2. View output: explorer $($CONFIG.VideosDir)" -ForegroundColor White
Write-Host "  3. Re-run bootstrap: .\scarify_bootstrap.ps1 -VideoCount 10" -ForegroundColor White
Write-Host ""

# Quick launch option
if ($FullDeploy) {
    Write-Host "🎬 Launching video generator..." -ForegroundColor Cyan
    Start-Process -FilePath "python" `
                  -ArgumentList @($generatorPath, $Archetype, "5") `
                  -WorkingDirectory $SCARIFY_ROOT
}

Write-Log "Bootstrap complete!" "DONE" Green
Write-Host ""

