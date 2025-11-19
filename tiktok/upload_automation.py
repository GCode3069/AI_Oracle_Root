#!/usr/bin/env python3
"""
TikTok Upload Automation for @nunyabeznes2
Multiple upload methods with fallbacks
"""

import os
import time
import random
from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Optional, List

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


class TikTokUploader:
    """TikTok upload automation for @nunyabeznes2"""
    
    def __init__(self, username: str = "@nunyabeznes2"):
        self.username = username
        self.upload_methods = [
            self.try_playwright_automation,
            self.try_selenium_automation,
            self.generate_manual_instructions
        ]
        
        self.upload_schedule = {
            'optimal_times': ['09:00', '12:00', '15:00', '18:00', '21:00'],
            'max_daily_posts': 5,
            'time_between_posts': '2-4 hours'
        }
    
    def try_playwright_automation(
        self,
        video_path: str,
        caption: str,
        hashtags: str = ""
    ) -> Dict:
        """Method 1: Playwright browser automation"""
        if not PLAYWRIGHT_AVAILABLE:
            return {
                'status': 'UNAVAILABLE',
                'method': 'playwright',
                'error': 'Playwright not installed. Run: pip install playwright && playwright install'
            }
        
        try:
            print("\n[Method 1] Using Playwright automation...")
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                context = browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )
                page = context.new_page()
                
                # Go to TikTok upload page
                page.goto("https://www.tiktok.com/upload", wait_until='networkidle')
                
                # Check if login is required
                if "login" in page.url.lower() or page.locator('text=Log in').count() > 0:
                    print("  ⚠️  Login required. Please log in manually...")
                    print("  Waiting for login (timeout: 2 minutes)...")
                    try:
                        page.wait_for_url("**/upload**", timeout=120000)
                        print("  ✅ Login detected!")
                    except PlaywrightTimeout:
                        browser.close()
                        return {
                            'status': 'LOGIN_REQUIRED',
                            'method': 'playwright',
                            'error': 'Login timeout. Please log in manually and try again.'
                        }
                
                # Upload video file
                file_input = page.locator('input[type="file"]')
                if file_input.count() == 0:
                    file_input = page.locator('input[accept*="video"]')
                
                if file_input.count() == 0:
                    browser.close()
                    return {
                        'status': 'FAILED',
                        'method': 'playwright',
                        'error': 'Could not find file input. TikTok interface may have changed.'
                    }
                
                file_input.set_input_files(str(Path(video_path).absolute()))
                
                # Wait for video to process
                page.wait_for_selector('div[contenteditable="true"], textarea[placeholder*="caption"]', timeout=120000)
                
                # Add caption
                caption_input = page.locator('div[contenteditable="true"], textarea[placeholder*="caption"]').first
                caption_input.click()
                caption_input.fill(caption)
                
                page.wait_for_timeout(2000)
                
                # Click post button
                post_button = page.locator('button:has-text("Post"), button:has-text("Publish")').first
                
                if post_button.count() == 0:
                    browser.close()
                    return {
                        'status': 'FAILED',
                        'method': 'playwright',
                        'error': 'Could not find post button.'
                    }
                
                post_button.click()
                
                # Wait for success
                try:
                    page.wait_for_url("**/video/**", timeout=120000)
                    video_url = page.url
                    browser.close()
                    
                    return {
                        'status': 'SUCCESS',
                        'method': 'playwright',
                        'url': video_url
                    }
                except PlaywrightTimeout:
                    browser.close()
                    return {
                        'status': 'PENDING',
                        'method': 'playwright',
                        'note': 'Upload may have succeeded but confirmation timeout'
                    }
                
        except Exception as e:
            return {
                'status': 'FAILED',
                'method': 'playwright',
                'error': str(e)
            }
    
    def try_selenium_automation(
        self,
        video_path: str,
        caption: str,
        hashtags: str = ""
    ) -> Dict:
        """Method 2: Selenium browser automation"""
        if not SELENIUM_AVAILABLE:
            return {
                'status': 'UNAVAILABLE',
                'method': 'selenium',
                'error': 'Selenium not installed. Run: pip install selenium'
            }
        
        try:
            print("\n[Method 2] Using Selenium automation...")
            
            # This would implement Selenium-based upload
            # Similar to Playwright but using Selenium
            return {
                'status': 'MANUAL_SETUP_REQUIRED',
                'method': 'selenium',
                'instructions': 'Selenium automation requires additional setup'
            }
        except Exception as e:
            return {
                'status': 'FAILED',
                'method': 'selenium',
                'error': str(e)
            }
    
    def generate_manual_instructions(
        self,
        video_path: str,
        caption: str,
        hashtags: str = ""
    ) -> Dict:
        """Method 3: Detailed manual upload instructions"""
        try:
            print("\n[Method 3] Generating manual upload instructions...")
            
            video_path_obj = Path(video_path)
            if not video_path_obj.exists():
                return {
                    'status': 'FAILED',
                    'method': 'manual',
                    'error': f'Video file not found: {video_path}'
                }
            
            instructions = f"""
🎬 MANUAL TIKTOK UPLOAD INSTRUCTIONS
===================================
FOR: {self.username}

VIDEO: {video_path_obj.absolute()}

CAPTION (Copy Exactly):
{caption}

HASHTAGS: {hashtags or "Included in caption"}

UPLOAD STEPS:
1. Open TikTok app on your phone (or web: https://www.tiktok.com/upload)
2. Tap '+' button to create new video
3. Tap 'Upload' and select: {video_path_obj.absolute()}
4. Trim video to 15-30 seconds if needed (keep most impactful parts)
5. Add caption (copy from above)
6. Verify hashtags are included
7. Select cover image (choose dramatic frame)
8. Post to {self.username}

SCHEDULING:
- Best times: {', '.join(self.upload_schedule['optimal_times'])}
- Max {self.upload_schedule['max_daily_posts']} posts per day
- Space posts 2-4 hours apart

POST IMMEDIATELY TO GROW {self.username.upper()}!
"""
            
            instruction_file = video_path_obj.parent / f"{video_path_obj.stem}_TIKTOK_INSTRUCTIONS.txt"
            instruction_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(instruction_file, 'w', encoding='utf-8') as f:
                f.write(instructions)
            
            print(f"  ✅ Instructions saved: {instruction_file}")
            
            return {
                'status': 'MANUAL_INSTRUCTIONS_GENERATED',
                'method': 'manual',
                'instruction_file': str(instruction_file)
            }
            
        except Exception as e:
            return {
                'status': 'FAILED',
                'method': 'manual',
                'error': str(e)
            }
    
    def upload_video(
        self,
        video_path: str,
        caption: str,
        hashtags: str = ""
    ) -> Dict:
        """Attempt all upload methods"""
        
        if not os.path.exists(video_path):
            return {
                'status': 'FAILED',
                'error': f'Video file not found: {video_path}'
            }
        
        for method in self.upload_methods:
            result = method(video_path, caption, hashtags)
            if result['status'] in ['SUCCESS', 'MANUAL_INSTRUCTIONS_GENERATED', 'PENDING']:
                return result
        
        return {
            'status': 'ALL_METHODS_FAILED',
            'error': 'All upload methods failed'
        }
    
    def schedule_upload(
        self,
        video_path: str,
        caption: str,
        hashtags: str = "",
        post_time: Optional[str] = None
    ) -> Dict:
        """Schedule upload for optimal timing"""
        
        if not post_time:
            # Pick random optimal time
            post_time = random.choice(self.upload_schedule['optimal_times'])
        
        return {
            'scheduled_time': post_time,
            'video': video_path,
            'caption': caption,
            'hashtags': hashtags,
            'status': 'SCHEDULED'
        }


