"""
ABRAHAM LINCOLN - FIXED MAX HEADROOM STYLE
- Removes stage directions from speech
- Uses deep male voice (sounds like Lincoln)
- Shows Abe on static TV screen
Run: python abe_FIXED.py 50
"""
import os, sys, json, requests, subprocess, random, time, re
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

ELEVENLABS_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
BTC = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"

# Deep male voices from ElevenLabs
MALE_VOICES = [
    "pNInz6obpgDQGcFmaJgB",  # Adam - deep
    "VR6AewLTigWG4xSOukaG",  # Arnold - masculine  
    "ErXwobaYiN019PkySvjV",  # Antoni - mature
    "yoZ06aMxZJJ28mfd3POQ",  # Sam - deep masculine
]

def scrape():
    headlines = []
    try:
        r = requests.get("https://news.google.com/rss", timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'xml')
            for item in soup.find_all('item')[:20]:
                if item.title:
                    headlines.append(item.title.text)
    except: pass
    return headlines if headlines else ["Trump Third Term", "Police Kill 64", "Climate Summit Fails"]

def roast_script(headline):
    """Create script WITHOUT stage directions in speech"""
    hl = headline.lower()
    
    # Script for SPEAKING (no stage directions)
    if "trump" in hl:
        speech = f"""Abraham Lincoln here. Dead since 1865.

{headline}.

Trump. This billionaire. Born with gold spoon. Never worked real day. Got handed everything. And he convinced POOR people he's one of them. The con of the century.

I grew up in a log cabin. ACTUAL poverty. Split rails. Read by candlelight. Taught myself law. EARNED everything.

This man? Inherited millions. Bankrupted casinos. Lost money running CASINOS. You know how hard that is?

But let's talk about YOU. You who enable this. You who make excuses. You who worship a man who wouldn't piss on you if you were on fire.

He calls you the poorly educated and you CHEER. He says he could shoot someone and you'd still vote for him and you NOD.

You're not victims. You're VOLUNTEERS. You're choosing this. Every day.

And the RICH people around him? The senators? The CEOs? The media moguls? You KNOW better. You went to good schools. You have resources.

But you enable him because it's PROFITABLE. Because you get tax cuts. Because you get power. You're selling out democracy for a yacht upgrade.

You're ALL guilty. Rich man manipulating. Poor people believing. Elite people enabling. Media people profiting.

EVERYONE has blood on their hands.

April 14, 1865. John Wilkes Booth shot me in the head. Lead ball through brain. Nine hours dying.

And you know what I saw? I saw THIS. I saw YOU. I saw what you'd become.

I died believing in America's potential. I was WRONG about you.

Stop pointing fingers. Start looking in mirrors.

Bitcoin: {BTC}"""

    elif any(w in hl for w in ["killed", "police", "dead", "shoot"]):
        speech = f"""Abraham Lincoln here. Speaking from beyond the grave.

{headline}.

Police violence. Let me roast ALL sides.

You got POWER. You got GUNS. You got AUTHORITY. And you're using it to kill people who can't fight back.

I commanded ARMIES during war. You know what my generals had? ACCOUNTABILITY. You know what you have? QUALIFIED IMMUNITY.

My soldiers faced enemy with weapons. You're shooting people with phones. With wallets. With NOTHING.

But YOU. You who see this and do NOTHING. You who say well they should have complied. You who value ORDER over JUSTICE.

When I saw injustice, I ACTED. I signed the Emancipation Proclamation knowing half the country would hate me.

What are YOU doing? Posting on Facebook? Sharing a hashtag? That's not activism, that's PERFORMANCE.

And the POLITICIANS. You who could change laws. Fund programs. Fix systems. But you don't because it's not politically convenient.

You give speeches. You take knees. You wear kente cloth. Then you vote for bigger police budgets.

You vote for these people. Every election. You pick the SAME corrupt politicians who promise change and deliver NOTHING.

Stop blaming the system. YOU ARE THE SYSTEM. You're choosing this every time you vote. Or DON'T vote.

Cops killing. Politicians enabling. People complying. Media profiting. EVERYONE is guilty.

I died for principles. What are you dying for?

Bitcoin: {BTC}"""

    else:
        speech = f"""Abraham Lincoln here. The tall guy with the beard. Got shot in the head at a theater.

{headline}.

Let me tell you who to blame: EVERYONE.

People with POWER doing NOTHING. People with MONEY hoarding it. People with PLATFORMS spreading lies.

You have resources. Education. Opportunity. And you use it for WHAT? To get richer? To get famous? To get MORE power?

And YOU. Regular people. You see problems and you complain but you don't ACT. You see injustice and you scroll past.

You have votes. You have voices. You have CHOICES. But you choose NOTHING. You choose COMFORT. You choose DISTRACTION.

The SYSTEM is broken? The system is people. It's YOU. It's THEM. It's ALL OF US.

Stop waiting for someone to save you. Stop blaming everyone else. Look in the mirror.

Rich people exploiting. Middle people enabling. Poor people suffering. Media people profiting. Politicians lying. Voters believing.

EVERYONE plays their part in this hellscape you call civilization.

And the worst part? You'll watch this. You'll laugh. You'll share it. Then you'll go right back to doing NOTHING.

April 14, 1865. Booth shot me. Lead ball through brain. Nine hours dying.

I died believing in human progress. I was wrong about you. All of you.

You're ALL complicit. You're ALL guilty. You're ALL responsible.

Stop pointing fingers. Start looking in mirrors.

Bitcoin: {BTC}"""

    return speech

