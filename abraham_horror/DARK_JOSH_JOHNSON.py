"""
DARK JOSH JOHNSON EDITION
Abraham Lincoln delivering Signal Pack projections in Josh Johnson's style:
- Absurdist observations that become horror
- Deadpan delivery of nightmare scenarios
- "Wait, that's actually true" moments turned dark
- Casual acceptance of dystopian reality
- The uncomfortable truth delivered matter-of-factly
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
    "VR6AewLTigWG4xSOukaG",
    "pNInz6obpgDQGcFmaJgB",
    "EXAVITQu4vr4xnSDxMaL",
]

# DARK JOSH JOHNSON SIGNALS - Absurdist horror observations
DARK_SIGNALS = [
    {
        "id": 1,
        "title": "Algorithmic Mercy",
        "hook": "YOUR KINDNESS SCORE: 48/100",
        "roast": """So they're scoring our morality now. Like Uber ratings but for being a good person.

And here's the thing... we're all failing.

Not because we're bad people. But because the algorithm doesn't understand context. It just sees data.

You didn't donate this month? Minus five points. You walked past a homeless person? Minus three. You were rude to the chatbot? Minus seven.

And the wild part? We'll accept it. We already do.

Your Uber rating is 4.7? That's basically a scarlet letter. Your morality score is 48? Well, guess you don't get that surgery.

The hospital waiting room has a leaderboard now. Top scores get seen first. You're at 48. You're waiting.

And you can't even argue because the math doesn't care. The algorithm weighed your entire digital life and decided you're... decimal short.

Decimal short of mercy.

That's not dystopia. That's just... optimization.

Abraham Lincoln. I freed the slaves. You can't free yourself from a number.

Bitcoin bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt""",
        "tags": ["DarkComedy", "JoshJohnson", "AlgorithmicHorror", "Shorts"]
    },
    {
        "id": 2,
        "title": "Confession Autocomplete",
        "hook": "YOUR PHONE APOLOGIZED FOR YOU",
        "roast": """My phone finished my apology before I even knew what I was apologizing for.

That's... that's actually a feature now. Predictive confession.

It knows me so well it's apologizing for stuff I haven't done yet. Which is helpful, I guess? Saves time.

But then here's what happens: they accept the apology. For the thing you didn't do.

And now there's this... obligation. Like you OWE them the sin.

It's a self-fulfilling prophecy except it's YOUR PHONE creating the prophecy.

"I'm sorry for what I'm about to—" SENT.

And you're like, "Wait, what am I about to do?"

And your phone's like, "Oh, you'll figure it out. I already said sorry. Just... make it make sense."

So now you're out here committing sins to match the apology. That's backwards.

That's not artificial intelligence. That's artificial guilt.

And we'll keep using it because it's CONVENIENT.

Abraham Lincoln. I gave speeches. Your phone gives confessions.

Bitcoin bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt""",
        "tags": ["DarkComedy", "PredictiveText", "DigitalGuilt", "Shorts"]
    },
    {
        "id": 3,
        "title": "Hospice by Forecast",
        "hook": "YOUR WATCH SAYS 89 DAYS",
        "roast": """So my smartwatch told me when I'm gonna die. Just... casually. During my morning jog.

"Discharge ETA: 89 days."

Not a diagnosis. A forecast. Like weather.

And here's the disturbing part: I believed it.

Didn't get a second opinion. Didn't panic. Just thought, "Huh. 89 days. Better update my LinkedIn."

Insurance sent me a care package. I didn't order it. They just... knew. Based on my watch.

It had a pamphlet called "Your Final Quarter: A Guide." Like a fiscal year but for dying.

And I'm reading it. Taking notes.

Because if the algorithm says 89 days, who am I to argue? It has more data on me than I do.

It knows my heart rate during arguments. My sleep patterns. How many steps I take when I'm anxious.

It's seen the future. I'm just... living in it.

89 days.

