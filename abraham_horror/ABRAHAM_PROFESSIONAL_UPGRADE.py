"""
ABRAHAM LINCOLN - PROFESSIONAL VIDEO SYSTEM
Matches/exceeds FarFromWeakFFW channel quality:
- Dynamic cuts every 2-3 seconds
- Multiple B-roll clips with transitions
- Professional text overlays with animations
- Retention hooks in first 3 seconds
- High-quality visuals from Pexels
- Smooth zooms and effects
- Algorithm-optimized pacing
"""
import os, sys, json, requests, subprocess, random, time, re
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
ELEVENLABS_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
PEXELS_KEY = "RgE9Mdn3ToSQhn2RiLJ4mPMISjjp587QKRG9uhpOrLVtkKPCibUPUDGh"
BTC = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"
PRODUCT = "https://trenchaikits.com/buy-rebel-$97"

VOICES = [
    "VR6AewLTigWG4xSOukaG",  # Deep male - best for Lincoln
    "pNInz6obpgDQGcFmaJgB",  # Ominous male - fallback
    "EXAVITQu4vr4xnSDxMaL",  # Another deep male
]

YOUTUBE_CREDENTIALS = Path("F:/AI_Oracle_Root/scarify/config/credentials/youtube/client_secrets.json")

# Optional Google Sheets integration
SHEET_ID = "1jvWP95U0ksaHw97PrPZsrh6ZVllviJJof7kQ2dV0ka0"
try:
    from sheets_helper import read_headlines as sheets_read_headlines
except Exception:
    sheets_read_headlines = None

def _build_audio_envelope(audio_clip):
    """Return a function env(t) in [0,1] based on audio loudness for subtle animation."""
    try:
        # Sample the audio to a coarse envelope for efficiency
        samples = audio_clip.to_soundarray(fps=24)
        import numpy as np
        # RMS per frame
        rms = np.sqrt((samples.astype(float) ** 2).mean(axis=1))
        # Normalize
        if rms.max() == 0:
            return lambda t: 0.0
        norm = (rms / rms.max()).clip(0, 1)
        # Create lookup
        def env(t: float) -> float:
            idx = int(min(len(norm) - 1, max(0, t * 24)))
            return float(norm[idx])
        return env
    except Exception:
        return lambda t: 0.0

def scrape_current_headlines():
    """Scrape trending headlines from multiple sources; prefer Google Sheets if configured."""
    # 1) Try Google Sheets first
    if sheets_read_headlines and SHEET_ID and len(SHEET_ID) > 10:
        try:
            hs, _, _ = sheets_read_headlines(SHEET_ID, "Sheet1", 200)
            if hs:
                return hs
        except Exception as e:
            print(f"    [WARNING] Sheets read failed: {e}")
    headlines = []
    sources = [
        "https://news.google.com/rss",
        "https://www.reddit.com/r/news/.rss",
        "https://www.reddit.com/r/worldnews/.rss",
        "https://feeds.feedburner.com/oreilly/radar",
    ]
    
    for url in sources:
        try:
            r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code == 200:
                soup = BeautifulSoup(r.content, 'xml')
                items = soup.find_all('item')[:10]
                for item in items:
                    title = item.title.text if item.title else ""
                    if title and len(title) > 20 and len(title) < 200:
                        headlines.append(title.strip())
        except Exception as e:
            if ELEVENLABS_KEY == "YOUR_KEY_HERE":
                print(f"    [WARNING] Config load failed: {e}")
            pass
    
    return headlines if headlines else ["Breaking: Major News Story", "Politics Update Today", "Tech Industry Changes"]