def get_male_voice():
    """Get available male voices and pick best one"""
    try:
        r = requests.get("https://api.elevenlabs.io/v1/voices", 
                        headers={"xi-api-key": ELEVENLABS_KEY}, timeout=10)
        if r.status_code == 200:
            voices = r.json()['voices']
            # Look for deep male voices
            for voice in voices:
                name = voice['name'].lower()
                labels = voice.get('labels', {})
                # Find deep, mature, masculine voices
                if any(w in name for w in ['adam', 'arnold', 'sam', 'daniel', 'josh']):
                    print(f"    Using voice: {voice['name']}")
                    return voice['voice_id']
    except: pass
    # Fallback to known good voice
    return MALE_VOICES[0]

def audio(speech_text, output_path):
    """Generate audio with MALE voice, NO stage directions"""
    print("    [AUDIO - MALE VOICE]")
    try:
        voice_id = get_male_voice()
        
        r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}", 
                         json={
                             "text": speech_text,
                             "model_id": "eleven_multilingual_v2", 
                             "voice_settings": {
                                 "stability": 0.4,
                                 "similarity_boost": 0.9,
                                 "style": 0.8,
                                 "use_speaker_boost": True
                             }
                         }, 
                         headers={"xi-api-key": ELEVENLABS_KEY}, 
                         timeout=240)
        
        if r.status_code == 200:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            temp = output_path.parent / f"temp_{output_path.name}"
            with open(temp, "wb") as f: 
                f.write(r.content)
            
            # Add slight echo for eerie effect
            subprocess.run([
                "ffmpeg", "-i", str(temp),
                "-af", "aecho=0.8:0.88:60:0.4,bass=g=2",
                "-y", str(output_path)
            ], capture_output=True)
            temp.unlink()
            return True
    except Exception as e:
        print(f"    Error: {e}")
    return False

