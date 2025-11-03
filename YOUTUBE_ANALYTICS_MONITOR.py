"""
YOUTUBE ANALYTICS MONITOR & AUTO-OPTIMIZER
Monitors channel performance in real-time and auto-adjusts content strategy
Based on your analytics: DissWhatImSayin (UCS5pEpSCw8k4wene0iv0uAg)

CURRENT STATUS (from screenshots):
- 13 subscribers (need 500 for monetization)
- 5.2K views, 14.4 watch hours (90 days)
- TOP PERFORMERS: 
  * Education System Destroyed: 1,247 views, 225% avg view %
  * Military Draft Activated: 1,194 views, 135% avg view %
  * Government Shutdown: 338 views, 70.9% avg view %
- GEOGRAPHY: 61.9% US, 7.4% UK, 5.9% Canada (need global expansion)
- FORMAT: All Shorts (need long videos)
- ISSUES: Some videos "Processing abandoned" (need to fix)
"""
import os, sys, json, requests, subprocess, time
from pathlib import Path
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
YOUTUBE_CREDENTIALS = Path("F:/AI_Oracle_Root/scarify/config/credentials/youtube/client_secrets.json")
CHANNEL_ID = "UCS5pEpSCw8k4wene0iv0uAg"

def log(msg, status="INFO"):
    icons = {"INFO": "[📊]", "SUCCESS": "[✅]", "ERROR": "[❌]", "ALERT": "[🚨]"}
    print(f"{icons.get(status, '[INFO]')} {msg}")

def get_youtube_service():
    """Authenticate with YouTube API"""
    SCOPES = [
        'https://www.googleapis.com/auth/youtube.readonly',
        'https://www.googleapis.com/auth/youtube'
    ]
    
    cred_files = [
        YOUTUBE_CREDENTIALS,
        Path("F:/AI_Oracle_Root/scarify/client_secret_679199614743-1fq6sini3p9kjs237ek4seg4ojp4a4qe.apps.googleusercontent.com.json"),
    ]
    
    cred_file = None
    for cf in cred_files:
        if cf and cf.exists():
            cred_file = cf
            break
    
    if not cred_file:
        log("YouTube credentials not found", "ERROR")
        return None
    
    token_file = BASE / "youtube_analytics_token.pickle"
    creds = None
    
    if token_file.exists():
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(cred_file), SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('youtube', 'v3', credentials=creds)

def analyze_current_performance(youtube):
    """Analyze channel performance from YouTube API"""
    log("\n🔍 ANALYZING CHANNEL PERFORMANCE", "INFO")
    log("="*70)
    
    try:
        # Get channel statistics
        channel_response = youtube.channels().list(
            part='statistics,snippet',
            id=CHANNEL_ID
        ).execute()
        
        if not channel_response['items']:
            log("Channel not found", "ERROR")
            return None
        
        stats = channel_response['items'][0]['statistics']
        snippet = channel_response['items'][0]['snippet']
        
        subs = int(stats.get('subscriberCount', 0))
        total_views = int(stats.get('viewCount', 0))
        total_videos = int(stats.get('videoCount', 0))
        
        log(f"Channel: {snippet['title']}")
        log(f"Subscribers: {subs} / 500 (need {500-subs} more for monetization)")
        log(f"Total Views: {total_views:,}")
        log(f"Total Videos: {total_videos}")
        
        # Get recent videos
        videos_response = youtube.search().list(
            part='snippet',
            channelId=CHANNEL_ID,
            order='date',
            maxResults=50,
            type='video'
        ).execute()
        
        video_ids = [item['id']['videoId'] for item in videos_response.get('items', [])]
        
        if video_ids:
            # Get video statistics
            stats_response = youtube.videos().list(
                part='statistics,contentDetails,snippet',
                id=','.join(video_ids[:50])
            ).execute()
            
            videos_data = []
            shorts_views = 0
            total_duration = 0
            
            for video in stats_response.get('items', []):
                vid_stats = video['statistics']
                duration_str = video['contentDetails']['duration']
                title = video['snippet']['title']
                
                # Parse ISO 8601 duration
                import re
                duration_match = re.search(r'PT(\d+)M?(\d+)?S?', duration_str)
                if duration_match:
                    minutes = int(duration_match.group(1)) if duration_match.group(1) else 0
                    seconds = int(duration_match.group(2)) if duration_match.group(2) else 0
                    duration_seconds = minutes * 60 + seconds
                else:
                    duration_seconds = 0
                
                views = int(vid_stats.get('viewCount', 0))
                likes = int(vid_stats.get('likeCount', 0))
                comments = int(vid_stats.get('commentCount', 0))
                
                is_short = duration_seconds <= 60
                if is_short:
                    shorts_views += views
                
                total_duration += duration_seconds
                
                videos_data.append({
                    'title': title[:60],
                    'views': views,
                    'likes': likes,
                    'comments': comments,
                    'duration': duration_seconds,
                    'is_short': is_short,
                    'engagement_rate': (likes + comments) / views if views > 0 else 0
                })
            
            # Sort by views
            videos_data.sort(key=lambda x: x['views'], reverse=True)
            
            log(f"\n📈 TOP 5 PERFORMERS:")
            log("="*70)
            for i, vid in enumerate(videos_data[:5], 1):
                log(f"{i}. {vid['title']}")
                log(f"   Views: {vid['views']:,} | Likes: {vid['likes']} | Comments: {vid['comments']}")
                log(f"   Duration: {vid['duration']}s | {'SHORT' if vid['is_short'] else 'LONG'} | Engagement: {vid['engagement_rate']:.2%}")
            
            log(f"\n📊 CONTENT BREAKDOWN:")
            log("="*70)
            shorts_count = sum(1 for v in videos_data if v['is_short'])
            longs_count = len(videos_data) - shorts_count
            
            log(f"Shorts: {shorts_count} ({shorts_count/len(videos_data)*100:.1f}%)")
            log(f"Long videos: {longs_count} ({longs_count/len(videos_data)*100:.1f}%)")
            log(f"Total Shorts views: {shorts_views:,} / 3,000,000 needed")
            log(f"Avg duration: {total_duration/len(videos_data):.0f}s")
            
            return {
                'subs': subs,
                'total_views': total_views,
                'total_videos': total_videos,
                'shorts_count': shorts_count,
                'longs_count': longs_count,
                'shorts_views': shorts_views,
                'top_videos': videos_data[:5],
                'all_videos': videos_data
            }
            
    except Exception as e:
        log(f"Analysis failed: {e}", "ERROR")
        import traceback
        traceback.print_exc()
    
    return None

