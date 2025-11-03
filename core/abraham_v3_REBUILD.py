#!/usr/bin/env python3
"""
ABRAHAM HORROR V3 - COMPLETE REBUILD
- Stability AI for Abraham Lincoln visuals
- GUARANTEED working audio
- Viral-optimized scripts
- Horror atmosphere
"""
import os, sys, json, requests, subprocess, random, time, base64
from pathlib import Path
from datetime import datetime
from io import BytesIO

# ═══════════════════════════════════════════════════════════════════════════
# API CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

ELEVENLABS_API_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
STABILITY_API_KEY = "sk-sP9331LezaVNYp1fbSDf9sn0rUaxhlr377fJ3V9V1t8wOEPQ1"
PEXELS_API_KEY = "RgE9Mdn3ToSQhn2RiLJ4mPMISjjp587QKRG9uhpOrLVtkKPCibUPUDGh"

# Better voice for Abraham Lincoln
VOICE_ID = "pNInz6obpgDQGcFmaJgB"  # Adam - deep, authoritative male

BASE_DIR = Path("F:/AI_Oracle_Root/scarify/abraham_horror")

# ═══════════════════════════════════════════════════════════════════════════
# VIRAL HEADLINES - October 28, 2025
# ═══════════════════════════════════════════════════════════════════════════

VIRAL_HEADLINES = [
    {
        'hook': "The storm that killed Jamaica",
        'headline': "Hurricane Melissa - Category 5 Apocalypse - 185mph Winds",
        'visual_prompt': "Abraham Lincoln ghost emerging from hurricane destruction, dramatic storm, dark apocalyptic, photorealistic",
        'keywords': "hurricane disaster storm"
    },
    {
        'hook': "They control your power. Forever.",
        'headline': "Sweden Power Grid Cyber Attack - Total Blackout Imminent",
        'visual_prompt': "Abraham Lincoln ghost in darkened city, power grid collapse, electrical sparks, dramatic lighting, photorealistic",
        'keywords': "blackout darkness power grid"
    },
    {
        'hook': "Your government sold you out",
        'headline': "US Data Breach - FEMA and CBP Records Exposed",
        'visual_prompt': "Abraham Lincoln ghost surrounded by burning government documents, data breach visualization, dark dramatic, photorealistic",
        'keywords': "government surveillance data"
    },
    {
        'hook': "The war spreads to your doorstep",
        'headline': "Gaza Airstrikes Escalate - 15 Dead in Israeli Attack",
        'visual_prompt': "Abraham Lincoln ghost in war-torn landscape, explosions, fire, dark dramatic, photorealistic",
        'keywords': "war fire explosions"
    },
    {
        'hook': "The flood that swallowed a nation",
        'headline': "Jamaica Floods - Bypass Bridges Destroyed - Island Submerged",
        'visual_prompt': "Abraham Lincoln ghost rising from flood waters, submerged city, dark dramatic, photorealistic",
        'keywords': "flood water disaster"
    }
]

# ═══════════════════════════════════════════════════════════════════════════
# VIRAL SCRIPT GENERATION
# ═══════════════════════════════════════════════════════════════════════════

def generate_viral_script(data):
    """Generate VIRAL horror script - optimized for watch time"""
    
    gore_variants = [
        "Booth's derringer exploded my skull. Brain matter painted the theatre walls crimson. Bone fragments embedded in velvet seats. My blood pooled on the presidential box floor.",
        "The bullet tore through my occiput. Grey matter sprayed across Mary's dress. Skull fragments scattered like shrapnel. I drowned in my own blood.",
        "Lead ball shattered my cranium. Cerebral cortex torn apart. Blood fountained from the wound. I died choking on brain tissue."
    ]
    
    prophecies = [
        f"As I died that night, I saw {data['headline']}. I saw YOUR future. The corruption metastasizes. The tyranny spreads. The darkness consumes.",
        f"My last vision before death: {data['headline']}. This is what I tried to prevent. The evil I fought returns stronger.",
        f"In my final breath, I witnessed {data['headline']}. The republic I saved collapses. The freedom I died for becomes chains."
    ]
    
    hook = data['hook']
    headline = data['headline']
    gore = random.choice(gore_variants)
    prophecy = random.choice(prophecies)
    
    script = f"""Listen closely. I am Abraham Lincoln.

{hook}

April 14th, 1865. Ford's Theatre. 10:15 PM. John Wilkes Booth climbs to my box. His derringer aims at my skull.

BANG.

{gore}

{prophecy}

Every lie you accept. Every freedom you surrender. Every compromise that rots the soul of this nation.

The Union I preserved fragments from within. The democracy I fought for drowns in corruption. The tyranny I warned against rises unchecked.

{headline}

This is not coincidence. This is the pattern. The evil compounds. The darkness spreads. And you... you let it happen.

From my blood-soaked seat in eternity, I watch America die.

Sic semper tyrannis. Thus always to tyrants.

But the question remains: Who are the tyrants now?

Look in the mirror.

You already know the answer."""

    return script

