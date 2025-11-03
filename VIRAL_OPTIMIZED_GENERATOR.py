#!/usr/bin/env python3
"""
VIRAL OPTIMIZED ABRAHAM LINCOLN GENERATOR
- Algorithm-optimized titles, descriptions, tags
- Cross-platform posting (YouTube, TikTok, Instagram, X)
- Viral hooks and CTAs
- Analytics tracking
- Channel performance analysis
"""
import os, sys, json, requests, subprocess, random, time, re
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

# API Keys
ELEVENLABS_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
PEXELS_KEY = "RgE9Mdn3ToSQhn2RiLJ4mPMISjjp587QKRG9uhpOrLVtkKPCibUPUDGh"
VOICE = "pNInz6obpgDQGcFmaJgB"
BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
BTC = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"
REBEL_KIT = "trenchaikits.com/buy-rebel-$97"

# Setup directories
for d in ['audio', 'videos', 'youtube_ready', 'tiktok_ready', 'instagram_ready', 'temp', 'images', 'uploaded', 'analytics']:
    (BASE / d).mkdir(parents=True, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════════════
# VIRAL TITLE GENERATOR - Algorithm Optimized
# ═══════════════════════════════════════════════════════════════════════════

VIRAL_PATTERNS = {
    'shock': [
        "They DON'T Want You To Know This...",
        "This Will SHOCK You...",
        "Lincoln's SECRET Warning Revealed",
        "The TRUTH They Hide From You"
    ],
    'curiosity': [
        "Why Did Lincoln Say THIS Before Death?",
        "The Prophecy That Came True",
        "Lincoln Predicted This 160 Years Ago",
        "What Really Happened in 1865?"
    ],
    'urgency': [
        "This Changes EVERYTHING",
        "You Need To See This NOW",
        "Lincoln's FINAL Warning",
        "The Warning They Silenced"
    ],
    'numbers': [
        "The 1 Secret They Hide",
        "3 Reasons This Matters",
        "The #1 Fear Americans Have",
        "69% Fear This (Why?)"
    ]
}

def generate_viral_title(headline):
    """Generate algorithm-optimized viral title"""
    
    # Pick random pattern
    pattern_type = random.choice(['shock', 'curiosity', 'urgency', 'numbers'])
    pattern = random.choice(VIRAL_PATTERNS[pattern_type])
    
    # Extract key words from headline
    headline_keywords = headline.split()[:5]
    headline_snippet = " ".join(headline_keywords)
    
    # Combine patterns
    title_variations = [
        f"{pattern} | {headline_snippet[:40]}",
        f"Lincoln's Warning: {headline_snippet[:50]}",
        f"{headline_snippet[:45]} | The Truth They Hide",
        f"⚠️ {headline_snippet[:45]} | #Shorts",
        f"From The Grave: {headline_snippet[:45]}"
    ]
    
    title = random.choice(title_variations)
    
    # Ensure #Shorts is included for algorithm
    if "#Shorts" not in title:
        title = f"{title} #Shorts"
    
    # Max 100 chars (YouTube limit), optimize first 50 for CTR
    if len(title) > 100:
        title = title[:97] + "..."
    
    return title[:100]

# ═══════════════════════════════════════════════════════════════════════════
# VIRAL DESCRIPTION GENERATOR
# ═══════════════════════════════════════════════════════════════════════════

def generate_viral_description(headline, script_preview=""):
    """Generate algorithm-optimized description"""
    
    # First 2 lines are CRITICAL - algorithm reads these first
    hook_lines = [
        f"⚠️ LINCOLN'S WARNING FROM BEYOND THE GRAVE ⚠️",
        f"Abraham Lincoln speaks from Ford's Theatre, April 14, 1865...",
        f"The assassination prophecy that echoes through YOUR timeline.",
        f"{headline}"
    ]
    
    # Core description with keywords
    core_description = f"""
🔥 What This Video Reveals:
• The truth they don't want you to know
• Lincoln's prophecy come true
• Why this matters NOW more than ever
• The warning you need to hear

💀 FROM FORD'S THEATRE, 1865:
{script_preview[:200] if script_preview else "The corruption I fought metastasizes. Every lie echoes through my shattered skull..."}

💰 BITCOIN DONATIONS: {BTC}
🎯 REBEL KIT: {REBEL_KIT}

📺 WATCH NEXT:
• The prophecy that came true
• Lincoln's final warning
• The curse of Ford's Theatre

🎃 HALLOWEEN 2025 - THE REVOLUTION STARTS NOW 🎃

⚠️ WARNING: This content is for mature audiences. Historical horror from beyond the grave.

#AbrahamLincoln #Halloween2025 #Horror #Shorts #Viral #Lincoln #Government #Corruption #Bitcoin #Truth #Warning #FordTheatre #1865 #History #HorrorTikTok #Scary #Ghost #Prophecy #Revolution #RebelKit

🔔 SUBSCRIBE FOR MORE WARNINGS FROM BEYOND THE GRAVE
👍 LIKE IF THIS CHILLED YOUR BONES
💬 COMMENT: What do you think Lincoln would say about 2025?
📤 SHARE to warn others

The corruption I fought metastasizes. The democracy I died for crumbles. The tyranny spreads... and you let it happen.

Sic semper tyrannis. Thus always to tyrants.

From my grave, I watch. From theirs, they'll scream.
"""
    
    # Combine hook with core
    full_description = "\n".join(hook_lines[:2]) + "\n" + core_description
    
    # Ensure first 2 lines have keywords
    first_line = hook_lines[0]
    if headline not in first_line:
        full_description = f"{headline}\n{full_description}"
    
    return full_description[:5000]  # YouTube limit is 5000 chars

# ═══════════════════════════════════════════════════════════════════════════
# VIRAL TAGS GENERATOR - Multi-platform optimized
# ═══════════════════════════════════════════════════════════════════════════

VIRAL_TAGS = {
    'youtube': [
        # Core tags (always include)
        'abraham lincoln', 'halloween 2025', 'horror', 'shorts', 'viral',
        
        # Trending tags
        'lincoln', 'government', 'corruption', 'bitcoin', 'truth', 
        'warning', 'ford theatre', '1865', 'history', 'horror shorts',
        
        # Algorithm boosters
        'scary', 'ghost', 'prophecy', 'revolution', 'rebel kit',
        'historical horror', 'presidential', 'assassination',
        'beyond the grave', 'curse', 'haunted', 'supernatural',
        
        # Engagement tags
        'trending', 'shocking', 'must watch', 'you need to see this',
        'watch until end', 'ending will shock you'
    ],
    
    'tiktok': [
        'abrahamlincoln', 'halloween2025', 'horror', 'scary', 'fyp',
        'viral', 'trending', 'foryou', 'foryoupage', 'ghost', 'spooky',
        'history', 'true story', 'scary story', 'horrortok', 'lincoln',
        'government', 'truth', 'warning', 'prophecy', 'ford theatre'
    ],
    
    'instagram': [
        'abrahamlincoln', 'halloween2025', 'horror', 'scary', 'viralreels',
        'spooky', 'haunted', 'history', 'presidential', 'truecrime',
        'horrortok', 'ghost', 'supernatural', 'curse', 'warning'
    ]
}

def get_viral_tags(platform='youtube', headline=""):
    """Get optimized tags for platform"""
    
    base_tags = VIRAL_TAGS.get(platform, VIRAL_TAGS['youtube']).copy()
    
    # Extract keywords from headline
    headline_words = headline.lower().split()
    relevant_words = [w for w in headline_words if len(w) > 4 and w not in ['from', 'that', 'this', 'with', 'they']]
    
    # Add headline keywords
    base_tags.extend(relevant_words[:5])
    
    # Limit to max tags (YouTube: 500 chars, TikTok: varies, Instagram: 30 tags)
    if platform == 'youtube':
        # Join until under 500 chars
        tag_str = ", ".join(base_tags[:20])
        while len(tag_str) > 500:
            base_tags.pop()
            tag_str = ", ".join(base_tags)
    elif platform == 'tiktok':
        base_tags = base_tags[:10]  # TikTok prefers fewer tags
    elif platform == 'instagram':
        base_tags = base_tags[:30]  # Instagram limit
    
    return base_tags

# ═══════════════════════════════════════════════════════════════════════════
# HEADLINE & SCRIPT GENERATION
# ═══════════════════════════════════════════════════════════════════════════

def scrape_headlines():
    """Scrape real headlines"""
    headlines = []
    try:
        r = requests.get("https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en", timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'xml')
            for item in soup.find_all('item')[:25]:
                if item.title:
                    headlines.append(item.title.text)
    except:
        pass
    
    fallbacks = [
        "Government Corruption Exposed - Leaders Accept Bribes",
        "Economic Collapse Threatens Millions",
        "Cyber Attack Cripples Infrastructure",
        "Russia Nuclear Threat Escalates",
        "Major Data Breach - 50 Million Exposed"
    ]
    
    return headlines if headlines else fallbacks

def generate_maxheadroom_script(headline):
    """Generate Max Headroom style script with viral hooks"""
    
    gore_variants = [
        "Booth's derringer explodes my skull. Brain matter paints the box crimson.",
        "The bullet tears through my occiput. Grey matter sprays. Blood pools.",
        "Lead ball shatters cranium. Cerebral cortex torn. I drown in my own blood."
    ]
    
    script = f"""[TV STATIC HISS]

{random.choice(gore_variants)}

[CUT TO: LINCOLN ON TV STATIC]

April 14, 1865. Ford's Theatre. The derringer aimed. BANG.

[GLITCH EFFECT]

Now I speak to you... from beyond the grave.

{headline}

The corruption I fought? It metastasizes. Every lie becomes law. Every bribe becomes policy.

You live the nightmare I warned against.

[CUT TO: CLOSE UP - LINCOLN'S FACE STATIC]

The Union I preserved? It fragments.

The democracy I died for? It crumbles.

The tyranny spreads... unchecked.

[TV STATIC INTENSIFIES]

{headline}

This is not coincidence. This is the pattern. The evil compounds.

[GLITCH]

From my blood-soaked seat in eternity... I watch.

Sic semper tyrannis.

But the question remains: Who are the tyrants now?

[FINAL STATIC BURST]

Look in the mirror. You already know.

[END STATIC]"""
    
    return script

# ═══════════════════════════════════════════════════════════════════════════
# AUDIO GENERATION
# ═══════════════════════════════════════════════════════════════════════════

def generate_audio_glitchy(script, output_path):
    """Generate glitchy TV-style audio"""
    print("    [AUDIO] Generating glitchy voice...")
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_KEY
    }
    
    data = {
        "text": script,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.3,  # Lower for more emotion
            "similarity_boost": 0.85,
            "style": 0.8,  # Higher for more character
            "use_speaker_boost": True
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=120)
        if response.status_code == 200:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            # Add glitch effects with FFmpeg
            glitch_audio = output_path.with_suffix('.glitch.mp3')
            cmd = [
                'ffmpeg', '-i', str(output_path),
                '-af', 'aecho=0.8:0.88:60:0.4,highpass=f=200,lowpass=f=3000,volume=1.2',
                '-y', str(glitch_audio)
            ]
            subprocess.run(cmd, capture_output=True, timeout=60)
            
            if glitch_audio.exists():
                output_path.unlink()
                glitch_audio.rename(output_path)
            
            size_kb = output_path.stat().st_size / 1024
            print(f"    [OK] Audio: {size_kb:.2f} KB")
            return True
    except Exception as e:
        print(f"    [ERROR] Audio: {e}")
    
    return False

