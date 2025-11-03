#!/usr/bin/env python3
"""
MULTI_PLATFORM_DEPLOYER.py - Deploy videos to all platforms automatically

Platforms:
1. YouTube (already done)
2. TikTok
3. Instagram Reels
4. Twitter/X
5. Rumble
6. Facebook Reels
7. Reddit

Takes existing YouTube videos and cross-posts to all platforms.
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict

class MultiPlatformDeployer:
    def __init__(self):
        self.base_dir = Path("F:/AI_Oracle_Root/scarify")
        self.video_dir = self.base_dir / "abraham_horror" / "uploaded"
        self.log_file = self.base_dir / "multi_platform_log.json"
    
    def get_recent_videos(self, count=10) -> List[Path]:
        """Get most recent generated videos"""
        videos = sorted(
            self.video_dir.glob("*.mp4"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        return videos[:count]
    
    def deploy_to_tiktok(self, video_path: Path, title: str, hashtags: List[str]):
        """Deploy to TikTok (manual for now)"""
        print(f"\n[TikTok] {video_path.name}")
        print(f"  Title: {title}")
        print(f"  Hashtags: {' '.join(hashtags)}")
        print(f"  Manual upload: https://www.tiktok.com/upload")
        print(f"  File: {video_path}")
        
        return {
            'platform': 'tiktok',
            'status': 'manual_required',
            'video': str(video_path),
            'title': title
        }
    
    def deploy_to_instagram(self, video_path: Path, caption: str):
        """Deploy to Instagram Reels (manual for now)"""
        print(f"\n[Instagram] {video_path.name}")
        print(f"  Caption: {caption[:100]}...")
        print(f"  Manual upload: https://www.instagram.com/")
        print(f"  File: {video_path}")
        
        return {
            'platform': 'instagram',
            'status': 'manual_required',
            'video': str(video_path),
            'caption': caption
        }
    
    def deploy_to_twitter(self, video_path: Path, tweet_text: str):
        """Deploy to Twitter/X (manual for now)"""
        print(f"\n[Twitter/X] {video_path.name}")
        print(f"  Tweet: {tweet_text[:280]}")
        print(f"  Manual upload: https://twitter.com/compose/tweet")
        print(f"  File: {video_path}")
        
        return {
            'platform': 'twitter',
            'status': 'manual_required',
            'video': str(video_path),
            'tweet': tweet_text
        }
    
    def deploy_to_rumble(self, video_path: Path, title: str, description: str):
        """Deploy to Rumble (manual for now)"""
        print(f"\n[Rumble] {video_path.name}")
        print(f"  Title: {title}")
        print(f"  Manual upload: https://rumble.com/upload")
        print(f"  File: {video_path}")
        
        return {
            'platform': 'rumble',
            'status': 'manual_required',
            'video': str(video_path),
            'title': title
        }
    
    def create_deployment_package(self, video_path: Path, youtube_url: str = ""):
        """Create complete deployment package for all platforms"""
        
        # Extract info from filename
        filename = video_path.stem
        
        # Generate platform-specific content
        base_title = "Lincoln's Max Headroom Horror - Dark Political Satire"
        hashtags = ['#Lincoln', '#MaxHeadroom', '#Horror', '#Satire', '#Viral', '#Shorts']
        
        package = {
            'video_path': str(video_path),
            'youtube_url': youtube_url,
            'deployment_time': datetime.now().isoformat(),
            'platforms': {}
        }
        
        # TikTok
        tiktok_hashtags = ['#foryou', '#fyp', '#viral', '#horror', '#lincoln', '#scary', '#glitch']
        package['platforms']['tiktok'] = {
            'title': base_title,
            'hashtags': tiktok_hashtags,
            'upload_url': 'https://www.tiktok.com/upload',
            'status': 'ready'
        }
        
        # Instagram
        instagram_caption = f"{base_title}\n\n" + " ".join(hashtags) + "\n\nCash App: $healthiwealthi"
        package['platforms']['instagram'] = {
            'caption': instagram_caption,
            'upload_url': 'https://www.instagram.com/',
            'status': 'ready'
        }
        
        # Twitter/X
        twitter_text = f"{base_title}\n\nWatch: {youtube_url}\n\n" + " ".join(hashtags[:5])
        package['platforms']['twitter'] = {
            'tweet': twitter_text,
            'upload_url': 'https://twitter.com/compose/tweet',
            'status': 'ready'
        }
        
        # Rumble
        package['platforms']['rumble'] = {
            'title': base_title,
            'description': f"Abraham Lincoln's ghost delivers dark political satire in Max Headroom glitch style.\n\nCash App: https://cash.app/$healthiwealthi/bitcoin/THZmAyn3nx",
            'upload_url': 'https://rumble.com/upload',
            'status': 'ready'
        }
        
        # Facebook
        package['platforms']['facebook'] = {
            'title': base_title,
            'description': instagram_caption,
            'upload_url': 'https://www.facebook.com/',
            'status': 'ready'
        }
        
        return package
    
    def deploy_batch(self, count=10):
        """Deploy batch of recent videos to all platforms"""
        print("="*70)
        print("  MULTI-PLATFORM DEPLOYMENT")
        print("="*70 + "\n")
        
        videos = self.get_recent_videos(count)
        
        print(f"Found {len(videos)} recent videos\n")
        
        deployment_log = []
        
        for i, video in enumerate(videos):
            print(f"\n[{i+1}/{len(videos)}] Processing: {video.name}")
            print("-"*70)
            
            package = self.create_deployment_package(video)
            deployment_log.append(package)
            
            # Display deployment instructions
            print(f"\nVIDEO: {video}")
            print(f"\nPLATFORM DEPLOYMENT:")
            
            for platform, info in package['platforms'].items():
                print(f"\n  {platform.upper()}:")
                print(f"    Upload: {info['upload_url']}")
                if 'title' in info:
                    print(f"    Title: {info['title']}")
                if 'caption' in info:
                    print(f"    Caption: {info['caption'][:80]}...")
                if 'tweet' in info:
                    print(f"    Tweet: {info['tweet'][:80]}...")
        
        # Save deployment log
        self.log_file.write_text(json.dumps(deployment_log, indent=2))
        
        print("\n" + "="*70)
        print("  DEPLOYMENT PACKAGE CREATED")
        print("="*70 + "\n")
        
        print(f"Log saved: {self.log_file}")
        print(f"\nTotal videos: {len(videos)}")
        print(f"Total platforms: 5 per video")
        print(f"Total uploads needed: {len(videos) * 5}\n")
        
        print("MANUAL UPLOAD INSTRUCTIONS:")
        print("  1. Open each platform upload page")
        print("  2. Upload video file")
        print("  3. Use title/caption from log")
        print("  4. Add hashtags")
        print("  5. Publish")
        print(f"\nOR: Use automation tools (Buffer, Hootsuite, etc.)\n")

if __name__ == "__main__":
    deployer = MultiPlatformDeployer()
    deployer.deploy_batch(10)


