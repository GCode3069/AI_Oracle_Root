"""
YOUTUBE ANALYTICS + GOOGLE SHEETS INTEGRATION
Syncs YouTube performance data to Google Sheets for analysis
Pulls headlines from Sheets for video generation
"""
import sys, json, time
from pathlib import Path
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials as ServiceCreds
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
CHANNEL_ID = "UCS5pEpSCw8k4wene0iv0uAg"

# Google Sheets
SHEET_ID = "1qu10uvlQCZI5lkEb_M5wQtrwA6YiF8rbyjIdiE09whc"
SERVICE_ACCOUNT = Path("F:/AI_Oracle_Root/scarify/config/credentials/google/service_account.json")

# YouTube API
YOUTUBE_SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

class YouTubeSheetsSync:
    """Sync YouTube analytics to Google Sheets"""
    
    def __init__(self):
        self.sheet = None
        self.youtube = None
        self.setup_sheets()
        self.setup_youtube()
    
    def setup_sheets(self):
        """Connect to Google Sheets"""
        print("[SHEETS] Connecting to Google Sheets...")
        
        try:
            scopes = ['https://www.googleapis.com/auth/spreadsheets']
            creds = ServiceCreds.from_service_account_file(str(SERVICE_ACCOUNT), scopes=scopes)
            client = gspread.authorize(creds)
            self.sheet = client.open_by_key(SHEET_ID)
            print(f"[SHEETS] OK Connected: {self.sheet.title}")
        except Exception as e:
            print(f"[SHEETS] ERROR: {e}")
    
    def setup_youtube(self):
        """Connect to YouTube API"""
        print("[YOUTUBE] Connecting to YouTube API...")
        
        try:
            token_file = BASE / "youtube_token.pickle"
            creds = None
            
            if token_file.exists():
                with open(token_file, 'rb') as token:
                    creds = pickle.load(token)
            
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    client_file = Path("F:/AI_Oracle_Root/scarify/client_secret_679199614743-1fq6sini3p9kjs237ek4seg4ojp4a4qe.apps.googleusercontent.com.json")
                    if client_file.exists():
                        flow = InstalledAppFlow.from_client_secrets_file(str(client_file), YOUTUBE_SCOPES)
                        creds = flow.run_local_server(port=0)
                    
                with open(token_file, 'wb') as token:
                    pickle.dump(creds, token)
            
            self.youtube = build('youtube', 'v3', credentials=creds)
            print("[YOUTUBE] OK Connected")
        except Exception as e:
            print(f"[YOUTUBE] ERROR: {e}")
    
    def get_top_performers(self, limit=20):
        """Get top performing videos from YouTube"""
        print(f"\n[YOUTUBE] Fetching top {limit} performers...")
        
        try:
            # Get uploads playlist
            channel_request = self.youtube.channels().list(
                part='contentDetails',
                id=CHANNEL_ID
            )
            response = channel_request.execute()
            
            uploads_playlist = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            # Get recent videos
            playlist_request = self.youtube.playlistItems().list(
                part='snippet,contentDetails',
                playlistId=uploads_playlist,
                maxResults=50
            )
            playlist_response = playlist_request.execute()
            
            videos = []
            for item in playlist_response.get('items', []):
                video_id = item['contentDetails']['videoId']
                
                # Get stats
                video_request = self.youtube.videos().list(
                    part='statistics,snippet',
                    id=video_id
                )
                video_response = video_request.execute()
                
                if video_response.get('items'):
                    video = video_response['items'][0]
                    stats = video['statistics']
                    snippet = video['snippet']
                    
                    videos.append({
                        'video_id': video_id,
                        'title': snippet['title'],
                        'published': snippet['publishedAt'],
                        'views': int(stats.get('viewCount', 0)),
                        'likes': int(stats.get('likeCount', 0)),
                        'comments': int(stats.get('commentCount', 0)),
                        'url': f"https://www.youtube.com/watch?v={video_id}"
                    })
            
            # Sort by views
            videos.sort(key=lambda x: x['views'], reverse=True)
            
            print(f"[YOUTUBE] OK Fetched {len(videos)} videos")
            return videos[:limit]
            
        except Exception as e:
            print(f"[YOUTUBE] ERROR: {e}")
            return []
    
    def sync_to_sheets(self, videos):
        """Sync video data to Google Sheets"""
        print(f"\n[SYNC] Writing {len(videos)} videos to Sheets...")
        
        try:
            # Get or create worksheet
            try:
                worksheet = self.sheet.worksheet("Analytics")
            except:
                worksheet = self.sheet.add_worksheet("Analytics", rows=100, cols=10)
            
            # Clear existing data
            worksheet.clear()
            
            # Headers
            headers = [
                "Rank", "Title", "Views", "Likes", "Comments", 
                "Published Date", "Video URL", "Last Updated"
            ]
            worksheet.update('A1:H1', [headers])
            
            # Data rows
            data = []
            for i, video in enumerate(videos, 1):
                row = [
                    i,
                    video['title'],
                    video['views'],
                    video['likes'],
                    video['comments'],
                    video['published'][:10],  # Just date
                    video['url'],
                    datetime.now().strftime("%Y-%m-%d %H:%M")
                ]
                data.append(row)
            
            # Write data
            if data:
                worksheet.update(f'A2:H{len(data)+1}', data)
            
            print(f"[SYNC] OK Updated {len(data)} rows")
            print(f"[SYNC] Sheet: https://docs.google.com/spreadsheets/d/{SHEET_ID}")
            
            return True
            
        except Exception as e:
            print(f"[SYNC] ERROR: {e}")
            return False
    
    def get_headlines_from_sheets(self):
        """Get headlines from Sheets for video generation"""
        print("\n[SHEETS] Reading headlines for generation...")
        
        try:
            worksheet = self.sheet.worksheet("Headlines")
            rows = worksheet.get_all_values()
            
            headlines = []
            for row in rows[1:]:  # Skip header
                if len(row) > 0 and row[0]:
                    headlines.append(row[0])
            
            print(f"[SHEETS] OK Found {len(headlines)} headlines")
            return headlines
            
        except Exception as e:
            print(f"[SHEETS] INFO: No Headlines worksheet (creating...)")
            try:
                worksheet = self.sheet.add_worksheet("Headlines", rows=100, cols=5)
                worksheet.update('A1:E1', [["Headline", "Category", "Priority", "Used", "Generated Video"]])
                
                # Add sample headlines
                samples = [
                    ["AI Healthcare Algorithm Denies Coverage", "Tech/AI", "High", "", ""],
                    ["Government Surveillance Expands Nationwide", "Politics", "High", "", ""],
                    ["Market Crash Predicted by Economic Models", "Economy", "Medium", "", ""],
                    ["Social Credit Scores Test in Major City", "Tech/AI", "High", "", ""],
                    ["Privacy Laws Weakened in Latest Bill", "Privacy", "High", "", ""]
                ]
                worksheet.update('A2:E6', samples)
                print("[SHEETS] OK Created Headlines worksheet with samples")
                return [s[0] for s in samples]
            except Exception as e2:
                print(f"[SHEETS] ERROR: {e2}")
                return []
    
    def run_full_sync(self):
        """Run complete sync operation"""
        print("\n" + "="*70)
        print("YOUTUBE <-> GOOGLE SHEETS SYNC")
        print("="*70)
        
        # Get YouTube data
        videos = self.get_top_performers(20)
        
        if videos:
            # Sync to Sheets
            self.sync_to_sheets(videos)
            
            # Print summary
            print("\n[SUMMARY]")
            print(f"   Videos synced: {len(videos)}")
            print(f"   Top performer: {videos[0]['title'][:50]} ({videos[0]['views']} views)")
            print(f"   Sheet: https://docs.google.com/spreadsheets/d/{SHEET_ID}")
        
        # Get headlines for future generation
        headlines = self.get_headlines_from_sheets()
        
        if headlines:
            print(f"\n[HEADLINES] {len(headlines)} headlines ready for generation")
            print(f"   Examples:")
            for h in headlines[:3]:
                print(f"   - {h[:60]}")
        
        print("\n" + "="*70)
        print("[SYNC COMPLETE]")
        print("="*70)
        
        return {
            'videos_synced': len(videos),
            'headlines_available': len(headlines),
            'sheet_url': f"https://docs.google.com/spreadsheets/d/{SHEET_ID}"
        }

def main():
    """Main execution"""
    sync = YouTubeSheetsSync()
    result = sync.run_full_sync()
    
    print("\n[NEXT STEPS]")
    print("   1. Check Google Sheet for analytics data")
    print("   2. Add headlines to 'Headlines' worksheet")
    print("   3. Run video generators using Sheet headlines")
    print(f"\n   Sheet URL: {result['sheet_url']}")

if __name__ == "__main__":
    main()

