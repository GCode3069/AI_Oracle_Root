"""
ABRAHAM LINCOLN - MAX HEADROOM EDITION
1980s cyberpunk, VHS degradation, analog horror, glitch art.
Features:
- Synthetic/compressed voice with subtle stutter
- Audio‑reactive "lip bar" for simple lip sync
- CRT scanlines, rolling lines, color bleed, macroblocking
"""
import os, sys, json, requests, subprocess, random, time
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

import numpy as np
from PIL import Image, ImageDraw

ELEVENLABS_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
ROOT = Path("F:/AI_Oracle_Root/scarify")
BTC = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"

def scrape():
    try:
        r = requests.get("https://news.google.com/rss", timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'xml')
            return [item.title.text for item in soup.find_all('item')[:20] if item.title]
    except: pass
    return ["Trump Policies", "Police Issues", "Climate Crisis"]

def stutterize(text: str) -> str:
    words = text.split()
    out = []
    for w in words:
        if random.random() < 0.07 and len(w) > 3:
            syl = w[:2]
            out.append(f"{syl}-{syl}-{w}")
        else:
            out.append(w)
    return " ".join(out)

def comedy(headline):
    hl = headline.lower()
    openers = [
        f"Abraham Lincoln. Digitized. Glitching. Reading: {headline}.",
        f"Honest Abe, Max Headroom edition. Headline: {headline}.",
        f"Sixteenth president. Now a corrupted VHS file. {headline}."
    ]
    body = (
        "I led a civil war. You led a comment section. I freed slaves. You freed influencers."
        " This news cycle is a broken tape— rewind, play, distort, repeat."
    )
    close = f"Funding truth: Bitcoin {BTC}." 
    script = f"{random.choice(openers)} {body} {close}"
    return stutterize(script)

def audio(text, out):
    print("    [AUDIO] Generating synthetic voice")
    try:
        r = requests.post(
            "https://api.elevenlabs.io/v1/text-to-speech/VR6AewLTigWG4xSOukaG",
            json={
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {"stability": 0.35, "similarity_boost": 0.85, "style": 0.9, "use_speaker_boost": True}
            },
            headers={"xi-api-key": ELEVENLABS_KEY}, timeout=240
        )
        if r.status_code == 200:
            out.parent.mkdir(parents=True, exist_ok=True)
            tmp = out.parent / f"tmp_{out.name}"
            with open(tmp, "wb") as f: f.write(r.content)
            # Post-process to add synthetic/robotic texture
            subprocess.run([
                "ffmpeg", "-y", "-i", str(tmp),
                "-af", "acompressor=threshold=-20dB:ratio=6:attack=5:release=50,"
                       "chorus=0.6:0.8:55:0.4:0.25:2,"
                       "atempo=0.98,acrusher=level_in=1:level_out=1:bits=8:mode=log:aa=1",
                str(out)
            ], capture_output=True, timeout=240)
            tmp.unlink(missing_ok=True)
            return True
    except Exception as e:
        print("    [ERROR] Audio:", e)
    return False

def build_scanlines_png(path, alpha=70):
    img = Image.new('RGBA', (1080, 1920), (0,0,0,0))
    d = ImageDraw.Draw(img)
    for y in range(0, 1920, 3):
        d.line([(0,y), (1080,y)], fill=(0,0,0,alpha), width=1)
    img.save(path)

