#!/usr/bin/env python3
"""
MULTI_PLATFORM_UPLOADER.py
Upload videos to 6 primary platforms: YouTube, TikTok, Instagram, Facebook, Twitter, Reddit
"""

import json
import time
from pathlib import Path
from datetime import datetime
import asyncio

BASE_DIR = Path(__file__).parent
VIDEOS_DIR = BASE_DIR / "abraham_horror" / "youtube_ready"
CONFIG_DIR = BASE_DIR / "config" / "platforms"
UPLOAD_LOG = BASE_DIR / "multi_platform_uploads.json"

BTC_ADDRESS = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"
PRODUCT_LINK = "https://trenchaikits.com/buy-rebel-$97"

# Platform configurations
PLATFORMS = {
    "youtube": {
        "enabled": True,
        "priority": 1,
        "max_length": 60,  # seconds
        "aspect_ratio": "9:16"
    },
    "tiktok": {
        "enabled": True,
        "priority": 2,
        "max_length": 60,
        "aspect_ratio": "9:16"
    },
    "instagram": {
        "enabled": True,
        "priority": 3,
        "max_length": 90,
        "aspect_ratio": "9:16"
    },
    "facebook": {
        "enabled": True,
        "priority": 4,
        "max_length": 120,
        "aspect_ratio": "9:16"
    },
    "twitter": {
        "enabled": True,
        "priority": 5,
        "max_length": 140,
        "aspect_ratio": "9:16"
    },
    "reddit": {
        "enabled": True,
        "priority": 6,
        "max_length": 60,
        "aspect_ratio": "9:16"
    }
}

class YouTubeUploader:
    """YouTube Shorts uploader"""
    def __init__(self):
        self.name = "YouTube"
        
    def upload(self, video_path, metadata):
        """Upload to YouTube (using existing system)"""
        try:
            from MULTI_CHANNEL_UPLOAD_OPTIMIZED import get_youtube_service, upload_video
            
            youtube = get_youtube_service(1)  # Channel 1
            result = upload_video(youtube, video_path, metadata, 1)
            
            return {
                "success": True,
                "platform": "youtube",
                "url": result.get("url"),
                "video_id": result.get("video_id")
            }
        except Exception as e:
            return {"success": False, "platform": "youtube", "error": str(e)}

class TikTokUploader:
    """TikTok uploader"""
    def __init__(self):
        self.name = "TikTok"
        self.session_file = CONFIG_DIR / "tiktok_session.json"
        
    def upload(self, video_path, metadata):
        """Upload to TikTok using instagrapi-like approach"""
        try:
            # TikTok requires browser automation (no official public API for uploads)
            # Using Playwright for automation
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)  # Visible browser for CAPTCHA
                page = browser.new_page()
                
                # Login to TikTok (requires manual first-time setup)
                page.goto("https://www.tiktok.com/upload")
                
                # Check if logged in
                if "login" in page.url.lower():
                    print(f"  [{self.name}] Please login manually (first time only)")
                    page.wait_for_url("**/upload**", timeout=120000)  # 2 min for login
                
                # Upload video
                file_input = page.locator('input[type="file"]')
                file_input.set_input_files(str(video_path))
                
                # Wait for upload processing
                page.wait_for_selector('textarea[placeholder*="caption"]', timeout=60000)
                
                # Add caption
                caption_box = page.locator('textarea[placeholder*="caption"]')
                caption = self._format_caption(metadata)
                caption_box.fill(caption)
                
                # Click post button
                post_button = page.locator('button:has-text("Post")')
                post_button.click()
                
                # Wait for success
                page.wait_for_url("**/video/**", timeout=60000)
                video_url = page.url
                
                browser.close()
                
                return {
                    "success": True,
                    "platform": "tiktok",
                    "url": video_url
                }
                
        except Exception as e:
            return {"success": False, "platform": "tiktok", "error": str(e)}
    
    def _format_caption(self, metadata):
        """Format caption for TikTok"""
        title = metadata.get("title", "")
        hashtags = ["#FYP", "#Viral", "#Horror", "#Conspiracy", "#AbrahamLincoln"]
        caption = f"{title[:100]} {' '.join(hashtags)}\n\nBTC: {BTC_ADDRESS}"
        return caption[:150]