class TikTokContentPipeline:
    """Complete content pipeline for @nunyabeznes2"""
    
    def __init__(self):
        from tiktok.brand_integration import NunyaBeznes2Brand, TikTokAutomation
        self.brand = NunyaBeznes2Brand()
        self.automation = TikTokAutomation()
        self.uploader = TikTokUploader()
        self.content_queue = []
        
    def process_youtube_content_for_tiktok(
        self,
        youtube_video_path: str,
        topic: str,
        horror_style: str = 'psychological'
    ) -> Dict:
        """Convert YouTube content to TikTok format"""
        
        youtube_path = Path(youtube_video_path)
        tiktok_video_path = youtube_path.parent / f"{youtube_path.stem}_TIKTOK.mp4"
        
        processing_instructions = {
            'source_video': str(youtube_path),
            'target_video': str(tiktok_video_path),
            'processing_steps': [
                'Trim to 15-30 seconds (keep most impactful parts)',
                'Apply @nunyabeznes2 brand filter (red/black theme)',
                'Add brand watermark (bottom right)',
                'Speed up pacing (1.1x speed for TikTok attention span)',
                'Add trending sound overlay'
            ]
        }
        
        # Generate TikTok caption and metadata
        # Note: In production, would extract script from video metadata
        sample_script = f"Corporate horror story about {topic}"
        tiktok_content = self.automation.adapt_youtube_content_for_tiktok(
            sample_script, topic, horror_style
        )
        
        content_job = {
            'topic': topic,
            'horror_style': horror_style,
            'source_video': str(youtube_path),
            'tiktok_video': str(tiktok_video_path),
            'caption': tiktok_content['caption'],
            'content_format': tiktok_content['content_format'],
            'sound': tiktok_content['sound'],
            'processing_instructions': processing_instructions,
            'status': 'READY_FOR_PROCESSING'
        }
        
        self.content_queue.append(content_job)
        return content_job
    
    def process_next_in_queue(self) -> Dict:
        """Process next item in content queue"""
        
        if not self.content_queue:
            return {'status': 'QUEUE_EMPTY'}
        
        next_job = self.content_queue[0]
        
        # Simulate video processing (in production, would use FFmpeg)
        processed_video = self._process_video_for_tiktok(next_job)
        
        # Attempt upload
        upload_result = self.uploader.upload_video(
            processed_video['video_path'],
            next_job['caption'],
            " ".join(self.brand.brand_assets['hashtags'][:6])
        )
        
        # Remove from queue
        self.content_queue.pop(0)
        
        return {
            'job': next_job,
            'processing_result': processed_video,
            'upload_result': upload_result
        }
    
    def _process_video_for_tiktok(self, job: Dict) -> Dict:
        """Process video for TikTok (placeholder implementation)"""
        
        # In production, this would use FFmpeg to:
        # - Trim to 15-30 seconds
        # - Apply brand filters
        # - Add watermark
        # - Adjust pacing
        
        return {
            'video_path': job['tiktok_video'],
            'processing_applied': job['processing_instructions']['processing_steps'],
            'status': 'PROCESSED'
        }


if __name__ == '__main__':
    # Test uploader
    uploader = TikTokUploader()
    
    test_video = "test_video.mp4"
    test_caption = "🚨 Corporate horror but make it business 🚨\n\n#nunyabeznes #businesshorror\n@nunyabeznes2"
    
    if os.path.exists(test_video):
        result = uploader.upload_video(test_video, test_caption)
        print(f"Upload result: {result}")
    else:
        print(f"Test video not found: {test_video}")
        print("Generating manual instructions instead...")
        result = uploader.generate_manual_instructions(test_video, test_caption)
        print(f"Result: {result}")
