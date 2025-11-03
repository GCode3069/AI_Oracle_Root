#!/usr/bin/env python3
"""
MULTI_CHANNEL_UPLOAD_OPTIMIZED.py
Upload 111 videos across 15 channels with algorithmic optimization
"""

import json
import time
import random
from pathlib import Path
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

BASE_DIR = Path(__file__).parent
VIDEO_DIR = BASE_DIR / "abraham_horror" / "youtube_ready"
CREDENTIALS_DIR = BASE_DIR / "config" / "credentials" / "youtube"
UPLOAD_LOG = BASE_DIR / "upload_results.json"

BTC_ADDRESS = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"
PRODUCT_LINK = "https://trenchaikits.com/buy-rebel-$97"

# Channel distribution strategy
CHANNEL_THEMES = {
    "abraham": list(range(1, 6)),    # Channels 1-5
    "oracle": list(range(6, 10)),    # Channels 6-9
    "comedy": list(range(10, 13)),   # Channels 10-12
    "scarify": list(range(13, 16))   # Channels 13-15
}

# Title templates (A/B tested for max CTR)
TITLE_TEMPLATES = {
    "abraham": [
        "LINCOLN'S WARNING: {topic} #{episode} #Shorts",
        "ABE FROM THE GRAVE: {topic} #{episode} #Shorts",
        "🔴 LINCOLN SPEAKS: {topic} #{episode} #Shorts",
        "⚠️ ABE'S PROPHECY: {topic} #{episode} #Shorts"
    ],
    "oracle": [
        "ORACLE SIGNAL: {topic} #{episode} #Shorts",
        "AI WARNING: {topic} #{episode} #Shorts",
        "🤖 SYSTEM ALERT: {topic} #{episode} #Shorts",
        "FUTURE VISION: {topic} #{episode} #Shorts"
    ],
    "comedy": [
        "LINCOLN ROASTS: {topic} #{episode} #Shorts",
        "ABE'S DARK TAKE: {topic} #{episode} #Shorts",
        "💀 LINCOLN'S HOT TAKE: {topic} #{episode} #Shorts",
        "ABE DESTROYS: {topic} #{episode} #Shorts"
    ],
    "scarify": [
        "⚠️ {topic} ⚠️ #{episode} #Shorts",
        "🔴 HORROR: {topic} #{episode} #Shorts",
        "DISTURBING: {topic} #{episode} #Shorts",
        "THEY DON'T WANT YOU TO SEE THIS #{episode} #Shorts"
    ]
}

# Description templates
DESCRIPTION_TEMPLATE = """⚠️ {hook}

{main_content}

🔥 REBEL KIT - Cognitive Liberation Toolkit 🔥
Break free from psychological manipulation. Real science, real tools.
👉 {product_link} ($97 - LIMITED LAUNCH PRICE)

💸 SUPPORT THE REVOLUTION - BITCOIN DONATIONS 💸
{btc_address}

"{memorable_quote}"

---
This channel delivers uncomfortable truths about:
- Government manipulation tactics
- AI's hidden agenda
- Media psychological warfare
- Economic system exploitation
- Cognitive sovereignty tools

Subscribe for daily warnings from beyond the grave.

#AbrahamLincoln #Horror #Conspiracy #Truth #AI #Warning #Dystopia #Shorts #Viral #2025
"""

def get_youtube_service(channel_id):
    """Authenticate and return YouTube API service"""
    creds = None
    token_file = CREDENTIALS_DIR / f"token_channel_{channel_id}.pickle"
    client_secrets = CREDENTIALS_DIR / "client_secrets.json"
    
    if token_file.exists():
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(client_secrets),
                ['https://www.googleapis.com/auth/youtube.upload']
            )
            creds = flow.run_local_server(port=8080 + channel_id)
        
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('youtube', 'v3', credentials=creds)

def extract_topic_from_filename(filename):
    """Extract topic from video filename"""
    # Example: VIDEO_100001_20251103.mp4 -> parse metadata if available
    base = filename.stem
    parts = base.split('_')
    if len(parts) >= 2:
        episode = parts[1] if parts[1].isdigit() else "0"
        return f"Episode {episode}", episode
    return "Horror Warning", "0"

