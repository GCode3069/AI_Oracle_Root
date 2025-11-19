#!/usr/bin/env python3
"""
SCARIFY TikTok Automation System
@nunyabeznes2 - Dark Satirical Business Horror Brand
"""

import os
import sys
import json
import random
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

try:
    from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip, ImageClip
    from moviepy.video.fx import resize, crop
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    print("⚠️  moviepy not installed. Install with: pip install moviepy")

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️  playwright not installed. Install with: pip install playwright && playwright install")

try:
    from PIL import Image, ImageDraw, ImageFont
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False


# Brand Configuration
BRAND_CONFIG = {
    "username": "@nunyabeznes2",
    "brand_voice": "dark satirical business horror",
    "color_scheme": {
        "primary": "#FF0000",  # Red
        "secondary": "#000000",  # Black
        "accent": "#FFFFFF"  # White
    },
    "hashtags": [
        "#nunyabeznes",
        "#businesshorror",
        "#corporatenightmare",
        "#profitsoverpeople",
        "#corporategreed",
        "#capitalismexposed",
        "#darkbusiness",
        "#corporatehorror",
        "#businessnightmare",
        "#corporatetruth"
    ],
    "posting_times": ["09:00", "12:00", "15:00", "18:00", "21:00"],  # Optimal TikTok times
    "watermark_opacity": 0.1,  # 10% opacity
    "watermark_position": "bottom_right"
}

# Content Calendar Themes
CONTENT_CALENDAR = {
    'monday': ['Business Horrors', 'Corporate Truths', 'Monday Dread'],
    'tuesday': ['Profit Nightmares', 'CEO Confessions', 'Corporate Lies'],
    'wednesday': ['Workplace Horror', 'Salary Secrets', 'Midweek Madness'],
    'thursday': ['Corporate Conspiracies', 'Business Lies', 'Thursday Truths'],
    'friday': ['Weekend Warning', 'Corporate Exposed', 'Friday Fears'],
    'saturday': ['Dark Business Facts', 'Capitalism Horrors', 'Weekend Warnings'],
    'sunday': ['Monday Preparation', 'Corporate Dread', 'Sunday Scaries']
}


