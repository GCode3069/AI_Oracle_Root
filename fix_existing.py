"""
FIX EXISTING VIDEOS
Regenerates audio for all existing videos with:
- Male voice (not female)
- No stage directions
Run: python fix_existing.py
"""
import os, sys, subprocess, requests, re
from pathlib import Path

ELEVENLABS_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")

def get_male_voice():
    """Get deep male voice"""
    try:
        r = requests.get("https://api.elevenlabs.io/v1/voices", 
                        headers={"xi-api-key": ELEVENLABS_KEY}, timeout=10)
        if r.status_code == 200:
            for voice in r.json()['voices']:
                if any(w in voice['name'].lower() for w in ['adam', 'arnold', 'sam']):
                    print(f"Using voice: {voice['name']}")
                    return voice['voice_id']
    except: pass
    return "pNInz6obpgDQGcFmaJgB"  # Adam fallback

def extract_text_from_audio(video_file):
    """Extract original script from video metadata or filename"""
    # For now, return placeholder - you'd need to transcribe
    # or store original scripts somewhere
    return None

def clean_script(text):
    """Remove stage directions from script"""
    # Remove anything in *[brackets]*
    text = re.sub(r'\*\[.*?\]\*', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def regenerate_audio(script, output_path):
    """Generate new audio with male voice"""
    voice_id = get_male_voice()
    
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}", 
                     json={
                         "text": script,
                         "model_id": "eleven_multilingual_v2", 
                         "voice_settings": {
                             "stability": 0.4,
                             "similarity_boost": 0.9,
                             "style": 0.8,
                             "use_speaker_boost": True
                         }
                     }, 
                     headers={"xi-api-key": ELEVENLABS_KEY}, 
                     timeout=240)
    
    if r.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(r.content)
        return True
    return False

def replace_audio_in_video(video_file, new_audio_file, output_file):
    """Replace audio in existing video"""
    subprocess.run([
        "ffmpeg", "-i", str(video_file), "-i", str(new_audio_file),
        "-c:v", "copy", "-map", "0:v:0", "-map", "1:a:0",
        "-shortest", "-y", str(output_file)
    ], capture_output=True)
    return output_file.exists()

def fix_videos():
    print("\n🔧 FIXING EXISTING VIDEOS\n")
    
    video_dir = BASE / "uploaded"
    if not video_dir.exists():
        print("❌ No uploaded videos found")
        return
    
    videos = list(video_dir.glob("*.mp4"))
    print(f"Found {len(videos)} videos to fix\n")
    
    fixed_count = 0
    for video in videos:
        print(f"Processing: {video.name}")
        
        # You'll need to either:
        # 1. Have the original scripts saved somewhere
        # 2. Use speech-to-text to extract current audio
        # 3. Manually provide scripts
        
        # For now, this is placeholder logic
        print("  ⚠️  Need original script to regenerate")
        print("  💡 Best solution: Generate new videos with abe_FIXED.py")
    
    print(f"\n{'='*70}")
    print("RECOMMENDATION:")
    print("Rather than fix 70+ videos, generate NEW ones with:")
    print("  python abe_FIXED.py 100")
    print("Then upload those to replace the old ones")
    print("{'='*70}\n")

if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════╗
║  FIX EXISTING VIDEOS - OPTIONS                                ║
╠═══════════════════════════════════════════════════════════════╣
║  OPTION 1 (RECOMMENDED):                                      ║
║    Generate NEW correct videos                                ║
║    python abe_FIXED.py 100                                    ║
║                                                               ║
║  OPTION 2 (MANUAL):                                           ║
║    Delete old videos from YouTube                             ║
║    Upload new ones                                            ║
║                                                               ║
║  OPTION 3 (IF YOU HAVE SCRIPTS):                              ║
║    Save all original scripts to text files                    ║
║    Run this script to regenerate audio                        ║
║    Replace audio in videos                                    ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    choice = input("\nPress Enter to see analysis of existing videos...")
    fix_videos()
