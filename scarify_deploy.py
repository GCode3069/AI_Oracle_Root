import os
import requests
import base64
from datetime import datetime

print('🚀 SCARIFY WORKING DEPLOYMENT')
print('=============================')

def generate_audio_free(script_text):
    try:
        from gtts import gTTS
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        audio_filename = f'F:\\AI_Oracle_Root\\scarify\\output\\audio\\tts_{timestamp}.mp3'
        os.makedirs(os.path.dirname(audio_filename), exist_ok=True)
        
        tts = gTTS(text=script_text, lang='en', slow=False)
        tts.save(audio_filename)
        
        if os.path.exists(audio_filename):
            size = os.path.getsize(audio_filename)
            print(f'✅ FREE AUDIO: {audio_filename}')
            return audio_filename
    except Exception as e:
        print(f'❌ TTS failed: {e}')
    
    return None

def generate_video_cartesia(prompt, audio_file=None):
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
            'duration': 6,
            'fps': 30
        }
    }
    
    if audio_file and os.path.exists(audio_file):
        try:
            with open(audio_file, 'rb') as f:
                audio_data = base64.b64encode(f.read()).decode('utf-8')
            
            payload['audio'] = {
                'data': audio_data,
                'format': 'mp3'
            }
            payload['voice'] = {
                'mode': 'id', 
                'id': '4e6f3d62-5f2f-4b62-97d0-5e6c6f6e4b3d'
            }
        except Exception as e:
            print(f'⚠️  Could not add audio: {e}')
    
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

def create_content(archetype='Mystic'):
    content = {
        'Rebel': 'Breaking free from conventional thinking. Revolutionary ideas that challenge the status quo and inspire real change in the world.',
        'Mystic': 'Exploring consciousness beyond physical reality. Journey into mystical dimensions and spiritual awakening through ancient wisdom.',
        'Sage': 'Wisdom in the information age. Cutting through noise to find timeless truths and practical insights for modern life.'
    }
    return content.get(archetype, content['Mystic'])

def get_video_prompt(archetype):
    prompts = {
        'Rebel': 'Cinematic urban exploration, gritty aesthetic, dynamic camera movements, revolutionary themes, dark and dramatic lighting, symbolic imagery of freedom',
        'Mystic': 'Ethereal landscapes, floating islands, cosmic phenomena, magical realism, soft glowing lighting, surreal dreamlike sequences, mystical atmosphere',
        'Sage': 'Ancient wisdom themes, library aesthetics, knowledge symbols, serene landscapes, contemplative cinematic shots, intellectual atmosphere'
    }
    return prompts.get(archetype, 'Cinematic, artistic footage with beautiful lighting and dynamic camera movements')

def main():
    archetype = 'Mystic'
    
    print(f'🎯 Generating {archetype} content...')
    
    script = create_content(archetype)
    print(f'📝 Script: {len(script)} characters')
    
    print('\n🎵 Generating audio...')
    audio_file = generate_audio_free(script)
    
    if audio_file:
        print('\n🎬 Generating video...')
        video_prompt = get_video_prompt(archetype)
        print(f'🎨 Prompt: {video_prompt}')
        
        video_file = generate_video_cartesia(video_prompt, audio_file)
        
        if video_file:
            print(f'\n🎉 DEPLOYMENT SUCCESS!')
            print(f'✅ Audio: {os.path.basename(audio_file)}')
            print(f'✅ Video: {os.path.basename(video_file)}')
            print(f'🚀 Real AI video generated with Cartesia!')
        else:
            print('\n❌ Video generation failed')
    else:
        print('❌ Audio generation failed')

if __name__ == '__main__':
    main()
