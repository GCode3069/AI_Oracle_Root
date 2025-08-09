"""
Video Engine for Oracle Horror
FFmpeg-based video rendering with horror effects and multi-format support
"""

import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json
import tempfile
import shutil

try:
    import cv2
    import numpy as np
    from PIL import Image
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("⚠️ OpenCV not available - using basic video generation")

from effects_library import EffectsLibrary

class VideoEngine:
    def __init__(self):
        self.effects = EffectsLibrary()
        self.ffmpeg_path = self._find_ffmpeg()
        
        # Video format specifications
        self.format_specs = {
            "shorts": {
                "resolution": (1080, 1920),
                "aspect_ratio": "9:16",
                "fps": 30,
                "bitrate": "2M",
                "codec": "libx264"
            },
            "full": {
                "resolution": (1920, 1080),
                "aspect_ratio": "16:9", 
                "fps": 30,
                "bitrate": "4M",
                "codec": "libx264"
            },
            "viral_series": {
                "resolution": (1080, 1080),
                "aspect_ratio": "1:1",
                "fps": 30,
                "bitrate": "3M",
                "codec": "libx264"
            }
        }
    
    def _find_ffmpeg(self) -> Optional[str]:
        """Find FFmpeg executable"""
        # Try common locations
        possible_paths = [
            "ffmpeg",  # In PATH
            "/usr/bin/ffmpeg",
            "/usr/local/bin/ffmpeg",
            "C:\\ffmpeg\\bin\\ffmpeg.exe",
            "C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe"
        ]
        
        for path in possible_paths:
            try:
                result = subprocess.run([path, "-version"], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"✅ FFmpeg found: {path}")
                    return path
            except (FileNotFoundError, subprocess.TimeoutExpired):
                continue
        
        print("⚠️ FFmpeg not found - attempting to install...")
        return self._install_ffmpeg()
    
    def _install_ffmpeg(self) -> Optional[str]:
        """Attempt to install FFmpeg"""
        try:
            # Try installing via package manager
            if os.name == 'posix':  # Linux/Mac
                subprocess.run(["sudo", "apt-get", "update"], check=False)
                result = subprocess.run(["sudo", "apt-get", "install", "-y", "ffmpeg"], 
                                      check=False, capture_output=True)
                if result.returncode == 0:
                    return "ffmpeg"
            
            print("❌ Could not install FFmpeg automatically")
            print("📝 Please install FFmpeg manually:")
            print("   Ubuntu/Debian: sudo apt-get install ffmpeg")
            print("   Windows: Download from https://ffmpeg.org/download.html")
            return None
            
        except Exception as e:
            print(f"❌ FFmpeg installation failed: {e}")
            return None
    
    def test_ffmpeg(self) -> bool:
        """Test FFmpeg availability"""
        if not self.ffmpeg_path:
            print("❌ FFmpeg not available")
            return False
        
        try:
            result = subprocess.run([self.ffmpeg_path, "-version"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("✅ FFmpeg is working correctly")
                return True
            else:
                print("❌ FFmpeg test failed")
                return False
        except Exception as e:
            print(f"❌ FFmpeg test error: {e}")
            return False
    
    def render_horror_video(self, manifest: Dict, audio_file: str, 
                          format_type: str, output_dir: str) -> str:
        """Render complete horror video with effects"""
        
        if format_type not in self.format_specs:
            raise ValueError(f"Unknown format: {format_type}")
        
        specs = self.format_specs[format_type]
        output_dir_path = Path(output_dir)
        output_dir_path.mkdir(parents=True, exist_ok=True)
        
        # Generate output filename
        video_id = manifest.get("id", "oracle_horror_video")
        output_file = output_dir_path / f"{video_id}.mp4"
        
        print(f"🎥 Rendering {format_type} video: {specs['resolution'][0]}x{specs['resolution'][1]}")
        
        try:
            if CV2_AVAILABLE and self.ffmpeg_path:
                return self._render_with_opencv(manifest, audio_file, specs, str(output_file))
            else:
                return self._render_basic_video(manifest, audio_file, specs, str(output_file))
        
        except Exception as e:
            print(f"❌ Video rendering failed: {e}")
            # Create placeholder file as fallback
            self._create_placeholder_video(str(output_file), specs)
            return str(output_file)
    
    def _render_with_opencv(self, manifest: Dict, audio_file: str, 
                          specs: Dict, output_file: str) -> str:
        """Render video using OpenCV and FFmpeg"""
        
        width, height = specs["resolution"]
        fps = specs["fps"]
        duration = manifest["metadata"]["duration"]
        
        # Create temporary directory for frames
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            frames_dir = temp_path / "frames"
            frames_dir.mkdir()
            
            print("🖼️ Generating video frames...")
            frame_count = int(fps * duration)
            
            # Generate frames with horror effects
            for frame_idx in range(frame_count):
                frame_file = frames_dir / f"frame_{frame_idx:06d}.png"
                self._generate_horror_frame(
                    manifest, frame_idx, frame_count, 
                    (width, height), str(frame_file)
                )
                
                if frame_idx % (fps * 2) == 0:  # Progress every 2 seconds
                    print(f"   Generated {frame_idx}/{frame_count} frames...")
            
            print("🎬 Combining frames with audio...")
            # Use FFmpeg to combine frames and audio
            video_without_audio = temp_path / "video_no_audio.mp4"
            final_video = output_file
            
            # Create video from frames
            ffmpeg_cmd1 = [
                self.ffmpeg_path,
                "-framerate", str(fps),
                "-i", str(frames_dir / "frame_%06d.png"),
                "-c:v", specs["codec"],
                "-pix_fmt", "yuv420p",
                "-b:v", specs["bitrate"],
                "-y",  # Overwrite output file
                str(video_without_audio)
            ]
            
            result = subprocess.run(ffmpeg_cmd1, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Frame combination failed: {result.stderr}")
                raise Exception("Frame combination failed")
            
            # Add audio to video
            ffmpeg_cmd2 = [
                self.ffmpeg_path,
                "-i", str(video_without_audio),
                "-i", audio_file,
                "-c:v", "copy",
                "-c:a", "aac",
                "-shortest",  # Use shortest input duration
                "-y",  # Overwrite output file
                str(final_video)
            ]
            
            result = subprocess.run(ffmpeg_cmd2, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Audio combination failed: {result.stderr}")
                # Copy video without audio as fallback
                shutil.copy2(video_without_audio, final_video)
            
            print(f"✅ Video rendered successfully: {output_file}")
            return output_file
    
    def _generate_horror_frame(self, manifest: Dict, frame_idx: int, 
                             total_frames: int, size: Tuple[int, int], 
                             output_file: str) -> None:
        """Generate a single horror video frame"""
        
        width, height = size
        progress = frame_idx / total_frames
        
        # Get theme and effects from manifest
        theme = manifest["theme"]
        effects_list = manifest["effects"]
        script = manifest["script"]
        
        # Generate base background
        color_scheme = theme["color_scheme"]
        background = self.effects.generate_background(size, color_scheme)
        
        # Apply visual effects based on manifest
        for effect in effects_list:
            effect_type = effect.get("type", "")
            
            if effect_type == "matrix_rain":
                intensity = effect.get("intensity", "medium")
                background = self.effects.add_matrix_rain(background, intensity)
            
            elif effect_type == "screen_glitch":
                frequency = effect.get("frequency", "medium")
                # Apply glitch intermittently
                if frame_idx % 30 < 5:  # Glitch for 5 frames every 30
                    background = self.effects.add_screen_glitch(background, frequency)
            
            elif effect_type == "neon_overlay":
                pattern = effect.get("pattern", "circuit")
                background = self.effects.add_neon_overlay(background, pattern)
            
            elif effect_type == "vhs_corruption":
                intensity = effect.get("intensity", "medium")
                if frame_idx % 60 < 10:  # Corruption for 10 frames every 60
                    background = self.effects.add_vhs_corruption(background, intensity)
        
        # Add text overlay with typewriter effect
        if progress < 0.8:  # Show text for most of the video
            # Calculate how much text to show (typewriter effect)
            chars_to_show = int(len(script) * min(1.0, progress * 1.5))
            visible_text = script[:chars_to_show]
            
            if visible_text:
                text_style = manifest["visual"]["text_style"]
                style_name = "glitch_neon"
                if color_scheme == "blood_red":
                    style_name = "blood_red"
                elif color_scheme == "cyber_blue":
                    style_name = "cyber_blue"
                
                background = self.effects.add_horror_text(background, visible_text, style_name)
        
        # Save frame
        background.save(output_file, "PNG")
    
    def _render_basic_video(self, manifest: Dict, audio_file: str, 
                          specs: Dict, output_file: str) -> str:
        """Basic video rendering without OpenCV"""
        
        print("📢 Using basic video generation (OpenCV not available)")
        
        width, height = specs["resolution"]
        duration = manifest["metadata"]["duration"]
        
        # Create a single frame and repeat it
        background = self.effects.generate_background((width, height), 
                                                    manifest["theme"]["color_scheme"])
        
        # Add some effects
        background = self.effects.add_matrix_rain(background, "medium")
        background = self.effects.add_horror_text(background, manifest["script"], "glitch_neon")
        
        # Save frame
        temp_frame = Path(output_file).parent / "temp_frame.png"
        background.save(temp_frame, "PNG")
        
        if self.ffmpeg_path:
            # Use FFmpeg to create video from single frame
            ffmpeg_cmd = [
                self.ffmpeg_path,
                "-loop", "1",
                "-i", str(temp_frame),
                "-i", audio_file,
                "-c:v", specs["codec"],
                "-t", str(duration),
                "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-b:v", specs["bitrate"],
                "-shortest",
                "-y",
                output_file
            ]
            
            result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
            
            # Clean up temp frame
            temp_frame.unlink(missing_ok=True)
            
            if result.returncode == 0:
                print(f"✅ Basic video created: {output_file}")
                return output_file
            else:
                print(f"❌ FFmpeg error: {result.stderr}")
        
        # Fallback: create placeholder
        return self._create_placeholder_video(output_file, specs)
    
    def _create_placeholder_video(self, output_file: str, specs: Dict) -> str:
        """Create a placeholder video file when rendering fails"""
        
        print("📝 Creating placeholder video file...")
        
        # Create a text file with video information
        placeholder_info = {
            "type": "Oracle Horror Video Placeholder",
            "resolution": f"{specs['resolution'][0]}x{specs['resolution'][1]}",
            "format": specs["aspect_ratio"],
            "fps": specs["fps"],
            "codec": specs["codec"],
            "bitrate": specs["bitrate"],
            "note": "This is a placeholder. Real MP4 generation requires FFmpeg and OpenCV.",
            "install_instructions": {
                "ffmpeg": "Install FFmpeg from https://ffmpeg.org/",
                "opencv": "pip install opencv-python",
                "dependencies": "pip install -r requirements.txt"
            }
        }
        
        # Save as JSON with .mp4 extension to indicate intended format
        with open(output_file.replace('.mp4', '_placeholder.json'), 'w') as f:
            json.dump(placeholder_info, f, indent=2)
        
        # Also create empty .mp4 file
        Path(output_file).touch()
        
        print(f"📁 Placeholder created: {output_file}")
        return output_file
    
    def create_thumbnail(self, video_file: str) -> str:
        """Create thumbnail for the video"""
        
        video_path = Path(video_file)
        thumbnail_path = video_path.with_suffix('.jpg')
        
        if self.ffmpeg_path and video_path.exists() and video_path.stat().st_size > 0:
            # Extract thumbnail from video
            ffmpeg_cmd = [
                self.ffmpeg_path,
                "-i", str(video_file),
                "-ss", "00:00:01",  # Take frame at 1 second
                "-vframes", "1",
                "-y",
                str(thumbnail_path)
            ]
            
            result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"🖼️ Thumbnail created: {thumbnail_path}")
                return str(thumbnail_path)
        
        # Fallback: create thumbnail using effects library
        try:
            thumbnail = self.effects.generate_background((320, 180), "dark_neon")
            thumbnail = self.effects.add_horror_text(thumbnail, "Oracle Horror", "glitch_neon")
            thumbnail.save(thumbnail_path, "JPEG", quality=85)
            print(f"🖼️ Fallback thumbnail created: {thumbnail_path}")
            return str(thumbnail_path)
        
        except Exception as e:
            print(f"❌ Thumbnail creation failed: {e}")
            return ""
    
    def get_video_info(self, video_file: str) -> Dict:
        """Get video file information"""
        
        if not Path(video_file).exists():
            return {"error": "Video file not found"}
        
        if not self.ffmpeg_path:
            return {"error": "FFmpeg not available for analysis"}
        
        try:
            # Use ffprobe to get video information
            ffprobe_cmd = [
                self.ffmpeg_path.replace('ffmpeg', 'ffprobe'),
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "-show_streams",
                video_file
            ]
            
            result = subprocess.run(ffprobe_cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                info = json.loads(result.stdout)
                return {
                    "duration": float(info.get("format", {}).get("duration", 0)),
                    "size": int(info.get("format", {}).get("size", 0)),
                    "bitrate": int(info.get("format", {}).get("bit_rate", 0)),
                    "streams": len(info.get("streams", []))
                }
            else:
                return {"error": f"ffprobe failed: {result.stderr}"}
        
        except Exception as e:
            return {"error": f"Analysis failed: {e}"}
    
    def optimize_for_platform(self, video_file: str, platform: str) -> str:
        """Optimize video for specific platforms"""
        
        if not self.ffmpeg_path:
            print("⚠️ Cannot optimize - FFmpeg not available")
            return video_file
        
        platform_specs = {
            "youtube": {
                "codec": "libx264",
                "profile": "high",
                "preset": "slow",
                "crf": "18"
            },
            "tiktok": {
                "codec": "libx264", 
                "profile": "baseline",
                "preset": "fast",
                "crf": "23"
            },
            "instagram": {
                "codec": "libx264",
                "profile": "main",
                "preset": "medium", 
                "crf": "20"
            }
        }
        
        if platform not in platform_specs:
            print(f"⚠️ Unknown platform: {platform}")
            return video_file
        
        input_path = Path(video_file)
        output_path = input_path.parent / f"{input_path.stem}_{platform}{input_path.suffix}"
        
        specs = platform_specs[platform]
        
        ffmpeg_cmd = [
            self.ffmpeg_path,
            "-i", str(video_file),
            "-c:v", specs["codec"],
            "-profile:v", specs["profile"],
            "-preset", specs["preset"],
            "-crf", specs["crf"],
            "-c:a", "aac",
            "-y",
            str(output_path)
        ]
        
        print(f"🔄 Optimizing for {platform}...")
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Optimized for {platform}: {output_path}")
            return str(output_path)
        else:
            print(f"❌ Optimization failed: {result.stderr}")
            return video_file