def generate_comedy_script(headline):
    """Generate dark satirical comedy script in Chappelle/Carlin/Pryor style"""
    hl_lower = headline.lower()
    
    # Detect topic
    is_trump = any(x in hl_lower for x in ["trump", "donald", "maga"])
    is_politics = any(x in hl_lower for x in ["congress", "senate", "vote", "election"])
    is_tech = any(x in hl_lower for x in ["ai", "tech", "musk", "apple", "google"])
    is_economy = any(x in hl_lower for x in ["billion", "stock", "market", "economy"])
    is_crime = any(x in hl_lower for x in ["shoot", "kill", "murder", "crime"])
    is_war = any(x in hl_lower for x in ["war", "ukraine", "russia", "military"])
    
    # Comedy opening hooks (Chappelle style)
    hooks = [
        "Yo, Abraham Lincoln here. I'm dead. Dead as hell. But I still read the news.",
        "It's me. The guy from the penny. And this headline? This is why I'm glad I'm dead.",
        "Abraham Lincoln speaking. I fought a civil war. I freed slaves. This headline? This is worse.",
        "Lincoln here. Dead since 1865. Still smarter than whoever wrote this headline.",
    ]
    
    # Topic-specific roasts
    if is_trump:
        roast = f"Look, {headline}. I preserved the Union through a civil war. He can't preserve his dignity through a tweet. We are not the same."
    elif is_politics:
        roast = f"So {headline}. Politics. The art of making people think you're solving problems while actually making them worse. I'd know. I was president."
    elif is_tech:
        roast = f"{headline}. Billionaires launching rockets while people can't afford rent. I freed slaves. You created an app for it. Progress."
    elif is_economy:
        roast = f"{headline}. Money changing hands. None of it reaching the people who need it. Trickle-down? More like trickle-away."
    elif is_crime:
        roast = f"{headline}. Another day, another tragedy. Your response? Thoughts and prayers. I got thoughts: you're useless. Also dead. But still smarter."
    elif is_war:
        roast = f"{headline}. War never changes. Except now you can watch it live on Twitter. At least I died before social media."
    else:
        roast = f"{headline}. This is what passes for news. I've been dead 160 years. This headline makes me glad."
    
    # Closing with call to action
    closer = f"Anyway. The truth costs money. Bitcoin: {BTC}. Get prepared: {PRODUCT}. From beyond the grave, Lincoln."
    
    script = f"{random.choice(hooks)}\n\n{roast}\n\n{closer}"
    
    # Clean script (remove any screen directions)
    script = re.sub(r'\*[^\*]*\*', '', script)
    script = re.sub(r'\[[^\]]*\]', '', script)
    
    return script.strip()

def generate_male_voice(script, output_path):
    """Generate audio with proper male Lincoln voice"""
    print("    [AUDIO] Generating professional voice...")
    
    for voice_id in VOICES:
        try:
            r = requests.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                json={
                    "text": script,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {
                        "stability": 0.4,
                        "similarity_boost": 0.9,
                        "style": 0.8,
                        "use_speaker_boost": True
                    }
                },
                headers={"xi-api-key": ELEVENLABS_KEY},
                timeout=240
            )
            if r.status_code == 200:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                temp_file = output_path.parent / f"temp_{output_path.name}"
                with open(temp_file, "wb") as f:
                    f.write(r.content)
                
                # Apply professional audio enhancement
                subprocess.run([
                    "ffmpeg", "-i", str(temp_file),
                    "-af", "aecho=0.6:0.5:500:0.3,atempo=0.98,bass=g=2,treble=g=1",
                    "-y", str(output_path)
                ], capture_output=True, timeout=180)
                temp_file.unlink()
                print(f"    [OK] Generated with voice: {voice_id}")
                return True
        except Exception as e:
            print(f"    [WARNING] Voice {voice_id} failed: {e}")
            continue
    
    return False

def get_pexels_video(keyword, count=3):
    """Get multiple high-quality video clips from Pexels"""
    try:
        r = requests.get(
            "https://api.pexels.com/videos/search",
            headers={"Authorization": PEXELS_KEY},
            params={"query": keyword, "per_page": min(count, 15), "orientation": "portrait"},
            timeout=30
        )
        if r.status_code == 200:
            data = r.json()
            videos = []
            for vid in data.get("videos", [])[:count]:
                # Get highest quality file
                files = vid.get("video_files", [])
                if files:
                    best_file = max(files, key=lambda x: x.get("width", 0) * x.get("height", 0))
                    videos.append({
                        "url": best_file["link"],
                        "width": best_file.get("width", 1080),
                        "height": best_file.get("height", 1920),
                        "duration": vid.get("duration", 5)
                    })
            return videos
    except Exception as e:
        print(f"    [WARNING] Pexels search failed: {e}")
    return []

