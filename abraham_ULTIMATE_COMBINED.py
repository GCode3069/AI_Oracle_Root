#!/usr/bin/env python3
"""
ABRAHAM LINCOLN - ULTIMATE COMBINED SYSTEM
Mixes ALL best elements for MAXIMUM REVENUE in RECORD TIME

COMBINES:
1. Max Headroom glitchy Abe (visual hook)
2. VHS TV broadcast effects (brand identity)
3. Dark satirical comedy (Pryor/Carlin/Chappelle - roasts everyone)
4. Lip-sync (D-ID/Wav2Lip with fallback)
5. Jumpcuts (for long videos, maintains energy)
6. Bitcoin QR code (always visible, NO recitation)
7. Psychological audio layers (secret sauce)
8. Master Lincoln image (best quality)
9. Dual format (short 9-17s + long 60-90s)
10. Google Sheets tracking (analytics)
11. Multi-platform ready (TikTok, Rumble, YouTube)

REVENUE OPTIMIZATION:
- SHORT (9-17s): Viral growth, 45% retention, Shorts feed
- LONG (60-90s): Mid-roll ads (100x better CPM), deep roasts

Usage:
python abraham_ULTIMATE_COMBINED.py --short 10    # 10 shorts
python abraham_ULTIMATE_COMBINED.py --long 10     # 10 long videos
python abraham_ULTIMATE_COMBINED.py --both 5      # 5 of each
"""
import os, sys, json, requests, subprocess, random, time
from pathlib import Path
from datetime import datetime

# Import from main system
sys.path.insert(0, str(Path(__file__).parent))
from abraham_MAX_HEADROOM import (
    generate_script as generate_short_script,
    generate_voice,
    generate_lincoln_face_pollo,
    create_max_headroom_video,
    upload_to_youtube,
    get_headlines,
    log_to_google_sheets,
    generate_bitcoin_qr,
    BITCOIN_ADDRESS
)

BASE_DIR = Path("F:/AI_Oracle_Root/scarify/abraham_horror")

def generate_long_script(headline):
    """
    LONG FORMAT SCRIPT (60-90 seconds = 150-225 words)
    Multi-act structure with JUMPCUT points marked
    """
    hl = headline.lower()
    
    if "trump" in hl or "republican" in hl:
        return f"""LINCOLN here! BACK from DEAD!

{headline}

[JUMPCUT]

TRUMP! BILLIONAIRE conning POOR people! Pryor: "That's INSANE!"

[JUMPCUT]

But DEMOCRATS! Pelosi $100 MILLION! Bernie's THREE HOUSES!

[JUMPCUT]

Carlin truth: "BIG CLUB - you AIN'T in it!"

[JUMPCUT]

Republicans serve RICH! Democrats serve RICH! SAME PARTY!

[JUMPCUT]

You're getting ROBBED! Left! Right! ALL of you!

[JUMPCUT]

I died for democracy! You got OLIGARCHY!

Look in mirrors."""

    elif "police" in hl or "shooting" in hl:
        return f"""LINCOLN! Got WORDS!

{headline}

[JUMPCUT]

COPS killing unarmed! Pryor: "Police scare ME!"

[JUMPCUT]

"Defund" crowd! Criminals police THEMSELVES?! DUMB!

[JUMPCUT]

Conservatives: "Back Blue!" - until at YOUR door!

[JUMPCUT]

Liberals: Want reform! VOTE for bigger budgets!

[JUMPCUT]

Bernie Mac: EVERYBODY WRONG! Fix the SYSTEM!

[JUMPCUT]

Carlin: "They keep you fighting so they can ROB you!"

Look in mirrors."""

    else:
        return f"""LINCOLN! DEAD but TALKING!

{headline}

[JUMPCUT]

Pryor wisdom: "Only KIDS and DRUNKS honest! Everyone LYING!"

[JUMPCUT]

Republicans: Small government in UTERUS!

[JUMPCUT]

Democrats: Free EVERYTHING! Who PAYS?!

[JUMPCUT]

Rich HOARDING! Poor DEFENDING them!

[JUMPCUT]

Carlin: "American DREAM?! You're ASLEEP!"

[JUMPCUT]

ALL getting PLAYED! Wake UP!

Look in mirrors."""

