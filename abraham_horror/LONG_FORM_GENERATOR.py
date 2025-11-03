"""
LONG-FORM VIDEO GENERATOR (3-10 minutes)
Creates deep-dive analysis videos for better watch time and monetization
Based on top performers: Education, Military, Government topics
"""
import os, sys, json, requests, subprocess, random, time, re
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
import numpy as np
from PIL import Image, ImageDraw

# API KEYS
ELEVENLABS_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
PEXELS_KEY = "RgE9Mdn3ToSQhn2RiLJ4mPMISjjp587QKRG9uhpOrLVtkKPCibUPUDGh"

BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
ROOT = Path("F:/AI_Oracle_Root/scarify")
YOUTUBE_CREDENTIALS = Path("F:/AI_Oracle_Root/scarify/config/credentials/youtube/client_secrets.json")
BTC = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"

# Google Sheets
SHEET_ID = "1jvWP95U0ksaHw97PrPZsrh6ZVllviJJof7kQ2dV0ka0"
try:
    from sheets_helper import read_headlines as sheets_read_headlines
except Exception:
    sheets_read_headlines = None

VOICES_MALE = [
    "VR6AewLTigWG4xSOukaG",
    "pNInz6obpgDQGcFmaJgB",
    "EXAVITQu4vr4xnSDxMaL",
]

# LONG-FORM TOPICS (Based on your top performers)
LONG_FORM_TOPICS = [
    {
        "theme": "Education System Collapse",
        "angle": "How the system is designed to fail you",
        "chapters": [
            "The Broken Promise",
            "Student Debt Slavery",
            "Corporate Takeover",
            "What Lincoln Would Say"
        ]
    },
    {
        "theme": "Military Draft Return",
        "angle": "Why they're bringing it back",
        "chapters": [
            "The Coming Wars",
            "Who Profits",
            "Your Kids on the Frontline",
            "Lincoln's Civil War vs Your War"
        ]
    },
    {
        "theme": "Government Shutdown Reality",
        "angle": "What they're not telling you",
        "chapters": [
            "The Real Reasons",
            "Who Benefits",
            "Your Money Disappeared",
            "Lincoln on Failed Government"
        ]
    },
    {
        "theme": "Economic Collapse Signals",
        "angle": "The recession they're hiding",
        "chapters": [
            "The Warning Signs",
            "1929 vs 2025",
            "Your Savings Evaporate",
            "Lincoln on Economic Slavery"
        ]
    }
]

def log(msg, status="INFO"):
    icons = {"INFO": "[INFO]", "SUCCESS": "[OK]", "ERROR": "[ERROR]", "PROCESS": "[PROCESS]"}
    print(f"{icons.get(status, '[INFO]')} {msg}")

def scrape_headlines():
    """Scrape headlines"""
    headlines = []
    
    if sheets_read_headlines and SHEET_ID:
        try:
            hs, _, _ = sheets_read_headlines(SHEET_ID, "Sheet1", 200)
            if hs:
                headlines.extend(hs[:20])
        except: pass
    
    try:
        r = requests.get("https://news.google.com/rss", timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'xml')
            news = [item.title.text for item in soup.find_all('item')[:30] if item.title]
            headlines.extend(news)
    except: pass
    
    if not headlines:
        headlines = ["Economic crisis deepens", "Government failures continue"]
    
    return headlines

