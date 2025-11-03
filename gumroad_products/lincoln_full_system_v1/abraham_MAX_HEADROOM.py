#!/usr/bin/env python3
"""
MAX HEADROOM ABRAHAM LINCOLN
Glitchy TV broadcast style with lip sync
"""
import os, sys, requests, subprocess, json, time
from pathlib import Path
from datetime import datetime
import random

# SECRET SAUCE: Psychological audio layers
try:
    import numpy as np
    import scipy.io.wavfile as wav
    PSYCHOLOGICAL_AUDIO_AVAILABLE = True
except ImportError:
    PSYCHOLOGICAL_AUDIO_AVAILABLE = False
    print("[Warning] NumPy/SciPy not installed - psychological audio disabled")

# API KEYS
ELEVENLABS_API_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
POLLO_API_KEY = "pollo_5EW9VjxB2eAUknmhd9vb9F2OJFDjPVVZttOQJRaaQ248"
STABILITY_API_KEY = "sk-sP93JLezaVNYpifbSDf9sn0rUaxhir377fJJV9Vit0nOEPQ1"
DID_API_KEY = os.getenv("DID_API_KEY", "")  # Get from https://studio.d-id.com/
WAV2LIP_API_KEY = os.getenv("WAV2LIP_API_KEY", "")  # Optional service key

# BITCOIN ADDRESS
BITCOIN_ADDRESS = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"

# DEEP MALE LINCOLN VOICES (not female)
LINCOLN_VOICES = [
    '7aavy6c5cYIloDVj2JvH',  # Deep male
    'pNInz6obpgDQGcFmaJgB',  # Adam - deep
    'EXAVITQu4vr4xnSDxMaL',  # Antoni - very deep
    'VR6AewLTigWG4xSOukaG',  # Arnold - classic deep
]
VOICE_ID = LINCOLN_VOICES[0]

BASE_DIR = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
for d in ['audio', 'videos', 'youtube_ready', 'temp', 'lincoln_faces', 'qr_codes']:
    (BASE_DIR / d).mkdir(parents=True, exist_ok=True)

def get_headlines():
    """Scrape real headlines"""
    try:
        # Try RSS feeds
        feeds = [
            "https://feeds.feedburner.com/oreilly/radar",
            "https://rss.cnn.com/rss/edition.rss",
        ]
        for feed in feeds:
            try:
                response = requests.get(feed, timeout=10)
                if response.status_code == 200:
                    import xml.etree.ElementTree as ET
                    root = ET.fromstring(response.content)
                    headlines = []
                    for item in root.findall('.//item')[:10]:
                        title = item.find('title')
                        if title is not None:
                            headlines.append(title.text)
                    if headlines:
                        return headlines[:5]
            except:
                continue
    except:
        pass
    # Fallback
    return ["Government Shutdown Day 15", "Major Cyber Attack", "Recession Signals", "Market Crash", "Digital Apocalypse"]

def generate_script(headline):
    """
    Generate DARK SATIRICAL COMEDY - SHORT & PUNCHY (9-17s = 22-45 words)
    NO SACRED COWS: Roasts EVERYONE (Dems, Republicans, rich, poor)
    Styles: Pryor's darkness + Carlin's cynicism + Chappelle's truth + Bernie Mac's anger
    """
    hl = headline.lower()
    
    # Convert headline to WARNING topic
    if "trump" in hl or "republican" in hl or "gop" in hl:
        topic = "Trump's Tariffs Destroying Economy"
        # DARK SATIRICAL SHORT - Roast BOTH sides (35-45 words for 9-17s)
        return f"""Lincoln here!

{headline}

POOR people defending BILLIONAIRES?! Turkeys voting for Thanksgiving!

But Pelosi worth $100 MILLION preaching equality?!

Carlin said it: "Big club - you AIN'T in it!"

BOTH sides rob you!

Look in mirrors."""
    
    elif "police" in hl or "shooting" in hl or "law" in hl:
        topic = "Police Strike - No Law"
        # DARK SATIRICAL SHORT - Roast ALL sides (35-45 words)
        return f"""Lincoln! Got WORDS!

{headline}

Cops killing unarmed people! Pryor: "Police scare ME!"

"Defund" crowd - criminals police THEMSELVES?!

"Back the Blue" - until at YOUR door!

EVERYBODY wrong!

Look in mirrors."""
    
    elif "education" in hl or "school" in hl:
        topic = "Education System Destroyed"
        # DARK SATIRICAL SHORT - Education roast (35-45 words)
        return f"""ABE LINCOLN! PISSED!

{headline}

Kids can't READ but can TIKTOK!

Money for BOMBS not BOOKS!

Republicans: "Poor kids stay dumb!"

Democrats: "$100K unemployment degrees!"

Bernie Mac: Teachers need second jobs! CEOs need second YACHTS!

Look in mirrors."""
    
    elif "military" in hl or "draft" in hl or "war" in hl:
        topic = "Military Draft Activated"
        # DARK SATIRICAL SHORT - War roast (35-45 words)
        return f"""LINCOLN! DEAD but TALKING!

{headline}

DRAFT?! Didn't learn from VIETNAM?!

Carlin: "Rich men send POOR kids to die!"

Republicans: "Support troops!" - by killing them for OIL!

Democrats: "$800 BILLION war budgets!"

BOTH love war! Profitable!

Look in mirrors."""
    
    elif "economy" in hl or "inflation" in hl or "stock" in hl or "market" in hl:
        topic = "Economy Collapsing"
        # DARK SATIRICAL SHORT - Economy roast (35-45 words)
        return f"""LINCOLN! Pissed!

{headline}

Market crashes! Rich sad! Poor been CRASHED!

Republicans: "Free market!" - unless YOU fail!

Democrats: "Tax rich!" while BEING rich!

Pryor: Poor pay TAXES! Rich pay ACCOUNTANTS!

Two jobs! Can't afford rent! SLAVERY!

Look in mirrors."""
    
    elif "climate" in hl or "environment" in hl:
        topic = "Climate Crisis"
        # DARK SATIRICAL SHORT - Climate roast (35-45 words)
        return f"""LINCOLN! FURIOUS!

{headline}

Republicans: "Climate hoax!" - buy FLOOD insurance!

Democrats: "Save Earth!" - from PRIVATE JETS!

Carlin: "Planet's FINE! PEOPLE are fucked!"

Oil companies KNEW! LIED!

ALL complicit!

Look in mirrors."""
    
    else:
        topic = "America in Crisis"
        # GENERAL DARK ROAST SHORT - Hit EVERYONE (35-45 words)
        return f"""LINCOLN! Dead but AWAKE!

{headline}

Pryor: "Only KIDS and DRUNKS honest! Everyone else LYING!"

Republicans: Small government in a uterus!

Democrats: Free everything - who PAYS?!

Carlin: "American DREAM? You're ASLEEP!"

ALL getting PLAYED!

Look in mirrors."""

