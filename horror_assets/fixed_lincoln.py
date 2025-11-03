import requests
import json
import random
from pathlib import Path
from datetime import datetime

print("🚀 Starting Lincoln Horror Generator...")

# Paths
BASE_DIR = Path(r"F:\AI_Oracle_Root\scarify")
CONFIG_FILE = BASE_DIR / "config" / "api_config.json"

# Load config
try:
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    
    # FIX: Strip whitespace from API key
    raw_api_key = config['keys']['ELEVENLABS_API_KEY']
    api_key = raw_api_key.strip()  # Remove leading/trailing whitespace
    
    print(f"✅ Raw API key: '{raw_api_key}'")
    print(f"✅ Clean API key: '{api_key}'")
    print(f"✅ Loaded API key: {api_key[:8]}...")
    
except Exception as e:
    print(f"❌ Failed to load config: {e}")
    exit(1)

# Lincoln horror script
scripts = [
    "The people's trust rots like my flesh. Corrupt government officials spread fear. Sic semper tyrannis. This purge begins now.",
    "My derringer still speaks through your fear of cyber-terrorism attacks. The corruption spreads like infection. Join me in the blood-soaked box.",
    "Economic collapse, another wound in democracy's corpse. I rise from the grave to cleanse this rot. Sic semper, join the purge or join the bleed."
]

chosen_script = random.choice(scripts)
print(f"📝 Script: {chosen_script}")

# Get voices
try:
    response = requests.get(
        'https://api.elevenlabs.io/v1/voices',
        headers={'xi-api-key': api_key}  # Use cleaned API key
    )
    
    if response.status_code == 200:
        voices = response.json()['voices']
        voice_id = voices[0]['voice_id']
        print(f"🎙️ Using voice: {voices[0]['name']}")
        
        # Generate audio
        url = f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}'
        headers = {
            'Accept': 'audio/mpeg',
            'Content-Type': 'application/json',
            'xi-api-key': api_key  # Use cleaned API key
        }
        
        data = {
            'text': chosen_script,
            'model_id': 'eleven_monolingual_v1',
            'voice_settings': {
                'stability': 0.3,
                'similarity_boost': 0.7
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            # Save file
            audio_dir = BASE_DIR / "audio"
            audio_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = audio_dir / f"lincoln_horror_{timestamp}.mp3"
            
            with open(output_file, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ SUCCESS! Audio saved: {output_file}")
        else:
            print(f"❌ Voice generation failed: {response.status_code}")
            print(f"Response: {response.text}")
    else:
        print(f"❌ Failed to get voices: {response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")
