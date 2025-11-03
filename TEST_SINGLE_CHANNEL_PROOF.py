#!/usr/bin/env python3
"""
TEST_SINGLE_CHANNEL_PROOF.py
Proof of concept: Upload 5 videos to 1 channel, validate full pipeline
"""

import json
import time
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
TEST_LOG = BASE_DIR / "test_single_channel_results.json"

BTC_ADDRESS = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"
PRODUCT_LINK = "https://trenchaikits.com/buy-rebel-$97"

def get_youtube_service():
    """Authenticate and return YouTube API service for channel 1"""
    creds = None
    token_file = CREDENTIALS_DIR / "token_channel_1.pickle"
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
            creds = flow.run_local_server(port=8080)
        
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('youtube', 'v3', credentials=creds)

def create_optimized_metadata(video_num):
    """Create metadata for test video"""
    
    title = f"LINCOLN'S WARNING: Test #{video_num} - The Truth They Hide #Shorts"
    
    description = f"""⚠️ Abraham Lincoln speaks from death. Episode #{video_num}

From Ford's Theatre, April 14, 1865, I warn you now.

🔥 REBEL KIT - Cognitive Liberation Toolkit 🔥
Break free from psychological manipulation. Real science, real tools.
👉 {PRODUCT_LINK} ($97 - LIMITED LAUNCH PRICE)

💸 SUPPORT THE REVOLUTION - BITCOIN DONATIONS 💸
{BTC_ADDRESS}

"Sic semper tyrannis - The revolution is inevitable"

---
This is a TEST VIDEO for proof of concept.

#AbrahamLincoln #Horror #Conspiracy #Truth #Warning #Shorts #Viral #2025
"""
    
    tags = [
        "abraham lincoln",
        "horror shorts",
        "conspiracy theory",
        "scary warning",
        "lincoln speaks",
        "shorts",
        "viral",
        "2025",
        "government secrets",
        "truth",
        "creepy"
    ]
    
    return {
        "title": title,
        "description": description,
        "tags": tags,
        "category": "24",  # Entertainment
        "privacy": "public"
    }

def upload_video(youtube, video_path, metadata, video_num):
    """Upload single video and track result"""
    print(f"\n[Video {video_num}/5] Uploading: {video_path.name}")
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
        
        print("  Uploading...", end='', flush=True)
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                print(f"\r  Progress: {progress}%", end='', flush=True)
        
        video_id = response['id']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        print(f"\n  ✅ SUCCESS: {video_url}")
        
        return {
            "success": True,
            "video_id": video_id,
            "url": video_url,
            "title": metadata['title'],
            "uploaded_at": datetime.now().isoformat(),
            "video_path": str(video_path)
        }
        
    except Exception as e:
        print(f"\n  ❌ FAILED: {e}")
        return {
            "success": False,
            "error": str(e),
            "video_path": str(video_path),
            "title": metadata['title']
        }

