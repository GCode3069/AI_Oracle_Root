import requests
import base64
from datetime import datetime

def test_cartesia():
    api_key = 'sk_car_pDuPjnKD6FdmmDMYXYqhzr'
    
    print('🧪 TESTING CARTESIA API...')
    
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': api_key
    }
    
    payload = {
        'model_id': 'cartesia-1.0',
        'prompt': 'A beautiful mystical landscape with floating islands and glowing orbs, cinematic quality',
        'video': {
            'resolution': {'width': 1280, 'height': 720},
            'duration': 3,
            'fps': 30
        }
    }
    
    try:
        print('📤 Sending request to Cartesia...')
        response = requests.post(
            'https://api.cartesia.ai/video/generate',
            headers=headers,
            json=payload,
            timeout=60
        )
        
        print(f'📥 Status: {response.status_code}')
        
        if response.status_code == 200:
            timestamp = datetime.now().strftime('%H%M%S')
            filename = f'cartesia_test_{timestamp}.mp4'
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f'✅ SUCCESS: {filename}')
            print(f'📊 Size: {len(response.content):,} bytes')
            return True
        else:
            print(f'❌ Failed: {response.status_code}')
            print(f'Details: {response.text}')
            return False
            
    except Exception as e:
        print(f'❌ Error: {e}')
        return False

if __name__ == '__main__':
    test_cartesia()
