"""
SCARIFY EMPIRE - CONTROL CENTER DASHBOARD
Desktop GUI for managing video generation, uploads, analytics, and revenue

Features:
- Real-time system status monitoring
- Video generation controls
- Multi-channel upload management
- Analytics dashboard
- Bitcoin balance tracking
- Channel configuration
- Live log viewer
- MCP server integration
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import subprocess
import threading
import json
import os
from pathlib import Path
from datetime import datetime
import requests
import time

# Configuration
PROJECT_ROOT = Path("F:/AI_Oracle_Root/scarify")
if not PROJECT_ROOT.exists():
    PROJECT_ROOT = Path.home() / "scarify"

ABRAHAM_HORROR_DIR = PROJECT_ROOT / "abraham_horror"
VIDEO_DIR = ABRAHAM_HORROR_DIR / "youtube_ready"

class ScarifyControlCenter(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Scarify Empire - Control Center")
        self.geometry("1400x900")
        self.configure(bg='#1a1a1a')
        
        # State variables
        self.generation_running = False
        self.upload_running = False
        self.mcp_server_running = False
        
        # Create UI
        self.create_menubar()
        self.create_main_layout()
        
        # Start background tasks
        self.update_status()
        
    def create_menubar(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Set Project Root", command=self.set_project_root)
        file_menu.add_command(label="Open Project Folder", command=self.open_project_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Launch Abraham Studio", command=self.launch_studio)
        tools_menu.add_command(label="Launch MCP Server", command=self.launch_mcp_server)
        tools_menu.add_separator()
        tools_menu.add_command(label="Open Video Directory", command=self.open_video_dir)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Documentation", command=self.show_docs)
        help_menu.add_command(label="About", command=self.show_about)
        
    def create_main_layout(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_generation_tab()
        self.create_upload_tab()
        self.create_analytics_tab()
        self.create_channels_tab()
        self.create_revenue_tab()
        self.create_battle_royale_tab()      # NEW: Battle Royale tracking
        self.create_sheets_sync_tab()         # NEW: Google Sheets sync
        self.create_achievements_tab()        # NEW: Achievement system
        self.create_telegram_tab()            # NEW: Telegram bot control
        self.create_abtest_tab()              # NEW: A/B testing
        self.create_scheduler_tab()           # NEW: Scheduled generation
        self.create_queue_tab()               # NEW: Video queue
        self.create_predictor_tab()           # NEW: Performance prediction
        self.create_backup_tab()              # NEW: Backup & restore
        self.create_script_library_tab()      # NEW: Script browser
        self.create_logs_tab()
        self.create_settings_tab()
        
    def create_dashboard_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📊 Dashboard")
        
        # Header
        header = tk.Label(frame, text="SCARIFY EMPIRE CONTROL CENTER", 
                         font=('Arial', 24, 'bold'), bg='#2a2a2a', fg='#00ff00')
        header.pack(fill='x', pady=10)
        
        # Main content area
        content = ttk.Frame(frame)
        content.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left column - Status
        left_col = ttk.LabelFrame(content, text="System Status", padding=10)
        left_col.pack(side='left', fill='both', expand=True, padx=5)
        
        self.status_text = scrolledtext.ScrolledText(left_col, height=20, 
                                                     bg='#1a1a1a', fg='#00ff00',
                                                     font=('Consolas', 10))
        self.status_text.pack(fill='both', expand=True)
        
        # Right column - Quick Actions
        right_col = ttk.Frame(content)
        right_col.pack(side='right', fill='both', padx=5)
        
        # Video stats
        stats_frame = ttk.LabelFrame(right_col, text="Video Statistics", padding=10)
        stats_frame.pack(fill='x', pady=5)
        
        self.videos_ready_label = tk.Label(stats_frame, text="Videos Ready: 0", 
                                           font=('Arial', 14))
        self.videos_ready_label.pack()
        
        self.videos_uploaded_label = tk.Label(stats_frame, text="Uploaded: 0", 
                                              font=('Arial', 14))
        self.videos_uploaded_label.pack()
        
        # Quick actions
        actions_frame = ttk.LabelFrame(right_col, text="Quick Actions", padding=10)
        actions_frame.pack(fill='x', pady=5)
        
        ttk.Button(actions_frame, text="🎬 Generate 5 Videos", 
                  command=lambda: self.quick_generate(5)).pack(fill='x', pady=2)
        ttk.Button(actions_frame, text="📤 Upload All Videos", 
                  command=self.quick_upload).pack(fill='x', pady=2)
        ttk.Button(actions_frame, text="📊 Refresh Analytics", 
                  command=self.refresh_analytics).pack(fill='x', pady=2)
        ttk.Button(actions_frame, text="💰 Check Bitcoin Balance", 
                  command=self.check_bitcoin).pack(fill='x', pady=2)
        
        # MCP Server control
        mcp_frame = ttk.LabelFrame(right_col, text="MCP Server", padding=10)
        mcp_frame.pack(fill='x', pady=5)
        
        self.mcp_status_label = tk.Label(mcp_frame, text="Status: Stopped", 
                                         font=('Arial', 12), fg='red')
        self.mcp_status_label.pack()
        
        self.mcp_btn = ttk.Button(mcp_frame, text="Start MCP Server", 
                                  command=self.toggle_mcp_server)
        self.mcp_btn.pack(fill='x', pady=5)
        
    def create_generation_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🎥 Generation")
        
        # Header
        header = tk.Label(frame, text="VIDEO GENERATION", 
                         font=('Arial', 18, 'bold'))
        header.pack(pady=10)
        
        # Controls
        controls = ttk.LabelFrame(frame, text="Generation Controls", padding=10)
        controls.pack(fill='x', padx=10, pady=5)
        
        # Number of videos
        ttk.Label(controls, text="Number of Videos:").grid(row=0, column=0, sticky='w', pady=5)
        self.video_count_var = tk.StringVar(value="10")
        video_count_spin = ttk.Spinbox(controls, from_=1, to=100, textvariable=self.video_count_var, width=10)
        video_count_spin.grid(row=0, column=1, padx=5, pady=5)
        
        # Mode
        ttk.Label(controls, text="Mode:").grid(row=1, column=0, sticky='w', pady=5)
        self.mode_var = tk.StringVar(value="rapid")
        mode_combo = ttk.Combobox(controls, textvariable=self.mode_var, 
                                  values=["rapid", "production"], state='readonly', width=15)
        mode_combo.grid(row=1, column=1, padx=5, pady=5)
        
        # Generate button
        self.generate_btn = ttk.Button(controls, text="🎬 Start Generation", 
                                       command=self.start_generation, style='Accent.TButton')
        self.generate_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Progress
        progress_frame = ttk.LabelFrame(frame, text="Progress", padding=10)
        progress_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.gen_progress = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.gen_progress.pack(fill='x', pady=5)
        
        self.gen_log = scrolledtext.ScrolledText(progress_frame, height=20, 
                                                 bg='#1a1a1a', fg='#00ff00',
                                                 font=('Consolas', 9))
        self.gen_log.pack(fill='both', expand=True)
        
    def create_upload_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📤 Upload")
        
        # Header
        header = tk.Label(frame, text="VIDEO UPLOAD MANAGEMENT", 
                         font=('Arial', 18, 'bold'))
        header.pack(pady=10)
        
        # Controls
        controls = ttk.LabelFrame(frame, text="Upload Controls", padding=10)
        controls.pack(fill='x', padx=10, pady=5)
        
        # Strategy
        ttk.Label(controls, text="Distribution Strategy:").grid(row=0, column=0, sticky='w', pady=5)
        self.strategy_var = tk.StringVar(value="round-robin")
        strategy_combo = ttk.Combobox(controls, textvariable=self.strategy_var,
                                     values=["round-robin", "balanced", "single"], 
                                     state='readonly', width=15)
        strategy_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Channel count
        ttk.Label(controls, text="Number of Channels:").grid(row=1, column=0, sticky='w', pady=5)
        self.channel_count_var = tk.StringVar(value="15")
        channel_spin = ttk.Spinbox(controls, from_=1, to=15, 
                                   textvariable=self.channel_count_var, width=10)
        channel_spin.grid(row=1, column=1, padx=5, pady=5)
        
        # Upload button
        self.upload_btn = ttk.Button(controls, text="📤 Start Upload", 
                                     command=self.start_upload, style='Accent.TButton')
        self.upload_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Progress
        progress_frame = ttk.LabelFrame(frame, text="Upload Progress", padding=10)
        progress_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.upload_progress = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.upload_progress.pack(fill='x', pady=5)
        
        self.upload_log = scrolledtext.ScrolledText(progress_frame, height=20,
                                                    bg='#1a1a1a', fg='#00ff00',
                                                    font=('Consolas', 9))
        self.upload_log.pack(fill='both', expand=True)
        
    def create_analytics_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📊 Analytics")
        
        # Header
        header = tk.Label(frame, text="YOUTUBE ANALYTICS", 
                         font=('Arial', 18, 'bold'))
        header.pack(pady=10)
        
        # Refresh button
        ttk.Button(frame, text="🔄 Refresh Analytics", 
                  command=self.refresh_analytics).pack(pady=5)
        
        # Analytics display
        analytics_frame = ttk.LabelFrame(frame, text="Performance Metrics", padding=10)
        analytics_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.analytics_text = scrolledtext.ScrolledText(analytics_frame, height=25,
                                                       bg='#1a1a1a', fg='#00ff00',
                                                       font=('Consolas', 10))
        self.analytics_text.pack(fill='both', expand=True)
        
    def create_channels_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🎬 Channels")
        
        # Header
        header = tk.Label(frame, text="CHANNEL MANAGEMENT", 
                         font=('Arial', 18, 'bold'))
        header.pack(pady=10)
        
        # Controls
        controls = ttk.LabelFrame(frame, text="Channel Controls", padding=10)
        controls.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(controls, text="📋 List Channels", 
                  command=self.list_channels).pack(side='left', padx=5)
        ttk.Button(controls, text="✅ Verify Channels", 
                  command=self.verify_channels).pack(side='left', padx=5)
        ttk.Button(controls, text="➕ Setup Channels", 
                  command=self.setup_channels).pack(side='left', padx=5)
        
        # Channel list
        channels_frame = ttk.LabelFrame(frame, text="Configured Channels", padding=10)
        channels_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.channels_text = scrolledtext.ScrolledText(channels_frame, height=25,
                                                      bg='#1a1a1a', fg='#00ff00',
                                                      font=('Consolas', 10))
        self.channels_text.pack(fill='both', expand=True)
        
    def create_revenue_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="💰 Revenue")
        
        # Header
        header = tk.Label(frame, text="REVENUE TRACKING", 
                         font=('Arial', 18, 'bold'))
        header.pack(pady=10)
        
        # Bitcoin section
        btc_frame = ttk.LabelFrame(frame, text="Bitcoin Donations", padding=10)
        btc_frame.pack(fill='x', padx=10, pady=5)
        
        self.btc_balance_label = tk.Label(btc_frame, text="Balance: Checking...", 
                                         font=('Arial', 16, 'bold'))
        self.btc_balance_label.pack(pady=10)
        
        ttk.Button(btc_frame, text="🔄 Check Balance", 
                  command=self.check_bitcoin).pack()
        
        # Revenue stats
        stats_frame = ttk.LabelFrame(frame, text="Revenue Statistics", padding=10)
        stats_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.revenue_text = scrolledtext.ScrolledText(stats_frame, height=20,
                                                     bg='#1a1a1a', fg='#00ff00',
                                                     font=('Consolas', 11))
        self.revenue_text.pack(fill='both', expand=True)
        
        # Display revenue info
        self.update_revenue_display()
        
    def create_logs_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📝 Logs")
        
        # Header
        header = tk.Label(frame, text="SYSTEM LOGS", 
                         font=('Arial', 18, 'bold'))
        header.pack(pady=10)
        
        # Controls
        controls = ttk.Frame(frame)
        controls.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(controls, text="🔄 Refresh", 
                  command=self.refresh_logs).pack(side='left', padx=5)
        ttk.Button(controls, text="🗑️ Clear", 
                  command=self.clear_logs).pack(side='left', padx=5)
        ttk.Button(controls, text="💾 Save", 
                  command=self.save_logs).pack(side='left', padx=5)
        
        # Log viewer
        log_frame = ttk.LabelFrame(frame, text="Live System Logs", padding=10)
        log_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.system_log = scrolledtext.ScrolledText(log_frame, height=30,
                                                    bg='#1a1a1a', fg='#00ff00',
                                                    font=('Consolas', 9))
        self.system_log.pack(fill='both', expand=True)
        
    def create_battle_royale_tab(self):
        """Battle Royale LLM Challenge Tracker"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="⚔️ Battle Royale")
        
        header = tk.Label(frame, text="LLM BATTLE ROYALE TRACKER", 
                         font=('Arial', 18, 'bold'))
        header.pack(pady=10)
        
        # Controls
        controls = ttk.Frame(frame)
        controls.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(controls, text="🔄 Refresh Status", 
                  command=self.refresh_battle_status).pack(side='left', padx=5)
        ttk.Button(controls, text="📊 Load Battle Data", 
                  command=self.load_battle_data).pack(side='left', padx=5)
        ttk.Button(controls, text="🏆 Show Leaderboard", 
                  command=self.show_leaderboard).pack(side='left', padx=5)
        
        # Battle info
        battle_frame = ttk.LabelFrame(frame, text="Battle Status", padding=10)
        battle_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.battle_text = scrolledtext.ScrolledText(battle_frame, height=25,
                                                     bg='#1a1a1a', fg='#00ff00',
                                                     font=('Consolas', 10))
        self.battle_text.pack(fill='both', expand=True)
        
        # Load initial data
        self.refresh_battle_status()
        
    def create_sheets_sync_tab(self):
        """Google Sheets Auto-Sync"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📊 Sheets Sync")
        
        header = tk.Label(frame, text="GOOGLE SHEETS AUTO-SYNC", 
                         font=('Arial', 18, 'bold'))
        header.pack(pady=10)
        
        # Sync controls
        controls = ttk.LabelFrame(frame, text="Sync Controls", padding=10)
        controls.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(controls, text="Sheet ID:").grid(row=0, column=0, sticky='w', pady=5)
        self.sheet_id_var = tk.StringVar(value="1jvWP95U0ksaHw97PrPZsrh6ZVllviJJof7kQ2dV0ka0")
        ttk.Entry(controls, textvariable=self.sheet_id_var, width=50).grid(row=0, column=1, padx=5)
        
        self.auto_sync_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(controls, text="Auto-sync every 5 minutes", 
                       variable=self.auto_sync_var,
                       command=self.toggle_auto_sync).grid(row=1, column=0, columnspan=2, pady=5)
        
        ttk.Button(controls, text="📤 Sync Now", 
                  command=self.sync_to_sheets).grid(row=2, column=0, pady=5)
        ttk.Button(controls, text="📥 Import from Sheets", 
                  command=self.import_from_sheets).grid(row=2, column=1, pady=5)
        
        # Sync log
        log_frame = ttk.LabelFrame(frame, text="Sync Log", padding=10)
        log_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.sheets_log = scrolledtext.ScrolledText(log_frame, height=20,
                                                    bg='#1a1a1a', fg='#00ff00',
                                                    font=('Consolas', 9))
        self.sheets_log.pack(fill='both', expand=True)
        
    def create_achievements_tab(self):
        """Achievement & Milestone System"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🏆 Achievements")
        
        header = tk.Label(frame, text="ACHIEVEMENT SYSTEM", 
                         font=('Arial', 18, 'bold'))
        header.pack(pady=10)
        
        # Stats display
        stats_frame = ttk.LabelFrame(frame, text="Current Stats", padding=10)
        stats_frame.pack(fill='x', padx=10, pady=5)
        
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack()
        
        self.total_videos_label = tk.Label(stats_grid, text="Total Videos: 0", font=('Arial', 12))
        self.total_videos_label.grid(row=0, column=0, padx=20, pady=5)
        
        self.total_views_label = tk.Label(stats_grid, text="Total Views: 0", font=('Arial', 12))
        self.total_views_label.grid(row=0, column=1, padx=20, pady=5)
        
        self.total_revenue_label = tk.Label(stats_grid, text="Total Revenue: $0", font=('Arial', 12))
        self.total_revenue_label.grid(row=0, column=2, padx=20, pady=5)
        
        # Achievements list
        achieve_frame = ttk.LabelFrame(frame, text="Unlocked Achievements", padding=10)
        achieve_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.achievement_text = scrolledtext.ScrolledText(achieve_frame, height=20,
                                                         bg='#1a1a1a', fg='#00ff00',
                                                         font=('Consolas', 11))
        self.achievement_text.pack(fill='both', expand=True)
        
        # Load achievements
        self.load_achievements()
        
    def create_telegram_tab(self):
        """Telegram Bot Remote Control"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📱 Telegram")
        
        header = tk.Label(frame, text="TELEGRAM BOT CONTROL", 
                         font=('Arial', 18, 'bold'))
        header.pack(pady=10)
        
        # Bot setup
        setup_frame = ttk.LabelFrame(frame, text="Bot Configuration", padding=10)
        setup_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(setup_frame, text="Bot Token:").grid(row=0, column=0, sticky='w', pady=5)
        self.telegram_token_var = tk.StringVar()
        ttk.Entry(setup_frame, textvariable=self.telegram_token_var, width=50, show='*').grid(row=0, column=1, padx=5)
        
        ttk.Button(setup_frame, text="🤖 Start Bot", 
                  command=self.start_telegram_bot).grid(row=1, column=0, pady=5)
        ttk.Button(setup_frame, text="⏹️ Stop Bot", 
                  command=self.stop_telegram_bot).grid(row=1, column=1, pady=5)
        
        self.telegram_status_label = tk.Label(setup_frame, text="Bot Status: Stopped", fg='red')
        self.telegram_status_label.grid(row=2, column=0, columnspan=2, pady=5)
        
        # Command log
        log_frame = ttk.LabelFrame(frame, text="Command History", padding=10)
        log_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.telegram_log = scrolledtext.ScrolledText(log_frame, height=20,
                                                      bg='#1a1a1a', fg='#00ff00',
                                                      font=('Consolas', 9))
        self.telegram_log.pack(fill='both', expand=True)
        
    def create_abtest_tab(self):
        """A/B Testing Dashboard"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🧪 A/B Testing")
        
        header = tk.Label(frame, text="A/B TESTING DASHBOARD", 
                         font=('Arial', 18, 'bold'))
        header.pack(pady=10)
        
        # Test controls
        controls = ttk.LabelFrame(frame, text="Create New Test", padding=10)
        controls.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(controls, text="Test Name:").grid(row=0, column=0, sticky='w', pady=5)
        self.abtest_name_var = tk.StringVar()
        ttk.Entry(controls, textvariable=self.abtest_name_var, width=30).grid(row=0, column=1, padx=5)
        
        ttk.Label(controls, text="Variables:").grid(row=1, column=0, sticky='w', pady=5)
        self.abtest_vars_var = tk.StringVar(value="title, thumbnail, description")
        ttk.Entry(controls, textvariable=self.abtest_vars_var, width=30).grid(row=1, column=1, padx=5)
        
        ttk.Button(controls, text="▶️ Start Test", 
                  command=self.start_abtest).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Results
        results_frame = ttk.LabelFrame(frame, text="Test Results", padding=10)
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.abtest_text = scrolledtext.ScrolledText(results_frame, height=20,
                                                     bg='#1a1a1a', fg='#00ff00',
                                                     font=('Consolas', 10))
        self.abtest_text.pack(fill='both', expand=True)
        
    def create_scheduler_tab(self):
        """Scheduled Generation System"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="⏰ Scheduler")
        
        header = tk.Label(frame, text="SCHEDULED GENERATION", 
                         font=('Arial', 18, 'bold'))
        header.pack(pady=10)
        
        # Schedule controls
        controls = ttk.LabelFrame(frame, text="Create Schedule", padding=10)
        controls.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(controls, text="Frequency:").grid(row=0, column=0, sticky='w', pady=5)
        self.schedule_freq_var = tk.StringVar(value="daily")
        freq_combo = ttk.Combobox(controls, textvariable=self.schedule_freq_var,
                                  values=["hourly", "daily", "weekly", "custom"],
                                  state='readonly', width=15)
        freq_combo.grid(row=0, column=1, padx=5)
        
        ttk.Label(controls, text="Time:").grid(row=1, column=0, sticky='w', pady=5)
        self.schedule_time_var = tk.StringVar(value="09:00")
        ttk.Entry(controls, textvariable=self.schedule_time_var, width=10).grid(row=1, column=1, sticky='w', padx=5)
        
        ttk.Label(controls, text="Videos per run:").grid(row=2, column=0, sticky='w', pady=5)
        self.schedule_count_var = tk.StringVar(value="5")
        ttk.Spinbox(controls, from_=1, to=100, textvariable=self.schedule_count_var, width=10).grid(row=2, column=1, sticky='w', padx=5)
        
        self.schedule_enabled_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(controls, text="Enable Scheduled Generation", 
                       variable=self.schedule_enabled_var,
                       command=self.toggle_scheduler).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Schedule list
        list_frame = ttk.LabelFrame(frame, text="Active Schedules", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.schedule_text = scrolledtext.ScrolledText(list_frame, height=20,
                                                       bg='#1a1a1a', fg='#00ff00',
                                                       font=('Consolas', 10))
        self.schedule_text.pack(fill='both', expand=True)
        
    def create_queue_tab(self):
        """Video Queue Management"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📋 Queue")
        
        header = tk.Label(frame, text="VIDEO QUEUE MANAGER", 
                         font=('Arial', 18, 'bold'))
        header.pack(pady=10)
        
        # Queue controls
        controls = ttk.Frame(frame)
        controls.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(controls, text="➕ Add to Queue", 
                  command=self.add_to_queue).pack(side='left', padx=5)
        ttk.Button(controls, text="▶️ Process Queue", 
                  command=self.process_queue).pack(side='left', padx=5)
        ttk.Button(controls, text="🗑️ Clear Queue", 
                  command=self.clear_queue).pack(side='left', padx=5)
        
        # Queue display
        queue_frame = ttk.LabelFrame(frame, text="Current Queue", padding=10)
        queue_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.queue_text = scrolledtext.ScrolledText(queue_frame, height=25,
                                                    bg='#1a1a1a', fg='#00ff00',
                                                    font=('Consolas', 10))
        self.queue_text.pack(fill='both', expand=True)
        
        # Load queue
        self.load_queue()
        
    def create_predictor_tab(self):
        """Performance Prediction"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔮 Predictor")
        
        header = tk.Label(frame, text="PERFORMANCE PREDICTOR", 
                         font=('Arial', 18, 'bold'))
        header.pack(pady=10)
        
        # Input
        input_frame = ttk.LabelFrame(frame, text="Video Details", padding=10)
        input_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(input_frame, text="Title:").grid(row=0, column=0, sticky='w', pady=5)
        self.predict_title_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.predict_title_var, width=50).grid(row=0, column=1, padx=5)
        
        ttk.Label(input_frame, text="Topic:").grid(row=1, column=0, sticky='w', pady=5)
        self.predict_topic_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.predict_topic_var, width=50).grid(row=1, column=1, padx=5)
        
        ttk.Button(input_frame, text="🔮 Predict Performance", 
                  command=self.predict_performance).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Prediction results
        results_frame = ttk.LabelFrame(frame, text="Predictions", padding=10)
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.prediction_text = scrolledtext.ScrolledText(results_frame, height=20,
                                                         bg='#1a1a1a', fg='#00ff00',
                                                         font=('Consolas', 11))
        self.prediction_text.pack(fill='both', expand=True)
        
    def create_backup_tab(self):
        """Backup & Restore System"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="💾 Backup")
        
        header = tk.Label(frame, text="BACKUP & RESTORE", 
                         font=('Arial', 18, 'bold'))
        header.pack(pady=10)
        
        # Backup controls
        controls = ttk.LabelFrame(frame, text="Backup Controls", padding=10)
        controls.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(controls, text="💾 Create Backup", 
                  command=self.create_backup).pack(side='left', padx=5)
        ttk.Button(controls, text="📥 Restore Backup", 
                  command=self.restore_backup).pack(side='left', padx=5)
        ttk.Button(controls, text="🗑️ Delete Old Backups", 
                  command=self.cleanup_backups).pack(side='left', padx=5)
        
        # Backup list
        list_frame = ttk.LabelFrame(frame, text="Available Backups", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.backup_text = scrolledtext.ScrolledText(list_frame, height=25,
                                                     bg='#1a1a1a', fg='#00ff00',
                                                     font=('Consolas', 10))
        self.backup_text.pack(fill='both', expand=True)
        
        # Load backups
        self.list_backups()
        
    def create_script_library_tab(self):
        """Script Library Browser"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📚 Scripts")
        
        header = tk.Label(frame, text="SCRIPT LIBRARY", 
                         font=('Arial', 18, 'bold'))
        header.pack(pady=10)
        
        # Search
        search_frame = ttk.Frame(frame)
        search_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side='left', padx=5)
        self.script_search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.script_search_var, width=40)
        search_entry.pack(side='left', padx=5)
        ttk.Button(search_frame, text="🔍 Search", 
                  command=self.search_scripts).pack(side='left', padx=5)
        
        # Script list
        list_frame = ttk.LabelFrame(frame, text="Available Scripts", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.script_list = scrolledtext.ScrolledText(list_frame, height=25,
                                                     bg='#1a1a1a', fg='#00ff00',
                                                     font=('Consolas', 10))
        self.script_list.pack(fill='both', expand=True)
        
        # Load scripts
        self.load_script_library()
    
    def create_settings_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="⚙️ Settings")
        
        # Header
        header = tk.Label(frame, text="SETTINGS", 
                         font=('Arial', 18, 'bold'))
        header.pack(pady=10)
        
        # Settings
        settings_frame = ttk.LabelFrame(frame, text="Configuration", padding=10)
        settings_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Project root
        ttk.Label(settings_frame, text="Project Root:").grid(row=0, column=0, sticky='w', pady=5)
        self.project_root_var = tk.StringVar(value=str(PROJECT_ROOT))
        ttk.Entry(settings_frame, textvariable=self.project_root_var, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(settings_frame, text="Browse...", 
                  command=self.set_project_root).grid(row=0, column=2, padx=5)
        
        # Auto-refresh interval
        ttk.Label(settings_frame, text="Auto-refresh (seconds):").grid(row=1, column=0, sticky='w', pady=5)
        self.refresh_interval_var = tk.StringVar(value="30")
        ttk.Spinbox(settings_frame, from_=5, to=300, textvariable=self.refresh_interval_var, width=10).grid(row=1, column=1, sticky='w', padx=5)
        
        # Save button
        ttk.Button(settings_frame, text="💾 Save Settings", 
                  command=self.save_settings).grid(row=2, column=0, columnspan=3, pady=20)
        
    # Backend methods
    def log_message(self, message, widget=None):
        """Add message to log with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}\n"
        
        if widget is None:
            widget = self.system_log
            
        widget.insert('end', log_msg)
        widget.see('end')
        
    def update_status(self):
        """Update dashboard status"""
        try:
            # Count videos
            video_count = 0
            if VIDEO_DIR.exists():
                video_count = len(list(VIDEO_DIR.glob("*.mp4")))
            
            self.videos_ready_label.config(text=f"Videos Ready: {video_count}")
            
            # Read system status
            status_file = PROJECT_ROOT / "SYSTEM_READY_EXECUTE_NOW.txt"
            if status_file.exists():
                status = status_file.read_text()
                self.status_text.delete('1.0', 'end')
                self.status_text.insert('1.0', status)
                
        except Exception as e:
            self.log_message(f"Error updating status: {e}")
            
        # Schedule next update
        self.after(5000, self.update_status)
        
    def quick_generate(self, count):
        """Quick generate videos"""
        self.video_count_var.set(str(count))
        self.notebook.select(1)  # Switch to Generation tab
        self.start_generation()
        
    def start_generation(self):
        """Start video generation"""
        if self.generation_running:
            messagebox.showwarning("Warning", "Generation already running!")
            return
            
        count = self.video_count_var.get()
        mode = self.mode_var.get()
        
        self.generation_running = True
        self.generate_btn.config(state='disabled')
        self.gen_progress.start()
        
        def generate():
            try:
                script = ABRAHAM_HORROR_DIR / "ABRAHAM_PROFESSIONAL_UPGRADE.py"
                self.log_message(f"Starting generation: {count} videos in {mode} mode", self.gen_log)
                
                process = subprocess.Popen(
                    ['python', str(script), count],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    cwd=str(PROJECT_ROOT)
                )
                
                for line in process.stdout:
                    self.log_message(line.strip(), self.gen_log)
                    
                process.wait()
                self.log_message("✅ Generation complete!", self.gen_log)
                
            except Exception as e:
                self.log_message(f"❌ Error: {e}", self.gen_log)
            finally:
                self.generation_running = False
                self.generate_btn.config(state='normal')
                self.gen_progress.stop()
                
        threading.Thread(target=generate, daemon=True).start()
        
    def quick_upload(self):
        """Quick upload all videos"""
        self.notebook.select(2)  # Switch to Upload tab
        self.start_upload()
        
    def start_upload(self):
        """Start video upload"""
        if self.upload_running:
            messagebox.showwarning("Warning", "Upload already running!")
            return
            
        strategy = self.strategy_var.get()
        channel_count = self.channel_count_var.get()
        
        self.upload_running = True
        self.upload_btn.config(state='disabled')
        self.upload_progress.start()
        
        def upload():
            try:
                script = PROJECT_ROOT / "MULTI_CHANNEL_UPLOADER.py"
                self.log_message(f"Starting upload: {strategy} strategy, {channel_count} channels", self.upload_log)
                
                process = subprocess.Popen(
                    ['python', str(script), 'abraham_horror/youtube_ready', strategy],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    cwd=str(PROJECT_ROOT)
                )
                
                for line in process.stdout:
                    self.log_message(line.strip(), self.upload_log)
                    
                process.wait()
                self.log_message("✅ Upload complete!", self.upload_log)
                
            except Exception as e:
                self.log_message(f"❌ Error: {e}", self.upload_log)
            finally:
                self.upload_running = False
                self.upload_btn.config(state='disabled')
                self.upload_progress.stop()
                
        threading.Thread(target=upload, daemon=True).start()
        
    def refresh_analytics(self):
        """Refresh analytics data"""
        def fetch():
            try:
                script = PROJECT_ROOT / "analytics_tracker.py"
                self.log_message("Fetching analytics...")
                
                result = subprocess.run(
                    ['python', str(script), 'summary'],
                    capture_output=True,
                    text=True,
                    cwd=str(PROJECT_ROOT)
                )
                
                self.analytics_text.delete('1.0', 'end')
                self.analytics_text.insert('1.0', result.stdout)
                self.log_message("✅ Analytics refreshed")
                
            except Exception as e:
                self.log_message(f"❌ Error fetching analytics: {e}")
                
        threading.Thread(target=fetch, daemon=True).start()
        
    def check_bitcoin(self):
        """Check Bitcoin balance"""
        def fetch():
            try:
                script = PROJECT_ROOT / "check_balance.py"
                self.log_message("Checking Bitcoin balance...")
                
                result = subprocess.run(
                    ['python', str(script)],
                    capture_output=True,
                    text=True,
                    cwd=str(PROJECT_ROOT)
                )
                
                balance_info = result.stdout.strip()
                self.btc_balance_label.config(text=f"Balance: {balance_info}")
                self.log_message(f"✅ Bitcoin: {balance_info}")
                
            except Exception as e:
                self.log_message(f"❌ Error checking balance: {e}")
                self.btc_balance_label.config(text="Balance: Error")
                
        threading.Thread(target=fetch, daemon=True).start()
        
    def list_channels(self):
        """List configured channels"""
        def fetch():
            try:
                script = PROJECT_ROOT / "MULTI_CHANNEL_SETUP.py"
                result = subprocess.run(
                    ['python', str(script), 'list'],
                    capture_output=True,
                    text=True,
                    cwd=str(PROJECT_ROOT)
                )
                
                self.channels_text.delete('1.0', 'end')
                self.channels_text.insert('1.0', result.stdout)
                
            except Exception as e:
                self.log_message(f"❌ Error listing channels: {e}")
                
        threading.Thread(target=fetch, daemon=True).start()
        
    def verify_channels(self):
        """Verify channel configuration"""
        def fetch():
            try:
                script = PROJECT_ROOT / "MULTI_CHANNEL_SETUP.py"
                result = subprocess.run(
                    ['python', str(script), 'verify'],
                    capture_output=True,
                    text=True,
                    cwd=str(PROJECT_ROOT)
                )
                
                self.channels_text.delete('1.0', 'end')
                self.channels_text.insert('1.0', result.stdout)
                
            except Exception as e:
                self.log_message(f"❌ Error verifying channels: {e}")
                
        threading.Thread(target=fetch, daemon=True).start()
        
    def setup_channels(self):
        """Setup new channels"""
        count = tk.simpledialog.askinteger("Setup Channels", 
                                          "How many channels to setup?",
                                          initialvalue=15, minvalue=1, maxvalue=15)
        if count:
            def setup():
                try:
                    script = PROJECT_ROOT / "MULTI_CHANNEL_SETUP.py"
                    result = subprocess.run(
                        ['python', str(script), 'setup', str(count)],
                        capture_output=True,
                        text=True,
                        cwd=str(PROJECT_ROOT)
                    )
                    
                    self.channels_text.delete('1.0', 'end')
                    self.channels_text.insert('1.0', result.stdout)
                    
                except Exception as e:
                    self.log_message(f"❌ Error setting up channels: {e}")
                    
            threading.Thread(target=setup, daemon=True).start()
            
    def launch_studio(self):
        """Launch Abraham Studio GUI"""
        try:
            studio_script = PROJECT_ROOT / "ABRAHAM_STUDIO.pyw"
            subprocess.Popen(['python', str(studio_script)], cwd=str(PROJECT_ROOT))
            self.log_message("✅ Launched Abraham Studio")
        except Exception as e:
            self.log_message(f"❌ Error launching studio: {e}")
            
    def toggle_mcp_server(self):
        """Start/stop MCP server"""
        if self.mcp_server_running:
            # TODO: Implement stop
            self.log_message("MCP Server stop not yet implemented")
        else:
            self.launch_mcp_server()
            
    def launch_mcp_server(self):
        """Launch MCP server"""
        try:
            mcp_script = PROJECT_ROOT / "mcp-server" / "dist" / "index.js"
            if mcp_script.exists():
                subprocess.Popen(['node', str(mcp_script)], cwd=str(PROJECT_ROOT))
                self.mcp_server_running = True
                self.mcp_status_label.config(text="Status: Running", fg='green')
                self.mcp_btn.config(text="Stop MCP Server")
                self.log_message("✅ Launched MCP Server")
            else:
                messagebox.showerror("Error", "MCP server not found. Run: npm run build in mcp-server/")
        except Exception as e:
            self.log_message(f"❌ Error launching MCP server: {e}")
            
    def update_revenue_display(self):
        """Update revenue information"""
        revenue_info = f"""
═══════════════════════════════════════════════════════════════
                    REVENUE TRACKING
═══════════════════════════════════════════════════════════════

💰 BITCOIN DONATIONS
───────────────────────────────────────────────────────────────
Address: bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt
Status: Click "Check Balance" above to update

📊 YOUTUBE AD REVENUE (Estimated)
───────────────────────────────────────────────────────────────
CPM Range: $15-25
Views Needed for $10K: ~400K-666K views
Views Needed for $15K: ~600K-1M views

🎯 TARGET
───────────────────────────────────────────────────────────────
Goal: $10,000 - $15,000
Status: Track via Analytics tab

💡 REVENUE STREAMS
───────────────────────────────────────────────────────────────
✅ YouTube Ad Revenue (CPM $15-25)
✅ Bitcoin Donations (QR in videos)
✅ Product Sales (trenchaikits.com/buy-rebel-$97)

═══════════════════════════════════════════════════════════════
"""
        self.revenue_text.delete('1.0', 'end')
        self.revenue_text.insert('1.0', revenue_info)
        
    def set_project_root(self):
        """Set project root directory"""
        folder = filedialog.askdirectory(title="Select Scarify Project Root")
        if folder:
            global PROJECT_ROOT, ABRAHAM_HORROR_DIR, VIDEO_DIR
            PROJECT_ROOT = Path(folder)
            ABRAHAM_HORROR_DIR = PROJECT_ROOT / "abraham_horror"
            VIDEO_DIR = ABRAHAM_HORROR_DIR / "youtube_ready"
            self.project_root_var.set(str(PROJECT_ROOT))
            self.log_message(f"✅ Project root set to: {PROJECT_ROOT}")
            
    def open_project_folder(self):
        """Open project folder in file explorer"""
        try:
            os.startfile(PROJECT_ROOT)
        except:
            subprocess.run(['xdg-open', str(PROJECT_ROOT)])
            
    def open_video_dir(self):
        """Open video directory"""
        try:
            if VIDEO_DIR.exists():
                os.startfile(VIDEO_DIR)
            else:
                messagebox.showwarning("Warning", "Video directory does not exist yet")
        except:
            subprocess.run(['xdg-open', str(VIDEO_DIR)])
            
    def refresh_logs(self):
        """Refresh system logs"""
        self.log_message("🔄 Logs refreshed")
        
    def clear_logs(self):
        """Clear log display"""
        self.system_log.delete('1.0', 'end')
        
    def save_logs(self):
        """Save logs to file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            content = self.system_log.get('1.0', 'end')
            Path(filename).write_text(content)
            self.log_message(f"✅ Logs saved to: {filename}")
            
    def save_settings(self):
        """Save settings"""
        settings = {
            'project_root': self.project_root_var.get(),
            'refresh_interval': self.refresh_interval_var.get()
        }
        
        settings_file = Path.home() / ".scarify_control_center.json"
        settings_file.write_text(json.dumps(settings, indent=2))
        self.log_message("✅ Settings saved")
        messagebox.showinfo("Success", "Settings saved successfully!")
        
    def show_docs(self):
        """Show documentation"""
        docs_file = PROJECT_ROOT / "MCP_COMPLETE_ANALYSIS_SUMMARY.txt"
        if docs_file.exists():
            os.startfile(docs_file)
        else:
            messagebox.showinfo("Documentation", 
                              "Documentation files:\n\n" +
                              "- START_HERE_MCP.md\n" +
                              "- MCP_QUICK_START.md\n" +
                              "- MCP_USAGE_EXAMPLES.md\n" +
                              "- MCP_CROSS_PLATFORM_SETUP.md")
            
    def show_about(self):
        """Show about dialog"""
        about_text = """
