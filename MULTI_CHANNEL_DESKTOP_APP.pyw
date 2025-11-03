#!/usr/bin/env python3
"""
MULTI-CHANNEL EMPIRE - DESKTOP APP
GUI for managing multiple YouTube channels across different industries
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import sys
from pathlib import Path
from datetime import datetime
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
from MULTI_CHANNEL_EMPIRE_SYSTEM import CHANNEL_TEMPLATES, MultiChannelManager

class MultiChannelApp:
    """Desktop app for multi-channel management"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Channel Empire - Industry Selector")
        self.root.geometry("900x700")
        self.root.configure(bg='#1a1a1a')
        
        self.manager = MultiChannelManager()
        self.selected_channel = None
        
        self.create_ui()
    
    def create_ui(self):
        """Create UI layout"""
        # Title
        title_frame = tk.Frame(self.root, bg='#1a1a1a')
        title_frame.pack(fill=tk.X, padx=20, pady=10)
        
        title = tk.Label(
            title_frame,
            text="MULTI-CHANNEL EMPIRE",
            font=("Arial", 24, "bold"),
            fg='#00ff00',
            bg='#1a1a1a'
        )
        title.pack()
        
        subtitle = tk.Label(
            title_frame,
            text="Deploy Unlimited Channels Across All Industries",
            font=("Arial", 12),
            fg='#888888',
            bg='#1a1a1a'
        )
        subtitle.pack()
        
        # Main content area
        content_frame = tk.Frame(self.root, bg='#1a1a1a')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel: Channel selection
        left_panel = tk.Frame(content_frame, bg='#2a2a2a', relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(
            left_panel,
            text="SELECT INDUSTRY / TOPIC",
            font=("Arial", 14, "bold"),
            fg='#00ccff',
            bg='#2a2a2a'
        ).pack(pady=10)
        
        # Industry dropdown
        self.industry_var = tk.StringVar()
        industry_dropdown = ttk.Combobox(
            left_panel,
            textvariable=self.industry_var,
            values=list(CHANNEL_TEMPLATES.keys()),
            state="readonly",
            font=("Arial", 11),
            width=30
        )
        industry_dropdown.pack(pady=10, padx=10)
        industry_dropdown.bind("<<ComboboxSelected>>", self.on_industry_selected)
        
        # Channel details
        details_frame = tk.Frame(left_panel, bg='#2a2a2a')
        details_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.details_text = scrolledtext.ScrolledText(
            details_frame,
            width=40,
            height=15,
            font=("Consolas", 10),
            bg='#1a1a1a',
            fg='#00ff00',
            wrap=tk.WORD
        )
        self.details_text.pack(fill=tk.BOTH, expand=True)
        
        # Right panel: Actions
        right_panel = tk.Frame(content_frame, bg='#2a2a2a', relief=tk.RAISED, bd=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(
            right_panel,
            text="CHANNEL ACTIONS",
            font=("Arial", 14, "bold"),
            fg='#00ccff',
            bg='#2a2a2a'
        ).pack(pady=10)
        
        # Video count
        count_frame = tk.Frame(right_panel, bg='#2a2a2a')
        count_frame.pack(pady=10)
        
        tk.Label(
            count_frame,
            text="Videos to Generate:",
            font=("Arial", 11),
            fg='#ffffff',
            bg='#2a2a2a'
        ).pack(side=tk.LEFT, padx=5)
        
        self.video_count_var = tk.IntVar(value=10)
        video_count_spinbox = tk.Spinbox(
            count_frame,
            from_=1,
            to=1000,
            textvariable=self.video_count_var,
            font=("Arial", 11),
            width=10
        )
        video_count_spinbox.pack(side=tk.LEFT)
        
        # Episode start
        episode_frame = tk.Frame(right_panel, bg='#2a2a2a')
        episode_frame.pack(pady=10)
        
        tk.Label(
            episode_frame,
            text="Starting Episode #:",
            font=("Arial", 11),
            fg='#ffffff',
            bg='#2a2a2a'
        ).pack(side=tk.LEFT, padx=5)
        
        self.episode_start_var = tk.IntVar(value=1)
        episode_spinbox = tk.Spinbox(
            episode_frame,
            from_=1,
            to=99999,
            textvariable=self.episode_start_var,
            font=("Arial", 11),
            width=10
        )
        episode_spinbox.pack(side=tk.LEFT)
        
        # Action buttons
        button_frame = tk.Frame(right_panel, bg='#2a2a2a')
        button_frame.pack(pady=20)
        
        self.create_btn = tk.Button(
            button_frame,
            text="CREATE CHANNEL",
            command=self.create_channel,
            font=("Arial", 12, "bold"),
            bg='#00aa00',
            fg='white',
            width=20,
            height=2
        )
        self.create_btn.pack(pady=5)
        
        self.generate_btn = tk.Button(
            button_frame,
            text="GENERATE VIDEOS",
            command=self.generate_videos,
            font=("Arial", 12, "bold"),
            bg='#0066cc',
            fg='white',
            width=20,
            height=2
        )
        self.generate_btn.pack(pady=5)
        
        self.export_btn = tk.Button(
            button_frame,
            text="EXPORT TO SHEETS",
            command=self.export_sheets,
            font=("Arial", 12, "bold"),
            bg='#cc6600',
            fg='white',
            width=20,
            height=2
        )
        self.export_btn.pack(pady=5)
        
        self.list_btn = tk.Button(
            button_frame,
            text="LIST ALL CHANNELS",
            command=self.list_channels,
            font=("Arial", 12, "bold"),
            bg='#666666',
            fg='white',
            width=20,
            height=2
        )
        self.list_btn.pack(pady=5)
        
        # Output log
        log_frame = tk.Frame(right_panel, bg='#2a2a2a')
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(
            log_frame,
            text="OUTPUT LOG",
            font=("Arial", 11, "bold"),
            fg='#00ccff',
            bg='#2a2a2a'
        ).pack()
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            width=40,
            height=10,
            font=("Consolas", 9),
            bg='#000000',
            fg='#00ff00',
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
    
    def log(self, message: str, color: str = "#00ff00"):
        """Log message to output"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def on_industry_selected(self, event=None):
        """Update details when industry selected"""
        industry = self.industry_var.get()
        
        if industry not in CHANNEL_TEMPLATES:
            return
        
        template = CHANNEL_TEMPLATES[industry]
        
        # Display details
        self.details_text.delete(1.0, tk.END)
        
        details = f"""
CHANNEL: {template['name']}

DESCRIPTION:
{template['description']}

STYLE:
{template['style']}

SCRIPT TYPE:
{template['script_type']}

VOICE ID:
{template['voice_id']}

TAGS:
{', '.join(template['tags'])}

HASHTAGS:
{' '.join(template['hashtags'])}

MONETIZATION:
- Cash App QR code (mandatory)
- YouTube ads (once eligible)
- Affiliate links
- Multi-platform revenue

TARGET AUDIENCE:
- Niche: {industry.replace('_', ' ').title()}
- Demographics: Varies by topic
- Platform: YouTube Shorts, TikTok, Rumble
"""
        
        self.details_text.insert(tk.END, details)
        self.selected_channel = industry
    
    def create_channel(self):
        """Create new channel"""
        if not self.selected_channel:
            messagebox.showwarning("No Selection", "Please select an industry first")
            return
        
        self.log(f"Creating channel: {self.selected_channel}", "#00ccff")
        
        channel_dir = self.manager.create_channel(self.selected_channel)
        
        if channel_dir:
            self.log(f"Channel created: {channel_dir.name}", "#00ff00")
            messagebox.showinfo("Success", f"Channel created successfully!\n\n{channel_dir}")
        else:
            self.log(f"Failed to create channel", "#ff0000")
            messagebox.showerror("Error", "Channel creation failed")
    
    def generate_videos(self):
        """Generate videos for selected channel"""
        if not self.selected_channel:
            messagebox.showwarning("No Selection", "Please select an industry first")
            return
        
        count = self.video_count_var.get()
        episode_start = self.episode_start_var.get()
        
        self.log(f"Generating {count} videos for {self.selected_channel}...", "#00ccff")
        
        # Get channel config
        template = CHANNEL_TEMPLATES[self.selected_channel]
        safe_name = template["name"].replace(" ", "_").replace("'", "").lower()
        channel_dir = self.manager.channels_dir / safe_name
        
        # Ensure channel exists
        if not channel_dir.exists():
            self.log("Channel doesn't exist, creating...", "#ffaa00")
            channel_dir = self.manager.create_channel(self.selected_channel)
        
        # Generate videos
        self.log(f"Starting generation: Episodes {episode_start} to {episode_start + count - 1}", "#ffffff")
        
        # Run generation script
        for i in range(count):
            episode_num = episode_start + i
            
            self.log(f"[{i+1}/{count}] Generating Episode #{episode_num}...", "#ffffff")
            
            # Run main generator with channel-specific config
            env = os.environ.copy()
            env["EPISODE_NUM"] = str(episode_num)
            env["VOICE_ID"] = template["voice_id"]
            env["CHANNEL_STYLE"] = template["style"]
            env["SCRIPT_TYPE"] = template["script_type"]
            
            try:
                result = subprocess.run(
                    [sys.executable, "abraham_MAX_HEADROOM.py", "1"],
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=600
                )
                
                if result.returncode == 0:
                    self.log(f"  [OK] Episode #{episode_num} complete", "#00ff00")
                else:
                    self.log(f"  [ERROR] Episode #{episode_num} failed", "#ff0000")
            except Exception as e:
                self.log(f"  [ERROR] {str(e)}", "#ff0000")
        
        self.log(f"\n[COMPLETE] Generated {count} videos", "#00ff00")
        messagebox.showinfo("Complete", f"Generated {count} videos for {self.selected_channel}")
    
    def export_sheets(self):
        """Export channels to Google Sheets"""
        self.log("Exporting to Google Sheets...", "#00ccff")
        
        try:
            self.manager.export_to_google_sheets()
            self.log("[OK] Exported to Google Sheets", "#00ff00")
            messagebox.showinfo("Success", "Channels exported to Google Sheets")
        except Exception as e:
            self.log(f"[ERROR] {str(e)}", "#ff0000")
            messagebox.showerror("Error", f"Export failed: {e}")
    
    def list_channels(self):
        """List all created channels"""
        self.log("Loading channels...", "#00ccff")
        
        channels = self.manager.list_channels()
        
        if not channels:
            self.log("No channels created yet", "#ffaa00")
            messagebox.showinfo("No Channels", "No channels created yet.\n\nSelect an industry and click CREATE CHANNEL")
            return
        
        self.log(f"\n[ACTIVE CHANNELS: {len(channels)}]", "#00ff00")
        
        for i, channel in enumerate(channels, 1):
            self.log(f"  {i}. {channel['name']}", "#ffffff")
            self.log(f"     Template: {channel['template']}", "#888888")
            self.log(f"     Videos: {channel['videos']}", "#888888")
        
        # Show in dialog
        channel_list = "\n".join([
            f"{i}. {ch['name']} - {ch['videos']} videos"
            for i, ch in enumerate(channels, 1)
        ])
        
        messagebox.showinfo(
            "Active Channels",
            f"Total Channels: {len(channels)}\n\n{channel_list}"
        )


def main():
    """Launch desktop app"""
    root = tk.Tk()
    app = MultiChannelApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()



