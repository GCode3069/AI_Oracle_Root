#!/usr/bin/env python3
"""
🌐 MULTI-PLATFORM DEPLOYER - MAXIMUM REACH
Deploys to ALL platforms simultaneously:
- YouTube (primary)
- TikTok
- Rumble
- X/Twitter
- Instagram Reels
- Snapchat Spotlight
- Facebook Reels
"""
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Platform uploaders
sys.path.insert(0, str(Path(__file__).parent))
try:
    from tiktok_auto_uploader import upload_to_tiktok
except ImportError:
    upload_to_tiktok = None

try:
    from rumble_auto_uploader import upload_to_rumble
except ImportError:
    upload_to_rumble = None

try:
    from abraham_MAX_HEADROOM import upload_to_youtube
except ImportError:
    upload_to_youtube = None

class MultiPlatformDeployer:
    """Deploy videos to all platforms simultaneously"""
    
    def __init__(self):
        self.results = {}
        self.base_dir = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
    
    def deploy_to_all(self, video_path: str, title: str, description: str, 
                     episode_num: int, headline: str) -> Dict:
        """Deploy video to all platforms"""
        print("\n" + "="*70)
        print(f"🌐 MULTI-PLATFORM DEPLOYMENT - Episode #{episode_num}")
        print("="*70)
        
        video_path_obj = Path(video_path)
        if not video_path_obj.exists():
            print(f"[ERROR] Video not found: {video_path}")
            return {}
        
        results = {}
        
        # 1. YouTube (Primary)
        if upload_to_youtube:
            print("\n[1/7] YouTube Upload...")
            try:
                youtube_url = upload_to_youtube(video_path, headline, episode_num)
                results["youtube"] = {"url": youtube_url, "status": "success"}
                print(f"  ✅ {youtube_url}")
            except Exception as e:
                results["youtube"] = {"status": "failed", "error": str(e)}
                print(f"  ❌ {e}")
        else:
            results["youtube"] = {"status": "skipped", "reason": "Module not available"}
        
        # 2. TikTok
        if upload_to_tiktok:
            print("\n[2/7] TikTok Upload...")
            try:
                tiktok_url = upload_to_tiktok(video_path, title, description)
                results["tiktok"] = {"url": tiktok_url, "status": "success"}
                print(f"  ✅ {tiktok_url}")
            except Exception as e:
                results["tiktok"] = {"status": "failed", "error": str(e)}
                print(f"  ❌ {e}")
        else:
            print("\n[2/7] TikTok Upload... (Skipped - API not configured)")
            results["tiktok"] = {"status": "skipped", "reason": "API not configured"}
        
        # 3. Rumble
        if upload_to_rumble:
            print("\n[3/7] Rumble Upload...")
            try:
                rumble_url = upload_to_rumble(video_path, title, description)
                results["rumble"] = {"url": rumble_url, "status": "success"}
                print(f"  ✅ {rumble_url}")
            except Exception as e:
                results["rumble"] = {"status": "failed", "error": str(e)}
                print(f"  ❌ {e}")
        else:
            print("\n[3/7] Rumble Upload... (Skipped - API not configured)")
            results["rumble"] = {"status": "skipped", "reason": "API not configured"}
        
        # 4. X/Twitter (Video Tweet)
        print("\n[4/7] X/Twitter Upload...")
        try:
            twitter_result = self._upload_to_twitter(video_path, title)
            results["twitter"] = twitter_result
            if twitter_result["status"] == "success":
                print(f"  ✅ {twitter_result.get('url', 'Tweet posted')}")
            else:
                print(f"  ⚠️ {twitter_result.get('reason', 'Skipped')}")
        except Exception as e:
            results["twitter"] = {"status": "failed", "error": str(e)}
            print(f"  ❌ {e}")
        
        # 5. Instagram Reels
        print("\n[5/7] Instagram Reels...")
        try:
            instagram_result = self._upload_to_instagram(video_path, title, description)
            results["instagram"] = instagram_result
            if instagram_result["status"] == "success":
                print(f"  ✅ Post uploaded")
            else:
                print(f"  ⚠️ {instagram_result.get('reason', 'Skipped')}")
        except Exception as e:
            results["instagram"] = {"status": "failed", "error": str(e)}
            print(f"  ❌ {e}")
        
        # 6. Snapchat Spotlight
        print("\n[6/7] Snapchat Spotlight...")
        results["snapchat"] = {"status": "skipped", "reason": "Requires Snapchat Ads API"}
        print("  ⚠️ Requires Snapchat Ads API (not configured)")
        
        # 7. Facebook Reels
        print("\n[7/7] Facebook Reels...")
        try:
            facebook_result = self._upload_to_facebook(video_path, title, description)
            results["facebook"] = facebook_result
            if facebook_result["status"] == "success":
                print(f"  ✅ Reel uploaded")
            else:
                print(f"  ⚠️ {facebook_result.get('reason', 'Skipped')}")
        except Exception as e:
            results["facebook"] = {"status": "failed", "error": str(e)}
            print(f"  ❌ {e}")
        
        print("\n" + "="*70)
        print("[DEPLOYMENT SUMMARY]")
        print("="*70)
        
        success_count = sum(1 for r in results.values() if r.get("status") == "success")
        total_count = len(results)
        
        print(f"\n  Success: {success_count}/{total_count} platforms")
        print(f"  Failed: {sum(1 for r in results.values() if r.get('status') == 'failed')}")
        print(f"  Skipped: {sum(1 for r in results.values() if r.get('status') == 'skipped')}")
        
        return results
    
    def _upload_to_twitter(self, video_path: str, title: str) -> Dict:
        """Upload to X/Twitter"""
        # Note: Requires Twitter API v2 with video upload
        # For now, return instructions
        return {
            "status": "skipped",
            "reason": "Requires Twitter API v2 with media upload (not configured)",
            "instructions": "Use Twitter API v2 media upload endpoint",
        }
    
    def _upload_to_instagram(self, video_path: str, title: str, description: str) -> Dict:
        """Upload to Instagram Reels"""
        # Note: Requires Instagram Graph API
        return {
            "status": "skipped",
            "reason": "Requires Instagram Graph API (not configured)",
            "instructions": "Use Instagram Graph API Reels endpoint",
        }
    
    def _upload_to_facebook(self, video_path: str, title: str, description: str) -> Dict:
        """Upload to Facebook Reels"""
        # Note: Requires Facebook Graph API
        return {
            "status": "skipped",
            "reason": "Requires Facebook Graph API (not configured)",
            "instructions": "Use Facebook Graph API Reels endpoint",
        }

def main():
    """Test multi-platform deployment"""
    if len(sys.argv) < 2:
        print("Usage: python MULTI_PLATFORM_DEPLOYER_COMPLETE.py <video_path> [title] [description] [episode_num]")
        sys.exit(1)
    
    video_path = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) > 2 else "Lincoln's WARNING"
    description = sys.argv[3] if len(sys.argv) > 3 else "Abe Lincoln delivers dark comedy warnings"
    episode_num = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    
    deployer = MultiPlatformDeployer()
    results = deployer.deploy_to_all(video_path, title, description, episode_num, title)
    
    print(f"\n[RESULTS SAVED]")
    import json
    results_file = Path("multi_platform_results.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"  {results_file}")

if __name__ == "__main__":
    main()