def generate_long_form_script(topic, headline):
    """Generate 3-10 minute script with chapters"""
    
    script = f"""Abraham Lincoln. April 14, 1865. Ford's Theatre.

They shot me. But I didn't die. I'm speaking to you. From 2025.

Today's topic: {topic['theme']}.

Current headline: {headline}.

Let me break this down. In chapters. So you understand.

[CHAPTER 1: {topic['chapters'][0]}]

First, let's talk about the promise they made you.

Education will set you free. Democracy will protect you. Hard work will reward you.

All lies.

I grew up in a log cabin. Taught myself law by candlelight. Became president.

You grew up with the internet. Every answer at your fingertips. And you're MORE enslaved than my generation.

Why? Because the system EVOLVED.

They don't need chains anymore. They have student debt. They have algorithms. They have... convenience.

You volunteered for slavery and called it progress.

[CHAPTER 2: {topic['chapters'][1]}]

Now let's talk about who benefits from this.

In my time, slave owners profited from free labor.

In your time, corporations profit from YOUR data. YOUR attention. YOUR compliance.

Same exploitation. Different packaging.

They track you. Monetize you. Sell you. And you THANK them for it.

"But it's so convenient!" you say.

Yeah. Slavery was convenient for slave owners too.

[CHAPTER 3: {topic['chapters'][2]}]

Here's what's coming. And you won't like it.

{topic['angle']}.

The signs are obvious. You're just not looking.

Or maybe you're looking but not SEEING. Because seeing means admitting. And admitting means acting.

And acting is inconvenient.

So you scroll. You consume. You comply.

And then you're shocked when they come for YOU.

[CHAPTER 4: {topic['chapters'][3]}]

I led a civil war. 620,000 Americans died. To end slavery.

Now you're volunteering for digital slavery. Economic slavery. Surveillance slavery.

And when I point this out, you say "That's different."

Is it?

You're tracked 24/7. You owe money you can't repay. You work for wages that don't cover rent. You're one algorithm away from unemployment.

How is that free?

[CONCLUSION]

So here's my message from beyond the grave:

Wake up. Or stay asleep. Your choice.

But don't act surprised when the chains get heavier.

You were warned.

Abraham Lincoln. Still dead. Still right.

Support the truth: Bitcoin {BTC}

Links in description. Subscribe if you're awake. Scroll if you're sheep.

End transmission."""
    
    return script

def generate_audio(text, output_path):
    """Generate voice for long-form content"""
    log("Generating long-form voice...", "PROCESS")
    
    for voice_id in VOICES_MALE:
        try:
            r = requests.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                json={
                    "text": text,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {
                        "stability": 0.55,  # Higher for long-form clarity
                        "similarity_boost": 0.85,
                        "style": 0.75,
                        "use_speaker_boost": True
                    }
                },
                headers={"xi-api-key": ELEVENLABS_KEY},
                timeout=240  # Longer timeout for long content
            )
            if r.status_code == 200:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "wb") as f: f.write(r.content)
                log(f"Long-form voice generated", "SUCCESS")
                return True
        except Exception as e:
            log(f"Voice {voice_id} failed: {e}", "ERROR")
            continue
    return False

