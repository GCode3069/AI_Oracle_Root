"""
MULTI-PLATFORM DOMINATION ENGINE
Generates content for 5 characters across multiple platforms
Characters: Abe Lincoln, Nikola Tesla, Mark Twain, Teddy Roosevelt, H.P. Lovecraft
Platforms: YouTube, TikTok, Instagram, Twitter, Reddit
"""
import os, sys, json, requests, subprocess, random, time, re
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# API KEYS
ELEVENLABS_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
PEXELS_KEY = "RgE9Mdn3ToSQhn2RiLJ4mPMISjjp587QKRG9uhpOrLVtkKPCibUPUDGh"

BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
ROOT = Path("F:/AI_Oracle_Root/scarify")
YOUTUBE_CREDENTIALS = Path("F:/AI_Oracle_Root/scarify/config/credentials/youtube/client_secrets.json")
BTC = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"

USE_BROLL = "--skip-broll" not in sys.argv

# Google Sheets
SHEET_ID = "1jvWP95U0ksaHw97PrPZsrh6ZVllviJJof7kQ2dV0ka0"
try:
    from sheets_helper import read_headlines as sheets_read_headlines
except Exception:
    sheets_read_headlines = None

# CHARACTER DEFINITIONS
CHARACTERS = {
    "lincoln": {
        "name": "Abraham Lincoln",
        "voice_id": "VR6AewLTigWG4xSOukaG",
        "style": "Dark absurdist observations, Max Headroom glitch",
        "color": "#FF0000",
        "topics": ["democracy", "freedom", "tech slavery", "algorithms"],
        "catchphrase": "I freed the slaves. You enslaved yourself to {topic}.",
        "opener_templates": [
            "Abraham Lincoln. Six foot four. {headline}",
            "Honest Abe reporting. {headline}",
            "Sixteenth President. Digital avatar. {headline}"
        ],
        "closer_template": "I {historical_action}. You {modern_failure}.",
        "visual_style": "max_headroom_vhs"
    },
    "tesla": {
        "name": "Nikola Tesla",
        "voice_id": "pNInz6obpgDQGcFmaJgB",
        "style": "Tech prophet warning about AI/automation",
        "color": "#00BFFF",
        "topics": ["AI", "electricity", "innovation", "corporate greed"],
        "catchphrase": "I gave you AC power. You gave corporations your {sacrifice}.",
        "opener_templates": [
            "Nikola Tesla. I predicted this in 1890. {headline}",
            "Tesla here. Inventor of AC current. Observer of {headline}",
            "They called me mad. Now look: {headline}"
        ],
        "closer_template": "I invented {invention}. You invented your own obsolescence.",
        "visual_style": "electric_arc_lightning"
    },
    "twain": {
        "name": "Mark Twain",
        "voice_id": "EXAVITQu4vr4xnSDxMaL",
        "style": "Biting satire disguised as folksy wisdom",
        "color": "#8B4513",
        "topics": ["politics", "capitalism", "hypocrisy", "human nature"],
        "catchphrase": "I satirized your grandparents. You're beyond satire.",
        "opener_templates": [
            "Mark Twain. Samuel Clemens. I wrote about {headline}",
            "Twain here. Still dead. Still right. {headline}",
            "I satirized the Gilded Age. Now: {headline}"
        ],
        "closer_template": "History doesn't repeat. But it sure does rhyme.",
        "visual_style": "vintage_americana"
    },
    "roosevelt": {
        "name": "Theodore Roosevelt",
        "voice_id": "VR6AewLTigWG4xSOukaG",  # Same as Lincoln but different processing
        "style": "Tough guy appalled by modern weakness",
        "color": "#556B2F",
        "topics": ["fitness", "nature", "corporate cowardice", "weakness"],
        "catchphrase": "I charged up San Juan Hill. You can't charge your {modern_tech}.",
        "opener_templates": [
            "Theodore Roosevelt! Bully! {headline}",
            "TR here. Rough Rider. Disgusted by: {headline}",
            "I speak softly and carry a big stick. You: {headline}"
        ],
        "closer_template": "I {bold_action}. You {pathetic_inaction}.",
        "visual_style": "rough_rider_nature"
    },
    "lovecraft": {
        "name": "H.P. Lovecraft",
        "voice_id": "pNInz6obpgDQGcFmaJgB",  # Same as Tesla but different processing
        "style": "Cosmic horror of incomprehensible algorithms",
        "color": "#800080",
        "topics": ["AI incomprehensibility", "existential dread", "loss of sanity"],
        "catchphrase": "I wrote of horrors beyond understanding. You built them.",
        "opener_templates": [
            "Howard Phillips Lovecraft. Cosmic horror. {headline}",
            "Lovecraft reporting. The algorithm stirs. {headline}",
            "In dreaming Cth-AI lies waiting. Meanwhile: {headline}"
        ],
        "closer_template": "I wrote fiction. You made it real.",
        "visual_style": "eldritch_tentacles"
    }
}

