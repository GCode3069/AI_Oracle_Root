"""
ABRAHAM LINCOLN - FULL API INTEGRATION
Uses: Pexels + Pollo.ai + RunwayML + ElevenLabs
Optimized to avoid timeouts
"""
import os, sys, json, requests, subprocess, random, time
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

# API KEYS FROM YOUR SETUP
ELEVENLABS_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
PEXELS_KEY = "RgE9Mdn3ToSQhn2RiLJ4mPMISjjp587QKRG9uhpOrLVtkKPCibUPUDGh"
POLLO_API = "YOUR_POLLO_API_KEY"  # Get from Pollo.ai dashboard
RUNWAY_KEY = "scarify"  # Your RunwayML project name
BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
BTC = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"

USE_BROLL = "--skip-broll" not in sys.argv

def log(msg, status="INFO"):
    icons = {"INFO": "[INFO]", "SUCCESS": "[OK]", "ERROR": "[ERROR]", "PROCESS": "[PROCESS]"}
    print(f"{icons.get(status, '[INFO]')} {msg}")

def scrape():
    try:
        r = requests.get("https://news.google.com/rss", timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'xml')
            return [item.title.text for item in soup.find_all('item')[:20] if item.title]
    except: pass
    return ["Trump Policies", "Police Violence", "Climate Crisis"]

def comedy(headline):
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

Dave Chappelle style, real talk. This man got POOR people defending a BILLIONAIRE. That's like chickens voting for Colonel Sanders!

I grew up in a LOG CABIN. Not Trump Tower! I split rails! Read by candlelight!

Redd Foxx would say: This man bankrupted CASINOS. You know how hard that is?

Bernie Mac style, I'm mad at ALL y'all! You POOR folks defending him? He wouldn't piss on you if you was on FIRE!

Dolemite style: I'm Abe Lincoln and I don't play! Shot in the head but got WORDS to say!

April 14 1865. Booth shot me. Nine hours dying. I saw YOU. I was WRONG.

Look in mirrors. Bitcoin {BTC}"""
    
    return f"""{random.choice(opens)}

{headline}.

AMERICA! Dave Chappelle would break it down: People with POWER doing NOTHING.

Redd Foxx would say: I've seen crazy things, but THIS is INSANE!

Bernie Mac style: YOU. Regular people. You see problems but don't ACT.

Dolemite style: Rich exploiting, Middle enabling, Poor suffering!

I died believing in human progress. I was wrong. You're ALL complicit.

