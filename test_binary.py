#!/usr/bin/env python3
"""
SCARIFY RunwayML Video Generator - Production Ready
Generates 45-60 second vertical videos for YouTube Shorts with audio overlay.
NO BLACK SCREENS. REAL CINEMATIC CONTENT.
"""

import os
import sys
import json
import time
import requests
from pathlib import Path
from dotenv import load_dotenv
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, ColorClip, TextClip
from moviepy.video.fx import resize

# Load environment
load_dotenv('config/credentials/.env')

class RunwayVideoGenerator:
    """Production-ready RunwayML Gen-3 Alpha Turbo video generator"""
    
    def __init__(self):
        self.api_key = os.getenv('RUNWAYML_API_KEY')
        if not self.api_key:
            raise ValueError(
                "❌ RUNWAYML_API_KEY not found!\n"
                "Get your API key: https://app.runwayml.com/settings/api\n"
                "Add to config/credentials/.env: RUNWAYML_API_KEY=your_key_here"
            )
        
        self.base_url = "https://api.runwayml.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_video_with_prompt(self, prompt, duration=10, style="cinematic"):
        """
        Generate video using RunwayML Gen-3 Alpha Turbo
        
        Args:
            prompt: Visual description for video generation
            duration: Video duration in seconds (5, 10)
            style: Visual style preset
        
        Returns:
            URL to generated video file
        """
        print(f"\n🎬 Generating RunwayML video...")
        print(f"   Prompt: {prompt[:80]}...")
        print(f"   Duration: {duration}s")
        print(f"   Style: {style}")
        
        # Create generation task
        payload = {
            "promptText": f"{style} style: {prompt}",
            "model": "gen3a_turbo",
            "duration": duration,
            "ratio": "9:16",  # Vertical for Shorts
            "watermark": False
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/image_to_video",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"❌ API Error: {response.status_code}")
                print(f"   Response: {response.text}")
                return None
            
            task_data = response.json()
            task_id = task_data.get("id")
            
            if not task_id:
                print(f"❌ No task ID returned: {task_data}")
                return None
            
            print(f"✅ Task created: {task_id}")
            print("⏳ Waiting for video generation...")
            
            # Poll for completion (RunwayML takes 60-180 seconds)
            max_attempts = 60  # 10 minutes max
            attempt = 0
            
            while attempt < max_attempts:
                time.sleep(10)  # Check every 10 seconds
                attempt += 1
                
                status_response = requests.get(
                    f"{self.base_url}/tasks/{task_id}",
                    headers=self.headers,
                    timeout=30
                )
                
                if status_response.status_code != 200:
                    print(f"⚠️  Status check failed: {status_response.status_code}")
                    continue
                
                status_data = status_response.json()
                status = status_data.get("status", "UNKNOWN")
                
                print(f"   [{attempt}/60] Status: {status}")
                
                if status == "SUCCEEDED":
                    video_url = status_data.get("output", {}).get("url")
                    if video_url:
                        print(f"✅ Video generated successfully!")
                        return video_url
                    else:
                        print(f"❌ No video URL in response: {status_data}")
                        return None
                
                elif status == "FAILED":
                    error = status_data.get("failure", "Unknown error")
                    print(f"❌ Generation failed: {error}")
                    return None
            
            print(f"⏱️ Timeout: Video generation took too long")
            return None
            
        except requests.exceptions.Timeout:
            print("⏱️ Request timeout - RunwayML may be overloaded")
            return None
        except Exception as e:
            print(f"❌ Error during generation: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def download_video(self, video_url, output_path):
        """Download generated video from RunwayML"""
        print(f"\n⬇️  Downloading video...")
        
        try:
            response = requests.get(video_url, stream=True, timeout=60)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"\r   Progress: {percent:.1f}%", end='', flush=True)
            
            print(f"\n✅ Downloaded: {output_path}")
            print(f"   Size: {os.path.getsize(output_path) / 1024 / 1024:.2f} MB")
            return True
            
        except Exception as e:
            print(f"\n❌ Download failed: {str(e)}")
            return False
    
    def create_multi_scene_video(self, script_text, target_duration=50):
        """
        Create 45-60 second video by generating multiple scenes
        
        Args:
            script_text: Full script/story text
            target_duration: Target video length (45-60 seconds optimal)
        
        Returns:
            List of video file paths
        """
        print(f"\n📝 Analyzing script for scene generation...")
        print(f"   Target duration: {target_duration}s")
        
        # Split script into scenes (aim for 10-second segments)
        scenes = self._extract_scenes_from_script(script_text, target_duration)
        
        print(f"✅ Extracted {len(scenes)} scenes")
        
        video_clips = []
        
        for i, scene in enumerate(scenes, 1):
            print(f"\n🎬 Scene {i}/{len(scenes)}")
            print(f"   {scene['prompt'][:60]}...")
            
            video_url = self.generate_video_with_prompt(
                prompt=scene['prompt'],
                duration=scene['duration'],
                style=scene.get('style', 'cinematic horror')
            )
            
            if video_url:
                temp_path = f"temp_scene_{i}.mp4"
                if self.download_video(video_url, temp_path):
                    video_clips.append(temp_path)
                else:
                    print(f"⚠️  Scene {i} download failed, skipping")
            else:
                print(f"⚠️  Scene {i} generation failed, skipping")
        
        return video_clips
    
    def _extract_scenes_from_script(self, script_text, target_duration):
        """Extract visual prompts from script text"""
        
        # For now, create 4-6 scenes of 10 seconds each
        num_scenes = min(6, max(4, target_duration // 10))
        scene_duration = 10
        
        # Split script into chunks
        words = script_text.split()
        words_per_scene = len(words) // num_scenes
        
        scenes = []
        
        for i in range(num_scenes):
            start_idx = i * words_per_scene
            end_idx = (i + 1) * words_per_scene if i < num_scenes - 1 else len(words)
            scene_text = ' '.join(words[start_idx:end_idx])
            
            # Extract key visual elements
            prompt = self._create_visual_prompt(scene_text, i, num_scenes)
            
            scenes.append({
                'prompt': prompt,
                'duration': scene_duration,
                'style': 'cinematic horror' if 'horror' in script_text.lower() else 'cinematic'
            })
        
        return scenes
    
    def _create_visual_prompt(self, text, scene_num, total_scenes):
        """Create visual prompt from script text"""
        
        # Visual progression templates
        progression = [
            "establishing shot, wide angle, atmospheric",
            "medium shot, detailed environment, building tension",
            "close-up, emotional intensity, dramatic lighting",
            "dynamic movement, action sequence, urgent pacing",
            "revealing shot, plot twist, shock value",
            "climactic moment, peak intensity, visual spectacle"
        ]
        
        template = progression[min(scene_num, len(progression) - 1)]
        
        # Extract key nouns/concepts from text
        keywords = [word for word in text.lower().split() 
                   if len(word) > 5 and word.isalpha()][:3]
        
        context = ' '.join(keywords) if keywords else "dramatic scene"
        
        return f"{template}, {context}, cinematic quality, high production value"
    
    def overlay_audio(self, video_path, audio_path, output_path):
        """
        Overlay audio on video with proper sync and duration matching
        
        Args:
            video_path: Path to video file
            audio_path: Path to audio file
            output_path: Output path for final video
        """
        print(f"\n🔊 Overlaying audio...")
        
        try:
            video = VideoFileClip(video_path)
            audio = AudioFileClip(audio_path)
            
            # Ensure video matches audio duration
            if video.duration < audio.duration:
                print(f"⚠️  Video ({video.duration}s) shorter than audio ({audio.duration}s)")
                print(f"   Looping video to match audio duration")
                
                # Loop video to match audio
                loops_needed = int(audio.duration / video.duration) + 1
                video = video.loop(n=loops_needed)
            
            # Trim to exact audio duration
            video = video.subclip(0, audio.duration)
            
            # Set audio
            final_video = video.set_audio(audio)
            
            # Write with high quality settings
            print(f"💾 Writing final video...")
            final_video.write_videofile(
                output_path,
                fps=30,
                codec='libx264',
                audio_codec='aac',
                bitrate='5000k',
                audio_bitrate='192k',
                preset='medium',
                threads=4
            )
            
            # Cleanup
            video.close()
            audio.close()
            final_video.close()
            
            duration = os.popen(f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{output_path}"').read().strip()
            
            print(f"\n✅ Final video created!")
            print(f"   Output: {output_path}")
            print(f"   Duration: {float(duration):.1f}s")
            print(f"   Size: {os.path.getsize(output_path) / 1024 / 1024:.2f} MB")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Audio overlay failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def stitch_scenes(self, video_clips, output_path):
        """Combine multiple video clips into single video"""
        
        print(f"\n✂️  Stitching {len(video_clips)} scenes together...")
        
        if not video_clips:
            print("❌ No video clips to stitch")
            return False
        
        try:
            # Load all clips
            clips = [VideoFileClip(clip) for clip in video_clips]
            
            # Ensure all clips are same resolution (1080x1920)
            clips = [resize.resize(clip, height=1920) for clip in clips]
            
            # Concatenate
            from moviepy.editor import concatenate_videoclips
            final_clip = concatenate_videoclips(clips, method="compose")
            
            # Write
            print(f"💾 Writing stitched video...")
            final_clip.write_videofile(
                output_path,
                fps=30,
                codec='libx264',
                preset='medium',
                threads=4
            )
            
            # Cleanup
            for clip in clips:
                clip.close()
            final_clip.close()
            
            print(f"✅ Scenes stitched: {output_path}")
            
            # Clean up temp files
            for temp_file in video_clips:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            
            return True
            
        except Exception as e:
            print(f"❌ Stitching failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return False


def generate_complete_video(script_path, audio_path, output_path, target_duration=50):
    """
    Main function: Generate complete 45-60 second video with audio
    
    Args:
        script_path: Path to script text file
        audio_path: Path to audio narration file
        output_path: Output video path
        target_duration: Target video length (45-60 optimal)
    """
    
    print("=" * 70)
    print("🔥 SCARIFY RUNWAYML VIDEO GENERATOR - PRODUCTION MODE")
    print("=" * 70)
    print(f"Script: {script_path}")
    print(f"Audio: {audio_path}")
    print(f"Output: {output_path}")
    print(f"Target: {target_duration}s (YouTube Shorts optimized)")
    print("=" * 70)
    
    # Validate inputs
    if not os.path.exists(script_path):
        print(f"❌ Script not found: {script_path}")
        return False
    
    if not os.path.exists(audio_path):
        print(f"❌ Audio not found: {audio_path}")
        return False
    
    # Read script
    with open(script_path, 'r', encoding='utf-8') as f:
        script_text = f.read()
    
    print(f"\n📝 Script loaded: {len(script_text)} characters")
    
    # Initialize generator
    try:
        generator = RunwayVideoGenerator()
    except ValueError as e:
        print(f"\n{e}")
        return False
    
    # Generate multi-scene video
    temp_stitched = "temp_stitched_video.mp4"
    video_clips = generator.create_multi_scene_video(script_text, target_duration)
    
    if not video_clips:
        print("\n❌ No video clips generated")
        return False
    
    # Stitch scenes
    if not generator.stitch_scenes(video_clips, temp_stitched):
        return False
    
    # Overlay audio
    if not generator.overlay_audio(temp_stitched, audio_path, output_path):
        if os.path.exists(temp_stitched):
            os.remove(temp_stitched)
        return False
    
    # Cleanup
    if os.path.exists(temp_stitched):
        os.remove(temp_stitched)
    
    # Final validation
    if os.path.exists(output_path):
        size_mb = os.path.getsize(output_path) / 1024 / 1024
        
        print("\n" + "=" * 70)
        print("🎉 VIDEO GENERATION COMPLETE!")
        print("=" * 70)
        print(f"✅ Output: {output_path}")
        print(f"✅ Size: {size_mb:.2f} MB")
        print(f"✅ Ready for YouTube Shorts upload!")
        print("=" * 70)
        
        return True
    else:
        print("\n❌ Final video file not created")
        return False


if __name__ == "__main__":
    # Command line interface
    if len(sys.argv) < 4:
        print("Usage: python generate_video_runway.py <script.txt> <audio.mp3> <output.mp4> [target_duration]")
        print("\nExample:")
        print("  python generate_video_runway.py output/scripts/rebel_script.txt output/audio/rebel_audio.mp3 output/videos/rebel_short.mp4 55")
        sys.exit(1)
    
    script_path = sys.argv[1]
    audio_path = sys.argv[2]
    output_path = sys.argv[3]
    target_duration = int(sys.argv[4]) if len(sys.argv) > 4 else 50
    
    # Ensure target is 45-60 seconds
    if target_duration < 45:
        print(f"⚠️  Duration {target_duration}s too short, setting to 45s")
        target_duration = 45
    elif target_duration > 60:
        print(f"⚠️  Duration {target_duration}s too long, setting to 60s")
        target_duration = 60
    
    success = generate_complete_video(script_path, audio_path, output_path, target_duration)
    sys.exit(0 if success else 1)
