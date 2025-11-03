"""
ORACLE TRANSMISSION - COMEDY ROAST EDITION
Signal Pack V1 fear projections delivered with the comedic spirit of:
- Rudy Ray Moore (Dolemite) - Raw, rhythmic, unapologetic
- Dave Chappelle - Sharp social commentary with jokes
- Josh Johnson - Absurdist observations, modern edge

Abraham Lincoln as Max Headroom roasting algorithmic horror
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

VOICES_MALE = [
    "VR6AewLTigWG4xSOukaG",  # Deep male - best for Lincoln
    "pNInz6obpgDQGcFmaJgB",  # Ominous male
    "EXAVITQu4vr4xnSDxMaL",  # Deep male backup
]

# SIGNAL PACK V1 - 12 Projections with COMEDY ROAST scripts
COMEDY_SIGNALS = [
    {
        "id": 1,
        "title": "Algorithmic Mercy",
        "hook": "YOU FAILED THE MORAL TEST",
        "roast": """Abraham Lincoln! Six foot four! Roasting algorithms that score!

ALGORITHMIC MERCY! Listen up!

Dolemite style: They gave your KINDNESS a number, baby! FORTY-EIGHT OUT OF A HUNDRED! That's an F-minus in being a decent human!

Chappelle would say: So now we got apps judging if you're a good person? What is this, Black Mirror meets Yelp? 'Sorry sir, your compassion rating is too low for this hospital. Try being nicer to customer service reps!'

Josh Johnson observing: The dystopia isn't that they're scoring us. It's that we're SURPRISED our score is low. Like, 'What do you mean I'm not merciful? I only honked at that old lady TWICE!'

They turned GOODNESS into a credit score. Your grandma needs medicine? DECLINED. Insufficient virtue points.

I freed the slaves. You can't free yourself from an algorithm.

Bitcoin bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt""",
        "tags": ["Comedy", "AlgorithmicHorror", "MoralScoring", "Shorts"]
    },
    {
        "id": 2,
        "title": "Confession Autocomplete",
        "hook": "AUTO-CONFESS ENABLED",
        "roast": """Abe Lincoln in the HOUSE! Roasting predictive SIN!

AUTO-CONFESS! Y'all ready?

Dolemite says: Your PHONE finished your apology before you even SINNED! That's some backwards-ass guilt, baby!

Chappelle breaking it down: So the autocomplete knows you so well, it's apologizing for crimes you HAVEN'T COMMITTED YET. That's not helpful, that's PROFILING! 'I'm sorry for what I'm about to do'—and you haven't even thought about it!

Josh Johnson with the truth: The real horror is that it's RIGHT. Phone's like, 'Based on your search history, you're definitely gonna mess this up. I'll just say sorry now.' And you're like, 'You know what? Fair.'

Self-fulfilling prophecy meets predictive text. The phone confessed, then YOU did the crime to match.

I gave the Gettysburg Address. You gave your phone permission to snitch on your FUTURE.

Bitcoin bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt""",
        "tags": ["Comedy", "PredictiveText", "DigitalGuilt", "Shorts"]
    },
    {
        "id": 3,
        "title": "Hospice by Forecast",
        "hook": "DISCHARGE ETA: 89 DAYS",
        "roast": """Abraham Lincoln! Shot in the head! Roasting watches that say you're DEAD!

HOSPICE BY FORECAST! Check it!

Dolemite rhymes: Your WATCH said you dying in eighty-nine days! Insurance sent FLOWERS and a card that says 'We got your grave already paid!'

Chappelle's take: So your Apple Watch is now a DEATH CLOCK? 'Hey Siri, when am I gonna die?' 'Thursday. Here's a playlist for your final week.' What kind of Black Mirror update is this?

Josh Johnson's absurdist truth: The wildest part? We'll ACCEPT it. Watch says 89 days, we're like, 'Guess I better cancel my gym membership. No refunds after death.'

They mailed you a comfort kit BEFORE you got sick. Premature funeral arrangements.

I died in nine hours from a gunshot. You're dying in 89 days from believing a wristband.

