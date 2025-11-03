#!/usr/bin/env python3
"""
ABRAHAM STUDIO - Desktop App for Batch Horror Video Generation
Professional GUI with Region-Based Headlines & Multi-Language Support
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys
import threading
import json
from pathlib import Path
from datetime import datetime
import subprocess

# Import generator
sys.path.insert(0, str(Path(__file__).parent))

BASE_DIR = Path("F:/AI_Oracle_Root/scarify/abraham_horror")

# ============================================================================
# REGION-BASED HEADLINES & LANGUAGES
# ============================================================================

REGIONS = {
    "USA (National)": {
        "headlines": [
            "Corrupt Government Officials - 69% Fear",
            "Cyber-Terrorism Surge - 55.9% Americans Terrified",
            "Economic Collapse Imminent - 58.2% Fear",
            "Political Violence Escalates Nationwide"
        ],
        "language": "en"
    },
    "USA - Texas": {
        "headlines": [
            "Border Crisis Intensifies - Families Fleeing",
            "Wildfires Rage Across State - Evacuations Ordered",
            "ICE Raids Target Undocumented Communities",
            "Power Grid Failures - Blackouts Expected"
        ],
        "language": "en"
    },
    "USA - California": {
        "headlines": [
            "Wildfires Threaten Entire Communities",
            "Homeless Crisis Explodes - Streets Overflow",
            "Power Outages Force Business Shutdowns",
            "Earthquake Risk Spikes - Experts Warn Big One"
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
            "Hurricane Threat Forces Emergency Evacuations",
            "Rising Sea Levels - Coastal Properties Sinking",
            "Insurance Companies Flee State - Crisis Looms",
            "Extreme Heat Breaks Records - Health Emergency"
        ],
        "language": "en"
    },
    "Spain": {
        "headlines": [
            "Crisis Económica - Desempleo Supera 15%",
            "Ola de Calor - Incendios Forestales Arden",
            "Conflictos Políticos - Tensión en Aumento",
            "Crisis Migratoria - Estado de Emergencia"
        ],
        "language": "es"
    },
    "Mexico": {
        "headlines": [
            "Crimen Organizado - Violencia Escalada",
            "Crisis de Sequía - Suministro de Agua Falla",
            "Inflación Galopante - Precios se Disparan",
            "Desastre Natural - Comunidades Devastadas"
        ],
        "language": "es"
    },
    "United Kingdom": {
        "headlines": [
            "Economic Recession Deepens - Millions Jobless",
            "Climate Crisis - Coastal Flooding Spreading",
            "Political Turmoil - Government Collapse Risk",
            "Cyber Attacks Target Critical Infrastructure"
        ],
        "language": "en"
    },
    "Brazil": {
        "headlines": [
            "Crises Climáticas - Inundações Devastadoras",
            "Violência Urbana - Taxas de Homicídio Disparam",
            "Recessão Econômica - Desemprego em Alta",
            "Corrupção Política - Escândalos Expostos"
        ],
        "language": "pt"
    },
    "Germany": {
        "headlines": [
            "Energiekrise - Blackouts Drohen",
            "Inflationsanstieg - Preise Steigen Stark",
            "Klimakatastrophe - Extreme Wetter",
            "Cybersicherheit - Angriffe auf Infrastruktur"
        ],
        "language": "de"
    }
}

class AbrahamStudio(tk.Tk):
    """Main desktop application"""
    
    def __init__(self):
        super().__init__()
        
        self.title("ABRAHAM STUDIO - Horror Video Generator")
        self.geometry("900x700")
        self.resizable(True, True)
        
        # Variables
        self.region_var = tk.StringVar(value="USA (National)")
        self.count_var = tk.IntVar(value=5)
        self.language_var = tk.StringVar(value="en")
        self.mode_var = tk.StringVar(value="auto")
        self.upload_var = tk.BooleanVar(value=False)
        
        self.create_widgets()
        self.load_generator()
    
    def create_widgets(self):
        """Create main GUI widgets"""
        
        # Header
        header = ttk.Label(
            self, 
            text="🎃 ABRAHAM STUDIO - BATCH HORROR VIDEO GENERATOR",
            font=("Arial", 16, "bold")
        )
        header.pack(pady=10)
        
        # Region Selection
        region_frame = ttk.LabelFrame(self, text="Region & Trending Topics", padding=10)
        region_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(region_frame, text="Select Region:").grid(row=0, column=0, sticky="w", pady=5)
        
        self.region_combo = ttk.Combobox(
            region_frame, 
            textvariable=self.region_var,
            values=list(REGIONS.keys()),
            state="readonly",
            width=50
        )
        self.region_combo.grid(row=0, column=1, sticky="ew", padx=10)
        self.region_combo.bind('<<ComboboxSelected>>', self.on_region_change)
        
        # Language Display
        ttk.Label(region_frame, text="Language:").grid(row=1, column=0, sticky="w", pady=5)
        self.language_label = ttk.Label(region_frame, text="en", font=("Arial", 12, "bold"))
        self.language_label.grid(row=1, column=1, sticky="w", padx=10)
        
        # Headlines Preview
        ttk.Label(region_frame, text="Available Headlines:").grid(row=2, column=0, sticky="nw", pady=5)
        
        self.headlines_text = scrolledtext.ScrolledText(
            region_frame, 
            height=4, 
            width=50,
            wrap=tk.WORD
        )
        self.headlines_text.grid(row=2, column=1, sticky="ew", padx=10)
        region_frame.columnconfigure(1, weight=1)
        
        # Generation Settings
        settings_frame = ttk.LabelFrame(self, text="Generation Settings", padding=10)
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
        
        ttk.Label(settings_frame, text="Generation Mode:").grid(row=1, column=0, sticky="w", pady=5)
        mode_combo = ttk.Combobox(
            settings_frame,
            textvariable=self.mode_var,
            values=["auto", "ai", "template"],
            state="readonly",
            width=20
        )
        mode_combo.grid(row=1, column=1, sticky="w", padx=10)
        
        # Upload Option
        upload_check = ttk.Checkbutton(
            settings_frame,
            text="Upload to YouTube automatically",
            variable=self.upload_var
        )
        upload_check.grid(row=2, column=0, columnspan=2, sticky="w", pady=10)
        
        # Halloween Optimization
        halloween_frame = ttk.LabelFrame(self, text="🎃 Halloween 2025 Optimization", padding=10)
        halloween_frame.pack(fill="x", padx=20, pady=10)
        
        tips = [
            "✓ Viral-optimized titles for maximum engagement",
            "✓ Fear-based keywords (69% fear triggers)",
            "✓ Historical horror angle increases shares",
            "✓ 15-second duration perfect for Shorts algorithm",
            "✓ Region-specific content boosts local relevance"
        ]
        
        for tip in tips:
            label = ttk.Label(halloween_frame, text=tip, font=("Arial", 9))
            label.pack(anchor="w", pady=2)
        
        # Control Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        self.generate_btn = ttk.Button(
            button_frame,
            text="🚀 GENERATE BATCH VIDEOS",
            command=self.start_generation,
            style="Accent.TButton"
        )
        self.generate_btn.pack(side="left", padx=5)
        
        ttk.Button(
            button_frame,
            text="📁 Open Output Folder",
            command=self.open_folder
        ).pack(side="left", padx=5)
        
        ttk.Button(
            button_frame,
            text="❌ Cancel",
            command=self.cancel
        ).pack(side="left", padx=5)
        
        # Progress
        self.progress = ttk.Progressbar(
            self, 
            length=400, 
            mode='determinate'
        )
        self.progress.pack(padx=20, pady=10)
        
        # Log Output
        log_frame = ttk.LabelFrame(self, text="Generation Log", padding=10)
        log_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=10,
            wrap=tk.WORD
        )
        self.log_text.pack(fill="both", expand=True)
        
        # Load initial region
        self.on_region_change()
    
    def on_region_change(self, event=None):
        """Update UI when region changes"""
        region = self.region_var.get()
        if region in REGIONS:
            config = REGIONS[region]
            
            # Update language
            lang = config["language"]
            self.language_label.config(text=lang.upper())
            
            # Update headlines preview
            self.headlines_text.delete(1.0, tk.END)
            headlines = "\n".join([f"• {h}" for h in config["headlines"]])
            self.headlines_text.insert(1.0, headlines)
    
    def load_generator(self):
        """Load the Python generator script"""
        pass
    
    def log(self, message):
        """Add message to log"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.update()
    
    def start_generation(self):
        """Start batch generation in background thread"""
        if not self.generate_btn["state"] == "normal":
            return
        
        self.generate_btn.config(state="disabled")
        self.progress.config(maximum=self.count_var.get())
        self.progress["value"] = 0
        self.log_text.delete(1.0, tk.END)
        
        # Run in background thread
        thread = threading.Thread(target=self.run_generation, daemon=True)
        thread.start()
    
    def run_generation(self):
        """Run batch generation"""
        try:
            self.log("🎃 ABRAHAM STUDIO - BATCH GENERATION STARTED\n")
            
            region = self.region_var.get()
            count = self.count_var.get()
            mode = self.mode_var.get()
            upload = self.upload_var.get()
            
            self.log(f"Region: {region}")
            self.log(f"Count: {count} videos")
            self.log(f"Mode: {mode}")
            self.log(f"Upload: {upload}\n")
            
            # Import the generator
            generator_path = Path(__file__).parent / "ABRAHAM_AI_HORROR.ps1"
            
            if not generator_path.exists():
                self.log("❌ Generator script not found!")
                return
            
            # Build command
            cmd = f'powershell -ExecutionPolicy Bypass -File "{generator_path}" -Count {count}'
            
            self.log("Starting generation...")
            self.log("=" * 50)
            
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Stream output
            for line in process.stdout:
                self.log(line.strip())
                if "VIDEO GENERATED" in line:
                    self.progress.step()
                    self.update()
            
            process.wait()
            
            self.log("\n" + "=" * 50)
            self.log("✅ BATCH GENERATION COMPLETE!")
            
            messagebox.showinfo("Success", f"Generated {count} videos successfully!")
            
        except Exception as e:
            self.log(f"❌ ERROR: {e}")
            messagebox.showerror("Error", f"Generation failed: {e}")
        finally:
            self.generate_btn.config(state="normal")
            self.progress["value"] = self.progress["maximum"]
    
    def open_folder(self):
        """Open output folder"""
        folder = BASE_DIR / "youtube_ready"
        folder.mkdir(parents=True, exist_ok=True)
        
        if sys.platform == 'win32':
            os.startfile(folder)
        elif sys.platform == 'darwin':
            subprocess.run(['open', folder])
        else:
            subprocess.run(['xdg-open', folder])
    
    def cancel(self):
        """Cancel operation"""
        self.quit()


def main():
    """Launch application"""
    root = AbrahamStudio()
    root.mainloop()


if __name__ == "__main__":
    main()

