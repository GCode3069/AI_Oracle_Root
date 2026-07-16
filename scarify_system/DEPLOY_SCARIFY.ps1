# SCARIFY System - Complete PowerShell Deployment
# Run this script to deploy all 6 Python scripts to D:\AI_Oracle_Projects

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "SCARIFY VIDEO GENERATION SYSTEM - DEPLOYMENT" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# Create directories
Write-Host "`nCreating directory structure..." -ForegroundColor Yellow
$dirs = @(
    "D:\AI_Oracle_Projects\Active\Scripts",
    "D:\AI_Oracle_Projects\Assets\Kling_Cache",
    "D:\AI_Oracle_Projects\Assets\Portraits",
    "D:\AI_Oracle_Projects\Output\Generated\Winners",
    "D:\AI_Oracle_Projects\Output\Generated\Comedy"
)

foreach ($dir in $dirs) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  ✅ Created: $dir" -ForegroundColor Green
    }
}

# Script 1: DUAL_STYLE_GENERATOR.py
Write-Host "`n[1/6] Deploying DUAL_STYLE_GENERATOR.py..." -ForegroundColor Yellow
$script1 = @'
# DUAL_STYLE_GENERATOR.py
import random

WARNING_TEMPLATES = {
    "Education": [
        {"title": "WARNING: Your School Is Teaching This", "hook": "They don't want you to know what's really in the curriculum..."},
        {"title": "URGENT: What They're Not Teaching Your Kids", "hook": "The education system is hiding something crucial..."},
        {"title": "ALERT: This Is What Schools Are Actually Doing", "hook": "Behind closed doors, education has changed dramatically..."},
        {"title": "WARNING: The Real Purpose of Modern Education", "hook": "I preserved the Union. Now watch what they're doing..."},
        {"title": "CRISIS: What Happened to American Education", "hook": "We fought a war to free minds. Now they're imprisoning them..."}
    ],
    "Military": [
        {"title": "WARNING: What They're Doing to Our Military", "hook": "I led armies in our darkest hour. What I'm seeing now..."},
        {"title": "URGENT: The Truth About Military Recruitment", "hook": "They can't find soldiers anymore. Here's why..."},
        {"title": "ALERT: What's Happening at Military Bases", "hook": "Behind the fences, something has changed..."},
        {"title": "WARNING: America's Military Readiness", "hook": "We preserved this nation through blood. Watch what they've done..."},
        {"title": "CRISIS: Why Veterans Are Speaking Out", "hook": "Those who served are trying to tell you something..."}
    ],
    "Government": [
        {"title": "WARNING: What Congress Just Did", "hook": "While you weren't watching, they made a critical decision..."},
        {"title": "URGENT: The Bill They Don't Want You to Read", "hook": "Buried in 2,000 pages is something they hoped you'd miss..."},
        {"title": "ALERT: How Your Government Changed", "hook": "I governed with transparency. Now watch what they're hiding..."},
        {"title": "WARNING: What Politicians Aren't Telling You", "hook": "Behind closed doors, the conversation is very different..."},
        {"title": "CRISIS: Why Trust in Government Is Collapsing", "hook": "The people are losing faith. Here's what caused it..."}
    ],
    "Economy": [
        {"title": "WARNING: What They're Not Telling You About Inflation", "hook": "Your money is disappearing faster than they admit..."},
        {"title": "URGENT: The Economic Crisis They're Hiding", "hook": "Behind the stock market, something is breaking..."},
        {"title": "ALERT: What's Really Happening to Your Paycheck", "hook": "You're working more. Earning less. Here's why..."},
        {"title": "WARNING: The Debt Crisis No One Is Addressing", "hook": "I preserved the nation. Now they're bankrupting it..."},
        {"title": "CRISIS: Why the Middle Class Is Disappearing", "hook": "The foundation of America is crumbling..."}
    ]
}

COMEDY_TEMPLATES = [
    {"title": "Lincoln Watches TikTok", "hook": "I'm dead. Been dead since 1865. And I'm watching your app..."},
    {"title": "Lincoln Roasts Student Debt", "hook": "Y'all got slavery 2.0. It's called student loans..."},
    {"title": "Lincoln Tries WiFi", "hook": "I freed the slaves but can't free myself from this loading screen..."},
    {"title": "Lincoln Reviews Congress", "hook": "I was president during CIVIL WAR. Your Congress can't agree on lunch..."},
    {"title": "Lincoln Roasts Inflation", "hook": "A penny used to mean something. Now it costs MORE than a penny to MAKE a penny..."}
]

