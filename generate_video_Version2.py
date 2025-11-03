# ELEVENLABS ROAR + MOVIEPY VISUAL GUT-PUNCH
import os
import sys
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
from moviepy.video.fx.all import crop, resize
from moviepy.video.tools.subtitles import SubtitlesClip
import random

def generate_video(script_path="output/scripts/rebel_script.txt", audio_path="output/audio/rebel_audio.mp3", output_path="output/videos/rebel_short.mp4", broll_dir="assets/b-roll"):
    audio = AudioFileClip(audio_path)
    duration = audio.duration
    if not os.path.exists(broll_dir):
        raise ValueError("B-roll dir missing—grab 5 free MP4s from Pexels, warlord")
    broll_files = [f for f in os.listdir(broll_dir) if f.endswith('.mp4')]
    if not broll_files:
        raise ValueError("No B-roll MP4s—stock your arsenal")
    broll_path = os.path.join(broll_dir, random.choice(broll_files))
    video = VideoFileClip(broll_path).subclip(0, min(duration, 10))

    # Vertical crop for Shorts (9:16)
    video = crop(video, x1=video.w/4, y1=0, x2=video.w*3/4, y2=video.h).resize(height=1920).resize(width=1080)

    # Timed captions from script (split lines, sync to audio segments)
    with open(script_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    subtitles = []
    for i, line in enumerate(lines):
        txt_clip = TextClip(line, fontsize=50, color='white', font='Arial-Bold', stroke_color='black', stroke_width=2)
        start_time = i * (duration / len(lines))
        end_time = start_time + (duration / len(lines))
        subtitles.append((txt_clip.set_position(('center', 'bottom')).set_start(start_time).set_end(end_time), None))
    sub_clip = SubtitlesClip(subtitles, lambda txt: TextClip(txt, font='Arial-Bold', fontsize=50, color='white'))
    final_video = CompositeVideoClip([video.set_audio(audio), sub_clip.set_duration(duration)])

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final_video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)
    final_video.close()
    audio.close()
    video.close()
    print(f"🔥 VIDEO FORGED: {output_path} – {duration}s of Rebel napalm, ready for YouTube flood")
    return output_path

if __name__ == "__main__":
    script_path = sys.argv[1] if len(sys.argv) > 1 else "output/scripts/rebel_script.txt"
    audio_path = sys.argv[2] if len(sys.argv) > 2 else "output/audio/rebel_audio.mp3"
    output_path = sys.argv[3] if len(sys.argv) > 3 else "output/videos/rebel_short.mp4"
    generate_video(script_path, audio_path, output_path)