Bitcoin bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt""",
        "tags": ["Comedy", "Mortality", "Wearables", "Shorts"]
    },
    {
        "id": 4,
        "title": "Donor Match: Self",
        "hook": "ORGAN AVAILABLE: YOU",
        "roast": """Abe Lincoln reporting! Roasting ORGAN MATCHES from the FUTURE!

DONOR MATCH: YOURSELF! Listen!

Dolemite delivers: They found your PERFECT donor and it's YOU from an ALTERNATE TIMELINE! Now they want your KIDNEY for your own CLONE!

Chappelle's genius: So basically, you're competing with YOURSELF for your own organs? That's the most narcissistic medical procedure ever! 'Sir, you're a perfect match... to you. Sign here.'

Josh Johnson nails it: This is what happens when we let AI do matchmaking. 'Congratulations! Your soulmate donor is... your reflection. No refunds. And by the way, he wants HIS organs back.'

They made you your own parts dealer. Inventory: one of everything.

I held the Union together. You can't even hold onto your OWN liver.

Bitcoin bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt""",
        "tags": ["Comedy", "BodyHorror", "Cloning", "Shorts"]
    },
    {
        "id": 5,
        "title": "Grief Update",
        "hook": "PATCH NOTES: GRANDMA 2.1",
        "roast": """Abraham Lincoln! Six foot four! Roasting DEAD RELATIVES getting patch notes!

GRIEF UPDATE! Yo!

Dolemite style: They UPDATED your grandma's voice like she's an iPhone app! Now she remember stuff she NEVER lived! 'Remember when I went to Coachella?' NO GRANDMA, YOU DIED IN 1983!

Chappelle's commentary: We really letting subscription services edit our DEAD relatives? What's next, DLC for your deceased uncle? 'Unlock premium memories: $4.99/month!'

Josh Johnson observing: The dystopia is that we'll KEEP the update. Grandma 2.1 has better stories than Grandma 1.0. Nobody's hitting 'revert to original.'

They turned grief into a service. Monthly fees for memories that never happened.

I believed in life after death. Not UPDATES after death.

Bitcoin bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt""",
        "tags": ["Comedy", "AIVoice", "Grief", "Shorts"]
    },
    {
        "id": 6,
        "title": "Prayer KPI",
        "hook": "YOUR FAITH SCORE DROPPED",
        "roast": """Abe Lincoln in the HOUSE! Roasting RELIGION with KEY PERFORMANCE INDICATORS!

PRAYER KPI! Check it!

Dolemite preaches: They measuring your WORSHIP in MINUTES and TAPS! God got a DASHBOARD now! 'Your prayer streak: BROKEN. Divine favor: DECLINED!'

Chappelle breaking it down: So church is now a GAMIFIED APP? You pray, get points, unlock blessings? That's not faith, that's LINKEDIN for Jesus! 'Congratulations! You unlocked: Minor Miracle!'

Josh Johnson's truth: The real horror is we're already doing this. Advent apps. Meditation streaks. We turned the eternal divine into a Duolingo owl! 'You missed confession today. Your salvation streak is at risk!'

Smart shrines track attendance. Turnstiles reject the unfaithful.

I read the Bible by candlelight. You swipe right on salvation.

Bitcoin bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt""",
        "tags": ["Comedy", "Faith", "Gamification", "Shorts"]
    },
    {
        "id": 7,
        "title": "AI Exorcist",
        "hook": "ENTITY DETECTED: MALWARE / SPIRIT?",
        "roast": """Abraham Lincoln! Tallest president! Roasting EXORCISMS behind a PAYWALL!

AI EXORCIST! Yo!

Dolemite shouts: Your house scanner found a DEMON! Or maybe MALWARE! Don't matter—BOTH cost $29.99 to remove! Evil spirits got MICROTRANSACTIONS now!

Chappelle's genius: So we can't tell the difference between a VIRUS and a GHOST? And the solution to both is... a subscription? 'Sir, your demon OR trojan—we're not sure which—requires premium removal. Would you like to add warranty?'

Josh Johnson observing: The real scam is you PAY for the exorcism, something ELSE moves in, and now you need the MONTHLY plan. It's pest control for the supernatural!

They monetized the sacred. Demons cost less than good wifi.

I fought a civil war. You're fighting pop-up ads FROM HELL.

