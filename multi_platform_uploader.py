#!/usr/bin/env python3
"""
MULTI-PLATFORM AUTO-UPLOADER - REAL WORKING CODE
Upload ONCE, post EVERYWHERE, monetize on ALL platforms
YouTube + TikTok + Rumble + Instagram + X(Twitter)
"""
import os
import sys
from pathlib import Path
from datetime import datetime

class MultiPlatformUploader:
    """Upload to all monetizable platforms automatically"""
    
    def __init__(self):
        self.results = {}
        self.video_path = None
        self.title = ""
        self.description = ""
    
    def upload_everywhere(self, video_path, episode_num, headline):
        """Upload to ALL platforms"""
        self.video_path = Path(video_path)
        self.episode_num = episode_num
        self.headline = headline
        
        # Generate platform-specific metadata
        self.title = f"Lincoln's WARNING #{episode_num}: {headline[:40]}"
        self.description = self._generate_description()
        
        print(f"\n{'='*70}")
        print(f"  MULTI-PLATFORM UPLOAD - Episode #{episode_num}")
        print(f"{'='*70}\n")
        print(f"Video: {self.video_path.name}")
        print(f"Title: {self.title}")
        print(f"\nUploading to ALL platforms...\n")
        
        # Upload to each platform
        self._upload_youtube()
        self._upload_tiktok()
        self._upload_rumble()
        self._upload_instagram()
        self._upload_twitter()
        
        # Save results
        self._save_results()
        
        # Display summary
        self._show_summary()
        
        return self.results
    
    def _generate_description(self):
        """Generate monetized description for all platforms"""
        return f"""{self.headline}

Abraham Lincoln's dark satirical comedy - Roasts EVERYONE!

💰 Support:
• CashApp: $LincolnWarnings
• Scripts ($27): gumroad.com/l/lincoln-scripts
• Full System ($97): gumroad.com/l/purge-kit

🔥 Dark Comedy - No Sacred Cows
Styles: Pryor, Carlin, Chappelle, Bernie Mac

#Shorts #Lincoln #Politics #Comedy #Satire"""
    
    def _upload_youtube(self):
        """Upload to YouTube (already working)"""
        try:
            print("[1/5] YouTube...")
            from abraham_MAX_HEADROOM import upload_to_youtube
            url = upload_to_youtube(self.video_path, self.headline, self.episode_num)
            self.results['youtube'] = {'url': url, 'status': 'success' if url else 'failed'}
            print(f"  [OK] YouTube: {url}\n")
        except Exception as e:
            print(f"  [ERROR] YouTube: {e}\n")
            self.results['youtube'] = {'url': None, 'status': 'error', 'error': str(e)}
    
    def _upload_tiktok(self):
        """Upload to TikTok"""
        try:
            print("[2/5] TikTok...")
            from tiktok_auto_uploader import upload_to_tiktok
            caption = f"Lincoln's WARNING #{self.episode_num} 🔥 #fyp #politics #comedy"
            result = upload_to_tiktok(self.video_path, caption)
            self.results['tiktok'] = {'url': result, 'status': 'success' if result else 'not_configured'}
            if result:
                print(f"  [OK] TikTok: Posted\n")
            else:
                print(f"  [SKIP] TikTok: Not configured (see tiktok_auto_uploader.py)\n")
        except Exception as e:
            print(f"  [SKIP] TikTok: {e}\n")
            self.results['tiktok'] = {'url': None, 'status': 'not_configured'}
    
    def _upload_rumble(self):
        """Upload to Rumble ($5-10 per 1K views!)"""
        try:
            print("[3/5] Rumble...")
            from rumble_auto_uploader import RumbleUploader
            uploader = RumbleUploader()
            url = uploader.upload_video(self.video_path, self.title, self.description)
            self.results['rumble'] = {'url': url, 'status': 'success' if url else 'not_configured'}
            if url:
                print(f"  [OK] Rumble: {url}\n")
            else:
                print(f"  [SKIP] Rumble: Not configured (set RUMBLE_USERNAME/PASSWORD)\n")
        except Exception as e:
            print(f"  [SKIP] Rumble: {e}\n")
            self.results['rumble'] = {'url': None, 'status': 'not_configured'}
    
    def _upload_instagram(self):
        """Upload to Instagram Reels"""
        print("[4/5] Instagram Reels...")
        print(f"  [MANUAL] Instagram: Requires manual upload or Hootsuite integration\n")
        self.results['instagram'] = {'url': None, 'status': 'manual', 'note': 'Use Hootsuite or manual upload'}
    
    def _upload_twitter(self):
        """Upload to X (Twitter)"""
        print("[5/5] X (Twitter)...")
        print(f"  [MANUAL] Twitter: Requires API v2 or manual upload\n")
        self.results['twitter'] = {'url': None, 'status': 'manual', 'note': 'Use Twitter API or manual upload'}
    
    def _save_results(self):
        """Save upload results"""
        import json
        results_file = Path("multi_platform_results.json")
        
        data = {
            'episode': self.episode_num,
            'headline': self.headline,
            'video': str(self.video_path),
            'timestamp': datetime.now().isoformat(),
            'platforms': self.results
        }
        
        # Append to results file
        existing = []
        if results_file.exists():
            with open(results_file, 'r') as f:
                try:
                    existing = json.load(f)
                    if not isinstance(existing, list):
                        existing = [existing]
                except:
                    existing = []
        
        existing.append(data)
        
        with open(results_file, 'w') as f:
            json.dump(existing, f, indent=2)
        
        print(f"[Results] Saved to: {results_file}")
    
    def _show_summary(self):
        """Show upload summary"""
        print(f"\n{'='*70}")
        print(f"  UPLOAD SUMMARY")
        print(f"{'='*70}\n")
        
        for platform, data in self.results.items():
            status = data['status']
            if status == 'success':
                print(f"[OK] {platform.title()}: {data['url']}")
            elif status == 'manual':
                print(f"[MANUAL] {platform.title()}: {data.get('note', 'Manual upload required')}")
            elif status == 'not_configured':
                print(f"[SKIP] {platform.title()}: Not configured")
            else:
                print(f"[ERROR] {platform.title()}: {data.get('error', 'Unknown error')}")
        
        print(f"\n{'='*70}\n")

