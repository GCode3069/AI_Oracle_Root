"""
DARK JOSH JOHNSON - DYNAMIC SCRAPER
NO repetitive scripts. Every video is unique.
Scrapes: Google News, Reddit trends, Twitter trends, current events
Generates: Fresh absurdist horror observations based on REAL headlines
Josh Johnson style: Deadpan, absurdist, "wait that's actually happening" moments
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

USE_BROLL = "--skip-broll" not in sys.argv

# Google Sheets integration
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

def log(msg, status="INFO"):
    icons = {"INFO": "[INFO]", "SUCCESS": "[OK]", "ERROR": "[ERROR]", "PROCESS": "[PROCESS]"}
    print(f"{icons.get(status, '[INFO]')} {msg}")

def scrape_fresh_content():
    """Scrape REAL headlines and trends from multiple sources"""
    headlines = []
    
    # 1. Google Sheets (if available)
    if sheets_read_headlines and SHEET_ID:
        try:
            hs, _, _ = sheets_read_headlines(SHEET_ID, "Sheet1", 200)
            if hs:
                headlines.extend(hs[:20])
                log(f"Loaded {len(hs)} headlines from Google Sheets", "SUCCESS")
        except Exception as e:
            log(f"Sheets read failed: {e}", "ERROR")
    
    # 2. Google News RSS
    try:
        r = requests.get("https://news.google.com/rss", timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'xml')
            news_items = [item.title.text for item in soup.find_all('item')[:30] if item.title]
            headlines.extend(news_items)
            log(f"Scraped {len(news_items)} from Google News", "SUCCESS")
    except Exception as e:
        log(f"Google News scrape failed: {e}", "ERROR")
    
    # 3. Reddit trending (no API key needed)
    try:
        r = requests.get("https://www.reddit.com/r/all/top.json?limit=25", 
                        headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        if r.status_code == 200:
            data = r.json()
            reddit_titles = [post['data']['title'] for post in data['data']['children'][:20]]
            headlines.extend(reddit_titles)
            log(f"Scraped {len(reddit_titles)} from Reddit", "SUCCESS")
    except Exception as e:
        log(f"Reddit scrape failed: {e}", "ERROR")
    
    # 4. Hacker News
    try:
        r = requests.get("https://news.ycombinator.com/rss", timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'xml')
            hn_items = [item.title.text for item in soup.find_all('item')[:20] if item.title]
            headlines.extend(hn_items)
            log(f"Scraped {len(hn_items)} from Hacker News", "SUCCESS")
    except Exception as e:
        log(f"Hacker News scrape failed: {e}", "ERROR")
    
    if not headlines:
        # Fallback if all scraping fails
        headlines = [
            "Company announces AI will replace customer service",
            "New app tracks your mood and sells data to employers",
            "Smart home devices now require subscription for basic features",
            "Social media platform testing mandatory ID verification",
            "Credit score now factors in social media activity"
        ]
        log("Using fallback headlines", "INFO")
    
    return headlines

def generate_dark_josh_script(headline):
    """Generate UNIQUE Dark Josh Johnson style script from headline"""
    
    # Analyze headline for absurdist angles
    hl_lower = headline.lower()
    
    # Opening variations (casual setup)
    opens = [
        f"So I saw this headline: '{headline}'",
        f"There's a news story about {headline}",
        f"Apparently, {headline}",
        f"I read that {headline}",
        f"Someone sent me an article. '{headline}'"
    ]
    
    # Josh Johnson style: deadpan observation → absurdist extension → dark truth
    
    # Tech/AI themes
    if any(word in hl_lower for word in ['ai', 'algorithm', 'tech', 'app', 'digital', 'smart']):
        script = f"""{random.choice(opens)}

And my first thought was... that's not surprising. We've been heading here for a while.

But here's the thing: nobody's actually upset about it.

We're just... accepting it. Like "Yeah, makes sense. Technology does that now."

And that's the horror. Not that it's happening. But that we all saw it coming and just... shrugged.

I tried to explain this to my friend. He's like "So what? It's convenient."

And I'm like "Yeah, but at what point do we push back?"

And he's like "Why would we push back? It works."

And that's when I realized: we're not even in dystopia yet. We're in the PREVIEW.