class InstagramUploader:
    """Instagram Reels uploader"""
    def __init__(self):
        self.name = "Instagram"
        from instagrapi import Client
        self.client = Client()
        self.session_file = CONFIG_DIR / "instagram_session.json"
        
    def login(self):
        """Login to Instagram"""
        try:
            if self.session_file.exists():
                self.client.load_settings(self.session_file)
                self.client.login_by_sessionid(self.client.sessionid)
            else:
                # First-time login (requires credentials)
                username = input("Instagram username: ")
                password = input("Instagram password: ")
                self.client.login(username, password)
                self.client.dump_settings(self.session_file)
            
            return True
        except Exception as e:
            print(f"  [{self.name}] Login failed: {e}")
            return False
    
    def upload(self, video_path, metadata):
        """Upload reel to Instagram"""
        try:
            if not self.login():
                return {"success": False, "platform": "instagram", "error": "Login failed"}
            
            caption = self._format_caption(metadata)
            
            # Upload as reel
            media = self.client.clip_upload(
                path=str(video_path),
                caption=caption
            )
            
            return {
                "success": True,
                "platform": "instagram",
                "url": f"https://www.instagram.com/reel/{media.code}/",
                "media_id": media.pk
            }
            
        except Exception as e:
            return {"success": False, "platform": "instagram", "error": str(e)}
    
    def _format_caption(self, metadata):
        """Format caption for Instagram"""
        title = metadata.get("title", "")
        caption = f"{title}\n\n🔥 Rebel Kit: {PRODUCT_LINK}\n💸 BTC: {BTC_ADDRESS}\n\n#horror #conspiracy #abrahamlincoln #scary #viral #reels"
        return caption[:2200]

class FacebookUploader:
    """Facebook Reels uploader"""
    def __init__(self):
        self.name = "Facebook"
        
    def upload(self, video_path, metadata):
        """Upload to Facebook Reels (via Graph API)"""
        try:
            # Facebook Graph API requires app setup
            # For now, using browser automation
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                page = browser.new_page()
                
                page.goto("https://www.facebook.com/")
                
                # Manual login check
                if "login" in page.url.lower():
                    print(f"  [{self.name}] Please login manually")
                    page.wait_for_url("https://www.facebook.com/", timeout=120000)
                
                # Create reel
                page.goto("https://www.facebook.com/reel/create")
                
                # Upload video
                file_input = page.locator('input[type="file"]')
                file_input.set_input_files(str(video_path))
                
                # Wait for processing
                time.sleep(10)
                
                # Add description
                description = self._format_description(metadata)
                desc_box = page.locator('textarea, div[contenteditable="true"]').first
                desc_box.fill(description)
                
                # Post
                post_button = page.locator('button:has-text("Post"), div[role="button"]:has-text("Post")').first
                post_button.click()
                
                # Wait for success
                time.sleep(5)
                
                browser.close()
                
                return {
                    "success": True,
                    "platform": "facebook",
                    "url": "Posted to Facebook"
                }
                
        except Exception as e:
            return {"success": False, "platform": "facebook", "error": str(e)}
    
    def _format_description(self, metadata):
        """Format description for Facebook"""
        title = metadata.get("title", "")
        return f"{title}\n\n🔥 Rebel Kit: {PRODUCT_LINK}\n💸 Bitcoin: {BTC_ADDRESS}\n\n#horror #conspiracy #abrahamlincoln"

class TwitterUploader:
    """Twitter/X uploader"""
    def __init__(self):
        self.name = "Twitter/X"
        
    def upload(self, video_path, metadata):
        """Upload to Twitter/X"""
        try:
            import tweepy
            
            # Load credentials
            creds_file = CONFIG_DIR / "twitter_credentials.json"
            if not creds_file.exists():
                return {"success": False, "platform": "twitter", "error": "Credentials not found"}
            
            with open(creds_file) as f:
                creds = json.load(f)
            
            # Authenticate
            auth = tweepy.OAuthHandler(creds["api_key"], creds["api_secret"])
            auth.set_access_token(creds["access_token"], creds["access_secret"])
            api = tweepy.API(auth)
            
            # Upload video
            media = api.media_upload(str(video_path), media_category="tweet_video")
            
            # Create tweet
            tweet_text = self._format_tweet(metadata)
            tweet = api.update_status(status=tweet_text, media_ids=[media.media_id])
            
            return {
                "success": True,
                "platform": "twitter",
                "url": f"https://twitter.com/user/status/{tweet.id}",
                "tweet_id": tweet.id
            }
            
        except Exception as e:
            return {"success": False, "platform": "twitter", "error": str(e)}
    
    def _format_tweet(self, metadata):
        """Format tweet text"""
        title = metadata.get("title", "")
        tweet = f"{title[:200]}\n\n💸 BTC: {BTC_ADDRESS}\n🔥 {PRODUCT_LINK}"
        return tweet[:280]