# ═══════════════════════════════════════════════════════════════════════════
# VIDEO GENERATION - MAX HEADROOM STYLE
# ═══════════════════════════════════════════════════════════════════════════

def download_lincoln_image():
    """Download real Lincoln image"""
    images_dir = BASE / "images"
    existing = list(images_dir.glob("lincoln_*.jpg"))
    if existing:
        return existing[0]
    
    lincoln_urls = [
        "https://upload.wikimedia.org/wikipedia/commons/a/ab/Abraham_Lincoln_O-77_matte_collodion_print.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/1/1b/Lincoln_in_1863_seated.jpg"
    ]
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(random.choice(lincoln_urls), headers=headers, timeout=30)
        if response.status_code == 200:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = images_dir / f"lincoln_{timestamp}.jpg"
            with open(output_file, 'wb') as f:
                f.write(response.content)
            return output_file
    except:
        pass
    
    return None

def create_maxheadroom_video(audio_path, output_path, headline):
    """Create Max Headroom style video with TV static effects"""
    print("    [VIDEO] Creating Max Headroom effect...")
    
    lincoln_img = download_lincoln_image()
    if not lincoln_img:
        print("    [ERROR] No Lincoln image")
        return False
    
    # Get audio duration
    try:
        result = subprocess.run([
            'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)
        ], capture_output=True, text=True)
        duration = float(result.stdout.strip())
    except:
        duration = 30
    
    # Create TV static overlay
    static_file = BASE / "temp" / "tv_static.mp4"
    if not static_file.exists():
        # Generate static noise
        cmd_static = [
            'ffmpeg', '-f', 'lavfi',
            '-i', 'nullsrc=size=1080x1920:rate=30',
            '-f', 'lavfi',
            '-i', 'noise=alls=20:allf=t+u',
            '-vf', 'format=yuv420p,eq=contrast=3.0:brightness=-0.5',
            '-t', '2',
            '-y', str(static_file)
        ]
        subprocess.run(cmd_static, capture_output=True, timeout=30)
    
    # Headline text (cleaned for FFmpeg)
    headline_clean = headline.replace("'", "").replace('"', "").replace(':', ' -')[:50]
    
    # Max Headroom video with effects
    filter_str = (
        f"scale=1080:1920,"
        f"eq=contrast=1.5:brightness=-0.4:gamma=0.8:saturation=0.5,"
        f"zoompan=z='min(zoom+0.002,1.3)':d={int(duration*25)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920,"
        f"fade=t=in:st=0:d=2,"
        f"curves=preset=darker,"
        f"drawtext=text='{headline_clean}':fontcolor=white:fontsize=85:x=(w-text_w)/2:y=80:box=1:boxcolor=black@0.9:boxborderw=5,"
        f"drawtext=text='REBEL KIT $97':fontcolor=yellow:fontsize=75:x=(w-text_w)/2:y=h-180:box=1:boxcolor=black@0.8,"
        f"drawtext=text='{REBEL_KIT[:40]}':fontcolor=cyan:fontsize=50:x=(w-text_w)/2:y=h-100:box=1:boxcolor=black@0.8"
    )
    
    cmd = [
        'ffmpeg', '-loop', '1', '-i', str(lincoln_img),
        '-i', str(audio_path),
        '-f', 'lavfi', '-i', 'noise=alls=20:allf=t+u',
        '-vf', filter_str,
        '-af', 'volume=0.9,highpass=f=200,lowpass=f=3000',
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
        '-c:a', 'aac', '-b:a', '192k',
        '-t', str(duration),
        '-pix_fmt', 'yuv420p',
        '-y', str(output_path)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True, timeout=300)
        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"    [OK] Video: {size_mb:.2f} MB")
        return True
    except Exception as e:
        print(f"    [ERROR] Video: {e}")
        return False