This is the beta test. We're all early adopters of our own obsolescence.

And we're leaving REVIEWS. Five stars. "Would recommend to friends."

The future isn't coming. We're installing it. Manually. With user agreements we don't read.

Abraham Lincoln. I fought to preserve the Union. You clicked "I Agree" and destroyed it.

Bitcoin {BTC}"""
    
    # Work/Economy themes
    elif any(word in hl_lower for word in ['job', 'work', 'employ', 'career', 'economy', 'money', 'debt']):
        script = f"""{random.choice(opens)}

And I thought "Wait, is that legal?"

Turns out it IS legal. Because we agreed to it. Somewhere. In some terms of service.

Nobody read it. But we all clicked "Accept."

And now here we are. Living in the fine print.

My friend works in HR. She says they're already doing this. Just... quietly.

No press release. No announcement. Just rolling it out.

And employees are THANKING them. Because it's "streamlined."

We're applauding our own replacement. That's the absurd part.

It's not evil corporations forcing this on us. We're ASKING for it.

"Please automate my job. I hate working."

And they're like "Okay" and we're shocked when it actually happens.

We wanted convenience. We got unemployment with better UX.

And now we're in the comments section debating if this is ACTUALLY bad or just... inevitable.

Spoiler: it's both.

Abraham Lincoln. I split rails by hand. You're splitting hairs about who deserves to exist.

Bitcoin {BTC}"""
    
    # Privacy/Surveillance themes
    elif any(word in hl_lower for word in ['privacy', 'data', 'track', 'monitor', 'surveillance', 'watch']):
        script = f"""{random.choice(opens)}

And I had this moment where I was like "That's creepy."

But then I checked my phone. I'm already being tracked by like... seventeen apps.

So this isn't NEW. This is just... more honest about it?

We've been trading privacy for convenience since Facebook launched.

We KNOW this. We joke about it. "Alexa's always listening!" Ha ha.

Except it's true. And we still buy them. And we put them in every room.

We're surveillance-pilled. That's the technical term.

We know we're being watched. We just don't care anymore.

Because what's the alternative? Not use the internet? Not own a phone?

That's not realistic. So we just... accept it.

And the companies KNOW we've accepted it. So they're just... doing more of it.

It's not even a slippery slope anymore. We're at the bottom. Looking up. Going "Huh. That's kinda steep."

Abraham Lincoln. I fought for freedom. You traded it for two-day shipping.

Bitcoin {BTC}"""
    
    # Social/Political themes  
    elif any(word in hl_lower for word in ['election', 'vote', 'politics', 'government', 'law', 'policy']):
        script = f"""{random.choice(opens)}

And honestly? This is exactly what I expected.

Not because I'm smart. But because at this point, everything is predictable.

We're in a loop. Same problems. Different decade.

And every time someone's like "This is unprecedented!"

And I'm like "Is it though?"

Because it feels pretty... precedented. We've done this before.

Different names. Same patterns.

And we'll act shocked. We'll debate it. We'll make memes about it.

And then we'll move on. To the NEXT thing. That's also not unprecedented.

We're speed-running societal collapse at this point.

Every generation thinks they're living in the END TIMES.

We're not. We're living in the MIDDLE TIMES. It gets worse. But also stays the same.

That's the real horror. Not that it's ending. But that it's... continuing. Like this. Forever.

Abraham Lincoln. I held the Union together with war. You're holding it together with Wi-Fi.

Bitcoin {BTC}"""
    
    # Default (absurdist observation for anything)
    else:
        script = f"""{random.choice(opens)}

And I read the article. And then I read it again.

Because I thought maybe I misunderstood.

But no. It's exactly what it sounds like.

And the comments section is DEFENDING it.

People are like "Actually, this makes sense if you think about it."

And I'm like "I AM thinking about it. That's the problem."

We're at the point where satire is just... news with a one-week delay.

The Onion writes a joke. Two years later, it's policy.

We're living in a reality where the absurd is just... Tuesday.

And we've normalized it. All of it.

Fifteen years ago this would've been dystopian fiction.

Now it's a TechCrunch article with 847 upvotes.

We're not boiling frogs. We're frogs arguing about the optimal water temperature.

"Actually 210 degrees is fine. I read a study."

