"""
ABRAHAM LINCOLN - MAX HEADROOM TV STATIC EDITION (UPDATED)
Now uses full abraham_MAX_HEADROOM.py system with all features:
- VHS TV broadcast effects
- Lip-sync (D-ID/Wav2Lip)
- Jumpscare effects
- Bitcoin QR code
- Clean roast-style scripts (NO scene descriptions)
- Psychological audio layers
Run: python abe_maxheadroom.py 50
"""
import os, sys, json, requests, subprocess, random, time
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

# Import the full MAX_HEADROOM system
try:
    sys.path.insert(0, str(Path(__file__).parent))
    from abraham_MAX_HEADROOM import (
        generate_script,
        create_max_headroom_video,
        upload_to_youtube,
        get_warning_title,
        generate_lincoln_face_pollo,
        generate_audio_with_psychological_layers
    )
    USE_FULL_SYSTEM = True
except ImportError as e:
    print(f"[WARNING] Could not import full system: {e}")
    print("[FALLBACK] Using simplified version...")
    USE_FULL_SYSTEM = False

ELEVENLABS_KEY = os.getenv("ELEVENLABS_API_KEY", "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa")
VOICE = "pNInz6obpgDQGcFmaJgB"
BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
BTC = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"

# Abe Lincoln portrait for Max Headroom effect
ABE_IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/a/ab/Abraham_Lincoln_O-77_matte_collodion_print.jpg"

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
    return headlines if headlines else ["Trump Third Term", "64 Killed Rio Raid", "Climate Summit Fails"]

