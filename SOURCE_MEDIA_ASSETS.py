#!/usr/bin/env python3
"""
SCARIFY - Media Asset Sourcing
Downloads kitchen footage, drone shots, and generates theta audio SFX
"""

import os, sys, json, requests, random
from pathlib import Path
import subprocess

BASE_DIR = Path("F:/AI_Oracle_Root/scarify")
ASSETS_DIR = BASE_DIR / "abraham_horror" / "assets"
AUDIO_SFX_DIR = ASSETS_DIR / "audio_sfx"
BROLL_DIR = ASSETS_DIR / "broll"

for d in [ASSETS_DIR, AUDIO_SFX_DIR, BROLL_DIR]:
    d.mkdir(parents=True, exist_ok=True)

PEXELS_API_KEY = "RgE9Mdn3ToSQhn2RiLJ4mPMISjjp587QKRG9uhpOrLVtkKPCibUPUDGh"

# B-roll search queries
BROLL_QUERIES = [
    "kitchen cooking dark moody",
    "industrial factory machinery",
    "city streets night crime",
    "hospital emergency medical",
    "government building corruption",
    "stock market crash",
    "nuclear power plant",
    "cybersecurity hacking",
    "military warfare",
    "abandoned building decay"
]

def download_pexels_broll(query, count=5):
    """Download B-roll footage from Pexels"""
    
    print(f"\n[PEXELS] Searching: {query}")
    
    try:
        response = requests.get(
            "https://api.pexels.com/videos/search",
            headers={"Authorization": PEXELS_API_KEY},
            params={
                "query": query,
                "per_page": count,
                "orientation": "portrait"
            },
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"[ERROR] API returned {response.status_code}")
            return []
        
        data = response.json()
        videos = data.get('videos', [])
        
        if not videos:
            print(f"[WARNING] No videos found for: {query}")
            return []
        
        downloaded = []
        
        for i, video in enumerate(videos, 1):
            # Get best quality file
            video_files = video.get('video_files', [])
            if not video_files:
                continue
            
            # Find portrait/vertical video
            portrait_files = [f for f in video_files if f.get('width', 0) < f.get('height', 0)]
            if not portrait_files:
                portrait_files = video_files
            
            # Get highest quality
            best_file = max(portrait_files, key=lambda x: x.get('width', 0))
            download_url = best_file.get('link')
            
            if not download_url:
                continue
            
            # Download
            safe_query = query.replace(' ', '_')
            output_file = BROLL_DIR / f"{safe_query}_{i}.mp4"
            
            if output_file.exists():
                print(f"  [{i}] Already exists: {output_file.name}")
                downloaded.append(str(output_file))
                continue
            
            print(f"  [{i}] Downloading: {output_file.name}")
            
            video_data = requests.get(download_url, timeout=120).content
            with open(output_file, 'wb') as f:
                f.write(video_data)
            
            size_mb = output_file.stat().st_size / (1024 * 1024)
            print(f"      Saved: {size_mb:.2f} MB")
            
            downloaded.append(str(output_file))
        
        print(f"[OK] Downloaded {len(downloaded)} videos for: {query}")
        return downloaded
        
    except Exception as e:
        print(f"[ERROR] {e}")
        return []

