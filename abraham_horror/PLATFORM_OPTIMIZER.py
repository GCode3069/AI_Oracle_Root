"""
PLATFORM OPTIMIZER - MULTI-FORMAT ENGINE
Generates content optimized for each platform:
- YouTube Shorts (9:16, 60s)
- YouTube Long (16:9, 3-10min)
- TikTok (9:16, 15-60s, trending sounds)
- Instagram Reels (9:16, 15-90s, aesthetic)
- Instagram Feed (4:5, polished)
- Twitter/X (1:1 or 16:9, 2:20 max)
- Facebook Reels (9:16)
- LinkedIn (16:9, professional)
- Reddit (various formats by subreddit)
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

# PLATFORM SPECIFICATIONS
PLATFORMS = {
    "youtube_shorts": {
        "name": "YouTube Shorts",
        "aspect_ratio": (9, 16),
        "resolution": (1080, 1920),
        "max_duration": 60,
        "min_duration": 15,
        "optimal_duration": 45,
        "format": "vertical",
        "hook_requirement": "first_3s",
        "text_overlay": "bold_top_bottom",
        "cta": "Like & Subscribe",
        "hashtags": 3,
        "description_length": 5000
    },
    "youtube_long": {
        "name": "YouTube Long",
        "aspect_ratio": (16, 9),
        "resolution": (1920, 1080),
        "max_duration": 600,
        "min_duration": 180,
        "optimal_duration": 300,
        "format": "horizontal",
        "hook_requirement": "first_10s",
        "text_overlay": "lower_third",
        "cta": "Subscribe for more",
        "hashtags": 5,
        "description_length": 5000,
        "chapters": True
    },
    "tiktok": {
        "name": "TikTok",
        "aspect_ratio": (9, 16),
        "resolution": (1080, 1920),
        "max_duration": 60,
        "min_duration": 15,
        "optimal_duration": 30,
        "format": "vertical",
        "hook_requirement": "first_1s",
        "text_overlay": "bold_center",
        "cta": "Follow for Part 2",
        "hashtags": 5,
        "trending_sounds": True,
        "description_length": 2200
    },
    "instagram_reels": {
        "name": "Instagram Reels",
        "aspect_ratio": (9, 16),
        "resolution": (1080, 1920),
        "max_duration": 90,
        "min_duration": 15,
        "optimal_duration": 45,
        "format": "vertical",
        "hook_requirement": "first_2s",
        "text_overlay": "aesthetic_minimal",
        "cta": "Save & Share",
        "hashtags": 10,
        "description_length": 2200
    },
    "instagram_feed": {
        "name": "Instagram Feed",
        "aspect_ratio": (4, 5),
        "resolution": (1080, 1350),
        "max_duration": 60,
        "min_duration": 3,
        "optimal_duration": 30,
        "format": "portrait",
        "hook_requirement": "first_frame",
        "text_overlay": "minimal_elegant",
        "cta": "See link in bio",
        "hashtags": 15,
        "description_length": 2200
    },
    "twitter": {
        "name": "Twitter/X",
        "aspect_ratio": (1, 1),
        "resolution": (1080, 1080),
        "max_duration": 140,
        "min_duration": 5,
        "optimal_duration": 45,
        "format": "square",
        "hook_requirement": "first_2s",
        "text_overlay": "quote_card",
        "cta": "Retweet if you agree",
        "hashtags": 2,
        "description_length": 280
    },
    "facebook_reels": {
        "name": "Facebook Reels",
        "aspect_ratio": (9, 16),
        "resolution": (1080, 1920),
        "max_duration": 90,
        "min_duration": 15,
        "optimal_duration": 60,
        "format": "vertical",
        "hook_requirement": "first_3s",
        "text_overlay": "bold_readable",
        "cta": "Share with friends",
        "hashtags": 5,
        "description_length": 2000
    },
    "linkedin": {
        "name": "LinkedIn",
        "aspect_ratio": (16, 9),
        "resolution": (1920, 1080),
        "max_duration": 600,
        "min_duration": 30,
        "optimal_duration": 120,
        "format": "horizontal",
        "hook_requirement": "first_5s",
        "text_overlay": "professional_lower_third",
        "cta": "Connect for insights",
        "hashtags": 3,
        "description_length": 3000,
        "tone": "professional"
    },
    "reddit": {
        "name": "Reddit",
        "aspect_ratio": (16, 9),
        "resolution": (1920, 1080),
        "max_duration": 900,
        "min_duration": 10,
        "optimal_duration": 120,
        "format": "horizontal_or_square",
        "hook_requirement": "first_5s",
        "text_overlay": "minimal",
        "cta": None,  # Reddit hates CTAs
        "hashtags": 0,
        "description_length": 40000,
        "tone": "authentic"
    }
}

def log(msg, status="INFO"):
    icons = {"INFO": "[INFO]", "SUCCESS": "[OK]", "ERROR": "[ERROR]", "PROCESS": "[PROCESS]"}
    print(f"{icons.get(status, '[INFO]')} {msg}")

def scrape_headlines():
    """Scrape headlines from multiple sources"""
    headlines = []
    
    if sheets_read_headlines and SHEET_ID:
        try:
            hs, _, _ = sheets_read_headlines(SHEET_ID, "Sheet1", 200)
            if hs:
                headlines.extend(hs[:20])
                log(f"Loaded {len(hs)} from Sheets", "SUCCESS")
        except: pass
    
    try:
        r = requests.get("https://news.google.com/rss", timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'xml')
            news = [item.title.text for item in soup.find_all('item')[:30] if item.title]
            headlines.extend(news)
            log(f"Scraped {len(news)} from News", "SUCCESS")
    except: pass
    
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
        headlines = ["AI automation replacing workers", "Social media addiction study"]
    
    return headlines

def generate_script_for_format(headline, format_type):
    """Generate platform-optimized script"""
    platform = PLATFORMS.get(format_type, PLATFORMS["youtube_shorts"])
    
    # Short format (15-60s)
    if platform["optimal_duration"] <= 60:
        script = f"""Abraham Lincoln. {headline}.

