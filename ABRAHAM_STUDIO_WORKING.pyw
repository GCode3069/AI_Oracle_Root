"""
ABRAHAM STUDIO - COMPLETE WORKING VERSION
- Shows Abe Lincoln face on static TV
- Deep male voice (no female)
- No stage directions in speech
- Working GUI that generates videos
- Punches up AND down at everyone
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os, sys, json, requests, subprocess, random, time, threading
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

# Configuration
ELEVENLABS_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
BTC = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"

class AbrahamStudio:
    def __init__(self, root):
        self.root = root
        self.root.title("🔥 ABRAHAM STUDIO - MAX HEADROOM EDITION")
        self.root.geometry("900x700")
        self.root.configure(bg='#0a0a0a')
        
        self.generating = False
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title = tk.Label(self.root, text="🔥 ABRAHAM STUDIO 🔥", 
                        font=("Impact", 24), fg="#ff0000", bg="#0a0a0a")
        title.pack(pady=10)
        
        subtitle = tk.Label(self.root, text="Abraham Lincoln Roasts Headlines on Static TV", 
                           font=("Arial", 12), fg="#ffffff", bg="#0a0a0a")
        subtitle.pack()
        
        # Settings Frame
        settings = tk.Frame(self.root, bg="#1a1a1a", relief=tk.RIDGE, bd=2)
        settings.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(settings, text="Batch Count:", font=("Arial", 11), 
                fg="#ffffff", bg="#1a1a1a").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        
        self.count_var = tk.StringVar(value="10")
        count_spin = tk.Spinbox(settings, from_=1, to=100, textvariable=self.count_var,
                               font=("Arial", 11), width=10)
        count_spin.grid(row=0, column=1, padx=10, pady=10)
        
        # Status Frame
        status_frame = tk.Frame(self.root, bg="#1a1a1a", relief=tk.RIDGE, bd=2)
        status_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(status_frame, text="📺 Generation Status:", font=("Arial", 12, "bold"),
                fg="#00ff00", bg="#1a1a1a").pack(anchor='w', padx=10, pady=5)
        
        self.status_text = tk.Text(status_frame, height=20, font=("Consolas", 9),
                                  bg="#000000", fg="#00ff00", insertbackground='#00ff00')
        self.status_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(self.status_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.status_text.yview)
        
        # Buttons
        btn_frame = tk.Frame(self.root, bg="#0a0a0a")
        btn_frame.pack(pady=10)
        
        self.gen_btn = tk.Button(btn_frame, text="🎬 GENERATE VIDEOS", 
                                font=("Arial", 14, "bold"), bg="#ff0000", fg="#ffffff",
                                command=self.start_generation, width=20, height=2)
        self.gen_btn.grid(row=0, column=0, padx=10)
        
        open_btn = tk.Button(btn_frame, text="📂 OPEN FOLDER",
                            font=("Arial", 12), bg="#333333", fg="#ffffff",
                            command=self.open_folder, width=15)
        open_btn.grid(row=0, column=1, padx=10)
        
        self.log("✅ Abraham Studio Ready!")
        self.log(f"📁 Output: {BASE / 'uploaded'}")
        
    def log(self, message):
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.root.update()
        
    def start_generation(self):
        if self.generating:
            messagebox.showwarning("Busy", "Already generating!")
            return
            
        count = int(self.count_var.get())
        self.gen_btn.config(state=tk.DISABLED, text="⏳ GENERATING...")
        self.generating = True
        
        thread = threading.Thread(target=self.generate_videos, args=(count,))
        thread.daemon = True
        thread.start()
        
    def generate_videos(self, count):
        try:
            self.log(f"\n🔥 STARTING GENERATION OF {count} VIDEOS 🔥\n")
            
            success = 0
            for i in range(count):
                self.log(f"{'='*60}")
                self.log(f"VIDEO {i+1}/{count}")
                self.log(f"{'='*60}")
                
                if self.generate_single_video():
                    success += 1
                    self.log(f"✅ SUCCESS! ({success}/{i+1})")
                else:
                    self.log(f"❌ FAILED ({success}/{i+1})")
                
                if i < count - 1:
                    self.log("Waiting 20 seconds...\n")
                    time.sleep(20)
            
            self.log(f"\n{'='*60}")
            self.log(f"🎉 COMPLETE: {success}/{count} VIDEOS GENERATED")
            self.log(f"{'='*60}\n")
            
            messagebox.showinfo("Complete!", f"Generated {success}/{count} videos!")
            
        except Exception as e:
            self.log(f"❌ ERROR: {e}")
            messagebox.showerror("Error", str(e))
        finally:
            self.generating = False
            self.gen_btn.config(state=tk.NORMAL, text="🎬 GENERATE VIDEOS")
    
    def generate_single_video(self):
        try:
            # 1. Scrape headline
            headlines = self.scrape_headlines()
            headline = random.choice(headlines)
            self.log(f"📰 Headline: {headline[:50]}...")
            
            # 2. Create script (NO stage directions)
            script = self.create_roast(headline)
            self.log(f"📝 Script: {len(script)} chars (clean)")
            
            # 3. Generate audio (MALE voice)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_path = BASE / f"audio/abe_{timestamp}.mp3"
            if not self.generate_audio(script, audio_path):
                return False
            self.log(f"🎤 Audio: DONE")
            
            # 4. Create video (Abe on TV)
            video_path = BASE / f"videos/ABE_{timestamp}.mp4"
            if not self.create_video(audio_path, video_path):
                return False
            self.log(f"📺 Video: DONE")
            
            # 5. Copy to uploaded
            final_path = BASE / "uploaded" / f"ABE_TV_{timestamp}.mp4"
            final_path.parent.mkdir(parents=True, exist_ok=True)
            import shutil
            shutil.copy2(video_path, final_path)
            
            mb = final_path.stat().st_size / (1024 * 1024)
            self.log(f"💾 Saved: {final_path.name} ({mb:.1f}MB)")
            
            return True
            
        except Exception as e:
            self.log(f"❌ Error: {e}")
            return False
    
    def scrape_headlines(self):
        try:
            r = requests.get("https://news.google.com/rss", timeout=10)
            if r.status_code == 200:
                soup = BeautifulSoup(r.content, 'xml')
                headlines = [item.title.text for item in soup.find_all('item')[:20] if item.title]
                if headlines:
                    return headlines
        except: pass
        return ["Trump Third Term", "Police Kill 64", "Climate Summit Fails"]
    
    def create_roast(self, headline):
        """Create script WITHOUT stage directions"""
        hl = headline.lower()
        
        if "trump" in hl:
            return f"""Abraham Lincoln here. Dead since 1865.