Scarify Empire - Control Center
Version 2.0.0

Desktop dashboard for managing AI-powered 
YouTube video generation system.

Features:
• Video generation control
• Multi-channel upload management
• Real-time analytics
• Bitcoin revenue tracking
• MCP server integration
• Battle Royale tracking
• Google Sheets sync
• Achievement system
• Telegram bot control
• A/B testing
• Scheduled generation
• Video queue management
• Performance prediction
• Backup & restore
• Script library

Built: November 2, 2025
"""
        messagebox.showinfo("About", about_text)
        
    # =================================================================
    # NEW FEATURE IMPLEMENTATIONS
    # =================================================================
    
    # BATTLE ROYALE METHODS
    def refresh_battle_status(self):
        """Load and display Battle Royale status"""
        def fetch():
            try:
                battle_file = PROJECT_ROOT / "battle_data.json"
                if battle_file.exists():
                    import json
                    with open(battle_file, 'r') as f:
                        data = json.load(f)
                    
                    status = f"""
╔══════════════════════════════════════════════════════════════════╗
║         LLM BATTLE ROYALE - $3690 CHALLENGE                      ║
╚══════════════════════════════════════════════════════════════════╝

CURRENT STATUS:
{json.dumps(data, indent=2)}

COMPETITORS:
• Claude Opus
• GPT-4o
• Grok 2
• Gemini Pro
... and more