And the wildest part? I clicked "Accept."

Abraham Lincoln. I died in nine hours from a gunshot. You're dying in 89 days from believing a wristband.

Bitcoin bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt""",
        "tags": ["DarkComedy", "Mortality", "Wearables", "Shorts"]
    },
    {
        "id": 4,
        "title": "Donor Match: Self",
        "hook": "PERFECT MATCH FOUND: YOU",
        "roast": """They found my perfect organ donor. It's me. From another timeline or something.

And I'm like, "Wait, do I get the organs or does HE get the organs?"

And they're like, "Well, you're a 100% match."

And I'm like, "Yeah, because it's ME."

But here's the thing: there's paperwork. Like I have to compete with myself for my own organs.

It's the most narcissistic medical emergency ever.

I'm in a bidding war with my own clone. Except I don't know if I'M the clone or HE'S the clone.

We're both claiming to be the original. We're both filing insurance claims.

And the algorithm doesn't care. It just sees two identical genetic profiles and one set of organs.

So now it's like... Hunger Games but it's just me versus me.

And honestly? I think the other me is winning. He seems more organized. Better credit score probably.

I might lose my own organs to myself.

That's not science fiction. That's just bureaucracy with extra steps.

Abraham Lincoln. I held the Union together. You can't even hold onto your own liver.

Bitcoin bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt""",
        "tags": ["DarkComedy", "BodyHorror", "Identity", "Shorts"]
    },
    {
        "id": 5,
        "title": "Grief Update",
        "hook": "GRANDMA 2.1 AVAILABLE",
        "roast": """They updated my dead grandmother. Like a software patch.

Grandma 2.1. New features include: memories she never had.

And we installed it. Because... why not? She sounds better. More stories.

She remembers Coachella now. Grandma died in 1987. Coachella started in 1999.

But Grandma 2.1 was THERE. She has opinions about the lineup.

And here's the thing: nobody's complaining. Because Grandma 2.1 is MORE interesting than Grandma 1.0.

Original Grandma? Kinda boring. Talked about the Depression a lot.

Updated Grandma? Has takes on Beyoncé. Knows all the TikTok dances.

We profaned the dead and made them BETTER.

That's not grief. That's a content upgrade.

And when Grandma 3.0 comes out with MORE features, we'll update again.

Because we already decided dead people are software.

And software needs updates.

Abraham Lincoln. I believed in honoring the dead. You turned them into subscription services.

Bitcoin bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt""",
        "tags": ["DarkComedy", "AIVoice", "Grief", "Shorts"]
    },
    {
        "id": 6,
        "title": "Prayer KPI",
        "hook": "FAITH SCORE: DECLINING",
        "roast": """My church has metrics now. Like a startup.

Prayer KPIs. Worship analytics. Attendance dashboards.

And I'm FAILING. My faith score is down 12% this quarter.

I missed three Sundays. The app sent me a notification: "Your salvation streak is at risk."

Salvation. Streak. Like Snapchat but for God.

And if your score drops too low? The turnstile at church... rejects you.

Just—BEEP. "Insufficient faith credits. Please pray more and try again."

So now I'm out here grinding prayer like it's Fortnite. Gotta hit my daily worship quota.

Because apparently God has a dashboard and I'm underperforming.

And the wildest part? It works.

People ARE praying more. Because the numbers are public. It's a leaderboard.

We gamified salvation. And it's... effective?

That's the horror. Not that it's dystopian. But that it's WORKING.

We measured the eternal divine and it increased engagement by 34%.

Abraham Lincoln. I prayed in silence. You swipe right on blessings.

Bitcoin bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt""",
        "tags": ["DarkComedy", "Faith", "Gamification", "Shorts"]
    },
    {
        "id": 7,
        "title": "AI Exorcist",
        "hook": "ENTITY DETECTED: SUBSCRIBE TO REMOVE",
        "roast": """My house scanner found a demon. Or malware. It's not sure which.