# ═══════════════════════════════════════════════════════════════════════════
# YOUTUBE UPLOAD - VIRAL OPTIMIZED
# ═══════════════════════════════════════════════════════════════════════════

def upload_to_youtube_viral(video_path, headline, script_preview=""):
    """Upload to YouTube with viral optimization"""
    
    try:
        import pickle
        from googleapiclient.discovery import build
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.http import MediaFileUpload
        from google.auth.transport.requests import Request
    except ImportError:
        print("    [WARNING] YouTube API packages not installed")
        return None
    
    creds_file = Path("F:/AI_Oracle_Root/scarify/client_secret_679199614743-1fq6sini3p9kjs237ek4seg4ojp4a4qe.apps.googleusercontent.com.json")
    token_file = BASE / "youtube_token.pickle"
    
    if not creds_file.exists():
        print("    [WARNING] YouTube credentials not found")
        return None
    
    try:
        creds = None
        if token_file.exists():
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(creds_file),
                    ['https://www.googleapis.com/auth/youtube.upload']
                )
                creds = flow.run_local_server(port=8080)
            
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        youtube = build('youtube', 'v3', credentials=creds)
        
        # Generate viral metadata
        title = generate_viral_title(headline)
        description = generate_viral_description(headline, script_preview)
        tags = get_viral_tags('youtube', headline)
        
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': '24'  # Entertainment
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
            }
        }
        
        print(f"    [UPLOAD] Title: {title}")
        print(f"    [UPLOAD] Tags: {len(tags)} tags")
        
        media = MediaFileUpload(str(video_path), chunksize=1024*1024, resumable=True)
        request = youtube.videos().insert(part=','.join(body.keys()), body=body, media_body=media)
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"    Upload: {int(status.progress() * 100)}%", end='\r')
        
        print()
        video_id = response['id']
        video_url = f"https://youtube.com/watch?v={video_id}"
        
        # Save analytics
        analytics_file = BASE / "analytics" / f"youtube_{video_id}.json"
        with open(analytics_file, 'w') as f:
            json.dump({
                'video_id': video_id,
                'url': video_url,
                'title': title,
                'headline': headline,
                'tags': tags,
                'uploaded_at': datetime.now().isoformat(),
                'platform': 'youtube'
            }, f, indent=2)
        
        print(f"    [OK] UPLOADED: {video_url}")
        return video_url
        
    except Exception as e:
        print(f"    [ERROR] Upload error: {e}")
        return None