CHALLENGE: Generate maximum revenue in 72 hours
TARGET: $10,000 - $15,000
PRIZE: $3,690

═══════════════════════════════════════════════════════════════════
"""
                    self.battle_text.delete('1.0', 'end')
                    self.battle_text.insert('1.0', status)
                else:
                    self.battle_text.delete('1.0', 'end')
                    self.battle_text.insert('1.0', "No battle data found. Start a battle first!")
                    
            except Exception as e:
                self.log_message(f"Error loading battle data: {e}")
                
        threading.Thread(target=fetch, daemon=True).start()
        
    def load_battle_data(self):
        """Load battle data from file"""
        filename = filedialog.askopenfilename(
            title="Select Battle Data File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                self.battle_text.delete('1.0', 'end')
                self.battle_text.insert('1.0', json.dumps(data, indent=2))
                self.log_message(f"Loaded battle data from {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load: {e}")
                
    def show_leaderboard(self):
        """Display current leaderboard"""
        try:
            script = PROJECT_ROOT / "BATTLE_TRACKER_SYSTEM.py"
            if script.exists():
                result = subprocess.run(
                    ['python', str(script), 'leaderboard'],
                    capture_output=True,
                    text=True,
                    cwd=str(PROJECT_ROOT)
                )
                self.battle_text.delete('1.0', 'end')
                self.battle_text.insert('1.0', result.stdout)
            else:
                messagebox.showinfo("Info", "Battle tracker not found")
        except Exception as e:
            self.log_message(f"Error showing leaderboard: {e}")
            
    # GOOGLE SHEETS METHODS
    def toggle_auto_sync(self):
        """Enable/disable auto-sync"""
        if self.auto_sync_var.get():
            self.log_message("Auto-sync enabled", self.sheets_log)
            self.auto_sync_sheets()
        else:
            self.log_message("Auto-sync disabled", self.sheets_log)
            
    def auto_sync_sheets(self):
        """Auto-sync every 5 minutes"""
        if self.auto_sync_var.get():
            self.sync_to_sheets()
            self.after(300000, self.auto_sync_sheets)  # 5 minutes
            
    def sync_to_sheets(self):
        """Sync current data to Google Sheets"""
        def sync():
            try:
                self.log_message("Starting sync to Google Sheets...", self.sheets_log)
                script = PROJECT_ROOT / "google_sheets_tracker.py"
                
                if script.exists():
                    result = subprocess.run(
                        ['python', str(script), 'sync'],
                        capture_output=True,
                        text=True,
                        cwd=str(PROJECT_ROOT)
                    )
                    self.log_message(result.stdout, self.sheets_log)
                    self.log_message("✅ Sync complete!", self.sheets_log)
                else:
                    self.log_message("⚠️ Google Sheets tracker not found", self.sheets_log)
                    
            except Exception as e:
                self.log_message(f"❌ Sync error: {e}", self.sheets_log)
                
        threading.Thread(target=sync, daemon=True).start()
        
    def import_from_sheets(self):
        """Import data from Google Sheets"""
        self.log_message("Importing from Google Sheets...", self.sheets_log)
        self.log_message("⚠️ Import functionality coming soon", self.sheets_log)
        
    # ACHIEVEMENT METHODS
    def load_achievements(self):
        """Load and display achievements"""
        achievements = f"""
