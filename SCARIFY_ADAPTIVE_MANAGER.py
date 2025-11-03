#!/usr/bin/env python3
"""
SCARIFY ADAPTIVE MANAGER - Real-time strategy adaptation
Monitors performance, identifies winners, auto-pivots to maximize revenue
"""

import json
import time
import requests
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import statistics

# CONFIG
BASE_DIR = Path(__file__).parent
ANALYTICS_FILE = BASE_DIR / "analytics_realtime.json"
STRATEGY_FILE = BASE_DIR / "active_strategy.json"
PERFORMANCE_LOG = BASE_DIR / "performance_history.json"

# YouTube Data API
YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY_HERE"  # Get from Google Cloud Console

# Thresholds
VIRAL_THRESHOLD = 10000  # Views in first hour = viral
UNDERPERFORM_THRESHOLD = 100  # Views in first hour = underperforming
HIGH_ENGAGEMENT_RATE = 0.05  # 5% likes+comments/views
MIN_RETENTION = 0.70  # 70% average view duration

# Strategy parameters
STRATEGIES = {
    "abraham_horror": {
        "title_format": "LINCOLN'S WARNING: {topic} #{episode} #Shorts",
        "voice_id": "VR6AewLTigWG4xSOukaG",
        "theme": "abraham",
        "tags": ["abraham lincoln", "horror", "warning", "conspiracy", "scary"],
        "upload_times": [18, 19, 20],  # 6-8 PM EST
    },
    "oracle_tech": {
        "title_format": "ORACLE SIGNAL: {topic} #{episode} #Shorts",
        "voice_id": "EXAVITQu4vr4xnSDxMaL",
        "theme": "oracle",
        "tags": ["ai warning", "tech horror", "future", "oracle", "dystopia"],
        "upload_times": [19, 20, 21],
    },
    "dark_comedy": {
        "title_format": "{topic} - Lincoln Roasts #{episode} #Shorts",
        "voice_id": "AZnzlk1XvdvUeBnXmlld",
        "theme": "comedy",
        "tags": ["dark humor", "roast", "comedy", "lincoln", "funny"],
        "upload_times": [20, 21, 22],
    },
    "pure_horror": {
        "title_format": "⚠️ {topic} ⚠️ #{episode} #Shorts",
        "voice_id": "pNInz6obpgDQGcFmaJgB",
        "theme": "scarify",
        "tags": ["horror", "scary", "creepy", "disturbing", "paranormal"],
        "upload_times": [21, 22, 23],
    }
}