def roast_all_sides(headline):
    """Punch UP at power, punch DOWN at complicity - roast EVERYONE (UPDATED: NO SCENE DESCRIPTIONS)"""
    if USE_FULL_SYSTEM:
        # Use the clean roast script from main system (NO scene descriptions)
        return generate_script(headline)
    
    # FALLBACK: Clean roast format (no scene descriptions)
    hl = headline.lower()
    
    intro = f"""Abraham Lincoln! Six foot four! Freed the slaves and MORE!

{headline}

AMERICA! Let me roast EVERYONE involved in this bullshit."""

    # Detect who's involved and roast them ALL
    if "trump" in hl:
        body = f"""T-Trump? *[glitch]* Oh b-boy. Here we go.

*[Punching UP at Trump]*
This m-man. This BILLIONAIRE. Born with a g-gold spoon. Never worked a real day. Got h-handed everything. And he convinced POOR people he's one of them? *[static]* The con of the c-century!

I grew up in a l-log cabin. ACTUAL poverty. Split rails. Read by c-candlelight. Taught myself law. EARNED everything.

This m-man? Inherited millions. Bankrupted c-casinos. Lost money running CASINOS! You know how h-hard that is? *[glitch]*

*[Punching DOWN at supporters]*
But let's talk about Y-YOU. You who enable this. You who m-make excuses. You who w-worship a man who wouldn't p-piss on you if you were on fire.

He calls you the "poorly e-educated" and you CHEER. He says he could shoot someone and you'd still v-vote for him and you NOD. *[static crackles]*

You're not v-victims. You're VOLUNTEERS. You're choosing this. Every d-day.

*[Punching UP at elite enablers]*
And the R-RICH people around him? The senators? The c-CEOs? The media moguls? You KNOW better! You w-went to good schools! You have resources!

But you enable him b-because it's PROFITABLE. Because you get t-tax cuts. Because you get p-power. You're selling out democracy for a f-fucking yacht upgrade!

*[Static blast]*

You're ALL guilty. Rich man m-manipulating. Poor people b-believing. Elite people enabling. Media people p-profiting.

EVERYONE'S got blood on their h-hands."""

    elif any(w in hl for w in ["killed", "police", "shooting", "dead"]):
        body = f"""P-Police violence? *[glitch]* Let me roast ALL sides.

*[Punching UP at police]*
You got POWER. You got GUNS. You got AUTHORITY. And you're using it to k-kill people who can't fight back? *[static]*

I commanded ARMIES during war. You know what my g-generals had? ACCOUNTABILITY. You know what you have? QUALIFIED IMMUNITY.

My s-soldiers faced enemy with weapons. You're shooting people with p-phones. With w-wallets. With NOTHING.

*[Punching DOWN at complicity]*
But Y-YOU. You who see this and do NOTHING. You who say "well they should have c-complied." You who value ORDER over J-JUSTICE.

When I s-saw injustice, I ACTED. I signed the E-Emancipation Proclamation knowing half the country would h-hate me.

What are YOU doing? Posting on Facebook? Sharing a h-hashtag? That's not activism, that's PERFORMANCE.

*[Punching UP at politicians]*
And the P-POLITICIANS. You who could change laws. Fund programs. Fix systems. But you don't because it's not p-politically convenient.

You give speeches. You take k-knees. You wear kente cloth. Then you v-vote for bigger police budgets! *[glitch]*

*[Punching DOWN at voters]*
You v-vote for these people! Every election! You pick the SAME corrupt p-politicians who promise change and deliver NOTHING!

Stop b-blaming the system. YOU ARE THE SYSTEM. You're choosing this e-every time you vote. Or DON'T vote.

*[Static roar]*

Cops killing. Politicians enabling. People c-complying. Media profiting. EVERYONE'S guilty."""

    elif any(w in hl for w in ["climate", "hurricane", "flood", "weather"]):
        body = f"""C-Climate? *[glitch]* Oh this is g-good. So many people to roast.

*[Punching UP at corporations]*
Oil c-companies KNEW. In the 1970s! They had the RESEARCH. They knew fossil fuels would destroy the planet. And they b-buried it. LIED about it. Funded denial for DECADES.

*[static blast]*

Exxon. Shell. BP. You m-murdered the future for quarterly profits. You're not businessmen. You're g-genocidal maniacs in suits.

*[Punching UP at politicians]*
And POLITICIANS. You who took their money. You who p-passed their laws. You who KNEW and did nothing because your c-campaign needed funding.

Republicans denying it. Democrats t-talking about it but not ACTING on it. You're ALL useless!

*[Punching DOWN at consumers]*
But let's talk about Y-YOU. You with your SUV. Your cheap Amazon shit. Your b-beef every meal. Your fast fashion. Your CONSUMPTION.

You KNOW it's wrong. You've SEEN the data. But you don't c-care because it's CONVENIENT. Because change is HARD.

*[glitch]*

You're not innocent victims. You're PARTICIPANTS. Every purchase. Every v-vote. Every choice.

*[Punching sideways at everyone]*
Rich people destroying. Politicians enabling. Middle class c-consuming. Poor people suffering.

And the planet? The p-planet doesn't care about your excuses. The planet will be FINE. It's YOU who are fucked.

*[Static intensifies]*

EVERYONE'S guilty. Including m-me for dying before I could stop you."""

    else:
        body = f"""*[Static crackles]*

{headline}. Let me tell you who to b-blame: EVERYONE.

*[Punching UP at elite]*
People with POWER doing NOTHING. People with MONEY hoarding it. People with PLATFORMS spreading l-lies.

You have resources. Education. Opportunity. And you use it for WHAT? To get richer? To get f-famous? To get MORE power?

*[Punching DOWN at masses]*
And YOU. Regular people. You see problems and you c-complain but you don't ACT. You see injustice and you scroll past.

You have v-votes. You have voices. You have CHOICES. But you choose NOTHING. You choose COMFORT. You choose DISTRACTION.

*[Punching at systems]*
The SYSTEM is broken? The system is p-people! It's YOU! It's THEM! It's ALL OF US!

Stop waiting for s-someone to save you. Stop blaming everyone else. Look in the m-mirror.

*[Static blast]*

Rich people exploiting. Middle people enabling. Poor people suffering. Media people p-profiting. Politicians lying. Voters believing.

EVERYONE plays their part in this h-hellscape you call civilization.

*[Glitch]*

And the worst part? You'll watch this. You'll laugh. You'll share it. Then you'll go right b-back to doing NOTHING.

Prove me wrong. I d-dare you."""

    closing = f"""April 14, 1865. John Wilkes Booth shot me in the head. Nine hours dying.

I saw YOU. I saw what you'd become.

I died believing in America's potential. In human progress. I was WRONG.

You're ALL complicit. You're ALL guilty. You're ALL responsible.

Stop pointing fingers. Start looking in mirrors.

Look in mirrors."""

    return f"{intro}\n\n{body}\n\n{closing}"

def audio(s, o):
    """Generate audio with psychological layers (UPDATED)"""
    if USE_FULL_SYSTEM:
        # Use full system with psychological audio layers
        return generate_audio_with_psychological_layers(s, o)
    
    # FALLBACK: Simple audio generation
    print("    [AUDIO]")
    try:
        r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}", 
                         json={"text": s, "model_id": "eleven_multilingual_v2", 
                               "voice_settings": {"stability": 0.4, "similarity_boost": 0.75, 
                                                "style": 0.6, "use_speaker_boost": True}}, 
                         headers={"xi-api-key": ELEVENLABS_KEY}, timeout=240)
        if r.status_code == 200:
            o.parent.mkdir(parents=True, exist_ok=True)
            with open(o, "wb") as f: f.write(r.content)
            print("    [OK] Audio generated")
            return True
    except Exception as e:
        print(f"    [ERROR] {e}")
    return False