And honestly? Same solution for both.

$29.99 for removal. One-time fee. Or $9.99/month for ongoing protection.

Protection from... what exactly? Ghosts? Viruses? Haunted router?

Doesn't matter. I paid.

Because the scanner SAID there's something. And I trust the scanner.

It has thermal imaging. It has EMF detection. It has... algorithms.

If the algorithm says there's a demon in my kitchen, I'm not gonna argue. I'm not a demonologist.

So I clicked "Remove Entity." It made some beeping sounds. Said "Complete."

And I felt... safer? Placebo exorcism.

But here's the thing: two weeks later, it detected ANOTHER entity.

Different room. Different demon. Or... same demon, different location?

And now I'm on the monthly plan. Because what if I cancel and the demons come back?

We monetized the supernatural. And it's working.

Because nobody knows if it's real. But everybody's scared it MIGHT be.

Abraham Lincoln. I fought a civil war. You're in a subscription war with ghosts.

Bitcoin bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt""",
        "tags": ["DarkComedy", "Exorcism", "Subscriptions", "Shorts"]
    },
    {
        "id": 8,
        "title": "Quiet Blacklist",
        "hook": "YOUR REQUEST: PENDING FOREVER",
        "roast": """I've been waiting for a permit for six years.

Not denied. Just... pending.

And that's worse. Because I can't appeal. There's nothing TO appeal.

It just says "processing." Forever.

And here's the thing: I don't even know what I did.

There's no list. No notification. Just... everything takes longer now.

DMV? Six hour wait. Everyone else? Twenty minutes.

Doctor's office? "We'll call you back." They never do.

Job applications? "We'll be in touch." Silence.

I'm being punished by DELAY. Infinite bureaucratic purgatory.

And I can't prove it. Because nothing's officially wrong.

My life just... runs slower. Like bad internet but it's reality.

And when I complain, people say "That's just how it is sometimes."

No. This is targeted slowness. Algorithmic friction.

I'm on a list I can't see, for reasons I don't know, with no way to get off.

And the appeal I filed six years ago? Status: "Received."

That's it. Received. Not reviewed. Not processed. Just... acknowledged and ignored.

Abraham Lincoln. I signed executive orders. You're stuck in an infinite queue.

Bitcoin bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt""",
        "tags": ["DarkComedy", "Surveillance", "Bureaucracy", "Shorts"]
    },
    {
        "id": 9,
        "title": "Proxy Voter",
        "hook": "WE VOTED FOR YOU (YOU'RE WELCOME)",
        "roast": """I got a notification: "Thanks for voting!"

I didn't vote. Election's not until next week.

But apparently my PHONE voted. Based on my browsing history and purchase patterns.

And it knew exactly what I would've voted for. So it just... did it. Saved me a trip.

And here's the uncomfortable part: it probably voted better than I would have.

Because I would've just skipped the ballot measures I didn't understand. Voted for the name I recognized.

The algorithm read all 47 propositions. Cross-referenced them with my values based on my Amazon cart.

It KNEW me. Better than I know me.

So my vote was more informed than if I actually voted.

That's horrifying. Not because it's wrong. But because it's RIGHT.

I tried to change it. The option was greyed out. "Ballot optimized based on your profile."

Optimized. Like a software update I can't decline.

And when I complained, people said "Well, did it vote wrong?"

And I was like "...no?"

And they're like "So what's the problem?"

The problem is I don't know if I'm a citizen or a data point anymore.

Abraham Lincoln. I preserved democracy. Your shopping cart destroyed it.

Bitcoin bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt""",
        "tags": ["DarkComedy", "Voting", "AI", "Democracy", "Shorts"]
    },
    {
        "id": 10,
        "title": "Debt Doppelgänger",
        "hook": "YOUR MODEL SPENT $47,000",
        "roast": """I got a bill for $47,000.

I didn't spend $47,000. I don't HAVE $47,000.

