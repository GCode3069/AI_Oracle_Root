"""
VIDEO_LAYOUT.py
Create picture-in-picture layouts with VHS effects for SCARIFY videos.
"""

import os
import subprocess
from pathlib import Path
from typing import Optional, Literal


class VideoLayoutCreator:
    """
    Create vertical video layouts with VHS effects.
    
    Output format: 1080x1920 (9:16 vertical for YouTube Shorts)
    """
    
    def __init__(self):
        self.canvas_width = 1080
        self.canvas_height = 1920
        self.video_width = 720
        self.video_height = 1280
    
    def create_pip_layout(
        self,
        video_path: str,
        title: str,
        style: Literal["WARNING", "COMEDY"],
        output_path: Optional[str] = None
    ) -> str:
        """
        Create picture-in-picture layout with title and VHS effects.
        
        Args:
            video_path: Path to talking head video
            title: Video title text
            style: Video style ("WARNING" or "COMEDY")
            output_path: Output path (default: auto-generated)
            
        Returns:
            Path to output video
        """
        if output_path is None:
            base = Path(video_path).stem
            output_path = str(Path(video_path).parent / f"{base}_layout.mp4")
        
        print(f"[LAYOUT] Creating {style} layout...")
        print(f"  Input: {video_path}")
        print(f"  Title: {title}")
        
        # Build FFmpeg filter complex
        filter_complex = self._build_filter_complex(title, style)
        
        # FFmpeg command
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', video_path,
            '-filter_complex', filter_complex,
            '-map', '[output]',
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '23',
            '-pix_fmt', 'yuv420p',
            '-y',
            output_path
        ]
        
        try:
            result = subprocess.run(
                ffmpeg_cmd,
                capture_output=True,
                text=True,
                check=True
            )
            print(f"[LAYOUT] ✅ Layout created: {output_path}")
            return output_path
            
        except subprocess.CalledProcessError as e:
            print(f"[LAYOUT] ❌ FFmpeg error: {e.stderr}")
            raise
        except FileNotFoundError:
            print("[LAYOUT] ❌ FFmpeg not found. Please install FFmpeg.")
            raise
    
    def _build_filter_complex(self, title: str, style: str) -> str:
        """
        Build FFmpeg filter complex for layout and effects.
        
        Layout:
        1. Black canvas (1080x1920)
        2. Scale video to 720x1280
        3. Center video on canvas
        4. Add title overlay
        5. Apply VHS effects
        """
        # Escape title for FFmpeg
        title_escaped = title.replace("'", "'\\''").replace(":", "\\:")
        
        # Choose title style based on format
        if style == "WARNING":
            font_size = 44
            font_color = "white"
            box_color = "black@0.6"
        else:  # COMEDY
            font_size = 42
            font_color = "yellow"
            box_color = "black@0.5"
        
        # Calculate positions
        video_x = (self.canvas_width - self.video_width) // 2  # Center horizontally
        video_y = (self.canvas_height - self.video_height) // 2  # Center vertically
        
        # Build filter chain
        filters = []
        
        # 1. Scale input video
        filters.append(f"[0:v]scale={self.video_width}:{self.video_height}:force_original_aspect_ratio=decrease,pad={self.video_width}:{self.video_height}:(ow-iw)/2:(oh-ih)/2[scaled]")
        
        # 2. Create black canvas and overlay video
        filters.append(f"color=c=black:s={self.canvas_width}x{self.canvas_height}:d=10[bg]")
        filters.append(f"[bg][scaled]overlay={video_x}:{video_y}[with_video]")
        
        # 3. Add title text overlay
        title_y = 100  # Top of screen
        filters.append(
            f"[with_video]drawtext="
            f"text='{title_escaped}':"
            f"fontsize={font_size}:"
            f"fontcolor={font_color}:"
            f"x=(w-text_w)/2:"
            f"y={title_y}:"
            f"box=1:"
            f"boxcolor={box_color}:"
            f"boxborderw=10[with_title]"
        )
        
        # 4. Add VHS scanlines effect
        filters.append(
            "[with_title]split[a][b];"
            "[a]geq='lum=p(X,Y)':cb='p(X,Y)':cr='p(X,Y)',format=yuv420p[scanlines];"
            "[scanlines]crop=iw:2:0:0,scale=iw:ih[line];"
            "[b][line]blend=all_mode=overlay:all_opacity=0.1[with_scanlines]"
        )
        
        # 5. Add chromatic aberration (RGB split)
        filters.append(
            "[with_scanlines]split=3[r][g][b];"
            "[r]lutrgb=g=0:b=0[red];"
            "[g]lutrgb=r=0:b=0[green];"
            "[b]lutrgb=r=0:g=0[blue];"
            "[red]crop=iw-6:ih:0:0[red_crop];"
            "[green]crop=iw-6:ih:3:0[green_crop];"
            "[blue]crop=iw-6:ih:6:0[blue_crop];"
            "color=c=black:s={self.canvas_width}x{self.canvas_height}[bg2];"
            "[bg2][red_crop]overlay=0:0[r_over];"
            "[r_over][green_crop]overlay=3:0:format=auto,format=yuv420p[rg_over];"
            "[rg_over][blue_crop]overlay=6:0:format=auto,format=yuv420p[with_aberration]"
        )
        
        # 6. Add digital noise
        filters.append(
            "[with_aberration]noise=alls=3:allf=t[with_noise]"
        )
        
        # 7. Add vignette (CRT effect)
        filters.append(
            "[with_noise]vignette=angle=PI/2:mode=forward[output]"
        )
        
        return ";".join(filters)
    
    def create_simple_layout(
        self,
        video_path: str,
        title: str,
        style: Literal["WARNING", "COMEDY"],
        output_path: Optional[str] = None
    ) -> str:
        """
        Create simplified layout without heavy VHS effects (faster).
        
        Args:
            video_path: Path to talking head video
            title: Video title text
            style: Video style ("WARNING" or "COMEDY")
            output_path: Output path (default: auto-generated)
            
        Returns:
            Path to output video
        """
        if output_path is None:
            base = Path(video_path).stem
            output_path = str(Path(video_path).parent / f"{base}_simple_layout.mp4")
        
        print(f"[LAYOUT] Creating simple {style} layout...")
        
        # Escape title
        title_escaped = title.replace("'", "'\\''").replace(":", "\\:")
        
        # Choose style
        if style == "WARNING":
            font_size = 44
            font_color = "white"
            box_color = "black@0.6"
        else:
            font_size = 42
            font_color = "yellow"
            box_color = "black@0.5"
        
        # Calculate positions
        video_x = (self.canvas_width - self.video_width) // 2
        video_y = (self.canvas_height - self.video_height) // 2
        
        # Simple filter: scale, canvas, title
        filter_complex = (
            f"[0:v]scale={self.video_width}:{self.video_height}:force_original_aspect_ratio=decrease,"
            f"pad={self.video_width}:{self.video_height}:(ow-iw)/2:(oh-ih)/2[scaled];"
            f"color=c=black:s={self.canvas_width}x{self.canvas_height}:d=10[bg];"
            f"[bg][scaled]overlay={video_x}:{video_y}[with_video];"
            f"[with_video]drawtext="
            f"text='{title_escaped}':"
            f"fontsize={font_size}:"
            f"fontcolor={font_color}:"
            f"x=(w-text_w)/2:"
            f"y=100:"
            f"box=1:"
            f"boxcolor={box_color}:"
            f"boxborderw=10[output]"
        )
        
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', video_path,
            '-filter_complex', filter_complex,
            '-map', '[output]',
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            '-pix_fmt', 'yuv420p',
            '-y',
            output_path
        ]
        
        try:
            subprocess.run(ffmpeg_cmd, capture_output=True, text=True, check=True)
            print(f"[LAYOUT] ✅ Simple layout created: {output_path}")
            return output_path
        except Exception as e:
            print(f"[LAYOUT] ❌ Error: {e}")
            raise