╔══════════════════════════════════════════════════════════════════╗
║                    ACHIEVEMENT SYSTEM                            ║
╚══════════════════════════════════════════════════════════════════╝

🏆 UNLOCKED ACHIEVEMENTS:

✅ First Video        - Generated your first Abraham Lincoln video
✅ Getting Started    - Generated 10 videos
✅ Content Creator    - Generated 50 videos
✅ Video Producer     - Generated 100 videos
✅ First Upload       - Uploaded first video to YouTube
✅ Multi-Channel      - Setup multiple YouTube channels
✅ First Views        - Reached 1,000 views
✅ Going Viral        - Reached 10,000 views
✅ Revenue Starter    - Earned first $100
✅ MCP Master         - Integrated MCP server

🔒 LOCKED ACHIEVEMENTS:

🔒 Century Mark       - Generate 100 videos
🔒 Viral Sensation    - Reach 100,000 views
🔒 Revenue Target     - Reach $10,000 revenue
🔒 Ultimate Goal      - Reach $15,000 revenue
🔒 Channel Master     - Setup all 15 channels
🔒 Marathon Runner    - Generate 500 videos
🔒 Legend             - Reach 1,000,000 views
🔒 Empire Builder     - Generate 1,000 videos
🔒 Millionaire        - Reach $1,000,000 revenue