def generate_video_concept():
    """Generate concept with 70% WARNING, 30% COMEDY split"""
    is_warning = random.random() < 0.70
    
    if is_warning:
        # WARNING format (70%)
        weights = {"Education": 0.30, "Military": 0.30, "Government": 0.20, "Economy": 0.20}
        category = random.choices(list(weights.keys()), weights=list(weights.values()))[0]
        template = random.choice(WARNING_TEMPLATES[category])
        
        script = f"{template['hook']}\n\nListen. I died for this country. I was shot at Ford's Theatre.\n\nThis isn't theory. This is happening RIGHT NOW.\n\nI preserved the Union. Don't let them destroy it from within."
        
        return {
            "style": "WARNING",
            "category": category,
            "title": template["title"],
            "hook": template["hook"],
            "script": script,
            "duration": random.randint(25, 45)
        }
    else:
        # COMEDY format (30%)
        template = random.choice(COMEDY_TEMPLATES)
        
        script = f"{template['hook']}\n\nY'all wanna know what I think?\n\nI was president during a CIVIL WAR. We had actual problems.\n\nI'm not mad. I'm just disappointed. And confused."
        
        return {
            "style": "COMEDY",
            "category": "Entertainment",
            "title": template["title"],
            "hook": template["hook"],
            "script": script,
            "duration": random.randint(25, 35)
        }

if __name__ == "__main__":
    for i in range(10):
        concept = generate_video_concept()
        print(f"{i+1}. {concept['style']:7} - {concept['title']}")
'@

$script1 | Out-File "D:\AI_Oracle_Projects\Active\Scripts\DUAL_STYLE_GENERATOR.py" -Encoding UTF8
Write-Host "  ✅ DUAL_STYLE_GENERATOR.py deployed" -ForegroundColor Green

# Script 2: KLING_CLIENT.py
Write-Host "`n[2/6] Deploying KLING_CLIENT.py..." -ForegroundColor Yellow
$script2 = @'
# KLING_CLIENT.py
import requests
import time
from API_KEYS import KLING_API_KEY

def generate_talking_head(audio_path, image_path):
    """Generate lip-sync video with Kling AI"""
    print(f"🗣️ Generating lip-sync with Kling AI...")
    
    # Upload files
    with open(audio_path, 'rb') as af, open(image_path, 'rb') as imf:
        files = {'audio': af, 'image': imf}
        headers = {'Authorization': f'Bearer {KLING_API_KEY}'}
        
        # Start generation
        response = requests.post(
            'https://api.klingai.com/v1/videos/generations',
            headers=headers,
            files=files,
            data={'duration': 'auto'}
        )
        
        if response.status_code != 200:
            raise Exception(f"Kling API error: {response.text}")
        
        task_id = response.json()['task_id']
        print(f"   Task ID: {task_id}")
    
    # Poll for completion
    for i in range(60):
        time.sleep(10)
        check_response = requests.get(
            f'https://api.klingai.com/v1/videos/generations/{task_id}',
            headers=headers
        )
        
        status = check_response.json()['status']
        print(f"   Status: {status} ({i*10}s elapsed)")
        
        if status == 'completed':
            video_url = check_response.json()['video_url']
            
            # Download video
            video_data = requests.get(video_url).content
            output_path = audio_path.replace('.mp3', '_lipsync.mp4')
            
            with open(output_path, 'wb') as f:
                f.write(video_data)
            
            print(f"✅ Lip-sync complete: {output_path}")
            return output_path
        
        elif status == 'failed':
            raise Exception(f"Kling generation failed")
    
    raise Exception("Kling timeout after 600 seconds")

if __name__ == "__main__":
    print("KLING_CLIENT.py - Ready for Kling AI lip-sync generation")
'@

$script2 | Out-File "D:\AI_Oracle_Projects\Active\Scripts\KLING_CLIENT.py" -Encoding UTF8
Write-Host "  ✅ KLING_CLIENT.py deployed" -ForegroundColor Green