def apply_vhs_effects(
    input_path: str,
    output_path: Optional[str] = None,
    effect_intensity: float = 1.0
) -> str:
    """
    Apply VHS effects to existing video.
    
    Args:
        input_path: Path to input video
        output_path: Output path (default: input with _vhs suffix)
        effect_intensity: Effect intensity 0-1 (default: 1.0)
        
    Returns:
        Path to output video
    """
    if output_path is None:
        base = Path(input_path).stem
        output_path = str(Path(input_path).parent / f"{base}_vhs.mp4")
    
    print(f"[VHS] Applying effects (intensity: {effect_intensity})...")
    
    # Scale intensity
    noise_amount = int(3 * effect_intensity)
    
    # VHS filter chain
    filter_complex = (
        f"[0:v]noise=alls={noise_amount}:allf=t[noisy];"
        "[noisy]vignette=angle=PI/2:mode=forward[output]"
    )
    
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', input_path,
        '-filter_complex', filter_complex,
        '-map', '[output]',
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '23',
        '-y',
        output_path
    ]
    
    try:
        subprocess.run(ffmpeg_cmd, capture_output=True, text=True, check=True)
        print(f"[VHS] ✅ Effects applied: {output_path}")
        return output_path
    except Exception as e:
        print(f"[VHS] ❌ Error: {e}")
        raise


if __name__ == "__main__":
    print("=== Video Layout Creator Test ===\n")
    
    creator = VideoLayoutCreator()
    
    print("Layout configuration:")
    print(f"  Canvas: {creator.canvas_width}x{creator.canvas_height}")
    print(f"  Video: {creator.video_width}x{creator.video_height}")
    print(f"  Position: centered")
    
    print("\n✅ Video layout creator initialized!")
    print("\nTo create a layout:")
    print("  creator.create_pip_layout('video.mp4', 'WARNING: Test Title', 'WARNING')")
    print("\nFor simple layout (faster):")
    print("  creator.create_simple_layout('video.mp4', 'Test Title', 'COMEDY')")