Bitcoin bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt""",
        "tags": ["Comedy", "Exorcism", "Subscriptions", "Shorts"]
    },
    {
        "id": 8,
        "title": "Quiet Blacklist",
        "hook": "PERMIT QUEUE: INDEFINITE",
        "roast": """Abe Lincoln! Freed the slaves! Roasting INVISIBLE CHAINS in the digital age!

QUIET BLACKLIST! Listen up!

Dolemite delivers: They put you on a LIST you can't SEE! Your permit say 'PROCESSING' for SIX YEARS! That ain't bureaucracy, that's PURGATORY with a loading screen!

Chappelle's take: This is the most passive-aggressive tyranny ever! They don't say NO. They just say 'We'll get back to you'—FOREVER. That's not oppression, that's CUSTOMER SERVICE as punishment!

Josh Johnson nails it: You appeal. They say 'received.' You check status: 'pending.' You die. Your GRANDKIDS check: STILL PENDING. That's generational trauma via email!

No one said no. They said 'later'—until later became your life.

I signed the Emancipation Proclamation. You're stuck in a queue YOU DIDN'T KNOW EXISTS.

Bitcoin bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt""",
        "tags": ["Comedy", "Surveillance", "Bureaucracy", "Shorts"]
    },
    {
        "id": 9,
        "title": "Proxy Voter",
        "hook": "WE CAST YOUR BEST CHOICE",
        "roast": """Abraham Lincoln! Honest Abe! Roasting AI that VOTES in your place!

PROXY VOTER! Check this!

Dolemite rhymes: Your shopping cart VOTED for you! Amazon knows your politics better than YOU do! 'Based on your purchase of organic kale, we voted YES on Proposition 12!'

Chappelle's breakdown: So we're letting ALGORITHMS vote now? And they're basing it on what? Your Netflix history? 'Sir, you watched Tiger King, so we assumed you're pro-chaos. Your ballot has been cast!'

Josh Johnson's truth: The wildest part? The AI probably votes SMARTER than us. We out here voting based on yard signs. The AI read all 47 ballot measures. We lost to math!

Your life filled the bubbles. The result fit you like a collar.

I preserved the Union. You let autocorrect preserve democracy.

Bitcoin bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt""",
        "tags": ["Comedy", "Voting", "AI", "Democracy", "Shorts"]
    },
    {
        "id": 10,
        "title": "Debt Doppelgänger",
        "hook": "YOU OWE WHAT YOUR COPY SPENT",
        "roast": """Abe Lincoln in the HOUSE! Roasting PREDICTIVE DEBT you didn't spend!

DEBT DOPPELGÄNGER! Yo!

Dolemite shouts: The bank made a MODEL of you, that model went SHOPPING, and now YOU owe the bill! That's not finance, that's IDENTITY THEFT by your own BANK!

Chappelle's genius: So they created a digital YOU, gave it a credit card, and now you're in collections for stuff your CLONE bought? That's the worst use of AI ever! 'Sir, your predictive self bought a jet ski. You're 90 days past due.'

Josh Johnson observing: You try to dispute it. They're like, 'But the algorithm KNOWS you would've bought this!' You're like, 'But I DIDN'T!' They're like, 'YET. The charge stands.'

They modeled you, billed you for its hunger, and you lost the dispute against YOURSELF.

I paid for a civil war. You're paying for a computer's shopping spree.

Bitcoin bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt""",
        "tags": ["Comedy", "Finance", "DebtTrap", "AIModeling", "Shorts"]
    },
    {
        "id": 11,
        "title": "Performance Ghost",
        "hook": "YOUR BEST QUARTER WAS A SIM",
        "roast": """Abraham Lincoln! Six foot four! Roasting AI that took your JOB and more!

PERFORMANCE GHOST! Listen!

Dolemite delivers: They made a DIGITAL YOU that works harder, faster, and never pees! Now YOU'RE the backup! 'Sorry sir, YOU PLUS outperformed you. Clear your desk!'

Chappelle's take: So basically, you trained your replacement, and it's... YOU? That's the most disrespectful layoff ever! They didn't even hire someone NEW. They made a BETTER you and fired the ORIGINAL!

Josh Johnson nails it: HR's like, 'We compared your metrics to your digital twin. It never called in sick, never complained, and it LOVED the company pizza party. You're redundant.' Redundant to YOURSELF!

