import os
import sys
import json
import time
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

print("🚀 YOUTUBE UPLOAD AUTOMATION - DESKTOP LAUNCHER 🚀")
print("=" * 70)

# PATHS
BASE_DIR = Path(r"F:\AI_Oracle_Root\scarify")
UPLOAD_DIR = BASE_DIR / "videos" / "youtube_ready"
DESKTOP_DIR = Path(os.path.expanduser("~/Desktop"))
CONFIG_FILE = BASE_DIR / "config" / "youtube_upload_config.json"

# CREATE DIRECTORIES
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
DESKTOP_DIR.mkdir(exist_ok=True)

def create_upload_config():
    """Create YouTube upload configuration"""
    if not CONFIG_FILE.exists():
        config = {
            "created": datetime.now().isoformat(),
            "youtube_channel": "@FarFromWeakFFW",
            "upload_settings": {
                "auto_open_browser": True,
                "batch_upload": True,
                "default_privacy": "public",
                "add_to_playlist": "Motivation Shorts"
            },
            "video_categories": {
                "motivation": "People & Blogs",
                "comedy": "Entertainment", 
                "education": "Education"
            },
            "hashtags": {
                "motivation": "#motivation #success #mindset #grind #alpha",
                "comedy": "#comedy #funny #humor #satire #lincoln",
                "education": "#education #history #facts #learning"
            }
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        print("✅ YouTube upload config created!")
    return True

def get_videos_for_upload():
    """Get all videos ready for YouTube upload"""
    video_files = []
    
    # Check youtube_ready directory
    if UPLOAD_DIR.exists():
        for file in UPLOAD_DIR.glob("*.mp4"):
            video_files.append({
                'path': file,
                'name': file.name,
                'size_mb': file.stat().st_size / (1024 * 1024),
                'created': datetime.fromtimestamp(file.stat().st_ctime)
            })
    
    # Also check root directory for any MP4 files
    for file in BASE_DIR.glob("*.mp4"):
        if file.stat().st_size > 10 * 1024 * 1024:  # Only files > 10MB
            video_files.append({
                'path': file,
                'name': file.name,
                'size_mb': file.stat().st_size / (1024 * 1024),
                'created': datetime.fromtimestamp(file.stat().st_ctime)
            })
    
    return sorted(video_files, key=lambda x: x['created'], reverse=True)

def generate_video_title(filename):
    """Generate YouTube title from filename"""
    name = Path(filename).stem
    
    # Remove timestamps and prefixes
    clean_name = name.replace('YT_', '').replace('SHORT_', '').replace('LINCOLN_', '').replace('ABRAHAM_', '')
    
    # Extract timestamp and remove it
    import re
    clean_name = re.sub(r'_\\d{8}_\\d{6}', '', clean_name)
    clean_name = re.sub(r'_\\d+$', '', clean_name)  # Remove trailing numbers
    
    # Convert to title case
    clean_name = clean_name.replace('_', ' ').title()
    
    return clean_name

def generate_video_description(title, category="motivation"):
    """Generate YouTube description"""
    config = load_config()
    hashtags = config['hashtags'].get(category, "#motivation #success")
    
    description = f'''
{title}

🔥 Daily Motivation & Mindset Training
💪 Become Unstoppable
🎯 Achieve Your Goals

{hashtags}

Subscribe for daily content that will change your life!

🔔 Turn on notifications so you never miss a video!

#FarFromWeak #Motivation #Success #Mindset #Alpha #Grind
'''
    return description.strip()

def load_config():
    """Load YouTube upload config"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return create_upload_config() or {}

def open_youtube_upload_page():
    """Open YouTube upload page in browser"""
    print("🌐 Opening YouTube upload page...")
    
    upload_url = "https://www.youtube.com/upload"
    
    # Try different methods to open browser
    try:
        import webbrowser
        webbrowser.open(upload_url)
        return True
    except:
        pass
    
    try:
        os.system(f"start {upload_url}")
        return True
    except:
        pass
    
    try:
        subprocess.Popen(["xdg-open", upload_url])
        return True
    except:
        pass
    
    print("❌ Could not open browser automatically")
    print(f"💡 Please manually visit: {upload_url}")
    return False

def create_upload_batch_file(videos):
    """Create batch file for easy upload"""
    batch_content = "@echo off\necho 🚀 YOUTUBE UPLOAD BATCH - FARFROMWEAK STYLE 🚀\necho ==========================================\n\n"
    
    for i, video in enumerate(videos, 1):
        title = generate_video_title(video['name'])
        batch_content += f"echo {i}. {title} - {video['size_mb']:.1f}MB\n"
    
    batch_content += f'''
echo.
echo 📁 Upload these {len(videos)} videos to YouTube:
echo   1. Go to: https://www.youtube.com/upload
echo   2. Drag and drop all MP4 files from:
echo      {UPLOAD_DIR}
echo   3. Use the titles and descriptions shown above
echo   4. Set as YouTube Shorts (vertical videos)
echo   5. Add to playlist: "Motivation Shorts"
echo.
echo 🎯 TIPS FOR VIRAL SUCCESS:
echo    - Upload 3-5 shorts per day
echo    - Use consistent hashtags  
echo    - Engage with comments
echo    - Cross-promote on other platforms
echo.
pause
'''
    
    batch_file = BASE_DIR / "YOUTUBE_UPLOAD_GUIDE.bat"
    with open(batch_file, 'w') as f:
        f.write(batch_content)
    
    return batch_file

def show_upload_dashboard():
    """Show upload dashboard with all videos"""
    videos = get_videos_for_upload()
    
    print("\\n📊 YOUTUBE UPLOAD DASHBOARD")
    print("=" * 70)
    print(f"📍 Channel: @FarFromWeakFFW")
    print(f"📁 Videos Ready: {len(videos)}")
    print(f"💾 Total Size: {sum(v['size_mb'] for v in videos):.1f} MB")
    print("=" * 70)
    
    if not videos:
        print("❌ No videos found for upload!")
        print("💡 Generate some videos first using the other scripts")
        return
    
    for i, video in enumerate(videos, 1):
        title = generate_video_title(video['name'])
        print(f"{i}. {title}")
        print(f"   📏 Size: {video['size_mb']:.1f}MB")
        print(f"   📅 Created: {video['created'].strftime('%Y-%m-%d %H:%M')}")
        print(f"   📍 Location: {video['path']}")
        print()
    
    # Create upload batch file
    batch_file = create_upload_batch_file(videos)
    print(f"📄 Upload guide created: {batch_file.name}")
    
    return videos

def copy_to_desktop():
    """Copy launcher to desktop for easy access"""
    try:
        # Copy this script to desktop
        current_script = Path(__file__)
        desktop_launcher = DESKTOP_DIR / "YouTube_Upload_Launcher.bat"
        
        batch_content = f'''@echo off
cd /d "{BASE_DIR}"
echo 🚀 YOUTUBE UPLOAD LAUNCHER - FARFROMWEAK STYLE 🚀
echo ================================================
python "{current_script.name}"
pause
'''
        with open(desktop_launcher, 'w') as f:
            f.write(batch_content)
        
        print(f"✅ Desktop launcher created: {desktop_launcher}")
        return True
    except Exception as e:
        print(f"❌ Could not create desktop launcher: {e}")
        return False

def main():
    """Main upload automation function"""
    print("🎯 YouTube Upload Automation System")
    print("=" * 50)
    
    # Create config
    create_upload_config()
    
    # Show dashboard
    videos = show_upload_dashboard()
    
    if videos:
        print("🚀 UPLOAD ACTIONS:")
        print("1. Open YouTube upload page")
        print("2. Show upload instructions") 
        print("3. Create desktop launcher")
        print("4. Exit")
        
        try:
            choice = input("\\nSelect action (1-4): ").strip()
            
            if choice == "1":
                open_youtube_upload_page()
                print("✅ Browser opened! Start uploading your videos!")
                
            elif choice == "2":
                print("\\n📋 UPLOAD INSTRUCTIONS:")
                print("1. Go to: https://www.youtube.com/upload")
                print("2. Upload ALL MP4 files from the 'youtube_ready' folder")
                print("3. For each video:")
                print("   - Use the suggested title")
                print("   - Add motivational description") 
                print("   - Use hashtags: #motivation #success #mindset #grind")
                print("   - Set as YouTube Shorts")
                print("4. Upload 3-5 videos per day for best results")
                
            elif choice == "3":
                if copy_to_desktop():
                    print("✅ Desktop launcher created!")
                    print("💡 You can now run this from your desktop anytime!")
                else:
                    print("❌ Failed to create desktop launcher")
                    
            elif choice == "4":
                print("👋 Goodbye! Come back after uploading!")
                
            else:
                print("❌ Invalid choice")
                
        except KeyboardInterrupt:
            print("\\n👋 Upload process cancelled")
            
    else:
        print("\\n💡 TIPS TO GET STARTED:")
        print("1. Run the YouTube Shorts generator first")
        print("2. Or use existing MP4 files in this folder")
        print("3. Make sure videos are 1080x1920 (vertical)")
        print("4. Videos should be 30-60 seconds for Shorts")

if __name__ == "__main__":
    main()