{headline}.

Trump. This billionaire born with gold spoon convinced POOR people he's one of them. The con of the century.

I grew up in log cabin. ACTUAL poverty. Split rails. Read by candlelight. EARNED everything.

This man? Inherited millions. Bankrupted casinos. You know how hard that is?

But YOU. You enable this. You worship a man who wouldn't piss on you if you were on fire.

He calls you poorly educated and you CHEER. He says he could shoot someone and you'd vote for him and you NOD.

You're not victims. You're VOLUNTEERS.

And the RICH around him? Senators? CEOs? You KNOW better. But you enable him because it's PROFITABLE.

You're ALL guilty. Rich man manipulating. Poor people believing. Elite enabling. Media profiting.

EVERYONE has blood on their hands.

April 14 1865. Booth shot me in the head. Nine hours dying.

I saw THIS. I saw YOU. I died believing in America. I was WRONG.

Stop pointing fingers. Look in mirrors.

Bitcoin {BTC}"""
        
        else:
            return f"""Abraham Lincoln here. The tall guy with beard. Got shot at theater.

{headline}.

Let me tell you who to blame: EVERYONE.

People with POWER doing NOTHING. People with MONEY hoarding it. People with PLATFORMS spreading lies.

And YOU. Regular people. You see problems but don't ACT. You see injustice and scroll past.

You have votes. Voices. CHOICES. But you choose NOTHING. Choose COMFORT. Choose DISTRACTION.

Rich people exploiting. Middle people enabling. Poor people suffering. Media profiting. Politicians lying.