def log(msg, status="INFO"):
    icons = {"INFO": "[INFO]", "SUCCESS": "[OK]", "ERROR": "[ERROR]", "PROCESS": "[PROCESS]"}
    print(f"{icons.get(status, '[INFO]')} {msg}")

def scrape_headlines():
    """Scrape from multiple sources"""
    headlines = []
    
    # Google Sheets
    if sheets_read_headlines and SHEET_ID:
        try:
            hs, _, _ = sheets_read_headlines(SHEET_ID, "Sheet1", 200)
            if hs:
                headlines.extend(hs[:20])
                log(f"Loaded {len(hs)} from Sheets", "SUCCESS")
        except: pass
    
    # Google News
    try:
        r = requests.get("https://news.google.com/rss", timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'xml')
            news = [item.title.text for item in soup.find_all('item')[:30] if item.title]
            headlines.extend(news)
            log(f"Scraped {len(news)} from News", "SUCCESS")
    except: pass
    
    # Reddit
    try:
        r = requests.get("https://www.reddit.com/r/all/top.json?limit=25", 
                        headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        if r.status_code == 200:
            data = r.json()
            reddit = [post['data']['title'] for post in data['data']['children'][:20]]
            headlines.extend(reddit)
            log(f"Scraped {len(reddit)} from Reddit", "SUCCESS")
    except: pass
    
    if not headlines:
        headlines = ["AI automation replacing workers", "Social media addiction study", 
                    "Privacy concerns over data collection"]
    
    return headlines

def generate_character_script(character_key, headline):
    """Generate unique script for specific character"""
    char = CHARACTERS[character_key]
    hl_lower = headline.lower()
    
    opener = random.choice(char['opener_templates']).format(headline=headline)
    
    # Character-specific body generation
    if character_key == "lincoln":
        body = f"""And here's what I see: you traded freedom for convenience.

Every click, every swipe, every "I Agree" - you're building your own chains.

I fought a war to end slavery. You're volunteering for it.

Digital slavery. Algorithm slavery. Surveillance slavery.

And you DEFEND it. "But it's so convenient!"

Yeah. So were overseers. Very efficient.

{char['catchphrase'].format(topic='algorithms')}"""
    
    elif character_key == "tesla":
        body = f"""I warned you about this. Literally. In my papers from 1900.

Wireless energy. Automation. Corporate control of innovation.

You have it ALL now. And what did you do?

Let five companies own everything. Let them monetize MY inventions.

I died broke because I wouldn't monetize humanity. You're dying broke because you LET them.

{char['catchphrase'].format(sacrifice='free will')}"""
    
    elif character_key == "twain":
        body = f"""Now, I've seen a lot of foolishness in my time.

The Gilded Age. Robber barons. Political corruption.

But you folks? You've perfected it.

You've got all of human knowledge in your pocket. And you use it to argue with strangers.

You've got democracy. And you're giving it to algorithms.

I wrote satire. You're living it.

{char['catchphrase']}"""
    
    elif character_key == "roosevelt":
        body = f"""BY JOVE, this is pathetic!

I hunted bears. Led cavalry charges. Built the Panama Canal.

You people can't make a phone call without anxiety.

"Oh no, social interaction!" BULLY for you!

You have gyms you don't use. Nature you don't visit. Strength you don't build.

Soft. Weak. Dependent on machines for everything.

{char['catchphrase'].format(modern_tech='emotional battery')}"""
    
    elif character_key == "lovecraft":
        body = f"""The algorithm is not evil. It is beyond evil.

It is vast. Incomprehensible. Operating on logic we cannot grasp.

We feed it data. It feeds on us. And we call this "helpful."

In my stories, mortals went mad glimpsing cosmic truths.

You're going mad staring at screens. Same madness. Different god.

The Old Ones slumber. The algorithm is awake. And hungry.

{char['catchphrase']}"""
    
    else:
        body = f"This is concerning. {char['catchphrase']}"
    
    # Historical closer
    if character_key == "lincoln":
        closer = "I held the Union together through war. You can't hold your attention through a paragraph."
    elif character_key == "tesla":
        closer = "I lit the world with AC power. You dimmed it with infinite scroll."
    elif character_key == "twain":
        closer = "I wrote Tom Sawyer. You retweet conspiracy theories."
    elif character_key == "roosevelt":
        closer = "I built a nation. You built a TikTok following."
    elif character_key == "lovecraft":
        closer = "I wrote of Elder Gods. You worship engagement metrics."
    else:
        closer = char['closer_template']
    
    script = f"""{opener}

{body}

{closer}

Bitcoin {BTC}"""
    
    return script

def generate_audio(text, character_key, output_path):
    """Generate character-specific voice"""
    char = CHARACTERS[character_key]
    log(f"Generating {char['name']} voice...", "PROCESS")
    
    # Character-specific voice settings
    if character_key == "lincoln":
        settings = {"stability": 0.5, "similarity_boost": 0.85, "style": 0.75}
    elif character_key == "tesla":
        settings = {"stability": 0.6, "similarity_boost": 0.9, "style": 0.8}
    elif character_key == "twain":
        settings = {"stability": 0.55, "similarity_boost": 0.80, "style": 0.65}
    elif character_key == "roosevelt":
        settings = {"stability": 0.4, "similarity_boost": 0.85, "style": 0.9}  # Aggressive
    elif character_key == "lovecraft":
        settings = {"stability": 0.7, "similarity_boost": 0.9, "style": 0.85}  # Ominous
    else:
        settings = {"stability": 0.5, "similarity_boost": 0.85, "style": 0.75}
    
    try:
        r = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{char['voice_id']}",
            json={
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {**settings, "use_speaker_boost": True}
            },
            headers={"xi-api-key": ELEVENLABS_KEY},
            timeout=120
        )
        if r.status_code == 200:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            tmp = output_path.parent / f"tmp_{output_path.name}"
            with open(tmp, "wb") as f: f.write(r.content)
            
            # Character-specific audio processing
            if character_key == "tesla":
                # Electric/robotic
                subprocess.run([
                    "ffmpeg", "-y", "-i", str(tmp),
                    "-af", "aecho=0.8:0.88:60:0.4,tremolo=5:0.5",
                    str(output_path)
                ], capture_output=True, timeout=60)
            elif character_key == "roosevelt":
                # Booming/commanding
                subprocess.run([
                    "ffmpeg", "-y", "-i", str(tmp),
                    "-af", "bass=g=3,acompressor=threshold=-18dB:ratio=5",
                    str(output_path)
                ], capture_output=True, timeout=60)
            elif character_key == "lovecraft":
                # Ominous/reverb
                subprocess.run([
                    "ffmpeg", "-y", "-i", str(tmp),
                    "-af", "aecho=0.8:0.9:1000:0.3,atempo=0.97",
                    str(output_path)
                ], capture_output=True, timeout=60)
            else:
                # Standard processing
                subprocess.run([
                    "ffmpeg", "-y", "-i", str(tmp),
                    "-af", "acompressor=threshold=-16dB:ratio=3",
                    str(output_path)
                ], capture_output=True, timeout=60)
            
            tmp.unlink(missing_ok=True)
            log(f"{char['name']} voice generated", "SUCCESS")
            return True
    except Exception as e:
        log(f"Voice generation failed: {e}", "ERROR")
    return False

