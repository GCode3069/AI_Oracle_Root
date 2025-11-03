"""
CHECK AND ANALYZE PENDING YOUTUBE VIDEOS
Identifies videos stuck in pending state and suggests fixes
"""
import sys
from pathlib import Path
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
CHANNEL_ID = "UCS5pEpSCw8k4wene0iv0uAg"
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

def get_pending_videos():
    """Get list of videos stuck in pending/processing state"""
    print("\n" + "="*70)
    print("CHECKING PENDING YOUTUBE VIDEOS")
    print("="*70)
    
    # Authenticate
    creds = None
    token_file = BASE / "youtube_token.pickle"
    
    if token_file.exists():
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("[ERROR] Not authenticated. Run YOUTUBE_ANALYTICS_CONNECTOR.py first")
            return []
    
    youtube = build('youtube', 'v3', credentials=creds)
    
    try:
        # Get uploads playlist
        channel_request = youtube.channels().list(
            part='contentDetails',
            id=CHANNEL_ID
        )
        channel_response = channel_request.execute()
        
        if not channel_response.get('items'):
            print("[ERROR] Channel not found")
            return []
        
        uploads_playlist = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        
        # Get recent videos
        videos_request = youtube.playlistItems().list(
            part='snippet,contentDetails',
            playlistId=uploads_playlist,
            maxResults=50
        )
        videos_response = videos_request.execute()
        
        pending = []
        processing = []
        public = []
        
        for item in videos_response.get('items', []):
            video_id = item['contentDetails']['videoId']
            
            # Get video status
            video_request = youtube.videos().list(
                part='status,snippet,statistics',
                id=video_id
            )
            video_response = video_request.execute()
            
            if video_response.get('items'):
                video = video_response['items'][0]
                status = video['status']
                snippet = video['snippet']
                stats = video['statistics']
                
                privacy = status.get('uploadStatus', 'unknown')
                
                if privacy == 'uploaded':
                    # Still processing
                    processing.append({
                        'id': video_id,
                        'title': snippet['title'],
                        'published': snippet.get('publishedAt', ''),
                        'privacy': status.get('privacyStatus', ''),
                        'views': int(stats.get('viewCount', 0))
                    })
                elif privacy == 'processed' and status.get('privacyStatus') == 'public':
                    public.append({
                        'id': video_id,
                        'title': snippet['title'],
                        'published': snippet.get('publishedAt', ''),
                        'views': int(stats.get('viewCount', 0))
                    })
                else:
                    pending.append({
                        'id': video_id,
                        'title': snippet['title'],
                        'status': privacy,
                        'privacy': status.get('privacyStatus', '')
                    })
        
        print(f"\n[STATUS BREAKDOWN]")
        print(f"   Processing/Uploaded: {len(processing)}")
        print(f"   Public/Published: {len(public)}")
        print(f"   Other/Pending: {len(pending)}")
        
        if processing:
            print(f"\n[PROCESSING VIDEOS] ({len(processing)} still being processed by YouTube):")
            for i, v in enumerate(processing[:10], 1):
                print(f"   {i}. {v['title'][:60]}")
                print(f"      Status: {v['privacy']} | Views: {v['views']}")
        
        if pending:
            print(f"\n[PENDING/ISSUES] ({len(pending)} videos with issues):")
            for i, v in enumerate(pending[:10], 1):
                print(f"   {i}. {v['title'][:60]}")
                print(f"      Status: {v['status']} | Privacy: {v['privacy']}")
        
        print(f"\n[RECENT PUBLIC] (Last 5 published videos):")
        for i, v in enumerate(sorted(public, key=lambda x: x['published'], reverse=True)[:5], 1):
            print(f"   {i}. {v['title'][:60]}")
            print(f"      Views: {v['views']} | Published: {v['published'][:10]}")
        
        print("\n" + "="*70)
        print("[RECOMMENDATIONS]")
        print("="*70)
        
        if len(processing) > 10:
            print("WARNING: Too many videos stuck processing!")
            print("  - YouTube may be throttling uploads")
            print("  - Wait 1-2 hours before uploading more")
            print("  - Delete failed uploads from Studio manually")
        elif len(processing) > 0:
            print("INFO: Some videos still processing (normal)")
            print("  - YouTube typically processes in 5-30 minutes")
            print("  - Check back in 1 hour")
        
        if len(pending) > 0:
            print("WARNING: Videos with upload issues detected")
            print("  - These may need manual deletion from Studio")
            print("  - Re-upload if content is important")
        
        return {
            'processing': processing,
            'pending': pending,
            'public': public
        }
        
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    get_pending_videos()

