import requests
import json
from pathlib import Path

print("🧪 Testing API Key Fix...")

config_path = Path(r'F:\AI_Oracle_Root\scarify\config\api_config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

raw_api_key = config['keys']['ELEVENLABS_API_KEY']
clean_api_key = raw_api_key.strip()

print(f"Raw API key: '{raw_api_key}'")
print(f"Clean API key: '{clean_api_key}'")
print(f"Length raw: {len(raw_api_key)}")
print(f"Length clean: {len(clean_api_key)}")

# Test with clean key
response = requests.get(
    'https://api.elevenlabs.io/v1/voices',
    headers={'xi-api-key': clean_api_key}
)

print(f"Status: {response.status_code}")

if response.status_code == 200:
    voices = response.json()['voices']
    print(f"✅ SUCCESS! Connected with clean key. Found {len(voices)} voices")
else:
    print(f"❌ Still failing: {response.text}")
