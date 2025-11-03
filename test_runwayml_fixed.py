import requests
import json
from pathlib import Path

def test_runwayml():
    try:
        # Read your RunwayML key
        api_key = Path("config/credentials/runwayml_api.key").read_text().strip()
        
        # Remove BOM if present (ï»¿)
        if api_key.startswith('ï»¿'):
            api_key = api_key[3:]
        api_key = api_key.strip()
        
        print(f"Testing with key: {api_key[:15]}...")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # CORRECT RunwayML API endpoints:
        # Option 1: Check account balance/status (usually works)
        url = "https://api.runwayml.com/v1/account"
        
        # Option 2: Try the models endpoint with correct path
        # url = "https://api.runwayml.com/v1/models"
        
        print(f"Testing endpoint: {url}")
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            print("✅ RUNWAYML API CONNECTED SUCCESSFULLY!")
            data = response.json()
            print(f"🎬 Account/Model data: {json.dumps(data, indent=2)[:200]}...")
            return True
        else:
            print(f"❌ RunwayML API Error: {response.status_code}")
            print(f"   Headers: {dict(response.headers)}")
            print(f"   Response: {response.text[:500]}...")
            
            # Try alternative endpoints
            print("\n🔄 Trying alternative endpoints...")
            
            endpoints = [
                "https://api.runwayml.com/v1/user",
                "https://api.runwayml.com/v1/balance",
                "https://api.runwayml.com/v1/credits"
            ]
            
            for endpoint in endpoints:
                print(f"   Testing: {endpoint}")
                resp = requests.get(endpoint, headers=headers)
                if resp.status_code == 200:
                    print(f"   ✅ Works: {endpoint}")
                    print(f"   Data: {resp.json()}")
                    return True
                else:
                    print(f"   ❌ {endpoint}: {resp.status_code}")
            
            return False
            
    except Exception as e:
        print(f"❌ RunwayML test failed: {e}")
        import traceback
        print(f"   Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    test_runwayml()
