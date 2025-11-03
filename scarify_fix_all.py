import os
import subprocess
from gtts import gTTS

print(' SCARIFY COMPLETE FIX')
print('======================')

def generate_new_audio():
    audio_dir = r'F:\AI_Oracle_Root\scarify\output\audio\new'
    os.makedirs(audio_dir, exist_ok=True)
    
    texts = [
        'I broke the matrix. Now making 15k per month from my garage. Stop being their pawn.',
        'Ancient wisdom meets AI power. Unlock your mystic potential. Transform your reality.',
        'From zero to hero. The blueprint they don\\'t want you to see. Your time is now.',
        'Escape the nine to five trap. Build your empire. The system is broken, be the fix.',
        'Your breakthrough moment starts here. No more excuses. Claim your power.',
        'The revolution begins with you. Stop waiting, start building. Your empire awaits.'
    ]
    
    audio_files = []
    for i, text in enumerate(texts, 1):
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            filename = f'new_audio_{i}.mp3'
            filepath = os.path.join(audio_dir, filename)
            tts.save(filepath)
            
            if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
                print(f' Generated: {filename} ({os.path.getsize(filepath)} bytes)')
                audio_files.append(filepath)
            else:
                print(f' Failed: {filename}')
        except Exception as e:
            print(f' TTS error: {e}')
    
    return audio_files

def create_video(audio_path, text, output_name):
    try:
        output_dir = r'F:\AI_Oracle_Root\scarify\output\videos\fixed'
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, output_name)
        
        cmd = f'ffmpeg -y -f lavfi -i \"color=color=#FF6B6B:size=1080x1920:duration=10\" -i \"{audio_path}\" -vf \"drawtext=text=\\'{text[:50]}\\':fontcolor=white:fontsize=48:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=(h-text_h)/2\" -c:v libx264 -c:a aac -shortest \"{output_path}\"'
        
        print(f' Creating: {output_name}')
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f' Created: {output_path}')
            return output_path
        else:
            print(f' FFmpeg failed')
            return None
            
    except Exception as e:
        print(f' Video creation failed: {e}')
        return None

print(' Step 1: Generating new audio files...')
audio_files = generate_new_audio()

if audio_files:
    print(f'\\n Step 2: Creating videos with new audio...')
    texts = [
        'I broke the matrix',
        'Ancient wisdom AI', 
        'From zero to hero',
        'Escape the 9-5',
        'Breakthrough moment',
        'Revolution begins'
    ]
    
    created_videos = []
    for i, (audio_path, text) in enumerate(zip(audio_files, texts), 1):
        output_name = f'fixed_video_{i}.mp4'
        video_path = create_video(audio_path, text, output_name)
        if video_path:
            created_videos.append(video_path)
    
    print(f'\\n COMPLETE FIX SUCCESS!')
    print(f' Generated {len(audio_files)} new audio files')
    print(f' Created {len(created_videos)} new videos')
else:
    print(' Audio generation failed')