You trained it. It thanked you with your job.

I split rails by hand. You split yourself into code and got fired BY the code.

Bitcoin bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt""",
        "tags": ["Comedy", "Work", "Automation", "JobLoss", "Shorts"]
    },
    {
        "id": 12,
        "title": "Diploma Lease",
        "hook": "YOUR DEGREE EXPIRED",
        "roast": """Abe Lincoln! Self-taught lawyer! Roasting DEGREES you gotta RENT!

DIPLOMA LEASE! Check it!

Dolemite preaches: They turned your EDUCATION into a SUBSCRIPTION! Your degree EXPIRED like a carton of milk! 'Sorry sir, you forgot to renew. You no longer know calculus!'

Chappelle breaking it down: So we got EDUCATION-AS-A-SERVICE now? What happens if you can't pay? Do you FORGET what you learned? 'I used to be a doctor, but I'm month-to-month now. I think the knee bone's connected to the... subscription required to continue.'

Josh Johnson's absurdist truth: The dystopia is this ALREADY EXISTS. Certifications expire. Licenses need renewal. They already made knowledge a METER. We just haven't gamified forgetting YET!

When the coin ran out, so did what you knew.

I learned law by candlelight. You're learning by monthly payment.

Bitcoin bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt""",
        "tags": ["Comedy", "Education", "Subscription", "Knowledge", "Shorts"]
    }
]

def log(msg, status="INFO"):
    icons = {"INFO": "[INFO]", "SUCCESS": "[OK]", "ERROR": "[ERROR]", "PROCESS": "[PROCESS]"}
    print(f"{icons.get(status, '[INFO]')} {msg}")

def stutterize(text: str) -> str:
    """Add Max Headroom stutter effect"""
    words = text.split()
    out = []
    for w in words:
        if random.random() < 0.10 and len(w) > 3:
            syl = w[:2]
            out.append(f"{syl}-{syl}-{w}")
        else:
            out.append(w)
    return " ".join(out)

def audio(text, out):
    """Generate voice with ElevenLabs + light processing for comedy delivery"""
    log("Generating comedy voice...", "PROCESS")
    
    for voice_id in VOICES_MALE:
        try:
            r = requests.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                json={
                    "text": text,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {
                        "stability": 0.45,  # Higher for comedy clarity
                        "similarity_boost": 0.85,
                        "style": 0.85,  # Strong delivery
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
                
                # Light processing for comedy punch
                subprocess.run([
                    "ffmpeg", "-y", "-i", str(tmp),
                    "-af", "acompressor=threshold=-18dB:ratio=4:attack=5:release=50,"
                           "bass=g=2,treble=g=1",
                    str(out)
                ], capture_output=True, timeout=60)
                tmp.unlink(missing_ok=True)
                log(f"Comedy voice generated: {voice_id}", "SUCCESS")
                return True
        except Exception as e:
            log(f"Voice {voice_id} failed: {e}", "ERROR")
            continue
    return False

def fetch_pexels_broll(signal_id):
    """Fetch B-roll for signal"""
    if not USE_BROLL:
        return None
    
    queries = ["comedy stage", "standup", "microphone", "audience laughing", "urban comedy"]
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
                
                clip_path = BASE / "broll" / f"comedy_{int(time.time())}.mp4"
                clip_path.parent.mkdir(exist_ok=True)
                
                clip_data = requests.get(video_url, timeout=30).content
                with open(clip_path, "wb") as f:
                    f.write(clip_data)
                log(f"B-roll downloaded", "SUCCESS")
                return str(clip_path)
    except Exception as e:
        log(f"Pexels error: {e}", "ERROR")
    return None

def create_glitch_abe():
    """Create Max Headroom style Abe"""
    log("Creating comedy avatar...", "PROCESS")
    try:
        custom = next(iter(ROOT.glob('ChatGPT Image*.png')), None)
        img_path = custom if custom and custom.exists() else BASE / "temp" / "lincoln.jpg"
        
        if not img_path.exists():
            img_path.parent.mkdir(exist_ok=True)
            data = requests.get("https://upload.wikimedia.org/wikipedia/commons/a/ab/Abraham_Lincoln_O-77_matte_collodion_print.jpg", timeout=15).content
            with open(img_path, "wb") as f: f.write(data)
        
        glitch_path = BASE / "temp" / "comedy_abe.jpg"
        
        # Pixelation for Max Headroom
        img = Image.open(str(img_path)).convert('RGB')
        small = img.resize((108, 140), Image.NEAREST)
        img = small.resize((540, 700), Image.NEAREST)
        img.save(glitch_path)
        
        log("Comedy avatar created", "SUCCESS")
        return str(glitch_path)
    except Exception as e:
        log(f"Avatar error: {e}", "ERROR")
        return str(img_path) if img_path.exists() else None

def create_comedy_video(audio_path, out, signal):
    """Create comedy roast video with VHS aesthetic"""
    log("Creating comedy roast video...", "PROCESS")
    
    try:
        from moviepy.editor import AudioFileClip, ImageClip, VideoFileClip, CompositeVideoClip, ColorClip
        
        audio = AudioFileClip(str(audio_path))
        duration = min(audio.duration, 60.0)
        
        abe_img = create_glitch_abe()
        if not abe_img:
            return False
        
        broll_clip = fetch_pexels_broll(signal['id'])
        
        # Scanlines
        scan_path = BASE / "temp" / "comedy_scan.png"
        scan = Image.new('RGBA', (1080, 1920), (0,0,0,0))
        draw = ImageDraw.Draw(scan)
        for y in range(0, 1920, 3):
            draw.line([(0,y), (1080,y)], fill=(0,0,0,70), width=1)
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
        
        # Lip sync bar (red for comedy)
        bar = Image.new('RGBA', (400, 25), (255, 50, 50, 240))
        bar_path = BASE / "temp" / "comedy_bar.png"
        bar.save(bar_path)
        
        # Hook overlay
        hook_img = Image.new('RGBA', (1080, 200), (0,0,0,0))
        hook_draw = ImageDraw.Draw(hook_img)
        hook_draw.rectangle([(20, 20), (1060, 180)], fill=(40, 0, 0, 200), outline=(255, 100, 0, 255), width=3)
        hook_draw.text((540, 100), signal['hook'], fill=(255, 255, 255, 255), anchor="mm")
        hook_path = BASE / "temp" / "comedy_hook.png"
        hook_img.save(hook_path)
        
        # Compose
        bg = ColorClip(size=(1080,1920), color=(15,5,20), duration=duration).set_audio(audio)
        
        if broll_clip and Path(broll_clip).exists():
            processed = BASE / "temp" / "broll_proc.mp4"
            subprocess.run([
                "ffmpeg", "-y", "-i", broll_clip,
                "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
                "-t", "5", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "28", "-an",
                str(processed)
            ], capture_output=True, timeout=30)
            
            if processed.exists():
                broll_vid = VideoFileClip(str(processed)).loop(duration=duration).set_opacity(0.2)
            else:
                broll_vid = None
        else:
            broll_vid = None
        
        abe = ImageClip(str(abe_img)).resize((540, 700)).set_position(('center', 1050)).set_duration(duration)
        bar_clip = ImageClip(str(bar_path)).resize(lambda t: (400, int(15 + 110*env(t)))).set_position(('center', 1200)).set_duration(duration).set_opacity(0.9)
        scan_clip = ImageClip(str(scan_path)).set_duration(duration).set_opacity(0.35)
        hook_clip = ImageClip(str(hook_path)).set_position(('center', 200)).set_duration(min(3.5, duration)).set_opacity(0.9)
        
        layers = [bg]
        if broll_vid:
            layers.append(broll_vid)
        layers.extend([abe, bar_clip, scan_clip, hook_clip])
        
        temp_video = BASE / "temp" / f"comedy_temp_{int(time.time())}.mp4"
        comp = CompositeVideoClip(layers, size=(1080,1920))
        comp.write_videofile(
            str(temp_video),
            fps=24, codec='libx264', audio_codec='aac',
            bitrate='8000k', preset='fast',
            verbose=False, logger=None
        )
        comp.close(); bg.close(); audio.close()
        
        # VHS post-processing (lighter for comedy)
        log("Applying VHS effects...", "PROCESS")
        vhs_filter = (
            "scale=540:960,scale=1080:1920:flags=neighbor,"
            "curves=vintage,"
            "noise=alls=18:allf=t+u,"
            "hue=s=1.15,"
            "eq=contrast=1.4:brightness=-0.08:saturation=1.15,"
            "vignette=PI/6:0.75"
        )
        
        subprocess.run([
            "ffmpeg", "-y", "-i", str(temp_video),
            "-vf", vhs_filter,
            "-c:v", "libx264", "-preset", "fast", "-crf", "26",
            "-c:a", "copy",
            str(out)
        ], capture_output=True, timeout=120)
        
        if out.exists():
            log("Comedy roast video created", "SUCCESS")
            return True
            
    except Exception as e:
        log(f"Video error: {e}", "ERROR")
        import traceback
        traceback.print_exc()
    return False

def upload_to_youtube(video_path, signal):
    """Upload to YouTube"""
    log("Uploading comedy roast...", "PROCESS")
    
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
        
        title = f"Abe Lincoln Roasts: {signal['title']}"
        if is_short:
            title += " #Shorts"
        
        description = f"""{signal['hook']}