# ═══════════════════════════════════════════════════════════════════════════
# MAIN GENERATION PIPELINE
# ═══════════════════════════════════════════════════════════════════════════

def generate_viral_video(count=1, upload=True):
    """Generate viral-optimized videos"""
    
    print(f"\n{'='*70}")
    print(f"🔥 VIRAL OPTIMIZED GENERATOR - {count} VIDEO(S)")
    print(f"{'='*70}\n")
    
    success_count = 0
    
    for i in range(count):
        print(f"\n{'='*70}")
        print(f"VIDEO {i+1}/{count}")
        print(f"{'='*70}")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Get headline
        headlines = scrape_headlines()
        headline = random.choice(headlines)
        print(f"Headline: {headline}")
        
        # Generate script
        script = generate_maxheadroom_script(headline)
        print(f"Script: {len(script)} chars")
        
        # Generate audio
        audio_path = BASE / "audio" / f"viral_{timestamp}.mp3"
        if not generate_audio_glitchy(script, audio_path):
            print("    [SKIP] Audio generation failed")
            continue
        
        # Generate video
        video_path = BASE / "videos" / f"VIRAL_{timestamp}.mp4"
        if not create_maxheadroom_video(audio_path, video_path, headline):
            print("    [SKIP] Video generation failed")
            continue
        
        size_mb = video_path.stat().st_size / (1024 * 1024)
        print(f"[OK] Video: {size_mb:.2f} MB")
        
        # Upload if requested
        if upload:
            url = upload_to_youtube_viral(video_path, headline, script[:200])
            if url:
                success_count += 1
                
                # Copy to platform folders
                import shutil
                for platform in ['youtube_ready', 'tiktok_ready', 'instagram_ready']:
                    platform_path = BASE / platform / video_path.name
                    shutil.copy2(video_path, platform_path)
                    print(f"    [COPIED] {platform}")
        
        if i < count - 1:
            print(f"\nWaiting 10 seconds...")
            time.sleep(10)
    
    print(f"\n{'='*70}")
    print(f"COMPLETE: {success_count}/{count} videos")
    print(f"{'='*70}\n")
    
    return success_count

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    upload = '--no-upload' not in sys.argv
    
    generate_viral_video(count, upload)