def run_single_channel_test():
    """Test upload 5 videos to channel 1"""
    print("="*80)
    print("  SINGLE CHANNEL PROOF OF CONCEPT TEST")
    print("="*80 + "\n")
    
    print("Testing: Upload 5 videos to Channel 1")
    print("Purpose: Validate full pipeline before 111-video deployment\n")
    
    # Get 5 videos
    video_files = sorted(VIDEO_DIR.glob("*.mp4"))
    if not video_files:
        print("❌ ERROR: No videos found in", VIDEO_DIR)
        print("\nGenerate videos first:")
        print("  python MASS_GENERATE_100_VIDEOS.py --total 5 --pollo 0")
        return
    
    test_videos = video_files[:5]
    print(f"📹 Found {len(video_files)} total videos")
    print(f"📹 Testing with first 5 videos\n")
    
    # Authenticate
    print("🔐 Authenticating YouTube API...")
    try:
        youtube = get_youtube_service()
        print("  ✅ Authentication successful\n")
    except Exception as e:
        print(f"  ❌ Authentication failed: {e}")
        print("\nMake sure client_secrets.json exists at:")
        print(f"  {CREDENTIALS_DIR / 'client_secrets.json'}")
        return
    
    # Upload videos
    print("🚀 Starting uploads...\n")
    print("-" * 80)
    
    results = []
    start_time = time.time()
    
    for i, video_path in enumerate(test_videos, 1):
        metadata = create_optimized_metadata(i)
        result = upload_video(youtube, video_path, metadata, i)
        results.append(result)
        
        # Save progress
        with open(TEST_LOG, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Wait between uploads (avoid rate limiting)
        if i < len(test_videos):
            print("\n  ⏳ Waiting 30 seconds before next upload...")
            time.sleep(30)
    
    elapsed = time.time() - start_time
    
    # Results
    print("\n" + "="*80)
    print("  TEST RESULTS")
    print("="*80 + "\n")
    
    successful = [r for r in results if r.get("success")]
    failed = [r for r in results if not r.get("success")]
    
    print(f"✅ Successful: {len(successful)}/5")
    print(f"❌ Failed: {len(failed)}/5")
    print(f"⏱️  Time elapsed: {elapsed/60:.1f} minutes")
    print(f"⚡ Average: {elapsed/len(results):.1f} seconds per video\n")
    
    if successful:
        print("🔗 UPLOADED VIDEOS:")
        for r in successful:
            print(f"  - {r['title']}")
            print(f"    {r['url']}")
        print()
    
    if failed:
        print("❌ FAILED UPLOADS:")
        for r in failed:
            print(f"  - {r['title']}")
            print(f"    Error: {r.get('error', 'Unknown')}")
        print()
    
    # Projections
    print("📊 PROJECTIONS FOR FULL DEPLOYMENT:")
    if len(successful) == 5:
        print("  ✅ 100% success rate")
        print(f"  ⏱️  111 videos × {elapsed/5:.1f}s = {(111*elapsed/5)/60:.1f} minutes")
        print(f"  📺 15 channels × 111 videos = 1,665 total uploads")
        print(f"  ⏱️  Estimated total time: {(1665*elapsed/5)/3600:.1f} hours\n")
    else:
        success_rate = len(successful) / 5
        print(f"  ⚠️  {success_rate*100:.0f}% success rate")
        print(f"  ⏱️  Expected successful uploads: {int(111 * success_rate)}")
        print(f"  ⚠️  May need to fix errors before full deployment\n")
    
    # Next steps
    print("="*80)
    print("  NEXT STEPS")
    print("="*80 + "\n")
    
    if len(successful) >= 4:  # 80%+ success
        print("✅ TEST PASSED - Ready for full deployment!\n")
        print("Execute full deployment:")
        print("  python MULTI_CHANNEL_UPLOAD_OPTIMIZED.py --batch --count 111\n")
        print("Or gradual rollout:")
        print("  python MULTI_CHANNEL_UPLOAD_OPTIMIZED.py --count 20  # Start with 20")
        print("  python SCARIFY_ADAPTIVE_MANAGER.py --monitor  # Monitor performance")
        print("  # Then scale up based on results\n")
    else:
        print("⚠️  TEST NEEDS IMPROVEMENT\n")
        print("Issues to fix:")
        if failed:
            for r in failed:
                print(f"  - {r.get('error', 'Unknown error')}")
        print("\nFix issues, then re-run:")
        print("  python TEST_SINGLE_CHANNEL_PROOF.py\n")
    
    print(f"📁 Full results saved to: {TEST_LOG}")
    print("\n" + "="*80 + "\n")
    
    return results

if __name__ == "__main__":
    results = run_single_channel_test()
    
    # Summary
    if results:
        success_count = len([r for r in results if r.get("success")])
        if success_count == 5:
            print("🎉 PERFECT TEST - ALL 5 VIDEOS UPLOADED!")
            print("💰 Pipeline validated. Ready to print money. 🔥")
        elif success_count >= 3:
            print(f"✅ {success_count}/5 successful - Good enough to proceed")
            print("⚠️  Monitor first batch for issues")
        else:
            print("❌ Too many failures - Fix issues before full deployment")

