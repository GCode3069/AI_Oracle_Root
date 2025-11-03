#!/usr/bin/env python3
"""
DEPLOY_ALL_PLATFORMS.py - Upload videos to YouTube, TikTok, Instagram
Real multi-platform deployment with authentication
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
import random

BASE_DIR = Path(__file__).parent / "abraham_horror"
BATCH_DIR = BASE_DIR / "batch_upload"

def upload_to_youtube(video_path, metadata):
    """Upload video to YouTube with metadata"""
    try:
        import pickle
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        
        # Load credentials
        token = Path("youtube_token.pickle")
        if not token.exists():
            token = BASE_DIR / "youtube_token.pickle"
        
        if not token.exists():
            print("  [SKIP] YouTube token not found - run youtube_auth.py first")
            return None
        
        with open(token, 'rb') as f:
            creds = pickle.load(f)
        
        youtube = build('youtube', 'v3', credentials=creds)
        
        # Prepare metadata
        is_short = metadata['format'] == 'short'
        title = metadata['title']
        description = f"{metadata['script']}\n\n"
        description += "🎯 PSYCHOLOGICAL AUDIO LAYERS:\n"
        description += "• Theta waves (6Hz) - Deep focus\n"
        description += "• Gamma waves (40Hz) - Peak awareness\n"
        description += "• Binaural beats (8Hz) - Alpha state\n"
        description += "• Subliminal affirmations (17Hz)\n\n"
        description += "💰 Support via CashApp: $GCode3069\n"
        description += "₿ Bitcoin: bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh\n\n"
        description += f"Tags: {', '.join(metadata['tags'][:10])}"
        
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': metadata['tags'],
                'categoryId': '22'  # People & Blogs
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
            }
        }
        
        # Upload
        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
        request = youtube.videos().insert(
            part='snippet,status',
            body=body,
            media_body=media
        )
        
        print(f"  [UPLOADING] {Path(video_path).name}...")
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"  [PROGRESS] {int(status.progress() * 100)}%")
        
        video_id = response['id']
        video_url = f"https://youtube.com/watch?v={video_id}"
        
        print(f"  [SUCCESS] YouTube: {video_url}")
        return video_url
        
    except Exception as e:
        print(f"  [ERROR] YouTube upload failed: {e}")
        return None

def upload_to_tiktok(video_path, metadata):
    """Upload to TikTok (manual process - generates instructions)"""
    print(f"  [MANUAL] TikTok upload required:")
    print(f"    1. Open TikTok Creator Studio")
    print(f"    2. Upload: {video_path}")
    print(f"    3. Title: {metadata['title'][:100]}")
    print(f"    4. Description: {metadata['script'][:150]}")
    print(f"    5. Hashtags: {' '.join(metadata['tags'][:5])}")
    return "MANUAL_UPLOAD_REQUIRED"

def upload_to_instagram(video_path, metadata):
    """Upload to Instagram (manual process - generates instructions)"""
    print(f"  [MANUAL] Instagram Reel upload required:")
    print(f"    1. Open Instagram app")
    print(f"    2. Create new Reel")
    print(f"    3. Upload: {video_path}")
    print(f"    4. Caption: {metadata['script'][:200]}")
    print(f"    5. Hashtags: {' '.join(metadata['tags'][:10])}")
    return "MANUAL_UPLOAD_REQUIRED"

def schedule_posts(video_count, platforms=['youtube', 'tiktok', 'instagram']):
    """Generate posting schedule for phantom timing"""
    schedule = []
    now = datetime.now()
    
    for i in range(video_count):
        # Random delay between 2-12 hours
        delay_hours = random.uniform(2, 12)
        post_time = now + timedelta(hours=delay_hours * (i + 1) / video_count * 48)
        
        schedule.append({
            'video_index': i,
            'post_time': post_time.isoformat(),
            'platforms': platforms.copy()
        })
    
    return schedule

def deploy_all():
    """Deploy all videos to all platforms"""
    print("\n" + "="*70)
    print("  MULTI-PLATFORM DEPLOYMENT - YOUTUBE/TIKTOK/INSTAGRAM")
    print("="*70 + "\n")
    
    # Find all videos
    videos = sorted(BATCH_DIR.glob("VIDEO_*.mp4"))
    
    if not videos:
        print("[ERROR] No videos found in batch_upload directory")
        return
    
    print(f"Found {len(videos)} videos to deploy\n")
    
    # Load metadata
    metadata_files = {v.stem: BATCH_DIR / f"{v.stem}.json" for v in videos}
    
    # Generate schedule
    schedule = schedule_posts(len(videos))
    schedule_file = BATCH_DIR / "deployment_schedule.json"
    with open(schedule_file, 'w') as f:
        json.dump(schedule, f, indent=2)
    print(f"[SCHEDULE] Created posting schedule: {schedule_file}\n")
    
    # Deploy to YouTube (automated)
    print("[YOUTUBE] Starting automated uploads...\n")
    youtube_results = []
    
    for i, video in enumerate(videos[:10]):  # Upload first 10 to YouTube
        print(f"[{i+1}/{min(10, len(videos))}] {video.name}")
        
        # Load metadata
        meta_file = metadata_files[video.stem]
        if not meta_file.exists():
            print(f"  [SKIP] No metadata found")
            continue
        
        with open(meta_file, 'r') as f:
            metadata = json.load(f)
        
        # Upload to YouTube
        url = upload_to_youtube(video, metadata)
        if url:
            youtube_results.append({
                'video': video.name,
                'url': url,
                'uploaded': datetime.now().isoformat()
            })
        
        # Rate limiting
        if i < min(10, len(videos)) - 1:
            print("  [WAIT] 60s cooldown...")
            time.sleep(60)
    
    # Save YouTube results
    youtube_log = BATCH_DIR / "youtube_uploads.json"
    with open(youtube_log, 'w') as f:
        json.dump(youtube_results, f, indent=2)
    
    print(f"\n[YOUTUBE] Uploaded {len(youtube_results)} videos")
    print(f"[YOUTUBE] Log saved: {youtube_log}\n")
    
    # TikTok instructions
    print("="*70)
    print("[TIKTOK] MANUAL UPLOAD INSTRUCTIONS")
    print("="*70 + "\n")
    print("1. Go to TikTok Creator Studio: https://www.tiktok.com/creator-tools/upload")
    print("2. Upload videos in batches of 10")
    print("3. Use metadata from .json files")
    print("4. Schedule posts using deployment_schedule.json\n")
    
    # Instagram instructions
    print("="*70)
    print("[INSTAGRAM] MANUAL UPLOAD INSTRUCTIONS")
    print("="*70 + "\n")
    print("1. Open Instagram app on mobile")
    print("2. Create Reels from batch_upload directory")
    print("3. Use metadata from .json files")
    print("4. Schedule posts using Buffer/Later\n")
    
    print("="*70)
    print(f"  DEPLOYMENT STATUS")
    print("="*70 + "\n")
    print(f"✅ YouTube: {len(youtube_results)} uploaded")
    print(f"⏳ TikTok: {len(videos)} ready (manual)")
    print(f"⏳ Instagram: {len(videos)} ready (manual)")
    print(f"\nTotal reach potential: {len(videos) * 3} posts across 3 platforms\n")
    
    # Revenue projection
    print("="*70)
    print("  REVENUE PROJECTION (48 HOURS)")
    print("="*70 + "\n")
    
    total_posts = len(videos) * 3  # 3 platforms
    avg_views_per_post = 5000  # Conservative
    total_views = total_posts * avg_views_per_post
    conversion_rate = 0.005  # 0.5%
    avg_donation = 5
    
    estimated_revenue = total_views * conversion_rate * avg_donation
    
    print(f"Total posts: {total_posts}")
    print(f"Estimated views: {total_views:,}")
    print(f"Conversion rate: {conversion_rate*100}%")
    print(f"Average donation: ${avg_donation}")
    print(f"\n💰 ESTIMATED REVENUE: ${estimated_revenue:,.2f}")
    print(f"🎯 TARGET: $3,690.00")
    print(f"📊 PROGRESS: {estimated_revenue/3690*100:.1f}%\n")
    
    if estimated_revenue >= 3690:
        print("✅ PROJECTION: TARGET ACHIEVABLE!")
    else:
        needed = 3690 - estimated_revenue
        print(f"⚠️  SHORTFALL: ${needed:,.2f}")
        print(f"   Need {int(needed / (conversion_rate * avg_donation)):,} more views\n")
    
    print("="*70 + "\n")
    
    return {
        'youtube': len(youtube_results),
        'tiktok': len(videos),
        'instagram': len(videos),
        'total_posts': total_posts,
        'estimated_revenue': estimated_revenue
    }

if __name__ == "__main__":
    deploy_all()