def generate_optimization_strategy(analytics):
    """Generate strategy based on analytics"""
    log("\n🎯 OPTIMIZATION STRATEGY", "ALERT")
    log("="*70)
    
    recommendations = []
    
    # Subscriber goal
    subs_needed = 500 - analytics['subs']
    if subs_needed > 0:
        recommendations.append(f"🎯 PRIORITY: Gain {subs_needed} subscribers")
        recommendations.append(f"   Strategy: Add end-screen CTAs, collaboration videos, subscriber-only content")
    
    # Shorts vs Long balance
    if analytics['longs_count'] < 5:
        recommendations.append(f"🎬 CRITICAL: Only {analytics['longs_count']} long videos")
        recommendations.append(f"   Strategy: Generate 3-10min deep dives DAILY (better watch time)")
    
    # Shorts views for monetization
    shorts_needed = 3_000_000 - analytics['shorts_views']
    if shorts_needed > 0:
        recommendations.append(f"📺 Shorts path: {shorts_needed:,} views needed")
        recommendations.append(f"   Strategy: 20 Shorts/day × 30 days = potential path")
    
    # Analyze top performers
    if analytics['top_videos']:
        top_keywords = []
        for vid in analytics['top_videos'][:3]:
            title = vid['title'].lower()
            if 'warning' in title:
                top_keywords.append('WARNING')
            if 'education' in title or 'military' in title or 'government' in title:
                top_keywords.append('CRISIS TOPICS')
            if vid['engagement_rate'] > 0.05:
                top_keywords.append('HIGH ENGAGEMENT')
        
        if top_keywords:
            recommendations.append(f"🔥 What's Working: {', '.join(set(top_keywords))}")
            recommendations.append(f"   Strategy: Double down on these themes")
    
    # Global reach
    recommendations.append(f"🌍 GLOBAL EXPANSION NEEDED")
    recommendations.append(f"   Current: 62% US-only")
    recommendations.append(f"   Strategy: Multi-language subtitles, international topics, timeless content")
    
    for rec in recommendations:
        log(rec)
    
    return recommendations

def generate_content_plan(analytics):
    """Generate specific content plan based on analytics"""
    log("\n📝 7-DAY CONTENT PLAN", "ALERT")
    log("="*70)
    
    plan = {
        "shorts_daily": 10,
        "longs_daily": 2,
        "themes": [],
        "formats": []
    }
    
    # Based on top performers
    if analytics and analytics.get('top_videos'):
        top = analytics['top_videos'][0]
        if 'education' in top['title'].lower():
            plan['themes'].append("Education system failures")
        if 'military' in top['title'].lower():
            plan['themes'].append("Military/war commentary")
        if 'government' in top['title'].lower():
            plan['themes'].append("Government corruption")
    
    # Add global themes
    plan['themes'].extend([
        "Climate crisis (global appeal)",
        "Technology addiction (universal)",
        "Economic inequality (worldwide)",
        "AI takeover (international fear)"
    ])
    
    # Format mix
    plan['formats'] = [
        "Shorts (60s) - Viral hooks",
        "Long (3-5min) - Deep analysis",
        "Long (8-10min) - Full rants with chapters"
    ]
    
    log("📺 DAILY OUTPUT:")
    log(f"  • {plan['shorts_daily']} Shorts (15-60s)")
    log(f"  • {plan['longs_daily']} Longs (3-10min)")
    log(f"  • Total: {plan['shorts_daily'] + plan['longs_daily']} videos/day")
    
    log("\n🎯 THEMES TO FOCUS ON:")
    for theme in plan['themes']:
        log(f"  • {theme}")
    
    log("\n📊 FORMAT MIX:")
    for fmt in plan['formats']:
        log(f"  • {fmt}")
    
    return plan

if __name__ == "__main__":
    log("\n" + "="*70)
    log("YOUTUBE ANALYTICS MONITOR & AUTO-OPTIMIZER")
    log("Channel: DissWhatImSayin (UCS5pEpSCw8k4wene0iv0uAg)")
    log("="*70)
    
    youtube = get_youtube_service()
    if not youtube:
        log("Failed to authenticate with YouTube", "ERROR")
        sys.exit(1)
    
    analytics = analyze_current_performance(youtube)
    if analytics:
        strategy = generate_optimization_strategy(analytics)
        plan = generate_content_plan(analytics)
        
        # Save analytics report
        report = {
            'timestamp': datetime.now().isoformat(),
            'analytics': analytics,
            'recommendations': strategy,
            'content_plan': plan
        }
        
        report_file = BASE / f"analytics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        log(f"\n💾 Report saved: {report_file.name}", "SUCCESS")
        log("\n🚀 READY TO EXECUTE OPTIMIZATION PLAN", "ALERT")
    
    log("\n" + "="*70)