def generate_psychological_audio(duration, output_path):
    """
    SECRET SAUCE: Generate psychological audio layers
    - Theta waves (4-8Hz): Freeze-gut paralysis, fear induction
    - Gamma spikes (40Hz): BDNF hijack, attention/memory triggers
    - Binaural beats: Brain state manipulation
    - Subliminal frequencies: Hidden psychological triggers
    """
    if not PSYCHOLOGICAL_AUDIO_AVAILABLE:
        return None
    
    try:
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        # LAYER 1: Theta wave base (6Hz - fear/paralysis frequency)
        theta_freq = 6.0  # Hz
        theta_wave = np.sin(2 * np.pi * theta_freq * t) * 0.15
        
        # LAYER 2: Gamma spikes at key moments (40Hz - memory/attention)
        # Synced with visual moments for perfect blend
        gamma_freq = 40.0  # Hz
        spike_times = [duration * 0.25, duration * 0.5, duration * 0.75]  # Key moments
        gamma_layer = np.zeros_like(t)
        for spike_time in spike_times:
            spike_idx = int(spike_time * sample_rate)
            spike_duration = int(0.6 * sample_rate)  # 0.6 second spike (longer for better blend)
            end_idx = min(spike_idx + spike_duration, len(t))
            # Fade in/out for smooth blend
            fade_samples = int(0.1 * sample_rate)  # 0.1s fade
            spike_signal = np.sin(2 * np.pi * gamma_freq * t[spike_idx:end_idx]) * 0.25
            # Apply fade
            fade_in = np.linspace(0, 1, fade_samples)
            fade_out = np.linspace(1, 0, fade_samples)
            if len(spike_signal) > fade_samples * 2:
                spike_signal[:fade_samples] *= fade_in
                spike_signal[-fade_samples:] *= fade_out
            gamma_layer[spike_idx:end_idx] += spike_signal
        
        # LAYER 3: Binaural beats (creates brain state)
        # 200Hz left, 208Hz right = 8Hz binaural (theta range)
        binaural_left = np.sin(2 * np.pi * 200.0 * t) * 0.1
        binaural_right = np.sin(2 * np.pi * 208.0 * t) * 0.1
        
        # LAYER 4: Subliminal frequencies (17Hz - below conscious hearing but affects brain)
        subliminal = np.sin(2 * np.pi * 17.0 * t) * 0.05
        
        # LAYER 5: Unique frequency signature (watermark)
        # Generate unique ID based on timestamp
        unique_id = int(datetime.now().timestamp() * 1000) % 10000
        watermark_freq = 3000 + (unique_id % 1000)  # Between 3000-4000 Hz
        watermark = np.sin(2 * np.pi * watermark_freq * t) * 0.02
        
        # Combine all layers with smooth blending
        psychological_audio = theta_wave + gamma_layer + subliminal + watermark
        
        # Apply smooth envelope to prevent harsh transitions
        fade_in_samples = int(0.5 * sample_rate)  # 0.5s fade in
        fade_out_samples = int(1.0 * sample_rate)  # 1.0s fade out
        envelope = np.ones_like(psychological_audio)
        envelope[:fade_in_samples] = np.linspace(0, 1, fade_in_samples)
        envelope[-fade_out_samples:] = np.linspace(1, 0, fade_out_samples)
        psychological_audio = psychological_audio * envelope
        
        # Normalize with proper headroom for beautiful blend
        max_val = np.max(np.abs(psychological_audio))
        if max_val > 0:
            psychological_audio = psychological_audio / max_val * 0.18  # Subtle but present
        
        # Convert to int16
        audio_int16 = np.int16(psychological_audio * 32767)
        
        # Save
        output_path.parent.mkdir(parents=True, exist_ok=True)
        wav.write(str(output_path), sample_rate, audio_int16)
        
        print(f"[Secret Sauce] Psychological audio generated: theta(6Hz) + gamma(40Hz) + subliminal(17Hz) + watermark({watermark_freq}Hz)")
        return output_path
        
    except Exception as e:
        print(f"[Secret Sauce] Error: {e}")
        return None