# ═══════════════════════════════════════════════════════════════════════════
# AUDIO GENERATION - FIXED METHOD
# ═══════════════════════════════════════════════════════════════════════════

def generate_audio_FIXED(script, output_path):
    """Generate audio with VERIFIED working output"""
    print(f"\n[AUDIO] Generating with ElevenLabs...")
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    data = {
        "text": script,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.9,
            "style": 0.9,
            "use_speaker_boost": True
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=180)
        
        if response.status_code != 200:
            print(f"[AUDIO] ❌ API error {response.status_code}")
            return False
        
        # Save audio
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        # Verify file
        size_kb = output_path.stat().st_size / 1024
        
        if size_kb < 10:
            print(f"[AUDIO] ❌ File too small: {size_kb:.1f} KB")
            return False
        
        # Verify it's valid audio with ffprobe
        probe = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', str(output_path)],
            capture_output=True, text=True
        )
        
        if probe.returncode != 0:
            print(f"[AUDIO] ❌ Invalid audio file")
            return False
        
        duration = float(probe.stdout.strip())
        
        if duration < 5:
            print(f"[AUDIO] ❌ Too short: {duration:.1f}s")
            return False
        
        print(f"[AUDIO] ✅ Success: {size_kb:.1f} KB, {duration:.1f}s")
        return True
        
    except Exception as e:
        print(f"[AUDIO] ❌ Error: {e}")
        return False

# ═══════════════════════════════════════════════════════════════════════════
# VISUAL GENERATION - STABILITY AI
# ═══════════════════════════════════════════════════════════════════════════

def generate_lincoln_visual(prompt):
    """Generate Abraham Lincoln visual with Stability AI"""
    print(f"\n[VISUAL] Generating Abraham Lincoln image...")
    
    url = "https://api.stability.ai/v2beta/stable-image/generate/core"
    
    headers = {
        "authorization": f"Bearer {STABILITY_API_KEY}",
        "accept": "image/*"
    }
    
    # Enhanced prompt for horror Lincoln
    full_prompt = f"{prompt}, 9:16 vertical aspect ratio, cinematic horror, dark dramatic lighting, high detail"
    
    files = {
        "prompt": (None, full_prompt),
        "output_format": (None, "png"),
        "aspect_ratio": (None, "9:16")
    }
    
    try:
        response = requests.post(url, headers=headers, files=files, timeout=120)
        
        if response.status_code == 200:
            temp_file = BASE_DIR / "temp" / f"lincoln_{random.randint(1000,9999)}.png"
            temp_file.parent.mkdir(exist_ok=True)
            
            with open(temp_file, 'wb') as f:
                f.write(response.content)
            
            size_kb = temp_file.stat().st_size / 1024
            print(f"[VISUAL] ✅ Stability AI: {size_kb:.1f} KB")
            return temp_file
        else:
            print(f"[VISUAL] ⚠️  Stability AI failed ({response.status_code}), falling back to Pexels")
            return None
            
    except Exception as e:
        print(f"[VISUAL] ⚠️  Stability error: {e}, falling back to Pexels")
        return None

def get_pexels_fallback(keywords):
    """Fallback: Get Pexels video if Stability fails"""
    print(f"[VISUAL] Using Pexels fallback...")
    
    try:
        url = "https://api.pexels.com/videos/search"
        headers = {"Authorization": PEXELS_API_KEY}
        params = {"query": keywords, "per_page": 1, "orientation": "portrait"}
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        data = response.json()
        
        if data.get('videos'):
            video = data['videos'][0]
            video_file = max(video['video_files'], key=lambda x: x.get('width', 0))
            download_url = video_file['link']
            
            video_data = requests.get(download_url, timeout=120).content
            temp_file = BASE_DIR / "temp" / f"pexels_{random.randint(1000,9999)}.mp4"
            
            with open(temp_file, 'wb') as f:
                f.write(video_data)
            
            print(f"[VISUAL] ✅ Pexels video downloaded")
            return temp_file
    except Exception as e:
        print(f"[VISUAL] ❌ Pexels failed: {e}")
    
    return None

# ═══════════════════════════════════════════════════════════════════════════
# VIDEO COMPOSITION - GUARANTEED AUDIO
# ═══════════════════════════════════════════════════════════════════════════

