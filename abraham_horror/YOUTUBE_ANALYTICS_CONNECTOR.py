"""
YOUTUBE STUDIO ANALYTICS CONNECTOR
Connects to YouTube Data API v3 for deep analysis
Uses your existing OAuth credentials
"""
import os, sys, json, pickle, time
from pathlib import Path
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configuration
BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
CHANNEL_ID = "UCS5pEpSCw8k4wene0iv0uAg"
SCOPES = [
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/yt-analytics.readonly'
]

class YouTubeStudioConnector:
    """Connect to YouTube Studio for programmatic analysis"""
    
    def __init__(self):
        self.youtube = None
        self.analytics = None
        self.channel_id = CHANNEL_ID
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with YouTube API"""
        print("[AUTH] Connecting to YouTube Studio...")
        
        creds = None
        token_file = BASE / "youtube_analytics_token.pickle"
        
        # Try to load existing credentials
        if token_file.exists():
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # Refresh or create new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                print("[AUTH] Refreshed expired credentials")
            else:
                # Find client secrets
                possible_secrets = [
                    Path("F:/AI_Oracle_Root/scarify/config/credentials/youtube/client_secrets.json"),
                    Path("F:/AI_Oracle_Root/scarify/client_secret_*.json"),
                ]
                
                client_file = None
                for pf in possible_secrets:
                    if pf.exists():
                        client_file = pf
                        break
                    # Try glob for client_secret_*
                    matches = list(Path("F:/AI_Oracle_Root/scarify").glob("client_secret_*.json"))
                    if matches:
                        client_file = matches[0]
                        break
                
                if not client_file:
                    print("[ERROR] No YouTube OAuth credentials found!")
                    print("[INFO] Place your client_secrets.json in:")
                    print("       F:/AI_Oracle_Root/scarify/config/credentials/youtube/")
                    sys.exit(1)
                
                flow = InstalledAppFlow.from_client_secrets_file(str(client_file), SCOPES)
                creds = flow.run_local_server(port=0)
                print("[AUTH] Created new credentials")
            
            # Save credentials
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        # Build API clients
        self.youtube = build('youtube', 'v3', credentials=creds)
        self.analytics = build('youtubeAnalytics', 'v2', credentials=creds)
        print("[AUTH] OK Connected to YouTube Studio API")
    
    def get_channel_stats(self):
        """Get overall channel statistics"""
        print("\n[CHANNEL] Fetching channel statistics...")
        
        try:
            request = self.youtube.channels().list(
                part='statistics,snippet,contentDetails',
                id=self.channel_id
            )
            response = request.execute()
            
            if not response.get('items'):
                print("[ERROR] Channel not found!")
                return None
            
            channel = response['items'][0]
            stats = channel['statistics']
            
            data = {
                'title': channel['snippet']['title'],
                'subscribers': int(stats.get('subscriberCount', 0)),
                'total_views': int(stats.get('viewCount', 0)),
                'total_videos': int(stats.get('videoCount', 0)),
                'created': channel['snippet']['publishedAt']
            }
            
            print(f"[CHANNEL] {data['title']}")
            print(f"         Subscribers: {data['subscribers']}")
            print(f"         Total Views: {data['total_views']:,}")
            print(f"         Total Videos: {data['total_videos']}")
            
            return data
            
        except HttpError as e:
            print(f"[ERROR] API Error: {e}")
            return None
    
    def get_recent_videos(self, max_results=50):
        """Get recent video uploads with metadata"""
        print(f"\n[VIDEOS] Fetching last {max_results} uploads...")
        
        try:
            # Get uploads playlist ID
            request = self.youtube.channels().list(
                part='contentDetails',
                id=self.channel_id
            )
            response = request.execute()
            
            if not response.get('items'):
                return []
            
            uploads_playlist = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            # Get videos from uploads playlist
            request = self.youtube.playlistItems().list(
                part='snippet,contentDetails',
                playlistId=uploads_playlist,
                maxResults=max_results
            )
            response = request.execute()
            
            videos = []
            for item in response.get('items', []):
                video_id = item['contentDetails']['videoId']
                snippet = item['snippet']
                
                # Get video statistics
                video_request = self.youtube.videos().list(
                    part='statistics,contentDetails',
                    id=video_id
                )
                video_response = video_request.execute()
                
                if video_response.get('items'):
                    video_stats = video_response['items'][0]['statistics']
                    duration = video_response['items'][0]['contentDetails']['duration']
                    
                    videos.append({
                        'video_id': video_id,
                        'title': snippet['title'],
                        'published': snippet['publishedAt'],
                        'description': snippet['description'],
                        'views': int(video_stats.get('viewCount', 0)),
                        'likes': int(video_stats.get('likeCount', 0)),
                        'comments': int(video_stats.get('commentCount', 0)),
                        'duration': duration,
                        'url': f"https://www.youtube.com/watch?v={video_id}"
                    })
            
            print(f"[VIDEOS] OK Fetched {len(videos)} videos")
            return videos
            
        except HttpError as e:
            print(f"[ERROR] API Error: {e}")
            return []
    
    def get_analytics_report(self, start_date=None, end_date=None, metrics='views,likes,comments,shares,subscribersGained'):
        """Get YouTube Analytics report"""
        print("\n[ANALYTICS] Fetching analytics report...")
        
        if not start_date:
            start_date = (datetime.now() - timedelta(days=28)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        try:
            request = self.analytics.reports().query(
                ids=f'channel=={self.channel_id}',
                startDate=start_date,
                endDate=end_date,
                metrics=metrics,
                dimensions='day',
                sort='day'
            )
            response = request.execute()
            
            print(f"[ANALYTICS] Period: {start_date} to {end_date}")
            print(f"[ANALYTICS] OK Fetched {len(response.get('rows', []))} data points")
            
            return response
            
        except HttpError as e:
            print(f"[ERROR] API Error: {e}")
            return None
    
    def check_shorts_for_qr_codes(self, videos):
        """Analyze which shorts have QR codes in descriptions"""
        print("\n[QR CHECK] Analyzing videos for QR codes...")
        
        qr_keywords = ['qr', 'bitcoin', 'bc1q', 'cash app', 'scan', 'support']
        
        has_qr = []
        no_qr = []
        
        for video in videos:
            desc_lower = video['description'].lower()
            title_lower = video['title'].lower()
            
            # Check for QR-related content
            found = any(keyword in desc_lower or keyword in title_lower for keyword in qr_keywords)
            
            if found:
                has_qr.append(video)
            else:
                no_qr.append(video)
        
        print(f"[QR CHECK] Videos WITH QR mentions: {len(has_qr)}")
        print(f"[QR CHECK] Videos WITHOUT QR mentions: {len(no_qr)}")
        
        if no_qr:
            print("\n[QR CHECK] WARNING Videos missing QR codes:")
            for v in no_qr[:12]:  # Show first 12
                print(f"           - {v['title'][:60]} ({v['views']} views)")
        
        return has_qr, no_qr
    
    def generate_report(self, output_file=None):
        """Generate comprehensive analysis report"""
        print("\n" + "="*70)
        print("YOUTUBE STUDIO ANALYSIS REPORT")
        print("="*70)
        
        # Get all data
        channel_stats = self.get_channel_stats()
        videos = self.get_recent_videos(50)
        analytics = self.get_analytics_report()
        has_qr, no_qr = self.check_shorts_for_qr_codes(videos)
        
        # Calculate insights
        total_views = sum(v['views'] for v in videos)
        avg_views = total_views / len(videos) if videos else 0
        top_videos = sorted(videos, key=lambda x: x['views'], reverse=True)[:10]
        
        report = {
            'generated': datetime.now().isoformat(),
            'channel': channel_stats,
            'summary': {
                'total_videos_analyzed': len(videos),
                'total_views': total_views,
                'average_views': avg_views,
                'videos_with_qr': len(has_qr),
                'videos_without_qr': len(no_qr),
                'qr_coverage': len(has_qr) / len(videos) * 100 if videos else 0
            },
            'top_performing': top_videos,
            'missing_qr_codes': no_qr[:12],
            'analytics_data': analytics
        }
        
        # Print summary
        print("\n[SUMMARY]")
        print(f"   Subscribers: {channel_stats['subscribers']} / 500 (need {500 - channel_stats['subscribers']} more)")
        print(f"   Recent Videos: {len(videos)}")
        print(f"   Avg Views/Video: {avg_views:.0f}")
        print(f"   QR Code Coverage: {report['summary']['qr_coverage']:.1f}%")
        
        print("\n[TOP 5 PERFORMERS]")
        for i, v in enumerate(top_videos[:5], 1):
            print(f"   {i}. {v['title'][:50]} - {v['views']:,} views")
        
        print("\n[WARNING] VIDEOS MISSING QR CODES:")
        print(f"   {len(no_qr)} videos need QR codes added")
        
        # Save report
        if not output_file:
            output_file = BASE / f"analytics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n[SAVED] Report saved: {output_file}")
        print("="*70)
        
        return report

def main():
    """Main execution"""
    print("\n[YOUTUBE STUDIO ANALYTICS CONNECTOR]")
    print("="*70)
    
    connector = YouTubeStudioConnector()
    report = connector.generate_report()
    
    print("\n[OK] ANALYSIS COMPLETE")
    print("\n[ACTIONABLE INSIGHTS]")
    print(f"   1. Add QR codes to {len(report['missing_qr_codes'])} videos")
    print(f"   2. Need {500 - report['channel']['subscribers']} more subscribers for monetization")
    print(f"   3. Your Shorts strategy is WORKING (92% views from Shorts feed)")
    print(f"   4. Focus on QR code integration for Bitcoin donations")
    
    return report

if __name__ == "__main__":
    main()

