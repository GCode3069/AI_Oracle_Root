#!/usr/bin/env python3
"""SCARIFY Video Generator - Professional Shorts with Text Overlays"""
import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv
from moviepy.editor import (
    VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip,
    concatenate_videoclips, ImageClip
)
import qrcode
import numpy as np
import scipy.io.wavfile as wav

# Load .env with ABSOLUTE path
env_path = Path(__file__).parent / "config" / "credentials" / ".env"
load_dotenv(env_path)

class VideoGenerator:
    """Professional YouTube Shorts generator with text overlays"""
    
    def __init__(self):
        self.pexels_key = 'RgE9Mdn3ToSQhn2RiLJ4mPMISjjp587QKRG9uhpOrLVtKkPCibUPUDGh'
        if not self.pexels_key:
            print("[WARNING] PEXELS_API_KEY not in .env")
        
        # Text overlay settings
        self.hook_duration = 3  # Hook text shown for first 3 seconds
        self.cta_duration = 5   # CTA text shown for last 5 seconds
        
        # Font settings (try multiple fonts for compatibility)
        self.font_options = [
            'Arial-Bold',
            'Impact',
            'Helvetica-Bold',
            'Arial',
            'Helvetica'
        ]
        self.font_size = 70  # Large and bold for mobile viewing
        self.font_color = 'white'
        self.stroke_color = 'black'
        self.stroke_width = 3
        
        # BTC QR settings
        self.btc_address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"  # Default BTC address
        self.qr_duration = 5  # Show QR for last 5 seconds
    
    def generate(self, keywords: str, audio_path: str, output_path: str, target_duration: int = 50, hook_text: str = None, cta_text: str = None, add_btc_qr: bool = True) -> bool:
        """
        Generate professional YouTube Short with text overlays
        
        Args:
            keywords: Pexels search keywords
            audio_path: Path to audio file
            output_path: Where to save final video
            target_duration: Video length in seconds
            hook_text: Text overlay for first 3 seconds (optional)
            cta_text: Call-to-action text for last 5 seconds (optional)
        """
        print(f"\n[VIDEO] VIDEO GENERATION (Professional)")
        print(f"   Keywords: {keywords}")
        print(f"   Target: {target_duration}s")
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        # Search Pexels
        print(f"   [SEARCH] Searching Pexels...")
        urls = self._search_pexels(keywords, 5)
        if not urls:
            print("   [ERROR] No videos found")
            return False
        
        # Download clips
        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)
        clips = []
        for i, url in enumerate(urls, 1):
            temp = temp_dir / f"clip_{i}.mp4"
            if self._download(url, str(temp)):
                clips.append(str(temp))
        
        if not clips:
            print("   [ERROR] No clips downloaded")
            return False
        
        print(f"   [SUCCESS] Downloaded {len(clips)} clips")
        
        # Stitch and add overlays
        return self._stitch_with_overlays(
            clips, audio_path, output_path, target_duration,
            hook_text, cta_text, add_btc_qr
        )
    
    def _search_pexels(self, query: str, count: int = 5):
        """Search Pexels for vertical videos"""
        if not self.pexels_key:
            return []
        
        try:
            r = requests.get(
                "https://api.pexels.com/videos/search",
                headers={"Authorization": self.pexels_key},
                params={"query": query, "per_page": count, "orientation": "portrait"},
                timeout=10
            )
            r.raise_for_status()
            
            videos = r.json().get('videos', [])
            urls = []
            for v in videos[:count]:
                for f in v.get('video_files', []):
                    if f.get('width', 0) < f.get('height', 0):
                        urls.append(f['link'])
                        break
            
            return urls
        except Exception as e:
            print(f"      Pexels error: {e}")
            return []
    
    def _download(self, url: str, path: str) -> bool:
        """Download video from URL"""
        try:
            r = requests.get(url, stream=True, timeout=30)
            r.raise_for_status()
            with open(path, 'wb') as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
            return os.path.exists(path) and os.path.getsize(path) > 0
        except Exception as e:
            print(f"      Download error: {e}")
            return False
    
    def _create_text_clip(self, text: str, duration: float, position: str = 'top'):
        """
        Create text overlay clip with professional styling
        
        Args:
            text: Text to display
            duration: How long to show text
            position: 'top' or 'bottom'
        """
        # Try fonts in order of preference
        font = None
        for font_name in self.font_options:
            try:
                test_clip = TextClip(
                    "TEST",
                    fontsize=self.font_size,
                    font=font_name,
                    color=self.font_color,
                    stroke_color=self.stroke_color,
                    stroke_width=self.stroke_width
                )
                test_clip.close()
                font = font_name
                break
            except:
                continue
        
        if not font:
            font = self.font_options[0]  # Fallback to first option
        
        # Create text clip
        txt_clip = TextClip(
            text,
            fontsize=self.font_size,
            font=font,
            color=self.font_color,
            stroke_color=self.stroke_color,
            stroke_width=self.stroke_width,
            method='caption',
            size=(1000, None),  # Width for mobile, auto height
            align='center'
        ).set_duration(duration)
        
        # Position the text
        if position == 'top':
            txt_clip = txt_clip.set_position(('center', 100))  # Top with margin
        else:  # bottom
            txt_clip = txt_clip.set_position(('center', 1700))  # Bottom with margin (1920 - 220)
        
        return txt_clip
    
    def _create_btc_qr_clip(self):
        """Create Bitcoin QR code overlay"""
        try:
            # Generate QR code
            qr = qrcode.QRCode(version=1, box_size=8, border=4)
            qr.add_data(f"bitcoin:{self.btc_address}")
            qr.make(fit=True)
            
            # Create QR image
            qr_img = qr.make_image(fill_color="white", back_color="black")
            
            # Convert to MoviePy clip
            qr_clip = ImageClip(qr_img).set_duration(self.qr_duration)
            
            # Position in top right corner
            qr_clip = qr_clip.set_position(('right', 'top')).resize(height=200)
            
            return qr_clip
            
        except Exception as e:
            print(f"      BTC QR error: {e}")
            return None
    
    def _stitch_with_overlays(self, files, audio_path, output, duration, hook_text=None, cta_text=None, add_btc_qr=True):
        """Stitch video clips with professional text overlays"""
        try:
            print(f"   [STITCH] Stitching clips...")
            clips = [VideoFileClip(f) for f in files]
            base_video = concatenate_videoclips(clips, method="compose")
            
            # Add audio
            if os.path.exists(audio_path):
                print(f"   [AUDIO] Adding audio...")
                audio = AudioFileClip(audio_path)
                
                # Loop video if shorter than audio
                if base_video.duration < audio.duration:
                    loops_needed = int(audio.duration / base_video.duration) + 1
                    base_video = base_video.loop(loops_needed)
                
                # Trim to audio length
                base_video = base_video.subclip(0, audio.duration).set_audio(audio)
            
            # Create composite with text overlays
            overlays = [base_video]
            
            # Hook text (first 3 seconds at top) - DISABLED (requires ImageMagick)
            if False and hook_text:  # Disabled for now
                print(f"   [TEXT] Adding hook text...")
                hook_clip = self._create_text_clip(
                    hook_text,
                    min(self.hook_duration, base_video.duration),
                    position='top'
                ).set_start(0)
                overlays.append(hook_clip)
            
            # CTA text (last 5 seconds at bottom) - DISABLED (requires ImageMagick)
            if False and cta_text and base_video.duration > self.cta_duration:  # Disabled for now
                print(f"   [TEXT] Adding CTA text...")
                cta_clip = self._create_text_clip(
                    cta_text,
                    self.cta_duration,
                    position='bottom'
                ).set_start(base_video.duration - self.cta_duration)
                overlays.append(cta_clip)
            
            # BTC QR code (last 5 seconds, top right) - DISABLED (requires ImageMagick)
            if False and add_btc_qr and base_video.duration > self.qr_duration:  # Disabled for now
                print(f"   [QR] Adding BTC QR code...")
                qr_clip = self._create_btc_qr_clip()
                qr_clip = qr_clip.set_start(base_video.duration - self.qr_duration)
                overlays.append(qr_clip)
            
            # Composite final video
            final_video = CompositeVideoClip(overlays)
            
            # Write to file
            print(f"   [RENDER] Rendering final video...")
            final_video.write_videofile(
                output,
                fps=30,
                codec='libx264',
                audio_codec='aac',
                preset='medium',
                threads=4,
                logger=None
            )
            
            # Cleanup
            for c in clips:
                try:
                    c.close()
                except:
                    pass
            
            try:
                base_video.close()
                final_video.close()
            except:
                pass
            
            # Verify output
            if os.path.exists(output):
                size_mb = os.path.getsize(output) / 1024 / 1024
                print(f"   [SUCCESS] Complete: {size_mb:.1f} MB")
                return True
            else:
                print(f"   [ERROR] Output file not created")
                return False
                
        except Exception as e:
            print(f"   [ERROR] Stitching error: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    gen = VideoGenerator()
    gen.generate(sys.argv[1], sys.argv[2], sys.argv[3]) if len(sys.argv) > 3 else print("Usage: python video_generator.py 'keywords' audio.wav output.mp4")
