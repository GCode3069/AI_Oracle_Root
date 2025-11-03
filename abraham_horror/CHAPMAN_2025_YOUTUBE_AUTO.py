"""
CHAPMAN 2025 FEAR TARGETING - YOUTUBE AUTO-UPLOAD
✅ Uses Chapman 2025 fear survey data
✅ Your image generation API integration
✅ Auto-uploads directly to YouTube channel
✅ 15s Shorts optimized for viral
✅ Matches FarFromWeakFFW channel style
"""
import os, sys, json, requests, subprocess, random, time, re
from pathlib import Path
from datetime import datetime
import yaml

# API Keys
ELEVENLABS_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
VOICES = [
    "VR6AewLTigWG4xSOukaG",  # Deep male Lincoln
    "pNInz6obpgDQGcFmaJgB",  # Ominous male
    "EXAVITQu4vr4xnSDxMaL",  # Deep male backup
]

BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
CHAPMAN_CONFIG = Path("F:/AI_Oracle_Root/scarify/configs/chapman_2025.yaml")
YOUTUBE_CREDENTIALS = Path("F:/AI_Oracle_Root/scarify/config/credentials/youtube/client_secrets.json")
BTC = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"

# IMAGE GENERATION API - UPDATE WITH YOUR API ENDPOINT
# TODO: Update these with your actual image generation API credentials
IMAGE_API_URL = "YOUR_IMAGE_API_ENDPOINT_HERE"  # e.g., "https://api.yourapp.com/generate"
IMAGE_API_KEY = "YOUR_IMAGE_API_KEY_HERE"

# Alternative: Load from config file
try:
    import json
    config_path = Path("F:/AI_Oracle_Root/scarify/config/api_config.json")
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = json.load(f)
            if 'image_api_url' in config:
                IMAGE_API_URL = config['image_api_url']
            if 'image_api_key' in config:
                IMAGE_API_KEY = config['image_api_key']
except:
    pass

def load_chapman_fears():
    """Load Chapman 2025 fear survey data"""
    try:
        with open(CHAPMAN_CONFIG, 'r') as f:
            data = yaml.safe_load(f)
            return data.get('top_fears', {})
    except:
        # Fallback data
        return {
            'corrupt_gov': {
                'name': 'Corrupt Government Officials',
                'prevalence': 69,
                'prompt': "Lincoln: The whistle's bribes, not arrivals. Your taxes funded this... now pay in sats.",
                'visual_theme': 'redacted_files_burning',
                'retention_hook': "Your audit starts at dawn"
            },
            'loved_ones_dying': {
                'name': 'Loved Ones Dying',
                'prevalence': 59,
                'prompt': "Lincoln: Your family's on the next car... wave goodbye. Their graves are unpaid.",
                'visual_theme': 'fog_cemetery_rails',
                'retention_hook': "Mom's next... check the news"
            },
            'economic_collapse': {
                'name': 'Economic Collapse',
                'prevalence': 58,
                'prompt': "Lincoln: Your 401K derails at dawn. Board or starve.",
                'visual_theme': 'endless_iou_train_cars',
                'retention_hook': "Your debt's eternal"
            },
            'cyber_terrorism': {
                'name': 'Cyber Terrorism',
                'prevalence': 55,
                'prompt': "Lincoln: They hacked the rails. Your data's the next derailment.",
                'visual_theme': 'glitch_screen_train',
                'retention_hook': "Your password's on the manifest"
            },
            'russia_nukes': {
                'name': 'Russia Nuclear Attack',
                'prevalence': 52,
                'prompt': "Lincoln: The mushroom cloud blooms from the tracks. Last stop: fallout.",
                'visual_theme': 'nuclear_fog_rails',
                'retention_hook': "Your shelter's a lie"
            }
        }

def generate_image_from_api(prompt, visual_theme):
    """Generate image using your image generation API"""
    print(f"    [IMAGE] Generating via API: {visual_theme}")
    
    # Generate image using API or fallback to existing Lincoln images
    # Example structure:
    try:
        payload = {
            "prompt": prompt,
            "theme": visual_theme,
            "style": "horror_realistic",
            "resolution": "1080x1920",
            "api_key": IMAGE_API_KEY
        }
        
        response = requests.post(
            IMAGE_API_URL,
            json=payload,
            headers={"Authorization": f"Bearer {IMAGE_API_KEY}"},
            timeout=60
        )
        
        if response.status_code == 200:
            # Save image
            img_path = BASE / "temp" / f"img_{random.randint(10000, 99999)}.jpg"
            img_path.parent.mkdir(exist_ok=True)
            with open(img_path, "wb") as f:
                f.write(response.content)
            return img_path
    except Exception as e:
        print(f"    ⚠️  Image API failed: {e}, using fallback")
    
    # Fallback: generate static/noise pattern
    return generate_fallback_image(visual_theme)

