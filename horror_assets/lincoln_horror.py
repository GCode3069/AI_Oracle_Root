import os
import sys
import json
import requests
import random
from pathlib import Path
from datetime import datetime

# REAL PATHS
BASE_DIR = Path(r"F:\AI_Oracle_Root\scarify")
CONFIG_FILE = BASE_DIR / "config" / "api_config.json"

class LincolnHorrorGenerator:
    def __init__(self):
        self.fear_themes = [
            "corrupt government officials", "ICE raids spreading fear", "cyber-terrorism attacks",
            "economic collapse", "government shutdown", "Bitcoin fear", "foreclosure crisis",
            "Gmail hacks", "antifa fearmongering", "weapons 2025"
        ]
        
        self.lincoln_templates = [
            "The people's trust rots like my flesh. {theme} Sic semper tyrannis always thus to tyrants. This purge begins now.",
            "My derringer still speaks through your fear of {theme}. The corruption spreads like infection. Join me in the blood-soaked box.",
            "{theme} another wound in democracy's corpse. I rise from the grave to cleanse this rot. Sic semper join the purge or join the bleed."
        ]
    
    def generate_script(self):
        theme = random.choice(self.fear_themes)
        template = random.choice(self.lincoln_templates)
        script = template.format(theme=theme)
        
        return {
            "theme": f"lincoln horror - {theme}",
            "script": script,
            "word_count": len(script.split())
        }

def generate_voice_elevenlabs(text, output_path):
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        
        api_key = config['keys']['ELEVENLABS_API_KEY']
        
        # Get available voices
        voices_url = "https://api.elevenlabs.io/v1/voices"
        headers = {"xi-api-key": api_key}
        
        response = requests.get(voices_url, headers=headers)
        if response.status_code != 200:
            print(f"❌ ElevenLabs error: {response.status_code}")
            return False
        
        voices = response.json()['voices']
        if not voices:
            print("❌ No voices found")
            return False
        
        # Find a deep voice for Lincoln
        voice_id = None
        for voice in voices:
            if any(keyword in voice['name'].lower() for keyword in ['deep', 'grave', 'authoritative']):
                voice_id = voice['voice_id']
                voice_name = voice['name']
                print(f"🎙️ Using voice: {voice_name}")
                break
        
        # Fallback to first voice
        if not voice_id:
            voice_id = voices[0]['voice_id']
            voice_name = voices[0]['name']
            print(f"🎙️ Using fallback voice: {voice_name}")
        
        # Generate speech
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json", 
            "xi-api-key": api_key
        }
        
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.3,
                "similarity_boost": 0.7,
                "style": 0.8,
                "use_speaker_boost": True
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"✅ Voice generated: {output_path}")
            return True
        else:
            print(f"❌ Voice generation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Voice generation error: {e}")
        return False

def generate_lincoln_horror():
    print("🩸 LINCOLN HORROR GENERATION ACTIVATED")
    print("=" * 60)
    
    # Create directories
    audio_dir = BASE_DIR / "audio"
    audio_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Step 1: Generate Lincoln horror script
    print("📝 Generating Lincoln horror script...")
    generator = LincolnHorrorGenerator()
    script_data = generator.generate_script()
    
    print(f"   Theme: {script_data['theme']}")
    print(f"   Script: {script_data['script']}")
    
    # Step 2: Generate Lincoln-style voice
    audio_file = audio_dir / f"lincoln_horror_{timestamp}.mp3"
    print("🎙️ Generating Lincoln's voice...")
    
    if not generate_voice_elevenlabs(script_data['script'], audio_file):
        print("❌ Voice generation failed")
        return None
    
    print("=" * 60)
    print("✅ LINCOLN HORROR AUDIO COMPLETE!")
    print(f"📁 Audio file: {audio_file}")
    print("💰 You can use this audio with any video editor")
    print("=" * 60)
    
    return {
        'audio_file': str(audio_file),
        'script_data': script_data
    }

if __name__ == "__main__":
    result = generate_lincoln_horror()
    if result:
        print("\n🎉 SUCCESS! Your Lincoln horror audio is ready!")
    else:
        print("\n💥 Generation failed. Check errors above.")
