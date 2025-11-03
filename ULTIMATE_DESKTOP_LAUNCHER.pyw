"""
ULTIMATE DESKTOP LAUNCHER - ALL GENERATORS IN ONE GUI
Updated with ALL analytics-driven enhancements
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import threading
from pathlib import Path
import sys

PROJECT_ROOT = Path("F:/AI_Oracle_Root/scarify")
ABRAHAM_HORROR = PROJECT_ROOT / "abraham_horror"

class UltimateLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("🔥 ULTIMATE GENERATOR - Analytics-Driven Domination")
        self.geometry("1200x800")
        self.configure(bg='#0a0a0a')
        
        self.create_ui()
        
    def create_ui(self):
        """Create the UI"""
        # Title
        title = tk.Label(
            self,
            text="🔥 SCARIFY EMPIRE - TOTAL DOMINATION 🔥",
            font=("Consolas", 20, "bold"),
            bg='#0a0a0a',
            fg='#ff0000'
        )
        title.pack(pady=20)
        
        # Subtitle
        subtitle = tk.Label(
            self,
            text="Based on YOUR YouTube Analytics | Decomposing Lincoln Max Headroom",
            font=("Consolas", 10),
            bg='#0a0a0a',
            fg='#00ff00'
        )
        subtitle.pack()
        
        # Main frame
        main_frame = tk.Frame(self, bg='#0a0a0a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel - Generators
        left_frame = tk.LabelFrame(
            main_frame,
            text=" 🎬 VIDEO GENERATORS ",
            font=("Consolas", 12, "bold"),
            bg='#1a1a1a',
            fg='#00ff00',
            bd=2
        )
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,10))
        
        # Generator buttons
        generators = [
            ("🎯 DAILY BATCH (20 Shorts + 3 Longs)", self.run_daily_batch, "#ff0000"),
            ("📺 Dark Josh Dynamic (Absurdist)", self.run_dark_josh, "#ff6600"),
            ("🎭 Long-Form (3-10min Deep Dives)", self.run_long_form, "#ff9900"),
            ("📱 QR Viral Campaign (10 videos)", self.run_qr_campaign, "#ffcc00"),
            ("🎪 Multi-Character (5 Personas)", self.run_multi_character, "#00ff00"),
            ("🌍 Platform Optimizer (All Formats)", self.run_platform_opt, "#00ffff"),
            ("🤖 Master Control (24/7 Auto)", self.run_master_control, "#ff00ff"),
            ("📊 YouTube Analytics Report", self.run_analytics, "#0099ff"),
        ]
        
        for text, command, color in generators:
            btn = tk.Button(
                left_frame,
                text=text,
                command=command,
                font=("Consolas", 11),
                bg=color,
                fg='black',
                activebackground='white',
                activeforeground='black',
                relief=tk.RAISED,
                bd=3,
                padx=10,
                pady=10
            )
            btn.pack(fill=tk.X, padx=10, pady=5)
        
        # Right panel - Status & Logs
        right_frame = tk.LabelFrame(
            main_frame,
            text=" 📊 STATUS & LOGS ",
            font=("Consolas", 12, "bold"),
            bg='#1a1a1a',
            fg='#00ff00',
            bd=2
        )
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Stats display
        stats_frame = tk.Frame(right_frame, bg='#1a1a1a')
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.stats_label = tk.Label(
            stats_frame,
            text="📊 CHANNEL: DissWhatImSayin\n"
                 "👥 Subs: 13 / 500 (need 487 more)\n"
                 "👁️ Top Video: 1,247 views (#277)\n"
                 "🎯 Goal: Monetization in 30 days",
            font=("Consolas", 10),
            bg='#1a1a1a',
            fg='#00ff00',
            justify=tk.LEFT
        )
        self.stats_label.pack(anchor=tk.W)
        
        # Log viewer
        log_label = tk.Label(
            right_frame,
            text="CONSOLE OUTPUT:",
            font=("Consolas", 10, "bold"),
            bg='#1a1a1a',
            fg='#ffff00'
        )
        log_label.pack(anchor=tk.W, padx=10, pady=(10,5))
        
        self.log_text = scrolledtext.ScrolledText(
            right_frame,
            height=30,
            width=60,
            bg='#000000',
            fg='#00ff00',
            font=("Consolas", 9),
            insertbackground='#00ff00'
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0,10))
        
        # Bottom panel - Quick actions
        bottom_frame = tk.Frame(self, bg='#0a0a0a')
        bottom_frame.pack(fill=tk.X, padx=20, pady=(0,20))
        
        quick_actions = [
            ("🚀 TEST VIDEO", self.test_video, "#00ff00"),
            ("📤 Open Studio", self.open_studio, "#0099ff"),
            ("📂 Open Uploads Folder", self.open_folder, "#ff9900"),
        ]
        
        for text, command, color in quick_actions:
            btn = tk.Button(
                bottom_frame,
                text=text,
                command=command,
                font=("Consolas", 10, "bold"),
                bg=color,
                fg='black',
                padx=20,
                pady=5
            )
            btn.pack(side=tk.LEFT, padx=5)
        
        self.log("✅ Ultimate Launcher initialized")
        self.log("✅ All generators loaded")
        self.log("✅ Based on YOUR YouTube analytics (1,247 & 1,194 view videos)")
        self.log("\n🎯 Ready to generate content with decomposing Lincoln aesthetic")
    
    def log(self, message):
        """Add message to log"""
        timestamp = Path(__file__).parent
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.update()
    
    def run_command(self, command, description):
        """Run command in background thread"""
        def execute():
            self.log(f"\n{'='*60}")
            self.log(f"🚀 {description}")
            self.log(f"{'='*60}")
            
            try:
                result = subprocess.run(
                    command,
                    cwd=str(ABRAHAM_HORROR),
                    capture_output=True,
                    text=True,
                    shell=True
                )
                
                if result.stdout:
                    for line in result.stdout.split('\n'):
                        if line.strip():
                            self.log(line)
                
                if result.returncode == 0:
                    self.log(f"\n✅ {description} - COMPLETE")
                else:
                    self.log(f"\n❌ Error: {result.stderr[:200]}")
                    
            except Exception as e:
                self.log(f"❌ Error: {str(e)}")
        
        thread = threading.Thread(target=execute)
        thread.daemon = True
        thread.start()
    
    def run_daily_batch(self):
        """Generate daily batch (20 Shorts + 3 Longs)"""
        self.log("\n📺 DAILY BATCH: 20 Shorts + 3 Longs")
        self.log("⏱️ Estimated time: 60 minutes")
        
        if messagebox.askyesno("Daily Batch", "Generate 20 Shorts + 3 Longs?\n\n(~60 minutes, auto-uploads to YouTube)"):
            self.run_command(
                f"python DARK_JOSH_DYNAMIC.py 20 && python LONG_FORM_GENERATOR.py 3",
                "DAILY BATCH (23 videos)"
            )
    
    def run_dark_josh(self):
        """Run Dark Josh generator"""
        count = 10
        self.log(f"\n🎭 Generating {count} Dark Josh observations...")
        self.run_command(
            f"python DARK_JOSH_DYNAMIC.py {count}",
            f"Dark Josh Dynamic ({count} videos)"
        )
    
    def run_long_form(self):
        """Run long-form generator"""
        count = 2
        self.log(f"\n📺 Generating {count} long-form videos (3-10min)...")
        self.run_command(
            f"python LONG_FORM_GENERATOR.py {count}",
            f"Long-Form Generator ({count} videos)"
        )
    
    def run_qr_campaign(self):
        """Run QR viral campaign"""
        self.log("\n📱 QR VIRAL CAMPAIGN")
        self.log("ℹ️ 10 videos already generated!")
        self.log("📂 Location: uploaded/ folder")
        
        if messagebox.askyesno("QR Campaign", "10 QR viral videos are already generated!\n\nOpen upload folder?"):
            subprocess.Popen(f'explorer "{ABRAHAM_HORROR / "uploaded"}"')
            subprocess.Popen('start https://studio.youtube.com/channel/UCS5pEpSCw8k4wene0iv0uAg/videos/upload', shell=True)
    
    def run_multi_character(self):
        """Run multi-character generator"""
        count = 10
        self.log(f"\n🎪 Generating {count} multi-character videos...")
        self.log("📝 Characters: Lincoln, Tesla, Twain, Roosevelt, Lovecraft")
        self.run_command(
            f"python MULTI_PLATFORM_ENGINE.py {count}",
            f"Multi-Character Generator ({count} videos)"
        )
    
    def run_platform_opt(self):
        """Run platform optimizer"""
        count = 5
        self.log(f"\n🌍 Generating {count} multi-platform sets...")
        self.log("📱 Creates: YouTube, TikTok, Instagram, Twitter variants")
        self.run_command(
            f"python PLATFORM_OPTIMIZER.py {count}",
            f"Platform Optimizer ({count*5} total videos)"
        )
    
    def run_master_control(self):
        """Run master control dashboard"""
        self.log("\n🤖 MASTER CONTROL - 24/7 AUTO-OPTIMIZATION")
        self.log("ℹ️ This runs continuously in a new window")
        
        if messagebox.askyesno("Master Control", "Start 24/7 auto-optimization?\n\n• Monitors YouTube analytics every 6 hours\n• Auto-generates optimized content\n• Runs until you stop it"):
            subprocess.Popen(
                f'start cmd /k "cd /d {PROJECT_ROOT} && python -Xutf8 MASTER_CONTROL_DASHBOARD.py --continuous"',
                shell=True
            )
            self.log("✅ Master Control started in new window")
    
    def run_analytics(self):
        """Run analytics report"""
        self.log("\n📊 Pulling YouTube analytics...")
        self.run_command(
            f"cd {PROJECT_ROOT} && python YOUTUBE_ANALYTICS_MONITOR.py",
            "YouTube Analytics Report"
        )
    
    def test_video(self):
        """Generate and upload test video"""
        self.log("\n🚀 GENERATING TEST VIDEO...")
        self.log("📝 Format: Dark Josh Short (45s)")
        self.log("🎭 Aesthetic: Decomposing Lincoln Max Headroom")
        self.log("📤 Will auto-upload to YouTube")
        
        if messagebox.askyesno("Test Video", "Generate 1 test video and upload to YouTube?"):
            self.run_command(
                "python DARK_JOSH_DYNAMIC.py 1",
                "TEST VIDEO"
            )
    
    def open_studio(self):
        """Open YouTube Studio"""
        self.log("\n📤 Opening YouTube Studio...")
        subprocess.Popen(
            'start https://studio.youtube.com/channel/UCS5pEpSCw8k4wene0iv0uAg/videos',
            shell=True
        )
    
    def open_folder(self):
        """Open uploads folder"""
        self.log("\n📂 Opening uploads folder...")
        subprocess.Popen(f'explorer "{ABRAHAM_HORROR / "uploaded"}"')

if __name__ == "__main__":
    app = UltimateLauncher()
    app.mainloop()