def create_long_form_video(audio_path, output_path, topic, headline):
    """Create 3-10min video with chapters"""
    log("Creating long-form video...", "PROCESS")
    
    try:
        from moviepy.editor import AudioFileClip, ImageClip, CompositeVideoClip, ColorClip
        
        audio = AudioFileClip(str(audio_path))
        duration = audio.duration  # No limit for long-form
        
        log(f"Long-form duration: {duration/60:.1f} minutes")
        
        # Get avatar
        custom = next(iter(ROOT.glob('ChatGPT Image*.png')), None)
        img_path = custom if custom and custom.exists() else BASE / "temp" / "lincoln.jpg"
        
        if not img_path.exists() or img_path.stat().st_size < 1000:
            img_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                data = requests.get("https://upload.wikimedia.org/wikipedia/commons/a/ab/Abraham_Lincoln_O-77_matte_collodion_print.jpg", timeout=15).content
                with open(img_path, "wb") as f: f.write(data)
            except:
                log("Failed to download image, using solid color", "ERROR")
                solid = Image.new('RGB', (1920, 1080), (20, 10, 15))
                solid_path = BASE / "temp" / "solid.jpg"
                solid.save(solid_path)
                img_path = solid_path
        
        # Long-form uses 16:9 horizontal format (not vertical)
        width, height = 1920, 1080
        
        bg = ColorClip(size=(width, height), color=(15, 10, 20), duration=duration).set_audio(audio)
        
        # Load and process avatar
        img = Image.open(str(img_path)).convert('RGB')
        small = img.resize((135, 175), Image.NEAREST)
        img_resized = small.resize((675, 875), Image.NEAREST)
        
        temp_img = BASE / "temp" / "long_avatar.jpg"
        img_resized.save(temp_img)
        
        # Position avatar on right side for 16:9
        abe = ImageClip(str(temp_img)).set_position((int(width*0.6), 'center')).set_duration(duration)
        
        # Create chapter markers (text overlays)
        chapter_times = [0, duration*0.25, duration*0.5, duration*0.75]
        chapter_clips = []
        
        for i, (chapter_name, chapter_time) in enumerate(zip(topic['chapters'], chapter_times)):
            if chapter_time < duration:
                chapter_img = Image.new('RGB', (800, 120), (30, 0, 0))
                chapter_draw = ImageDraw.Draw(chapter_img)
                chapter_draw.rectangle([(10, 10), (790, 110)], outline=(255, 100, 0), width=3)
                chapter_draw.text((400, 60), f"CHAPTER {i+1}: {chapter_name}", 
                                fill=(255, 255, 255), anchor="mm")
                
                chapter_path = BASE / f"temp/chapter_{i}.jpg"
                chapter_img.save(chapter_path)
                
                chapter_clip = ImageClip(str(chapter_path)).set_position((50, 50)).set_start(chapter_time).set_duration(3).set_opacity(0.9)
                chapter_clips.append(chapter_clip)
        
        # Compose
        layers = [bg, abe] + chapter_clips
        
        comp = CompositeVideoClip(layers, size=(width, height))
        
        comp.write_videofile(
            str(output_path),
            fps=24,
            codec='libx264',
            audio_codec='aac',
            bitrate='12000k',  # High quality for long-form
            preset='slow',  # Best quality
            verbose=False,
            logger=None
        )
        
        comp.close()
        bg.close()
        audio.close()
        
        log(f"Long-form video created: {duration/60:.1f}min", "SUCCESS")
        return True
        
    except Exception as e:
        log(f"Video creation failed: {e}", "ERROR")
        import traceback
        traceback.print_exc()
    return False

def upload_to_youtube(video_path, topic, headline):
    """Upload long-form to YouTube with chapters"""
    log("Uploading long-form to YouTube...", "PROCESS")
    
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        import pickle
        
        SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
        
        cred_files = [
            YOUTUBE_CREDENTIALS,
            Path("F:/AI_Oracle_Root/scarify/client_secret_679199614743-1fq6sini3p9kjs237ek4seg4ojp4a4qe.apps.googleusercontent.com.json"),
        ]
        
        cred_file = None
        for cf in cred_files:
            if cf and cf.exists():
                cred_file = cf
                break
        
        if not cred_file:
            log("YouTube credentials not found", "ERROR")
            return None
        
        token_file = BASE / "youtube_token.pickle"
        creds = None
        
        if token_file.exists():
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(str(cred_file), SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        youtube = build('youtube', 'v3', credentials=creds)
        
        # Get duration
        try:
            duration_result = subprocess.run([
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)
            ], capture_output=True, text=True, timeout=30)
            duration = float(duration_result.stdout.strip())
            minutes = int(duration // 60)
            seconds = int(duration % 60)
        except:
            duration = 300.0
            minutes, seconds = 5, 0
        
        title = f"Lincoln's DEEP DIVE: {topic['theme']} | {headline[:30]}"
        
        # Create chapters in description
        chapter_timestamps = []
        chapter_duration = duration / len(topic['chapters'])
        for i, chapter in enumerate(topic['chapters']):
            timestamp_seconds = int(i * chapter_duration)
            mins = timestamp_seconds // 60
            secs = timestamp_seconds % 60
            chapter_timestamps.append(f"{mins}:{secs:02d} - Chapter {i+1}: {chapter}")
        
        description = f"""Abraham Lincoln's {minutes}:{seconds:02d} deep dive on {topic['theme']}.

{headline}

CHAPTERS:
{chr(10).join(chapter_timestamps)}

Lincoln speaks from beyond the grave about modern slavery to systems.

{topic['angle']}

This is LONG-FORM analysis. Not a short. Sit down. Listen. Think.

Support truth: Bitcoin {BTC}

#AbrahamLincoln #DeepDive #LongForm #Analysis #Truth"""
        
        tags = [
            "Abraham Lincoln", topic['theme'].split()[0], "Deep Dive",
            "Long Form", "Analysis", "Commentary", "History"
        ]
        
        request_body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': '25'  # News & Politics for long-form
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
            }
        }
        
        media = MediaFileUpload(str(video_path), chunksize=-1, resumable=True)
        request = youtube.videos().insert(
            part=','.join(request_body.keys()),
            body=request_body,
            media_body=media
        )
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"    Upload: {int(status.progress() * 100)}%", end='\r')
        
        video_id = response['id']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        log(f"Uploaded LONG-FORM: {video_url}", "SUCCESS")
        log(f"Duration: {minutes}:{seconds:02d}", "INFO")
        log(f"Studio: https://studio.youtube.com/channel/UCS5pEpSCw8k4wene0iv0uAg/videos", "INFO")
        
        return video_url
        
    except Exception as e:
        log(f"Upload failed: {e}", "ERROR")
        return None

