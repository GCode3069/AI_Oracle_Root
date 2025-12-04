# KLING_CLIENT.py
import requests
import time
from API_KEYS import KLING_API_KEY

def generate_talking_head(audio_path, image_path):
    """Generate lip-sync video with Kling AI"""
    print(f"🗣️ Generating lip-sync with Kling AI...")
    
    # Upload files
    with open(audio_path, 'rb') as af, open(image_path, 'rb') as imf:
        files = {'audio': af, 'image': imf}
        headers = {'Authorization': f'Bearer {KLING_API_KEY}'}
        
        # Start generation
        response = requests.post(
            'https://api.klingai.com/v1/videos/generations',
            headers=headers,
            files=files,
            data={'duration': 'auto'}
        )
        
        if response.status_code != 200:
            raise Exception(f"Kling API error: {response.text}")
        
        task_id = response.json()['task_id']
        print(f"   Task ID: {task_id}")
    
    # Poll for completion
    for i in range(60):
        time.sleep(10)
        check_response = requests.get(
            f'https://api.klingai.com/v1/videos/generations/{task_id}',
            headers=headers
        )
        
        status = check_response.json()['status']
        print(f"   Status: {status} ({i*10}s elapsed)")
        
        if status == 'completed':
            video_url = check_response.json()['video_url']
            
            # Download video
            video_data = requests.get(video_url).content
            output_path = audio_path.replace('.mp3', '_lipsync.mp4')
            
            with open(output_path, 'wb') as f:
                f.write(video_data)
            
            print(f"✅ Lip-sync complete: {output_path}")
            return output_path
        
        elif status == 'failed':
            raise Exception(f"Kling generation failed")
    
    raise Exception("Kling timeout after 600 seconds")
