#!/usr/bin/env python3
"""
ABRAHAM STUDIO - Complete Desktop App
Region-Based | Multi-Language | Batch Control | Halloween 2025 Optimized
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
import sys
import threading
import json
import random
import time
import subprocess
from pathlib import Path
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

BASE_DIR = Path("F:/AI_Oracle_Root/scarify/abraham_studio")

# EMBEDDED API KEYS
POLLO_API_KEY = "pollo_5EW9VjxB2eAUknmhd9vb9F2OJFDjPVVZttOQJRaaQ248"
ELEVENLABS_API_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
STABILITY_API_KEY = "sk-sP9EO0Ybb3L7SfGbpEtfrmOIhXVf8DdK9eSaTSBuTcNhjpQi"

# ============================================================================
# REGION-BASED HEADLINES
# ============================================================================

REGIONS = {
    "USA (National)": {
        "headlines": [
            "Corrupt Government Officials - 69% Fear",
            "Cyber-Terrorism Surge - 55.9% Terrified",
            "Economic Collapse Imminent - 58.2% Fear",
            "Political Violence Escalates Nationwide"
        ],
        "language": "en"
    },
    "USA - Texas": {
        "headlines": [
            "Border Crisis Intensifies - Families Fleeing",
            "Wildfires Rage Across State - Evacuations",
            "ICE Raids Target Communities",
            "Power Grid Failures - Blackouts Expected"
        ],
        "language": "en"
    },
    "USA - California": {
        "headlines": [
            "Wildfires Threaten Entire Communities",
            "Homeless Crisis Explodes - Streets Overflow",
            "Power Outages Force Business Shutdowns",
            "Earthquake Risk Spikes - Big One Coming"
        ],
        "language": "en"
    },
    "USA - New York": {
        "headlines": [
            "Subway Attacks Increase 300% - Riders Terrified",
            "Housing Costs Force Families Out",
            "Cybersecurity Breach - Millions At Risk",
            "Extreme Weather Threatens Infrastructure"
        ],
        "language": "en"
    },
    "USA - Florida": {
        "headlines": [
            "Hurricane Threat Forces Evacuations",
            "Rising Sea Levels - Properties Sinking",
            "Insurance Companies Flee State - Crisis",
            "Extreme Heat Breaks Records - Emergency"
        ],
        "language": "en"
    },
    "Spain": {
        "headlines": [
            "Crisis Económica - Desempleo Supera 15%",
            "Ola de Calor - Incendios Forestales",
            "Conflictos Políticos - Tensión Crece",
            "Crisis Migratoria - Estado Emergencia"
        ],
        "language": "es"
    },
    "Mexico": {
        "headlines": [
            "Crimen Organizado - Violencia Escalada",
            "Crisis de Sequía - Agua Falla",
            "Inflación Galopante - Precios Disparan",
            "Desastre Natural - Comunidades Devastadas"
        ],
        "language": "es"
    },
    "United Kingdom": {
        "headlines": [
            "Economic Recession Deepens - Millions Jobless",
            "Climate Crisis - Coastal Flooding",
            "Political Turmoil - Government Collapse Risk",
            "Cyber Attacks Target Infrastructure"
        ],
        "language": "en"
    },
    "Brazil": {
        "headlines": [
            "Crises Climáticas - Inundações Devastadoras",
            "Violência Urbana - Homicídio Disparam",
            "Recessão Econômica - Desemprego Alta",
            "Corrupção Política - Escândalos Expostos"
        ],
        "language": "pt"
    },
    "Germany": {
        "headlines": [
            "Energiekrise - Blackouts Drohen",
            "Inflationsanstieg - Preise Steigen",
            "Klimakatastrophe - Extreme Wetter",
            "Cybersicherheit - Angriffe Infrastruktur"
        ],
        "language": "de"
    }
}

# ============================================================================
# GORE ELEMENTS
# ============================================================================

GORE = [
    "occiput explosion, brain spray, bone shards",
    "jaw unhinged, fingers squelch gray matter",
    "skull fragments grind, rotting flesh",
    "derringer execution, bone shrapnel",
    "corpse-dragging butcher, blood stench"
]

# ============================================================================
# DESKTOP APP
# ============================================================================

class AbrahamStudio(tk.Tk):
    """Main Desktop Application"""
    
    def __init__(self):
        super().__init__()
        
        self.title("🎃 ABRAHAM STUDIO - Halloween 2025")
        self.geometry("1000x800")
        self.resizable(True, True)
        
        # Theme
        self.configure(bg='#1a0000')
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background='#1a0000', foreground='white')
        style.configure('TFrame', background='#1a0000')
        style.configure('TLabelframe', background='#1a0000', foreground='white')
        style.configure('TLabelframe.Label', background='#1a0000', foreground='#ff0000')
        
        # Variables
        self.region_var = tk.StringVar(value="USA (National)")
        self.count_var = tk.IntVar(value=5)
        self.engine_var = tk.StringVar(value="stability")
        self.adult_var = tk.BooleanVar(value=True)
        
        self.is_generating = False
        self.cancel_requested = False
        
        self.create_widgets()
        self.update_region_info()
    
    def create_widgets(self):
        """Create GUI"""
        
        # Header
        header = tk.Label(
            self,
            text="🩸 ABRAHAM STUDIO - HARDCORE VIDEO GENERATOR",
            font=("Arial", 18, "bold"),
            bg='#1a0000',
            fg='#ff0000'
        )
        header.pack(pady=15)
        
        # Region Selection
        region_frame = ttk.LabelFrame(self, text="🌍 REGION & HEADLINES", padding=15)
        region_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(region_frame, text="Select Region:").grid(row=0, column=0, sticky="w", pady=5)
        
        self.region_combo = ttk.Combobox(
            region_frame,
            textvariable=self.region_var,
            values=list(REGIONS.keys()),
            state="readonly",
            width=40
        )
        self.region_combo.grid(row=0, column=1, sticky="ew", padx=10)
        self.region_combo.bind('<<ComboboxSelected>>', lambda e: self.update_region_info())
        
        ttk.Label(region_frame, text="Language:").grid(row=1, column=0, sticky="w", pady=5)
        self.language_label = ttk.Label(region_frame, text="EN", font=("Arial", 12, "bold"))
        self.language_label.grid(row=1, column=1, sticky="w", padx=10)
        
        ttk.Label(region_frame, text="Headlines:").grid(row=2, column=0, sticky="nw", pady=5)
        
        self.headlines_text = scrolledtext.ScrolledText(
            region_frame,
            height=4,
            width=50,
            wrap=tk.WORD,
            bg='#2a0000',
            fg='white'
        )
        self.headlines_text.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        region_frame.columnconfigure(1, weight=1)
        
        # Generation Settings
        settings_frame = ttk.LabelFrame(self, text="⚙️ GENERATION SETTINGS", padding=15)
        settings_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(settings_frame, text="Batch Count:").grid(row=0, column=0, sticky="w", pady=5)
        count_spin = ttk.Spinbox(
            settings_frame,
            from_=1,
            to=50,
            textvariable=self.count_var,
            width=10
        )
        count_spin.grid(row=0, column=1, sticky="w", padx=10)
        ttk.Label(settings_frame, text="videos (1-50)").grid(row=0, column=2, sticky="w")
        
        ttk.Label(settings_frame, text="Engine:").grid(row=1, column=0, sticky="w", pady=5)
        engine_combo = ttk.Combobox(
            settings_frame,
            textvariable=self.engine_var,
            values=["stability", "pollo", "both"],
            state="readonly",
            width=15
        )
        engine_combo.grid(row=1, column=1, sticky="w", padx=10)
        ttk.Label(settings_frame, text="(Stability recommended)").grid(row=1, column=2, sticky="w")
        
        adult_check = ttk.Checkbutton(
            settings_frame,
            text="🩸 Adult Gore Mode (hardcore scripts)",
            variable=self.adult_var
        )
        adult_check.grid(row=2, column=0, columnspan=3, sticky="w", pady=10)
        
        # Halloween Stats
        stats_frame = ttk.LabelFrame(self, text="🎃 HALLOWEEN 2025 OPTIMIZATION", padding=15)
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        tips = [
            "✓ Viral-optimized titles for max engagement",
            "✓ Fear-based keywords (69% fear triggers)",
            "✓ Historical horror boosts shares",
            "✓ 15-second duration for Shorts algorithm",
            "✓ Region-specific content = local relevance"
        ]
        
        for tip in tips:
            label = ttk.Label(stats_frame, text=tip, font=("Arial", 9))
            label.pack(anchor="w", pady=2)
        
        # Control Buttons
        button_frame = tk.Frame(self, bg='#1a0000')
        button_frame.pack(fill="x", padx=20, pady=15)
        
        self.generate_btn = tk.Button(
            button_frame,
            text="🚀 GENERATE VIDEOS",
            command=self.start_generation,
            bg='#ff0000',
            fg='white',
            font=("Arial", 14, "bold"),
            padx=20,
            pady=10
        )
        self.generate_btn.pack(side="left", padx=5)
        
        tk.Button(
            button_frame,
            text="📁 Open Output",
            command=self.open_folder,
            bg='#333333',
            fg='white',
            font=("Arial", 10),
            padx=15,
            pady=10
        ).pack(side="left", padx=5)
        
        self.cancel_btn = tk.Button(
            button_frame,
            text="❌ Cancel",
            command=self.cancel,
            bg='#333333',
            fg='white',
            font=("Arial", 10),
            padx=15,
            pady=10,
            state="disabled"
        )
        self.cancel_btn.pack(side="left", padx=5)
        
        # Progress
        self.progress = ttk.Progressbar(self, length=600, mode='determinate')
        self.progress.pack(padx=20, pady=10)
        
        self.progress_label = tk.Label(
            self,
            text="Ready to generate",
            bg='#1a0000',
            fg='white',
            font=("Arial", 10)
        )
        self.progress_label.pack()
        
        # Log
        log_frame = ttk.LabelFrame(self, text="📋 GENERATION LOG", padding=10)
        log_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=12,
            wrap=tk.WORD,
            bg='#0a0000',
            fg='#00ff00',
            font=("Consolas", 9)
        )
        self.log_text.pack(fill="both", expand=True)
    
    def update_region_info(self):
        """Update region info display"""
        region = self.region_var.get()
        if region in REGIONS:
            config = REGIONS[region]
            
            # Update language
            lang = config["language"].upper()
            self.language_label.config(text=lang)
            
            # Update headlines
            self.headlines_text.delete(1.0, tk.END)
            headlines = "\n".join([f"• {h}" for h in config["headlines"]])
            self.headlines_text.insert(1.0, headlines)
    
    def log(self, message):
        """Add to log"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.update()
    
    def start_generation(self):
        """Start generation in background"""
        if self.is_generating:
            return
        
        self.is_generating = True
        self.cancel_requested = False
        self.generate_btn.config(state="disabled")
        self.cancel_btn.config(state="normal")
        self.progress["value"] = 0
        self.progress["maximum"] = self.count_var.get()
        self.log_text.delete(1.0, tk.END)
        
        thread = threading.Thread(target=self.run_generation, daemon=True)
        thread.start()
    
    def run_generation(self):
        """Run generation process"""
        try:
            self.log("╔═══════════════════════════════════════════════════════════╗")
            self.log("║   🩸 ABRAHAM STUDIO - GENERATION STARTED                ║")
            self.log("╚═══════════════════════════════════════════════════════════╝\n")
            
            region = self.region_var.get()
            count = self.count_var.get()
            engine = self.engine_var.get()
            adult = self.adult_var.get()
            
            self.log(f"Region: {region}")
            self.log(f"Count: {count} videos")
            self.log(f"Engine: {engine}")
            self.log(f"Mode: {'ADULT GORE' if adult else 'STANDARD'}\n")
            
            # Generate videos
            results = self.generate_batch(region, count, engine, adult)
            
            self.log("\n╔═══════════════════════════════════════════════════════════╗")
            self.log(f"║   ✅ COMPLETE: {len(results)}/{count} VIDEOS             ")
            self.log("╚═══════════════════════════════════════════════════════════╝\n")
            
            messagebox.showinfo("Success", f"Generated {len(results)} videos!\n\nCheck youtube_ready folder.")
            
        except Exception as e:
            self.log(f"\n❌ ERROR: {e}")
            messagebox.showerror("Error", f"Generation failed:\n{e}")
        finally:
            self.is_generating = False
            self.generate_btn.config(state="normal")
            self.cancel_btn.config(state="disabled")
            self.progress["value"] = self.progress["maximum"]
            self.progress_label.config(text="Complete!")
    
    def generate_batch(self, region, count, engine, adult_mode):
        """Generate batch using embedded Python"""
        
        results = []
        region_config = REGIONS[region]
        
        for i in range(count):
            if self.cancel_requested:
                self.log("\n❌ CANCELLED BY USER")
                break
            
            self.log(f"\n{'='*60}")
            self.log(f"VIDEO {i+1}/{count}")
            self.log(f"{'='*60}")
            
            self.progress_label.config(text=f"Generating {i+1}/{count}...")
            
            # Generate one video
            result = self.generate_one_video(region_config, engine, adult_mode)
            
            if result:
                results.append(result)
                self.progress.step()
            
            if i < count - 1 and not self.cancel_requested:
                self.log("Waiting 5 seconds...")
                time.sleep(5)
        
        return results
    
    def generate_one_video(self, region_config, engine, adult_mode):
        """Generate single video"""
        
        # Get headline
        headline = random.choice(region_config["headlines"])
        self.log(f"📰 Headline: {headline}")
        
        # Generate script
        script = self.generate_script(headline, adult_mode)
        self.log(f"📝 Script: {len(script)} chars")
        
        # Generate audio
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        audio_path = BASE_DIR / "audio" / f"abraham_{timestamp}.mp3"
        
        if not self.generate_audio(script, audio_path):
            self.log("❌ Audio failed")
            return None
        
        # Generate video
        video_path = BASE_DIR / "videos" / f"ABRAHAM_{timestamp}.mp4"
        
        if engine == "stability":
            success = self.generate_video_stability(script, audio_path, video_path)
        else:
            success = False
        
        if not success:
            self.log("❌ Video failed")
            return None
        
        # Prepare for YouTube
        youtube_file = self.prepare_youtube(video_path, headline, script, adult_mode)
        
        self.log(f"✅ Complete: {youtube_file.name}")
        
        return str(youtube_file)
    
    def generate_script(self, headline, adult_mode):
        """Generate CLEAN script - NO VIDEO DESCRIPTIONS, ONLY COMEDIC CONTENT"""
        # Comedic satirical style (Dolemite/Pryor/Chappelle)
        openings = [
            "Now hold up, hold up. Let me tell y'all something real quick.",
            "Aight, look here. I'm watching this mess unfold and I got thoughts.",
            "You know what? I'm dead, but this here got me spinning in my grave.",
            "Listen, I ain't even supposed to be talking but this right here?",
            "Hold on now, let me break this down for you real simple like.",
            "Nah, forreal though. Y'all seein' this same mess I'm seein'?"
        ]
        
        observations = [
            "This is wild, man. Straight wild.",
            "Y'all really out here doing the most, huh?",
            "I'm telling you, this country done lost its mind.",
            "See, this is why I fought the war. Now look at us.",
            "Man, this is crazier than a soup sandwich.",
            "Hold on, let me make sure I heard that right.",
            "This is the kind of mess that got me coming back from the dead."
        ]
        
        rants = [
            "Sic semper tyrannis. That means thus always to tyrants, in case y'all forgot.",
            "I'm Abe Lincoln, man. The real Abe. And I'm telling you, this ain't it.",
            "Purge the corruption. That's the move. Ain't no other way.",
            "From the grave, I'm watching. And y'all better listen up.",
            "I came back for a reason. This is it right here."
        ]
        
        opening = random.choice(openings)
        observation = random.choice(observations)
        rant = random.choice(rants)
        
        # Clean script - ONLY what Abe says, nothing about video effects
        template = f"{opening} {headline}. {observation} {rant}"
        
        # Ensure script is clean - remove any accidental video description text
        template = template.strip()
        
        # Remove common video description phrases that might leak in
        video_description_phrases = [
            "tv static", "pop effect", "glitch", "zoom", "fade",
            "9:16", "1080x1920", "aspect ratio", "video quality",
            "visual effect", "static overlay", "noise", "distortion"
        ]
        
        words = template.split()
        clean_words = [w for w in words if not any(phrase in w.lower() for phrase in video_description_phrases)]
        template = " ".join(clean_words)
        
        return template
    
    def generate_audio(self, script, output_path):
        """Generate audio with ElevenLabs"""
        self.log("🎙️ Voice generation...")
        
        try:
            import requests
            
            url = f"https://api.elevenlabs.io/v1/text-to-speech/7aavy6c5cYIloDVj2JvH"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": ELEVENLABS_API_KEY
            }
            
            # COMEDIC SETTINGS - More expressive, animated like Dolemite/Pryor/Chappelle
            data = {
                "text": script,  # CLEAN SCRIPT ONLY - NO VIDEO DESCRIPTIONS
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.3,  # Lower = more expressive/comedic
                    "similarity_boost": 0.8,
                    "style": 0.95,  # Higher = more animated/performative
                    "use_speaker_boost": True
                }
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=120)
            
            if response.status_code == 200:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                self.log("   ✅ ElevenLabs voice")
                return True
            
        except Exception as e:
            self.log(f"   ⚠️ Error: {e}")
        
        return False
    
    def generate_video_stability(self, script, audio_path, output_path):
        """Generate video with Stability AI"""
        self.log("🎬 Stability AI generation...")
        
        try:
            import requests
            
            url = "https://api.stability.ai/v2beta/stable-image/generate/ultra"
            
            headers = {
                "authorization": f"Bearer {STABILITY_API_KEY}",
                "accept": "image/*"
            }
            
            # Visual prompt for Abe (SEPARATE from audio script - will NOT be read aloud)
            visual_prompt = "Abraham Lincoln portrait, vintage photograph, serious expression, 9:16 vertical"
            
            files = {
                "prompt": (None, visual_prompt),  # VISUAL ONLY, NOT IN AUDIO
                "output_format": (None, "png"),
                "aspect_ratio": (None, "9:16")
            }
            
            response = requests.post(url, headers=headers, files=files, timeout=180)
            
            if response.status_code != 200:
                self.log(f"   ❌ Stability error: {response.status_code}")
                return False
            
            # Save image
            image_path = output_path.with_suffix('.png')
            with open(image_path, 'wb') as f:
                f.write(response.content)
            
            self.log("   ✅ Image generated")
            
            # Create video with FFmpeg
            self.log("   🎬 Creating video...")
            
            # Create base video first
            cmd = [
                'ffmpeg', '-loop', '1', '-i', str(image_path),
                '-i', str(audio_path),
                '-t', '15',
                '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p',
                '-vf', 'scale=1080:1920,zoompan=z=\'min(zoom+0.0015,1.5)\':d=360:s=1080x1920',
                '-c:a', 'aac',
                '-shortest', '-y', str(output_path)
            ]
            
            subprocess.run(cmd, capture_output=True, check=True)
            
            # ADD TV STATIC EFFECT with Abe's face
            self.log("   Adding TV static overlay...")
            static_output = output_path.with_name(f"{output_path.stem}_temp_static.mp4")
            
            try:
                # Create static noise overlay
                static_cmd = [
                    'ffmpeg', '-f', 'lavfi', '-i', 'testsrc=duration=15:size=1080x1920:rate=30',
                    '-f', 'lavfi', '-i', 'noise=alls=30:allf=t+u',
                    '-filter_complex',
                    '[0:v][1:v]blend=all_mode=screen:all_opacity=0.3[static]',
                    '-map', '[static]', '-t', '15', '-pix_fmt', 'yuv420p', '-y', str(BASE_DIR / "temp_static.mp4")
                ]
                
                subprocess.run(static_cmd, capture_output=True, check=True, timeout=30)
                
                # Overlay static on main video
                overlay_cmd = [
                    'ffmpeg', '-i', str(output_path),
                    '-i', str(BASE_DIR / "temp_static.mp4"),
                    '-filter_complex', '[0:v][1:v]blend=all_mode=screen:all_opacity=0.4[v]',
                    '-map', '[v]', '-map', '0:a', '-c:v', 'libx264', '-c:a', 'copy',
                    '-shortest', '-y', str(static_output)
                ]
                
                subprocess.run(overlay_cmd, capture_output=True, check=True, timeout=30)
                
                # Replace original with static version
                output_path.unlink()
                static_output.rename(output_path)
                
                # Cleanup
                if (BASE_DIR / "temp_static.mp4").exists():
                    (BASE_DIR / "temp_static.mp4").unlink()
                
                self.log("   TV static effect applied")
            except Exception as static_error:
                self.log(f"   Static effect skipped: {static_error}")
            
            image_path.unlink()
            
            self.log("   ✅ Video ready")
            return True
            
        except Exception as e:
            self.log(f"   ❌ Error: {e}")
            return False
    
    def prepare_youtube(self, video_path, headline, script, adult_mode):
        """Prepare for YouTube"""
        youtube_dir = BASE_DIR / "youtube_ready"
        youtube_dir.mkdir(parents=True, exist_ok=True)
        
        youtube_file = youtube_dir / video_path.name
        
        import shutil
        shutil.copy2(video_path, youtube_file)
        
        metadata = {
            'title': f"LINCOLN: {headline[:40].upper()}",
            'description': f"""🩸 {headline}

{script}

🎃 HALLOWEEN 2025
#Halloween2025 #AbrahamLincoln #Horror""",
            'tags': ['halloween', 'horror', 'lincoln']
        }
        
        with open(youtube_file.with_suffix('.json'), 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return youtube_file
    
    def open_folder(self):
        """Open output folder"""
        folder = BASE_DIR / "youtube_ready"
        folder.mkdir(parents=True, exist_ok=True)
        
        if sys.platform == 'win32':
            os.startfile(folder)
    
    def cancel(self):
        """Cancel generation"""
        self.cancel_requested = True
        self.log("\n⚠️ Cancellation requested...")


def main():
    """Launch app"""
    
    # Create directories
    (BASE_DIR / "audio").mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "videos").mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "youtube_ready").mkdir(parents=True, exist_ok=True)
    
    # Launch
    app = AbrahamStudio()
    app.mainloop()


if __name__ == "__main__":
    main()