EVERYONE plays their part in this hellscape.

Worst part? You'll watch this. Laugh. Share it. Then go back to doing NOTHING.

Booth shot me. Lead through brain. Nine hours dying.

I died believing in human progress. I was wrong about you.

You're ALL complicit. ALL guilty. ALL responsible.

Look in mirrors.

Bitcoin {BTC}"""
    
    def generate_audio(self, script, output_path):
        try:
            # Get male voice
            r = requests.get("https://api.elevenlabs.io/v1/voices",
                           headers={"xi-api-key": ELEVENLABS_KEY}, timeout=10)
            
            voice_id = "pNInz6obpgDQGcFmaJgB"  # Adam - deep male
            if r.status_code == 200:
                for voice in r.json()['voices']:
                    if 'adam' in voice['name'].lower():
                        voice_id = voice['voice_id']
                        break
            
            # Generate
            r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
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
                            timeout=240)
            
            if r.status_code == 200:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(r.content)
                return True
        except: pass
        return False
    
    def create_video(self, audio_path, output_path):
        try:
            from moviepy.editor import AudioFileClip, ImageClip, CompositeVideoClip, ColorClip
            from PIL import Image, ImageDraw
            import math
            
            audio = AudioFileClip(str(audio_path))
            duration = min(audio.duration, 60.0)
            
            abe_img = BASE / "temp" / "lincoln.jpg"
            if not abe_img.exists():
                abe_img.parent.mkdir(exist_ok=True)
                url = "https://upload.wikimedia.org/wikipedia/commons/a/ab/Abraham_Lincoln_O-77_matte_collodion_print.jpg"
                img_data = requests.get(url, timeout=30).content
                with open(abe_img, "wb") as f:
                    f.write(img_data)
            
            bg = ColorClip(size=(1080, 1920), color=(30, 20, 40), duration=duration).set_audio(audio)
            overlays = [bg]
            
            try:
                import numpy as np
                samples = audio.to_soundarray(fps=24)
                rms = np.sqrt((samples.astype(float) ** 2).mean(axis=1))
                rms = (rms / (rms.max() or 1)).clip(0, 1)
                def env(t):
                    idx = int(min(len(rms)-1, max(0, t*24)))
                    return float(rms[idx])
            except Exception:
                env = lambda t: 0.0
            
            base_w, base_h = 460, 600
            abe_base = ImageClip(str(abe_img)).resize((base_w, base_h))
            def size_fn(t):
                return (int(base_w * (1.0 + 0.05 * env(t))), int(base_h * (1.0 + 0.05 * env(t))))
            def pos_fn(t):
                return ((1080 - size_fn(t)[0]) // 2 + int(2 * math.sin(t*6.0)), 1050 + int(3 * math.sin(t*4.0)))
            abe_clip = abe_base.resize(lambda t: size_fn(t)).set_position(pos_fn).set_duration(duration).fadein(0.6).fadeout(0.6)
            overlays.append(abe_clip)
            
            try:
                scan = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
                draw = ImageDraw.Draw(scan)
                for y in range(0, 1920, 4):
                    draw.line([(0, y), (1080, y)], fill=(0, 0, 0, 70), width=2)
                scan_path = BASE / "temp" / f"scanlines_{int(time.time())}.png"
                scan.save(scan_path)
                scan_clip = ImageClip(str(scan_path)).set_opacity(0.3).set_duration(duration)
                overlays.append(scan_clip)
            except Exception:
                pass
            
            final = CompositeVideoClip(overlays, size=(1080, 1920))
            output_path.parent.mkdir(parents=True, exist_ok=True)
            final.write_videofile(str(output_path), fps=24, codec='libx264', audio_codec='aac', bitrate='8000k', preset='medium', verbose=False, logger=None)
            final.close(); bg.close()
            return output_path.exists()
        except Exception:
            pass
        return False
    
    def open_folder(self):
        folder = BASE / "uploaded"
        folder.mkdir(parents=True, exist_ok=True)
        os.startfile(folder)

if __name__ == "__main__":
    root = tk.Tk()
    app = AbrahamStudio(root)
    root.mainloop()