class TikTokVideoOptimizer:
    """Optimize videos for TikTok format"""
    
    TIKTOK_RESOLUTION = (1080, 1920)  # 9:16 aspect ratio
    TIKTOK_MAX_DURATION = 30  # seconds
    TIKTOK_MIN_DURATION = 15  # seconds
    
    def __init__(self, base_path: Optional[Path] = None):
        if base_path is None:
            current = Path(__file__).parent
            if (current / "abraham_horror").exists():
                base_path = current
            else:
                base_path = Path("/workspace")
        
        self.base_path = Path(base_path)
        self.output_dir = self.base_path / "tiktok_content" / "ready_to_upload"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def optimize_for_tiktok(
        self,
        input_video: str,
        output_path: Optional[str] = None,
        trim_to_best: bool = True
    ) -> Optional[str]:
        """
        Convert YouTube video → TikTok format
        
        Args:
            input_video: Path to input video
            output_path: Optional output path (auto-generated if None)
            trim_to_best: If True, trim to most impactful 15-30 seconds
        
        Returns:
            Path to optimized video or None on failure
        """
        if not MOVIEPY_AVAILABLE:
            print("❌ moviepy not available. Cannot optimize video.")
            return None
        
        try:
            input_path = Path(input_video)
            if not input_path.exists():
                print(f"❌ Input video not found: {input_video}")
                return None
            
            # Generate output path
            if output_path is None:
                output_path = self.output_dir / f"tiktok_{input_path.stem}.mp4"
            else:
                output_path = Path(output_path)
            
            print(f"\n🎬 Optimizing for TikTok: {input_path.name}")
            
            # Load video
            video = VideoFileClip(str(input_path))
            duration = video.duration
            
            print(f"   Original duration: {duration:.1f}s")
            
            # Trim to optimal length
            if trim_to_best and duration > self.TIKTOK_MAX_DURATION:
                # Keep first 30 seconds (most impactful hook)
                video = video.subclip(0, min(self.TIKTOK_MAX_DURATION, duration))
                print(f"   Trimmed to: {video.duration:.1f}s")
            elif duration < self.TIKTOK_MIN_DURATION:
                print(f"   ⚠️  Video too short ({duration:.1f}s). Minimum: {self.TIKTOK_MIN_DURATION}s")
                # Still process, but warn
            
            # Get current dimensions
            w, h = video.size
            target_aspect = 9 / 16  # TikTok aspect ratio
            
            print(f"   Original size: {w}x{h}")
            
            # Crop to 9:16 aspect ratio
            current_aspect = w / h
            
            if current_aspect > target_aspect:
                # Too wide - crop sides
                new_width = int(h * target_aspect)
                x1 = int((w - new_width) / 2)
                video = crop(video, x1=x1, width=new_width)
                print(f"   Cropped to: {new_width}x{h}")
            elif current_aspect < target_aspect:
                # Too tall - crop top/bottom
                new_height = int(w / target_aspect)
                y1 = int((h - new_height) / 2)
                video = crop(video, y1=y1, height=new_height)
                print(f"   Cropped to: {w}x{new_height}")
            
            # Resize to TikTok resolution
            video = resize(video, self.TIKTOK_RESOLUTION)
            print(f"   Resized to: {self.TIKTOK_RESOLUTION[0]}x{self.TIKTOK_RESOLUTION[1]}")
            
            # Apply red/black color filter
            video = self._apply_brand_filter(video)
            
            # Add watermark
            video = self._add_watermark(video)
            
            # Write output
            print(f"   Rendering to: {output_path.name}")
            video.write_videofile(
                str(output_path),
                codec='libx264',
                audio_codec='aac',
                fps=30,
                preset='medium',
                bitrate='8000k',
                threads=4,
                logger=None  # Suppress verbose output
            )
            
            video.close()
            
            print(f"   ✅ Optimized video saved: {output_path}")
            return str(output_path)
            
        except Exception as e:
            print(f"   ❌ Optimization failed: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _apply_brand_filter(self, video):
        """Apply red/black color scheme filter"""
        try:
            # Apply color correction to enhance red/black theme
            # This is a simplified version - can be enhanced with actual color grading
            def make_frame(t):
                frame = video.get_frame(t)
                # Enhance reds and darken other colors
                # This is a placeholder - actual implementation would use proper color grading
                return frame
            
            return video.fl(lambda gf, t: make_frame(t))
        except:
            # If filter fails, return original
            return video
    
    def _add_watermark(self, video):
        """Add @nunyabeznes2 watermark"""
        if not PILLOW_AVAILABLE:
            return video
        
        try:
            # Create watermark text
            watermark_text = BRAND_CONFIG["username"]
            
            # Create text clip
            txt_clip = TextClip(
                watermark_text,
                fontsize=30,
                color='white',
                font='Arial-Bold'
            ).set_duration(video.duration).set_opacity(BRAND_CONFIG["watermark_opacity"])
            
            # Position at bottom right
            w, h = video.size
            txt_w, txt_h = txt_clip.size
            txt_clip = txt_clip.set_position(('right', 'bottom')).set_margin((10, 10))
            
            # Composite
            final = CompositeVideoClip([video, txt_clip])
            return final
            
        except Exception as e:
            print(f"   ⚠️  Watermark failed: {e}. Continuing without watermark.")
            return video


class TikTokCaptionGenerator:
    """Generate TikTok captions with brand voice"""
    
    def __init__(self):
        self.brand_config = BRAND_CONFIG
    
    def generate_caption(self, topic: str, video_title: Optional[str] = None) -> str:
        """
        Generate TikTok caption with brand voice
        
        Args:
            topic: Video topic/theme
            video_title: Optional original video title
        
        Returns:
            Formatted caption with hooks and hashtags
        """
        # Generate hook based on topic
        hooks = [
            f"🚨 {topic} but make it corporate horror 🚨",
            f"Business tip: Stop the {topic} madness",
            f"Corporate America's {topic} secret exposed",
            f"They don't teach this {topic} in business school",
            f"🚨 {topic} = modern slavery 🔗",
            f"Corporate horror story: {topic}",
            f"Business nightmare: {topic}",
            f"Profit over people: {topic} exposed"
        ]
        
        hook = random.choice(hooks)
        
        # Add brand hashtags
        hashtags = " ".join(self.brand_config["hashtags"][:6])  # Use top 6
        
        # Add username mention
        username = self.brand_config["username"]
        
        # Build caption (TikTok limit: 2200 characters, but shorter is better)
        caption = f"{hook}\n\n{hashtags}\n{username}"
        
        # Ensure it's under 500 characters (optimal length)
        if len(caption) > 500:
            caption = caption[:497] + "..."
        
        return caption
    
    def get_todays_themes(self) -> List[str]:
        """Get content themes for today"""
        day_name = datetime.now().strftime('%A').lower()
        return CONTENT_CALENDAR.get(day_name, ['Business Horror', 'Corporate Truth'])


class TikTokUploader:
    """Upload videos to TikTok using browser automation"""
    
    def __init__(self, base_path: Optional[Path] = None):
        if base_path is None:
            current = Path(__file__).parent
            if (current / "abraham_horror").exists():
                base_path = current
            else:
                base_path = Path("/workspace")
        
        self.base_path = Path(base_path)
        self.uploaded_dir = self.base_path / "tiktok_content" / "uploaded"
        self.uploaded_dir.mkdir(parents=True, exist_ok=True)
        self.analytics_dir = self.base_path / "tiktok_content" / "analytics"
        self.analytics_dir.mkdir(parents=True, exist_ok=True)
    
    def upload_video(
        self,
        video_path: str,
        caption: str,
        headless: bool = False
    ) -> Dict:
        """
        Upload video to TikTok using Playwright
        
        Args:
            video_path: Path to video file
            caption: Video caption
            headless: Run browser in headless mode (not recommended for first upload)
        
        Returns:
            Dict with upload status and URL
        """
        if not PLAYWRIGHT_AVAILABLE:
            return {
                "success": False,
                "error": "Playwright not installed. Run: pip install playwright && playwright install"
            }
        
        video_path_obj = Path(video_path)
        if not video_path_obj.exists():
            return {"success": False, "error": f"Video not found: {video_path}"}
        
        print(f"\n📤 Uploading to TikTok: {video_path_obj.name}")
        print(f"   Caption: {caption[:60]}...")
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=headless)
                context = browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )
                page = context.new_page()
                
                # Go to TikTok upload page
                print("   Navigating to TikTok upload page...")
                page.goto("https://www.tiktok.com/upload", wait_until='networkidle')
                
                # Check if login is required
                if "login" in page.url.lower() or page.locator('text=Log in').count() > 0:
                    print("   ⚠️  Login required. Please log in manually...")
                    print("   Waiting for login (timeout: 2 minutes)...")
                    try:
                        # Wait for upload page
                        page.wait_for_url("**/upload**", timeout=120000)
                        print("   ✅ Login detected!")
                    except PlaywrightTimeout:
                        return {
                            "success": False,
                            "error": "Login timeout. Please log in manually and try again."
                        }
                
                # Upload video file
                print("   Uploading video file...")
                file_input = page.locator('input[type="file"]')
                
                if file_input.count() == 0:
                    # Try alternative selectors
                    file_input = page.locator('input[accept*="video"]')
                
                if file_input.count() == 0:
                    return {
                        "success": False,
                        "error": "Could not find file input. TikTok interface may have changed."
                    }
                
                file_input.set_input_files(str(video_path_obj.absolute()))
                
                # Wait for video to process
                print("   Waiting for video processing...")
                try:
                    page.wait_for_selector('div[contenteditable="true"], textarea[placeholder*="caption"]', timeout=120000)
                except PlaywrightTimeout:
                    return {
                        "success": False,
                        "error": "Video processing timeout. File may be too large or corrupted."
                    }
                
                # Add caption
                print("   Adding caption...")
                caption_input = page.locator('div[contenteditable="true"], textarea[placeholder*="caption"]').first
                caption_input.click()
                caption_input.fill(caption)
                
                # Wait a moment
                page.wait_for_timeout(2000)
                
                # Click post button
                print("   Posting video...")
                post_button = page.locator('button:has-text("Post"), button:has-text("Publish")').first
                
                if post_button.count() == 0:
                    return {
                        "success": False,
                        "error": "Could not find post button. Please check TikTok interface."
                    }
                
                post_button.click()
                
                # Wait for success (redirect to video page)
                print("   Waiting for upload confirmation...")
                try:
                    page.wait_for_url("**/video/**", timeout=120000)
                    video_url = page.url
                    
                    print(f"   ✅ Upload successful!")
                    print(f"   🔗 URL: {video_url}")
                    
                    # Save to uploaded directory
                    uploaded_file = self.uploaded_dir / video_path_obj.name
                    if video_path_obj != uploaded_file:
                        import shutil
                        shutil.copy2(video_path_obj, uploaded_file)
                    
                    # Log analytics
                    self._log_upload(video_path_obj.name, video_url, caption)
                    
                    browser.close()
                    
                    return {
                        "success": True,
                        "url": video_url,
                        "video_path": str(uploaded_file)
                    }
                    
                except PlaywrightTimeout:
                    # Upload may have succeeded but didn't redirect
                    print("   ⚠️  Upload may have succeeded but confirmation timeout.")
                    return {
                        "success": True,
                        "url": "",
                        "note": "Upload completed but URL not captured"
                    }
                
        except Exception as e:
            print(f"   ❌ Upload failed: {e}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": str(e)}
    
    def _log_upload(self, video_name: str, url: str, caption: str):
        """Log upload to analytics"""
        log_file = self.analytics_dir / f"uploads_{datetime.now().strftime('%Y%m')}.json"
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "video": video_name,
            "url": url,
            "caption": caption[:200]  # Truncate long captions
        }
        
        # Load existing logs
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(entry)
        
        # Save
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)