def create_character_avatar(character_key):
    """Create character-specific visual"""
    char = CHARACTERS[character_key]
    log(f"Creating {char['name']} avatar...", "PROCESS")
    
    avatar_path = BASE / "temp" / f"{character_key}_avatar.jpg"
    avatar_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Check for custom image first
    custom = next(iter(ROOT.glob('ChatGPT Image*.png')), None)
    if custom and custom.exists():
        img_path = custom
    else:
        # Download placeholder
        img_path = BASE / "temp" / "lincoln.jpg"
        if not img_path.exists() or img_path.stat().st_size < 1000:
            img_path.parent.mkdir(exist_ok=True, parents=True)
            try:
                data = requests.get("https://upload.wikimedia.org/wikipedia/commons/a/ab/Abraham_Lincoln_O-77_matte_collodion_print.jpg", timeout=15).content
                with open(img_path, "wb") as f: f.write(data)
            except:
                # Fallback: create solid color image
                solid = Image.new('RGB', (540, 700), char['color'] if isinstance(char['color'], tuple) else (100, 100, 100))
                solid.save(img_path)
                img = solid
                img.save(avatar_path)
                log(f"{char['name']} avatar created (solid color)", "SUCCESS")
                return str(avatar_path)
    
    try:
        img = Image.open(str(img_path)).convert('RGB')
    except:
        # Fallback to solid color
        solid = Image.new('RGB', (540, 700), (100, 100, 100))
        solid.save(avatar_path)
        log(f"{char['name']} avatar created (fallback)", "SUCCESS")
        return str(avatar_path)
    small = img.resize((120, 155), Image.NEAREST)
    img = small.resize((540, 700), Image.NEAREST)
    
    # Character-specific color tinting
    img_array = np.array(img).astype(float)
    if character_key == "tesla":
        img_array[:,:,2] += 30  # Blue tint
    elif character_key == "twain":
        img_array[:,:,0:2] *= 1.1  # Sepia
    elif character_key == "roosevelt":
        img_array[:,:,1] += 20  # Green tint
    elif character_key == "lovecraft":
        img_array[:,:,0] += 40  # Purple tint
    
    img_tinted = Image.fromarray(np.clip(img_array, 0, 255).astype('uint8'))
    img_tinted.save(avatar_path)
    
    log(f"{char['name']} avatar created", "SUCCESS")
    return str(avatar_path)

