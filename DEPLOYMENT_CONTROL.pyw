#!/usr/bin/env python3
"""
DEPLOYMENT CONTROL - Full Control Over Video Generation & Upload
No placeholders, no bullshit - real working controls
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
import threading
import subprocess
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("F:/AI_Oracle_Root/scarify/abraham_studio")

# Create dirs immediately - no placeholders
for d in ['audio', 'videos', 'youtube_ready']:
    (BASE_DIR / d).mkdir(parents=True, exist_ok=True)

class DeploymentControl(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("DEPLOYMENT CONTROL - Video Generator")
        self.geometry("1200x900")
        self.configure(bg='#0a0a0a')
        
        # State
        self.is_generating = False
        self.current_video = 0
        self.total_videos = 0
        
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header = tk.Label(
            self, text="DEPLOYMENT CONTROL",
            font=("Arial", 20, "bold"),
            bg='#0a0a0a', fg='#00ff00'
        )
        header.pack(pady=20)
        
        # Main container
        container = tk.Frame(self, bg='#0a0a0a')
        container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left: Settings
        left = tk.Frame(container, bg='#1a1a1a', padx=20, pady=20)
        left.pack(side='left', fill='both', padx=(0, 10))
        
        tk.Label(left, text="GENERATION SETTINGS", font=("Arial", 14, "bold"),
                bg='#1a1a1a', fg='white').pack(pady=(0, 20))
        
        # Number of videos
        tk.Label(left, text="Number of Videos:", bg='#1a1a1a', fg='white').pack(anchor='w')
        self.count_var = tk.IntVar(value=5)
        count_spin = ttk.Spinbox(left, from_=1, to=100, textvariable=self.count_var, width=10)
        count_spin.pack(anchor='w', pady=5)
        
        # Region
        tk.Label(left, text="Region:", bg='#1a1a1a', fg='white').pack(anchor='w', pady=(15, 0))
        self.region_var = tk.StringVar(value="USA National")
        region_combo = ttk.Combobox(left, textvariable=self.region_var,
                                   values=["USA National", "Texas", "California", "New York", "Florida"],
                                   width=25)
        region_combo.pack(anchor='w', pady=5)
        
        # Mode
        self.mode_var = tk.StringVar(value="Comedic")
        tk.Label(left, text="Voice Mode:", bg='#1a1a1a', fg='white').pack(anchor='w', pady=(15, 0))
        mode_combo = ttk.Combobox(left, textvariable=self.mode_var,
                                 values=["Comedic", "Serious", "Satirical"],
                                 width=25)
        mode_combo.pack(anchor='w', pady=5)
        
        # Engine
        self.engine_var = tk.StringVar(value="Fallback")
        tk.Label(left, text="Visual Engine:", bg='#1a1a1a', fg='white').pack(anchor='w', pady=(15, 0))
        engine_combo = ttk.Combobox(left, textvariable=self.engine_var,
                                   values=["Fallback", "Stability AI", "Pollo AI"],
                                   width=25)
        engine_combo.pack(anchor='w', pady=5)
        
        # Buttons
        btn_frame = tk.Frame(left, bg='#1a1a1a')
        btn_frame.pack(pady=30)
        
        self.generate_btn = tk.Button(
            btn_frame, text="GENERATE VIDEOS",
            command=self.start_generation,
            bg='#00ff00', fg='black',
            font=("Arial", 12, "bold"),
            padx=30, pady=15,
            cursor='hand2'
        )
        self.generate_btn.pack(pady=5)
        
        tk.Button(
            btn_frame, text="OPEN OUTPUT FOLDER",
            command=self.open_folder,
            bg='#444444', fg='white',
            font=("Arial", 10),
            padx=20, pady=10,
            cursor='hand2'
        ).pack(pady=5)
        
        tk.Button(
            btn_frame, text="UPLOAD TO YOUTUBE",
            command=self.upload_youtube,
            bg='#ff4444', fg='white',
            font=("Arial", 10, "bold"),
            padx=20, pady=10,
            cursor='hand2'
        ).pack(pady=5)
        
        self.cancel_btn = tk.Button(
            btn_frame, text="CANCEL",
            command=self.cancel,
            bg='#444444', fg='white',
            font=("Arial", 10),
            padx=20, pady=10,
            state='disabled',
            cursor='hand2'
        )
        self.cancel_btn.pack(pady=5)
        
        # Right: Output
        right = tk.Frame(container, bg='#1a1a1a')
        right.pack(side='right', fill='both', expand=True)
        
        tk.Label(right, text="OUTPUT LOG", font=("Arial", 14, "bold"),
                bg='#1a1a1a', fg='white').pack(pady=(0, 10))
        
        # Progress
        self.progress = ttk.Progressbar(right, length=400, mode='determinate')
        self.progress.pack(pady=10)
        
        self.progress_label = tk.Label(right, text="Ready", bg='#1a1a1a', fg='#00ff00')
        self.progress_label.pack()
        
        # Log
        log_frame = tk.Frame(right, bg='#0a0a0a')
        log_frame.pack(fill='both', expand=True, pady=10)
        
        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.log_text = tk.Text(
            log_frame,
            bg='#0a0a0a', fg='#00ff00',
            font=("Consolas", 9),
            yscrollcommand=scrollbar.set,
            wrap='word'
        )
        self.log_text.pack(fill='both', expand=True)
        scrollbar.config(command=self.log_text.yview)
        
        self.log("DEPLOYMENT CONTROL - Ready")
        self.log(f"Output folder: {BASE_DIR / 'youtube_ready'}")
    
    def log(self, message):
        self.log_text.insert('end', f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
        self.log_text.see('end')
        self.update()
    
    def start_generation(self):
        if self.is_generating:
            return
        
        self.is_generating = True
        self.current_video = 0
        self.total_videos = self.count_var.get()
        
        self.generate_btn.config(state='disabled')
        self.cancel_btn.config(state='normal')
        self.progress['maximum'] = self.total_videos
        self.progress['value'] = 0
        self.log_text.delete('1.0', 'end')
        
        self.log(f"Starting generation: {self.total_videos} videos")
        
        thread = threading.Thread(target=self.generate_batch, daemon=True)
        thread.start()
    
    def generate_batch(self):
        try:
            from TEST_GENERATE_ONE import generate_clean_script, generate_audio, generate_video
            
            headlines = [
                "Corrupt Government Officials - 69% Fear",
                "Cyber-Terrorism Surge - 55.9% Terrified",
                "Economic Collapse Imminent - 58.2% Fear",
                "Political Violence Escalates Nationwide",
                "Border Crisis Intensifies - Families Fleeing"
            ]
            
            for i in range(self.total_videos):
                if not self.is_generating:
                    break
                
                headline = headlines[i % len(headlines)]
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                
                self.log(f"\nGenerating video {i+1}/{self.total_videos}")
                self.progress_label.config(text=f"Video {i+1}/{self.total_videos}")
                
                # Script
                script = generate_clean_script(headline)
                self.log(f"Script: {script[:80]}...")
                
                # Audio
                audio_path = BASE_DIR / "audio" / f"dctrl_{timestamp}.mp3"
                if not generate_audio(script, audio_path):
                    self.log("FAILED: Audio")
                    continue
                self.log("OK: Audio")
                
                # Video
                video_path = BASE_DIR / "videos" / f"DCTRL_{timestamp}.mp4"
                if not generate_video(headline, audio_path, video_path):
                    self.log("FAILED: Video")
                    continue
                self.log("OK: Video")
                
                # Copy to ready
                youtube_path = BASE_DIR / "youtube_ready" / f"DCTRL_{timestamp}.mp4"
                import shutil
                shutil.copy2(video_path, youtube_path)
                self.log(f"READY: {youtube_path.name}")
                
                self.current_video += 1
                self.progress['value'] = self.current_video
                
                if i < self.total_videos - 1:
                    self.log("Waiting 3 seconds...")
                    import time
                    time.sleep(3)
            
            self.log(f"\nCOMPLETE: {self.current_video}/{self.total_videos} videos")
            messagebox.showinfo("Complete", f"Generated {self.current_video} videos!")
            
        except Exception as e:
            self.log(f"ERROR: {e}")
            messagebox.showerror("Error", str(e))
        finally:
            self.is_generating = False
            self.generate_btn.config(state='normal')
            self.cancel_btn.config(state='disabled')
            self.progress_label.config(text="Complete")
    
    def cancel(self):
        self.is_generating = False
        self.log("Cancelled by user")
    
    def open_folder(self):
        folder = BASE_DIR / "youtube_ready"
        if sys.platform == 'win32':
            os.startfile(folder)
        self.log(f"Opened: {folder}")
    
    def upload_youtube(self):
        folder = BASE_DIR / "youtube_ready"
        if not folder.exists():
            messagebox.showerror("Error", "No videos to upload")
            return
        
        videos = list(folder.glob('*.mp4'))
        if not videos:
            messagebox.showwarning("No Videos", "No videos in output folder")
            return
        
        # Open YouTube Studio
        url = "https://studio.youtube.com/video/upload"
        if sys.platform == 'win32':
            os.system(f'start {url}')
        
        self.log(f"Opening YouTube Studio ({len(videos)} videos ready)")

if __name__ == "__main__":
    app = DeploymentControl()
    app.mainloop()




