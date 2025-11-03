import os
import subprocess
import time

def create_video_with_ffmpeg(audio_path, output_path, text):
    """Create video using FFmpeg directly - no Python dependencies"""
    
    # Create a simple image with text using PIL if available, else use fallback
    try:
        from PIL import Image, ImageDraw, ImageFont
        # Create background image
        img = Image.new('RGB', (1080, 1920), color=(20, 20, 40))
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()
        
        # Add text
        lines = text.split('. ')
        y = 400
        for line in lines[:3]:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (1080 - text_width) // 2
            draw.text((x, y), line, fill=(255, 255, 255), font=font)
            y += 100
        
        # Add CTA
        cta = "trenchaikits.com/buy-rebel-$97"
        bbox = draw.textbbox((0, 0), cta, font=font)
        text_width = bbox[2] - bbox[0]
        x = (1080 - text_width) // 2
        draw.text((x, 1720), cta, fill=(255, 215, 0), font=font)
        
        img.save("temp_background.jpg")
        image_path = "temp_background.jpg"
        
    except Exception as e:
        print(f"❌ Image creation failed: {e}")
        # Use a solid color background
        image_path = "none"
    
    try:
        # Get audio duration
        import wave
        with wave.open(audio_path, 'rb') as audio_file:
            frames = audio_file.getnframes()
            rate = audio_file.getframerate()
            duration = frames / float(rate)
        
        # Create video using FFmpeg
        if image_path != "none" and os.path.exists(image_path):
            cmd = [
                'ffmpeg', '-y',
                '-loop', '1',
                '-i', image_path,
                '-i', audio_path,
                '-c:v', 'libx264',
                '-t', str(duration),
                '-pix_fmt', 'yuv420p',
                '-c:a', 'aac',
                '-shortest',
                output_path
            ]
        else:
            # Create color background
            cmd = [
                'ffmpeg', '-y',
                '-f', 'lavfi',
                '-i', f'color=c=0x141428:s=1080x1920:d={duration}',
                '-i', audio_path,
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-shortest',
                output_path
            ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            return True
        else:
            print(f"FFmpeg error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ FFmpeg video creation failed: {e}")
        return False

# Process audio files
audio_files = [f for f in os.listdir('output/audio') if f.endswith('.mp3')]
texts = [
    "I broke the matrix. Now making 15k/month from my garage. Stop being their pawn.",
    "Ancient wisdom meets AI power. Unlock your mystic potential. Transform your reality.",
    "From zero to hero. The blueprint they don't want you to see. Your time is now.",
    "Escape the 9-5 trap. Build your empire. The system is broken, be the fix.",
    "Your breakthrough moment starts here. No more excuses. Claim your power.",
    "The revolution begins with you. Stop waiting, start building. Your empire awaits."
]

print("🎬 EMERGENCY VIDEO GENERATION WITH FFMPEG...")

success_count = 0
for i, audio_file in enumerate(audio_files):
    if i >= len(texts):
        break
        
    audio_path = f"output/audio/{audio_file}"
    output_path = f"output/videos/emergency_{audio_file.replace('.mp3', '.mp4')}"
    
    if create_video_with_ffmpeg(audio_path, output_path, texts[i]):
        success_count += 1
        print(f"✅ CREATED: {output_path}")
    else:
        print(f"❌ FAILED: {audio_file}")

print(f"\n🎯 EMERGENCY GENERATION: {success_count}/{len(audio_files)} videos")