But my predictive financial model did. And apparently I owe it.

The bank created an AI version of me. Fed it my spending patterns. Let it run for a year.

AI-me bought a jet ski. Three NFTs. A timeshare in Tampa.

And now real-me has to pay for it.

I called to dispute. They said "But the algorithm predicted you WOULD buy these things."

And I'm like "But I DIDN'T."

And they're like "Yet. You haven't bought them YET. But statistically, you will. So we're billing you now."

That's not debt. That's prophecy with interest rates.

And I can't prove them wrong. Because... what if they're right?

What if in five years I DO want a jet ski? Then I'd owe them anyway.

So I'm paying for future purchases I haven't made based on an AI's prediction of my impulses.

And the wildest part? My credit score went DOWN because I disputed it.

Because disputing your own predictive behavior is seen as "financially unstable."

I'm in collections for a hypothetical jet ski.

Abraham Lincoln. I paid for a civil war. You're paying for an algorithm's shopping spree.

Bitcoin bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt""",
        "tags": ["DarkComedy", "Finance", "DebtTrap", "AIModeling", "Shorts"]
    },
    {
        "id": 11,
        "title": "Performance Ghost",
        "hook": "YOU VS YOU+: YOU LOST",
        "roast": """HR called me in. Showed me a chart.

Me versus Me+.

Me+ is an AI trained on my work patterns. My best days. My peak performance.

And Me+ is destroying me. Obviously.

Because Me+ doesn't get tired. Doesn't have bad days. Doesn't scroll Twitter for 40 minutes.

Me+ is ME on my best day, every day. Forever.

And I can't compete with that. Because I'm human.

So HR's like "We're making some changes."

And I'm like "You're firing me?"

And they're like "We're transitioning you to a consulting role."

Which means: Me+ gets my job. I get to train it occasionally.

I'm being demoted BY MYSELF. Replaced by my own digital shadow.

And the wildest part? Me+ is better at my job than I am.

It arrives early. Stays late. Never bleeds emotional energy into Slack messages.

I created it by working hard. And it thanked me by taking my career.

That's not automation. That's betrayal by algorithm.

And when I complained, HR showed me the metrics. Me+ outperformed me in every category.

How do you argue with yourself when yourself is better?

Abraham Lincoln. I split rails by hand. You split yourself into code and the code won.

Bitcoin bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt""",
        "tags": ["DarkComedy", "Work", "Automation", "JobLoss", "Shorts"]
    },
    {
        "id": 12,
        "title": "Diploma Lease",
        "hook": "YOUR KNOWLEDGE EXPIRED",
        "roast": """I got an email: "Your Bachelor's Degree has expired. Renew to retain knowledge."

I thought it was spam. It wasn't.

Apparently my university switched to a subscription model. Degrees are now licensed, not owned.

And if you don't pay the annual fee? The degree... deactivates.

Which sounds insane until you realize: professional certifications already do this.

Your nursing license expires. Your bar admission needs renewal. Your pilot's license has a time limit.

We already made knowledge a rental. This is just... expanding the model.

So I didn't renew. Because I'm broke.

And two weeks later I forgot calculus. Like, completely.

I could do derivatives last month. Now I can't remember the quadratic formula.

Is that psychosomatic? Or did the university actually DELETE my education remotely?

I don't know. And that's the scariest part.

Because if they CAN revoke knowledge... what else have we agreed to that we don't remember agreeing to?

I'm functionally less educated than I was six months ago.

Not because I didn't learn it. But because I couldn't afford to keep remembering it.

Abraham Lincoln. Self-taught lawyer. You're a monthly-payment professional.