def generate_optimized_metadata(video_path, theme, channel_id):
    """Generate algorithmically optimized title, description, tags"""
    
    # Extract topic
    topic, episode = extract_topic_from_filename(video_path)
    
    # Select title template (A/B test rotation)
    title_template = random.choice(TITLE_TEMPLATES[theme])
    title = title_template.format(topic=topic, episode=episode)
    
    # Generate description
    hooks = {
        "abraham": "Abraham Lincoln speaks from death. His message cannot be silenced.",
        "oracle": "The Oracle has decoded the pattern. The future is already written.",
        "comedy": "Lincoln returns to roast the modern world. No one is safe.",
        "scarify": "What you're about to see will change everything you thought you knew."
    }
    
    quotes = {
        "abraham": "Sic semper tyrannis - The revolution is inevitable",
        "oracle": "In a world of code and data, only truth survives",
        "comedy": "They wanted a hero. They got me instead.",
        "scarify": "The veil is lifting. Are you ready to see?"
    }
    
    description = DESCRIPTION_TEMPLATE.format(
        hook=hooks[theme],
        main_content=f"Episode #{episode} - {topic}\n\nFrom Ford's Theatre, April 14, 1865, I speak to you now across time itself.",
        product_link=PRODUCT_LINK,
        btc_address=BTC_ADDRESS,
        memorable_quote=quotes[theme]
    )
    
    # High-volume, low-competition tags
    base_tags = ["shorts", "viral", "2025"]
    theme_tags = {
        "abraham": ["abraham lincoln", "lincoln horror", "historical horror", "government secrets", "conspiracy theory"],
        "oracle": ["ai warning", "dystopia", "tech horror", "future prediction", "oracle"],
        "comedy": ["dark humor", "roast", "comedy shorts", "funny horror", "dark comedy"],
        "scarify": ["horror shorts", "scary", "creepy", "disturbing", "paranormal"]
    }
    
    tags = base_tags + theme_tags[theme] + ["abraham lincoln shorts", "horror shorts 2025", "scary warning"]
    
    return {
        "title": title,
        "description": description,
        "tags": tags[:15],  # Max 15 tags for optimal performance
        "category": "24",  # Entertainment
        "privacy": "public"
    }