class RedditUploader:
    """Reddit uploader"""
    def __init__(self):
        self.name = "Reddit"
        
    def upload(self, video_path, metadata):
        """Upload to Reddit"""
        try:
            import praw
            
            # Load credentials
            creds_file = CONFIG_DIR / "reddit_credentials.json"
            if not creds_file.exists():
                return {"success": False, "platform": "reddit", "error": "Credentials not found"}
            
            with open(creds_file) as f:
                creds = json.load(f)
            
            # Authenticate
            reddit = praw.Reddit(
                client_id=creds["client_id"],
                client_secret=creds["client_secret"],
                user_agent=creds["user_agent"],
                username=creds["username"],
                password=creds["password"]
            )
            
            # Upload to multiple subreddits
            subreddits = ["conspiracy", "horror", "CreepyPasta", "oddlyterrifying"]
            title = self._format_title(metadata)
            
            results = []
            for subreddit_name in subreddits:
                try:
                    subreddit = reddit.subreddit(subreddit_name)
                    submission = subreddit.submit_video(
                        title=title,
                        video_path=str(video_path)
                    )
                    results.append(f"https://reddit.com{submission.permalink}")
                except Exception as e:
                    print(f"  [{self.name}] Failed to post to r/{subreddit_name}: {e}")
            
            return {
                "success": len(results) > 0,
                "platform": "reddit",
                "urls": results
            }
            
        except Exception as e:
            return {"success": False, "platform": "reddit", "error": str(e)}
    
    def _format_title(self, metadata):
        """Format Reddit title"""
        title = metadata.get("title", "")
        return title[:300]

def upload_to_all_platforms(video_path, metadata, platforms=None):
    """Upload single video to all enabled platforms"""
    
    if platforms is None:
        platforms = [name for name, config in PLATFORMS.items() if config["enabled"]]
    
    results = {}
    
    uploaders = {
        "youtube": YouTubeUploader(),
        "tiktok": TikTokUploader(),
        "instagram": InstagramUploader(),
        "facebook": FacebookUploader(),
        "twitter": TwitterUploader(),
        "reddit": RedditUploader()
    }
    
    print(f"\n📹 Uploading: {video_path.name}")
    print(f"🎯 Platforms: {', '.join(platforms)}\n")
    
    for platform_name in platforms:
        if platform_name not in uploaders:
            print(f"  [SKIP] {platform_name} - uploader not implemented")
            continue
        
        uploader = uploaders[platform_name]
        print(f"  [{uploader.name}] Uploading...")
        
        try:
            result = uploader.upload(video_path, metadata)
            results[platform_name] = result
            
            if result.get("success"):
                print(f"  [{uploader.name}] ✅ SUCCESS")
                if "url" in result:
                    print(f"    {result['url']}")
            else:
                print(f"  [{uploader.name}] ❌ FAILED: {result.get('error', 'Unknown')}")
        
        except Exception as e:
            print(f"  [{uploader.name}] ❌ ERROR: {e}")
            results[platform_name] = {"success": False, "platform": platform_name, "error": str(e)}
        
        # Rate limiting delay
        time.sleep(5)
    
    return results

def batch_upload_all_platforms(video_count=None, platforms=None):
    """Upload multiple videos to all platforms"""
    
    print("="*80)
    print("  MULTI-PLATFORM BATCH UPLOADER")
    print("="*80 + "\n")
    
    # Get videos
    videos = sorted(VIDEOS_DIR.glob("*.mp4"))
    if not videos:
        print("❌ No videos found in", VIDEOS_DIR)
        return
    
    if video_count:
        videos = videos[:video_count]
    
    if platforms is None:
        platforms = [name for name, config in PLATFORMS.items() if config["enabled"]]
    
    print(f"📹 Videos: {len(videos)}")
    print(f"🎯 Platforms: {', '.join(platforms)}")
    print(f"📤 Total uploads: {len(videos)} × {len(platforms)} = {len(videos) * len(platforms)}\n")
    
    all_results = []
    
    for i, video_path in enumerate(videos, 1):
        print(f"\n[{i}/{len(videos)}] Processing: {video_path.name}")
        print("-" * 80)
        
        metadata = {
            "title": f"Lincoln's Warning #{i}",
            "description": "Abraham Lincoln speaks from death",
            "tags": ["horror", "conspiracy", "lincoln"]
        }
        
        results = upload_to_all_platforms(video_path, metadata, platforms)
        
        all_results.append({
            "video": str(video_path),
            "timestamp": datetime.now().isoformat(),
            "platforms": results
        })
        
        # Save progress
        with open(UPLOAD_LOG, 'w') as f:
            json.dump(all_results, f, indent=2)
    
    # Summary
    print("\n" + "="*80)
    print("  UPLOAD COMPLETE")
    print("="*80 + "\n")
    
    for platform_name in platforms:
        successes = sum(1 for r in all_results if r["platforms"].get(platform_name, {}).get("success"))
        print(f"  {platform_name.upper()}: {successes}/{len(videos)} successful")
    
    print(f"\n📊 Full log saved to: {UPLOAD_LOG}")
    print("\n🔥 EMPIRE EXPANDING ACROSS PLATFORMS! 🔥\n")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', type=int, help='Number of videos to upload')
    parser.add_argument('--platforms', nargs='+', choices=list(PLATFORMS.keys()) + ['all'], 
                        default=['all'], help='Platforms to upload to')
    parser.add_argument('--test', action='store_true', help='Test with 1 video')
    
    args = parser.parse_args()
    
    platforms = None if 'all' in args.platforms else args.platforms
    count = 1 if args.test else args.count
    
    batch_upload_all_platforms(count, platforms)