Here's the truth: You traded freedom for convenience.

Every click. Every swipe. Every "I Agree."

You're building your own chains.

I fought a war to end slavery. You volunteered for it.

Digital slavery. Algorithm slavery.

And you DEFEND it.

I freed the slaves. You enslaved yourself to apps.

Bitcoin {BTC}"""
    
    # Medium format (60-180s)
    elif platform["optimal_duration"] <= 180:
        script = f"""Abraham Lincoln. Six foot four. Honest Abe. {headline}.

Let me tell you what I see in 2025.

You have more freedom than any generation in history. And what did you do?

Gave it away. Click by click. Agreement by agreement.

Every app you download. Every terms of service you don't read. Every "convenient" feature.

You're building a prison. And calling it progress.

I led a war. 620,000 died. To end slavery in America.

Now you're volunteering for digital slavery. Surveillance slavery. Algorithm slavery.

Your phone tracks you. Your car tracks you. Your TV watches YOU watch IT.

And when someone points this out? You say "But it's so convenient!"

Yeah. Overseers were convenient too. Very efficient.

You know what's wild? You could stop. Right now. Delete the apps. Turn off the phone.

But you won't. Because the chains feel like comfort.

I freed the slaves. You enslaved yourself to convenience.

Bitcoin {BTC}"""
    
    # Long format (3-10min)
    else:
        script = f"""Abraham Lincoln. Sixteenth President of the United States. Born in a log cabin. Self-taught lawyer. Freed the slaves. Died for the Union.

Today's topic: {headline}.

Now, I want to talk about freedom. Real freedom. Not the kind you post about. The kind you LIVE.

[CHAPTER 1: THE PROBLEM]

In my time, slavery was obvious. Chains. Whips. Auction blocks.

In your time? It's invisible. It's voluntary. It's CONVENIENT.

You wake up. Check your phone. That's surveillance. You drive to work. That's tracking. You buy coffee. That's data collection.

Every single action. Monitored. Recorded. Analyzed. Sold.

And you know this. We're not breaking news here. You KNOW you're being watched.

But you accept it. Why? Convenience.

[CHAPTER 2: THE HISTORY]

Let me give you some context. In the 1850s, we had a choice. Compromise with slavery. Keep the peace. Maintain the economy.

Or fight for freedom. Real freedom. Even if it meant war.

We chose war. 620,000 Americans died. But we ended legal slavery.

You have the same choice. Right now. Compromise with digital slavery. Keep the convenience. Maintain your lifestyle.