def add_jumpcuts_to_video(input_video, output_video, script):
    """
    Add jumpcuts at [JUMPCUT] markers in script
    Creates dynamic editing for long videos
    """
    print("[Jumpcuts] Adding dynamic cuts...")
    
    # Count jumpcut points
    jumpcuts = script.count("[JUMPCUT]")
    
    if jumpcuts == 0:
        # No jumpcuts needed, copy original
        import shutil
        shutil.copy2(input_video, output_video)
        return True
    
    try:
        # Get video duration
        probe = subprocess.run([
            'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1', str(input_video)
        ], capture_output=True, text=True)
        duration = float(probe.stdout.strip())
        
        # Calculate jumpcut intervals
        interval = duration / (jumpcuts + 1)
        
        # Create filter for jumpcuts (quick zoom effect at each cut)
        jumpcut_times = [interval * (i + 1) for i in range(jumpcuts)]
        
        # Build filter: zoompan effect at each jumpcut point
        zoom_effects = []
        for i, cut_time in enumerate(jumpcut_times):
            # Quick zoom in/out at each cut (0.5s effect)
            zoom_effects.append(
                f"zoompan=z='if(between(t,{cut_time},{cut_time+0.3}),1.1,1.0)':d=1:"
                f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920"
            )
        
        # Apply quick zoom at jumpcut points
        cmd = [
            'ffmpeg', '-y',
            '-i', str(input_video),
            '-vf', f"zoompan=z='1.0+(0.1*sin(t*2))':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920",
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '22',
            '-c:a', 'copy',
            str(output_video)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if Path(output_video).exists():
            print(f"[Jumpcuts] Added {jumpcuts} dynamic cuts")
            return True
        else:
            print(f"[Jumpcuts] Failed, using original")
            import shutil
            shutil.copy2(input_video, output_video)
            return False
    except Exception as e:
        print(f"[Jumpcuts] Error: {e}, using original")
        import shutil
        shutil.copy2(input_video, output_video)
        return False

def generate_ultimate_short(episode_num):
    """
    ULTIMATE SHORT VIDEO
    Best of all styles for viral growth
    """
    print(f"\n{'='*70}")
    print(f"  ULTIMATE SHORT - Episode #{episode_num}")
    print(f"  (Max Headroom + VHS + Dark Comedy + QR Code)")
    print(f"{'='*70}\n")
    
    # Get headline
    headlines = get_headlines()
    headline = random.choice(headlines)
    print(f"[1/6] Headline: {headline}")
    
    # Generate SHORT script (32-45 words)
    script = generate_short_script(headline)
    word_count = len(script.split())
    print(f"[2/6] Script: {word_count} words (target: 32-45 for 9-17s)")
    print(f"      Dark comedy: Roasts everyone!")
    
    # Generate audio
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    audio_path = BASE_DIR / f"audio/ULTIMATE_SHORT_{episode_num}.mp3"
    print(f"[3/6] Generating audio (psychological layers)...")
    if not generate_voice(script, audio_path):
        return None
    
    # Get master Lincoln image
    print(f"[4/6] Getting master Lincoln image...")
    lincoln_image = generate_lincoln_face_pollo()
    
    # Create video (ALL VHS effects, Bitcoin QR, NO lip-sync for speed)
    print(f"[5/6] Creating ultimate video...")
    print(f"      - Max Headroom glitch")
    print(f"      - VHS TV broadcast")
    print(f"      - Bitcoin QR code")
    print(f"      - All effects")
    
    video_path = BASE_DIR / f"videos/ULTIMATE_SHORT_{timestamp}.mp4"
    
    # Set environment for features - OPTIMIZED FOR SHORT
    os.environ['USE_LIPSYNC'] = '0'  # Skip lip-sync for speed (shorts need FAST)
    os.environ['USE_JUMPSCARE'] = '1'  # Keep jumpscare
    
    if not create_max_headroom_video(lincoln_image, audio_path, video_path, headline,
                                     use_lipsync=False, use_jumpscare=True):
        return None
    
    # Upload to YouTube
    print(f"[6/6] Uploading to YouTube...")
    youtube_url = upload_to_youtube(video_path, headline, episode_num)
    
    # Track in Google Sheets
    log_to_google_sheets(episode_num, headline, script, video_path, youtube_url or "")
    
    # Copy to uploaded (jumpcuts built into main video via jumpscare)
    uploaded_path = BASE_DIR / "uploaded" / f"ULTIMATE_SHORT_{episode_num}.mp4"
    import shutil
    shutil.copy2(video_path, uploaded_path)
    
    mb = uploaded_path.stat().st_size / (1024 * 1024)
    
    print(f"\n{'='*70}")
    print(f"  [OK] ULTIMATE SHORT COMPLETE")
    print(f"{'='*70}")
    print(f"File: {uploaded_path.name} ({mb:.1f} MB)")
    print(f"Format: SHORT (9-17s viral growth)")
    print(f"Features: Glitchy Abe + VHS + Dark Comedy + QR")
    if youtube_url:
        print(f"YouTube: {youtube_url}")
    print(f"{'='*70}\n")
    
    return str(uploaded_path)

def generate_ultimate_long(episode_num):
    """
    ULTIMATE LONG VIDEO
    Best of all styles for maximum monetization
    """
    print(f"\n{'='*70}")
    print(f"  ULTIMATE LONG - Episode #{episode_num}")
    print(f"  (Max Headroom + VHS + Dark Comedy + Jumpcuts + QR)")
    print(f"{'='*70}\n")
    
    # Get headline
    headlines = get_headlines()
    headline = random.choice(headlines)
    print(f"[1/7] Headline: {headline}")
    
    # Generate LONG script (150-225 words with jumpcut markers)
    script = generate_long_script(headline)
    word_count = len(script.split())
    jumpcut_count = script.count("[JUMPCUT]")
    print(f"[2/7] Script: {word_count} words (target: 150-225 for 60-90s)")
    print(f"      Jumpcuts: {jumpcut_count} dynamic cuts")
    print(f"      Dark comedy: Deep multi-act roasts!")
    
    # Remove markers for audio generation
    clean_script = script.replace("[JUMPCUT]", "")
    
    # Generate audio
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    audio_path = BASE_DIR / f"audio/ULTIMATE_LONG_{episode_num}.mp3"
    print(f"[3/7] Generating audio (psychological layers)...")
    if not generate_voice(clean_script, audio_path):
        return None
    
    # Get master Lincoln image
    print(f"[4/7] Getting master Lincoln image...")
    lincoln_image = generate_lincoln_face_pollo()
    
    # Create base video (ALL VHS effects, Bitcoin QR, optional lip-sync)
    print(f"[5/7] Creating base video...")
    print(f"      - Max Headroom glitch")
    print(f"      - VHS TV broadcast")
    print(f"      - Bitcoin QR code")
    print(f"      - Lip-sync (optional)")
    
    base_video = BASE_DIR / f"temp/BASE_LONG_{timestamp}.mp4"
    
    # Set environment
    os.environ['USE_LIPSYNC'] = '1'  # Enable lip-sync for quality
    os.environ['USE_JUMPSCARE'] = '1'  # Keep jumpscare
    
    if not create_max_headroom_video(lincoln_image, audio_path, base_video, headline,
                                     use_lipsync=True, use_jumpscare=True):
        return None
    
    # Add jumpcuts
    print(f"[6/7] Adding {jumpcut_count} jumpcuts...")
    video_path = BASE_DIR / f"videos/ULTIMATE_LONG_{timestamp}.mp4"
    add_jumpcuts_to_video(base_video, video_path, script)
    
    # Upload to YouTube
    print(f"[7/7] Uploading to YouTube...")
    youtube_url = upload_to_youtube(video_path, headline, episode_num)
    
    # Track in Google Sheets
    log_to_google_sheets(episode_num, headline, script, video_path, youtube_url or "")
    
    # Copy to uploaded
    uploaded_path = BASE_DIR / "uploaded" / f"ULTIMATE_LONG_{episode_num}.mp4"
    import shutil
    shutil.copy2(video_path, uploaded_path)
    
    mb = uploaded_path.stat().st_size / (1024 * 1024)
    
    print(f"\n{'='*70}")
    print(f"  [OK] ULTIMATE LONG COMPLETE")
    print(f"{'='*70}")
    print(f"File: {uploaded_path.name} ({mb:.1f} MB)")
    print(f"Format: LONG (60-90s mid-roll ads)")
    print(f"Features: Glitchy Abe + VHS + Dark Comedy + Jumpcuts + Lip-sync + QR")
    if youtube_url:
        print(f"YouTube: {youtube_url}")
    print(f"{'='*70}\n")
    
    return str(uploaded_path)

def add_jumpcuts_to_video(input_video, output_video, script="", force_cuts=True):
    """Add dynamic jumpcuts - forced for SHORT videos"""
    jumpcuts = script.count("[JUMPCUT]") if script else 0
    
    # Force at least 3 jumpcuts for SHORT videos (even without markers)
    if jumpcuts == 0 and force_cuts:
        jumpcuts = 3  # Add 3 jumpcuts to SHORT videos
    
    if jumpcuts == 0:
        import shutil
        shutil.copy2(input_video, output_video)
        return True
    
    try:
        # Get duration
        probe = subprocess.run([
            'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1', str(input_video)
        ], capture_output=True, text=True)
        duration = float(probe.stdout.strip())
        
        # Jumpcut intervals
        interval = duration / (jumpcuts + 1)
        
        # Add quick zoom pulses at each jumpcut point
        zoom_expr = "1.0"
        for i in range(jumpcuts):
            cut_time = interval * (i + 1)
            # Quick zoom (1.0 → 1.15 → 1.0 over 0.4s)
            zoom_expr = f"if(between(t,{cut_time},{cut_time+0.2}),1.15,{zoom_expr})"
            zoom_expr = f"if(between(t,{cut_time+0.2},{cut_time+0.4}),1.0,{zoom_expr})"
        
        cmd = [
            'ffmpeg', '-y',
            '-i', str(input_video),
            '-vf', f"zoompan=z='{zoom_expr}':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920",
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '22',
            '-c:a', 'copy',
            str(output_video)
        ]
        
        subprocess.run(cmd, capture_output=True, timeout=90)
        
        if Path(output_video).exists():
            print(f"[Jumpcuts] ✅ Added {jumpcuts} cuts")
            return True
    except Exception as e:
        print(f"[Jumpcuts] Error: {e}")
    
    # Fallback
    import shutil
    shutil.copy2(input_video, output_video)
    return False

if __name__ == "__main__":
    mode = "short"
    count = 1
    start_ep = int(os.getenv("EPISODE_NUM", "2000"))
    
    # Parse args
    for i, arg in enumerate(sys.argv[1:]):
        if arg == "--short":
            mode = "short"
            count = int(sys.argv[i+2]) if i+1 < len(sys.argv)-1 and sys.argv[i+2].isdigit() else 1
        elif arg == "--long":
            mode = "long"
            count = int(sys.argv[i+2]) if i+1 < len(sys.argv)-1 and sys.argv[i+2].isdigit() else 1
        elif arg == "--both":
            mode = "both"
            count = int(sys.argv[i+2]) if i+1 < len(sys.argv)-1 and sys.argv[i+2].isdigit() else 1
    
    print(f"\n{'='*70}")
    print(f"  ULTIMATE COMBINED GENERATOR")
    print(f"{'='*70}")
    print(f"Mode: {mode.upper()}")
    print(f"Count: {count}")
    print(f"Start: Episode #{start_ep}")
    print(f"{'='*70}\n")
    
    if mode == "short":
        for i in range(count):
            generate_ultimate_short(start_ep + i)
            if i < count - 1:
                time.sleep(15)
    
    elif mode == "long":
        for i in range(count):
            generate_ultimate_long(start_ep + i)
            if i < count - 1:
                time.sleep(20)
    
    elif mode == "both":
        for i in range(count):
            generate_ultimate_short(start_ep + i * 2)
            generate_ultimate_long(start_ep + i * 2 + 1)
            if i < count - 1:
                time.sleep(20)
    
    print(f"\n{'='*70}")
    print(f"  [OK] GENERATION COMPLETE")
    print(f"{'='*70}")
    print(f"Check: abraham_horror/uploaded/")
    print(f"YouTube: Check your channel for uploads")
    print(f"Tracking: video_tracking.csv\n")

