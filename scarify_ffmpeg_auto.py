import os
import subprocess
from datetime import datetime

print('🚀 SCARIFY FFMPEG AUTOMATION')
print('============================')

class FFmpegAutoVideo:
    def __init__(self):
        self.output_dir = r'F:\AI_Oracle_Root\scarify\output\videos\auto'
        self.audio_dir = r'F:\AI_Oracle_Root\scarify\output\audio'
        os.makedirs(self.output_dir, exist_ok=True)
    
    def create_video_with_ffmpeg(self, audio_file, text, output_name):
        try:
            audio_path = os.path.join(self.audio_dir, audio_file)
            output_path = os.path.join(self.output_dir, output_name)
            
            # FFmpeg command to create video with text overlay
            cmd = [
                'ffmpeg',
                '-y',
                '-f', 'lavfi',
                '-i', 'color=color=#FF6B6B:size=1080x1920:duration=15',
                '-i', audio_path,
                '-vf', f'drawtext=text=\"{text}\":fontcolor=white:fontsize=48:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=(h-text_h)/2',
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-shortest',
                output_path
            ]
            
            print(f'🎬 Creating: {output_name}')
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            
            if result.returncode == 0:
                print(f'✅ Created: {output_path}')
                return output_path
            else:
                print(f'❌ FFmpeg failed')
                return None
                
        except Exception as e:
            print(f'❌ Video creation failed: {e}')
            return None
    
    def batch_create_videos(self):
        assignments = [
            {'audio': 'test_narration_20251020_194413.mp3', 'text': 'I broke the matrix. Now making 15k/month from my garage'},
            {'audio': 'first_upload_test.mp3', 'text': 'Ancient wisdom meets AI power. Unlock your mystic potential'},
            {'audio': 'test_audio_20251020_201054.mp3', 'text': 'From zero to hero. The blueprint they don\\'t want you to see'},
            {'audio': 'test_audio_20251020_201103.mp3', 'text': 'Escape the 9-5 trap. Build your empire'},
            {'audio': 'Mystic_narration_20251020_225409.mp3', 'text': 'Your breakthrough moment starts here'},
            {'audio': 'Rebel_narration_20251020_230050.mp3', 'text': 'The revolution begins with you'}
        ]
        
        created_videos = []
        
        for i, assignment in enumerate(assignments, 1):
            output_name = f'auto_video_{i}.mp4'
            video_path = self.create_video_with_ffmpeg(
                assignment['audio'],
                assignment['text'],
                output_name
            )
            if video_path:
                created_videos.append(video_path)
        
        return created_videos

automator = FFmpegAutoVideo()
videos = automator.batch_create_videos()

print(f'\\n🎉 AUTOMATION COMPLETE!')
print(f'✅ Generated {len(videos)} videos programmatically')
for video in videos:
    print(f'   🎬 {os.path.basename(video)}')