Or fight for freedom. Real freedom. Even if it means inconvenience.

But here's the difference: Your fight doesn't require bloodshed. It requires DISCIPLINE.

[CHAPTER 3: THE SOLUTION]

Delete the apps. Turn off location. Read the terms of service. Say NO to convenience that costs freedom.

It's that simple. And that hard.

Because you're addicted. Literally. These apps are designed to be addictive. The algorithms WANT you dependent.

And they won won. You're dependent.

[CHAPTER 4: THE CALL TO ACTION]

I fought to preserve the Union. I signed the Emancipation Proclamation. I died for these principles.

What are YOU willing to sacrifice? Convenience? Comfort? Likes?

The choice is yours. It always has been.

Freedom isn't free. It never was. It costs something.

In my time, it cost blood.

In your time? It costs discipline.

Choose wisely.

Abraham Lincoln. Still dead. Still right.

Bitcoin {BTC}"""
    
    return script

def generate_audio(text, output_path):
    """Generate voice (platform-optimized pacing)"""
    log("Generating voice...", "PROCESS")
    
    for voice_id in VOICES_MALE:
        try:
            r = requests.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                json={
                    "text": text,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.85,
                        "style": 0.75,
                        "use_speaker_boost": True
                    }
                },
                headers={"xi-api-key": ELEVENLABS_KEY},
                timeout=180
            )
            if r.status_code == 200:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "wb") as f: f.write(r.content)
                log(f"Voice generated", "SUCCESS")
                return True
        except Exception as e:
            log(f"Voice {voice_id} failed: {e}", "ERROR")
            continue
    return False

def create_platform_optimized_video(audio_path, output_path, platform_key, headline):
    """Create video optimized for specific platform"""
    platform = PLATFORMS[platform_key]
    log(f"Creating {platform['name']} optimized video...", "PROCESS")
    
    try:
        from moviepy.editor import AudioFileClip, ImageClip, CompositeVideoClip, ColorClip, TextClip
        
        audio = AudioFileClip(str(audio_path))
        
        # Platform-specific duration limits
        duration = min(audio.duration, platform["max_duration"])
        duration = max(duration, platform["min_duration"])
        
        # Get resolution
        width, height = platform["resolution"]
        
        # Get avatar
        custom = next(iter(ROOT.glob('ChatGPT Image*.png')), None)
        if custom and custom.exists():
            img_path = custom
        else:
            img_path = BASE / "temp" / "lincoln.jpg"
            if not img_path.exists() or img_path.stat().st_size < 1000:
                img_path.parent.mkdir(exist_ok=True, parents=True)
                try:
                    data = requests.get("https://upload.wikimedia.org/wikipedia/commons/a/ab/Abraham_Lincoln_O-77_matte_collodion_print.jpg", timeout=15).content
                    with open(img_path, "wb") as f: f.write(data)
                except:
                    # Solid color fallback
                    solid = Image.new('RGB', (width, height), (20, 10, 15))
                    solid_path = BASE / "temp" / "solid.jpg"
                    solid.save(solid_path)
                    img_path = solid_path
        
        # Platform-specific composition
        bg = ColorClip(size=(width, height), color=(15, 10, 20), duration=duration).set_audio(audio)
        
        try:
            img = Image.open(str(img_path)).convert('RGB')
            small = img.resize((108, 140), Image.NEAREST)
            img_resized = small.resize((int(width*0.5), int(height*0.36)), Image.NEAREST)
            
            temp_img_path = BASE / "temp" / f"resized_{platform_key}.jpg"
            img_resized.save(temp_img_path)
            
            # Platform-specific positioning
            if platform["format"] == "vertical":
                abe = ImageClip(str(temp_img_path)).set_position(('center', int(height*0.55))).set_duration(duration)
            elif platform["format"] == "horizontal":
                abe = ImageClip(str(temp_img_path)).set_position((int(width*0.6), 'center')).set_duration(duration)
            else:  # square
                abe = ImageClip(str(temp_img_path)).set_position(('center', 'center')).set_duration(duration)
        except:
            abe = None
        
        # Platform-specific text overlay (using PIL instead of TextClip)
        hook_text = headline[:40] + "..." if len(headline) > 40 else headline
        hook_img = Image.new('RGBA', (width, int(height*0.15)), (0,0,0,0))
        hook_draw = ImageDraw.Draw(hook_img)
        
        # Platform-specific styling
        if platform_key == "tiktok":
            # Bold center
            hook_draw.rectangle([(20, 20), (width-20, int(height*0.15)-20)], 
                              fill=(255, 0, 0, 200), outline=(255, 255, 255, 255), width=3)
        elif platform_key == "instagram_reels":
            # Aesthetic minimal
            hook_draw.rectangle([(40, 30), (width-40, int(height*0.15)-30)], 
                              fill=(0, 0, 0, 150), outline=(200, 200, 200, 200), width=2)
        elif platform_key == "linkedin":
            # Professional lower third
            hook_draw.rectangle([(0, 0), (width, int(height*0.15))], 
                              fill=(10, 102, 194, 180))
        else:
            # Default
            hook_draw.rectangle([(30, 30), (width-30, int(height*0.15)-30)], 
                              fill=(20, 0, 0, 180), outline=(200, 0, 0, 255), width=2)
        
        hook_draw.text((width//2, int(height*0.075)), hook_text[:30], 
                      fill=(255, 255, 255, 255), anchor="mm")
        
        hook_path = BASE / "temp" / f"hook_{platform_key}.png"
        hook_img.save(hook_path)
        
        # Platform-specific hook duration
        hook_duration = {
            "tiktok": 1.5,
            "youtube_shorts": 3.0,
            "instagram_reels": 2.0,
            "twitter": 2.0,
        }.get(platform_key, 3.0)
        
        hook_clip = ImageClip(str(hook_path)).set_position(('center', int(height*0.15))).set_duration(min(hook_duration, duration)).set_opacity(0.9)
        
        # Compose
        layers = [bg]
        if abe:
            layers.append(abe)
        layers.append(hook_clip)
        
        comp = CompositeVideoClip(layers, size=(width, height))
        
        # Platform-specific export settings
        if platform_key in ["tiktok", "instagram_reels"]:
            # Higher quality for social
            preset = "fast"
            crf = "23"
            bitrate = "8000k"
        elif platform_key == "youtube_long":
            # Highest quality for long-form
            preset = "slow"
            crf = "20"
            bitrate = "12000k"
        else:
            # Balanced
            preset = "fast"
            crf = "25"
            bitrate = "6000k"
        
        comp.write_videofile(
            str(output_path),
            fps=24 if platform_key != "tiktok" else 30,  # TikTok prefers 30fps
            codec='libx264',
            audio_codec='aac',
            bitrate=bitrate,
            preset=preset,
            verbose=False,
            logger=None
        )
        
        comp.close()
        bg.close()
        audio.close()
        
        log(f"{platform['name']} video created", "SUCCESS")
        return True
        
    except Exception as e:
        log(f"Video error: {e}", "ERROR")
        import traceback
        traceback.print_exc()
    return False

def generate_platform_metadata(platform_key, headline, script):
    """Generate platform-specific titles, descriptions, hashtags"""
    platform = PLATFORMS[platform_key]
    
    # Platform-specific title
    if platform_key == "youtube_shorts":
        title = f"Abe Lincoln: {headline[:45]}... #Shorts"
    elif platform_key == "youtube_long":
        title = f"Abraham Lincoln on {headline[:50]} | Full Analysis"
    elif platform_key == "tiktok":
        title = f"{headline[:30]}... 💀"
    elif platform_key == "instagram_reels":
        title = f"✨ {headline[:40]} ✨"
    elif platform_key == "linkedin":
        title = f"Historical Perspective: {headline[:50]}"
    else:
        title = headline[:60]
    
    # Platform-specific description
    if platform_key in ["youtube_shorts", "youtube_long"]:
        description = f"""{script[:500]}...