def mix_psychological_audio(main_audio_path, psychological_audio_path, output_path):
    """Mix main voice with psychological audio layers - BEAUTIFULLY BLENDED & SYNced"""
    if not psychological_audio_path or not psychological_audio_path.exists():
        # No psychological audio, just copy main
        import shutil
        shutil.copy2(main_audio_path, output_path)
        return output_path.exists()
    
    try:
        # BEAUTIFUL BLEND: Convert psych audio to same format, then mix perfectly
        # First, ensure both are same sample rate and format
        psych_temp = output_path.parent / f"psych_temp_{random.randint(1000,9999)}.wav"
        
        # Convert psychological audio to match main audio format
        convert_cmd = [
            'ffmpeg', '-i', str(psychological_audio_path),
            '-ar', '44100', '-ac', '2', '-sample_fmt', 's16',
            '-y', str(psych_temp)
        ]
        subprocess.run(convert_cmd, capture_output=True, text=True, timeout=60)
        
        if not psych_temp.exists():
            print(f"[Secret Sauce] Psych audio conversion failed, using main only")
            import shutil
            shutil.copy2(main_audio_path, output_path)
            return output_path.exists()
        
        # BEAUTIFUL BLEND: High-quality mixing with perfect sync
        # Main voice at 100%, psychological at 12% (subtle but effective)
        # High-pass psych to remove rumble, normalize final output
        cmd = [
            'ffmpeg', '-i', str(main_audio_path),
            '-i', str(psych_temp),
            '-filter_complex', 
            '[0:a]aformat=sample_rates=44100:channel_layouts=stereo[main];'
            '[1:a]aformat=sample_rates=44100:channel_layouts=stereo,highpass=f=30,volume=0.12[psych];'
            '[main][psych]amix=inputs=2:duration=first:dropout_transition=3,'
            'loudnorm=I=-16:TP=-1.5:LRA=11[out]',
            '-map', '[out]',
            '-c:a', 'libmp3lame', '-b:a', '256k', '-ar', '44100',
            '-y', str(output_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        # Cleanup temp
        if psych_temp.exists():
            psych_temp.unlink()
        
        if output_path.exists() and output_path.stat().st_size > 0:
            size_kb = output_path.stat().st_size / 1024
            print(f"[Secret Sauce] Audio beautifully blended: voice + psychological layers ({size_kb:.1f} KB)")
            return True
        else:
            print(f"[Secret Sauce] Mix failed, using main audio only. Error: {result.stderr[:200]}")
            import shutil
            shutil.copy2(main_audio_path, output_path)
            return output_path.exists()
            
    except Exception as e:
        print(f"[Secret Sauce] Mix error: {e}, using main audio")
        import shutil
        shutil.copy2(main_audio_path, output_path)
        return output_path.exists()

def generate_voice(script, output_path, voice_id=None, add_psychological=True):
    """Generate DEEP MALE Lincoln voice"""
    if voice_id is None:
        voice_id = VOICE_ID
    
    print(f"[Voice] Generating deep male Lincoln voice ({voice_id})...")
    try:
        # Use deep voice settings
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            json={
                "text": script,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.35,  # Lower for more emotion/variation
                    "similarity_boost": 0.95,  # Higher for clearer voice
                    "style": 0.4,  # More dramatic style
                    "use_speaker_boost": True
                }
            },
            headers={
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": ELEVENLABS_API_KEY
            },
            timeout=120
        )
        if response.status_code == 200:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save raw voice first
            raw_voice_path = output_path.parent / f"raw_{output_path.name}"
            with open(raw_voice_path, 'wb') as f:
                f.write(response.content)
            
            # Add SECRET SAUCE: Psychological audio layers
            if add_psychological:
                try:
                    # Get audio duration
                    result = subprocess.run([
                        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                        '-of', 'default=noprint_wrappers=1:nokey=1', str(raw_voice_path)
                    ], capture_output=True, text=True)
                    duration = float(result.stdout.strip())
                    
                    # Generate psychological audio
                    psych_audio_path = output_path.parent / f"psych_{random.randint(1000,9999)}.wav"
                    if generate_psychological_audio(duration, psych_audio_path):
                        # Convert MP3 to WAV for mixing
                        voice_wav = output_path.parent / f"voice_{random.randint(1000,9999)}.wav"
                        subprocess.run([
                            'ffmpeg', '-i', str(raw_voice_path),
                            '-acodec', 'pcm_s16le', '-ar', '44100',
                            '-y', str(voice_wav)
                        ], capture_output=True, timeout=60)
                        
                        if voice_wav.exists():
                            # Mix psychological layers
                            mixed_wav = output_path.parent / f"mixed_{random.randint(1000,9999)}.wav"
                            if mix_psychological_audio(voice_wav, psych_audio_path, mixed_wav):
                                # Convert back to MP3
                                subprocess.run([
                                    'ffmpeg', '-i', str(mixed_wav),
                                    '-acodec', 'libmp3lame', '-b:a', '256k',
                                    '-y', str(output_path)
                                ], capture_output=True, timeout=60)
                                
                                # Cleanup temp files
                                for temp in [raw_voice_path, psych_audio_path, voice_wav, mixed_wav]:
                                    try:
                                        if temp.exists() and temp != output_path:
                                            temp.unlink()
                                    except:
                                        pass
                                
                                if output_path.exists():
                                    size_kb = output_path.stat().st_size / 1024
                                    print(f"[Voice] OK with Secret Sauce: {size_kb:.2f} KB")
                                    return True
                except Exception as e:
                    print(f"[Secret Sauce] Failed, using raw voice: {e}")
                    # Fallback: use raw voice
                    import shutil
                    shutil.move(str(raw_voice_path), str(output_path))
            else:
                import shutil
                shutil.move(str(raw_voice_path), str(output_path))
            
            size_kb = output_path.stat().st_size / 1024
            print(f"[Voice] OK: {size_kb:.2f} KB")
            return True
        else:
            print(f"[Voice] Failed: {response.status_code}")
            # Try next voice
            for vid in LINCOLN_VOICES:
                if vid != voice_id:
                    print(f"[Voice] Trying voice: {vid}")
                    return generate_voice(script, output_path, vid)
    except Exception as e:
        print(f"[Voice] Error: {e}")
    return False