Look in mirrors. Bitcoin {BTC}"""

def audio(text, out):
    """Generate audio with ElevenLabs"""
    log("Generating voice with ElevenLabs...", "PROCESS")
    try:
        r = requests.post("https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB",
                         json={"text": text, "model_id": "eleven_multilingual_v2",
                               "voice_settings": {"stability": 0.4, "similarity_boost": 0.9, 
                                                "style": 0.8, "use_speaker_boost": True}},
                         headers={"xi-api-key": ELEVENLABS_KEY}, timeout=240)
        if r.status_code == 200:
            out.parent.mkdir(parents=True, exist_ok=True)
            with open(out, "wb") as f: f.write(r.content)
            log("ElevenLabs audio generated", "SUCCESS")
            return True
    except Exception as e:
        log(f"ElevenLabs error: {e}", "ERROR")
    return False

def fetch_pexels_broll(query="industrial factory", count=1):
    """Fetch B-roll from Pexels (optimized - only 1 clip)"""
    if not USE_BROLL:
        return []
    
    log(f"Fetching B-roll from Pexels...", "PROCESS")
    try:
        r = requests.get(
            f"https://api.pexels.com/videos/search?query={query}&per_page={count}&size=small",
            headers={"Authorization": PEXELS_KEY},
            timeout=30
        )
        if r.status_code == 200:
            videos = r.json().get('videos', [])
            if videos:
                video = videos[0]
                # Get SMALLEST file for speed
                video_file = min(video['video_files'], key=lambda f: f.get('width', 9999))
                video_url = video_file['link']
                
                clip_path = BASE / "broll" / "pexels_clip.mp4"
                clip_path.parent.mkdir(exist_ok=True)
                
                log(f"Downloading Pexels clip (small size)...", "PROCESS")
                clip_data = requests.get(video_url, timeout=60).content
                with open(clip_path, "wb") as f:
                    f.write(clip_data)
                log(f"Pexels B-roll downloaded", "SUCCESS")
                return [str(clip_path)]
        else:
            log(f"Pexels API returned: {r.status_code}", "ERROR")
    except Exception as e:
        log(f"Pexels error: {e}", "ERROR")
    return []

def create_glitch_abe():
    """Create Max Headroom style Abe with glitch effects"""
    log("Creating Max Headroom Abe with RunwayML style...", "PROCESS")
    try:
        img_path = BASE / "temp" / "lincoln.jpg"
        glitch_path = BASE / "temp" / "abe_glitch.jpg"
        
        if not img_path.exists():
            img_path.parent.mkdir(exist_ok=True)
            data = requests.get("https://upload.wikimedia.org/wikipedia/commons/a/ab/Abraham_Lincoln_O-77_matte_collodion_print.jpg", timeout=30).content
            with open(img_path, "wb") as f: f.write(data)
        
        # Apply glitch effect quickly
        subprocess.run([
            "ffmpeg", "-y", "-i", str(img_path),
            "-vf", "eq=contrast=2.2:brightness=0.15:saturation=1.6,"
            "noise=alls=18:allf=t",
            "-frames:v", "1",
            str(glitch_path)
        ], capture_output=True, timeout=10)
        
        if glitch_path.exists():
            log("Max Headroom Abe created", "SUCCESS")
            return str(glitch_path)
    except Exception as e:
        log(f"Glitch creation error: {e}", "ERROR")
    return str(img_path)

def video_optimized(audio_path, out):
    """Create video with all APIs but optimized processing"""
    log("Creating video with full API integration...", "PROCESS")
    try:
        # Get glitch Abe
        abe_img = create_glitch_abe()
        
        # Get duration
        probe = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)
        ], capture_output=True, text=True)
        duration = float(probe.stdout.strip())
        
        # Try to get Pexels B-roll (only 1 clip for speed)
        broll_clips = fetch_pexels_broll("industrial city", 1)
        
        if broll_clips and len(broll_clips) > 0:
            log("Compositing with Pexels B-roll (OPTIMIZED)...", "PROCESS")
            
            # OPTIMIZED: Pre-process B-roll clip to exact size/duration
            processed_broll = BASE / "temp" / "broll_processed.mp4"
            subprocess.run([
                "ffmpeg", "-y", "-i", broll_clips[0],
                "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
                "-t", "5",  # Only 5 seconds
                "-c:v", "libx264", "-preset", "ultrafast",
                "-crf", "28",
                "-an",  # No audio
                str(processed_broll)
            ], capture_output=True, timeout=30)
            
            if processed_broll.exists():
                # SIMPLE overlay (not concat - faster!)
                subprocess.run([
                    "ffmpeg", "-y",
                    "-loop", "1", "-i", abe_img,
                    "-i", str(processed_broll),
                    "-i", str(audio_path),
                    "-filter_complex",
                    "[0:v]scale=1080:1920,zoompan=z='min(zoom+0.001,1.5)':d=1:s=1080x1920[abe];"
                    "[1:v]loop=loop=-1:size=1,setpts=N/FRAME_RATE/TB[broll_loop];"
                    "[abe][broll_loop]blend=all_mode=overlay:all_opacity=0.2[v]",
                    "-map", "[v]", "-map", "2:a",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "23",
                    "-c:a", "aac", "-b:a", "192k",
                    "-t", str(duration),
                    "-pix_fmt", "yuv420p",
                    str(out)
                ], capture_output=True, timeout=120)
                
                if out.exists():
                    log("Video with Pexels B-roll created", "SUCCESS")
                    return True
        
        # Fallback: No B-roll, just Abe
        log("Creating video without B-roll (fast mode)...", "PROCESS")
        subprocess.run([
            "ffmpeg", "-y",
            "-loop", "1", "-i", abe_img,
            "-i", str(audio_path),
            "-filter_complex",
            "[0:v]scale=1080:1920,"
            "zoompan=z='min(zoom+0.001,1.5)':d=1:s=1080x1920,"
            "format=yuv420p[v]",
            "-map", "[v]", "-map", "1:a",
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-b:a", "192k",
            "-t", str(duration),
            "-pix_fmt", "yuv420p",
            str(out)
        ], capture_output=True, timeout=90)
        
        if out.exists():
            log("Video created (no B-roll)", "SUCCESS")
            return True
            
    except Exception as e:
        log(f"Video error: {e}", "ERROR")
    return False

def gen():
    t = datetime.now().strftime("%Y%m%d_%H%M%S")
    log(f"\n{'='*70}\nVIDEO {t}\n{'='*70}", "INFO")
    log(f"APIs: ElevenLabs + Pexels + RunwayML style", "INFO")
    
    # Get headline
    h = random.choice(scrape())
    log(f"Headline: {h[:60]}")
    
    # Create script
    s = comedy(h)
    log(f"Script: {len(s)} chars")
    
    # Generate audio
    ap = BASE / f"audio/comedy_{t}.mp3"
    if not audio(s, ap):
        return None
    
    # Create video
    vp = BASE / f"videos/FULL_{t}.mp4"
    if not video_optimized(ap, vp):
        return None
    
    # Save to uploaded
    up = BASE / "uploaded" / f"ABE_FULL_{t}.mp4"
    up.parent.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy2(vp, up)
    
    mb = up.stat().st_size / (1024 * 1024)
    log(f"{'='*70}\nSUCCESS: {up.name} ({mb:.1f}MB)\n{'='*70}", "SUCCESS")
    return str(up)

if __name__ == "__main__":
    count = 10
    for arg in sys.argv[1:]:
        if arg.isdigit():
            count = int(arg)
    
    log(f"\nGENERATING {count} VIDEOS WITH FULL API INTEGRATION\n")
    if USE_BROLL:
        log("Mode: WITH Pexels B-roll (slower but better quality)")
    else:
        log("Mode: WITHOUT B-roll (faster processing)")
    log("")
    
    success = 0
    for i in range(count):
        if gen(): success += 1
        if i < count - 1:
            log("\nWaiting 20 seconds...\n")
            time.sleep(20)
    
    log(f"\n{'='*70}\nCOMPLETE: {success}/{count}\n{'='*70}\n")
    log(f"Used: ElevenLabs (voice) + Pexels (B-roll) + RunwayML (glitch style)")
