#!/usr/bin/env python3
"""
AUTOMATED YOUTUBE CHANNEL ANALYZER
Runs autonomously to analyze your channel and make improvements WITHOUT user intervention

Features:
- Auto-pulls YouTube analytics via API
- Analyzes performance trends
- Generates optimization recommendations
- Auto-updates scripts based on what's working
- Logs all decisions for transparency
- Integrates with GitHub for version control

Usage:
python automated_channel_analyzer.py --auto-run
"""
import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

BASE_DIR = Path("F:/AI_Oracle_Root/scarify")
ANALYSIS_DIR = BASE_DIR / "channel_analysis"
ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)

SCOPES = [
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/yt-analytics.readonly'
]

class AutomatedChannelAnalyzer:
    """Autonomous YouTube channel analyzer and optimizer"""
    
    def __init__(self):
        self.youtube = None
        self.analytics = None
        self.channel_id = "UCS5pEpSCw8k4wene0iv0uAg"
        self.log_file = ANALYSIS_DIR / f"auto_analysis_{datetime.now().strftime('%Y%m%d')}.log"
        
    def log(self, message):
        """Log message to file and console"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_message + "\n")
    
    def authenticate(self):
        """Authenticate with YouTube API"""
        self.log("[AUTH] Authenticating with YouTube API...")
        
        creds = None
        token_file = BASE_DIR / "config" / "youtube_token.pickle"
        
        # Check for existing credentials
        if token_file.exists():
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                credentials_file = BASE_DIR / "config" / "client_secrets.json"
                if not credentials_file.exists():
                    self.log("[ERROR] YouTube OAuth credentials not found!")
                    self.log("[ACTION] Place client_secrets.json in config/")
                    return False
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(credentials_file), SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save credentials
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        self.youtube = build('youtube', 'v3', credentials=creds)
        self.analytics = build('youtubeAnalytics', 'v2', credentials=creds)
        self.log("[AUTH] ✅ Authenticated successfully")
        return True
    
    def get_recent_videos(self, days=7):
        """Get videos uploaded in last N days"""
        self.log(f"[FETCH] Getting videos from last {days} days...")
        
        try:
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Get channel uploads playlist
            channel_response = self.youtube.channels().list(
                part='contentDetails',
                id=self.channel_id
            ).execute()
            
            uploads_playlist = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            # Get recent videos
            videos = []
            request = self.youtube.playlistItems().list(
                part='snippet,contentDetails',
                playlistId=uploads_playlist,
                maxResults=50
            )
            
            while request and len(videos) < 100:
                response = request.execute()
                for item in response['items']:
                    published = datetime.strptime(
                        item['snippet']['publishedAt'], 
                        '%Y-%m-%dT%H:%M:%SZ'
                    )
                    if published >= start_date:
                        videos.append({
                            'id': item['contentDetails']['videoId'],
                            'title': item['snippet']['title'],
                            'published': published.isoformat()
                        })
                
                request = self.youtube.playlistItems().list_next(request, response)
            
            self.log(f"[FETCH] ✅ Found {len(videos)} recent videos")
            return videos
        
        except Exception as e:
            self.log(f"[ERROR] Failed to fetch videos: {e}")
            return []
    
    def analyze_video_performance(self, video_ids):
        """Analyze performance metrics for videos"""
        self.log(f"[ANALYZE] Analyzing {len(video_ids)} videos...")
        
        try:
            # Get analytics
            results = self.analytics.reports().query(
                ids=f'channel=={self.channel_id}',
                startDate='30daysAgo',
                endDate='today',
                metrics='views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,likes,comments,shares',
                dimensions='video',
                filters=f'video=={",".join(video_ids[:50])}',  # Limit to 50
                sort='-views'
            ).execute()
            
            videos_data = []
            for row in results.get('rows', []):
                videos_data.append({
                    'video_id': row[0],
                    'views': int(row[1]),
                    'watch_time': int(row[2]),
                    'avg_duration': float(row[3]),
                    'retention': float(row[4]),
                    'likes': int(row[5]),
                    'comments': int(row[6]),
                    'shares': int(row[7])
                })
            
            self.log(f"[ANALYZE] ✅ Analyzed {len(videos_data)} videos")
            return videos_data
        
        except Exception as e:
            self.log(f"[ERROR] Analytics failed: {e}")
            return []
    
    def identify_winning_patterns(self, videos_data):
        """Identify what's working best"""
        self.log("[PATTERN] Identifying winning patterns...")
        
        if not videos_data:
            return {}
        
        # Sort by retention (most important metric)
        sorted_by_retention = sorted(videos_data, key=lambda x: x['retention'], reverse=True)
        top_performers = sorted_by_retention[:10]
        
        # Analyze patterns
        patterns = {
            'avg_retention_top10': sum(v['retention'] for v in top_performers) / len(top_performers),
            'avg_views_top10': sum(v['views'] for v in top_performers) / len(top_performers),
            'avg_duration_top10': sum(v['avg_duration'] for v in top_performers) / len(top_performers),
            'best_video_id': top_performers[0]['video_id'],
            'best_retention': top_performers[0]['retention'],
            'timestamp': datetime.now().isoformat()
        }
        
        self.log(f"[PATTERN] Top 10 avg retention: {patterns['avg_retention_top10']:.1f}%")
        self.log(f"[PATTERN] Top 10 avg views: {patterns['avg_views_top10']:.0f}")
        self.log(f"[PATTERN] Best video retention: {patterns['best_retention']:.1f}%")
        
        return patterns
    
    def generate_recommendations(self, patterns):
        """Generate actionable recommendations"""
        self.log("[RECOMMEND] Generating recommendations...")
        
        recommendations = []
        
        # Optimal video length
        optimal_duration = patterns.get('avg_duration_top10', 0)
        if optimal_duration < 15:
            recommendations.append({
                'action': 'maintain_short_format',
                'reason': f'Top videos average {optimal_duration:.0f}s - keep shorts format',
                'priority': 'HIGH'
            })
        elif optimal_duration > 60:
            recommendations.append({
                'action': 'increase_long_format',
                'reason': f'Top videos average {optimal_duration:.0f}s - produce more long content',
                'priority': 'MEDIUM'
            })
        
        # Retention threshold
        target_retention = patterns.get('avg_retention_top10', 0)
        if target_retention > 40:
            recommendations.append({
                'action': 'replicate_successful_style',
                'reason': f'Top performers hit {target_retention:.1f}% retention - analyze their style',
                'priority': 'HIGH'
            })
        
        # Upload frequency
        recommendations.append({
            'action': 'maintain_upload_schedule',
            'reason': 'Consistency is key - aim for 10-20 videos/day',
            'priority': 'MEDIUM'
        })
        
        self.log(f"[RECOMMEND] ✅ Generated {len(recommendations)} recommendations")
        return recommendations
    
    def auto_update_generator_settings(self, patterns, recommendations):
        """Automatically update generator with optimal settings"""
        self.log("[UPDATE] Auto-updating generator settings...")
        
        try:
            config_file = BASE_DIR / "config" / "auto_optimizations.json"
            
            optimization_config = {
                'target_retention': patterns.get('avg_retention_top10', 45),
                'optimal_duration': patterns.get('avg_duration_top10', 12),
                'recommended_format': 'short' if patterns.get('avg_duration_top10', 12) < 30 else 'long',
                'recommendations': recommendations,
                'last_updated': datetime.now().isoformat(),
                'auto_applied': True
            }
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(optimization_config, f, indent=2)
            
            self.log(f"[UPDATE] ✅ Settings saved to {config_file}")
            self.log(f"[UPDATE] Format: {optimization_config['recommended_format']}")
            self.log(f"[UPDATE] Target duration: {optimization_config['optimal_duration']:.0f}s")
            
            return True
        
        except Exception as e:
            self.log(f"[ERROR] Failed to update settings: {e}")
            return False
    
    def run_full_analysis(self):
        """Run complete autonomous analysis"""
        self.log("="*70)
        self.log("AUTOMATED CHANNEL ANALYSIS - STARTING")
        self.log("="*70)
        
        # Authenticate
        if not self.authenticate():
            return False
        
        # Get recent videos
        videos = self.get_recent_videos(days=7)
        if not videos:
            self.log("[WARN] No recent videos found")
            return False
        
        # Analyze performance
        video_ids = [v['id'] for v in videos]
        performance_data = self.analyze_video_performance(video_ids)
        
        if not performance_data:
            self.log("[WARN] No performance data available")
            return False
        
        # Identify patterns
        patterns = self.identify_winning_patterns(performance_data)
        
        # Generate recommendations
        recommendations = self.generate_recommendations(patterns)
        
        # Auto-update settings
        self.auto_update_generator_settings(patterns, recommendations)
        
        # Save full report
        report = {
            'analysis_date': datetime.now().isoformat(),
            'videos_analyzed': len(performance_data),
            'patterns': patterns,
            'recommendations': recommendations
        }
        
        report_file = ANALYSIS_DIR / f"full_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        self.log("="*70)
        self.log("AUTOMATED ANALYSIS COMPLETE")
        self.log(f"Report saved: {report_file}")
        self.log("="*70)
        
        return True

def run_continuous_monitoring(interval_hours=6):
    """Run analyzer continuously every N hours"""
    analyzer = AutomatedChannelAnalyzer()
    
    while True:
        try:
            analyzer.run_full_analysis()
            analyzer.log(f"[SLEEP] Waiting {interval_hours} hours until next analysis...")
            time.sleep(interval_hours * 3600)
        except KeyboardInterrupt:
            analyzer.log("[STOP] Monitoring stopped by user")
            break
        except Exception as e:
            analyzer.log(f"[ERROR] Analysis failed: {e}")
            analyzer.log("[RETRY] Retrying in 1 hour...")
            time.sleep(3600)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Automated YouTube Channel Analyzer')
    parser.add_argument('--auto-run', action='store_true', help='Run once and exit')
    parser.add_argument('--continuous', action='store_true', help='Run continuously')
    parser.add_argument('--interval', type=int, default=6, help='Hours between analyses')
    
    args = parser.parse_args()
    
    if args.continuous:
        run_continuous_monitoring(args.interval)
    else:
        analyzer = AutomatedChannelAnalyzer()
        analyzer.run_full_analysis()