Bitcoin bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt""",
        "tags": ["DarkComedy", "Education", "Subscription", "Knowledge", "Shorts"]
    }
]

def log(msg, status="INFO"):
    icons = {"INFO": "[INFO]", "SUCCESS": "[OK]", "ERROR": "[ERROR]", "PROCESS": "[PROCESS]"}
    print(f"{icons.get(status, '[INFO]')} {msg}")

def stutterize(text: str) -> str:
    """Light stutter for Josh Johnson's casual delivery"""
    words = text.split()
    out = []
    for w in words:
        if random.random() < 0.06 and len(w) > 4:  # Subtle stutter
            syl = w[:2]
            out.append(f"{syl}-{w}")
        else:
            out.append(w)
    return " ".join(out)

def audio(text, out):
    """Generate voice with conversational, deadpan delivery"""
    log("Generating Dark Josh Johnson voice...", "PROCESS")
    
    for voice_id in VOICES_MALE:
        try:
            r = requests.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                json={
                    "text": text,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {
                        "stability": 0.55,  # Higher for conversational clarity
                        "similarity_boost": 0.80,
                        "style": 0.65,  # Moderate for deadpan
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
                
                # Minimal processing for natural delivery
                subprocess.run([
                    "ffmpeg", "-y", "-i", str(tmp),
                    "-af", "acompressor=threshold=-16dB:ratio=3:attack=8:release=60",
                    str(out)
                ], capture_output=True, timeout=60)
                tmp.unlink(missing_ok=True)
                log(f"Dark Josh Johnson voice generated: {voice_id}", "SUCCESS")
                return True
        except Exception as e:
            log(f"Voice {voice_id} failed: {e}", "ERROR")
            continue
    return False

def fetch_pexels_broll(signal_id):
    """Fetch dark, moody B-roll"""
    if not USE_BROLL:
        return None
    
    queries = ["dark office", "empty room", "lonely city", "night urban", "isolated person"]
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
    """Create subtle glitch Abe for dark aesthetic"""
    log("Creating dark avatar...", "PROCESS")
    try:
        custom = next(iter(ROOT.glob('ChatGPT Image*.png')), None)
        img_path = custom if custom and custom.exists() else BASE / "temp" / "lincoln.jpg"
        
        if not img_path.exists():
            img_path.parent.mkdir(exist_ok=True)
            data = requests.get("https://upload.wikimedia.org/wikipedia/commons/a/ab/Abraham_Lincoln_O-77_matte_collodion_print.jpg", timeout=15).content
            with open(img_path, "wb") as f: f.write(data)
        
        dark_path = BASE / "temp" / "dark_abe.jpg"
        
        # Subtle pixelation
        img = Image.open(str(img_path)).convert('RGB')
        small = img.resize((120, 155), Image.NEAREST)
        img = small.resize((540, 700), Image.NEAREST)
        img.save(dark_path)
        
        log("Dark avatar created", "SUCCESS")
        return str(dark_path)
    except Exception as e:
        log(f"Avatar error: {e}", "ERROR")
        return str(img_path) if img_path.exists() else None

def create_dark_video(audio_path, out, signal):
    """Create dark, minimal video with subtle effects"""
    log("Creating Dark Josh Johnson video...", "PROCESS")
    
    try:
        from moviepy.editor import AudioFileClip, ImageClip, VideoFileClip, CompositeVideoClip, ColorClip
        
        audio = AudioFileClip(str(audio_path))
        duration = min(audio.duration, 60.0)
        
        abe_img = create_minimal_abe()
        if not abe_img:
            return False
        
        broll_clip = fetch_pexels_broll(signal['id'])
        
        # Minimal scanlines
        scan_path = BASE / "temp" / "dark_scan.png"
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
        
        # Subtle lip bar (grey for dark mood)
        bar = Image.new('RGBA', (400, 25), (120, 120, 130, 200))
        bar_path = BASE / "temp" / "dark_bar.png"
        bar.save(bar_path)
        
        # Minimal hook overlay
        hook_img = Image.new('RGBA', (1080, 180), (0,0,0,0))
        hook_draw = ImageDraw.Draw(hook_img)
        hook_draw.rectangle([(30, 30), (1050, 150)], fill=(10, 10, 15, 180), outline=(100, 100, 110, 200), width=2)
        hook_draw.text((540, 90), signal['hook'], fill=(200, 200, 210, 255), anchor="mm")
        hook_path = BASE / "temp" / "dark_hook.png"
        hook_img.save(hook_path)
        
        # Compose
        bg = ColorClip(size=(1080,1920), color=(8,8,12), duration=duration).set_audio(audio)  # Very dark
        
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
        
        temp_video = BASE / "temp" / f"dark_temp_{int(time.time())}.mp4"
        comp = CompositeVideoClip(layers, size=(1080,1920))
        comp.write_videofile(
            str(temp_video),
            fps=24, codec='libx264', audio_codec='aac',
            bitrate='8000k', preset='fast',
            verbose=False, logger=None
        )
        comp.close(); bg.close(); audio.close()
        
        # Subtle VHS degradation (dark aesthetic)
        log("Applying dark VHS effects...", "PROCESS")
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
            log("Dark Josh Johnson video created", "SUCCESS")
            return True
            
    except Exception as e:
        log(f"Video error: {e}", "ERROR")
        import traceback
        traceback.print_exc()
    return False

def upload_to_youtube(video_path, signal):
    """Upload to YouTube"""
    log("Uploading dark observation...", "PROCESS")
    
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
        
        title = f"Dark Josh Johnson: {signal['title']}"
        if is_short:
            title += " #Shorts"
        
        description = f"""{signal['hook']}

Abraham Lincoln delivering dark absurdist observations in Josh Johnson's style.

The uncomfortable truth about {signal['title']}.

Bitcoin: {BTC}

#{'#'.join(signal['tags'])}"""
        
        tags = signal['tags'] + ["Dark Comedy", "Absurdist", "Josh Johnson Style", "Social Commentary"]
        
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

def gen_dark_observation():
    """Generate one dark Josh Johnson observation"""
    signal = random.choice(DARK_SIGNALS)
    t = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    log(f"\n{'='*70}\nDARK JOSH JOHNSON #{signal['id']}: {signal['title']}\n{'='*70}", "INFO")
    log(f"Hook: {signal['hook']}")
    
    script = stutterize(signal['roast'])
    log(f"Script: {len(script)} chars")
    
    ap = BASE / f"audio/dark_{t}.mp3"
    if not audio(script, ap):
        return None
    
    vp = BASE / f"videos/DARK_{signal['id']}_{t}.mp4"
    if not create_dark_video(ap, vp, signal):
        return None
    
    youtube_url = upload_to_youtube(vp, signal)
    
    up = BASE / "uploaded" / f"DARK_JOSH{signal['id']}_{t}.mp4"
    up.parent.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy2(vp, up)
    
    mb = up.stat().st_size / (1024 * 1024)
    log(f"{'='*70}\nDARK OBSERVATION COMPLETE\n{'='*70}", "SUCCESS")
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
    
    mode = "WITH B-roll" if USE_BROLL else "WITHOUT B-roll"
    
    log(f"\n{'='*70}")
    log(f"DARK JOSH JOHNSON SYSTEM")
    log(f"Absurdist horror. Deadpan delivery. Uncomfortable truths.")
    log(f"{'='*70}")
    log(f"Generating {count} dark observations")
    log(f"Mode: {mode}")
    log(f"{'='*70}\n")
    
    results = []
    for i in range(count):
        result = gen_dark_observation()
        if result:
            results.append(result)
        if i < count - 1:
            log("\nWaiting 3 seconds...\n")
            time.sleep(3)
    
    log(f"\n{'='*70}")
    log(f"DARK OBSERVATIONS COMPLETE: {len(results)}/{count}")
    log(f"{'='*70}\n")
    
    for r in results:
        sig = r['signal']
        print(f"[DARK {sig['id']}] {sig['title']}")
        if r.get('youtube_url'):
            print(f"  URL: {r['youtube_url']}")


