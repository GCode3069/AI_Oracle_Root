import os
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_playable_video(audio_path, output_path, text_content):
    """Create actual playable MP4 videos with audio and visuals"""
    
    # Create a simple background image
    width, height = 1080, 1920  # Vertical for Shorts
    background = Image.new('RGB', (width, height), color=(20, 20, 40))  # Dark blue
    draw = ImageDraw.Draw(background)
    
    try:
        # Try to use a system font
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Add text to image
    text_lines = text_content.split('. ')
    y_position = 400
    for line in text_lines[:3]:  # First 3 lines
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x_position = (width - text_width) // 2
        draw.text((x_position, y_position), line, fill=(255, 255, 255), font=font)
        y_position += 100
    
    # Add CTA at bottom
    cta_text = "trenchaikits.com/buy-rebel-$97"
    bbox = draw.textbbox((0, 0), cta_text, font=font)
    text_width = bbox[2] - bbox[0]
    x_position = (width - text_width) // 2
    draw.text((x_position, height - 200), cta_text, fill=(255, 215, 0), font=font)
    
    # Convert PIL image to numpy array for moviepy
    background_np = np.array(background)
    
    try:
        # Load audio file
        audio_clip = AudioFileClip(audio_path)
        
        # Create video clip with duration matching audio
        video_clip = ImageClip(background_np, duration=audio_clip.duration)
        video_clip = video_clip.set_audio(audio_clip)
        video_clip.fps = 24
        
        # Write video file
        video_clip.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None
        )
        
        return True
        
    except Exception as e:
        print(f"❌ Video creation failed: {e}")
        return False

# Process all audio files
audio_files = [
    "output/audio/Rebel_narration_20251020_230050.mp3",
    "output/audio/Mystic_narration_20251020_225409.mp3", 
    "output/audio/test_audio_20251020_201103.mp3",
    "output/audio/test_audio_20251020_201054.mp3",
    "output/audio/first_upload_test.mp3",
    "output/audio/test_narration_20251020_194413.mp3"
]

video_texts = [
    "I broke the matrix. Now making 15k/month from my garage. Stop being their pawn.",
    "Ancient wisdom meets AI power. Unlock your mystic potential. Transform your reality.",
    "From zero to hero. The blueprint they don't want you to see. Your time is now.",
    "Escape the 9-5 trap. Build your empire. The system is broken, be the fix.",
    "Your breakthrough moment starts here. No more excuses. Claim your power.",
    "The revolution begins with you. Stop waiting, start building. Your empire awaits."
]

print("🎬 GENERATING REAL, PLAYABLE VIDEOS...")

success_count = 0
for i, audio_file in enumerate(audio_files):
    if os.path.exists(audio_file):
        output_file = f"output/videos/playable_{os.path.basename(audio_file).replace('.mp3', '.mp4')}"
        text_content = video_texts[i % len(video_texts)]
        
        if create_playable_video(audio_file, output_file, text_content):
            success_count += 1
            print(f"✅ CREATED: {output_file}")
        else:
            print(f"❌ FAILED: {audio_file}")
    else:
        print(f"❌ MISSING: {audio_file}")

print(f"\n🎯 VIDEO GENERATION COMPLETE: {success_count}/{len(audio_files)} successful")
