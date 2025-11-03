#!/usr/bin/env python3
"""
CROSS-PLATFORM POSTER
Automatically posts videos to YouTube, TikTok, Instagram, X (Twitter)
"""
import os, sys, json, time
from pathlib import Path
from datetime import datetime

BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")

class CrossPlatformPoster:
    """Post videos across all platforms"""
    
    def __init__(self):
        self.platforms = {
            'youtube': {'enabled': True, 'path': BASE / 'youtube_ready'},
            'tiktok': {'enabled': False, 'path': BASE / 'tiktok_ready'},  # Requires TikTok API
            'instagram': {'enabled': False, 'path': BASE / 'instagram_ready'},  # Requires Instagram API
            'twitter': {'enabled': False, 'path': BASE / 'youtube_ready'}  # Requires Twitter API
        }
    
    def post_to_youtube(self, video_path, metadata):
        """Post to YouTube (already handled by VIRAL_OPTIMIZED_GENERATOR)"""
        print(f"  ✅ YouTube: Upload handled by generator")
        return True
    
    def prepare_for_tiktok(self, video_path):
        """Prepare video metadata for TikTok"""
        # TikTok specific formatting
        metadata = {
            'title': '',  # TikTok doesn't use titles
            'hashtags': '#abrahamlincoln #halloween2025 #horror #scary #fyp #viral',
            'description': 'Lincoln speaks from beyond the grave... Watch until the end! 🔥',
            'privacy': 'public'
        }
        return metadata
    
    def prepare_for_instagram(self, video_path):
        """Prepare video metadata for Instagram Reels"""
        metadata = {
            'caption': '⚠️ Lincoln\'s Warning from 1865... The prophecy that came true 🔥 #abrahamlincoln #horror #reels #viral',
            'hashtags': '#abrahamlincoln #halloween2025 #horror #scary #reels #viral',
            'privacy': 'public'
        }
        return metadata
    
    def prepare_for_twitter(self, video_path):
        """Prepare video metadata for Twitter/X"""
        metadata = {
            'text': '⚠️ LINCOLN\'S WARNING FROM BEYOND THE GRAVE ⚠️\n\nThe prophecy that came true... Watch until the end 🔥\n\n#AbrahamLincoln #Horror #Truth',
            'hashtags': ['AbrahamLincoln', 'Horror', 'Truth', 'Warning']
        }
        return metadata
    
    def batch_post(self, platform='all'):
        """Batch post videos to platforms"""
        print(f"\n{'='*70}")
        print(f"🌐 CROSS-PLATFORM POSTING")
        print(f"{'='*70}\n")
        
        if platform == 'all':
            platforms_to_use = ['youtube']
        else:
            platforms_to_use = [platform]
        
        for platform_name in platforms_to_use:
            if not self.platforms[platform_name]['enabled']:
                print(f"  ⚠️  {platform_name}: Not enabled (API not configured)")
                continue
            
            folder = self.platforms[platform_name]['path']
            if not folder.exists():
                print(f"  ⚠️  {platform_name}: No videos in {folder}")
                continue
            
            videos = list(folder.glob("*.mp4"))
            if not videos:
                print(f"  ⚠️  {platform_name}: No videos found")
                continue
            
            print(f"  📺 {platform_name.upper()}: {len(videos)} video(s) ready")
            print(f"     Location: {folder}")
            
            for video in videos[:5]:  # Limit to 5 for testing
                print(f"     • {video.name}")

if __name__ == "__main__":
    poster = CrossPlatformPoster()
    poster.batch_post()