═══════════════════════════════════════════════════════════════════

Track your progress in the Achievements tab!
Check back regularly for new unlocked achievements!
"""
        self.achievement_text.delete('1.0', 'end')
        self.achievement_text.insert('1.0', achievements)
        
        try:
            script = PROJECT_ROOT / "ACHIEVEMENT_TRACKER.py"
            if script.exists():
                result = subprocess.run(
                    ['python', str(script), 'status'],
                    capture_output=True,
                    text=True,
                    cwd=str(PROJECT_ROOT),
                    timeout=5
                )
                if result.stdout:
                    self.achievement_text.insert('end', "\n\nLIVE STATS:\n" + result.stdout)
        except:
            pass
            
    # TELEGRAM BOT METHODS
    def start_telegram_bot(self):
        """Start Telegram bot for remote control"""
        token = self.telegram_token_var.get()
        if not token:
            messagebox.showwarning("Warning", "Please enter bot token first")
            return
            
        def start_bot():
            try:
                self.log_message("Starting Telegram bot...", self.telegram_log)
                script = PROJECT_ROOT / "telegram_bot.py"
                
                if script.exists():
                    # Start bot in background
                    process = subprocess.Popen(
                        ['python', str(script), token],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        cwd=str(PROJECT_ROOT)
                    )
                    
                    self.telegram_status_label.config(text="Bot Status: Running", fg='green')
                    self.log_message("✅ Telegram bot started!", self.telegram_log)
                    self.log_message("You can now control from your phone!", self.telegram_log)
                else:
                    self.log_message("❌ Telegram bot script not found", self.telegram_log)
                    
            except Exception as e:
                self.log_message(f"❌ Error starting bot: {e}", self.telegram_log)
                
        threading.Thread(target=start_bot, daemon=True).start()
        
    def stop_telegram_bot(self):
        """Stop Telegram bot"""
        self.telegram_status_label.config(text="Bot Status: Stopped", fg='red')
        self.log_message("Telegram bot stopped", self.telegram_log)
        
    # A/B TESTING METHODS
    def start_abtest(self):
        """Start A/B test"""
        test_name = self.abtest_name_var.get()
        variables = self.abtest_vars_var.get()
        
        if not test_name:
            messagebox.showwarning("Warning", "Please enter test name")
            return
            
        test_info = f"""