def generate_long_form_video():
    """Generate one long-form video"""
    t = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Choose topic
    topic = random.choice(LONG_FORM_TOPICS)
    
    # Get current headline
    headlines = scrape_headlines()
    headline = random.choice(headlines)
    
    log(f"\n{'='*70}\nLONG-FORM VIDEO\n{'='*70}", "INFO")
    log(f"Topic: {topic['theme']}")
    log(f"Headline: {headline[:60]}")
    log(f"Chapters: {len(topic['chapters'])}")
    
    # Generate script
    script = generate_long_form_script(topic, headline)
    log(f"Script: {len(script)} chars (long-form)")
    
    # Generate audio
    ap = BASE / f"audio/long_{t}.mp3"
    if not generate_audio(script, ap):
        return None
    
    # Create video
    vp = BASE / f"videos/LONG_{t}.mp4"
    if not create_long_form_video(ap, vp, topic, headline):
        return None
    
    # Upload
    youtube_url = upload_to_youtube(vp, topic, headline)
    
    # Save
    up = BASE / "uploaded" / f"LONG_FORM_{t}.mp4"
    up.parent.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy2(vp, up)
    
    mb = up.stat().st_size / (1024 * 1024)
    
    log(f"\n{'='*70}\nLONG-FORM COMPLETE\n{'='*70}", "SUCCESS")
    log(f"Topic: {topic['theme']}")
    log(f"File: {up.name} ({mb:.1f}MB)")
    if youtube_url:
        log(f"YouTube: {youtube_url}")
    log(f"{'='*70}\n")
    
    return {
        'topic': topic['theme'],
        'video_path': str(up),
        'youtube_url': youtube_url
    }

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 2
    
    log(f"\n{'='*70}")
    log(f"LONG-FORM VIDEO GENERATOR (3-10 minutes)")
    log(f"{'='*70}")
    log(f"Format: 16:9 horizontal (1920×1080)")
    log(f"Duration: 3-10 minutes with chapters")
    log(f"Based on top performers: Education, Military, Government")
    log(f"Generating {count} long-form videos")
    log(f"{'='*70}\n")
    
    results = []
    for i in range(count):
        result = generate_long_form_video()
        if result:
            results.append(result)
        if i < count - 1:
            log("\nWaiting 5 seconds...\n")
            time.sleep(5)
    
    log(f"\n{'='*70}")
    log(f"LONG-FORM GENERATION COMPLETE: {len(results)}/{count}")
    log(f"{'='*70}\n")
    
    for r in results:
        print(f"[LONG] {r['topic']}")
        if r.get('youtube_url'):
            print(f"  URL: {r['youtube_url']}")


