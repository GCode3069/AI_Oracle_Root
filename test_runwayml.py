import requests
import json
from pathlib import Path

def test_runwayml():
    try:
        # Read your RunwayML key
        api_key = Path("config/credentials/runwayml_api.key").read_text().strip()
        print(f"Testing with key: {api_key[:10]}...")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Test API connection - get user info or models
        url = "https://api.runwayml.com/v1/models"
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            print("✅ RUNWAYML API CONNECTED SUCCESSFULLY!")
            data = response.json()
            print(f"🎬 Available models: {len(data.get('data', []))}")
            
            # Show some available models
            for model in data.get('data', [])[:3]:
                print(f"   - {model.get('name', 'Unknown')} (ID: {model.get('id', 'N/A')})")
            return True
        else:
            print(f"❌ RunwayML API Error: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed - check your API key")
            elif response.status_code == 403:
                print("   Permission denied - check your plan limits")
            else:
                print(f"   Response: {response.text[:100]}...")
            return False
            
    except Exception as e:
        print(f"❌ RunwayML test failed: {e}")
        return False

if __name__ == "__main__":
    test_runwayml()