def video_max_headroom(audio_path, out):
    print("    [VIDEO] Building Max Headroom CRT with lip-sync bar")
    try:
        from moviepy.editor import AudioFileClip, ImageClip, ColorClip, CompositeVideoClip
        audio = AudioFileClip(str(audio_path))
        duration = min(audio.duration, 60.0)

        # Choose image: prefer provided cyberpunk TV image if present
        custom = next(iter((ROOT.glob('ChatGPT Image*.png'))), None)
        img_path = custom if custom and custom.exists() else BASE / "temp" / "lincoln.jpg"
        if not img_path.exists():
            img_path.parent.mkdir(exist_ok=True)
            data = requests.get("https://upload.wikimedia.org/wikipedia/commons/a/ab/Abraham_Lincoln_O-77_matte_collodion_print.jpg", timeout=30).content
            with open(img_path, "wb") as f: f.write(data)

        bg = ColorClip(size=(1080,1920), color=(15,10,20), duration=duration).set_audio(audio)
        base = ImageClip(str(img_path)).resize(height=1200)
        base = base.set_position(('center', 420)).set_duration(duration)

        # Audio envelope for lip bar
        try:
            samples = audio.to_soundarray(fps=24)
            rms = np.sqrt((samples.astype(float) ** 2).mean(axis=1))
            rms = (rms / (rms.max() or 1)).clip(0,1)
            def env(t):
                idx = int(min(len(rms)-1, max(0, t*24)))
                return float(rms[idx])
        except Exception:
            env = lambda t: 0.0

        # Lip bar (simple mouth sync)
        bar = Image.new('RGBA', (360, 22), (255, 60, 60, 220))
        bar_path = BASE / "temp" / "lipbar.png"
        bar_path.parent.mkdir(exist_ok=True)
        bar.save(bar_path)
        bar_clip = ImageClip(str(bar_path)).set_position(lambda t: (360, 1220)).set_duration(duration)
        bar_clip = bar_clip.resize(lambda t: (360, int(10 + 90*env(t))))
        bar_clip = bar_clip.set_opacity(0.85)

        # Scanlines overlay
        scan_path = BASE / "temp" / "scanlines_vhs.png"
        build_scanlines_png(scan_path)
        scan_clip = ImageClip(str(scan_path)).set_duration(duration).set_opacity(0.35)

        comp = CompositeVideoClip([bg, base, bar_clip, scan_clip], size=(1080,1920))
        temp_video = BASE / "temp" / f"mh_{int(time.time())}.mp4"
        temp_video.parent.mkdir(exist_ok=True)
        comp.write_videofile(str(temp_video), fps=24, codec='libx264', audio_codec='aac', bitrate='8000k', preset='medium', verbose=False, logger=None)
        comp.close(); bg.close(); audio.close()

        # VHS/analog glitch postprocess
        vhs = BASE / "temp" / f"vhs_{int(time.time())}.mp4"
        filter_str = (
            "curves=vintage,format=yuv420p,noise=alls=20:allf=t+u,"
            "tmix=frames=2,hue=s=0.9,signalstats,"
            "eq=contrast=1.3:brightness=-0.05:saturation=1.05,"
            "vignette=PI/8,drawbox=y=mod(n\\,10)*10:h=2:w=iw:color=black@0.4:t=fill"
        )
        subprocess.run(["ffmpeg","-y","-i",str(temp_video),"-vf",filter_str,str(vhs)], capture_output=True, timeout=300)
        if vhs.exists():
            os.replace(vhs, out)
        else:
            os.replace(temp_video, out)
        return Path(out).exists()
    except Exception as e:
        print("    [ERROR] Video:", e)
        return False

def gen():
    t = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"\n{'='*70}\nVIDEO {t}\n{'='*70}")
    h = random.choice(scrape())
    print(f"Headline: {h[:60]}")
    s = comedy(h)
    print(f"Script: {len(s)} chars (MAX HEADROOM STYLE)")
    ap = BASE / f"audio/mh_{t}.mp3"
    if not audio(s, ap):
        print("AUDIO FAILED"); return None
    vp = BASE / f"videos/MAXHEADROOM_{t}.mp4"
    if not video_max_headroom(ap, vp):
        print("VIDEO FAILED"); return None
    up = BASE / "uploaded" / f"ABE_MAXHEADROOM_{t}.mp4"
    up.parent.mkdir(parents=True, exist_ok=True)
    import shutil; shutil.copy2(vp, up)
    mb = up.stat().st_size / (1024*1024)
    print(f"{'='*70}\nSUCCESS: {up.name} ({mb:.1f}MB)\n{'='*70}")
    return str(up)

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    print(f"\nGENERATING {count} MAX HEADROOM ABE VIDEOS\n")
    success = 0
    for i in range(count):
        if gen(): success += 1
        if i < count-1:
            print("\nWaiting 15 seconds...\n"); time.sleep(15)
    print(f"\n{'='*70}\nCOMPLETE: {success}/{count}\n{'='*70}\n")