Abraham Lincoln delivers dark observations on modern society.

Bitcoin: {BTC}

#AbrahamLincoln #DarkComedy #SocialCommentary"""
    
    elif platform_key == "tiktok":
        description = f"Abe Lincoln spitting facts 💀 {headline[:100]}... #fyp #viral #comedy"
    
    elif platform_key == "instagram_reels":
        description = f"{headline}\n\nAbraham Lincoln × Modern Commentary\n\n{BTC}"
    
    elif platform_key == "linkedin":
        description = f"""Historical Analysis: {headline}

Abraham Lincoln's perspective on contemporary issues provides valuable insights for leaders and professionals.

Key Takeaways:
• Digital transformation challenges
• Leadership in uncertain times
• Balancing innovation with ethics

#Leadership #History #Innovation"""
    
    else:
        description = script[:platform["description_length"]]
    
    # Platform-specific hashtags
    base_tags = ["AbrahamLincoln", "History", "Commentary"]
    
    if platform_key == "tiktok":
        hashtags = ["fyp", "viral", "comedy", "darkhumor", "truth"] + base_tags
    elif platform_key == "instagram_reels":
        hashtags = ["reels", "viral", "trending", "explore", "comedy"] + base_tags
    elif platform_key == "linkedin":
        hashtags = ["Leadership", "Innovation", "Business", "History"]
    else:
        hashtags = base_tags
    
    return {
        "title": title[:platform.get("title_max", 100)],
        "description": description[:platform["description_length"]],
        "hashtags": hashtags[:platform["hashtags"]] if platform["hashtags"] > 0 else [],
        "cta": platform.get("cta")
    }

