import requests
import json
from pathlib import Path

print("🔑 Testing ElevenLabs API Connection...")

try:
    config_path = Path(r'F:\AI_Oracle_Root\scarify\config\api_config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    api_key = config['keys']['ELEVENLABS_API_KEY']
    print(f"✅ API Key found: {api_key[:8]}...{api_key[-4:]}")
    
    # Test voices endpoint
    response = requests.get(
        'https://api.elevenlabs.io/v1/voices',
        headers={'xi-api-key': api_key}
    )
    
    if response.status_code == 200:
        voices = response.json()['voices']
        print(f"✅ Connected! Found {len(voices)} voices")
        
        # Show first 3 voices
        for i, voice in enumerate(voices[:3]):
            print(f"   {i+1}. {voice['name']} (ID: {voice['voice_id'][:8]}...)")
    else:
        print(f"❌ API Connection failed: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("Make sure your config file exists at: F:\AI_Oracle_Root\scarify\config\api_config.json")
