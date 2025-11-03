"""
QR CODE VIRAL VIDEO GENERATOR
Creates videos specifically designed to maximize QR code scans
Uses psychological triggers: curiosity, FOMO, mystery, reward
"""
import os, sys, json, requests, subprocess, random, time, re
from pathlib import Path
from datetime import datetime
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageSequence
import numpy as np

# API KEYS
ELEVENLABS_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
PEXELS_KEY = "RgE9Mdn3ToSQhn2RiLJ4mPMISjjp587QKRG9uhpOrLVtkKPCibUPUDGh"

BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
ROOT = Path("F:/AI_Oracle_Root/scarify")
BTC = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"

VOICES_MALE = [
    "VR6AewLTigWG4xSOukaG",
    "pNInz6obpgDQGcFmaJgB",
    "EXAVITQu4vr4xnSDxMaL",
]

# QR CODE VIRAL CONCEPTS
QR_CONCEPTS = {
    "lincoln_message": {
        "name": "The Message Lincoln Left",
        "hook": "Abraham Lincoln left a message. Hidden for 160 years. I found it.",
        "script": """Abraham Lincoln. April 14, 1865.

They think I died in that theater. I didn't.

I left a message. For the future. For YOU.

It's been hidden for 160 years. Encrypted. Protected.

Until now.

I'm releasing it. But only to those brave enough to scan.

The QR code on your screen contains Lincoln's final message.

Scan it. Before they remove this video.

Some truths are too dangerous for history books.

Bitcoin {btc}""",
        "visual_style": "historical_document",
        "qr_destination": "https://forms.gle/YourFormHere",  # Replace with actual
        "urgency": "high",
        "cta": "SCAN BEFORE THIS IS DELETED"
    },
    
    "government_censorship": {
        "name": "Scan Before Government Does",
        "hook": "They're trying to remove this. Screenshot and scan NOW.",
        "script": """URGENT MESSAGE.

This video will be taken down. I know how this works.

The information in this QR code is being actively suppressed.

Government doesn't want you to know. Big Tech is complicit.

But I'm smarter. I encrypted it. Put it in a QR code.

They can delete the video. But if you screenshot and scan NOW, you have it forever.

First 1000 scanners get the full document.

After that, this gets censored.

Scan. Save. Share.

Your window is closing.

Bitcoin {btc}""",
        "visual_style": "redacted_document",
        "qr_destination": f"bitcoin:{BTC}?message=Truth",
        "urgency": "extreme",
        "cta": "SCREENSHOT AND SCAN NOW"
    },
    
    "intelligence_test": {
        "name": "Only 3% Can Solve This",
        "hook": "97% can't figure this out. Are you in the 3%?",
        "script": """Abraham Lincoln. IQ test.

I'm going to show you a puzzle. Most people can't solve it.

In fact, 97% fail.

The answer isn't obvious. It requires critical thinking.

The QR code contains the solution. But also a challenge.

If you're smart enough to scan and solve, you'll understand.

If you're part of the 97%, you'll scroll past.

Which are you?

The 3% who scan. Or the 97% who don't?

Prove it.

Bitcoin {btc}""",
        "visual_style": "puzzle_challenge",
        "qr_destination": "https://example.com/puzzle",  # Replace
        "urgency": "medium",
        "cta": "SCAN TO PROVE YOUR IQ"
    },
    
    "free_bitcoin": {
        "name": "Free Bitcoin in QR Code",
        "hook": "First 1000 scanners get 0.001 BTC. Go.",
        "script": """ATTENTION.

Free Bitcoin. Right now.

First 1000 people to scan this QR code get 0.001 BTC.

That's $60+ USD. Free.

Why? Because I want to prove a point about human nature.

How many of you will actually scan?

The QR code is on your screen. Takes 2 seconds.

But I bet 90% of you won't do it.

Prove me wrong.

Scan. Claim. It's that simple.

Timer starts now.

Bitcoin {btc}""",
        "visual_style": "bitcoin_glow",
        "qr_destination": f"bitcoin:{BTC}?amount=0.00001&message=Claim",
        "urgency": "extreme",
        "cta": "SCAN TO CLAIM BTC"
    },
    
    "password_vault": {
        "name": "The Password is in the Code",
        "hook": "Scan to access the private Discord/content/files",
        "script": """You found the vault.

But it's locked.

The password is in this QR code.

Behind that password? Everything.

Private Discord. Exclusive content. Files they don't want you to have.

Thousands of people know. You could be next.

Or you could scroll past and never know what you missed.

The QR code is visible for 10 seconds.

Scan it. Enter the password. Access granted.

Choose wisely.

Bitcoin {btc}""",
        "visual_style": "vault_locked",
        "qr_destination": "https://discord.gg/YourInvite",  # Replace
        "urgency": "high",
        "cta": "SCAN FOR PASSWORD"
    },
    
    "tesla_blueprint": {
        "name": "Tesla's Lost Invention",
        "hook": "Tesla hid this invention. The full blueprint requires scanning.",
        "script": """Nikola Tesla. 1943. Died in poverty.

Why? Because he invented something they couldn't allow.

Free energy. Wireless power for everyone.

They confiscated his papers. Classified them.

But I found the blueprint. Encrypted it. Put it in a QR code.

The full schematic is on your screen.

Scan it. Study it. Build it if you can.

This is what they killed Tesla to hide.

Don't let it die with him.

Bitcoin {btc}""",
        "visual_style": "electric_blueprint",
        "qr_destination": "https://example.com/tesla",  # Replace
        "urgency": "medium",
        "cta": "SCAN TO SEE BLUEPRINT"
    },
    
    "social_proof": {
        "name": "10 Million Scanned This",
        "hook": "Join the 10M who know the truth.",
        "script": """10 million people have scanned this QR code.

You see the counter on screen? That's real-time.

Right now, as you watch, people are scanning.

They know something you don't.

Unless you scan too.

What's behind it? I can't tell you. That would ruin it.

But 10 million people thought it was worth 2 seconds of their time.

Are you more skeptical than 10 million people?

Or more curious?

Scan and find out.

Bitcoin {btc}""",
        "visual_style": "live_counter",
        "qr_destination": "https://example.com/truth",  # Replace
        "urgency": "medium",
        "cta": "JOIN 10M SCANNERS"
    },
    
    "media_coverup": {
        "name": "What Media Won't Show",
        "hook": "They deleted this. I saved it. Scan before it's gone.",
        "script": """This footage was removed from every platform.

YouTube. Twitter. Facebook. All of it.

Gone.

But I downloaded it first. Archived it. Encrypted it into this QR code.

The media won't show you this. The government doesn't want you to see it.

But I do.

Scan the code. Watch the footage they tried to erase.

Decide for yourself.

Before this video gets flagged too.

Bitcoin {btc}""",
        "visual_style": "censored_footage",
        "qr_destination": "https://rumble.com/YourVideo",  # Replace
        "urgency": "extreme",
        "cta": "SCAN BEFORE DELETION"
    },
    
    "illegal_knowledge": {
        "name": "Illegal in 37 Countries",
        "hook": "This QR code is illegal in 37 countries. Scan at your own risk.",
        "script": """WARNING.

This QR code contains information banned in 37 countries.

Scanning it may put you on a list. I'm not joking.

Governments don't want you to have this knowledge.

China banned it. Russia banned it. Even some EU countries.

But you're free. For now.

Scan if you dare.

Some information is worth the risk.

Your choice.

Bitcoin {btc}""",
        "visual_style": "forbidden_glitch",
        "qr_destination": "https://example.com/forbidden",  # Replace
        "urgency": "extreme",
        "cta": "SCAN AT YOUR RISK"
    },
    
    "arg_resistance": {
        "name": "Join the Resistance ARG",
        "hook": "Scan to receive your mission.",
        "script": """Recruit.

You've been selected.

The resistance needs you.

Your mission is encoded in this QR code.

Scan it. Follow the instructions. Complete the objective.

There are others like you. Scanning. Acting. Changing things.

But we can't do it without you.

This is your recruitment.

Accept or decline.

The QR code is your answer.

Bitcoin {btc}""",
        "visual_style": "dystopian_recruitment",
        "qr_destination": "https://example.com/mission1",  # Replace
        "urgency": "medium",
        "cta": "SCAN TO ACCEPT MISSION"
    }
}

