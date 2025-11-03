import os
import requests
import base64
from datetime import datetime

print('🚀 SCARIFY SIMPLIFIED DEPLOYMENT')
print('================================')

def generate_video_cartesia(prompt):
    api_key = 'sk_car_pDuPjnKD6FdmmDMYXYqhzr'
    
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': api_key
    }
    
    payload = {
        'model_id': 'cartesia-1.0',
        'prompt': prompt,
        'video': {
            'resolution': {'width': 1280, 'height': 720},
            'duration': 8,
            'fps': 30
        }
    }
    
    try:
        print('🎬 Generating video with Cartesia...')
        response = requests.post(
            'https://api.cartesia.ai/video/generate',
            headers=headers,
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            video_filename = f'F:\\AI_Oracle_Root\\scarify\\output\\videos\\cartesia_{timestamp}.mp4'
            os.makedirs(os.path.dirname(video_filename), exist_ok=True)
            
            with open(video_filename, 'wb') as f:
                f.write(response.content)
            
            file_size = os.path.getsize(video_filename)
            print(f'✅ REAL VIDEO: {video_filename}')
            print(f'📊 Size: {file_size:,} bytes')
            return video_filename
        else:
            print(f'❌ Cartesia error: {response.status_code}')
            print(f'🔧 Response: {response.text}')
            return None
            
    except Exception as e:
        print(f'❌ Video generation failed: {e}')
        return None

def main():
    archetype = 'Mystic'
    
    print(f'🎯 Generating {archetype} video...')
    
    prompts = {
        'Rebel': 'Cinematic urban exploration, gritty aesthetic, dynamic camera movements, revolutionary themes, dark and dramatic lighting, symbolic imagery of freedom and rebellion',
        'Mystic': 'Ethereal landscapes, floating islands, cosmic phenomena, magical realism, soft glowing lighting, surreal dreamlike sequences, mystical atmosphere, consciousness themes',
        'Sage': 'Ancient wisdom themes, library aesthetics, knowledge symbols, serene landscapes, contemplative cinematic shots, intellectual atmosphere, timeless principles'
    }
    
    video_prompt = prompts.get(archetype, prompts['Mystic'])
    print(f'🎨 Prompt: {video_prompt}')
    
    video_file = generate_video_cartesia(video_prompt)
    
    if video_file:
        print(f'\n🎉 DEPLOYMENT SUCCESS!')
        print(f'✅ Video: {os.path.basename(video_file)}')
        print(f'🚀 Real AI video generated with Cartesia!')
        
        video_size = os.path.getsize(video_file)
        print(f'📊 Video file: {video_size:,} bytes')
        print(f'📍 Location: {video_file}')
    else:
        print('❌ Video generation failed')

if __name__ == '__main__':
    main()