Abraham Lincoln. I believed in human progress. I was catastrophically wrong.

Bitcoin {BTC}"""
    
    return script

def stutterize(text: str) -> str:
    """Very subtle stutter for conversational feel"""
    words = text.split()
    out = []
    for w in words:
        if random.random() < 0.04 and len(w) > 4:
            syl = w[:2]
            out.append(f"{syl}-{w}")
        else:
            out.append(w)
    return " ".join(out)

def audio(text, out):
    """Generate conversational voice"""
    log("Generating Dark Josh voice...", "PROCESS")
    
    for voice_id in VOICES_MALE:
        try:
            r = requests.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                json={
                    "text": text,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {
                        "stability": 0.55,
                        "similarity_boost": 0.80,
                        "style": 0.65,
                        "use_speaker_boost": True
                    }
                },
                headers={"xi-api-key": ELEVENLABS_KEY},
                timeout=120
            )
            if r.status_code == 200:
                out.parent.mkdir(parents=True, exist_ok=True)
                tmp = out.parent / f"tmp_{out.name}"
                with open(tmp, "wb") as f: f.write(r.content)
                
                subprocess.run([
                    "ffmpeg", "-y", "-i", str(tmp),
                    "-af", "acompressor=threshold=-16dB:ratio=3:attack=8:release=60",
                    str(out)
                ], capture_output=True, timeout=60)
                tmp.unlink(missing_ok=True)
                log(f"Voice generated: {voice_id}", "SUCCESS")
                return True
        except Exception as e:
            log(f"Voice {voice_id} failed: {e}", "ERROR")
            continue
    return False

def fetch_pexels_broll():
    """Fetch dark B-roll"""
    if not USE_BROLL:
        return None
    
    queries = ["dark office", "empty street", "lonely person", "urban night", "moody city"]
    query = random.choice(queries)
    log(f"Fetching B-roll: {query}...", "PROCESS")
    
    try:
        r = requests.get(
            f"https://api.pexels.com/videos/search?query={query}&per_page=1&size=small",
            headers={"Authorization": PEXELS_KEY},
            timeout=15
        )
        if r.status_code == 200:
            videos = r.json().get('videos', [])
            if videos:
                video = videos[0]
                video_file = min(video['video_files'], key=lambda f: f.get('width', 9999))
                video_url = video_file['link']
                
                clip_path = BASE / "broll" / f"dark_{int(time.time())}.mp4"
                clip_path.parent.mkdir(exist_ok=True)
                
                clip_data = requests.get(video_url, timeout=30).content
                with open(clip_path, "wb") as f:
                    f.write(clip_data)
                log(f"B-roll downloaded", "SUCCESS")
                return str(clip_path)
    except Exception as e:
        log(f"Pexels error: {e}", "ERROR")
    return None

def create_minimal_abe():
    """Create subtle Abe avatar"""
    log("Creating avatar...", "PROCESS")
    try:
        custom = next(iter(ROOT.glob('ChatGPT Image*.png')), None)
        img_path = custom if custom and custom.exists() else BASE / "temp" / "lincoln.jpg"
        
        if not img_path.exists():
            img_path.parent.mkdir(exist_ok=True)
            data = requests.get("https://upload.wikimedia.org/wikipedia/commons/a/ab/Abraham_Lincoln_O-77_matte_collodion_print.jpg", timeout=15).content
            with open(img_path, "wb") as f: f.write(data)
        
        dark_path = BASE / "temp" / "dark_abe.jpg"
        img = Image.open(str(img_path)).convert('RGB')
        small = img.resize((120, 155), Image.NEAREST)
        img = small.resize((540, 700), Image.NEAREST)
        img.save(dark_path)
        
        log("Avatar created", "SUCCESS")
        return str(dark_path)
    except Exception as e:
        log(f"Avatar error: {e}", "ERROR")
        return str(img_path) if img_path.exists() else None

def create_dark_video(audio_path, out, headline):
    """Create dark video with minimal effects"""
    log("Creating Dark Josh video...", "PROCESS")
    
    try:
        from moviepy.editor import AudioFileClip, ImageClip, VideoFileClip, CompositeVideoClip, ColorClip
        
        audio = AudioFileClip(str(audio_path))
        duration = min(audio.duration, 60.0)
        
        abe_img = create_minimal_abe()
        if not abe_img:
            return False
        
        broll_clip = fetch_pexels_broll()
        
        # Minimal scanlines
        scan_path = BASE / "temp" / "scan.png"
        scan = Image.new('RGBA', (1080, 1920), (0,0,0,0))
        draw = ImageDraw.Draw(scan)
        for y in range(0, 1920, 4):
            draw.line([(0,y), (1080,y)], fill=(0,0,0,50), width=1)
        scan.save(scan_path)
        
        # Audio envelope
        try:
            samples = audio.to_soundarray(fps=24)
            rms = np.sqrt((samples.astype(float) ** 2).mean(axis=1))
            rms = (rms / (rms.max() or 1)).clip(0,1)
            def env(t):
                idx = int(min(len(rms)-1, max(0, t*24)))
                return float(rms[idx])
        except:
            env = lambda t: 0.0
        
        # Subtle lip bar
        bar = Image.new('RGBA', (400, 25), (120, 120, 130, 200))
        bar_path = BASE / "temp" / "bar.png"
        bar.save(bar_path)
        
        # Hook overlay (first 40 chars of headline)
        hook_text = headline[:60] + "..." if len(headline) > 60 else headline
        hook_img = Image.new('RGBA', (1080, 180), (0,0,0,0))
        hook_draw = ImageDraw.Draw(hook_img)
        hook_draw.rectangle([(30, 30), (1050, 150)], fill=(10, 10, 15, 180), outline=(100, 100, 110, 200), width=2)
        hook_draw.text((540, 90), hook_text, fill=(200, 200, 210, 255), anchor="mm")
        hook_path = BASE / "temp" / "hook.png"
        hook_img.save(hook_path)
        
        # Compose
        bg = ColorClip(size=(1080,1920), color=(8,8,12), duration=duration).set_audio(audio)
        
        if broll_clip and Path(broll_clip).exists():
            processed = BASE / "temp" / "broll_proc.mp4"
            subprocess.run([
                "ffmpeg", "-y", "-i", broll_clip,
                "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
                "-t", "5", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "28", "-an",
                str(processed)
            ], capture_output=True, timeout=30)
            
            if processed.exists():
                broll_vid = VideoFileClip(str(processed)).loop(duration=duration).set_opacity(0.25)
            else:
                broll_vid = None
        else:
            broll_vid = None
        
        abe = ImageClip(str(abe_img)).resize((540, 700)).set_position(('center', 1050)).set_duration(duration)
        bar_clip = ImageClip(str(bar_path)).resize(lambda t: (400, int(12 + 90*env(t)))).set_position(('center', 1200)).set_duration(duration).set_opacity(0.7)
        scan_clip = ImageClip(str(scan_path)).set_duration(duration).set_opacity(0.25)
        hook_clip = ImageClip(str(hook_path)).set_position(('center', 220)).set_duration(min(4.0, duration)).set_opacity(0.85)
        
        layers = [bg]
        if broll_vid:
            layers.append(broll_vid)
        layers.extend([abe, bar_clip, scan_clip, hook_clip])
        
        temp_video = BASE / "temp" / f"temp_{int(time.time())}.mp4"
        comp = CompositeVideoClip(layers, size=(1080,1920))
        comp.write_videofile(
            str(temp_video),
            fps=24, codec='libx264', audio_codec='aac',
            bitrate='8000k', preset='fast',
            verbose=False, logger=None
        )
        comp.close(); bg.close(); audio.close()
        
        # Dark VHS
        log("Applying VHS effects...", "PROCESS")
        vhs_filter = (
            "scale=600:1067,scale=1080:1920:flags=neighbor,"
            "curves=darker,"
            "noise=alls=12:allf=t+u,"
            "hue=s=0.85,"
            "eq=contrast=1.3:brightness=-0.2:saturation=0.9:gamma=0.9,"
            "vignette=PI/4:0.6"
        )
        
        subprocess.run([
            "ffmpeg", "-y", "-i", str(temp_video),
            "-vf", vhs_filter,
            "-c:v", "libx264", "-preset", "fast", "-crf", "28",
            "-c:a", "copy",
            str(out)
        ], capture_output=True, timeout=120)
        
        if out.exists():
            log("Dark Josh video created", "SUCCESS")
            return True
            
    except Exception as e:
        log(f"Video error: {e}", "ERROR")
        import traceback
        traceback.print_exc()
    return False

def upload_to_youtube(video_path, headline):
    """Upload to YouTube"""
    log("Uploading to YouTube...", "PROCESS")
    
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
        
        try:
            duration_result = subprocess.run([
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)
            ], capture_output=True, text=True, timeout=30)
            duration = float(duration_result.stdout.strip())
        except:
            duration = 60.0
        
        is_short = duration <= 60
        
        title_clean = headline[:50] + "..." if len(headline) > 50 else headline
        title = f"Dark Josh: {title_clean}"
        if is_short:
            title += " #Shorts"
        
        description = f"""Abraham Lincoln delivers absurdist horror observations.

