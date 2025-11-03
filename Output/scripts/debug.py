import os,sys,json,time,requests
from dotenv import load_dotenv

load_dotenv('F:/AI_Oracle_Root/scarify/config/credentials/.env')
k=os.getenv('RUNWAYML_API_KEY')

if not k:
    print('❌ No API key found')
    sys.exit(1)

print(f'✅ Key loaded: {k[:20]}...')

u='https://api.dev.runwayml.com/v1'
h={'Authorization':f'Bearer {k}','X-Runway-Version':'2024-09-13','Content-Type':'application/json'}

# Test API connection first
print('\n🔍 Testing API connection...')
try:
    test = requests.get(f'{u}/tasks', headers=h, timeout=10)
    print(f'   Status: {test.status_code}')
    print(f'   Response: {test.text[:200]}')
except Exception as e:
    print(f'   ❌ Connection failed: {e}')
    sys.exit(1)

# Try creating ONE task with full error logging
print('\n🎬 Creating test task...')
payload = {
    'taskType': 'gen3a_turbo',
    'internal': False,
    'options': {
        'name': 'Test',
        'seconds': 10,
        'text_prompt': 'Cinematic horror abandoned factory dark atmospheric',
        'watermark': False,
        'enhance_prompt': True,
        'resolution': '720p',
        'gen3a_turbo:aspect_ratio': '9:16'
    }
}

try:
    r = requests.post(f'{u}/tasks', headers=h, json=payload, timeout=30)
    print(f'   Status: {r.status_code}')
    print(f'   Response: {r.text[:500]}')
    
    if r.status_code in [200, 201]:
        task_id = r.json().get('id')
        print(f'   ✅ Task created: {task_id}')
    else:
        print(f'   ❌ Task creation failed')
        print(f'   Full response: {r.text}')
        
except Exception as e:
    print(f'   ❌ Request failed: {e}')
    import traceback
    traceback.print_exc()
