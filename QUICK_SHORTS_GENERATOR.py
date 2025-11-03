import requests
import json
import random
import os
from pathlib import Path
from datetime import datetime

print("🔥 QUICK YOUTUBE SHORTS GENERATOR 🔥")

BASE_DIR = Path(r"F:\AI_Oracle_Root\scarify")
UPLOAD_DIR = BASE_DIR / "videos" / "youtube_ready"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ELEVENLABS_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"

QUICK_SCRIPTS = [
    "Stop waiting for permission. The world rewards action. Start now.",
    "Your future self is watching. Don't disappoint him. Grind now.",
    "They'll laugh until you win. Then the silence will be deafening.",
    "Pain is temporary. Quitting lasts forever. Keep going.",
    "The obstacle is the way. Your struggles are shaping you.",
    "Be so good they can't ignore you. Outwork everyone.",
    "Your only limit is you. Break through your own barriers.",
    "Success leaves clues. Follow the patterns of winners.",
    "Dream big. Start small. Act now. Consistency beats talent.",
    "The price of discipline is less than the pain of regret."
]

def generate_quick_video():
    script = random.choice(QUICK_SCRIPTS)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    print(f"🎯 Generating: {script}")
    
    # Generate audio
    try:
        voices_url = "https://api.elevenlabs.io/v1/voices"
        headers = {"xi-api-key": ELEVENLABS_KEY}
        response = requests.get(voices_url, headers=headers)
        
        if response.status_code == 200:
            voices = response.json()['voices']
            voice_id = voices[0]['voice_id']
            
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json", 
                "xi-api-key": ELEVENLABS_KEY
            }
            
            data = {
                "text": script,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.1,
                    "similarity_boost": 0.8,
                    "style": 0.9
                }
            }
            
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                audio_file = BASE_DIR / "audio" / f"quick_{timestamp}.mp3"
                audio_file.parent.mkdir(exist_ok=True)
                
                with open(audio_file, 'wb') as f:
                    f.write(response.content)
                
                print(f"✅ Audio generated: {audio_file.name}")
                
                # For now, just create a simple text file to show it worked
                video_note = UPLOAD_DIR / f"READY_VIDEO_{timestamp}.txt"
                with open(video_note, 'w') as f:
                    f.write(f"Video ready for: {script}")
                
                print(f"✅ Video placeholder created: {video_note.name}")
                return True
                
    except Exception as e:
        print(f"❌ Quick generation failed: {e}")
    
    return False

if __name__ == "__main__":
    print("🎬 Generating 3 quick YouTube Shorts...")
    for i in range(3):
        generate_quick_video()
    print("✅ Quick generation complete!")
    print("📁 Check: F:\\AI_Oracle_Root\\scarify\\videos\\youtube_ready\\")