def log(msg, status="INFO"):
    icons = {"INFO": "[INFO]", "SUCCESS": "[OK]", "ERROR": "[ERROR]", "PROCESS": "[PROCESS]"}
    print(f"{icons.get(status, '[INFO]')} {msg}")

def create_qr_code(data, filename, style="standard"):
    """Generate QR code with styling"""
    log(f"Creating QR code: {style}", "PROCESS")
    
    qr = qrcode.QRCode(
        version=5,  # Size
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create QR image
    if style == "bitcoin_glow":
        # Orange/gold for Bitcoin
        img = qr.make_image(fill_color="#FF9500", back_color="black")
    elif style == "redacted_document":
        # Red on black for urgency
        img = qr.make_image(fill_color="red", back_color="#0A0A0A")
    elif style == "electric_blueprint":
        # Electric blue
        img = qr.make_image(fill_color="#00BFFF", back_color="#001020")
    elif style == "forbidden_glitch":
        # Purple/magenta
        img = qr.make_image(fill_color="#FF00FF", back_color="black")
    else:
        # Standard high contrast
        img = qr.make_image(fill_color="black", back_color="white")
    
    # Save
    img.save(filename)
    log(f"QR code saved: {filename}", "SUCCESS")
    return filename

def create_animated_qr(qr_path, output_path, frames=30):
    """Create glitching/pulsing QR code animation"""
    log("Creating animated QR code...", "PROCESS")
    
    try:
        qr_img = Image.open(qr_path).convert('RGBA')
        qr_img = qr_img.resize((800, 800), Image.NEAREST)
        
        images = []
        for i in range(frames):
            frame = qr_img.copy()
            
            # Pulse effect
            scale = 1.0 + 0.1 * np.sin(i * 2 * np.pi / frames)
            new_size = (int(800 * scale), int(800 * scale))
            frame_scaled = frame.resize(new_size, Image.NEAREST)
            
            # Center on canvas
            canvas = Image.new('RGBA', (800, 800), (0, 0, 0, 0))
            offset = ((800 - new_size[0]) // 2, (800 - new_size[1]) // 2)
            canvas.paste(frame_scaled, offset)
            
            # Glitch effect every 10 frames
            if i % 10 == 0:
                # Add some noise
                arr = np.array(canvas)
                noise = np.random.randint(0, 50, arr.shape, dtype='uint8')
                arr = np.clip(arr.astype(int) + noise, 0, 255).astype('uint8')
                canvas = Image.fromarray(arr)
            
            images.append(canvas)
        
        # Save as animated PNG or GIF
        images[0].save(
            output_path,
            save_all=True,
            append_images=images[1:],
            duration=50,
            loop=0
        )
        
        log(f"Animated QR saved: {output_path}", "SUCCESS")
        return output_path
    except Exception as e:
        log(f"Animation failed: {e}", "ERROR")
        return qr_path

def generate_audio(text, output_path):
    """Generate urgent voice"""
    log("Generating voice...", "PROCESS")
    
    for voice_id in VOICES_MALE:
        try:
            r = requests.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                json={
                    "text": text,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {
                        "stability": 0.4,  # More urgent
                        "similarity_boost": 0.85,
                        "style": 0.9,  # Maximum intensity
                        "use_speaker_boost": True
                    }
                },
                headers={"xi-api-key": ELEVENLABS_KEY},
                timeout=120
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

def create_qr_viral_video(concept_key, output_path, platform="youtube_shorts"):
    """Create viral QR code video"""
    concept = QR_CONCEPTS[concept_key]
    log(f"Creating viral video: {concept['name']}", "PROCESS")
    
    try:
        from moviepy.editor import (
            AudioFileClip, ImageClip, CompositeVideoClip, 
            ColorClip, VideoFileClip, TextClip
        )
        
        # Generate script
        script = concept['script'].format(btc=BTC)
        
        # Generate audio
        audio_path = BASE / f"audio/qr_{concept_key}.mp3"
        if not generate_audio(script, audio_path):
            return False
        
        audio = AudioFileClip(str(audio_path))
        duration = min(audio.duration, 60.0)
        
        # Create QR code
        qr_path = BASE / f"temp/qr_{concept_key}.png"
        qr_path.parent.mkdir(parents=True, exist_ok=True)
        create_qr_code(concept['qr_destination'], qr_path, concept['visual_style'])
        
        # Platform-specific resolution
        if platform in ["youtube_shorts", "tiktok", "instagram_reels"]:
            width, height = 1080, 1920  # Vertical
        elif platform == "twitter":
            width, height = 1080, 1080  # Square
        else:
            width, height = 1920, 1080  # Horizontal
        
        # Background based on style
        if concept['visual_style'] == "bitcoin_glow":
            bg_color = (10, 5, 0)
        elif concept['visual_style'] == "redacted_document":
            bg_color = (10, 0, 0)
        elif concept['visual_style'] == "electric_blueprint":
            bg_color = (0, 10, 20)
        elif concept['visual_style'] == "forbidden_glitch":
            bg_color = (15, 0, 15)
        else:
            bg_color = (5, 5, 10)
        
        bg = ColorClip(size=(width, height), color=bg_color, duration=duration).set_audio(audio)
        
        # QR code placement (ensure RGB not RGBA)
        qr_img = Image.open(qr_path).convert('RGB')  # Force RGB
        qr_size = int(min(width, height) * 0.6)  # 60% of smaller dimension
        qr_img_resized = qr_img.resize((qr_size, qr_size), Image.NEAREST)
        qr_temp = BASE / f"temp/qr_{concept_key}_resized.jpg"  # Use JPG not PNG
        qr_img_resized.save(qr_temp)
        
        # Show QR code for last 2/3 of video (gives time for hook first)
        qr_start_time = duration * 0.33
        qr_clip = ImageClip(str(qr_temp)).set_position('center').set_start(qr_start_time).set_duration(duration - qr_start_time)
        
        # Urgency text overlays (RGB for MoviePy compatibility)
        hook_img = Image.new('RGB', (width, int(height*0.2)), (0, 0, 0))
        hook_draw = ImageDraw.Draw(hook_img)
        hook_draw.rectangle([(20, 20), (width-20, int(height*0.2)-20)], 
                          fill=(255, 0, 0), outline=(255, 255, 255), width=4)
        hook_draw.text((width//2, int(height*0.1)), concept['hook'][:50], 
                      fill=(255, 255, 255), anchor="mm")
        hook_path = BASE / f"temp/hook_{concept_key}.jpg"
        hook_img.save(hook_path)
        hook_clip = ImageClip(str(hook_path)).set_position(('center', int(height*0.1))).set_duration(min(5.0, duration)).set_opacity(0.95)
        
        # CTA text (last 3 seconds - RGB)
        cta_img = Image.new('RGB', (width, 150), (0, 0, 0))
        cta_draw = ImageDraw.Draw(cta_img)
        cta_draw.rectangle([(30, 30), (width-30, 120)], 
                          fill=(255, 100, 0), outline=(255, 255, 255), width=5)
        cta_draw.text((width//2, 75), concept['cta'], 
                     fill=(255, 255, 255), anchor="mm")
        cta_path = BASE / f"temp/cta_{concept_key}.jpg"
        cta_img.save(cta_path)
        cta_clip = ImageClip(str(cta_path)).set_position(('center', height-200)).set_start(duration-3).set_duration(3).set_opacity(0.95)
        
        # Urgency timer (if extreme urgency)
        layers = [bg]
        
        if concept['urgency'] == "extreme":
            # Add pulsing red border (RGB)
            border_img = Image.new('RGB', (width, height), (0, 0, 0))
            border_draw = ImageDraw.Draw(border_img)
            border_draw.rectangle([(0, 0), (width-1, height-1)], 
                                outline=(255, 0, 0), width=15)
            border_path = BASE / f"temp/border_{concept_key}.jpg"
            border_img.save(border_path)
            border_clip = ImageClip(str(border_path)).set_duration(duration).set_opacity(0.7)
            layers.append(border_clip)
        
        layers.extend([qr_clip, hook_clip, cta_clip])
        
        comp = CompositeVideoClip(layers, size=(width, height))
        
        comp.write_videofile(
            str(output_path),
            fps=30,
            codec='libx264',
            audio_codec='aac',
            bitrate='10000k',
            preset='fast',
            verbose=False,
            logger=None
        )
        
        comp.close()
        bg.close()
        audio.close()
        
        log(f"Viral QR video created: {concept['name']}", "SUCCESS")
        return True
        
    except Exception as e:
        log(f"Video creation failed: {e}", "ERROR")
        import traceback
        traceback.print_exc()
    return False

def generate_qr_campaign():
    """Generate all QR viral videos"""
    t = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    log(f"\n{'='*70}\nQR CODE VIRAL CAMPAIGN\n{'='*70}", "INFO")
    log(f"Generating {len(QR_CONCEPTS)} viral QR videos", "INFO")
    log(f"{'='*70}\n")
    
    results = []
    
    for i, (concept_key, concept) in enumerate(QR_CONCEPTS.items(), 1):
        log(f"\n[{i}/{len(QR_CONCEPTS)}] {concept['name']}", "PROCESS")
        
        vp = BASE / f"videos/QR_{concept_key}_{t}.mp4"
        if create_qr_viral_video(concept_key, vp):
            # Save to uploaded
            up = BASE / "uploaded" / f"QR_{concept_key}_{t}.mp4"
            up.parent.mkdir(parents=True, exist_ok=True)
            import shutil
            shutil.copy2(vp, up)
            
            mb = up.stat().st_size / (1024 * 1024)
            
            results.append({
                'concept': concept['name'],
                'file': str(up),
                'size_mb': round(mb, 2),
                'urgency': concept['urgency'],
                'expected_ctr': "15-45%",
                'destination': concept['qr_destination']
            })
            
            log(f"Saved: {up.name} ({mb:.1f}MB)", "SUCCESS")
        
        if i < len(QR_CONCEPTS):
            time.sleep(2)
    
    log(f"\n{'='*70}\nCAMPAIGN COMPLETE: {len(results)} videos\n{'='*70}", "SUCCESS")
    
    for r in results:
        print(f"\n[{r['concept']}]")
        print(f"  File: {r['file']}")
        print(f"  Size: {r['size_mb']}MB")
        print(f"  Urgency: {r['urgency']}")
        print(f"  Expected CTR: {r['expected_ctr']}")
    
    return results

if __name__ == "__main__":
    # Install qrcode if not present
    try:
        import qrcode
    except ImportError:
        log("Installing qrcode library...", "PROCESS")
        subprocess.run([sys.executable, "-m", "pip", "install", "qrcode[pil]"], 
                      capture_output=True)
        import qrcode
    
    log(f"\n{'='*70}")
    log(f"QR CODE VIRAL VIDEO GENERATOR")
    log(f"{'='*70}")
    log(f"Concepts: {len(QR_CONCEPTS)}")
    log(f"Psychology: Curiosity, FOMO, urgency, reward")
    log(f"{'='*70}\n")
    
    generate_qr_campaign()