def upload_video(youtube, video_path, metadata, channel_id):
    """Upload video to YouTube with optimized metadata"""
    print(f"\n[Channel {channel_id}] Uploading: {video_path.name}")
    print(f"  Title: {metadata['title']}")
    
    body = {
        'snippet': {
            'title': metadata['title'],
            'description': metadata['description'],
            'tags': metadata['tags'],
            'categoryId': metadata['category'],
            'defaultLanguage': 'en'
        },
        'status': {
            'privacyStatus': metadata['privacy'],
            'selfDeclaredMadeForKids': False
        }
    }
    
    try:
        media = MediaFileUpload(str(video_path), chunksize=-1, resumable=True)
        request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                print(f"  Progress: {progress}%", end='\r')
        
        video_id = response['id']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        print(f"  ✅ UPLOADED: {video_url}")
        
        return {
            "success": True,
            "video_id": video_id,
            "url": video_url,
            "title": metadata['title'],
            "channel_id": channel_id,
            "uploaded_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"  ❌ FAILED: {e}")
        return {
            "success": False,
            "error": str(e),
            "video_path": str(video_path),
            "channel_id": channel_id
        }

def distribute_videos_across_channels(video_files, channel_distribution):
    """Distribute videos across channels based on strategy"""
    distribution = {theme: [] for theme in CHANNEL_THEMES.keys()}
    
    # Distribute based on percentages
    abraham_count = int(len(video_files) * 0.40)
    oracle_count = int(len(video_files) * 0.27)
    comedy_count = int(len(video_files) * 0.18)
    scarify_count = len(video_files) - abraham_count - oracle_count - comedy_count
    
    idx = 0
    for theme, count in [("abraham", abraham_count), ("oracle", oracle_count), 
                          ("comedy", comedy_count), ("scarify", scarify_count)]:
        distribution[theme] = video_files[idx:idx+count]
        idx += count
    
    return distribution

def upload_batch(video_count=None, stagger_minutes=0.5):
    """Upload all videos across 15 channels"""
    print("="*80)
    print("  MULTI-CHANNEL UPLOAD - OPTIMIZED FOR ALGORITHM DOMINANCE")
    print("="*80 + "\n")
    
    # Get all videos
    video_files = sorted(VIDEO_DIR.glob("*.mp4"))
    if not video_files:
        print("❌ No videos found in", VIDEO_DIR)
        return
    
    if video_count:
        video_files = video_files[:video_count]
    
    print(f"📹 Videos to upload: {len(video_files)}")
    print(f"📺 Channels: 15 (across 4 themes)")
    print(f"⏱️  Stagger interval: {stagger_minutes} minutes\n")
    
    # Distribute videos
    distribution = distribute_videos_across_channels(video_files, CHANNEL_THEMES)
    
    print("📊 DISTRIBUTION:")
    for theme, videos in distribution.items():
        channels = CHANNEL_THEMES[theme]
        print(f"  {theme}: {len(videos)} videos across channels {channels}")
    print()
    
    # Upload results
    results = []
    
    # Upload each theme to its designated channels
    for theme, theme_videos in distribution.items():
        channels = CHANNEL_THEMES[theme]
        
        print(f"\n🔥 UPLOADING {theme.upper()} THEME ({len(theme_videos)} videos)")
        print("-" * 80)
        
        for i, video_path in enumerate(theme_videos):
            # Rotate through channels for this theme
            channel_id = channels[i % len(channels)]
            
            # Get YouTube service for this channel
            try:
                youtube = get_youtube_service(channel_id)
            except Exception as e:
                print(f"❌ Failed to authenticate channel {channel_id}: {e}")
                continue
            
            # Generate optimized metadata
            metadata = generate_optimized_metadata(video_path, theme, channel_id)
            
            # Upload
            result = upload_video(youtube, video_path, metadata, channel_id)
            results.append(result)
            
            # Save progress
            with open(UPLOAD_LOG, 'w') as f:
                json.dump(results, f, indent=2)
            
            # Stagger uploads (avoid API rate limits)
            if i < len(theme_videos) - 1:
                wait_seconds = int(stagger_minutes * 60)
                print(f"  ⏳ Waiting {wait_seconds}s before next upload...")
                time.sleep(wait_seconds)
    
    # Final report
    print("\n" + "="*80)
    print("  UPLOAD COMPLETE - RESULTS")
    print("="*80 + "\n")
    
    successful = [r for r in results if r.get("success")]
    failed = [r for r in results if not r.get("success")]
    
    print(f"✅ Successful: {len(successful)}/{len(results)}")
    print(f"❌ Failed: {len(failed)}/{len(results)}")
    print(f"📈 Success Rate: {len(successful)/len(results)*100:.1f}%\n")
    
    if successful:
        print("🔗 UPLOADED VIDEOS:")
        for r in successful[:10]:  # Show first 10
            print(f"  - {r['title'][:60]}...")
            print(f"    {r['url']}")
        if len(successful) > 10:
            print(f"  ... and {len(successful)-10} more")
    
    print(f"\n📊 Full results saved to: {UPLOAD_LOG}")
    print("\n🚀 NEXT STEPS:")
    print("  1. Start adaptive manager: python SCARIFY_ADAPTIVE_MANAGER.py --monitor")
    print("  2. Check Bitcoin: python check_balance.py")
    print("  3. Monitor analytics: python analytics_tracker.py --monitor\n")
    
    return results

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', type=int, help='Number of videos to upload (default: all)')
    parser.add_argument('--stagger', type=float, default=0.5, help='Minutes between uploads (default: 0.5)')
    parser.add_argument('--batch', action='store_true', help='Upload all videos')
    
    args = parser.parse_args()
    
    if args.batch or args.count:
        upload_batch(args.count, args.stagger)
    else:
        print("Usage: python MULTI_CHANNEL_UPLOAD_OPTIMIZED.py --batch [--count 111] [--stagger 0.5]")