class TikTokAutomationSystem:
    """Complete TikTok automation system"""
    
    def __init__(self, base_path: Optional[Path] = None):
        if base_path is None:
            current = Path(__file__).parent
            if (current / "abraham_horror").exists():
                base_path = current
            else:
                base_path = Path("/workspace")
        
        self.base_path = Path(base_path)
        self.optimizer = TikTokVideoOptimizer(base_path)
        self.caption_gen = TikTokCaptionGenerator()
        self.uploader = TikTokUploader(base_path)
    
    def process_video(
        self,
        input_video: str,
        topic: Optional[str] = None,
        auto_upload: bool = False
    ) -> Dict:
        """
        Complete pipeline: optimize → caption → upload
        
        Args:
            input_video: Path to input video
            topic: Video topic (for caption generation)
            auto_upload: If True, automatically upload after optimization
        
        Returns:
            Dict with processing results
        """
        results = {
            "input": input_video,
            "optimized": None,
            "caption": None,
            "uploaded": False,
            "url": None
        }
        
        # Step 1: Optimize
        print("\n" + "="*80)
        print("STEP 1: OPTIMIZING FOR TIKTOK")
        print("="*80)
        
        optimized_path = self.optimizer.optimize_for_tiktok(input_video)
        if not optimized_path:
            return {**results, "error": "Optimization failed"}
        
        results["optimized"] = optimized_path
        
        # Step 2: Generate caption
        print("\n" + "="*80)
        print("STEP 2: GENERATING CAPTION")
        print("="*80)
        
        if topic is None:
            # Try to extract from filename or use default
            video_name = Path(input_video).stem
            topic = video_name.replace("_", " ").title()
        
        caption = self.caption_gen.generate_caption(topic)
        results["caption"] = caption
        
        print(f"   Caption: {caption}")
        
        # Step 3: Upload (if requested)
        if auto_upload:
            print("\n" + "="*80)
            print("STEP 3: UPLOADING TO TIKTOK")
            print("="*80)
            
            upload_result = self.uploader.upload_video(optimized_path, caption)
            
            if upload_result.get("success"):
                results["uploaded"] = True
                results["url"] = upload_result.get("url")
            else:
                results["error"] = upload_result.get("error", "Upload failed")
        else:
            print("\n" + "="*80)
            print("STEP 3: READY FOR UPLOAD")
            print("="*80)
            print(f"   Video optimized: {optimized_path}")
            print(f"   Caption ready: {caption}")
            print(f"   Run with --upload to auto-upload")
        
        return results
    
    def batch_process(
        self,
        video_dir: str,
        limit: Optional[int] = None,
        auto_upload: bool = False
    ) -> List[Dict]:
        """Process multiple videos"""
        video_dir_path = Path(video_dir)
        videos = list(video_dir_path.glob("*.mp4"))
        
        if limit:
            videos = videos[:limit]
        
        print(f"\n🎬 Batch Processing {len(videos)} videos")
        
        results = []
        for i, video in enumerate(videos, 1):
            print(f"\n[{i}/{len(videos)}] Processing: {video.name}")
            result = self.process_video(str(video), auto_upload=auto_upload)
            results.append(result)
            
            if i < len(videos):
                print(f"\n⏳ Waiting 30s before next video...")
                import time
                time.sleep(30)
        
        return results


