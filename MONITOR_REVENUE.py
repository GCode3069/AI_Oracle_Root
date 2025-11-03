#!/usr/bin/env python3
"""Monitor revenue progress toward $3,690 target"""
import sys, json, time
from pathlib import Path
from datetime import datetime

TARGET = 3690

def check_youtube_views():
    """Get total views from all videos"""
    try:
        import pickle
        from googleapiclient.discovery import build
        
        token = Path("youtube_token.pickle")
        if not token.exists():
            token = Path("abraham_horror/youtube_token.pickle")
        
        with open(token, 'rb') as f:
            creds = pickle.load(f)
        
        youtube = build('youtube', 'v3', credentials=creds)
        
        # Get channel's videos
        request = youtube.channels().list(part='contentDetails', mine=True)
        response = request.execute()
        
        uploads_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        
        # Get all video IDs
        videos_request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=uploads_id,
            maxResults=50
        )
        videos_response = videos_request.execute()
        
        video_ids = [item['contentDetails']['videoId'] for item in videos_response['items']]
        
        # Get statistics
        stats_request = youtube.videos().list(
            part='statistics',
            id=','.join(video_ids)
        )
        stats_response = stats_request.execute()
        
        total_views = sum(int(item['statistics'].get('viewCount', 0)) for item in stats_response['items'])
        
        return total_views, len(video_ids)
        
    except Exception as e:
        print(f"YouTube API error: {e}")
        return 0, 0

def estimate_revenue(views, conversion_rate=0.005):
    """Estimate revenue from views"""
    donations = int(views * conversion_rate)
    revenue = donations * 5  # $5 average
    return revenue, donations

def monitor():
    """Monitor revenue progress"""
    print("\n" + "="*70)
    print("  REVENUE MONITOR - $3,690 TARGET")
    print("="*70 + "\n")
    
    views, video_count = check_youtube_views()
    revenue, donations = estimate_revenue(views)
    
    print(f"Videos: {video_count}")
    print(f"Total Views: {views:,}")
    print(f"Estimated Donations: {donations} (at 0.5% conversion)")
    print(f"Estimated Revenue: ${revenue:,}")
    print(f"\nTarget: ${TARGET:,}")
    print(f"Progress: {revenue/TARGET*100:.1f}%")
    print(f"Remaining: ${TARGET - revenue:,}\n")
    
    if revenue >= TARGET:
        print("✅ TARGET ACHIEVED!")
    else:
        needed_views = int((TARGET - revenue) / 5 / 0.005)
        print(f"Need {needed_views:,} more views to hit target\n")
    
    # Save status
    status = {
        'timestamp': datetime.now().isoformat(),
        'views': views,
        'videos': video_count,
        'revenue': revenue,
        'target': TARGET,
        'progress': revenue/TARGET*100
    }
    
    with open('revenue_status.json', 'w') as f:
        json.dump(status, f, indent=2)
    
    print("="*70 + "\n")

if __name__ == "__main__":
    monitor()