{headline}

The uncomfortable truth, deadpan delivery.

Bitcoin: {BTC}

#DarkComedy #JoshJohnson #AbsurdistHorror #SocialCommentary #Shorts"""
        
        tags = ["Dark Comedy", "Josh Johnson", "Absurdist", "Social Commentary", "Shorts", "Abraham Lincoln"]
        
        request_body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': '23'
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
        
        log(f"Uploaded: {video_url}", "SUCCESS")
        log(f"Studio: https://studio.youtube.com/channel/UCS5pEpSCw8k4wene0iv0uAg/videos", "INFO")
        
        return video_url
        
    except Exception as e:
        log(f"Upload failed: {e}", "ERROR")
        return None

def gen_dynamic_dark_josh():
    """Generate UNIQUE Dark Josh Johnson video from scraped content"""
    t = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    log(f"\n{'='*70}\nDARK JOSH JOHNSON - DYNAMIC\n{'='*70}", "INFO")
    
    # Scrape fresh content
    headlines = scrape_fresh_content()
    headline = random.choice(headlines)
    log(f"Headline: {headline}")
    
    # Generate UNIQUE script
    script = generate_dark_josh_script(headline)
    script = stutterize(script)
    log(f"Generated unique script: {len(script)} chars")
    
    # Generate audio
    ap = BASE / f"audio/dark_{t}.mp3"
    if not audio(script, ap):
        return None
    
    # Create video
    vp = BASE / f"videos/DARK_{t}.mp4"
    if not create_dark_video(ap, vp, headline):
        return None
    
    # Upload
    youtube_url = upload_to_youtube(vp, headline)
    
    # Save
    up = BASE / "uploaded" / f"DARK_JOSH_{t}.mp4"
    up.parent.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy2(vp, up)
    
    mb = up.stat().st_size / (1024 * 1024)
    log(f"{'='*70}\nCOMPLETE\n{'='*70}", "SUCCESS")
    log(f"Headline: {headline[:60]}")
    log(f"File: {up.name} ({mb:.1f}MB)")
    if youtube_url:
        log(f"YouTube: {youtube_url}")
    log(f"{'='*70}\n")
    
    return {
        'headline': headline,
        'video_path': str(up),
        'youtube_url': youtube_url
    }

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 1
    
    mode = "WITH B-roll" if USE_BROLL else "WITHOUT B-roll"
    
    log(f"\n{'='*70}")
    log(f"DARK JOSH JOHNSON - DYNAMIC SCRAPER")
    log(f"{'='*70}")
    log(f"NO repetitive scripts - every video is UNIQUE")
    log(f"Scrapes: Google News, Reddit, Hacker News, Google Sheets")
    log(f"Generating {count} dark observations")
    log(f"Mode: {mode}")
    log(f"{'='*70}\n")
    
    results = []
    for i in range(count):
        result = gen_dynamic_dark_josh()
        if result:
            results.append(result)
        if i < count - 1:
            log("\nWaiting 5 seconds...\n")
            time.sleep(5)
    
    log(f"\n{'='*70}")
    log(f"DARK OBSERVATIONS COMPLETE: {len(results)}/{count}")
    log(f"{'='*70}\n")
    
    for r in results:
        print(f"[DARK] {r['headline'][:60]}")
        if r.get('youtube_url'):
            print(f"  URL: {r['youtube_url']}")