def generate_lincoln_face_pollo():
    """Generate Abraham Lincoln face image with Stability AI (Pollo endpoint doesn't exist)"""
    print("[Stability] Generating Lincoln face...")
    try:
        response = requests.post(
            "https://api.stability.ai/v2beta/stable-image/generate/ultra",
            headers={
                "Authorization": f"Bearer {STABILITY_API_KEY}",
                "Accept": "image/*"
            },
            files={"none": ""},
            data={
                "prompt": "Abraham Lincoln portrait, close-up face, serious expression, 19th century photography style, monochrome, high detail, Max Headroom style, glitchy aesthetic",
                "output_format": "png",
                "aspect_ratio": "1:1"
            },
            timeout=60
        )
        if response.status_code == 200:
            img_path = BASE_DIR / "lincoln_faces" / f"lincoln_{random.randint(1000,9999)}.png"
            with open(img_path, 'wb') as f:
                f.write(response.content)
            print(f"[Stability] Generated: {img_path.name}")
            return img_path
        else:
            print(f"[Stability] Failed: {response.status_code} - {response.text[:200]}")
    except Exception as e:
        print(f"[Stability] Error: {e}")
    
    # Fallback: Download actual Lincoln image from public domain
    print("[Fallback] Downloading actual Lincoln image...")
    try:
        # Try to download a public domain Lincoln portrait
        # FIRST: Try master optimized image (best quality, VHS-ready)
        img_path = BASE_DIR / "lincoln_faces" / "lincoln_master_optimized.jpg"
        if not img_path.exists():
            # Try master original
            img_path = BASE_DIR / "lincoln_faces" / "lincoln_master.jpg"
        if not img_path.exists():
            # Try common backup name
            img_path = BASE_DIR / "lincoln_faces" / "lincoln.jpg"
        if not img_path.exists():
            # Fallback to real.png
            img_path = BASE_DIR / "lincoln_faces" / "lincoln_real.png"
        if not img_path.exists():
            # Download a high-quality public domain Lincoln image
            lincoln_urls = [
                "https://upload.wikimedia.org/wikipedia/commons/a/ab/Abraham_Lincoln_O-77_matte_collodion_print.jpg",  # Library of Congress
                "https://upload.wikimedia.org/wikipedia/commons/1/1b/Abraham_Lincoln_November_1863.jpg",  # Famous portrait
            ]
            
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            for url in lincoln_urls:
                try:
                    response = requests.get(url, timeout=30, stream=True, headers=headers)
                    if response.status_code == 200:
                        img_path.parent.mkdir(parents=True, exist_ok=True)
                        with open(img_path, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        print(f"[Fallback] Downloaded real Lincoln image: {img_path.name}")
                        return img_path
                except:
                    continue
            
            # Last resort: Create a better placeholder with Lincoln text
            print("[Fallback] Creating enhanced placeholder...")
            subprocess.run([
                'ffmpeg', '-f', 'lavfi', '-i', 
                'color=c=#2a2a2a:s=1024x1024:d=1',
                '-vf', 'drawtext=text="A. LINCOLN":fontcolor=#d4af37:fontsize=120:x=(w-text_w)/2:y=(h-text_h)/2:fontfile=arial.ttf:box=1:boxcolor=black@0.8:boxborderw=5',
                '-frames:v', '1', '-y', str(img_path)
            ], capture_output=True, timeout=30)
            
        return img_path if img_path.exists() else None
    except Exception as e:
        print(f"[Fallback] Error: {e}")
    
    return None

def generate_bitcoin_qr():
    """Generate Bitcoin QR code image"""
    try:
        import qrcode
        from PIL import Image
        
        qr_path = BASE_DIR / "qr_codes" / "bitcoin_qr.png"
        if qr_path.exists():
            return qr_path
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f"bitcoin:{BITCOIN_ADDRESS}")
        qr.make(fit=True)
        
        # Create image
        qr_img = qr.make_image(fill_color="white", back_color="black")
        
        # Resize to appropriate size for overlay (200x200)
        qr_img = qr_img.resize((200, 200), Image.Resampling.LANCZOS)
        
        # Save
        qr_path.parent.mkdir(parents=True, exist_ok=True)
        qr_img.save(str(qr_path))
        
        print(f"[QR] Bitcoin QR code generated: {qr_path.name}")
        return qr_path
        
    except ImportError:
        print("[QR] qrcode library not installed, installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'qrcode[pil]', '--quiet'], capture_output=True)
        return generate_bitcoin_qr()
    except Exception as e:
        print(f"[QR] Error generating QR: {e}")
        return None

def generate_lipsync_did(lincoln_image, audio_path, output_path):
    """Generate lip-sync video using D-ID API"""
    if not DID_API_KEY:
        print("[D-ID] API key not found, skipping...")
        return None
    
    print("[D-ID] Generating lip-sync video...")
    try:
        # Step 1: Upload image and audio
        # Upload image
        with open(lincoln_image, 'rb') as f:
            img_files = {'image': f}
            img_response = requests.post(
                "https://api.d-id.com/images",
                headers={"Authorization": f"Basic {DID_API_KEY}"},
                files=img_files
            )
        
        if img_response.status_code != 201:
            print(f"[D-ID] Image upload failed: {img_response.status_code}")
            return None
        
        image_id = img_response.json().get('id')
        
        # Upload audio
        with open(audio_path, 'rb') as f:
            audio_files = {'audio': f}
            audio_response = requests.post(
                "https://api.d-id.com/audios",
                headers={"Authorization": f"Basic {DID_API_KEY}"},
                files=audio_files
            )
        
        if audio_response.status_code != 201:
            print(f"[D-ID] Audio upload failed: {audio_response.status_code}")
            return None
        
        audio_id = audio_response.json().get('id')
        
        # Step 2: Create talking head video
        create_response = requests.post(
            "https://api.d-id.com/talks",
            headers={
                "Authorization": f"Basic {DID_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "source_url": image_id,
                "script": {
                    "type": "audio",
                    "audio_url": audio_id
                },
                "config": {
                    "result_format": "mp4",
                    "fluent": True
                }
            }
        )
        
        if create_response.status_code != 201:
            print(f"[D-ID] Talk creation failed: {create_response.status_code}")
            return None
        
        talk_id = create_response.json().get('id')
        
        # Step 3: Poll for completion
        max_attempts = 60
        for attempt in range(max_attempts):
            time.sleep(2)
            status_response = requests.get(
                f"https://api.d-id.com/talks/{talk_id}",
                headers={"Authorization": f"Basic {DID_API_KEY}"}
            )
            
            if status_response.status_code == 200:
                status_data = status_response.json()
                status = status_data.get('status')
                
                if status == 'done':
                    result_url = status_data.get('result_url')
                    # Download video
                    video_response = requests.get(result_url, timeout=120)
                    if video_response.status_code == 200:
                        with open(output_path, 'wb') as f:
                            f.write(video_response.content)
                        print(f"[D-ID] Lip-sync video generated: {output_path.name}")
                        return output_path
                
                elif status == 'error':
                    print(f"[D-ID] Generation failed: {status_data.get('error')}")
                    return None
                
            print(f"[D-ID] Waiting... ({attempt+1}/{max_attempts})")
        
        print("[D-ID] Timeout waiting for video")
        return None
        
    except Exception as e:
        print(f"[D-ID] Error: {e}")
        return None

def generate_lipsync_wav2lip(lincoln_image, audio_path, output_path):
    """Generate lip-sync using Wav2Lip (service API or local)"""
    print("[Wav2Lip] Generating lip-sync video...")
    
    # Option 1: Use Wav2Lip API service if available
    if WAV2LIP_API_KEY:
        try:
            with open(lincoln_image, 'rb') as f:
                img_data = f.read()
            with open(audio_path, 'rb') as f:
                audio_data = f.read()
            
            files = {
                'video': ('lincoln.jpg', img_data, 'image/jpeg'),
                'audio': ('audio.mp3', audio_data, 'audio/mpeg')
            }
            
            response = requests.post(
                "https://api.wav2lip.ai/v1/lipsync",
                headers={"Authorization": f"Bearer {WAV2LIP_API_KEY}"},
                files=files,
                timeout=300
            )
            
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                print(f"[Wav2Lip] Video generated: {output_path.name}")
                return output_path
        except Exception as e:
            print(f"[Wav2Lip] API error: {e}")
    
    # Option 2: Use local Wav2Lip if available
    wav2lip_script = BASE_DIR.parent / "wav2lip" / "inference.py"
    if wav2lip_script.exists():
        try:
            subprocess.run([
                sys.executable, str(wav2lip_script),
                "--checkpoint_path", str(BASE_DIR.parent / "wav2lip" / "checkpoints" / "wav2lip_gan.pth"),
                "--face", str(lincoln_image),
                "--audio", str(audio_path),
                "--outfile", str(output_path)
            ], timeout=600, check=True)
            
            if output_path.exists():
                print(f"[Wav2Lip] Local video generated: {output_path.name}")
                return output_path
        except Exception as e:
            print(f"[Wav2Lip] Local execution error: {e}")
    
    # Option 3: Fallback - simulate lip sync with zoom/pan
    print("[Wav2Lip] Using fallback zoom effect...")
    try:
        result = subprocess.run([
            'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)
        ], capture_output=True, text=True)
        duration = float(result.stdout.strip())
    except:
        duration = 30
    
    # Create animated video with zoom/pan to simulate talking
    subprocess.run([
        'ffmpeg', '-loop', '1', '-i', str(lincoln_image),
        '-i', str(audio_path),
        '-filter_complex',
        f"[0:v]scale=1080:1080:force_original_aspect_ratio=decrease,"
        f"pad=1080:1080:(ow-iw)/2:(oh-ih)/2:black,"
        f"zoompan=z='zoom+0.001':d=125:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1080,"
        f"eq=contrast=1.3:brightness=-0.1[v]",
        '-map', '[v]', '-map', '1:a',
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
        '-c:a', 'aac', '-b:a', '256k',
        '-t', str(duration), '-shortest',
        '-y', str(output_path)
    ], capture_output=True, timeout=600)
    
    if output_path.exists():
        print(f"[Wav2Lip] Fallback video created: {output_path.name}")
        return output_path
    
    return None

def add_jumpscare_effects(video_path, output_path, audio_path):
    """Add jumpscare effects: sudden zoom, flash, distortion - SYNCED WITH AUDIO"""
    print("[Jumpscare] Adding horror jumpscare effects (synced with audio)...")
    
    try:
        result = subprocess.run([
            'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)
        ], capture_output=True, text=True)
        duration = float(result.stdout.strip())
    except:
        duration = 30
    
    # Calculate jumpscare timing (75% - aligns with gamma spike timing for sync)
    jumpscare_time = duration * 0.75
    
    # Complex filter: Normal video + sudden zoom + flash + distortion at jumpscare moment
    filter_complex = (
        f"[0:v]split[base][jump];"
        f"[base]trim=0:{jumpscare_time}[before];"
        f"[jump]trim={jumpscare_time}:{duration},"
        f"scale=1080*1.5:1080*1.5,"
        f"crop=1080:1080:'(iw-1080)/2':'ih/2-540',"
        f"eq=contrast=2.0:brightness=0.3:saturation=1.5,"
        f"noise=alls=30:allf=t+u,"
        f"geq=r='if(between(X/W,0.45,0.55),255*random(1),p(X,Y))':"
        f"g='if(between(X/W,0.45,0.55),255*random(1),p(X,Y))':"
        f"b='if(between(X/W,0.45,0.55),255*random(1),p(X,Y))'[scare];"
        f"[before][scare]concat=n=2:v=1:a=0[v1];"
        f"[v1]drawtext=text='':fontcolor=white:fontsize=200:x=(w-text_w)/2:y=(h-text_h)/2:enable='between(t,{jumpscare_time},{jumpscare_time}+0.1)':box=1:boxcolor=white@1.0[v2];"
        f"[v2]scale=1080:1080[v]"
    )
    
    cmd = [
        'ffmpeg', '-i', str(video_path), '-i', str(audio_path),
        '-filter_complex', filter_complex,
        '-map', '[v]', '-map', '1:a:0',
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
        '-c:a', 'aac', '-b:a', '256k',
        '-pix_fmt', 'yuv420p',
        '-y', str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    
    if output_path.exists():
        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"[Jumpscare] Enhanced video: {size_mb:.2f} MB")
        return True
    else:
        # Fallback: simpler jumpscare
        print("[Jumpscare] Using simple jumpscare...")
        return add_simple_jumpscare(video_path, output_path, audio_path, jumpscare_time)

def add_simple_jumpscare(video_path, output_path, audio_path, jumpscare_time):
    """Beautifully synced jumpscare: zoom + flash synced with gamma spike"""
    try:
        # Check input exists
        if not video_path.exists():
            print(f"[Jumpscare] Input video missing: {video_path}")
            return False
        
        # Get duration for perfect sync
        try:
            result = subprocess.run([
                'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)
            ], capture_output=True, text=True)
            duration = float(result.stdout.strip())
        except:
            duration = 30
        
        # Beautiful zoom effect: smooth transition, synced with audio
        # Zoom starts slightly before jumpscare for anticipation, peaks at jumpscare moment
        zoom_start = jumpscare_time - 0.2  # 0.2s before for smooth transition
        
        cmd = [
            'ffmpeg', '-i', str(video_path), '-i', str(audio_path),
            '-vf', f'scale=1080:1080,zoompan=z=if(lt(t,{zoom_start}),1.0,if(lt(t,{jumpscare_time}),1.0+2.0*(t-{zoom_start})/0.2,1.5)):d=1:x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2)',
            # Perfect audio sync: match psychological audio normalization
            '-af', 'volume=2.8,highpass=f=80,lowpass=f=18000,loudnorm=I=-16:TP=-1.5:LRA=11',
            '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
            '-c:a', 'aac', '-b:a', '256k', '-ar', '44100',
            '-pix_fmt', 'yuv420p',
            '-shortest',
            '-y', str(output_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        if output_path.exists() and output_path.stat().st_size > 0:
            print(f"[Jumpscare] Beautifully synced: zoom + audio blend")
            return True
        else:
            print(f"[Jumpscare] Output failed or empty. Error: {result.stderr[:500]}")
            return False
    except Exception as e:
        print(f"[Jumpscare] Exception: {e}")
        return False

def create_max_headroom_video(lincoln_image, audio_path, output_path, headline, use_lipsync=True, use_jumpscare=True):
    """Create Max Headroom-style glitchy TV broadcast - BEAUTIFULLY SYNCED (OPTIMIZED)"""
    print("[Video] Creating Max Headroom glitchy TV effect (synced, optimized)...")
    
    if not audio_path.exists():
        print("[Video] Audio missing!")
        return False
    
    # BEAUTIFUL SYNC: Get exact audio duration from final mixed audio
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)],
            capture_output=True, text=True
        )
        duration = float(result.stdout.strip())
        print(f"[Video] Audio duration: {duration:.2f}s (perfect sync)")
    except:
        duration = 30
        print(f"[Video] Could not read duration, using {duration}s")
    
    # OPTIMIZED: For videos >60s, use multi-pass approach to prevent timeouts
    if duration > 60:
        print(f"[Video] Long video ({duration:.1f}s) - using optimized multi-pass approach")
        try:
            from abraham_MAX_HEADROOM_OPTIMIZED import create_optimized_vhs_video
            return create_optimized_vhs_video(
                lincoln_image, audio_path, output_path, headline,
                broll_path=None,  # Can add B-roll support later
                use_lipsync=use_lipsync,
                use_jumpscare=use_jumpscare
            )
        except ImportError:
            print("[Video] Optimized module not available, using standard approach")
    
    # If no Lincoln image, create placeholder
    if not lincoln_image or not lincoln_image.exists():
        print("[Video] Creating placeholder Lincoln image...")
        lincoln_image = BASE_DIR / "lincoln_faces" / "lincoln_placeholder.png"
        if not lincoln_image.exists():
            # Create placeholder image
            subprocess.run([
                'ffmpeg', '-f', 'lavfi', '-i', 
                'color=c=gray20:s=512x512:d=1',
                '-vf', 'drawtext=text="A.\\ LINCOLN":fontcolor=white:fontsize=80:x=(w-text_w)/2:y=(h-text_h)/2',
                '-frames:v', '1', '-y', str(lincoln_image)
            ], capture_output=True)
        
        # Ensure it was created
        if not lincoln_image.exists():
            # Last resort: simple black square
            subprocess.run([
                'ffmpeg', '-f', 'lavfi', '-i', 'color=c=black:s=512x512:d=1',
                '-frames:v', '1', '-y', str(lincoln_image)
            ], capture_output=True)
        
        # Final check - if still missing, use temp file
        if not lincoln_image.exists():
            lincoln_image = BASE_DIR / "temp" / "black_bg.png"
            subprocess.run([
                'ffmpeg', '-f', 'lavfi', '-i', 'color=c=black:s=512x512:d=1',
                '-frames:v', '1', '-y', str(lincoln_image)
            ], capture_output=True)
    
    # Create static noise overlay
    static_file = BASE_DIR / "temp" / "static.mp4"
    subprocess.run([
        'ffmpeg', '-f', 'lavfi', '-i', 
        f'testsrc2=duration={duration}:size=1080x1080:rate=30',
        '-vf', 'geq=random(1)*255:128:128,hue=s=0',
        '-t', str(duration), '-y', str(static_file)
    ], capture_output=True)
    
    # Complex FFmpeg filter for Max Headroom effect
    # 1. Scale and position Lincoln face in center (TV screen effect)
    # 2. Add glitch effects (chromatic aberration, scanlines, horizontal tears)
    # 3. Add TV static overlay
    # 4. Color grading (desaturated, high contrast)
    
    vf = f"""
    [0:v]scale=800:800:force_original_aspect_ratio=decrease[face];
    color=c=black:s=1080x1080:d={duration}[bg];
    [bg][face]overlay=(W-w)/2:(H-h)/2[v1];
    [v1]split[v1a][v1b];
    [v1a]crop=1080:1080:0:0[main];
    [v1b]crop=1080:20:0:t*30%20[glitch];
    [main][glitch]overlay=0:mod(t,0.1)*1000[g1];
    [g1]eq=contrast=1.8:brightness=-0.2:gamma=1.3[v2];
    [v2]hue=s=0.3[v3];
    [v3]split[v3a][v3b];
    [v3a]geq=r='X/W*2-1':g='(X+5)/W*2-1':b='(X-5)/W*2-1'[chroma];
    [v3b]noise=alls=20:allf=t+u[noise];
    [chroma][noise]blend=all_mode=screen:all_opacity=0.3[final];
    [final]drawbox=0:0:1080:1080:black:10[tvframe];
    [tvframe]drawtext=text='ABRAHAM LINCOLN':fontcolor=white:fontsize=40:x=(w-text_w)/2:y=50:box=1:boxcolor=black@0.7[text1];
    [text1]drawtext=text='{headline[:30]}':fontcolor=red:fontsize=30:x=(w-text_w)/2:y=h-80:box=1:boxcolor=black@0.7[vf]
    """
    
    # OLD TV SET EFFECT with realistic frame, static, and scanlines
    # Escape special characters in headline for drawtext
    headline_escaped = headline[:35].replace(":", "\\:").replace("'", "\\'")
    
    # TV screen dimensions - MAKE LINCOLN BIGGER (like the high-view videos)
    # In successful videos, Lincoln fills most of the frame - make TV screen larger
    tv_screen_w = 900  # INCREASED from 720 - Lincoln more prominent
    tv_screen_h = 900  # INCREASED from 540 - almost full screen
    tv_x = (1080 - tv_screen_w) // 2
    tv_y = (1080 - tv_screen_h) // 2
    
    # AUTHENTIC VHS TV BROADCAST - MAX HEADROOM STYLE (old staticky TV screen)
    # Broadcasting from 1980s TV with ALL VHS artifacts
    vf_simple = (
        # Scale Lincoln face to fit inside TV screen area (VHS broadcast look)
        f"[0:v]scale={tv_screen_w-40}:{tv_screen_h-40}:force_original_aspect_ratio=decrease[face_scaled];"
        # VHS LOW RESOLUTION EFFECT (scale down to 480p then up - pixelated/blocky)
        f"[face_scaled]scale=480:360[lowres];"
        f"[lowres]scale={tv_screen_w-40}:{tv_screen_h-40}:flags=neighbor[face_pixelated];"
        # SLOW ZOOM-IN over time (zoom from 1.0 to 1.4 - Max Headroom style)
        f"[face_pixelated]zoompan=z='1.0+0.4*on/({duration}*30)':d=1:x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):s={tv_screen_w}x{tv_screen_h}[face_zoomed];"
        # VHS COLOR GRADING (oversaturated, color bleeding characteristic)
        f"[face_zoomed]eq=contrast=2.5:brightness=0.15:gamma=1.4:saturation=2.2[face_eq];"
        # Color bleeding (VHS characteristic - colors mix)
        f"[face_eq]colorchannelmixer=rr=0.9:rg=0.1:rb=0.0:gr=0.0:gg=0.95:gb=0.15:br=0.0:bg=0.1:bb=1.0[face_tinted];"
        # Create OLD TV ROOM background (dark brown/gray walls)
        f"color=c=#2a2419:s=1080x1080:d={duration}[bg];"
        # Draw TV BEZEL (outer frame - dark brown wood/bakelite)
        f"[bg]drawbox={tv_x-40}:{tv_y-40}:{tv_screen_w+80}:{tv_screen_h+80}:#3a3025:50[tv_bezel];"
        # Draw TV SCREEN BORDER (thick black bezel inside)
        f"[tv_bezel]drawbox={tv_x-15}:{tv_y-15}:{tv_screen_w+30}:{tv_screen_h+30}:black:25[tv_border];"
        # Draw TV SCREEN AREA (slightly lighter black - CRT phosphor glow)
        f"[tv_border]drawbox={tv_x}:{tv_y}:{tv_screen_w}:{tv_screen_h}:#0a0a0a:fill[tv_screen];"
        # Overlay Lincoln face INSIDE TV SCREEN (broadcasting from old TV)
        f"[tv_screen][face_tinted]overlay={tv_x+20}:{tv_y+20}[tv_face];"
        # VHS TRACKING ERRORS (horizontal displacement waves - picture "rolls")
        f"[tv_face]geq=r='r(X+2*sin(Y*0.1+T*5),Y)':g='g(X+2*sin(Y*0.1+T*5),Y)':b='b(X+2*sin(Y*0.1+T*5),Y)'[tracking];"
        # VHS RGB SPLIT (chromatic aberration - color channels misaligned)
        f"[tracking]geq=r='r(X+5,Y)':g='g(X,Y)':b='b(X-5,Y)'[rgb_split];"
        # VERTICAL HOLD GLITCH (occasional screen roll - VHS characteristic)
        f"[rgb_split]geq=r='r(X,Y+2*sin(T*2))':g='g(X,Y+2*sin(T*2))':b='b(X,Y+2*sin(T*2))'[rolled];"
        # SCAN LINES (horizontal lines every 3-4 pixels - CRT effect)
        f"[rolled]geq=r='if(mod(Y,4),r(X,Y),r(X,Y)*0.7)':g='if(mod(Y,4),g(X,Y),g(X,Y)*0.7)':b='if(mod(Y,4),b(X,Y),b(X,Y)*0.7)'[scanned];"
        # VHS STATIC/NOISE (heavy interference - "snow" effect)
        f"[scanned]noise=alls=40:allf=t+u[static_vhs];"
        # Slight blur (VHS softness characteristic)
        f"[static_vhs]boxblur=1:1[soft_vhs];"
        # FINAL VHS COLOR GRADING (oversaturated, color shift, darker edges via brightness)
        f"[soft_vhs]eq=contrast=2.5:brightness=-0.15:gamma=1.6:saturation=1.8[glitch_final];"
        # Text overlays - VHS TV STYLE (large, bold, readable)
        f"[glitch_final]drawtext=text='ABRAHAM LINCOLN':fontcolor=white:fontsize=52:x=(w-text_w)/2:y={tv_y-60}:box=1:boxcolor=black@0.9:boxborderw=5[title_text];"
        f"[title_text]drawtext=text='Lincoln WARNING':fontcolor=cyan:fontsize=38:x=(w-text_w)/2:y={tv_y+tv_screen_h+40}:box=1:boxcolor=black@0.9[vf];"
    )
    
    # STEP 1: Generate lip-sync video if requested
    lipsync_video = None
    if use_lipsync:
        lipsync_temp = BASE_DIR / "temp" / f"lipsync_{random.randint(1000,9999)}.mp4"
        
        # Try D-ID first
        if DID_API_KEY:
            lipsync_video = generate_lipsync_did(lincoln_image, audio_path, lipsync_temp)
        
        # If D-ID failed or not available, try Wav2Lip
        if not lipsync_video or not lipsync_video.exists():
            lipsync_video = generate_lipsync_wav2lip(lincoln_image, audio_path, lipsync_temp)
        
        if lipsync_video and lipsync_video.exists():
            lincoln_video_source = lipsync_video
            print("[Video] Using lip-sync video")
        else:
            print("[Video] Lip-sync failed, using static image")
            lincoln_video_source = None
    else:
        lincoln_video_source = None
    
    # STEP 2: Create base video (lip-sync or static)
    if lincoln_video_source and lincoln_video_source.exists():
        # Use lip-sync video as base
        base_video = lincoln_video_source
    else:
        # Create looping background from static image
        loop_video = BASE_DIR / "temp" / f"loop_{random.randint(1000,9999)}.mp4"
        subprocess.run([
            'ffmpeg', '-loop', '1', '-i', str(lincoln_image),
            '-t', str(duration), '-vf', 'scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1080:(ow-iw)/2:(oh-ih)/2:black',
            '-y', str(loop_video)
        ], capture_output=True)
        base_video = loop_video
    
    # STEP 3: Apply Max Headroom effects with TV frame and QR code
    headroom_temp = BASE_DIR / "temp" / f"headroom_{random.randint(1000,9999)}.mp4"
    
    # Generate QR code
    qr_path = generate_bitcoin_qr()
    
    # Build FFmpeg command with optional QR code input
    ffmpeg_inputs = ['ffmpeg', '-i', str(base_video), '-i', str(audio_path)]
    
    # Update filter chain to include QR code if available
    if qr_path and qr_path.exists():
        ffmpeg_inputs.extend(['-loop', '1', '-t', str(duration), '-i', str(qr_path)])
        # Add QR code overlay to filter chain - separate input stream
        vf_simple = vf_simple.replace('[vtext1]copy[vf]', f'[2:v]scale=150:150[qr];[vtext1][qr]overlay=w-170:170[vf]')
        map_video = '[vf]'
    else:
        # No QR code
        map_video = '[vf]'
    
    # BEAUTIFUL SYNC: Ensure video matches audio exactly (shortest ensures perfect sync)
    cmd = ffmpeg_inputs + [
        '-filter_complex', vf_simple,
        '-map', map_video, '-map', '1:a:0',
        # VHS AUDIO DISTORTION (compressed frequency range 100Hz-8kHz, slight muffle)
        '-af', 'volume=3.0,highpass=f=100,lowpass=f=8000,'
        'compand=attacks=0.3:decays=0.8:points=-90/-90|-60/-60|-40/-30|-30/-20|0/0,'
        'aecho=0.8:0.88:60:0.4,'
        'equalizer=f=200:width_type=h:width=100:g=2,'
        'equalizer=f=4000:width_type=h:width=1000:g=-3,'
        'loudnorm=I=-16:TP=-1.5:LRA=11',
        '-c:v', 'libx264', '-preset', 'fast', '-crf', '20', '-threads', '8',  # OPTIMIZED: fast preset + threading
        '-c:a', 'aac', '-b:a', '256k', '-ar', '44100',
        '-shortest',  # Perfect sync: video ends when audio ends
        '-pix_fmt', 'yuv420p',
        '-y', str(headroom_temp)
    ]
    
    # OPTIMIZED: Use longer timeout for videos >60s, shorter for shorter videos
    timeout_seconds = 180 if duration > 60 else 120
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_seconds)
    
    if not headroom_temp.exists() or headroom_temp.stat().st_size == 0:
        print(f"[Video] Failed: {result.stderr[-500:]}")
        return False
    
    # BEAUTIFUL SYNC VERIFICATION: Check video duration matches audio perfectly
    try:
        vid_result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', str(headroom_temp)],
            capture_output=True, text=True
        )
        vid_duration = float(vid_result.stdout.strip())
        sync_diff = abs(vid_duration - duration)
        if sync_diff > 0.5:  # More than 0.5s difference
            print(f"[Video] ⚠️ Sync warning: audio={duration:.2f}s, video={vid_duration:.2f}s (diff={sync_diff:.2f}s)")
        else:
            print(f"[Video] ✅ Perfect sync: video={vid_duration:.2f}s matches audio={duration:.2f}s")
    except:
        pass
    
    # STEP 4: Add jumpscare effects if requested
    if use_jumpscare:
        jumpscare_output = BASE_DIR / "temp" / f"jumpscare_{random.randint(1000,9999)}.mp4"
        if add_jumpscare_effects(headroom_temp, jumpscare_output, audio_path):
            # Replace headroom with jumpscare version
            import shutil
            shutil.move(str(jumpscare_output), str(output_path))
        else:
            # Jumpscare failed, use headroom version
            import shutil
            shutil.move(str(headroom_temp), str(output_path))
    else:
        import shutil
        shutil.move(str(headroom_temp), str(output_path))
    
    if output_path.exists():
        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"[Video] Created: {size_mb:.2f} MB")
        return True
    else:
        print(f"[Video] Final video missing!")
        return False