def create_professional_video(audio_path, output_path, headline, script):
    """Create professional video with dynamic cuts, transitions, and effects"""
    print("    [VIDEO] Creating professional video...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        from moviepy.editor import (
            VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip,
            concatenate_videoclips, ImageClip
        )
        from PIL import Image
        import numpy as np
        
        audio = AudioFileClip(str(audio_path))
        duration = audio.duration
        
        # Get multiple B-roll clips for dynamic editing
        keywords = ["dark dramatic", "industrial", "cinematic", "urban", "moody"]
        keyword = random.choice(keywords)
        
        print(f"    [B-ROLL] Fetching {keyword} videos from Pexels...")
        pexels_videos = get_pexels_video(keyword, count=5)
        
        # Download video clips
        video_clips = []
        temp_dir = BASE / "temp" / "video_clips"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        for i, vid_info in enumerate(pexels_videos[:3]):  # Use up to 3 clips
            try:
                vid_data = requests.get(vid_info["url"], timeout=60).content
                temp_vid_path = temp_dir / f"clip_{i}.mp4"
                with open(temp_vid_path, "wb") as f:
                    f.write(vid_data)
                
                clip = VideoFileClip(str(temp_vid_path))
                # Crop to vertical and resize
                if clip.w > clip.h:
                    # Landscape - crop center
                    x_center = clip.w / 2
                    clip = clip.crop(x_center=clip.w/2, width=clip.h)
                clip = clip.resize((1080, 1920))
                
                # Limit clip duration for faster cuts
                clip_duration = min(3.0, clip.duration)  # 2-3 second cuts
                clip = clip.subclip(0, clip_duration).without_audio()
                video_clips.append(clip)
                print(f"    [OK] Added clip {i+1}: {clip_duration:.1f}s")
            except Exception as e:
                print(f"    [WARNING] Clip {i+1} failed: {e}")
                continue
        
        # If no Pexels clips, create dynamic background
        if not video_clips:
            print("    [FALLBACK] Creating dynamic background...")
            from moviepy.video.tools.drawing import color_gradient
            
            # Create animated gradient background
            bg = ImageClip(str(create_animated_bg(duration))).set_duration(duration)
            video_clips.append(bg)
        
        # Stitch clips with loops to match audio duration
        base_video = concatenate_videoclips(video_clips, method="compose")
        if base_video.duration < duration:
            loops = int(duration / base_video.duration) + 1
            base_video = concatenate_videoclips([base_video] * loops, method="compose")
        base_video = base_video.subclip(0, duration).set_audio(audio)
        
        # Add Lincoln portrait overlay (animated, audio-reactive)
        images_dir = BASE / "images"
        lincoln_img_path = None
        if images_dir.exists():
            possible_images = list(images_dir.glob("*lincoln*.jpg")) + list(images_dir.glob("*lincoln*.png"))
            if possible_images:
                lincoln_img_path = possible_images[0]
        
        overlays = [base_video]
        
        # Add animated Lincoln portrait (bottom third) with CRT scanlines
        if lincoln_img_path and lincoln_img_path.exists():
            env = _build_audio_envelope(audio)
            base_w, base_h = 430, 540
            lincoln_base = ImageClip(str(lincoln_img_path)).resize((base_w, base_h))
            # Audio-reactive scale and slight jitter
            def lincoln_size(t):
                factor = 1.0 + 0.05 * env(t)
                return (int(base_w * factor), int(base_h * factor))
            def lincoln_pos(t):
                import math
                x = (1080 - lincoln_size(t)[0]) // 2 + int(2 * math.sin(t * 6.0))
                y = 1380 + int(3 * math.sin(t * 4.0))
                return (x, y)
            lincoln_clip = lincoln_base.resize(lambda t: lincoln_size(t)).set_position(lincoln_pos).set_duration(duration)
            lincoln_clip = lincoln_clip.fadein(0.8).fadeout(0.8)
            overlays.append(lincoln_clip)
            # CRT scanlines overlay
            try:
                from PIL import Image, ImageDraw
                scan = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
                draw = ImageDraw.Draw(scan)
                for y in range(0, 1920, 4):
                    draw.line([(0, y), (1080, y)], fill=(0, 0, 0, 70), width=2)
                scan_path = BASE / "temp" / f"scanlines_{timestamp}.png"
                scan.save(scan_path)
                scan_clip = ImageClip(str(scan_path)).set_opacity(0.30).set_duration(duration)
                overlays.append(scan_clip)
            except Exception:
                pass
        
        # Add headline text (first 3 seconds - retention hook) - using PIL instead of TextClip
        try:
            from PIL import Image, ImageDraw, ImageFont
            headline_img = Image.new('RGBA', (1080, 200), (0, 0, 0, 0))
            draw = ImageDraw.Draw(headline_img)
            # Try to use Impact font, fallback to default
            try:
                font = ImageFont.truetype("arial.ttf", 56)  # Windows default
            except:
                font = ImageFont.load_default()
            
            text = headline.upper()[:50]
            # Get text size and center it
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (1080 - text_width) // 2
            y = (200 - text_height) // 2
            
            # Draw text with outline (stroke)
            for adj in range(-3, 4):
                for adj2 in range(-3, 4):
                    if adj != 0 or adj2 != 0:
                        draw.text((x+adj, y+adj2), text, font=font, fill=(0, 0, 0, 200))
            draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
            
            headline_img_path = BASE / "temp" / f"headline_{timestamp}.png"
            headline_img.save(headline_img_path)
            
            headline_clip = ImageClip(str(headline_img_path)).set_position(('center', 200)).set_duration(3.5).fadein(0.3).fadeout(0.5)
            overlays.append(headline_clip)
        except Exception as e:
            print(f"    [WARNING] Headline text overlay failed: {e}, continuing without it")
        
        # Add key phrases as animated text (word-by-word for retention) - using PIL
        try:
            words = script.split()[:20]  # First 20 words
            word_duration = min(0.5, duration / len(words))
            
            for i, word in enumerate(words[:15]):  # Show 15 words max
                if i * word_duration >= duration - 2:
                    break  # Don't overlap with CTA
                
                try:
                    from PIL import Image, ImageDraw, ImageFont
                    word_img = Image.new('RGBA', (400, 80), (0, 0, 0, 0))
                    draw = ImageDraw.Draw(word_img)
                    try:
                        font = ImageFont.truetype("arial.ttf", 42)
                    except:
                        font = ImageFont.load_default()
                    
                    text = word.upper()
                    bbox = draw.textbbox((0, 0), text, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    x = (400 - text_width) // 2
                    y = (80 - text_height) // 2
                    
                    # Draw text with outline
                    for adj in range(-2, 3):
                        for adj2 in range(-2, 3):
                            if adj != 0 or adj2 != 0:
                                draw.text((x+adj, y+adj2), text, font=font, fill=(0, 0, 0, 200))
                    draw.text((x, y), text, font=font, fill=(255, 215, 0, 255))  # Yellow
                    
                    word_img_path = BASE / "temp" / f"word_{timestamp}_{i}.png"
                    word_img.save(word_img_path)
                    
                    word_clip = ImageClip(str(word_img_path)).set_position(('center', 1600)).set_duration(word_duration * 1.5).set_start(i * word_duration)
                    word_clip = word_clip.fadein(0.1).fadeout(0.1)
                    overlays.append(word_clip)
                except Exception as e:
                    continue  # Skip this word if it fails
        except Exception as e:
            print(f"    [WARNING] Word overlay failed: {e}, continuing without it")
        
        # Add CTA text (last 3 seconds) - using PIL
        try:
            from PIL import Image, ImageDraw, ImageFont
            cta_img = Image.new('RGBA', (1080, 150), (0, 0, 0, 0))
            draw = ImageDraw.Draw(cta_img)
            try:
                font = ImageFont.truetype("arial.ttf", 50)
            except:
                font = ImageFont.load_default()
            
            cta_text = f"SUPPORT: {BTC[:30]}..."
            bbox = draw.textbbox((0, 0), cta_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (1080 - text_width) // 2
            y = (150 - text_height) // 2
            
            # Draw text with outline
            for adj in range(-3, 4):
                for adj2 in range(-3, 4):
                    if adj != 0 or adj2 != 0:
                        draw.text((x+adj, y+adj2), cta_text, font=font, fill=(0, 0, 0, 200))
            draw.text((x, y), cta_text, font=font, fill=(255, 215, 0, 255))  # Gold
            
            cta_img_path = BASE / "temp" / f"cta_{timestamp}.png"
            cta_img.save(cta_img_path)
            
            cta_clip = ImageClip(str(cta_img_path)).set_position(('center', 250)).set_duration(3.0).set_start(duration - 3.5)
            cta_clip = cta_clip.fadein(0.5)
            overlays.append(cta_clip)
        except Exception as e:
            print(f"    [WARNING] CTA text overlay failed: {e}, continuing without it")
        
        # Composite final video
        final = CompositeVideoClip(overlays, size=(1080, 1920))
        
        # Export with high quality
        output_path.parent.mkdir(parents=True, exist_ok=True)
        final.write_videofile(
            str(output_path),
            fps=24,
            codec='libx264',
            audio_codec='aac',
            bitrate='10000k',
            preset='medium',
            verbose=False,
            logger=None
        )
        
        # Cleanup
        base_video.close()
        final.close()
        for clip in video_clips:
            clip.close()
        
        print(f"    [OK] Professional video created: {output_path.name}")
        return True
        
    except Exception as e:
        print(f"    [ERROR] Video creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_animated_bg(duration):
    """Create animated gradient background"""
    try:
        from PIL import Image, ImageDraw
        from moviepy.video.VideoClip import ColorClip
        
        temp_dir = BASE / "temp"
        temp_dir.mkdir(parents=True, exist_ok=True)
        bg_path = temp_dir / f"animated_bg_{int(time.time())}.mp4"
        
        # Method 1: Try creating frames and stitching with FFmpeg
        frame_count = int(duration * 8)  # 8 fps
        frame_dir = temp_dir / "bg_frames"
        frame_dir.mkdir(exist_ok=True)
        
        frames_created = False
        try:
            for i in range(min(frame_count, 120)):  # Max 120 frames (15 seconds @ 8fps)
                img = Image.new('RGB', (1080, 1920), (20 + (i % 30), 20, 30 + (i % 20)))
                draw = ImageDraw.Draw(img)
                # Add subtle animated pattern
                for y in range(0, 1920, 50):
                    alpha = int(20 * (1 + 0.5 * ((i % 10) / 10)))
                    draw.rectangle([0, y, 1080, y+25], fill=(alpha, alpha, alpha+10))
                # Save frame
                frame_path = frame_dir / f"bg_frame_{i:04d}.png"
                img.save(frame_path)
            
            frames_created = True
            # Stitch frames into video
            result = subprocess.run([
                "ffmpeg", "-y", "-framerate", "8", 
                "-i", str(frame_dir / "bg_frame_%04d.png"),
                "-t", str(duration), "-s", "1080x1920", 
                "-c:v", "libx264", "-pix_fmt", "yuv420p",
                "-pix_fmt", "yuv420p", str(bg_path)
            ], capture_output=True, timeout=90)
            
            if result.returncode == 0 and bg_path.exists():
                # Cleanup frames
                for f in frame_dir.glob("*.png"):
                    f.unlink()
                return bg_path
        except Exception as e:
            print(f"    [WARNING] Frame-based bg failed: {e}, trying ColorClip method")
        
        # Method 2: Fallback to MoviePy ColorClip (more reliable)
        try:
            from moviepy.editor import ColorClip
            bg_clip = ColorClip(size=(1080, 1920), color=(30, 20, 40), duration=duration)
            bg_clip.write_videofile(str(bg_path), fps=24, codec='libx264', audio=False, 
                                  verbose=False, logger=None, preset='medium')
            bg_clip.close()
            if bg_path.exists():
                return bg_path
        except Exception as e:
            print(f"    [WARNING] ColorClip method failed: {e}")
        
        # Method 3: Final fallback - solid color video with FFmpeg
        try:
            result = subprocess.run([
                "ffmpeg", "-y", "-f", "lavfi", 
                "-i", f"color=c=0x1e1428:s=1080x1920:d={duration}",
                "-c:v", "libx264", "-pix_fmt", "yuv420p",
                "-pix_fmt", "yuv420p", str(bg_path)
            ], capture_output=True, timeout=60)
            if result.returncode == 0 and bg_path.exists():
                return bg_path
        except:
            pass
        
        return None
    except Exception as e:
        print(f"    [ERROR] Background creation failed: {e}")
        return None

def get_audio_duration(audio_path):
    """Get audio duration in seconds"""
    try:
        result = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)
        ], capture_output=True, text=True, timeout=30)
        return float(result.stdout.strip())
    except:
        return 60.0

