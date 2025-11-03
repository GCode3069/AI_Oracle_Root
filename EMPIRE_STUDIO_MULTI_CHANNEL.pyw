#!/usr/bin/env python3
"""
EMPIRE STUDIO - MULTI-CHANNEL DESKTOP APP
Deploy unlimited YouTube channels across different industries
With Cash App QR + Battle Tracking + Google Sheets
"""
import os
import sys
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from pathlib import Path
from datetime import datetime
import threading
import subprocess

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from MULTI_CHANNEL_EMPIRE_SYSTEM import MultiChannelManager, CHANNEL_TEMPLATES
    from abraham_MAX_HEADROOM import (
        generate_script, generate_voice, generate_lincoln_face_pollo,
        create_max_headroom_video, upload_to_youtube, get_headlines
    )
    SYSTEM_READY = True
except ImportError as e:
    print(f"[Warning] Import error: {e}")
    SYSTEM_READY = False

class EmpireStudioApp:
    """Desktop app for multi-channel empire management"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("EMPIRE STUDIO - Multi-Channel Generator")
        self.root.geometry("900x700")
        self.root.configure(bg='#1a1a1a')
        
        self.manager = MultiChannelManager() if SYSTEM_READY else None
        self.is_generating = False
        self.base_dir = Path("F:/AI_Oracle_Root/scarify")
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create UI elements"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title = tk.Label(
            main_frame,
            text="🏆 EMPIRE STUDIO - MULTI-CHANNEL GENERATOR",
            font=('Arial', 16, 'bold'),
            bg='#1a1a1a',
            fg='#00ff00'
        )
        title.pack(pady=10)
        
        # Channel selection frame
        channel_frame = tk.LabelFrame(
            main_frame,
            text="1. SELECT CHANNEL TYPE",
            font=('Arial', 11, 'bold'),
            bg='#2a2a2a',
            fg='#00ffff',
            padx=10,
            pady=10
        )
        channel_frame.pack(fill=tk.X, pady=5)
        
        # Channel dropdown
        self.channel_var = tk.StringVar()
        channel_options = list(CHANNEL_TEMPLATES.keys()) if SYSTEM_READY else ["abraham_lincoln"]
        
        channel_dropdown = ttk.Combobox(
            channel_frame,
            textvariable=self.channel_var,
            values=channel_options,
            state='readonly',
            width=50,
            font=('Arial', 10)
        )
        channel_dropdown.pack(pady=5)
        channel_dropdown.current(0)
        
        # Show channel info
        self.info_label = tk.Label(
            channel_frame,
            text="",
            font=('Arial', 9),
            bg='#2a2a2a',
            fg='#cccccc',
            justify=tk.LEFT
        )
        self.info_label.pack(pady=5)
        
        # Update info when selection changes
        channel_dropdown.bind('<<ComboboxSelected>>', self.update_channel_info)
        self.update_channel_info(None)
        
        # Episode controls frame
        episode_frame = tk.LabelFrame(
            main_frame,
            text="2. EPISODE SETTINGS",
            font=('Arial', 11, 'bold'),
            bg='#2a2a2a',
            fg='#00ffff',
            padx=10,
            pady=10
        )
        episode_frame.pack(fill=tk.X, pady=5)
        
        # Episode number
        ep_row = tk.Frame(episode_frame, bg='#2a2a2a')
        ep_row.pack(fill=tk.X, pady=5)
        
        tk.Label(ep_row, text="Start Episode #:", bg='#2a2a2a', fg='white', font=('Arial', 10)).pack(side=tk.LEFT)
        self.episode_var = tk.StringVar(value="1000")
        tk.Entry(ep_row, textvariable=self.episode_var, width=10, font=('Arial', 10)).pack(side=tk.LEFT, padx=10)
        
        # Video count
        count_row = tk.Frame(episode_frame, bg='#2a2a2a')
        count_row.pack(fill=tk.X, pady=5)
        
        tk.Label(count_row, text="Videos to Generate:", bg='#2a2a2a', fg='white', font=('Arial', 10)).pack(side=tk.LEFT)
        self.count_var = tk.StringVar(value="5")
        tk.Entry(count_row, textvariable=self.count_var, width=10, font=('Arial', 10)).pack(side=tk.LEFT, padx=10)
        
        # Format selection
        format_row = tk.Frame(episode_frame, bg='#2a2a2a')
        format_row.pack(fill=tk.X, pady=5)
        
        tk.Label(format_row, text="Format:", bg='#2a2a2a', fg='white', font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.format_var = tk.StringVar(value="SHORT")
        tk.Radiobutton(format_row, text="SHORT (9-17s)", variable=self.format_var, value="SHORT",
                      bg='#2a2a2a', fg='white', selectcolor='#1a1a1a', font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(format_row, text="LONG (40-60s)", variable=self.format_var, value="LONG",
                      bg='#2a2a2a', fg='white', selectcolor='#1a1a1a', font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(format_row, text="BOTH", variable=self.format_var, value="BOTH",
                      bg='#2a2a2a', fg='white', selectcolor='#1a1a1a', font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
        
        # Features frame
        features_frame = tk.LabelFrame(
            main_frame,
            text="3. FEATURES (All Enabled)",
            font=('Arial', 11, 'bold'),
            bg='#2a2a2a',
            fg='#00ffff',
            padx=10,
            pady=10
        )
        features_frame.pack(fill=tk.X, pady=5)
        
        features_text = (
            "[OK] Cash App QR Code (600x600, scannable)\n"
            "[OK] Max Headroom VHS Effects\n"
            "[OK] Dark Satirical Comedy Scripts\n"
            "[OK] Auto-Upload to YouTube\n"
            "[OK] Google Sheets Tracking\n"
            "[OK] Battle Tracker Integration"
        )
        tk.Label(
            features_frame,
            text=features_text,
            font=('Arial', 9),
            bg='#2a2a2a',
            fg='#00ff00',
            justify=tk.LEFT
        ).pack()
        
        # Action buttons frame
        action_frame = tk.Frame(main_frame, bg='#1a1a1a')
        action_frame.pack(fill=tk.X, pady=10)
        
        self.generate_btn = tk.Button(
            action_frame,
            text="🚀 GENERATE VIDEOS",
            command=self.start_generation,
            bg='#00aa00',
            fg='white',
            font=('Arial', 12, 'bold'),
            width=20,
            height=2
        )
        self.generate_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(
            action_frame,
            text="⏹️ STOP",
            command=self.stop_generation,
            bg='#aa0000',
            fg='white',
            font=('Arial', 12, 'bold'),
            width=15,
            height=2,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            action_frame,
            text="📁 Open Output",
            command=self.open_output,
            bg='#0066cc',
            fg='white',
            font=('Arial', 10),
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        # Progress frame
        progress_frame = tk.LabelFrame(
            main_frame,
            text="4. PROGRESS",
            font=('Arial', 11, 'bold'),
            bg='#2a2a2a',
            fg='#00ffff',
            padx=10,
            pady=10
        )
        progress_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.progress_text = scrolledtext.ScrolledText(
            progress_frame,
            bg='#1a1a1a',
            fg='#00ff00',
            font=('Consolas', 9),
            height=15
        )
        self.progress_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            bg='#2a2a2a',
            fg='#00ff00',
            font=('Arial', 9),
            anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def update_channel_info(self, event):
        """Update channel info when selection changes"""
        if not SYSTEM_READY:
            return
        
        template_key = self.channel_var.get()
        if template_key in CHANNEL_TEMPLATES:
            template = CHANNEL_TEMPLATES[template_key]
            info = (
                f"Name: {template['name']}\n"
                f"Style: {template['style']}\n"
                f"Type: {template['script_type']}"
            )
            self.info_label.config(text=info)
    
    def log(self, message):
        """Log message to progress text"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.progress_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.progress_text.see(tk.END)
        self.root.update()
    
    def start_generation(self):
        """Start video generation in background thread"""
        if self.is_generating:
            messagebox.showwarning("Warning", "Generation already in progress!")
            return
        
        self.is_generating = True
        self.generate_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress_text.delete('1.0', tk.END)
        
        # Start generation thread
        thread = threading.Thread(target=self.generate_videos_thread, daemon=True)
        thread.start()
    
    def stop_generation(self):
        """Stop video generation"""
        self.is_generating = False
        self.generate_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.log("[STOPPED] Generation cancelled by user")
        self.status_var.set("Stopped")
    
    def generate_videos_thread(self):
        """Generate videos in background thread"""
        try:
            template_key = self.channel_var.get()
            start_episode = int(self.episode_var.get())
            count = int(self.count_var.get())
            video_format = self.format_var.get()
            
            self.log(f"[START] Generating {count} videos for {template_key}")
            self.log(f"[FORMAT] {video_format}")
            self.log(f"[EPISODES] #{start_episode}-#{start_episode+count-1}")
            self.log("")
            
            # Get channel config
            if template_key in CHANNEL_TEMPLATES:
                template = CHANNEL_TEMPLATES[template_key]
                self.log(f"[CHANNEL] {template['name']}")
                self.log(f"[STYLE] {template['style']}")
                self.log("")
            
            # Get headlines
            self.log("[HEADLINES] Fetching current headlines...")
            headlines = get_headlines()
            self.log(f"[OK] Got {len(headlines)} headlines")
            self.log("")
            
            # Generate videos
            for i in range(count):
                if not self.is_generating:
                    break
                
                episode_num = start_episode + i
                headline = headlines[i % len(headlines)]
                
                self.log(f"[{i+1}/{count}] Episode #{episode_num}: {headline[:40]}...")
                self.status_var.set(f"Generating {i+1}/{count}...")
                
                # Generate based on format
                formats_to_generate = []
                if video_format == "SHORT":
                    formats_to_generate = ["short"]
                elif video_format == "LONG":
                    formats_to_generate = ["long"]
                else:  # BOTH
                    formats_to_generate = ["short", "long"]
                
                for fmt in formats_to_generate:
                    try:
                        # Generate script
                        self.log(f"  [{fmt.upper()}] Generating script...")
                        if fmt == "short":
                            script = self.manager.generate_script(template_key, headline)
                        else:
                            # Longer script for long format
                            script = self.manager.generate_script(template_key, headline) * 3
                        
                        # Generate voice
                        self.log(f"  [{fmt.upper()}] Generating voice...")
                        audio_path = self.base_dir / "abraham_horror" / "audio" / f"{template_key}_{episode_num}_{fmt}.mp3"
                        
                        # Use template voice
                        os.environ['VOICE_ID'] = template['voice_id']
                        generate_voice(script, audio_path)
                        
                        if not audio_path.exists():
                            self.log(f"  [ERROR] Voice generation failed")
                            continue
                        
                        # Generate face image
                        self.log(f"  [{fmt.upper()}] Generating character image...")
                        face_path = generate_lincoln_face_pollo(headline)
                        
                        # Generate video
                        self.log(f"  [{fmt.upper()}] Generating video...")
                        video_filename = f"{template_key}_{episode_num}_{fmt}.mp4"
                        video_path = self.base_dir / "abraham_horror" / "uploaded" / video_filename
                        
                        success = create_max_headroom_video(
                            lincoln_image=face_path,
                            audio_path=audio_path,
                            output_path=video_path,
                            headline=headline,
                            use_lipsync=False,  # Faster
                        )
                        
                        if success and video_path.exists():
                            size_mb = video_path.stat().st_size / (1024 * 1024)
                            self.log(f"  [OK] Video created ({size_mb:.1f} MB)")
                            
                            # Upload to YouTube
                            self.log(f"  [UPLOAD] Uploading to YouTube...")
                            youtube_url = upload_to_youtube(str(video_path), headline, episode_num)
                            
                            if youtube_url:
                                self.log(f"  [OK] {youtube_url}")
                            else:
                                self.log(f"  [INFO] Upload skipped or failed")
                        else:
                            self.log(f"  [ERROR] Video generation failed")
                    
                    except Exception as e:
                        self.log(f"  [ERROR] {type(e).__name__}: {str(e)[:100]}")
                
                self.log("")
            
            self.log("[COMPLETE] All videos generated!")
            self.log("")
            self.log(f"[OUTPUT] Check: abraham_horror/uploaded/")
            self.status_var.set("Complete")
            
        except Exception as e:
            self.log(f"[ERROR] Generation failed: {e}")
            self.status_var.set("Error")
        
        finally:
            self.is_generating = False
            self.generate_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
    
    def open_output(self):
        """Open output directory"""
        output_dir = self.base_dir / "abraham_horror" / "uploaded"
        if output_dir.exists():
            os.startfile(str(output_dir))
        else:
            messagebox.showinfo("Info", "No output directory yet")

def main():
    """Launch desktop app"""
    root = tk.Tk()
    app = EmpireStudioApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()



