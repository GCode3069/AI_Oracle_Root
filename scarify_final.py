import os
import subprocess

print("🚀 SCARIFY AUTOMATED VIDEO GENERATION")
print("=====================================")

def create_video(audio_file, text, output_name):
    try:
        audio_dir = r"F:\AI_Oracle_Root\scarify\output\audio"
        output_dir = r"F:\AI_Oracle_Root\scarify\output\videos\auto"
        os.makedirs(output_dir, exist_ok=True)
        
        audio_path = os.path.join(audio_dir, audio_file)
        output_path = os.path.join(output_dir, output_name)
        
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", "color=color=#FF6B6B:size=1080x1920:duration=15",
            "-i", audio_path,
            "-vf", f"drawtext=text='{text}':fontcolor=white:fontsize=48:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=(h-text_h)/2",
            "-c:v", "libx264",
            "-c:a", "aac",
            "-shortest",
            output_path
        ]
        
        print(f"🎬 Creating: {output_name}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Created: {output_path}")
            return output_path
        else:
            print(f"❌ FFmpeg failed")
            return None
            
    except Exception as e:
        print(f"❌ Video creation failed: {e}")
        return None

assignments = [
    {"audio": "test_narration_20251020_194413.mp3", "text": "I broke the matrix"},
    {"audio": "first_upload_test.mp3", "text": "Ancient wisdom meets AI"},
    {"audio": "test_audio_20251020_201054.mp3", "text": "From zero to hero"},
    {"audio": "test_audio_20251020_201103.mp3", "text": "Escape the 9-5 trap"},
    {"audio": "Mystic_narration_20251020_225409.mp3", "text": "Your breakthrough moment"},
    {"audio": "Rebel_narration_20251020_230050.mp3", "text": "The revolution begins"}
]

created_videos = []
for i, assignment in enumerate(assignments, 1):
    output_name = f"auto_video_{i}.mp4"
    video_path = create_video(assignment["audio"], assignment["text"], output_name)
    if video_path:
        created_videos.append(video_path)

print(f"\n🎉 AUTOMATION COMPLETE!")
print(f"✅ Generated {len(created_videos)} videos programmatically")
for video in created_videos:
    print(f"   🎬 {os.path.basename(video)}")