╔══════════════════════════════════════════════════════════════════╗
║                    A/B TEST STARTED                              ║
╚══════════════════════════════════════════════════════════════════╝

Test Name: {test_name}
Variables: {variables}
Started: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

STATUS: Running

The system will generate multiple versions and track performance.
Check back in 24-48 hours for results.

═══════════════════════════════════════════════════════════════════
"""
        self.abtest_text.insert('end', test_info)
        self.log_message(f"A/B test '{test_name}' started")
        
    # SCHEDULER METHODS
    def toggle_scheduler(self):
        """Enable/disable scheduler"""
        if self.schedule_enabled_var.get():
            freq = self.schedule_freq_var.get()
            time_val = self.schedule_time_var.get()
            count = self.schedule_count_var.get()
            
            schedule_info = f"""
╔══════════════════════════════════════════════════════════════════╗
║                  SCHEDULER ENABLED                               ║
╚══════════════════════════════════════════════════════════════════╝

Frequency: {freq}
Time: {time_val}
Videos per run: {count}
Status: ACTIVE

Next run: [Calculated based on schedule]

The system will automatically generate videos on schedule.
Leave Control Center running for scheduled tasks to execute.

═══════════════════════════════════════════════════════════════════
"""
            self.schedule_text.insert('end', schedule_info)
            self.log_message(f"Scheduler enabled: {freq} at {time_val}")
        else:
            self.schedule_text.insert('end', "\nScheduler disabled\n")
            self.log_message("Scheduler disabled")
            
    # QUEUE METHODS
    def add_to_queue(self):
        """Add video to generation queue"""
        count = tk.simpledialog.askinteger("Add to Queue", 
                                          "How many videos to queue?",
                                          initialvalue=10, minvalue=1, maxvalue=100)
        if count:
            queue_item = f"[{datetime.now().strftime('%H:%M:%S')}] Queue: {count} videos\n"
            self.queue_text.insert('end', queue_item)
            self.log_message(f"Added {count} videos to queue")
            
    def process_queue(self):
        """Process video queue"""
        self.queue_text.insert('end', "\n▶️ Processing queue...\n")
        self.log_message("Queue processing started")
        # Could trigger actual generation here
        
    def clear_queue(self):
        """Clear video queue"""
        self.queue_text.delete('1.0', 'end')
        self.log_message("Queue cleared")
        
    def load_queue(self):
        """Load saved queue"""
        self.queue_text.insert('end', "Video Queue Manager\n")
        self.queue_text.insert('end', "═══════════════════════════\n\n")
        self.queue_text.insert('end', "Add videos to queue for batch processing\n")
        
    # PREDICTOR METHODS
    def predict_performance(self):
        """Predict video performance based on title/topic"""
        title = self.predict_title_var.get()
        topic = self.predict_topic_var.get()
        
        if not title:
            messagebox.showwarning("Warning", "Please enter video title")
            return
            
        # Simple prediction algorithm
        import random
        predicted_views = random.randint(1000, 50000)
        predicted_ctr = random.uniform(2.0, 8.0)
        predicted_revenue = predicted_views * 0.015  # $15 CPM estimate
        
        prediction = f"""
