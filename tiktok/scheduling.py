#!/usr/bin/env python3
"""
TikTok Scheduling System for @nunyabeznes2
Content scheduling and queue management
"""

import json
try:
    import schedule
    SCHEDULE_AVAILABLE = True
except ImportError:
    SCHEDULE_AVAILABLE = False
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional


class TikTokScheduler:
    """Advanced scheduling system for @nunyabeznes2"""
    
    def __init__(self, base_path: Optional[Path] = None):
        if base_path is None:
            base_path = Path(__file__).parent.parent
        
        self.base_path = Path(base_path)
        self.schedule_db_path = self.base_path / "tiktok" / "schedule_db.json"
        self.schedule_db = self._load_schedule_db()
        
        self.optimal_post_times = [
            "09:00", "12:00", "15:00", "18:00", "21:00"  # Peak TikTok hours
        ]
        
        self.content_calendar = {
            'monday': ['Business Horrors', 'Corporate Truths'],
            'tuesday': ['Profit Nightmares', 'CEO Confessions'],
            'wednesday': ['Workplace Horror', 'Salary Secrets'],
            'thursday': ['Corporate Conspiracies', 'Business Lies'],
            'friday': ['Weekend Warning', 'Corporate Exposed'],
            'saturday': ['Dark Business Facts', 'Capitalism Horrors'],
            'sunday': ['Monday Preparation', 'Corporate Dread']
        }
    
    def _load_schedule_db(self) -> Dict:
        """Load schedule database"""
        try:
            if self.schedule_db_path.exists():
                with open(self.schedule_db_path, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {'scheduled_posts': [], 'posted_content': []}
    
    def _save_schedule_db(self):
        """Save schedule database"""
        self.schedule_db_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.schedule_db_path, 'w') as f:
            json.dump(self.schedule_db, f, indent=2)
    
    def schedule_content_batch(
        self,
        content_batch: List[Dict],
        start_date: Optional[datetime] = None
    ) -> List[Dict]:
        """Schedule a batch of content"""
        
        if not start_date:
            start_date = datetime.now()
        
        scheduled_posts = []
        
        for i, content in enumerate(content_batch):
            # Space posts throughout the day
            post_time = self.optimal_post_times[i % len(self.optimal_post_times)]
            
            # Schedule for different days
            post_date = start_date + timedelta(days=i // len(self.optimal_post_times))
            
            scheduled_post = {
                'post_id': f"tiktok_{post_date.strftime('%Y%m%d')}_{i}",
                'content': content,
                'scheduled_time': f"{post_date.strftime('%Y-%m-%d')} {post_time}",
                'status': 'SCHEDULED',
                'platform': 'tiktok',
                'account': '@nunyabeznes2'
            }
            
            scheduled_posts.append(scheduled_post)
            self.schedule_db['scheduled_posts'].append(scheduled_post)
        
        self._save_schedule_db()
        return scheduled_posts
    
    def get_todays_schedule(self) -> List[Dict]:
        """Get today's scheduled posts"""
        
        today = datetime.now().strftime('%Y-%m-%d')
        todays_posts = []
        
        for post in self.schedule_db['scheduled_posts']:
            if post['scheduled_time'].startswith(today) and post['status'] == 'SCHEDULED':
                todays_posts.append(post)
        
        return todays_posts
    
    def mark_as_posted(self, post_id: str, tiktok_url: Optional[str] = None):
        """Mark post as completed"""
        
        for post in self.schedule_db['scheduled_posts']:
            if post['post_id'] == post_id:
                post['status'] = 'POSTED'
                post['posted_at'] = datetime.now().isoformat()
                post['tiktok_url'] = tiktok_url
                
                # Move to posted content
                self.schedule_db['posted_content'].append(post)
        
        self._save_schedule_db()
    
    def generate_content_calendar(self, weeks: int = 4) -> Dict:
        """Generate content calendar for upcoming weeks"""
        
        calendar = {}
        start_date = datetime.now()
        
        for week in range(weeks):
            week_key = f"week_{week+1}"
            calendar[week_key] = {}
            
            for day in range(7):
                current_date = start_date + timedelta(days=(week * 7 + day))
                day_name = current_date.strftime('%A').lower()
                
                calendar[week_key][current_date.strftime('%Y-%m-%d')] = {
                    'day': day_name,
                    'themes': self.content_calendar.get(day_name, ['Business Horror']),
                    'optimal_times': self.optimal_post_times
                }
        
        return calendar


class TikTokAnalytics:
    """Track TikTok performance for @nunyabeznes2"""
    
    def __init__(self, base_path: Optional[Path] = None):
        if base_path is None:
            base_path = Path(__file__).parent.parent
        
        self.base_path = Path(base_path)
        self.analytics_db_path = self.base_path / "tiktok" / "analytics_db.json"
        self.analytics_db = self._load_analytics_db()
    
    def _load_analytics_db(self) -> Dict:
        """Load analytics database"""
        try:
            if self.analytics_db_path.exists():
                with open(self.analytics_db_path, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {'videos': [], 'performance_metrics': {}}
    
    def _save_analytics_db(self):
        """Save analytics database"""
        self.analytics_db_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.analytics_db_path, 'w') as f:
            json.dump(self.analytics_db, f, indent=2)
    
    def track_video_performance(
        self,
        video_data: Dict,
        tiktok_url: Optional[str] = None,
        metrics: Optional[Dict] = None
    ) -> Dict:
        """Track video performance metrics"""
        
        if metrics is None:
            metrics = {}
        
        video_entry = {
            'video_id': video_data.get('post_id', 'unknown'),
            'topic': video_data.get('topic', 'unknown'),
            'tiktok_url': tiktok_url,
            'posted_at': datetime.now().isoformat(),
            'metrics': metrics,
            'content_type': video_data.get('content_format', 'unknown')
        }
        
        self.analytics_db['videos'].append(video_entry)
        self._save_analytics_db()
        
        return video_entry
    
    def get_performance_insights(self) -> Dict:
        """Generate performance insights"""
        
        if not self.analytics_db['videos']:
            return {
                'status': 'NO_DATA',
                'message': 'No videos tracked yet'
            }
        
        videos = self.analytics_db['videos']
        
        # Basic analytics
        total_videos = len(videos)
        avg_views = sum(v['metrics'].get('views', 0) for v in videos) / total_videos if total_videos > 0 else 0
        avg_likes = sum(v['metrics'].get('likes', 0) for v in videos) / total_videos if total_videos > 0 else 0
        
        # Find best performing content
        best_video = max(videos, key=lambda x: x['metrics'].get('views', 0)) if videos else None
        
        insights = {
            'total_videos_posted': total_videos,
            'average_views': round(avg_views, 2),
            'average_likes': round(avg_likes, 2),
            'best_performing_video': {
                'topic': best_video['topic'] if best_video else 'N/A',
                'views': best_video['metrics'].get('views', 0) if best_video else 0,
                'content_type': best_video['content_type'] if best_video else 'N/A'
            } if best_video else None,
            'recommendations': self._generate_recommendations(videos)
        }
        
        return insights
    
    def _generate_recommendations(self, videos: List[Dict]) -> List[str]:
        """Generate content recommendations based on performance"""
        
        if len(videos) < 5:
            return ["Post more content to gather performance data"]
        
        # Analyze what works
        high_performers = [v for v in videos if v['metrics'].get('views', 0) > 1000]
        
        if not high_performers:
            return ["Experiment with different content formats and posting times"]
        
        # Find patterns in successful content
        successful_topics = [v['topic'] for v in high_performers]
        successful_formats = [v['content_type'] for v in high_performers]
        
        recommendations = [
            f"Focus on topics like: {', '.join(set(successful_topics[:3]))}",
            f"Use content formats: {', '.join(set(successful_formats[:2]))}",
            "Post during peak engagement hours: 9AM, 12PM, 6PM, 9PM"
        ]
        
        return recommendations


if __name__ == '__main__':
    # Test scheduler
    scheduler = TikTokScheduler()
    
    # Generate content calendar
    calendar = scheduler.generate_content_calendar(weeks=2)
    print("Content Calendar (2 weeks):")
    print(json.dumps(calendar, indent=2))
    
    # Test analytics
    analytics = TikTokAnalytics()
    insights = analytics.get_performance_insights()
    print("\nAnalytics Insights:")
    print(json.dumps(insights, indent=2))