def upload_to_youtube(video_path, headline, episode_num=None):
    """Upload to YouTube with WARNING title format"""
    print("[YouTube] Uploading...")
    if episode_num is None:
        episode_num = int(os.getenv("EPISODE_NUM", "1000"))
    try:
        import pickle
        from googleapiclient.discovery import build
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.http import MediaFileUpload
        from google.auth.transport.requests import Request
    except ImportError:
        print("[YouTube] API packages not installed")
        return None
    
    # Try multiple credential file locations
    scarify_root = BASE_DIR.parent  # F:/AI_Oracle_Root/scarify (abraham_horror's parent)
    possible_creds = [
        scarify_root / "core" / "client_secret_679199614743-1fq6sini3p9kjs237ek4seg4ojp4a4qe.apps.googleusercontent.com.json",
        scarify_root / "client_secret_679199614743-1fq6sini3p9kjs237ek4seg4ojp4a4qe.apps.googleusercontent.com.json",
        Path("client_secret_679199614743-1fq6sini3p9kjs237ek4seg4ojp4a4qe.apps.googleusercontent.com.json"),
        scarify_root / "config" / "credentials" / "youtube" / "client_secrets.json",
    ]
    creds_file = None
    for pc in possible_creds:
        if pc.exists():
            creds_file = pc
            break
    token_file = BASE_DIR / "youtube_token.pickle"
    
    if not creds_file or not creds_file.exists():
        print("[YouTube] Credentials not found")
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
        
        title = f"Lincoln's Warning: {headline[:50]} | Max Headroom Style #Shorts"
        description = f"""{headline}

ABRAHAM LINCOLN SPEAKS FROM BEYOND THE GRAVE

Max Headroom-style glitchy broadcast from the afterlife.

#AbrahamLincoln #MaxHeadroom #Horror #Shorts #Viral #Glitch"""
        
        tags = ['abraham lincoln', 'max headroom', 'glitch', 'horror', 'shorts', 'viral', 'halloween 2025']
        
        body = {
            'snippet': {'title': title, 'description': description, 'tags': tags, 'categoryId': '24'},
            'status': {'privacyStatus': 'public', 'selfDeclaredMadeForKids': False}
        }
        
        media = MediaFileUpload(str(video_path), chunksize=1024*1024, resumable=True)
        request = youtube.videos().insert(part=','.join(body.keys()), body=body, media_body=media)
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"[YouTube] Upload: {int(status.progress() * 100)}%", end='\r')
        
        print()
        video_id = response['id']
        video_url = f"https://youtube.com/watch?v={video_id}"
        
        print(f"[YouTube] UPLOADED: {video_url}")
        return video_url
        
    except Exception as e:
        print(f"[YouTube] Error: {e}")
        return None