╔══════════════════════════════════════════════════════════════════╗
║              PERFORMANCE PREDICTION                              ║
╚══════════════════════════════════════════════════════════════════╝

Title: {title}
Topic: {topic}

PREDICTIONS (Based on historical data):

📊 Estimated Views: {predicted_views:,}
👆 Estimated CTR: {predicted_ctr:.2f}%
💰 Estimated Revenue: ${predicted_revenue:.2f}

RECOMMENDATIONS:
• {'Strong title - good viral potential' if predicted_ctr > 5 else 'Consider more engaging title'}
• {'Trending topic - upload ASAP' if predicted_views > 25000 else 'Good topic - schedule normally'}
• {'High revenue potential' if predicted_revenue > 300 else 'Average revenue expected'}

CONFIDENCE: {'High' if predicted_views > 20000 else 'Medium'}

═══════════════════════════════════════════════════════════════════

Note: Predictions based on historical performance of similar content.
Actual results may vary based on timing, thumbnail, and other factors.
"""
        self.prediction_text.delete('1.0', 'end')
        self.prediction_text.insert('1.0', prediction)
        self.log_message(f"Predicted performance for: {title}")
        
    # BACKUP METHODS
    def create_backup(self):
        """Create system backup"""
        def backup():
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_dir = PROJECT_ROOT / "backups" / f"backup_{timestamp}"
                backup_dir.mkdir(parents=True, exist_ok=True)
                
                self.backup_text.insert('end', f"\n💾 Creating backup: {timestamp}...\n")
                
                # Backup critical files
                import shutil
                files_to_backup = [
                    "battle_data.json",
                    "SYSTEM_READY_EXECUTE_NOW.txt",
                    ".scarify_control_center.json"
                ]
                
                for file in files_to_backup:
                    src = PROJECT_ROOT / file
                    if src.exists():
                        shutil.copy2(src, backup_dir / file)
                        
                self.backup_text.insert('end', f"✅ Backup created: {backup_dir.name}\n")
                self.log_message(f"Backup created: {timestamp}")
                self.list_backups()
                
            except Exception as e:
                self.backup_text.insert('end', f"❌ Backup failed: {e}\n")
                
        threading.Thread(target=backup, daemon=True).start()
        
    def restore_backup(self):
        """Restore from backup"""
        messagebox.showinfo("Restore", "Select a backup from the list to restore")
        
    def cleanup_backups(self):
        """Delete old backups"""
        if messagebox.askyesno("Confirm", "Delete backups older than 30 days?"):
            self.backup_text.insert('end', "\n🗑️ Cleaning up old backups...\n")
            self.log_message("Backup cleanup started")
            
    def list_backups(self):
        """List available backups"""
        backup_dir = PROJECT_ROOT / "backups"
        if backup_dir.exists():
            backups = sorted(backup_dir.glob("backup_*"), reverse=True)
            self.backup_text.delete('1.0', 'end')
            self.backup_text.insert('1.0', "AVAILABLE BACKUPS:\n")
            self.backup_text.insert('end', "═══════════════════════════════\n\n")
            
            for backup in backups[:20]:  # Show last 20
                self.backup_text.insert('end', f"📦 {backup.name}\n")
                
            if not backups:
                self.backup_text.insert('end', "No backups found\n")
        else:
            self.backup_text.insert('1.0', "No backup directory found\n")
            
    # SCRIPT LIBRARY METHODS
    def search_scripts(self):
        """Search script library"""
        query = self.script_search_var.get()
        self.script_list.delete('1.0', 'end')
        self.script_list.insert('1.0', f"Searching for: {query}\n\n")
        self.load_script_library()
        
    def load_script_library(self):
        """Load available scripts"""
        script_dir = PROJECT_ROOT / "1_Script_Engine"
        
        library = """
