#!/usr/bin/env python3
"""
REVENUE_TRACKER_LIVE.py - Real-time revenue monitoring
Tracks YouTube views, donations, and progress toward $3,690 target
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime, timedelta

TARGET = 3690
BATCH_DIR = Path(__file__).parent / "abraham_horror" / "batch_upload"

def get_youtube_stats():
    """Get real YouTube statistics"""
    try:
        import pickle
        from googleapiclient.discovery import build
        
        token = Path("youtube_token.pickle")
        if not token.exists():
            token = Path("abraham_horror/youtube_token.pickle")
        
        if not token.exists():
            return {'views': 0, 'videos': 0, 'likes': 0, 'comments': 0}
        
        with open(token, 'rb') as f:
            creds = pickle.load(f)
        
        youtube = build('youtube', 'v3', credentials=creds)
        
        # Get channel stats
        request = youtube.channels().list(part='statistics', mine=True)
        response = request.execute()
        
        if response['items']:
            stats = response['items'][0]['statistics']
            return {
                'views': int(stats.get('viewCount', 0)),
                'videos': int(stats.get('videoCount', 0)),
                'likes': int(stats.get('likeCount', 0)),
                'comments': int(stats.get('commentCount', 0))
            }
        
        return {'views': 0, 'videos': 0, 'likes': 0, 'comments': 0}
        
    except Exception as e:
        print(f"[ERROR] YouTube API: {e}")
        return {'views': 0, 'videos': 0, 'likes': 0, 'comments': 0}

def estimate_revenue(views, conversion_rate=0.005, avg_donation=5):
    """Estimate revenue from views"""
    donations = int(views * conversion_rate)
    revenue = donations * avg_donation
    return revenue, donations

def calculate_velocity(current_revenue, elapsed_hours, target_hours=48):
    """Calculate revenue velocity"""
    if elapsed_hours == 0:
        return 0
    
    hourly_rate = current_revenue / elapsed_hours
    projected_revenue = hourly_rate * target_hours
    return projected_revenue

def monitor_live(interval_minutes=15):
    """Monitor revenue in real-time"""
    print("\n" + "="*70)
    print("  LIVE REVENUE TRACKER - $3,690 TARGET")
    print("="*70 + "\n")
    
    start_time = datetime.now()
    iteration = 0
    
    while True:
        iteration += 1
        elapsed = (datetime.now() - start_time).total_seconds() / 3600  # hours
        
        print(f"\n[UPDATE #{iteration}] {datetime.now().strftime('%H:%M:%S')}")
        print("-" * 70)
        
        # Get YouTube stats
        stats = get_youtube_stats()
        revenue, donations = estimate_revenue(stats['views'])
        projected = calculate_velocity(revenue, elapsed if elapsed > 0 else 0.01)
        
        # Display stats
        print(f"Videos: {stats['videos']}")
        print(f"Total Views: {stats['views']:,}")
        print(f"Engagement: {stats['likes']} likes, {stats['comments']} comments")
        print(f"\nEstimated Donations: {donations} (at 0.5% conversion)")
        print(f"Current Revenue: ${revenue:,.2f}")
        print(f"\nTarget: ${TARGET:,}")
        print(f"Progress: {revenue/TARGET*100:.1f}%")
        print(f"Remaining: ${TARGET - revenue:,.2f}")
        
        # Velocity analysis
        print(f"\n⚡ VELOCITY ANALYSIS:")
        print(f"   Elapsed: {elapsed:.1f} hours")
        print(f"   Hourly rate: ${revenue/elapsed if elapsed > 0 else 0:.2f}/hr")
        print(f"   48h projection: ${projected:,.2f}")
        
        if projected >= TARGET:
            print(f"   ✅ ON TRACK (${projected - TARGET:,.2f} above target)")
        else:
            shortfall = TARGET - projected
            needed_views = int(shortfall / (0.005 * 5))
            print(f"   ⚠️  BEHIND (need ${shortfall:,.2f} more)")
            print(f"   📈 Need {needed_views:,} more views to hit target")
        
        # Save snapshot
        snapshot = {
            'timestamp': datetime.now().isoformat(),
            'elapsed_hours': elapsed,
            'stats': stats,
            'revenue': revenue,
            'donations': donations,
            'target': TARGET,
            'progress_percent': revenue/TARGET*100,
            'projected_48h': projected,
            'on_track': projected >= TARGET
        }
        
        snapshot_file = BATCH_DIR / f"revenue_snapshot_{iteration}.json"
        with open(snapshot_file, 'w') as f:
            json.dump(snapshot, f, indent=2)
        
        # Wait for next update
        print(f"\n⏰ Next update in {interval_minutes} minutes...")
        print("   (Press Ctrl+C to stop)")
        
        try:
            time.sleep(interval_minutes * 60)
        except KeyboardInterrupt:
            print("\n\n[STOPPED] Revenue tracking ended")
            break
    
    # Final summary
    print("\n" + "="*70)
    print("  FINAL SUMMARY")
    print("="*70 + "\n")
    print(f"Total runtime: {elapsed:.1f} hours")
    print(f"Final revenue: ${revenue:,.2f}")
    print(f"Target progress: {revenue/TARGET*100:.1f}%")
    
    if revenue >= TARGET:
        print("\n🎉 TARGET ACHIEVED!")
    else:
        print(f"\n📊 ${TARGET - revenue:,.2f} remaining")

def quick_check():
    """Quick one-time revenue check"""
    print("\n" + "="*70)
    print("  REVENUE QUICK CHECK - $3,690 TARGET")
    print("="*70 + "\n")
    
    stats = get_youtube_stats()
    revenue, donations = estimate_revenue(stats['views'])
    
    print(f"Videos: {stats['videos']}")
    print(f"Total Views: {stats['views']:,}")
    print(f"Estimated Revenue: ${revenue:,.2f}")
    print(f"\nTarget: ${TARGET:,}")
    print(f"Progress: {revenue/TARGET*100:.1f}%")
    print(f"Remaining: ${TARGET - revenue:,.2f}\n")
    
    if revenue >= TARGET:
        print("✅ TARGET ACHIEVED!")
    else:
        needed_views = int((TARGET - revenue) / (0.005 * 5))
        print(f"Need {needed_views:,} more views\n")
    
    print("="*70 + "\n")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--live', action='store_true', help='Live monitoring mode')
    parser.add_argument('--interval', type=int, default=15, help='Update interval (minutes)')
    
    args = parser.parse_args()
    
    if args.live:
        monitor_live(args.interval)
    else:
        quick_check()