def generate_multi_platform_content():
    """Generate one piece of content in ALL platform formats"""
    t = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    log(f"\n{'='*70}\nMULTI-PLATFORM CONTENT GENERATION\n{'='*70}", "INFO")
    
    # Scrape headline
    headlines = scrape_headlines()
    headline = random.choice(headlines)
    log(f"Headline: {headline[:60]}")
    
    results = {}
    
    # Generate for each platform
    platforms_to_generate = [
        "youtube_shorts",
        "youtube_long",
        "tiktok",
        "instagram_reels",
        "twitter",
    ]
    
    for platform_key in platforms_to_generate:
        platform = PLATFORMS[platform_key]
        log(f"\n[{platform['name']}]", "PROCESS")
        
        # Generate platform-specific script
        script = generate_script_for_format(headline, platform_key)
        log(f"Script: {len(script)} chars")
        
        # Generate audio
        ap = BASE / f"audio/{platform_key}_{t}.mp3"
        if not generate_audio(script, ap):
            log(f"Skipping {platform_key} - audio failed", "ERROR")
            continue
        
        # Create video
        vp = BASE / f"videos/{platform_key}_{t}.mp4"
        if not create_platform_optimized_video(ap, vp, platform_key, headline):
            log(f"Skipping {platform_key} - video failed", "ERROR")
            continue
        
        # Generate metadata
        metadata = generate_platform_metadata(platform_key, headline, script)
        
        # Save
        up = BASE / "uploaded" / f"{platform_key}_{t}.mp4"
        up.parent.mkdir(parents=True, exist_ok=True)
        import shutil
        shutil.copy2(vp, up)
        
        mb = up.stat().st_size / (1024 * 1024)
        
        results[platform_key] = {
            "file": str(up),
            "size_mb": round(mb, 2),
            "metadata": metadata,
            "resolution": platform["resolution"],
            "duration": f"~{platform['optimal_duration']}s"
        }
        
        log(f"{platform['name']}: {mb:.1f}MB - {platform['resolution']}", "SUCCESS")
    
    log(f"\n{'='*70}\nCOMPLETE - Generated {len(results)} platform variants\n{'='*70}", "SUCCESS")
    
    return {
        "headline": headline,
        "timestamp": t,
        "platforms": results
    }

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 1
    
    log(f"\n{'='*70}")
    log(f"PLATFORM-OPTIMIZED MULTI-FORMAT GENERATOR")
    log(f"{'='*70}")
    log(f"Platforms: YouTube (Shorts + Long), TikTok, Instagram, Twitter")
    log(f"Generating {count} multi-platform content sets")
    log(f"{'='*70}\n")
    
    all_results = []
    for i in range(count):
        result = generate_multi_platform_content()
        if result:
            all_results.append(result)
        if i < count - 1:
            log("\nWaiting 5 seconds...\n")
            time.sleep(5)
    
    log(f"\n{'='*70}")
    log(f"GENERATION COMPLETE: {len(all_results)} content sets")
    log(f"{'='*70}\n")
    
    for r in all_results:
        print(f"\n[{r['timestamp']}] {r['headline'][:50]}")
        for platform, data in r['platforms'].items():
            print(f"  • {platform:20s} {data['size_mb']:6.1f}MB  {data['resolution']}")