def generate_theta_audio(duration=30, frequency=4, output_name="theta_4hz.wav"):
    """Generate theta wave audio (4-8Hz) using FFmpeg"""
    
    output_file = AUDIO_SFX_DIR / output_name
    
    if output_file.exists():
        print(f"[SKIP] Already exists: {output_file.name}")
        return str(output_file)
    
    print(f"\n[AUDIO] Generating {frequency}Hz theta wave ({duration}s)...")
    
    # Generate theta wave with FFmpeg
    cmd = [
        'ffmpeg',
        '-f', 'lavfi',
        '-i', f'sine=frequency={frequency}:duration={duration}',
        '-af', 'volume=0.3',  # Lower volume for background
        '-ar', '44100',
        '-ac', '2',
        '-y',
        str(output_file)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        size_kb = output_file.stat().st_size / 1024
        print(f"[OK] Generated: {output_file.name} ({size_kb:.2f} KB)")
        return str(output_file)
    except Exception as e:
        print(f"[ERROR] Failed to generate: {e}")
        return None

def generate_binaural_beat(base_freq=200, beat_freq=4, duration=30, output_name="binaural_theta.wav"):
    """Generate binaural beat for theta state"""
    
    output_file = AUDIO_SFX_DIR / output_name
    
    if output_file.exists():
        print(f"[SKIP] Already exists: {output_file.name}")
        return str(output_file)
    
    print(f"\n[AUDIO] Generating binaural beat ({base_freq}Hz ± {beat_freq}Hz)...")
    
    left_freq = base_freq
    right_freq = base_freq + beat_freq
    
    cmd = [
        'ffmpeg',
        '-f', 'lavfi',
        '-i', f'sine=frequency={left_freq}:duration={duration}',
        '-f', 'lavfi',
        '-i', f'sine=frequency={right_freq}:duration={duration}',
        '-filter_complex', '[0:a][1:a]amerge=inputs=2[a]',
        '-map', '[a]',
        '-af', 'volume=0.2',
        '-ar', '44100',
        '-y',
        str(output_file)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        size_kb = output_file.stat().st_size / 1024
        print(f"[OK] Generated: {output_file.name} ({size_kb:.2f} KB)")
        return str(output_file)
    except Exception as e:
        print(f"[ERROR] Failed to generate: {e}")
        return None

def generate_horror_ambience():
    """Generate creepy background ambience"""
    
    output_file = AUDIO_SFX_DIR / "horror_ambience.wav"
    
    if output_file.exists():
        print(f"[SKIP] Already exists: {output_file.name}")
        return str(output_file)
    
    print(f"\n[AUDIO] Generating horror ambience...")
    
    # Low rumble + high tension
    cmd = [
        'ffmpeg',
        '-f', 'lavfi',
        '-i', 'sine=frequency=60:duration=30',  # Low rumble
        '-f', 'lavfi',
        '-i', 'sine=frequency=5000:duration=30',  # High tension
        '-filter_complex',
        '[0:a]volume=0.4[low];[1:a]volume=0.1,tremolo=f=0.5:d=0.9[high];[low][high]amix=inputs=2:duration=first[a]',
        '-map', '[a]',
        '-ar', '44100',
        '-ac', '2',
        '-y',
        str(output_file)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        size_kb = output_file.stat().st_size / 1024
        print(f"[OK] Generated: {output_file.name} ({size_kb:.2f} KB)")
        return str(output_file)
    except Exception as e:
        print(f"[ERROR] Failed to generate: {e}")
        return None

def download_all_assets():
    """Download all B-roll and generate all audio SFX"""
    
    print(f"\n{'='*70}")
    print(f"SCARIFY - MEDIA ASSET SOURCING")
    print(f"{'='*70}\n")
    
    # Download B-roll
    print(f"[STEP 1] Downloading B-roll footage...")
    print(f"Output: {BROLL_DIR}\n")
    
    all_videos = []
    for query in BROLL_QUERIES[:5]:  # Limit to 5 queries to start
        videos = download_pexels_broll(query, count=3)
        all_videos.extend(videos)
    
    print(f"\n[OK] Downloaded {len(all_videos)} B-roll videos")
    
    # Generate audio SFX
    print(f"\n[STEP 2] Generating audio SFX...")
    print(f"Output: {AUDIO_SFX_DIR}\n")
    
    audio_files = []
    
    # Theta waves (4-8Hz for dread/paralysis)
    audio_files.append(generate_theta_audio(30, 4, "theta_4hz.wav"))
    audio_files.append(generate_theta_audio(30, 6, "theta_6hz.wav"))
    audio_files.append(generate_theta_audio(30, 8, "theta_8hz.wav"))
    
    # Binaural beats
    audio_files.append(generate_binaural_beat(200, 4, 30, "binaural_theta_4hz.wav"))
    audio_files.append(generate_binaural_beat(200, 6, 30, "binaural_theta_6hz.wav"))
    
    # Horror ambience
    audio_files.append(generate_horror_ambience())
    
    audio_files = [f for f in audio_files if f]  # Remove None
    
    print(f"\n[OK] Generated {len(audio_files)} audio SFX files")
    
    # Summary
    print(f"\n{'='*70}")
    print(f"ASSET SOURCING COMPLETE")
    print(f"{'='*70}\n")
    print(f"B-roll videos: {len(all_videos)}")
    print(f"  Location: {BROLL_DIR}")
    print(f"\nAudio SFX: {len(audio_files)}")
    print(f"  Location: {AUDIO_SFX_DIR}")
    print(f"\n{'='*70}\n")
    
    # Save manifest
    manifest = {
        'generated_at': str(subprocess.check_output(['powershell', 'Get-Date'], text=True).strip()),
        'broll_videos': all_videos,
        'audio_sfx': audio_files,
        'total_broll': len(all_videos),
        'total_audio': len(audio_files)
    }
    
    manifest_file = ASSETS_DIR / "assets_manifest.json"
    with open(manifest_file, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"Manifest saved: {manifest_file}\n")
    
    return manifest

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "broll":
            print("Downloading B-roll only...")
            for query in BROLL_QUERIES:
                download_pexels_broll(query, count=3)
        elif sys.argv[1] == "audio":
            print("Generating audio SFX only...")
            generate_theta_audio(30, 4, "theta_4hz.wav")
            generate_theta_audio(30, 6, "theta_6hz.wav")
            generate_theta_audio(30, 8, "theta_8hz.wav")
            generate_binaural_beat(200, 4, 30, "binaural_theta_4hz.wav")
            generate_horror_ambience()
    else:
        download_all_assets()