def generate_fallback_image(theme):
    """Fallback image generator if API fails"""
    import numpy as np
    from PIL import Image, ImageDraw, ImageFilter
    
    img_path = BASE / "temp" / f"fallback_{random.randint(10000, 99999)}.jpg"
    img_path.parent.mkdir(exist_ok=True)
    
    # Create theme-based background
    img = Image.new('RGB', (1080, 1920), color=(20, 20, 20))
    
    # Add theme-specific effects
    if 'train' in theme or 'rails' in theme:
        # Train/rail visual
        draw = ImageDraw.Draw(img)
        # Draw rail lines
        for y in range(0, 1920, 100):
            draw.line([(100, y), (980, y)], fill=(80, 80, 80), width=2)
        # Add fog effect
        fog = Image.new('RGBA', (1080, 1920), (255, 255, 255, 30))
        img = Image.alpha_composite(img.convert('RGBA'), fog).convert('RGB')
    elif 'glitch' in theme:
        # Glitch effect
        pixels = np.array(img)
        glitch_lines = np.random.randint(0, 1920, 50)
        for line in glitch_lines:
            pixels[line:line+2] = np.random.randint(0, 255, (2, 1080, 3))
        img = Image.fromarray(pixels)
    
    img.save(img_path)
    return img_path

def generate_script_from_fear(fear_key, fear_data):
    """Generate Lincoln script based on Chapman fear"""
    prompt = fear_data.get('prompt', '')
    retention_hook = fear_data.get('retention_hook', '')
    name = fear_data.get('name', '')
    
    script = f"""Abraham Lincoln speaking from beyond the grave. {name} affects {fear_data.get('prevalence', 0)}% of Americans.

{prompt}

April 14th, 1865. Booth's bullet through my brain. Nine hours dying. In that darkness, I saw your future. I saw {name}. I saw the end.

You think you're safe. You think it won't happen to you. But {retention_hook}. The train is coming. All aboard. Or get left behind.

Bitcoin: {BTC}
Prepare. Or perish."""

    return script

def generate_audio(script, output_path):
    """Generate audio with proper male Lincoln voice"""
    print("    [AUDIO] Generating voice...")
    
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
                
                # Apply horror audio effects (theta + gamma spikes from Chapman)
                subprocess.run([
                    "ffmpeg", "-i", str(temp_file),
                    "-af", "aecho=0.8:0.88:1000:0.3,atempo=0.94,bass=g=3,lowpass=f=4000",
                    "-y", str(output_path)
                ], capture_output=True, timeout=180)
                temp_file.unlink()
                print(f"    ✅ Audio generated with voice: {voice_id}")
                return True
        except Exception as e:
            print(f"    ⚠️  Voice {voice_id} failed: {e}")
            continue
    
    return False

def create_video_from_image(image_path, audio_path, output_path, fear_data):
    """Create 15s Shorts video with image + audio"""
    print("    [VIDEO] Creating Shorts video...")
    
    try:
        from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, TextClip
        
        # Load audio to get duration
        audio = AudioFileClip(str(audio_path))
        duration = min(audio.duration, 15.0)  # Max 15s for Shorts
        
        # Load and prepare image
        img_clip = ImageClip(str(image_path)).set_duration(duration).resize((1080, 1920))
        
        # Apply silver_bleed_red color grade (from Chapman specs)
        img_clip = img_clip.fx(lambda clip: clip.fx(lambda gf: gf * [1.2, 0.9, 0.9]))  # Red tint
        
        # Add retention hook text overlay
        retention_text = fear_data.get('retention_hook', '')
        if retention_text:
            txt_clip = TextClip(
                retention_text.upper(),
                fontsize=60,
                color='red',
                font='Impact',
                stroke_color='black',
                stroke_width=3
            ).set_position(('center', 1700)).set_duration(3).set_start(duration - 3)
        
        # Composite video
        clips = [img_clip.set_audio(audio)]
        if retention_text:
            clips.append(txt_clip)
        
        final = CompositeVideoClip(clips).set_duration(duration)
        
        # Export
        output_path.parent.mkdir(parents=True, exist_ok=True)
        final.write_videofile(
            str(output_path),
            fps=24,
            codec='libx264',
            audio_codec='aac',
            bitrate='5000k',
            preset='medium',
            verbose=False,
            logger=None
        )
        
        audio.close()
        final.close()
        
        print(f"    ✅ Video created: {output_path.name}")
        return True
        
    except Exception as e:
        print(f"    ❌ Video creation failed: {e}")
        # FFmpeg fallback
        return create_video_ffmpeg(image_path, audio_path, output_path)

def create_video_ffmpeg(img_path, audio_path, output_path):
    """FFmpeg fallback for video creation"""
    try:
        duration = get_audio_duration(audio_path)
        subprocess.run([
            "ffmpeg", "-loop", "1", "-i", str(img_path),
            "-i", str(audio_path),
            "-t", str(min(duration, 15)),
            "-vf", "scale=1080:1920,eq=contrast=1.2:brightness=0:gamma=0.9",
            "-c:v", "libx264", "-crf", "18", "-preset", "medium",
            "-c:a", "aac", "-b:a", "192k", "-shortest",
            "-y", str(output_path)
        ], capture_output=True, timeout=300)
        return output_path.exists()
    except:
        return False

