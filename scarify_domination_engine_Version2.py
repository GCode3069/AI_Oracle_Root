"""
SCARIFY Domination Engine - One-File Executable Bootstrapper
Organizes workspace, optimizes system, runs horror content pipeline (narration, video, upload).
Designed for collaborative editing with Cursor or any code editor.

Usage:
    python scarify_domination_engine.py

Requirements:
    - Python 3.8+
    - Powershell available on Windows
    - All dependencies installed (see 'install_dependencies' step)
"""

import os
import sys
import shutil
import subprocess
import json
from pathlib import Path

# --- CONFIG ---
ROOT = Path(__file__).parent.resolve()
FOLDERS = ["core", "horror_assets", "audio", "video", "archive", "docs", "temp"]
MANIFEST_PATH = ROOT / "core" / "SCARIFY_manifest.json"
SYSINFO_PATH = ROOT / "core" / "system_info.json"

# --- UTILS ---
def ensure_folders():
    for folder in FOLDERS:
        (ROOT / folder).mkdir(exist_ok=True)

def move_files():
    for file in ROOT.glob("*"):
        if not file.is_file(): continue
        dest = None
        if file.name.startswith("abraham_") and file.suffix == ".py":
            dest = "core"
        elif file.suffix in [".mp3", ".wav"]:
            dest = "audio"
        elif file.suffix in [".mp4", ".mov"]:
            dest = "video"
        elif file.suffix in [".md", ".txt", ".pdf"]:
            dest = "docs"
        elif "horror" in file.name or "lincoln" in file.name:
            dest = "horror_assets"
        elif file.suffix in [".json", ".toml"]:
            dest = "core"
        if dest:
            shutil.move(str(file), str(ROOT / dest / file.name))

def remove_duplicates():
    seen = {}
    for folder in FOLDERS:
        files = list((ROOT / folder).glob("*"))
        for f in files:
            key = f.name
            if key in seen:
                # Keep the latest modified file
                if f.stat().st_mtime > seen[key].stat().st_mtime:
                    seen[key].unlink()
                    seen[key] = f
                else:
                    f.unlink()
            else:
                seen[key] = f

def log_manifest():
    manifest = []
    for folder in FOLDERS:
        for file in (ROOT / folder).glob("*"):
            if file.is_file():
                manifest.append({
                    "file": file.name,
                    "folder": folder,
                    "modified": file.stat().st_mtime
                })
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)

def log_system_info():
    # Windows: Use Powershell for detailed info
    if sys.platform.startswith("win"):
        ps_script = "[ordered]@{CsName=(Get-ComputerInfo).CsName;OsName=(Get-ComputerInfo).OsName;" \
                    "WindowsVersion=(Get-ComputerInfo).WindowsVersion;OsArchitecture=(Get-ComputerInfo).OsArchitecture;" \
                    "CsProcessorCount=(Get-ComputerInfo).CsProcessorCount;CsTotalPhysicalMemory=(Get-ComputerInfo).CsTotalPhysicalMemory} | ConvertTo-Json"
        result = subprocess.run(["powershell", "-Command", ps_script], capture_output=True, text=True)
        sysinfo = json.loads(result.stdout)
    else:
        sysinfo = {
            "hostname": os.uname().nodename,
            "os": os.uname().sysname,
            "release": os.uname().release,
            "cpu_count": os.cpu_count(),
            "ram": "Unknown"
        }
    with open(SYSINFO_PATH, "w") as f:
        json.dump(sysinfo, f, indent=2)

def optimize_windows():
    # High Performance Power Plan
    try:
        powercfg = 'powercfg -L'
        result = subprocess.run(["powershell", "-Command", powercfg], capture_output=True, text=True)
        lines = result.stdout.splitlines()
        guid = None
        for line in lines:
            if "High performance" in line:
                parts = line.split()
                guid = parts[3] if len(parts) > 3 else None
                break
        if guid:
            subprocess.run(["powershell", "-Command", f"powercfg -S {guid}"])
        # Clean temp
        subprocess.run(["powershell", "-Command", 'Remove-Item -Path $env:TEMP\\* -Recurse -Force -ErrorAction SilentlyContinue'])
    except Exception as e:
        print(f"System optimization skipped: {e}")

def install_dependencies():
    # Optionally, check and install required Python packages
    try:
        import pip
    except ImportError:
        print("pip not found. Please install pip!")
        return
    pkgs = [
        "google-auth-oauthlib", "google-auth", "google-api-python-client",
        "httpx", "aiohttp", "sqlalchemy",
        "moviepy", "pillow", "pydub",
        "elevenlabs", "runwayml"
    ]
    for pkg in pkgs:
        subprocess.run([sys.executable, "-m", "pip", "install", pkg])

def run_step(name, func):
    print(f"\n=== {name} ===")
    try:
        func()
        print(f"{name} complete.")
    except Exception as e:
        print(f"Error in {name}: {e}")
        sys.exit(1)

# --- PIPELINE SKELETONS ---
def generate_narration():
    # Pseudo-code for ElevenLabs/psych audio
    print("Generating Jiminex Lincoln horror narration...")
    # TODO: Integrate ElevenLabs API, psychological overlays, save to audio/horror_narration.mp3

def generate_video():
    print("Generating video with RunwayML API...")
    # TODO: Use RunwayML API, sync to narration, save to video/lincoln_horror.mp4

def youtube_upload():
    print("Uploading video to YouTube...")
    # TODO: Use YouTube Data API, auto-fill metadata, enforce script-only uploads

# --- MAIN BOOTSTRAP ---
def main():
    print("SCARIFY Domination Engine - Bootstrap Starting...")
    ensure_folders()
    move_files()
    remove_duplicates()
    log_manifest()
    log_system_info()
    if sys.platform.startswith("win"):
        optimize_windows()
    run_step("Dependency Installation", install_dependencies)
    run_step("Narration Generation", generate_narration)
    run_step("Video Generation", generate_video)
    run_step("YouTube Upload", youtube_upload)
    print("\nSCARIFY pipeline complete! Check the video folder for your viral horror content.")

if __name__ == "__main__":
    main()

# --- COLLABORATIVE EDITING TIP ---
"""
For collaborative build in Cursor or VSCode:
- Use TODOs above each major function for teammates to fill in API integrations.
- Edit/extend FOLDERS, manifest logic, and pipeline skeletons as project grows.
- Save this script at project root; all folders/files are auto-managed.
"""