class AdaptiveManager:
    def __init__(self):
        self.analytics = self.load_analytics()
        self.active_strategy = self.load_strategy()
        self.performance_history = self.load_performance_history()
        
    def load_analytics(self):
        if ANALYTICS_FILE.exists():
            with open(ANALYTICS_FILE, 'r') as f:
                return json.load(f)
        return {"videos": [], "channels": {}}
    
    def save_analytics(self):
        with open(ANALYTICS_FILE, 'w') as f:
            json.dump(self.analytics, f, indent=2)
    
    def load_strategy(self):
        if STRATEGY_FILE.exists():
            with open(STRATEGY_FILE, 'r') as f:
                return json.load(f)
        # Default strategy distribution
        return {
            "abraham_horror": 0.40,
            "oracle_tech": 0.30,
            "dark_comedy": 0.20,
            "pure_horror": 0.10
        }
    
    def save_strategy(self):
        with open(STRATEGY_FILE, 'w') as f:
            json.dump(self.active_strategy, f, indent=2)
    
    def load_performance_history(self):
        if PERFORMANCE_LOG.exists():
            with open(PERFORMANCE_LOG, 'r') as f:
                return json.load(f)
        return {"checks": []}
    
    def save_performance_history(self):
        with open(PERFORMANCE_LOG, 'w') as f:
            json.dump(self.performance_history, f, indent=2)
    
    def fetch_video_stats(self, video_id):
        """Fetch real-time stats from YouTube Data API"""
        url = f"https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part": "statistics,contentDetails",
            "id": video_id,
            "key": YOUTUBE_API_KEY
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if "items" in data and len(data["items"]) > 0:
                stats = data["items"][0]["statistics"]
                return {
                    "views": int(stats.get("viewCount", 0)),
                    "likes": int(stats.get("likeCount", 0)),
                    "comments": int(stats.get("commentCount", 0)),
                    "favorites": int(stats.get("favoriteCount", 0))
                }
        except Exception as e:
            print(f"[ERROR] Failed to fetch stats for {video_id}: {e}")
        
        return None
    
    def calculate_engagement_rate(self, stats):
        """Calculate engagement rate (likes + comments) / views"""
        if stats["views"] == 0:
            return 0
        return (stats["likes"] + stats["comments"]) / stats["views"]
    
    def calculate_view_velocity(self, video_data):
        """Calculate views per hour"""
        if "uploaded_at" not in video_data:
            return 0
        
        uploaded = datetime.fromisoformat(video_data["uploaded_at"])
        hours_since_upload = (datetime.now() - uploaded).total_seconds() / 3600
        
        if hours_since_upload == 0:
            return 0
        
        return video_data["views"] / hours_since_upload
    
    def identify_viral_videos(self):
        """Identify videos that crossed viral threshold"""
        viral_videos = []
        
        for video in self.analytics["videos"]:
            velocity = self.calculate_view_velocity(video)
            if velocity >= VIRAL_THRESHOLD:
                viral_videos.append({
                    "video_id": video["video_id"],
                    "title": video["title"],
                    "strategy": video["strategy"],
                    "velocity": velocity,
                    "views": video["views"],
                    "engagement_rate": self.calculate_engagement_rate(video)
                })
        
        return viral_videos
    
    def identify_underperformers(self):
        """Identify videos that are underperforming"""
        underperformers = []
        
        for video in self.analytics["videos"]:
            # Only check videos uploaded >1 hour ago
            if "uploaded_at" not in video:
                continue
            
            uploaded = datetime.fromisoformat(video["uploaded_at"])
            hours_since = (datetime.now() - uploaded).total_seconds() / 3600
            
            if hours_since < 1:
                continue
            
            velocity = self.calculate_view_velocity(video)
            if velocity < UNDERPERFORM_THRESHOLD:
                underperformers.append({
                    "video_id": video["video_id"],
                    "title": video["title"],
                    "strategy": video["strategy"],
                    "velocity": velocity,
                    "views": video["views"]
                })
        
        return underperformers
    
    def analyze_strategy_performance(self):
        """Analyze which strategies are performing best"""
        strategy_stats = defaultdict(lambda: {
            "videos": 0,
            "total_views": 0,
            "total_engagement": 0,
            "avg_velocity": []
        })
        
        for video in self.analytics["videos"]:
            strategy = video.get("strategy", "unknown")
            strategy_stats[strategy]["videos"] += 1
            strategy_stats[strategy]["total_views"] += video["views"]
            strategy_stats[strategy]["total_engagement"] += video["likes"] + video["comments"]
            
            velocity = self.calculate_view_velocity(video)
            strategy_stats[strategy]["avg_velocity"].append(velocity)
        
        # Calculate averages
        performance = {}
        for strategy, stats in strategy_stats.items():
            if stats["videos"] == 0:
                continue
            
            performance[strategy] = {
                "videos": stats["videos"],
                "avg_views": stats["total_views"] / stats["videos"],
                "avg_engagement": stats["total_engagement"] / stats["videos"],
                "avg_velocity": statistics.mean(stats["avg_velocity"]) if stats["avg_velocity"] else 0,
                "total_views": stats["total_views"]
            }
        
        return performance
    
    def recommend_pivot(self, performance):
        """Recommend strategy adjustments based on performance"""
        if not performance:
            return None
        
        # Sort strategies by avg_velocity (proxy for virality)
        sorted_strategies = sorted(
            performance.items(),
            key=lambda x: x[1]["avg_velocity"],
            reverse=True
        )
        
        if len(sorted_strategies) < 2:
            return None
        
        best_strategy = sorted_strategies[0]
        worst_strategy = sorted_strategies[-1]
        
        # If best is >2x better than worst, recommend shift
        if best_strategy[1]["avg_velocity"] > 2 * worst_strategy[1]["avg_velocity"]:
            recommendation = {
                "action": "SHIFT_BUDGET",
                "from_strategy": worst_strategy[0],
                "to_strategy": best_strategy[0],
                "reason": f"{best_strategy[0]} has {best_strategy[1]['avg_velocity']:.0f} views/hr vs {worst_strategy[1]['avg_velocity']:.0f} views/hr",
                "suggested_allocation": {
                    best_strategy[0]: min(self.active_strategy.get(best_strategy[0], 0) + 0.10, 0.60),
                    worst_strategy[0]: max(self.active_strategy.get(worst_strategy[0], 0) - 0.10, 0.05)
                }
            }
            return recommendation
        
        return None
    
    def update_all_videos(self):
        """Fetch latest stats for all tracked videos"""
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Updating video stats...")
        
        for video in self.analytics["videos"]:
            video_id = video["video_id"]
            stats = self.fetch_video_stats(video_id)
            
            if stats:
                video.update(stats)
                print(f"  {video['title'][:50]}... | {stats['views']} views | {self.calculate_engagement_rate(stats)*100:.2f}% engagement")
        
        self.save_analytics()
    
    def generate_report(self):
        """Generate performance report"""
        print("\n" + "="*80)
        print("  SCARIFY ADAPTIVE MANAGER - PERFORMANCE REPORT")
        print("="*80 + "\n")
        
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Videos tracked: {len(self.analytics['videos'])}\n")
        
        # Viral videos
        viral = self.identify_viral_videos()
        print(f"🔥 VIRAL VIDEOS: {len(viral)}")
        for v in viral[:5]:  # Top 5
            print(f"  - {v['title'][:50]}... | {v['views']:,} views | {v['velocity']:.0f} views/hr")
        print()
        
        # Underperformers
        under = self.identify_underperformers()
        print(f"⚠️  UNDERPERFORMING: {len(under)}")
        for v in under[:5]:
            print(f"  - {v['title'][:50]}... | {v['views']:,} views | {v['velocity']:.0f} views/hr")
        print()
        
        # Strategy performance
        performance = self.analyze_strategy_performance()
        print("📊 STRATEGY PERFORMANCE:")
        for strategy, stats in sorted(performance.items(), key=lambda x: x[1]["avg_velocity"], reverse=True):
            print(f"  {strategy}:")
            print(f"    Videos: {stats['videos']}")
            print(f"    Avg Views: {stats['avg_views']:.0f}")
            print(f"    Avg Velocity: {stats['avg_velocity']:.0f} views/hr")
            print(f"    Current Allocation: {self.active_strategy.get(strategy, 0)*100:.0f}%")
        print()
        
        # Pivot recommendation
        pivot = self.recommend_pivot(performance)
        if pivot:
            print("🎯 RECOMMENDED ACTION:")
            print(f"  {pivot['action']}: {pivot['from_strategy']} → {pivot['to_strategy']}")
            print(f"  Reason: {pivot['reason']}")
            print(f"  Suggested allocation:")
            for strat, alloc in pivot['suggested_allocation'].items():
                print(f"    {strat}: {alloc*100:.0f}%")
        else:
            print("✅ No pivots recommended - continue current strategy")
        
        print("\n" + "="*80 + "\n")
        
        # Log this check
        self.performance_history["checks"].append({
            "timestamp": datetime.now().isoformat(),
            "viral_count": len(viral),
            "underperform_count": len(under),
            "total_views": sum(v["views"] for v in self.analytics["videos"]),
            "strategy_performance": performance,
            "pivot_recommended": pivot
        })
        self.save_performance_history()
    
    def monitor_loop(self, interval_seconds=300):
        """Main monitoring loop"""
        print(f"🚀 SCARIFY ADAPTIVE MANAGER STARTED")
        print(f"Monitoring every {interval_seconds/60:.0f} minutes\n")
        
        while True:
            try:
                self.update_all_videos()
                self.generate_report()
                
                print(f"Next check in {interval_seconds/60:.0f} minutes...")
                time.sleep(interval_seconds)
                
            except KeyboardInterrupt:
                print("\n[STOPPED] Manual interrupt")
                break
            except Exception as e:
                print(f"\n[ERROR] {e}")
                print("Continuing in 60 seconds...")
                time.sleep(60)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--monitor', action='store_true', help='Start monitoring loop')
    parser.add_argument('--report', action='store_true', help='Generate one-time report')
    parser.add_argument('--interval', type=int, default=300, help='Monitoring interval (seconds)')
    
    args = parser.parse_args()
    
    manager = AdaptiveManager()
    
    if args.monitor:
        manager.monitor_loop(args.interval)
    elif args.report:
        manager.update_all_videos()
        manager.generate_report()
    else:
        print("Usage: python SCARIFY_ADAPTIVE_MANAGER.py --monitor [--interval 300]")
        print("   or: python SCARIFY_ADAPTIVE_MANAGER.py --report")

