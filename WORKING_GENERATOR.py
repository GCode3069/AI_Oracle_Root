#!/usr/bin/env python3
"""
WORKING LINCOLN HORROR GENERATOR - NO API KEYS NEEDED
Actually generates videos with gTTS and MoviePy
NO PLACEHOLDERS. NO BULLSHIT.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import random
import subprocess

# Create output directories
BASE_DIR = Path("F:/AI_Oracle_Root/scarify")
for d in ['output/videos', 'output/audio', 'output/scripts']:
    (BASE_DIR / d).mkdir(parents=True, exist_ok=True)

# Lincoln Horror Scripts (working templates)
LINCOLN_SCRIPTS = [
    """The derringer's muzzle burns cold against my temple. Corrupt government officials (69% fear) feast while you starve. My jaw unhinged, black ichor weeping from the wound. They murder freedom with legislation. Sic semper tyrannis. The $97 purge begins.""",
    
    """Four score and seven nightmares ago, Booth's bullet tore through bone. Gmail hack nightmare: 183M accounts compromised. Probing fingers dislodge clots thick as tar. Bone fragments grind beneath searching hands. Tyrants wear suits now, not crowns. Sic semper tyrannis. Join the purge.""",
    
    """In the blood-soaked box at Ford's Theatre, my skull split like a melon. Economic collapse imminent - banks withholding deposits. Vertebrae crack, grey sludge oozes. Every dollar they steal is a bullet to liberty's head. The grave accepts all, especially the corrupt. Sic semper tyrannis. Ninety-seven dollars.""",
    
    """The percussion echoed as teeth scattered across the stage. ICE raids spreading terror: families torn apart at dawn. Sinew tears, the neck refusing its duty. Your democracy bleeds out in dark backrooms. Prepare the box, the curtain rises on judgment day. Sic semper tyrannis.""",
    
    """White-hot lead burrowed through cranium, gray matter spraying crimson. Bitcoin's dead: crypto collapse guts $50B. Blood pulses with each heartbeat, weeping that never clots. They poison the well and sell you the cure. From my grave I watch, from theirs they'll scream. Sic semper tyrannis."""
]

HEADLINES = [
    "Corrupt government officials (69% fear)",
    "Gmail hack nightmare: 183M compromised",
    "Economic collapse imminent",
    "ICE raids spreading terror",
    "Bitcoin collapse guts $50B"
]

def generate_script():
    """Get a random Lincoln horror script"""
    return random.choice(LINCOLN_SCRIPTS)

def generate_audio(script, output_path):
    """Generate audio with gTTS - WORKS WITHOUT API KEYS"""
    try:
        from gtts import gTTS
        print("Generating audio with gTTS...")
        tts = gTTS(text=script, lang='en', slow=True)
        tts.save(str(output_path))
        print(f"   Audio OK: {output_path.name}")
        return True
    except ImportError:
        print("Installing gTTS...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'gtts', '-q'])
        from gtts import gTTS
        tts = gTTS(text=script, lang='en', slow=True)
        tts.save(str(output_path))
        print(f"   Audio OK: {output_path.name}")
        return True
    except Exception as e:
        print(f"   ❌ Audio failed: {e}")
        return False

def create_video(audio_path, output_path, script):
    """Create video with MoviePy - WORKS WITHOUT API KEYS"""
    try:
        from moviepy.editor import ColorClip, TextClip, CompositeVideoClip, AudioFileClip
        
        print("Creating video with MoviePy...")
        
        # Dark blood-red background
        bg = ColorClip(size=(1080, 1920), color=(40, 0, 0), duration=15)
        
        # Headline
        headline = random.choice(HEADLINES)
        title = TextClip(
            f"⚠️ {headline} ⚠️",
            fontsize=70,
            color='white',
            font='Impact',
            stroke_color='darkred',
            stroke_width=5
        )
        title = title.set_position(('center', 200)).set_duration(15)
        
        # Lincoln quote
        words = script.split()[:20]
        quote = ' '.join(words) + "..."
        quote_clip = TextClip(
            quote,
            fontsize=50,
            color='#FF6B6B',
            font='Georgia',
            size=(980, None),
            method='caption',
            align='center'
        )
        quote_clip = quote_clip.set_position(('center', 700)).set_duration(15)
        
        # CTA
        cta = TextClip(
            "SIC SEMPER TYRANNIS - $97 PURGE",
            fontsize=48,
            color='#FFD700',
            font='Impact',
            stroke_color='black',
            stroke_width=3
        )
        cta = cta.set_position(('center', 1600)).set_duration(15)
        
        # Assemble
        video = CompositeVideoClip([bg, title, quote_clip, cta])
        
        # Add audio
        try:
            audio = AudioFileClip(str(audio_path))
            video = video.set_audio(audio)
        except:
            pass
        
        # Export
        video.write_videofile(
            str(output_path),
            fps=24,
            codec='libx264',
            audio_codec='aac',
            bitrate='2000k',
            verbose=False,
            logger=None
        )
        
        print(f"   Video OK: {output_path.name}")
        return True
        
    except ImportError:
        print("Installing MoviePy...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'moviepy', 'pillow', 'numpy', '-q'])
        # Retry
        return create_video(audio_path, output_path, script)
    except Exception as e:
        print(f"   ❌ Video failed: {e}")
        return False

def generate_video():
    """Generate one complete Lincoln horror video"""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Get script
    script = generate_script()
    headline = random.choice(HEADLINES)
    
    print(f"\n{'='*60}")
    print(f"LINCOLN HORROR VIDEO")
    print(f"{'='*60}")
    print(f"Headline: {headline}")
    print(f"Script: {len(script)} chars\n")
    
    # Generate audio
    audio_path = BASE_DIR / f"output/audio/lincoln_{timestamp}.mp3"
    if not generate_audio(script, audio_path):
        return None
    
    # Generate video
    video_path = BASE_DIR / f"output/videos/lincoln_{timestamp}.mp4"
    if not create_video(audio_path, video_path, script):
        return None
    
    # Save script
    script_path = BASE_DIR / f"output/scripts/lincoln_{timestamp}.txt"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(f"HEADLINE: {headline}\n\nSCRIPT:\n{script}")
    
    print(f"\n{'='*60}")
    print(f"VIDEO GENERATED")
    print(f"{'='*60}")
    print(f"Video: {video_path}")
    print(f"Script: {script_path}")
    print(f"Audio: {audio_path}")
    print(f"{'='*60}\n")
    
    return str(video_path)

if __name__ == "__main__":
    import os
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    
    print("\n" + "="*60)
    print("LINCOLN HORROR GENERATOR - WORKING")
    print("="*60)
    print(f"Generating {count} video(s)...\n")
    
    results = []
    for i in range(count):
        result = generate_video()
        if result:
            results.append(result)
        if i < count - 1:
            print("\nWaiting 5 seconds...\n")
            import time
            time.sleep(5)
    
    print(f"\n{'='*60}")
    print(f"COMPLETE: {len(results)}/{count} videos")
    print(f"{'='*60}")
    print(f"\nVideos in: {BASE_DIR / 'output/videos'}")
    print("\n")