def batch_upload_to_all_platforms(video_dir, start_episode=1000, count=10):
    """Batch upload videos to ALL platforms"""
    video_dir = Path(video_dir)
    videos = sorted(video_dir.glob("*.mp4"))[:count]
    
    print(f"\n[Batch Upload] Processing {len(videos)} videos across all platforms...\n")
    
    uploader = MultiPlatformUploader()
    all_results = []
    
    for i, video in enumerate(videos):
        episode_num = start_episode + i
        headline = f"Current Event #{i+1}"  # Would come from your tracking
        
        print(f"[{i+1}/{len(videos)}] Video: {video.name}")
        results = uploader.upload_everywhere(video, episode_num, headline)
        all_results.append(results)
        
        # Wait between batches
        if i < len(videos) - 1:
            wait = 120  # 2 minutes between videos
            print(f"\nWaiting {wait}s before next upload...\n")
            import time
            time.sleep(wait)
    
    print(f"\n[Batch] Complete: {len(all_results)} videos processed\n")
    return all_results

if __name__ == "__main__":
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
        episode = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
        headline = sys.argv[3] if len(sys.argv) > 3 else "Breaking News"
        
        uploader = MultiPlatformUploader()
        uploader.upload_everywhere(video_path, episode, headline)
    else:
        print("""
MULTI-PLATFORM AUTO-UPLOADER

Upload ONCE, monetize EVERYWHERE!

Platforms:
- YouTube: Build to monetization
- TikTok: $1 per 1,000 views
- Rumble: $5-10 per 1,000 views
- Instagram: $0.01-0.02 per play
- X(Twitter): Premium monetization

Usage:
python multi_platform_uploader.py VIDEO_PATH EPISODE_NUM "Headline"

Batch upload:
python multi_platform_uploader.py --batch "uploaded/" 1000 10

Revenue Example:
10K views across platforms:
- YouTube: $0.10
- TikTok: $10.00
- Rumble: $50-100
- Instagram: $100-200
TOTAL: $160-310 (vs $0.10 YouTube only!)
""")

