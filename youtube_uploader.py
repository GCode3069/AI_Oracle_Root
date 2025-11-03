#!/usr/bin/env python3
"""
SCARIFY YouTube Uploader
OAuth 2.0 authenticated YouTube Shorts uploader
"""

import os
import sys
import pickle
from pathlib import Path
from datetime import datetime

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError
except ImportError:
    print("❌ Missing YouTube API dependencies. Installing...")
    import subprocess
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", 
        "google-auth-oauthlib", "google-auth-httplib2", "google-api-python-client"
    ])
    print("✅ Dependencies installed. Please restart the script.")
    sys.exit(1)


class YouTubeUploader:
    """YouTube OAuth 2.0 uploader for Shorts with Multi-Channel Rotation"""
    
    # OAuth 2.0 scopes
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    # Multi-Channel Configuration
    CHANNELS = {
        "the_vet_edge": {
            "name": "The Vet Edge",
            "token_file": Path("config/credentials/youtube/the_vet_edge_token.pickle"),
            "focus": "business_tactics",
            "daily_limit": 20,
            "upload_count": 0
        },
        "scarify_archive": {
            "name": "SCARIFY Archive", 
            "token_file": Path("config/credentials/youtube/scarify_archive_token.pickle"),
            "focus": "backup_testing",
            "daily_limit": 10,
            "upload_count": 0
        },
        "btc_empire": {
            "name": "BTC Empire",
            "token_file": Path("config/credentials/youtube/btc_empire_token.pickle"), 
            "focus": "crypto_business",
            "daily_limit": 15,
            "upload_count": 0
        }
    }
    
    # File paths
    CLIENT_SECRETS_FILE = Path("config/credentials/youtube/client_secrets.json")
    TOKEN_FILE = Path("config/credentials/youtube/token.pickle")
    
    # YouTube API settings
    API_SERVICE_NAME = 'youtube'
    API_VERSION = 'v3'
    
    # Shorts requirements
    MAX_FILE_SIZE = 256 * 1024 * 1024  # 256 MB
    DAILY_QUOTA_LIMIT = 50  # YouTube allows ~50 uploads/day
    
    def __init__(self):
        """Initialize YouTube uploader with multi-channel support"""
        self.youtube = None
        self.credentials = None
        self.upload_count_today = 0
        self.current_channel = "the_vet_edge"
        self.channel_rotation_enabled = True
        self._check_credentials_setup()
    
    def _check_credentials_setup(self):
        """Check if YouTube API credentials are configured"""
        if not self.CLIENT_SECRETS_FILE.exists():
            print("\n" + "="*80)
            print("⚠️  YOUTUBE API CREDENTIALS NOT FOUND")
            print("="*80)
            print("\nYou need to set up YouTube OAuth 2.0 credentials:")
            print("\n1. Go to: https://console.cloud.google.com/")
            print("2. Create a new project (or select existing)")
            print("3. Enable YouTube Data API v3")
            print("4. Create OAuth 2.0 credentials (Desktop app)")
            print("5. Download client_secrets.json")
            print(f"6. Save it to: {self.CLIENT_SECRETS_FILE.absolute()}")
            print("\n" + "="*80)
            print("\nFull setup guide:")
            print("https://developers.google.com/youtube/v3/getting-started")
            print("="*80 + "\n")
            
            # Create directory structure
            self.CLIENT_SECRETS_FILE.parent.mkdir(parents=True, exist_ok=True)
            
            # Create placeholder file with instructions
            setup_instructions = {
                "README": "Place your client_secrets.json here",
                "steps": [
                    "1. Go to https://console.cloud.google.com/",
                    "2. Create project",
                    "3. Enable YouTube Data API v3",
                    "4. Create OAuth 2.0 credentials (Desktop app)",
                    "5. Download as client_secrets.json",
                    "6. Replace this file with your downloaded file"
                ]
            }
            
            import json
            with open(self.CLIENT_SECRETS_FILE, 'w') as f:
                json.dump(setup_instructions, f, indent=2)
            
            raise FileNotFoundError(
                f"YouTube credentials not configured. "
                f"See: {self.CLIENT_SECRETS_FILE.absolute()}"
            )
    
    def authenticate(self) -> bool:
        """
        Authenticate with YouTube using OAuth 2.0
        
        Returns:
            True if authentication successful
        """
        print("\n🔐 YouTube Authentication")
        
        try:
            # Load existing credentials
            if self.TOKEN_FILE.exists():
                print("   Loading saved credentials...")
                with open(self.TOKEN_FILE, 'rb') as token:
                    self.credentials = pickle.load(token)
            
            # Refresh or get new credentials
            if not self.credentials or not self.credentials.valid:
                if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                    print("   Refreshing expired token...")
                    self.credentials.refresh(Request())
                else:
                    print("   Starting OAuth 2.0 flow...")
                    print("   ⚠️  Browser will open for authentication")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        str(self.CLIENT_SECRETS_FILE), self.SCOPES
                    )
                    self.credentials = flow.run_local_server(
                        port=8080,
                        prompt='consent',
                        success_message='Authentication successful! You can close this window.'
                    )
                
                # Save credentials
                self.TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
                with open(self.TOKEN_FILE, 'wb') as token:
                    pickle.dump(self.credentials, token)
                print("   ✅ Credentials saved")
            
            # Build YouTube service
            self.youtube = build(
                self.API_SERVICE_NAME,
                self.API_VERSION,
                credentials=self.credentials
            )
            
            print("   ✅ Authentication successful")
            return True
            
        except Exception as e:
            print(f"   ❌ Authentication failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def upload(
        self,
        video_path: str,
        pain_point: str,
        gumroad_url: str = "https://gumroad.com/l/buy-rebel-97"
    ) -> str:
        """
        Upload video to YouTube as a Short with optimized metadata
        
        Args:
            video_path: Path to MP4 file
            pain_point: Pain point text for title/description
            gumroad_url: Product link
            
        Returns:
            YouTube video URL or empty string on failure
        """
        print(f"\n📤 YouTube Upload (Optimized)")
        print(f"   File: {Path(video_path).name}")
        
        # Validate file
        if not os.path.exists(video_path):
            print(f"   ❌ File not found: {video_path}")
            return ""
        
        file_size = os.path.getsize(video_path)
        if file_size > self.MAX_FILE_SIZE:
            print(f"   ❌ File too large: {file_size/1024/1024:.1f} MB (max 256 MB)")
            return ""
        
        print(f"   Size: {file_size/1024/1024:.1f} MB")
        
        # Check quota
        if self.upload_count_today >= self.DAILY_QUOTA_LIMIT:
            print(f"   ⚠️  Daily quota reached ({self.DAILY_QUOTA_LIMIT} uploads)")
            return ""
        
        # Authenticate if needed
        if not self.youtube:
            if not self.authenticate():
                return ""
        
        # Optimize title (front-load pain point for algorithm)
        # Extract first key phrase (before dash)
        title_hook = pain_point.split('–')[0].split('-')[0].strip()
        title = f"{title_hook[:40]} | Ex-Vet $97 Emergency Kit #Shorts"
        
        # Optimize description (algorithm-friendly with keywords)
        description = f"""{pain_point}

⚠️ PROBLEM SOLVED: Ex-veteran garage owner reveals the $97 emergency kit that fixes this crisis in 48 hours.

🔗 Get the Ex-Vet Emergency Business Kit: {gumroad_url}

💡 What's inside:
• Crisis response protocols
• Cash flow emergency templates  
• Veteran-tested systems
• Small business survival tactics

This is the same kit that saved my business during the supply chain meltdown. Now helping 1000+ small business owners.

#Shorts #SmallBusiness #Entrepreneur #BusinessTips #VeteranOwned #GarageOwner #BusinessGrowth #StartupLife"""
        
        # Optimize tags (mix of broad + specific)
        tags = [
            "shorts",
            "short",
            "youtube shorts",
            "business",
            "small business",
            "entrepreneur",
            "entrepreneurship",
            "startup",
            "business tips",
            "business advice",
            "small business owner",
            "business growth",
            "veteran owned",
            "garage business",
            "mechanic business",
            "plumber business",
            "barber business",
            "welder business",
            "business problems",
            "cash flow",
            "scarify"
        ]
        
        # YouTube Shorts indicator (vertical video + #Shorts tag)
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': '22'  # People & Blogs
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
            }
        }
        
        print(f"   Title: {title}")
        print(f"   Uploading...")
        
        try:
            # Upload video
            media = MediaFileUpload(
                video_path,
                chunksize=1024*1024,  # 1MB chunks
                resumable=True,
                mimetype='video/mp4'
            )
            
            request = self.youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            # Execute upload with progress
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    print(f"   Progress: {progress}%", end='\r')
            
            print()  # New line after progress
            
            # Get video ID and URL
            video_id = response['id']
            video_url = f"https://youtube.com/shorts/{video_id}"
            
            self.upload_count_today += 1
            
            print("   ✅ Upload successful!")
            print(f"   🔗 URL: {video_url}")
            print(f"   📊 Daily uploads: {self.upload_count_today}/{self.DAILY_QUOTA_LIMIT}")
            
            return video_url
            
        except HttpError as e:
            print(f"\n   ❌ YouTube API error: {e}")
            if e.resp.status == 403:
                print("   ⚠️  Quota exceeded or API not enabled")
            return ""
            
        except Exception as e:
            print(f"\n   ❌ Upload failed: {e}")
            import traceback
            traceback.print_exc()
            return ""
    
    def get_channel_info(self) -> dict:
        """Get authenticated channel information"""
        if not self.youtube:
            if not self.authenticate():
                return {}
        
        try:
            request = self.youtube.channels().list(
                part='snippet,statistics',
                mine=True
            )
            response = request.execute()
            
            if response['items']:
                channel = response['items'][0]
                return {
                    'title': channel['snippet']['title'],
                    'subscribers': channel['statistics'].get('subscriberCount', '0'),
                    'videos': channel['statistics'].get('videoCount', '0')
                }
        except Exception as e:
            print(f"Error getting channel info: {e}")
        
        return {}


def main():
    """Test the uploader"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Upload video to YouTube Shorts')
    parser.add_argument('video', help='Path to video file')
    parser.add_argument('--pain-point', default='Test upload', help='Pain point text')
    parser.add_argument('--test-auth', action='store_true', help='Test authentication only')
    
    args = parser.parse_args()
    
    uploader = YouTubeUploader()
    
    if args.test_auth:
        print("\n🔧 Testing YouTube Authentication")
        if uploader.authenticate():
            info = uploader.get_channel_info()
            if info:
                print(f"\n✅ Connected to channel: {info['title']}")
                print(f"   Subscribers: {info['subscribers']}")
                print(f"   Videos: {info['videos']}")
        sys.exit(0)
    
    if not os.path.exists(args.video):
        print(f"❌ Video not found: {args.video}")
        sys.exit(1)
    
    url = uploader.upload(args.video, args.pain_point)
    sys.exit(0 if url else 1)


if __name__ == '__main__':
    main()


