#!/usr/bin/env python3
"""
SCARIFY - Analytics Tracker & A/B Testing System
Monitors video performance and optimizes content strategy
"""

import os, sys, json, time, pickle
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

try:
    from googleapiclient.discovery import build
    YOUTUBE_AVAILABLE = True
except ImportError:
    print("[WARNING] YouTube API not available")
    YOUTUBE_AVAILABLE = False

BASE_DIR = Path("F:/AI_Oracle_Root/scarify")
CHANNELS_DIR = BASE_DIR / "channels"
ANALYTICS_DIR = BASE_DIR / "analytics"
ANALYTICS_DIR.mkdir(exist_ok=True)

# Fear types from Chapman 2025
FEAR_TYPES = [
    "corrupt_officials",
    "loved_ones_dying",
    "economic_collapse",
    "cyber_terrorism",
    "russia_nukes"
]

class AnalyticsTracker:
    def __init__(self):
        self.analytics_file = ANALYTICS_DIR / "performance_data.json"
        self.load_data()
    
    def load_data(self):
        """Load existing analytics data"""
        if self.analytics_file.exists():
            with open(self.analytics_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {
                'videos': {},
                'fear_performance': defaultdict(lambda: {
                    'total_views': 0,
                    'total_videos': 0,
                    'avg_retention': 0,
                    'avg_ctr': 0
                }),
                'title_variants': defaultdict(lambda: {
                    'impressions': 0,
                    'clicks': 0,
                    'ctr': 0
                }),
                'last_updated': None
            }
    
    def save_data(self):
        """Save analytics data"""
        self.data['last_updated'] = datetime.now().isoformat()
        with open(self.analytics_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def get_video_stats(self, video_id, channel_num):
        """Fetch stats for a specific video"""
        
        if not YOUTUBE_AVAILABLE:
            return None
        
        # Load channel credentials
        from MULTI_CHANNEL_SETUP import get_channel_credentials
        creds = get_channel_credentials(channel_num)
        
        if not creds:
            return None
        
        try:
            youtube = build('youtube', 'v3', credentials=creds)
            
            # Get video statistics
            request = youtube.videos().list(
                part='statistics,contentDetails',
                id=video_id
            )
            response = request.execute()
            
            if not response['items']:
                return None
            
            item = response['items'][0]
            stats = item['statistics']
            
            return {
                'video_id': video_id,
                'views': int(stats.get('viewCount', 0)),
                'likes': int(stats.get('likeCount', 0)),
                'comments': int(stats.get('commentCount', 0)),
                'duration': item['contentDetails']['duration'],
                'timestamp': datetime.now().isoformat()
            }
        
        except Exception as e:
            print(f"[ERROR] Failed to get stats for {video_id}: {e}")
            return None
    
    def track_video(self, video_id, channel_num, fear_type=None, title_variant=None):
        """Track a video's performance"""
        
        stats = self.get_video_stats(video_id, channel_num)
        
        if not stats:
            return
        
        # Store video data
        self.data['videos'][video_id] = {
            **stats,
            'channel': channel_num,
            'fear_type': fear_type,
            'title_variant': title_variant
        }
        
        # Update fear performance
        if fear_type and fear_type in FEAR_TYPES:
            fear_stats = self.data['fear_performance'][fear_type]
            fear_stats['total_views'] += stats['views']
            fear_stats['total_videos'] += 1
        
        self.save_data()
        
        print(f"[TRACKED] {video_id}: {stats['views']} views")
    
    def get_best_performing_fear(self):
        """Identify which fear type performs best"""
        
        fear_performance = []
        
        for fear_type in FEAR_TYPES:
            stats = self.data['fear_performance'].get(fear_type, {})
            if stats.get('total_videos', 0) > 0:
                avg_views = stats['total_views'] / stats['total_videos']
                fear_performance.append({
                    'fear_type': fear_type,
                    'avg_views': avg_views,
                    'total_videos': stats['total_videos'],
                    'total_views': stats['total_views']
                })
        
        fear_performance.sort(key=lambda x: x['avg_views'], reverse=True)
        
        return fear_performance
    
    def generate_report(self):
        """Generate performance report"""
        
        print(f"\n{'='*70}")
        print(f"SCARIFY ANALYTICS REPORT")
        print(f"{'='*70}\n")
        
        # Overall stats
        total_videos = len(self.data['videos'])
        total_views = sum(v['views'] for v in self.data['videos'].values())
        
        print(f"Total Videos: {total_videos}")
        print(f"Total Views: {total_views:,}")
        if total_videos > 0:
            print(f"Average Views/Video: {total_views/total_videos:,.0f}")
        print()
        
        # Fear type performance
        print(f"FEAR TYPE PERFORMANCE")
        print(f"{'-'*70}")
        
        fear_perf = self.get_best_performing_fear()
        
        for i, fear in enumerate(fear_perf, 1):
            print(f"{i}. {fear['fear_type']}")
            print(f"   Videos: {fear['total_videos']}")
            print(f"   Total Views: {fear['total_views']:,}")
            print(f"   Avg Views: {fear['avg_views']:,.0f}")
            print()
        
        # Recommendations
        print(f"RECOMMENDATIONS")
        print(f"{'-'*70}")
        
        if fear_perf:
            best = fear_perf[0]
            print(f"1. Focus on: {best['fear_type']}")
            print(f"   (Averaging {best['avg_views']:,.0f} views)")
            print()
            
            if len(fear_perf) > 1:
                worst = fear_perf[-1]
                print(f"2. Reduce: {worst['fear_type']}")
                print(f"   (Only {worst['avg_views']:,.0f} views avg)")
                print()
        
        print(f"{'='*70}\n")
        
        # Save report
        report_file = ANALYTICS_DIR / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w') as f:
            f.write(f"SCARIFY ANALYTICS REPORT\n")
            f.write(f"Generated: {datetime.now()}\n\n")
            f.write(f"Total Videos: {total_videos}\n")
            f.write(f"Total Views: {total_views:,}\n\n")
            f.write(f"Fear Type Performance:\n")
            for fear in fear_perf:
                f.write(f"  {fear['fear_type']}: {fear['avg_views']:,.0f} avg views\n")
        
        print(f"Report saved: {report_file}\n")

def scan_and_track_all():
    """Scan all upload results and track performance"""
    
    tracker = AnalyticsTracker()
    
    # Find all upload result files
    result_files = list(BASE_DIR.glob("upload_results_*.json"))
    
    if not result_files:
        print("[WARNING] No upload results found")
        return
    
    print(f"\n{'='*70}")
    print(f"SCANNING UPLOAD RESULTS")
    print(f"{'='*70}\n")
    
    tracked_count = 0
    
    for result_file in result_files:
        with open(result_file, 'r') as f:
            results = json.load(f)
        
        for result in results:
            video_url = result.get('url')
            if not video_url or 'watch?v=' not in video_url:
                continue
            
            video_id = video_url.split('watch?v=')[1].split('&')[0]
            channel_num = result.get('channel')
            
            # Try to get fear type from metadata
            video_file = Path(result.get('video', ''))
            metadata_file = BASE_DIR / "abraham_horror" / "youtube_ready" / video_file.with_suffix('.json').name
            
            fear_type = None
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                    fear_type = metadata.get('fear_type')
            
            tracker.track_video(video_id, channel_num, fear_type)
            tracked_count += 1
            
            time.sleep(1)  # Rate limit
    
    print(f"\n[OK] Tracked {tracked_count} videos")
    
    # Generate report
    tracker.generate_report()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "scan":
            scan_and_track_all()
        elif sys.argv[1] == "report":
            tracker = AnalyticsTracker()
            tracker.generate_report()
    else:
        print("""
SCARIFY ANALYTICS TRACKER

Usage:
  python analytics_tracker.py scan      # Scan all videos and track performance
  python analytics_tracker.py report    # Generate performance report
""")


