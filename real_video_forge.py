import os
import random
import glob
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
from moviepy.video.fx.all import resize, crop

class RealVideoForge:
    def __init__(self):
        self.broll_dir = "assets/b-roll/"
        self.ensure_assets()
    
    def ensure_assets(self):
        os.makedirs(self.broll_dir, exist_ok=True)
        if not glob.glob(os.path.join(self.broll_dir, "*.mp4")):
            self.create_sample_broll()
    
    def create_sample_broll(self):
        from moviepy.video.VideoClip import ColorClip
        colors = [(30,30,60), (60,30,30), (30,60,30), (60,60,30), (30,60,60)]
        
        for i, color in enumerate(colors, 1):
            clip = ColorClip(size=(1080, 1920), color=color, duration=20)
            output_path = os.path.join(self.broll_dir, f"broll_{i}.mp4")
            clip.write_videofile(output_path, fps=24, verbose=False, logger=None)
            clip.close()
    
    def create_video(self, script, audio_path, output_path, duration=20):
        broll_files = glob.glob(os.path.join(self.broll_dir, "*.mp4"))
        if not broll_files:
            from moviepy.video.VideoClip import ColorClip
            video_clip = ColorClip(size=(1080, 1920), color=(40,40,40), duration=duration)
        else:
            video_clip = VideoFileClip(random.choice(broll_files))
            if video_clip.duration < duration:
                video_clip = video_clip.loop(duration=duration)
            else:
                video_clip = video_clip.subclip(0, duration)
        
        try:
            audio_clip = AudioFileClip(audio_path).subclip(0, duration)
            video_clip = video_clip.set_audio(audio_clip)
        except:
            print("Audio load failed - creating silent video")
        
        words = script.split()
        caption_clips = []
        duration_per_chunk = duration / max(1, len(words) // 5)
        
        for i in range(0, len(words), 5):
            chunk = words[i:i+5]
            caption_text = " ".join(chunk)
            text_clip = TextClip(
                caption_text,
                fontsize=36,
                color="white",
                font="Arial-Bold",
                stroke_color="black",
                stroke_width=2
            ).set_position(("center", 1600)).set_duration(duration_per_chunk).set_start(i//5 * duration_per_chunk)
            caption_clips.append(text_clip)
        
        title = TextClip(
            "TRENCH KIT REBEL",
            fontsize=48,
            color="yellow",
            font="Arial-Bold"
        ).set_position(("center", 200)).set_duration(duration)
        
        final_clip = CompositeVideoClip([video_clip, title] + caption_clips)
        final_clip.write_videofile(output_path, fps=24, verbose=False, logger=None)
        
        video_clip.close()
        final_clip.close()
        for clip in caption_clips:
            clip.close()