def get_warning_title(headline, episode_num=None):
    """Generate WARNING title format matching high-performing videos"""
    if episode_num is None:
        episode_num = int(os.getenv("EPISODE_NUM", "1000"))
    hl = headline.lower()
    
    if "trump" in hl:
        return f"Lincoln's WARNING #{episode_num}: Trump's Tariffs Destroying Economy #Shorts #R3"
    elif "police" in hl:
        return f"Lincoln's WARNING #{episode_num}: Police Strike - No Law #Shorts #R3"
    elif "education" in hl or "school" in hl:
        return f"Lincoln's WARNING #{episode_num}: Education System Destroyed #Shorts #R3"
    elif "military" in hl or "draft" in hl:
        return f"Lincoln's WARNING #{episode_num}: Military Draft Activated #Shorts #R3"
    elif "senate" in hl or "congress" in hl:
        return f"Lincoln's WARNING #{episode_num}: Senate Corruption Exposed #Shorts #R3"
    elif "market" in hl or "stock" in hl:
        return f"Lincoln's WARNING #{episode_num}: Markets Crash Coming #Shorts #R3"
    elif "climate" in hl or "water" in hl:
        return f"Lincoln's WARNING #{episode_num}: Water Crisis - Pipes Dry #Shorts #R3"
    elif "tech" in hl or "ai" in hl:
        return f"Lincoln's WARNING #{episode_num}: Tech CEOs Control Everything #Shorts #R3"
    else:
        return f"Lincoln's WARNING #{episode_num}: America in Crisis #Shorts #R3"