# Script 3: KLING_CACHE.py
Write-Host "`n[3/6] Deploying KLING_CACHE.py..." -ForegroundColor Yellow
$script3 = @'
# KLING_CACHE.py
import os
import json
import hashlib
import shutil
from pathlib import Path

class KlingCache:
    """MD5-based caching - saves $0.04 per reuse!"""
    
    def __init__(self, cache_dir="D:/AI_Oracle_Projects/Assets/Kling_Cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = self.cache_dir / "cache_index.json"
        self.index = self._load_index()
    
    def _load_index(self):
        if self.index_file.exists():
            with open(self.index_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_index(self):
        with open(self.index_file, 'w') as f:
            json.dump(self.index, f, indent=2)
    
    def _compute_hash(self, audio_path, image_path):
        """MD5 hash of audio + image"""
        hasher = hashlib.md5()
        with open(audio_path, 'rb') as f:
            hasher.update(f.read())
        with open(image_path, 'rb') as f:
            hasher.update(f.read())
        return hasher.hexdigest()
    
    def check_cache(self, audio_path, image_path):
        """Check if video exists in cache - ALWAYS call this BEFORE Kling API!"""
        cache_hash = self._compute_hash(audio_path, image_path)
        
        if cache_hash in self.index:
            entry = self.index[cache_hash]
            video_path = entry["video_path"]
            
            if os.path.exists(video_path):
                entry["reuse_count"] = entry.get("reuse_count", 0) + 1
                self._save_index()
                
                cost_saved = entry["reuse_count"] * 0.04
                print(f"💾 CACHE HIT! Reused {entry['reuse_count']} times (${cost_saved:.2f} saved)")
                return video_path
        
        print(f"❌ Cache miss - will generate new video")
        return None
    
    def save_to_cache(self, video_path, audio_path, image_path):
        """Save generated video to cache"""
        cache_hash = self._compute_hash(audio_path, image_path)
        cache_dir = self.cache_dir / cache_hash
        cache_dir.mkdir(exist_ok=True)
        
        cached_video = cache_dir / "video.mp4"
        shutil.copy2(video_path, cached_video)
        
        self.index[cache_hash] = {
            "video_path": str(cached_video),
            "reuse_count": 0,
            "hash": cache_hash
        }
        self._save_index()
        print(f"💾 Saved to cache: {cache_hash[:8]}...")
    
    def get_stats(self):
        """Get cache statistics"""
        total_entries = len(self.index)
        total_reuses = sum(e.get("reuse_count", 0) for e in self.index.values())
        cost_saved = total_reuses * 0.04
        
        return {
            "entries": total_entries,
            "reuses": total_reuses,
            "cost_saved": cost_saved
        }

if __name__ == "__main__":
    cache = KlingCache()
    stats = cache.get_stats()
    print(f"Cache entries: {stats['entries']}")
    print(f"Total reuses: {stats['reuses']}")
    print(f"Cost saved: ${stats['cost_saved']:.2f}")
'@

$script3 | Out-File "D:\AI_Oracle_Projects\Active\Scripts\KLING_CACHE.py" -Encoding UTF8
Write-Host "  ✅ KLING_CACHE.py deployed" -ForegroundColor Green

# Script 4: SUBLIMINAL_AUDIO.py
Write-Host "`n[4/6] Deploying SUBLIMINAL_AUDIO.py..." -ForegroundColor Yellow
$script4 = @'
# SUBLIMINAL_AUDIO.py
import numpy as np
from scipy.io import wavfile
import subprocess
from pathlib import Path

def generate_binaural_beat(duration, sample_rate=44100):
    """Generate 10Hz alpha wave binaural beat at -20dB"""
    t = np.linspace(0, duration, int(sample_rate * duration))
    left = 0.1 * np.sin(2 * np.pi * 200 * t)  # Base 200Hz
    right = 0.1 * np.sin(2 * np.pi * 210 * t)  # 210Hz (10Hz beat)
    return np.column_stack((left, right))

def generate_attention_tone(duration, sample_rate=44100):
    """Generate 528Hz Solfeggio frequency at -25dB"""
    t = np.linspace(0, duration, int(sample_rate * duration))
    tone = 0.056 * np.sin(2 * np.pi * 528 * t)
    return np.column_stack((tone, tone))

def generate_vhs_hiss(duration, sample_rate=44100):
    """Generate VHS tape hiss at -30dB"""
    samples = int(sample_rate * duration)
    return np.random.normal(0, 0.032, (samples, 2))

def mix_subliminal_audio(voice_path, duration):
    """Mix voice with subliminal layers using FFmpeg"""
    print(f"🎵 Adding subliminal audio layers...")
    
    temp_dir = Path("temp_audio")
    temp_dir.mkdir(exist_ok=True)
    
    # Generate layers
    sample_rate = 44100
    binaural = generate_binaural_beat(duration, sample_rate)
    attention = generate_attention_tone(duration, sample_rate)
    hiss = generate_vhs_hiss(duration, sample_rate)
    
    # Save as WAV files
    def save_wav(audio, path):
        audio_int16 = (np.clip(audio, -1, 1) * 32767).astype(np.int16)
        wavfile.write(path, sample_rate, audio_int16)
    
    save_wav(binaural, temp_dir / "binaural.wav")
    save_wav(attention, temp_dir / "attention.wav")
    save_wav(hiss, temp_dir / "hiss.wav")
    
    # Mix with FFmpeg
    output_path = voice_path.replace('.mp3', '_mixed.mp3')
    
    cmd = [
        'ffmpeg', '-y',
        '-i', voice_path,
        '-i', str(temp_dir / "binaural.wav"),
        '-i', str(temp_dir / "attention.wav"),
        '-i', str(temp_dir / "hiss.wav"),
        '-filter_complex',
        '[0:a]volume=1.0[v];[1:a]volume=0.1[b];[2:a]volume=0.056[a];[3:a]volume=0.032[h];[v][b][a][h]amix=inputs=4:duration=first',
        '-ac', '2',
        output_path
    ]
    
    subprocess.run(cmd, capture_output=True, check=True)
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)
    
    print(f"   ✅ Subliminal audio mixed: {output_path}")
    return output_path

if __name__ == "__main__":
    print("SUBLIMINAL_AUDIO.py - Ready to add binaural beats")
'@

$script4 | Out-File "D:\AI_Oracle_Projects\Active\Scripts\SUBLIMINAL_AUDIO.py" -Encoding UTF8
Write-Host "  ✅ SUBLIMINAL_AUDIO.py deployed" -ForegroundColor Green

# Script 5: VIDEO_LAYOUT.py
Write-Host "`n[5/6] Deploying VIDEO_LAYOUT.py..." -ForegroundColor Yellow
$script5 = @'
# VIDEO_LAYOUT.py
import subprocess
from pathlib import Path

def create_pip_layout(video_path, title, style):
    """Create 1080x1920 vertical layout with title overlay and VHS effects"""
    print(f"🎬 Creating {style} layout...")
    
    output_path = video_path.replace('.mp4', '_layout.mp4')
    
    # Escape title for FFmpeg
    title_escaped = title.replace("'", "'\\''").replace(":", "\\:")
    
    # Style settings
    if style == "WARNING":
        font_size = 44
        font_color = "white"
        box_color = "black@0.6"
    else:  # COMEDY
        font_size = 42
        font_color = "yellow"
        box_color = "black@0.5"
    
    # FFmpeg filter: scale to 720x1280, center on 1080x1920 canvas, add title
    filter_complex = (
        f"[0:v]scale=720:1280:force_original_aspect_ratio=decrease,"
        f"pad=720:1280:(ow-iw)/2:(oh-ih)/2[scaled];"
        f"color=c=black:s=1080x1920:d=10[bg];"
        f"[bg][scaled]overlay=180:320[with_video];"
        f"[with_video]drawtext="
        f"text='{title_escaped}':"
        f"fontsize={font_size}:"
        f"fontcolor={font_color}:"
        f"x=(w-text_w)/2:"
        f"y=100:"
        f"box=1:"
        f"boxcolor={box_color}:"
        f"boxborderw=10,"
        f"noise=alls=3:allf=t,"
        f"vignette=angle=PI/2[output]"
    )
    
    cmd = [
        'ffmpeg', '-y',
        '-i', video_path,
        '-filter_complex', filter_complex,
        '-map', '[output]',
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-pix_fmt', 'yuv420p',
        output_path
    ]
    
    subprocess.run(cmd, capture_output=True, check=True)
    print(f"   ✅ Layout created: {output_path}")
    return output_path

if __name__ == "__main__":
    print("VIDEO_LAYOUT.py - Ready to create 1080x1920 layouts")
'@

$script5 | Out-File "D:\AI_Oracle_Projects\Active\Scripts\VIDEO_LAYOUT.py" -Encoding UTF8
Write-Host "  ✅ VIDEO_LAYOUT.py deployed" -ForegroundColor Green

# Script 6: SCARIFY_COMPLETE.py
Write-Host "`n[6/6] Deploying SCARIFY_COMPLETE.py..." -ForegroundColor Yellow
$script6 = @'
# SCARIFY_COMPLETE.py - Complete 9-step pipeline
import os
import time
from pathlib import Path
from elevenlabs import generate, save

from DUAL_STYLE_GENERATOR import generate_video_concept
from KLING_CLIENT import generate_talking_head
from KLING_CACHE import KlingCache
from SUBLIMINAL_AUDIO import mix_subliminal_audio
from VIDEO_LAYOUT import create_pip_layout
from API_KEYS import ELEVENLABS_API_KEY

# Initialize
cache = KlingCache()
portraits = list(Path("D:/AI_Oracle_Projects/Assets/Portraits").glob("*.jpg"))
portrait_index = 0

def get_portrait():
    """Get portrait with 80% reuse rate"""
    import random
    global portrait_index
    if random.random() > 0.80:
        portrait_index = (portrait_index + 1) % len(portraits)
    return str(portraits[portrait_index])

def generate_complete_video():
    """Complete 9-step pipeline"""
    start_time = time.time()
    
    print("\n" + "="*60)
    print("SCARIFY VIDEO GENERATION PIPELINE")
    print("="*60)
    
    # Step 1: Generate concept
    print("\n[1/9] Generating concept...")
    concept = generate_video_concept()
    print(f"   Style: {concept['style']}")
    print(f"   Title: {concept['title']}")
    
    # Step 2: Script ready
    print("\n[2/9] Script ready")
    script = concept['script']
    
    # Step 3: Synthesize voice
    print("\n[3/9] Synthesizing voice with ElevenLabs...")
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    
    voice_path = temp_dir / "voice.mp3"
    audio = generate(text=script, voice="Rachel", api_key=ELEVENLABS_API_KEY)
    save(audio, str(voice_path))
    print(f"   ✅ Voice saved: {voice_path}")
    
    # Step 4: Add subliminal audio
    print("\n[4/9] Adding subliminal audio layers...")
    try:
        mixed_audio = mix_subliminal_audio(str(voice_path), concept['duration'])
    except:
        mixed_audio = str(voice_path)
        print("   ⚠️ Skipped subliminal mixing (FFmpeg required)")
    
    # Step 5: Get portrait
    print("\n[5/9] Selecting portrait...")
    portrait = get_portrait()
    print(f"   Portrait: {Path(portrait).name}")
    
    # Step 6: Check cache FIRST, then generate if needed
    print("\n[6/9] Checking Kling cache...")
    cached_video = cache.check_cache(mixed_audio, portrait)
    
    if cached_video:
        lipsync_video = cached_video
    else:
        print("   Generating lip-sync video (this costs $0.04)...")
        lipsync_video = generate_talking_head(mixed_audio, portrait)
        cache.save_to_cache(lipsync_video, mixed_audio, portrait)
    
    # Step 7: Create layout
    print("\n[7/9] Creating picture-in-picture layout...")
    layout_video = create_pip_layout(lipsync_video, concept['title'], concept['style'])
    
    # Step 8: VHS effects (applied in layout)
    print("\n[8/9] VHS effects applied ✅")
    
    # Step 9: Save to output
    print("\n[9/9] Saving to output directory...")
    
    if concept['style'] == "WARNING":
        output_dir = Path("D:/AI_Oracle_Projects/Output/Generated/Winners")
    else:
        output_dir = Path("D:/AI_Oracle_Projects/Output/Generated/Comedy")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    safe_title = "".join(c for c in concept['title'] if c.isalnum() or c in ' -_')[:50]
    video_id = int(time.time())
    final_path = output_dir / f"scarify_{video_id}_{safe_title}.mp4"
    
    import shutil
    shutil.copy2(layout_video, final_path)
    
    elapsed = time.time() - start_time
    
    print(f"\n{'='*60}")
    print(f"✅ VIDEO COMPLETE!")
    print(f"{'='*60}")
    print(f"Output: {final_path}")
    print(f"Time: {elapsed:.1f}s")
    print(f"Style: {concept['style']}")
    print(f"{'='*60}\n")
    
    return final_path

def generate_batch(count):
    """Generate multiple videos"""
    print(f"\n{'='*60}")
    print(f"BATCH GENERATION: {count} VIDEOS")
    print(f"{'='*60}\n")
    
    videos = []
    for i in range(count):
        print(f"\n[VIDEO {i+1}/{count}]")
        try:
            video = generate_complete_video()
            videos.append(video)
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n{'='*60}")
    print(f"BATCH COMPLETE: {len(videos)}/{count} successful")
    print(f"{'='*60}\n")
    
    # Show cache stats
    stats = cache.get_stats()
    print(f"Cache entries: {stats['entries']}")
    print(f"Total reuses: {stats['reuses']}")
    print(f"Cost saved: ${stats['cost_saved']:.2f}\n")
    
    return videos

if __name__ == "__main__":
    print("SCARIFY_COMPLETE.py - Full 9-step pipeline ready")
    print("Usage:")
    print("  generate_complete_video()  # Generate 1 video")
    print("  generate_batch(10)         # Generate 10 videos")
'@

$script6 | Out-File "D:\AI_Oracle_Projects\Active\Scripts\SCARIFY_COMPLETE.py" -Encoding UTF8
Write-Host "  ✅ SCARIFY_COMPLETE.py deployed" -ForegroundColor Green

# API_KEYS.py template
Write-Host "`n[BONUS] Creating API_KEYS.py template..." -ForegroundColor Yellow
$apikeys = @'
# API_KEYS.py
# Edit this file with your actual API keys

# Get from: https://klingai.com/
KLING_API_KEY = "your_kling_api_key_here"

# Get from: https://elevenlabs.io/
ELEVENLABS_API_KEY = "your_elevenlabs_api_key_here"

# Configuration
WARNING_RATIO = 0.70  # 70% WARNING format
COMEDY_RATIO = 0.30   # 30% COMEDY format
PORTRAIT_REUSE_RATE = 0.80  # Reuse portrait 80% of time
'@

$apikeys | Out-File "D:\AI_Oracle_Projects\Active\Scripts\API_KEYS.py" -Encoding UTF8
Write-Host "  ✅ API_KEYS.py template created" -ForegroundColor Green

# Summary
Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "✅ DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "All 6 scripts deployed to:" -ForegroundColor White
Write-Host "  D:\AI_Oracle_Projects\Active\Scripts\" -ForegroundColor Yellow
Write-Host ""
Write-Host "📋 NEXT STEPS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Edit API_KEYS.py with your actual keys:" -ForegroundColor White
Write-Host "   notepad D:\AI_Oracle_Projects\Active\Scripts\API_KEYS.py" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Add 5-10 Abraham Lincoln portraits to:" -ForegroundColor White
Write-Host "   D:\AI_Oracle_Projects\Assets\Portraits\" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Install Python dependencies:" -ForegroundColor White
Write-Host "   pip install requests numpy scipy elevenlabs" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Install FFmpeg (required):" -ForegroundColor White
Write-Host "   choco install ffmpeg" -ForegroundColor Gray
Write-Host ""
Write-Host "5. Test the system:" -ForegroundColor White
Write-Host "   cd D:\AI_Oracle_Projects\Active\Scripts" -ForegroundColor Gray
Write-Host "   python DUAL_STYLE_GENERATOR.py" -ForegroundColor Gray
Write-Host ""
Write-Host "6. Generate first video:" -ForegroundColor White
Write-Host "   python -c ""from SCARIFY_COMPLETE import generate_complete_video; generate_complete_video()""" -ForegroundColor Gray
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "System ready! Good luck with your videos! 🎬" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