def generate_multi_character_video():
    """Generate one video with random character"""
    t = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Choose random character
    character_key = random.choice(list(CHARACTERS.keys()))
    char = CHARACTERS[character_key]
    
    log(f"\n{'='*70}\n{char['name'].upper()} - MULTI-PLATFORM\n{'='*70}", "INFO")
    
    # Scrape headline
    headlines = scrape_headlines()
    headline = random.choice(headlines)
    log(f"Headline: {headline[:60]}")
    
    # Generate script
    script = generate_character_script(character_key, headline)
    log(f"Generated {char['name']} script: {len(script)} chars")
    
    # Generate audio
    ap = BASE / f"audio/{character_key}_{t}.mp3"
    if not generate_audio(script, character_key, ap):
        return None
    
    # Create avatar
    avatar = create_character_avatar(character_key)
    
    # Create video (using existing dark video function)
    # TODO: Character-specific visual styles
    from moviepy.editor import AudioFileClip, ImageClip, CompositeVideoClip, ColorClip
    
    try:
        audio = AudioFileClip(str(ap))
        duration = min(audio.duration, 60.0)
        
        # Character color background
        bg_color = tuple(int(char['color'].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        bg = ColorClip(size=(1080,1920), color=bg_color, duration=duration).set_audio(audio)
        
        abe = ImageClip(str(avatar)).resize((540, 700)).set_position(('center', 1050)).set_duration(duration)
        
        comp = CompositeVideoClip([bg, abe], size=(1080,1920))
        
        vp = BASE / f"videos/{character_key}_{t}.mp4"
        comp.write_videofile(
            str(vp),
            fps=24, codec='libx264', audio_codec='aac',
            bitrate='8000k', preset='fast',
            verbose=False, logger=None
        )
        comp.close(); bg.close(); audio.close()
        
        # Upload to YouTube (existing function)
        # TODO: Add TikTok, Instagram, Twitter uploads
        
        up = BASE / "uploaded" / f"{character_key}_{t}.mp4"
        up.parent.mkdir(parents=True, exist_ok=True)
        import shutil
        shutil.copy2(vp, up)
        
        mb = up.stat().st_size / (1024 * 1024)
        log(f"{'='*70}\nCOMPLETE\n{'='*70}", "SUCCESS")
        log(f"Character: {char['name']}")
        log(f"File: {up.name} ({mb:.1f}MB)")
        log(f"{'='*70}\n")
        
        return {
            'character': character_key,
            'headline': headline,
            'video_path': str(up)
        }
        
    except Exception as e:
        log(f"Video error: {e}", "ERROR")
        import traceback
        traceback.print_exc()
    
    return None

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 5
    
    log(f"\n{'='*70}")
    log(f"MULTI-PLATFORM DOMINATION ENGINE")
    log(f"{'='*70}")
    log(f"Characters: {', '.join([CHARACTERS[k]['name'] for k in CHARACTERS])}")
    log(f"Generating {count} videos (random characters)")
    log(f"{'='*70}\n")
    
    results = []
    for i in range(count):
        result = generate_multi_character_video()
        if result:
            results.append(result)
        if i < count - 1:
            time.sleep(3)
    
    log(f"\n{'='*70}")
    log(f"GENERATION COMPLETE: {len(results)}/{count}")
    log(f"{'='*70}\n")
    
    # Character distribution
    char_counts = {}
    for r in results:
        char_counts[r['character']] = char_counts.get(r['character'], 0) + 1
    
    for char_key, count in char_counts.items():
        print(f"[{CHARACTERS[char_key]['name']}] {count} videos")