def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='TikTok Automation System for @nunyabeznes2')
    parser.add_argument('--optimize', help='Optimize video for TikTok', metavar='VIDEO_PATH')
    parser.add_argument('--upload', help='Upload video to TikTok', metavar='VIDEO_PATH')
    parser.add_argument('--full', help='Full pipeline: optimize + upload', metavar='VIDEO_PATH')
    parser.add_argument('--batch', help='Batch process directory', metavar='DIR')
    parser.add_argument('--limit', type=int, help='Limit number of videos in batch')
    parser.add_argument('--topic', help='Video topic for caption generation')
    parser.add_argument('--headless', action='store_true', help='Run browser in headless mode')
    
    args = parser.parse_args()
    
    system = TikTokAutomationSystem()
    
    if args.optimize:
        result = system.optimizer.optimize_for_tiktok(args.optimize)
        if result:
            print(f"\n✅ Optimized video: {result}")
        else:
            print("\n❌ Optimization failed")
            sys.exit(1)
    
    elif args.upload:
        caption_gen = TikTokCaptionGenerator()
        topic = args.topic or "Business Horror"
        caption = caption_gen.generate_caption(topic)
        
        result = system.uploader.upload_video(args.upload, caption, headless=args.headless)
        if result.get("success"):
            print(f"\n✅ Upload successful: {result.get('url')}")
        else:
            print(f"\n❌ Upload failed: {result.get('error')}")
            sys.exit(1)
    
    elif args.full:
        result = system.process_video(args.full, topic=args.topic, auto_upload=True)
        if result.get("uploaded"):
            print(f"\n✅ Complete! URL: {result.get('url')}")
        else:
            print(f"\n❌ Failed: {result.get('error', 'Unknown error')}")
            sys.exit(1)
    
    elif args.batch:
        results = system.batch_process(args.batch, limit=args.limit, auto_upload=True)
        successful = sum(1 for r in results if r.get("uploaded"))
        print(f"\n✅ Batch complete: {successful}/{len(results)} successful")
    
    else:
        parser.print_help()
        print("\n" + "="*80)
        print("EXAMPLES:")
        print("="*80)
        print("# Optimize a video:")
        print("python TIKTOK_AUTOMATION_SYSTEM.py --optimize video.mp4")
        print("\n# Upload a video:")
        print("python TIKTOK_AUTOMATION_SYSTEM.py --upload video.mp4 --topic 'Corporate Horror'")
        print("\n# Full pipeline (optimize + upload):")
        print("python TIKTOK_AUTOMATION_SYSTEM.py --full video.mp4 --topic 'Business Nightmare'")
        print("\n# Batch process directory:")
        print("python TIKTOK_AUTOMATION_SYSTEM.py --batch ./videos --limit 5")


if __name__ == '__main__':
    main()