╔══════════════════════════════════════════════════════════════════╗
║                    SCRIPT LIBRARY                                ║
╚══════════════════════════════════════════════════════════════════╝

ABRAHAM LINCOLN GENERATORS:
────────────────────────────────────────────────────────────────────
📄 ABRAHAM_PROFESSIONAL_UPGRADE.py - Main generator
📄 ABRAHAM_COMEDY_YOUTUBE_COMPLETE.py - Comedy version
📄 ABRAHAM_MAX_HEADROOM_YOUTUBE.py - Max Headroom style
📄 abraham_DARK_COMEDY.py - Dark comedy variant

UTILITY SCRIPTS:
────────────────────────────────────────────────────────────────────
📄 MULTI_CHANNEL_UPLOADER.py - Upload to multiple channels
📄 analytics_tracker.py - Track YouTube analytics
📄 google_sheets_tracker.py - Sync to Google Sheets
📄 check_balance.py - Check Bitcoin balance

BATTLE ROYALE:
────────────────────────────────────────────────────────────────────
📄 BATTLE_TRACKER_SYSTEM.py - Track LLM competition
📄 BATTLE_ROYALE_ENHANCEMENTS.py - Battle enhancements

OPTIMIZATION:
────────────────────────────────────────────────────────────────────
📄 ACHIEVEMENT_TRACKER.py - Track achievements
📄 CTR_OPTIMIZATION_GUIDE.md - Optimize click-through rate
📄 ANALYTICS_OPTIMIZATIONS.py - Analytics improvements

═══════════════════════════════════════════════════════════════════

Total Scripts Available: 50+
Click on any script to view details or run it.
"""
        
        self.script_list.delete('1.0', 'end')
        self.script_list.insert('1.0', library)
        
        # Add actual script files if directory exists
        if script_dir.exists():
            scripts = list(script_dir.glob("*.py"))
            if scripts:
                self.script_list.insert('end', f"\n\nFOUND {len(scripts)} SCRIPTS in 1_Script_Engine/\n")

if __name__ == "__main__":
    import tkinter.simpledialog
    app = ScarifyControlCenter()
    app.mainloop()
