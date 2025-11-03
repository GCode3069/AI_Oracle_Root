import requests
import json
from pathlib import Path

def test_runway_generation():
    """Test RunwayML by attempting to start a generation"""
    try:
        api_key = Path("config/credentials/runwayml_api.key").read_text().strip()
        
        # Clean the key
        if api_key.startswith('ï»¿'):
            api_key = api_key[3:]
        api_key = api_key.strip()
        
        print(f"Using key: {api_key[:15]}...")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Try to get available models first
        models_url = "https://api.runwayml.com/v1/models"
        print(f"Getting available models from: {models_url}")
        
        models_response = requests.get(models_url, headers=headers)
        
        if models_response.status_code == 200:
            models = models_response.json()
            print("✅ Successfully retrieved models!")
            print(f"Available models: {len(models)}")
            for model in models[:3]:  # Show first 3 models
                print(f"  - {model.get('name', 'Unknown')} (ID: {model.get('id', 'N/A')})")
            return True
        else:
            print(f"❌ Models endpoint failed: {models_response.status_code}")
            print(f"Response: {models_response.text[:200]}")
            
            # Try a simple generation test
            print("\n🔄 Trying generation endpoint...")
            generate_url = "https://api.runwayml.com/v1/generations"
            
            # Simple test payload
            test_payload = {
                "model": "text-to-video",  # Common model name
                "prompt": "test connection",
                "width": 512,
                "height": 512
            }
            
            gen_response = requests.post(generate_url, headers=headers, json=test_payload)
            print(f"Generation test status: {gen_response.status_code}")
            
            if gen_response.status_code in [200, 201, 202]:
                print("✅ Generation endpoint works!")
                return True
            else:
                print(f"Generation response: {gen_response.text[:200]}")
                return False
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_runway_generation()