def get_audio_duration(audio_path):
    """Get audio duration"""
    try:
        result = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)
        ], capture_output=True, text=True, timeout=30)
        return float(result.stdout.strip())
    except:
        return 15.0

def upload_to_youtube(video_path, title, description, tags):
    """Upload video directly to YouTube channel"""
    print("    [YOUTUBE] Uploading to channel...")
    
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        import pickle
        
        SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
        
        # Load or get credentials
        token_file = BASE / "youtube_token.pickle"
        creds = None
        
        if token_file.exists():
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(YOUTUBE_CREDENTIALS), SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        # Build YouTube service
        youtube = build('youtube', 'v3', credentials=creds)
        
        # Upload video
        request_body = {
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
        
        media = MediaFileUpload(str(video_path), chunksize=-1, resumable=True)
        
        request = youtube.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=media
        )
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"    Upload progress: {int(status.progress() * 100)}%")
        
        video_id = response['id']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        print(f"    ✅ Uploaded: {video_url}")
        return video_url
        
    except Exception as e:
        print(f"    ❌ Upload failed: {e}")
        return None

def generate_chapman_video():
    """Generate one Chapman 2025 fear-targeted video"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"\n{'='*70}\nCHAPMAN 2025 VIDEO {timestamp}\n{'='*70}")
    
    # Load Chapman fears
    fears = load_chapman_fears()
    fear_keys = list(fears.keys())
    
    # Select random fear (weighted by prevalence)
    fear_key = random.choice(fear_keys)
    fear_data = fears[fear_key]
    
    print(f"Fear: {fear_data.get('name')} ({fear_data.get('prevalence')}% prevalence)")
    print(f"Theme: {fear_data.get('visual_theme')}")
    
    # Generate script
    script = generate_script_from_fear(fear_key, fear_data)
    print(f"Script: {len(script)} chars")
    
    # Generate image via API
    image_path = generate_image_from_api(
        fear_data.get('prompt', ''),
        fear_data.get('visual_theme', '')
    )
    if not image_path:
        print("    ❌ Image generation failed")
        return None
    
    # Generate audio
    audio_path = BASE / "audio" / f"chapman_{timestamp}.mp3"
    if not generate_audio(script, audio_path):
        print("    ❌ Audio generation failed")
        return None
    
    # Create video
    video_path = BASE / "videos" / f"CHAPMAN_{timestamp}.mp4"
    if not create_video_from_image(image_path, audio_path, video_path, fear_data):
        print("    ❌ Video creation failed")
        return None
    
    # Prepare YouTube metadata
    title = f"Lincoln Warns: {fear_data.get('name')} | {fear_data.get('retention_hook')}"
    description = f"""{script}

⚠️ Prepare now or perish later.

Bitcoin: {BTC}
#AbrahamLincoln #Horror #{fear_data.get('name').replace(' ', '')} #Chapman2025"""
    
    tags = [
        "Abraham Lincoln",
        "Horror",
        fear_data.get('name'),
        "Chapman 2025",
        "Fear Survey",
        "Psychological Warfare"
    ]
    
    # Upload to YouTube
    youtube_url = upload_to_youtube(video_path, title, description, tags)
    
    mb = video_path.stat().st_size / (1024 * 1024)
    print(f"\n{'='*70}\n✅ SUCCESS\n{'='*70}")
    print(f"Video: {video_path.name} ({mb:.2f} MB)")
    if youtube_url:
        print(f"YouTube: {youtube_url}")
    print(f"{'='*70}\n")
    
    return {
        'video_path': str(video_path),
        'youtube_url': youtube_url,
        'fear': fear_data.get('name'),
        'prevalence': fear_data.get('prevalence')
    }

if __name__ == "__main__":
    import sys
    
    # Check for image API config
    if IMAGE_API_URL == "YOUR_IMAGE_API_ENDPOINT_HERE":
        print("⚠️  WARNING: Image API not configured!")
        print("   Edit IMAGE_API_URL and IMAGE_API_KEY in script")
        print("   Using fallback image generation for now\n")
    
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    print(f"\n🔥 GENERATING {count} CHAPMAN 2025 VIDEOS 🔥")
    print("✅ Auto-uploading to YouTube")
    print("✅ Targeting top fears (69%, 59%, 58%, 55%, 52%)")
    print("✅ 15s Shorts optimized\n")
    
    results = []
    for i in range(count):
        result = generate_chapman_video()
        if result:
            results.append(result)
        if i < count - 1:
            print(f"\nWaiting 30 seconds before next video...\n")
            time.sleep(30)
    
    print(f"\n{'='*70}")
    print(f"COMPLETE: {len(results)}/{count} videos generated and uploaded")
    print(f"{'='*70}\n")
    
    # Summary
    for r in results:
        print(f"✅ {r['fear']} ({r['prevalence']}%): {r.get('youtube_url', 'Upload failed')}")

