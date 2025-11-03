"""
YOUTUBE STUDIO API ANALYZER
Programmatic access to your YouTube data for deep analysis
"""
import os, json, pickle, time
from pathlib import Path
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

BASE = Path("F:/AI_Oracle_Root/scarify")
CHANNEL_ID = "UCS5pEpSCw8k4wene0iv0uAg"

# YouTube Data API v3 scopes
SCOPES = [
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/yt-analytics.readonly'
]

CRED_FILES = [
    BASE / "config/credentials/youtube/client_secrets.json",
    BASE / "client_secret_679199614743-1fq6sini3p9kjs237ek4seg4ojp4a4qe.apps.googleusercontent.com.json",
]

def get_youtube_service():
    """Authenticate and return YouTube API service"""
    print("[PROCESS] Connecting to YouTube API...")
    
    token_file = BASE / "youtube_analytics_token.pickle"
    creds = None
    
    # Load existing credentials
    if token_file.exists():
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    
    # Refresh or get new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Find credentials file
            cred_file = None
            for cf in CRED_FILES:
                if cf.exists():
                    cred_file = cf
                    break
            
            if not cred_file:
                print("[ERROR] YouTube credentials not found!")
                print("Place client_secrets.json in config/credentials/youtube/")
                return None, None
            
            flow = InstalledAppFlow.from_client_secrets_file(str(cred_file), SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
    
    youtube = build('youtube', 'v3', credentials=creds)
    analytics = build('youtubeAnalytics', 'v2', credentials=creds)
    
    print("[OK] Connected to YouTube API")
    return youtube, analytics

def get_channel_stats(youtube):
    """Get overall channel statistics"""
    print("\n[PROCESS] Fetching channel stats...")
    
    try:
        request = youtube.channels().list(
            part='statistics,snippet',
            id=CHANNEL_ID
        )
        response = request.execute()
        
        if response['items']:
            channel = response['items'][0]
            stats = channel['statistics']
            
            print(f"\n{'='*70}")
            print(f"CHANNEL: {channel['snippet']['title']}")
            print(f"{'='*70}")
            print(f"Subscribers: {stats.get('subscriberCount', 'Hidden')}")
            print(f"Total Views: {stats.get('viewCount', 0):,}")
            print(f"Total Videos: {stats.get('videoCount', 0)}")
            print(f"{'='*70}\n")
            
            return stats
    except HttpError as e:
        print(f"[ERROR] {e}")
    
    return None

def get_recent_videos(youtube, max_results=50):
    """Get recent video uploads"""
    print(f"[PROCESS] Fetching last {max_results} videos...")
    
    try:
        # Get uploads playlist ID
        request = youtube.channels().list(
            part='contentDetails',
            id=CHANNEL_ID
        )
        response = request.execute()
        
        if not response['items']:
            return []
        
        uploads_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        
        # Get videos from uploads playlist
        videos = []
        request = youtube.playlistItems().list(
            part='snippet,contentDetails',
            playlistId=uploads_id,
            maxResults=max_results
        )
        
        while request:
            response = request.execute()
            videos.extend(response['items'])
            
            if len(videos) >= max_results:
                break
            
            request = youtube.playlistItems().list_next(request, response)
        
        print(f"[OK] Found {len(videos)} videos\n")
        return videos[:max_results]
    
    except HttpError as e:
        print(f"[ERROR] {e}")
        return []

def get_video_analytics(analytics, video_id, days=28):
    """Get detailed analytics for a specific video"""
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    try:
        request = analytics.reports().query(
            ids=f'channel=={CHANNEL_ID}',
            startDate=start_date,
            endDate=end_date,
            metrics='views,likes,comments,shares,estimatedMinutesWatched,averageViewDuration',
            dimensions='video',
            filters=f'video=={video_id}'
        )
        response = request.execute()
        
        if response.get('rows'):
            return response['rows'][0]
        return None
    
    except HttpError as e:
        print(f"[ERROR] {e}")
        return None

def analyze_shorts_without_qr(youtube):
    """Identify shorts without QR codes (by checking descriptions)"""
    print("\n[PROCESS] Analyzing shorts for QR codes...")
    
    videos = get_recent_videos(youtube, 50)
    shorts = []
    no_qr = []
    
    for video in videos:
        snippet = video['snippet']
        title = snippet['title']
        description = snippet.get('description', '')
        video_id = snippet['resourceId']['videoId']
        
        # Check if it's a short (title contains #Shorts or duration < 60s)
        if '#Shorts' in title or '#shorts' in title.lower():
            shorts.append({
                'id': video_id,
                'title': title,
                'published': snippet['publishedAt'],
                'description': description
            })
            
            # Check for QR code indicators
            qr_indicators = ['bitcoin', 'BTC', 'bc1q', 'cash.app', 'QR', 'SCAN']
            has_qr = any(indicator.lower() in description.lower() for indicator in qr_indicators)
            
            if not has_qr:
                no_qr.append({
                    'id': video_id,
                    'title': title,
                    'url': f"https://youtube.com/shorts/{video_id}"
                })
    
    print(f"\n{'='*70}")
    print(f"SHORTS ANALYSIS")
    print(f"{'='*70}")
    print(f"Total Shorts Found: {len(shorts)}")
    print(f"Shorts WITHOUT QR indicators: {len(no_qr)}")
    print(f"{'='*70}\n")
    
    if no_qr:
        print("⚠️  SHORTS MISSING QR CODES:")
        for i, short in enumerate(no_qr[:12], 1):
            print(f"{i}. {short['title'][:60]}")
            print(f"   URL: {short['url']}\n")
    
    return shorts, no_qr

def get_traffic_sources(analytics, days=28):
    """Get traffic source breakdown"""
    print(f"\n[PROCESS] Analyzing traffic sources (last {days} days)...")
    
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    try:
        request = analytics.reports().query(
            ids=f'channel=={CHANNEL_ID}',
            startDate=start_date,
            endDate=end_date,
            metrics='views',
            dimensions='insightTrafficSourceType',
            sort='-views'
        )
        response = request.execute()
        
        if response.get('rows'):
            print(f"\n{'='*70}")
            print(f"TRAFFIC SOURCES (Last {days} days)")
            print(f"{'='*70}")
            
            total_views = sum(row[1] for row in response['rows'])
            
            for row in response['rows']:
                source = row[0]
                views = row[1]
                percent = (views / total_views) * 100
                print(f"{source:30} {views:>8,} views ({percent:>5.1f}%)")
            
            print(f"{'='*70}")
            print(f"{'TOTAL':30} {total_views:>8,} views")
            print(f"{'='*70}\n")
            
            return response['rows']
    
    except HttpError as e:
        print(f"[ERROR] {e}")
    
    return []

def export_analytics_report(youtube, analytics):
    """Generate comprehensive analytics report"""
    print("\n[PROCESS] Generating comprehensive report...")
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'channel_id': CHANNEL_ID,
        'channel_stats': {},
        'recent_videos': [],
        'shorts_analysis': {},
        'traffic_sources': []
    }
    
    # Get channel stats
    stats = get_channel_stats(youtube)
    if stats:
        report['channel_stats'] = stats
    
    # Get recent videos
    videos = get_recent_videos(youtube, 50)
    report['recent_videos'] = [
        {
            'id': v['snippet']['resourceId']['videoId'],
            'title': v['snippet']['title'],
            'published': v['snippet']['publishedAt']
        }
        for v in videos
    ]
    
    # Analyze shorts
    shorts, no_qr = analyze_shorts_without_qr(youtube)
    report['shorts_analysis'] = {
        'total_shorts': len(shorts),
        'shorts_without_qr': len(no_qr),
        'missing_qr_ids': [s['id'] for s in no_qr]
    }
    
    # Get traffic sources
    traffic = get_traffic_sources(analytics, 28)
    report['traffic_sources'] = traffic
    
    # Save report
    report_file = BASE / f"youtube_analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"[OK] Report saved: {report_file.name}\n")
    return report

if __name__ == "__main__":
    print(f"\n{'='*70}")
    print(f"YOUTUBE STUDIO API ANALYZER")
    print(f"{'='*70}\n")
    
    # Connect to YouTube API
    youtube, analytics = get_youtube_service()
    
    if not youtube:
        print("[ERROR] Could not connect to YouTube API")
        print("\nSetup instructions:")
        print("1. Go to: https://console.cloud.google.com/")
        print("2. Create project or select existing")
        print("3. Enable YouTube Data API v3 and YouTube Analytics API")
        print("4. Create OAuth 2.0 credentials")
        print("5. Download client_secrets.json")
        print("6. Place in: config/credentials/youtube/")
        exit(1)
    
    # Run analysis
    export_analytics_report(youtube, analytics)
    
    print("\n✅ ANALYSIS COMPLETE")
    print("\nYou can now run this anytime to:")
    print("- Check subscriber count")
    print("- Find shorts without QR codes")
    print("- Analyze traffic sources")
    print("- Export full analytics data")