def compose_with_GUARANTEED_audio(visual_source, audio_path, output_path, is_image=False):
    """Compose video with GUARANTEED audio - tested and verified"""
    print(f"\n[COMPOSE] Combining visual + audio...")
    
    # Get audio duration
    try:
        probe = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)],
            capture_output=True, text=True, check=True
        )
        duration = float(probe.stdout.strip())
        print(f"[COMPOSE] Audio duration: {duration:.1f}s")
    except:
        print(f"[COMPOSE] ❌ Cannot read audio duration")
        return False
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if is_image:
        # Image source with Ken Burns zoom effect
        cmd = [
            'ffmpeg', '-loop', '1', '-i', str(visual_source),
            '-i', str(audio_path),
            '-vf', f"scale=1080:1920,zoompan=z='min(zoom+0.0015,1.5)':d={int(duration * 30)}:s=1080x1920,eq=contrast=1.4:brightness=-0.3:saturation=0.8",
            '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
            '-c:a', 'aac', '-b:a', '192k', '-ar', '44100',
            '-t', str(duration), '-pix_fmt', 'yuv420p',
            '-y', str(output_path)
        ]
    else:
        # Video source with explicit audio mapping
        cmd = [
            'ffmpeg',
            '-i', str(visual_source),
            '-i', str(audio_path),
            '-map', '0:v:0',  # Map video
            '-map', '1:a:0',  # Map audio
            '-vf', 'eq=contrast=1.4:brightness=-0.3,crop=1080:1920,scale=1080:1920',
            '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
            '-c:a', 'aac', '-b:a', '192k', '-ar', '44100',
            '-t', str(duration), '-shortest',
            '-y', str(output_path)
        ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=300)
        
        if not output_path.exists():
            print(f"[COMPOSE] ❌ Output file not created")
            return False
        
        # VERIFY audio exists in output
        probe = subprocess.run(
            ['ffprobe', '-v', 'error', '-select_streams', 'a:0',
             '-show_entries', 'stream=codec_name', '-of', 'default=noprint_wrappers=1:nokey=1',
             str(output_path)],
            capture_output=True, text=True
        )
        
        if 'aac' not in probe.stdout.lower():
            print(f"[COMPOSE] ❌ NO AUDIO IN OUTPUT!")
            return False
        
        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"[COMPOSE] ✅ Success: {size_mb:.2f} MB with audio")
        
        # Cleanup temp file
        visual_source.unlink()
        
        return True
        
    except subprocess.TimeoutExpired:
        print(f"[COMPOSE] ❌ FFmpeg timeout")
        return False
    except subprocess.CalledProcessError as e:
        print(f"[COMPOSE] ❌ FFmpeg error: {e.stderr[:200]}")
        return False
    except Exception as e:
        print(f"[COMPOSE] ❌ Error: {e}")
        return False

# ═══════════════════════════════════════════════════════════════════════════
# MAIN GENERATION
# ═══════════════════════════════════════════════════════════════════════════

def generate_video():
    """Generate complete video with VERIFIED audio"""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    print("\n" + "="*70)
    print("ABRAHAM HORROR V3 - COMPLETE REBUILD")
    print("="*70)
    
    # Select headline
    data = random.choice(VIRAL_HEADLINES)
    print(f"\n[HEADLINE] {data['headline']}")
    
    # Generate script
    script = generate_viral_script(data)
    print(f"[SCRIPT] {len(script)} characters")
    
    # Generate audio
    audio_path = BASE_DIR / f"audio/abraham_{timestamp}.mp3"
    if not generate_audio_FIXED(script, audio_path):
        print("\n❌ ABORT: Audio generation failed")
        return None
    
    # Try Stability AI first
    visual_source = generate_lincoln_visual(data['visual_prompt'])
    is_image = True
    
    # Fallback to Pexels if Stability fails
    if not visual_source:
        visual_source = get_pexels_fallback(data['keywords'])
        is_image = False
    
    if not visual_source:
        print("\n❌ ABORT: No visual source available")
        return None
    
    # Compose video
    video_path = BASE_DIR / f"videos/ABRAHAM_{timestamp}.mp4"
    if not compose_with_GUARANTEED_audio(visual_source, audio_path, video_path, is_image):
        print("\n❌ ABORT: Video composition failed")
        return None
    
    # Copy to YouTube folder
    youtube_file = BASE_DIR / "youtube_ready" / f"ABRAHAM_{timestamp}.mp4"
    youtube_file.parent.mkdir(exist_ok=True)
    
    import shutil
    shutil.copy2(video_path, youtube_file)
    
    size_mb = youtube_file.stat().st_size / (1024 * 1024)
    
    # Save metadata
    metadata = {
        'timestamp': datetime.now().isoformat(),
        'headline': data['headline'],
        'hook': data['hook'],
        'visual_method': 'stability_ai' if is_image else 'pexels',
        'file_size_mb': round(size_mb, 2),
        'audio_verified': True
    }
    
    with open(youtube_file.with_suffix('.json'), 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("\n" + "="*70)
    print("✅ SUCCESS - AUDIO VERIFIED")
    print("="*70)
    print(f"File: {youtube_file.name}")
    print(f"Size: {size_mb:.2f} MB")
    print(f"Visual: {metadata['visual_method']}")
    print("="*70 + "\n")
    
    return str(youtube_file)

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    
    print(f"\n🔥 GENERATING {count} VIDEO(S) - V3 REBUILD\n")
    
    success = 0
    failed = 0
    
    for i in range(count):
        print(f"\n{'='*70}")
        print(f"VIDEO {i+1}/{count}")
        print(f"{'='*70}")
        
        result = generate_video()
        
        if result:
            success += 1
        else:
            failed += 1
        
        if i < count - 1:
            print(f"\nWaiting 10 seconds before next video...")
            time.sleep(10)
    
    print(f"\n{'='*70}")
    print(f"COMPLETE: {success} success, {failed} failed")
    print(f"{'='*70}\n")
