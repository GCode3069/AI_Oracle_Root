#!/usr/bin/env python3
"""
SCARIFY EMPIRE - DESKTOP LAUNCHER GUI
Beautiful graphical launcher for all systems!

Features:
- Visual launcher with icons
- One-click access to all systems
- System status indicators
- Quick actions
- Beautiful modern UI
"""

import tkinter as tk
from tkinter import ttk
import subprocess
from pathlib import Path
import sys
import os

PROJECT_ROOT = Path(__file__).parent.absolute()

class ScarifyDesktopLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("🚀 Scarify Empire - Desktop Launcher")
        self.geometry("600x700")
        self.configure(bg='#1a1a1a')
        self.resizable(False, False)
        
        # Center window
        self.center_window()
        
        # Create UI
        self.create_ui()
        
    def center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_ui(self):
        """Create the launcher UI"""
        
        # Header
        header_frame = tk.Frame(self, bg='#2a2a2a', height=100)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="SCARIFY EMPIRE",
            font=('Arial', 28, 'bold'),
            bg='#2a2a2a',
            fg='#00ff00'
        )
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Desktop Command Center",
            font=('Arial', 12),
            bg='#2a2a2a',
            fg='#888888'
        )
        subtitle_label.pack()
        
        # Main content
        content_frame = tk.Frame(self, bg='#1a1a1a')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Main Launchers
        main_frame = ttk.LabelFrame(content_frame, text="🚀 Main Systems", padding=15)
        main_frame.pack(fill='x', pady=5)
        
        self.create_launch_button(
            main_frame,
            "🚀 LAUNCH EMPIRE",
            "Start Everything: Desktop + MCP + Mobile + Telegram",
            lambda: self.launch_script("LAUNCH_EMPIRE.bat"),
            bg='#00aa00'
        ).pack(fill='x', pady=5)
        
        self.create_launch_button(
            main_frame,
            "🖥️ Control Center",
            "Desktop Dashboard Only (18 tabs)",
            lambda: self.launch_python("SCARIFY_CONTROL_CENTER.pyw"),
            bg='#0066cc'
        ).pack(fill='x', pady=5)
        
        self.create_launch_button(
            main_frame,
            "📱 Mobile Web UI",
            "Start Mobile Interface (http://localhost:5000)",
            lambda: self.launch_python("MOBILE_MCP_SERVER.py"),
            bg='#cc6600'
        ).pack(fill='x', pady=5)
        
        # Tools
        tools_frame = ttk.LabelFrame(content_frame, text="🛠️ Tools", padding=15)
        tools_frame.pack(fill='x', pady=5)
        
        self.create_launch_button(
            tools_frame,
            "🤖 Self Deploy Agent",
            "Auto-configure & deploy (5 modes)",
            lambda: self.launch_python("SELF_DEPLOY.py"),
            bg='#9900cc'
        ).pack(fill='x', pady=5)
        
        self.create_launch_button(
            tools_frame,
            "📤 Sync to GitHub",
            "Backup your work to GitHub",
            lambda: self.launch_script("SYNC_TO_GITHUB.bat"),
            bg='#cc0066'
        ).pack(fill='x', pady=5)
        
        # Quick Actions
        quick_frame = ttk.LabelFrame(content_frame, text="⚡ Quick Actions", padding=15)
        quick_frame.pack(fill='x', pady=5)
        
        quick_grid = tk.Frame(quick_frame, bg='#f0f0f0')
        quick_grid.pack(fill='x')
        
        self.create_small_button(
            quick_grid,
            "🎬 Gen 10",
            lambda: self.quick_generate(10)
        ).grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        
        self.create_small_button(
            quick_grid,
            "📤 Upload",
            lambda: self.quick_upload()
        ).grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        self.create_small_button(
            quick_grid,
            "💰 Bitcoin",
            lambda: self.quick_bitcoin()
        ).grid(row=0, column=2, padx=5, pady=5, sticky='ew')
        
        quick_grid.columnconfigure(0, weight=1)
        quick_grid.columnconfigure(1, weight=1)
        quick_grid.columnconfigure(2, weight=1)
        
        # Documentation
        docs_frame = ttk.LabelFrame(content_frame, text="📚 Documentation", padding=15)
        docs_frame.pack(fill='x', pady=5)
        
        self.create_launch_button(
            docs_frame,
            "📖 Quick Start Guide",
            "Read this first!",
            lambda: self.open_file("⚡_DO_THIS_NOW.txt"),
            bg='#006666'
        ).pack(fill='x', pady=3)
        
        self.create_launch_button(
            docs_frame,
            "📱 Mobile Guide",
            "How to use mobile interface",
            lambda: self.open_file("MOBILE_INTERFACE_GUIDE.md"),
            bg='#006666'
        ).pack(fill='x', pady=3)
        
        # Status
        status_frame = tk.Frame(self, bg='#2a2a2a', height=60)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="✅ Ready to launch! Click any button above.",
            font=('Arial', 10),
            bg='#2a2a2a',
            fg='#00ff00'
        )
        self.status_label.pack(pady=20)
        
    def create_launch_button(self, parent, text, desc, command, bg='#0066cc'):
        """Create a launch button"""
        btn_frame = tk.Frame(parent, bg='white', relief='raised', borderwidth=2)
        
        btn = tk.Button(
            btn_frame,
            text=text,
            font=('Arial', 12, 'bold'),
            bg=bg,
            fg='white',
            activebackground=self.darken_color(bg),
            activeforeground='white',
            command=command,
            cursor='hand2',
            relief='flat',
            padx=15,
            pady=10
        )
        btn.pack(fill='both', expand=True)
        
        desc_label = tk.Label(
            btn_frame,
            text=desc,
            font=('Arial', 8),
            bg='white',
            fg='#666666'
        )
        desc_label.pack(fill='x', padx=5, pady=(0, 5))
        
        return btn_frame
        
    def create_small_button(self, parent, text, command):
        """Create a small quick action button"""
        btn = tk.Button(
            parent,
            text=text,
            font=('Arial', 10, 'bold'),
            bg='#00aa00',
            fg='white',
            command=command,
            cursor='hand2',
            relief='raised',
            padx=10,
            pady=8
        )
        return btn
        
    def darken_color(self, color):
        """Darken a hex color"""
        # Simple darkening - reduce each component
        if color.startswith('#'):
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            
            r = max(0, r - 30)
            g = max(0, g - 30)
            b = max(0, b - 30)
            
            return f'#{r:02x}{g:02x}{b:02x}'
        return color
        
    def update_status(self, message, color='#00ff00'):
        """Update status message"""
        self.status_label.config(text=message, fg=color)
        
    def launch_script(self, script_name):
        """Launch a batch/shell script"""
        script_path = PROJECT_ROOT / script_name
        if script_path.exists():
            self.update_status(f"🚀 Launching {script_name}...")
            subprocess.Popen([str(script_path)], cwd=str(PROJECT_ROOT), shell=True)
            self.update_status(f"✅ Launched! Check separate window.")
        else:
            self.update_status(f"❌ Not found: {script_name}", '#ff0000')
            
    def launch_python(self, script_name):
        """Launch a Python script"""
        script_path = PROJECT_ROOT / script_name
        if script_path.exists():
            self.update_status(f"🚀 Launching {script_name}...")
            if sys.platform == 'win32':
                subprocess.Popen(['pythonw', str(script_path)], cwd=str(PROJECT_ROOT))
            else:
                subprocess.Popen(['python3', str(script_path)], cwd=str(PROJECT_ROOT))
            self.update_status(f"✅ Launched!")
        else:
            self.update_status(f"❌ Not found: {script_name}", '#ff0000')
            
    def open_file(self, filename):
        """Open a file with default application"""
        file_path = PROJECT_ROOT / filename
        if file_path.exists():
            if sys.platform == 'win32':
                os.startfile(str(file_path))
            elif sys.platform == 'darwin':
                subprocess.Popen(['open', str(file_path)])
            else:
                subprocess.Popen(['xdg-open', str(file_path)])
            self.update_status(f"✅ Opened {filename}")
        else:
            self.update_status(f"❌ Not found: {filename}", '#ff0000')
            
    def quick_generate(self, count):
        """Quick generate videos"""
        self.update_status(f"🎬 Generating {count} videos...")
        script = PROJECT_ROOT / "abraham_horror" / "ABRAHAM_PROFESSIONAL_UPGRADE.py"
        if script.exists():
            subprocess.Popen(['python', str(script), str(count)], cwd=str(PROJECT_ROOT))
            self.update_status(f"✅ Generation started! ({count} videos)")
        else:
            self.update_status("❌ Generator not found", '#ff0000')
            
    def quick_upload(self):
        """Quick upload all videos"""
        self.update_status("📤 Uploading all videos...")
        script = PROJECT_ROOT / "MULTI_CHANNEL_UPLOADER.py"
        if script.exists():
            subprocess.Popen(['python', str(script), 'abraham_horror/youtube_ready', 'round-robin'],
                           cwd=str(PROJECT_ROOT))
            self.update_status("✅ Upload started!")
        else:
            self.update_status("❌ Uploader not found", '#ff0000')
            
    def quick_bitcoin(self):
        """Quick check Bitcoin balance"""
        self.update_status("💰 Checking Bitcoin balance...")
        script = PROJECT_ROOT / "check_balance.py"
        if script.exists():
            subprocess.Popen(['python', str(script)], cwd=str(PROJECT_ROOT))
            self.update_status("✅ Check running! See console window.")
        else:
            self.update_status("❌ Balance checker not found", '#ff0000')

if __name__ == "__main__":
    app = ScarifyDesktopLauncher()
    app.mainloop()