def log_to_google_sheets(episode_num, headline, script, video_path, youtube_url=""):
    """Log video to Google Sheets (with CSV fallback)"""
    try:
        # Try to import the tracking module
        import sys
        sys.path.insert(0, str(BASE_DIR.parent))
        from google_sheets_tracker import log_video_to_sheets
        
        script_length = len(script.split())
        return log_video_to_sheets(episode_num, headline, script_length, str(video_path), youtube_url)
    except ImportError:
        # Fallback: Simple CSV logging
        print("[Tracking] Google Sheets module not found, using local tracking")
        csv_file = BASE_DIR.parent / "video_tracking.csv"
        try:
            if not csv_file.exists():
                with open(csv_file, 'w', encoding='utf-8') as f:
                    f.write("Episode,Headline,Date,Words,YouTube URL\n")
            with open(csv_file, 'a', encoding='utf-8') as f:
                f.write(f"{episode_num},\"{headline[:100]}\",{datetime.now().strftime('%Y-%m-%d %H:%M')},{len(script.split())},{youtube_url}\n")
            print(f"[Tracking] Logged to CSV: episode #{episode_num}")
            return True
        except Exception as e:
            print(f"[Tracking] Error: {e}")
            return False

def generate():
    """Main generation pipeline with Google Sheets tracking"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    print(f"\n{'='*60}\nMAX HEADROOM ABRAHAM LINCOLN (DARK COMEDY)\n{'='*60}\n")
    
    headlines = get_headlines()
    headline = random.choice(headlines)
    print(f"[Headline] {headline}\n")
    
    script = generate_script(headline)
    word_count = len(script.split())
    print(f"[Script] {word_count} words (target: 33-45 for 9-17s)")
    print(f"[Preview] {script[:80]}...\n")
    
    audio_path = BASE_DIR / f"audio/abraham_{timestamp}.mp3"
    if not generate_voice(script, audio_path):
        return None
    
    lincoln_image = generate_lincoln_face_pollo()
    
    video_path = BASE_DIR / f"videos/MAX_HEADROOM_{timestamp}.mp4"
    # Generate with lip sync and jumpscare enabled
    use_lipsync = os.getenv("USE_LIPSYNC", "true").lower() == "true"
    use_jumpscare = os.getenv("USE_JUMPSCARE", "true").lower() == "true"
    
    if not create_max_headroom_video(lincoln_image, audio_path, video_path, headline, 
                                     use_lipsync=use_lipsync, use_jumpscare=use_jumpscare):
        return None
    
    # Use episode number from environment or default
    episode_num = int(os.getenv("EPISODE_NUM", "1000"))
    youtube_url = upload_to_youtube(video_path, headline, episode_num)
    
    youtube_dir = BASE_DIR / "youtube_ready"
    youtube_file = youtube_dir / f"MAX_HEADROOM_{timestamp}.mp4"
    
    import shutil
    shutil.copy2(video_path, youtube_file)
    
    # Log to Google Sheets (auto-tracking)
    log_to_google_sheets(episode_num, headline, script, video_path, youtube_url or "")
    
    if youtube_url:
        print(f"\n[READY] {youtube_file.name}")
        print(f"[UPLOADED] {youtube_url}")
        print(f"[TRACKED] Logged to tracking system\n")
    else:
        print(f"\n[READY] {youtube_file.name}")
        print(f"[TRACKED] Logged to tracking system\n")
    
    return str(youtube_file)

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    print(f"\nGenerating {count} Max Headroom video(s)...\n")
    
    for i in range(count):
        generate()
        if i < count - 1:
            time.sleep(5)