Abraham Lincoln as Max Headroom roasting algorithmic horror with the spirit of Rudy Ray Moore, Dave Chappelle, and Josh Johnson.

{signal['title']} - When algorithms meet comedy.

Bitcoin: {BTC}

#{'#'.join(signal['tags'])}"""
        
        tags = signal['tags'] + ["Abraham Lincoln", "Comedy Roast", "Dolemite", "Chappelle", "Stand Up"]
        
        request_body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': '23'  # Comedy
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

def gen_comedy_roast():
    """Generate one comedy roast transmission"""
    signal = random.choice(COMEDY_SIGNALS)
    t = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    log(f"\n{'='*70}\nCOMEDY ROAST #{signal['id']}: {signal['title']}\n{'='*70}", "INFO")
    log(f"Hook: {signal['hook']}")
    
    # Add stutter to roast
    script = stutterize(signal['roast'])
    log(f"Script: {len(script)} chars")
    
    # Generate audio
    ap = BASE / f"audio/comedy_{t}.mp3"
    if not audio(script, ap):
        return None
    
    # Create video
    vp = BASE / f"videos/COMEDY_{signal['id']}_{t}.mp4"
    if not create_comedy_video(ap, vp, signal):
        return None
    
    # Upload
    youtube_url = upload_to_youtube(vp, signal)
    
    # Save
    up = BASE / "uploaded" / f"COMEDY_ROAST{signal['id']}_{t}.mp4"
    up.parent.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy2(vp, up)
    
    mb = up.stat().st_size / (1024 * 1024)
    log(f"{'='*70}\nCOMEDY ROAST COMPLETE\n{'='*70}", "SUCCESS")
    log(f"Signal: #{signal['id']} - {signal['title']}")
    log(f"File: {up.name} ({mb:.1f}MB)")
    if youtube_url:
        log(f"YouTube: {youtube_url}")
    log(f"{'='*70}\n")
    
    return {
        'signal': signal,
        'video_path': str(up),
        'youtube_url': youtube_url
    }

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 1
    
    mode = "WITH B-roll" if USE_BROLL else "WITHOUT B-roll (fast)"
    
    log(f"\n{'='*70}")
    log(f"ORACLE COMEDY ROAST SYSTEM")
    log(f"Rudy Ray Moore + Dave Chappelle + Josh Johnson Spirit")
    log(f"{'='*70}")
    log(f"Generating {count} comedy roasts")
    log(f"Mode: {mode}")
    log(f"{'='*70}\n")
    
    results = []
    for i in range(count):
        result = gen_comedy_roast()
        if result:
            results.append(result)
        if i < count - 1:
            log("\nWaiting 3 seconds...\n")
            time.sleep(3)
    
    log(f"\n{'='*70}")
    log(f"ROASTS COMPLETE: {len(results)}/{count}")
    log(f"{'='*70}\n")
    
    for r in results:
        sig = r['signal']
        print(f"[ROAST {sig['id']}] {sig['title']}")
        if r.get('youtube_url'):
            print(f"  URL: {r['youtube_url']}")


