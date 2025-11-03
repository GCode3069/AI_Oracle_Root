#!/usr/bin/env python3
"""
SCARIFY - MULTI-CHANNEL UPLOADER
Distributes videos across 15 YouTube channels with rotation and A/B testing
"""

import os, sys, json, pickle, random, time
from pathlib import Path
from datetime import datetime

try:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from google.auth.transport.requests import Request
    YOUTUBE_AVAILABLE = True
except ImportError:
    print("[ERROR] YouTube API not available")
    YOUTUBE_AVAILABLE = False

BASE_DIR = Path("F:/AI_Oracle_Root/scarify")
CHANNELS_DIR = BASE_DIR / "channels"

BTC_ADDRESS = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"
PRODUCT_LINK = "https://trenchaikits.com/buy-rebel-$97"

# Title variations for A/B testing
TITLE_TEMPLATES = [
    "{headline} - Lincoln's Warning",
    "Abraham Lincoln: {headline}",
    "{headline} | Ford's Theatre Truth",
    "Lincoln Speaks: {headline}",
    "{headline} - The President's Ghost"
]

# Description template with BTC and product
DESC_TEMPLATE = """{script}

💰 SUPPORT TRUTH: {btc}
🔥 REBEL KIT: {product}

#AbrahamLincoln #Truth #Horror #Shorts"""

def load_channel_credentials(channel_num):
    """Load credentials for a specific channel"""
    from MULTI_CHANNEL_SETUP import get_channel_credentials
    return get_channel_credentials(channel_num)

def upload_to_channel(video_path, metadata, channel_num, test_mode=False):
    """Upload video to a specific channel"""
    
    if not YOUTUBE_AVAILABLE:
        print(f"[{channel_num}] YouTube API not available")
        return None
    
    # Load credentials
    creds = load_channel_credentials(channel_num)
    if not creds:
        print(f"[{channel_num}] No credentials found")
        return None
    
    # Build YouTube service
    youtube = build('youtube', 'v3', credentials=creds)
    
    # Prepare metadata
    title = metadata.get('title', 'Lincoln Horror Short')
    description = metadata.get('description', DESC_TEMPLATE).format(
        script=metadata.get('script', ''),
        btc=BTC_ADDRESS,
        product=PRODUCT_LINK
    )
    tags = metadata.get('tags', ['abraham lincoln', 'horror', 'shorts', 'truth'])
    
    print(f"\n[Channel {channel_num}] Uploading...")
    print(f"  Title: {title[:50]}...")
    print(f"  File: {Path(video_path).name}")
    
    if test_mode:
        print(f"  [TEST MODE] Would upload to channel {channel_num}")
        return f"TEST_UPLOAD_{channel_num}"
    
    try:
        # Upload video
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': '24'  # Entertainment
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
            }
        }
        
        media = MediaFileUpload(
            video_path,
            chunksize=1024*1024,
            resumable=True
        )
        
        request = youtube.videos().insert(
            part='snippet,status',
            body=body,
            media_body=media
        )
        
        response = None
        last_progress = 0
        
        while response is None:
            status, response = request.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                if progress != last_progress and progress % 10 == 0:
                    print(f"  Progress: {progress}%")
                    last_progress = progress
        
        video_id = response['id']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        print(f"  [SUCCESS] {video_url}")
        
        # Update channel config
        update_channel_stats(channel_num, video_id)
        
        return video_url
        
    except Exception as e:
        print(f"  [ERROR] {e}")
        return None

def update_channel_stats(channel_num, video_id):
    """Update channel statistics after upload"""
    config_file = CHANNELS_DIR / f"channel_{channel_num}_config.json"
    
    if not config_file.exists():
        return
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    config['upload_count'] = config.get('upload_count', 0) + 1
    config['last_upload'] = datetime.now().isoformat()
    config['last_video_id'] = video_id
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

def distribute_videos(video_dir, mode='round-robin', test_mode=False):
    """Distribute videos across channels"""
    
    # Load channels
    master_file = CHANNELS_DIR / "channels_master.json"
    if not master_file.exists():
        print("[ERROR] No channels configured. Run MULTI_CHANNEL_SETUP.py first")
        return
    
    with open(master_file, 'r') as f:
        data = json.load(f)
    
    channels = data.get('channels', [])
    if not channels:
        print("[ERROR] No channels available")
        return
    
    # Get videos
    video_path = Path(video_dir)
    videos = list(video_path.glob("*.mp4"))
    
    if not videos:
        print(f"[ERROR] No videos found in {video_dir}")
        return
    
    print(f"\n{'='*70}")
    print(f"SCARIFY MULTI-CHANNEL DISTRIBUTION")
    print(f"{'='*70}")
    print(f"Videos: {len(videos)}")
    print(f"Channels: {len(channels)}")
    print(f"Mode: {mode}")
    print(f"Test Mode: {test_mode}")
    print(f"{'='*70}\n")
    
    results = []
    
    if mode == 'round-robin':
        # Distribute evenly across channels
        for i, video in enumerate(videos):
            channel = channels[i % len(channels)]
            channel_num = channel['channel_number']
            
            # Load metadata if exists
            metadata_file = video.with_suffix('.json')
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
            else:
                # Generate default metadata
                metadata = {
                    'title': f"Lincoln Horror #{i+1}",
                    'script': 'Abraham Lincoln speaks truth from beyond',
                    'tags': ['lincoln', 'horror', 'shorts']
                }
            
            # A/B test: randomize title format
            if 'headline' in metadata:
                template = random.choice(TITLE_TEMPLATES)
                metadata['title'] = template.format(headline=metadata['headline'])
            
            # Upload
            url = upload_to_channel(str(video), metadata, channel_num, test_mode)
            
            if url:
                results.append({
                    'video': video.name,
                    'channel': channel_num,
                    'url': url
                })
            
            # Stagger uploads
            if not test_mode and i < len(videos) - 1:
                delay = random.randint(60, 180)  # 1-3 minutes
                print(f"\n  Waiting {delay}s before next upload...")
                time.sleep(delay)
    
    elif mode == 'random':
        # Random distribution
        for video in videos:
            channel = random.choice(channels)
            channel_num = channel['channel_number']
            
            # Similar upload process...
            url = upload_to_channel(str(video), {}, channel_num, test_mode)
            
            if url:
                results.append({
                    'video': video.name,
                    'channel': channel_num,
                    'url': url
                })
    
    # Save results
    results_file = BASE_DIR / f"upload_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"DISTRIBUTION COMPLETE")
    print(f"{'='*70}")
    print(f"Uploaded: {len(results)}/{len(videos)}")
    print(f"Results: {results_file}")
    print(f"{'='*70}\n")
    
    for r in results:
        print(f"[{r['channel']}] {r['video']}: {r['url']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""
SCARIFY MULTI-CHANNEL UPLOADER

Usage:
  python MULTI_CHANNEL_UPLOADER.py <video_dir> [mode] [--test]
  
Modes:
  round-robin - Distribute evenly (default)
  random      - Random distribution
  
Example:
  python MULTI_CHANNEL_UPLOADER.py abraham_horror/youtube_ready round-robin
  python MULTI_CHANNEL_UPLOADER.py abraham_horror/videos random --test
""")
    else:
        video_dir = sys.argv[1]
        mode = sys.argv[2] if len(sys.argv) > 2 else 'round-robin'
        test_mode = '--test' in sys.argv
        
        distribute_videos(video_dir, mode, test_mode)