def create_video_with_abe(audio_path, output_path):
    """Create video with animated Abe portrait on CRT-style TV (offline, fast)."""
    print("    [VIDEO - ABE ON TV]")
    try:
        from moviepy.editor import AudioFileClip, ImageClip, CompositeVideoClip, ColorClip
        from PIL import Image, ImageDraw
        import math
        
        audio = AudioFileClip(str(audio_path))
        duration = min(audio.duration, 60.0)
        
        # Download Abe portrait if needed
        abe_img = BASE / "temp" / "lincoln.jpg"
        if not abe_img.exists():
            abe_img.parent.mkdir(exist_ok=True)
            url = "https://upload.wikimedia.org/wikipedia/commons/a/ab/Abraham_Lincoln_O-77_matte_collodion_print.jpg"
            img_data = requests.get(url, timeout=30).content
            with open(abe_img, "wb") as f:
                f.write(img_data)
        
        # Base background (dark purple)
        bg = ColorClip(size=(1080, 1920), color=(30, 20, 40), duration=duration).set_audio(audio)
        overlays = [bg]
        
        # Audio envelope for subtle zoom
        try:
            samples = audio.to_soundarray(fps=24)
            import numpy as np
            rms = np.sqrt((samples.astype(float) ** 2).mean(axis=1))
            rms = (rms / (rms.max() or 1)).clip(0, 1)
            def env(t):
                idx = int(min(len(rms)-1, max(0, t*24)))
                return float(rms[idx])
        except Exception:
            env = lambda t: 0.0
        
        base_w, base_h = 460, 600
        abe_base = ImageClip(str(abe_img)).resize((base_w, base_h))
        def size_fn(t):
            return (int(base_w * (1.0 + 0.05 * env(t))), int(base_h * (1.0 + 0.05 * env(t))))
        def pos_fn(t):
            return ((1080 - size_fn(t)[0]) // 2 + int(2 * math.sin(t * 6.0)), 1050 + int(3 * math.sin(t * 4.0)))
        abe_clip = abe_base.resize(lambda t: size_fn(t)).set_position(pos_fn).set_duration(duration).fadein(0.6).fadeout(0.6)
        overlays.append(abe_clip)
        
        # CRT scanlines overlay
        try:
            scan = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
            draw = ImageDraw.Draw(scan)
            for y in range(0, 1920, 4):
                draw.line([(0, y), (1080, y)], fill=(0, 0, 0, 70), width=2)
            scan_path = BASE / "temp" / f"scanlines_{int(time.time())}.png"
            scan.save(scan_path)
            scan_clip = ImageClip(str(scan_path)).set_opacity(0.3).set_duration(duration)
            overlays.append(scan_clip)
        except Exception:
            pass
        
        final = CompositeVideoClip(overlays, size=(1080, 1920))
        output_path.parent.mkdir(parents=True, exist_ok=True)
        final.write_videofile(str(output_path), fps=24, codec='libx264', audio_codec='aac', bitrate='8000k', preset='medium', verbose=False, logger=None)
        final.close()
        bg.close()
        return output_path.exists()
    except Exception as e:
        print(f"    Error: {e}")
        return False

def gen():
    t = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"\n{'='*70}\nVIDEO {t}\n{'='*70}")
    
    headlines = scrape()
    h = random.choice(headlines)
    print(f"Headline: {h[:60]}")
    
    speech = roast_script(h)
    print(f"Script: {len(speech)} chars (NO STAGE DIRECTIONS)")
    
    ap = BASE / f"audio/fixed_{t}.mp3"
    if not audio(speech, ap): 
        print("Audio failed")
        return None
    
    vp = BASE / f"videos/FIXED_{t}.mp4"
    if not create_video_with_abe(ap, vp): 
        print("Video failed")
        return None
    
    up = BASE / "uploaded" / f"ABE_FIXED_{t}.mp4"
    up.parent.mkdir(exist_ok=True)
    import shutil
    shutil.copy2(vp, up)
    
    mb = up.stat().st_size / (1024 * 1024)
    print(f"{'='*70}\nSUCCESS: {up.name} ({mb:.2f} MB)\n{'='*70}")
    return str(up)

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    print(f"\n🔧 GENERATING {count} FIXED ABE VIDEOS 🔧\n")
    
    success = 0
    for i in range(count):
        if gen(): 
            success += 1
        if i < count - 1: 
            time.sleep(20)
    
    print(f"\n{'='*70}\nCOMPLETE: {success}/{count}\n{'='*70}\n")