def create_maxheadroom_video(audio_path, output_path, headline="", lincoln_image=None):
    """Create Max Headroom style video with ALL features (UPDATED)"""
    print("    [VIDEO - MAX HEADROOM WITH ALL FEATURES]")
    
    if USE_FULL_SYSTEM:
        # Use full MAX_HEADROOM system with all features
        try:
            # Get or create Lincoln image
            if not lincoln_image:
                lincoln_image = generate_lincoln_face_pollo()
            
            # Convert paths to Path objects if needed
            audio_path_obj = Path(audio_path)
            output_path_obj = Path(output_path)
            lincoln_img_obj = Path(lincoln_image) if lincoln_image else None
            
            # Set environment for features
            os.environ['USE_LIPSYNC'] = '1'
            os.environ['USE_JUMPSCARE'] = '1'
            
            # Call full system
            success = create_max_headroom_video(
                lincoln_img_obj,
                audio_path_obj,
                output_path_obj,
                headline,
                use_lipsync=True,
                use_jumpscare=True
            )
            
            if success and Path(output_path).exists():
                mb = Path(output_path).stat().st_size / (1024 * 1024)
                print(f"    [OK] Video created: {mb:.2f} MB (ALL FEATURES)")
                return True
        except Exception as e:
            print(f"    [WARNING] Full system failed: {e}")
            print("    [FALLBACK] Using simplified version...")
    
    # FALLBACK: Simplified version
    try:
        probe = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)
        ], capture_output=True, text=True)
        duration = float(probe.stdout.strip())
        
        # Download Abe portrait if not exists
        abe_img = BASE / "temp" / "abe_portrait.jpg"
        if not abe_img.exists():
            abe_img.parent.mkdir(exist_ok=True)
            img_data = requests.get(ABE_IMAGE_URL, timeout=30).content
            with open(abe_img, "wb") as f: f.write(img_data)
        
        subprocess.run([
            "ffmpeg",
            "-loop", "1", "-i", str(abe_img),
            "-i", str(audio_path),
            "-vf", "scale=1080:1920,eq=contrast=1.8:brightness=0.1",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-c:a", "aac", "-b:a", "320k",
            "-t", str(duration),
            "-pix_fmt", "yuv420p",
            "-y", str(output_path)
        ], capture_output=True, timeout=600)
        
        return Path(output_path).exists()
        
    except Exception as e:
        print(f"    [ERROR] {e}")
        return False

def gen():
    t = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"\n{'='*70}\nMAX HEADROOM ABE {t} (UPDATED - ALL FEATURES)\n{'='*70}")
    
    headlines = scrape()
    h = random.choice(headlines)
    print(f"Headline: {h[:60]}")
    
    # Generate script (NO scene descriptions if using full system)
    s = roast_all_sides(h)
    print(f"Script: {len(s)} chars (CLEAN ROAST - NO scene descriptions)")
    
    # Generate audio with psychological layers
    ap = BASE / f"audio/maxhead_{t}.mp3"
    if not audio(s, ap): return None
    
    # Create video with ALL features (VHS, lip-sync, jumpscare, QR)
    vp = BASE / f"videos/MAXHEAD_{t}.mp4"
    if not create_maxheadroom_video(ap, vp, headline=h): return None
    
    # Copy to uploaded folder
    up = BASE / "uploaded" / f"ABE_MAXHEAD_{t}.mp4"
    up.parent.mkdir(exist_ok=True)
    import shutil
    shutil.copy2(vp, up)
    
    mb = up.stat().st_size / (1024 * 1024)
    print(f"{'='*70}\nSUCCESS: {up.name} ({mb:.2f} MB)")
    print("Features: VHS TV, Lip-sync, Jumpscare, Bitcoin QR")
    print(f"{'='*70}")
    
    # Auto-upload to YouTube if using full system
    if USE_FULL_SYSTEM:
        try:
            episode_num = int(os.getenv("EPISODE_NUM", random.randint(1000, 9999)))
            upload_to_youtube(up, h, episode_num=episode_num)
        except Exception as e:
            print(f"[WARNING] YouTube upload failed: {e}")
    
    return str(up)

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    print(f"\n📺 GENERATING {count} MAX HEADROOM ABE VIDEOS 📺\n")
    
    success = 0
    for i in range(count):
        if gen(): success += 1
        if i < count - 1: 
            time.sleep(20)
    
    print(f"\n{'='*70}\nCOMPLETE: {success}/{count}\n{'='*70}\n")