def upload_to_youtube(video_path, title, description, tags):
    """Upload to YouTube with channel ID"""
    print("    [YOUTUBE] Uploading to channel UCS5pEpSCw8k4wene0iv0uAg...")
    
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        import pickle
        
        SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
        
        # Try multiple credential locations
        cred_files = [
            YOUTUBE_CREDENTIALS,
            Path("F:/AI_Oracle_Root/scarify/client_secret_679199614743-1fq6sini3p9kjs237ek4seg4ojp4a4qe.apps.googleusercontent.com.json"),
            Path("F:/AI_Oracle_Root/scarify/config/credentials/youtube/client_secrets.json"),
        ]
        
        cred_file = None
        for cf in cred_files:
            if cf and cf.exists():
                cred_file = cf
                break
        
        if not cred_file:
            print("    [ERROR] YouTube credentials not found")
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
        except:
            duration = 60.0
        
        is_short = duration <= 60
        short_tag = " #Shorts" if is_short else ""
        
        request_body = {
            'snippet': {
                'title': title + short_tag,
                'description': description,
                'tags': tags,
                'categoryId': '24'
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
        
        print(f"    [OK] Uploaded: {video_url}")
        print(f"    [STUDIO] https://studio.youtube.com/channel/UCS5pEpSCw8k4wene0iv0uAg/videos")
        
        return video_url
        
    except Exception as e:
        print(f"    [ERROR] Upload failed: {e}")
        return None

def generate_professional_video():
    """Generate one complete professional video"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Scrape headline
    headlines = scrape_current_headlines()
    headline = random.choice(headlines) if headlines else "Breaking News Update"
    print(f"Headline: {headline[:60]}")
    
    # Generate script
    script = generate_comedy_script(headline)
    print(f"Script: {len(script)} chars")
    
    # Generate audio
    audio_path = BASE / "audio" / f"pro_{timestamp}.mp3"
    if not generate_male_voice(script, audio_path):
        return None
    
    # Create professional video
    video_path = BASE / "videos" / f"PRO_{timestamp}.mp4"
    if not create_professional_video(audio_path, video_path, headline, script):
        return None
    
    # Prepare metadata
    title = f"Lincoln Roasts: {headline[:50]}"
    description = f"""{script}

Subscribe for more Lincoln comedy!

Bitcoin: {BTC}
Product: {PRODUCT}

#AbrahamLincoln #Comedy #Roast #CurrentEvents #Standup #DarkComedy"""
    
    tags = [
        "Abraham Lincoln", "Comedy", "Roast", "Standup", "Dark Comedy",
        "Dave Chappelle", "George Carlin", "Richard Pryor", headline.replace(" ", "").replace("#", "")
    ]
    
    # Upload
    youtube_url = upload_to_youtube(video_path, title, description, tags)
    
    return {
        'video_path': str(video_path),
        'youtube_url': youtube_url,
        'headline': headline
    }

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    print(f"\n{'='*70}")
    print(f"PROFESSIONAL ABRAHAM LINCOLN VIDEO GENERATOR")
    print(f"{'='*70}")
    print(f"Generating {count} professional videos...")
    print(f"Quality: Exceeds FarFromWeakFFW channel")
    print()
    
    results = []
    for i in range(count):
        print(f"\n{'='*70}\nVIDEO {i+1}/{count}\n{'='*70}")
        result = generate_professional_video()
        if result:
            results.append(result)
            print(f"\n[SUCCESS] Video {i+1} complete!")
        else:
            print(f"\n[ERROR] Video {i+1} failed")
        
        if i < count - 1:
            time.sleep(2)
    
    print(f"\n{'='*70}")
    print(f"COMPLETE: {len(results)}/{count} videos generated")
    print(f"{'='*70}\n")
    
    for r in results:
        print(f"[OK] {r['headline'][:50]}: {r.get('youtube_url', 'Upload failed')}")

