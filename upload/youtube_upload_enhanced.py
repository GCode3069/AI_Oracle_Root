#!/usr/bin/env python3
"""
SCARIFY Enhanced YouTube Uploader
Multiple fallback methods for reliable uploads
"""

import os
import sys
import pickle
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError
    YOUTUBE_API_AVAILABLE = True
except ImportError:
    YOUTUBE_API_AVAILABLE = False
    print("⚠️  YouTube API libraries not installed. Install with: pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client")

try:
    import yt_dlp
    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False

try:
    from yt_uploader import upload_video as yt_uploader_upload
    YT_UPLOADER_AVAILABLE = True
except ImportError:
    YT_UPLOADER_AVAILABLE = False


class YouTubeUploaderEnhanced:
    """Enhanced YouTube uploader with multiple fallback methods"""
    
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    API_SERVICE_NAME = 'youtube'
    API_VERSION = 'v3'
    MAX_FILE_SIZE = 256 * 1024 * 1024  # 256 MB
    
    def __init__(self, base_path: Optional[Path] = None):
        """Initialize uploader"""
        if base_path is None:
            # Try to detect project root
            current = Path(__file__).parent
            if (current.parent / "abraham_horror").exists():
                base_path = current.parent
            else:
                base_path = Path("/workspace")
        
        self.base_path = Path(base_path)
        self.config_dir = self.base_path / "config" / "credentials" / "youtube"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.client_secrets_file = self.config_dir / "client_secrets.json"
        self.token_file = self.config_dir / "token.pickle"
        self.youtube = None
        self.credentials = None
        
        self._check_setup()
    
    def _check_setup(self):
        """Check if credentials are configured"""
        if not self.client_secrets_file.exists():
            print("\n" + "="*80)
            print("⚠️  YOUTUBE API CREDENTIALS NOT FOUND")
            print("="*80)
            print("\nSetup Instructions:")
            print("1. Go to: https://console.cloud.google.com/")
            print("2. Create a new project (or select existing)")
            print("3. Enable YouTube Data API v3")
            print("4. Create OAuth 2.0 credentials (Desktop app)")
            print("5. Download client_secrets.json")
            print(f"6. Save it to: {self.client_secrets_file.absolute()}")
            print("\n" + "="*80)
            
            # Create placeholder
            placeholder = {
                "installed": {
                    "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
                    "project_id": "your-project-id",
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_secret": "YOUR_CLIENT_SECRET",
                    "redirect_uris": ["http://localhost"]
                }
            }
            with open(self.client_secrets_file, 'w') as f:
                json.dump(placeholder, f, indent=2)
    
    def try_youtube_api(self, video_path: str, title: str, description: str, tags: list) -> Dict:
        """Method 1: YouTube Data API v3 (official)"""
        if not YOUTUBE_API_AVAILABLE:
            return {"status": "SKIPPED", "reason": "API libraries not installed"}
        
        try:
            # Authenticate
            if not self.youtube:
                if not self.authenticate():
                    return {"status": "FAILED", "reason": "Authentication failed"}
            
            # Validate file
            video_path_obj = Path(video_path)
            if not video_path_obj.exists():
                return {"status": "FAILED", "reason": f"File not found: {video_path}"}
            
            file_size = video_path_obj.stat().st_size
            if file_size > self.MAX_FILE_SIZE:
                return {"status": "FAILED", "reason": f"File too large: {file_size/1024/1024:.1f} MB"}
            
            # Prepare metadata
            body = {
                'snippet': {
                    'title': title[:100],  # YouTube limit
                    'description': description[:5000],  # YouTube limit
                    'tags': tags[:50],  # YouTube limit
                    'categoryId': '22'  # People & Blogs
                },
                'status': {
                    'privacyStatus': 'public',
                    'selfDeclaredMadeForKids': False
                }
            }
            
            # Upload
            media = MediaFileUpload(
                str(video_path),
                chunksize=1024*1024,
                resumable=True,
                mimetype='video/mp4'
            )
            
            request = self.youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            # Execute with progress
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    print(f"   Progress: {progress}%", end='\r')
            
            print()  # New line
            
            video_id = response['id']
            video_url = f"https://youtube.com/watch?v={video_id}"
            
            return {
                "status": "SUCCESS",
                "method": "youtube_api",
                "url": video_url,
                "video_id": video_id
            }
            
        except HttpError as e:
            if e.resp.status == 403:
                return {"status": "FAILED", "reason": "Quota exceeded or API not enabled"}
            return {"status": "FAILED", "reason": f"HTTP Error: {e}"}
        except Exception as e:
            return {"status": "FAILED", "reason": str(e)}
    
    def try_yt_dlp(self, video_path: str, title: str, description: str, tags: list) -> Dict:
        """Method 2: yt-dlp upload (requires yt-dlp with upload support)"""
        if not YT_DLP_AVAILABLE:
            return {"status": "SKIPPED", "reason": "yt-dlp not installed"}
        
        try:
            # yt-dlp doesn't natively support uploads, but we can use it for validation
            # This is a placeholder - actual upload would need custom implementation
            return {"status": "SKIPPED", "reason": "yt-dlp upload not implemented (requires custom solution)"}
        except Exception as e:
            return {"status": "FAILED", "reason": str(e)}
    
    def try_yt_uploader(self, video_path: str, title: str, description: str, tags: list) -> Dict:
        """Method 3: yt-uploader library (third-party)"""
        if not YT_UPLOADER_AVAILABLE:
            return {"status": "SKIPPED", "reason": "yt-uploader not installed"}
        
        try:
            result = yt_uploader_upload(
                video_path=video_path,
                title=title,
                description=description,
                tags=tags
            )
            if result and result.get('success'):
                return {
                    "status": "SUCCESS",
                    "method": "yt_uploader",
                    "url": result.get('url', '')
                }
            return {"status": "FAILED", "reason": "Upload returned failure"}
        except Exception as e:
            return {"status": "FAILED", "reason": str(e)}
    
    def generate_manual_instructions(self, video_path: str, title: str, description: str, tags: list) -> Dict:
        """Method 4: Generate manual upload instructions"""
        instructions_file = self.base_path / "upload" / "manual_upload_instructions.txt"
        
        instructions = f"""
================================================================================
                    MANUAL YOUTUBE UPLOAD INSTRUCTIONS
================================================================================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

VIDEO FILE:
{video_path}

TITLE:
{title}

DESCRIPTION:
{description}

TAGS:
{', '.join(tags)}

STEPS:
1. Go to: https://studio.youtube.com/
2. Click "Create" → "Upload video"
3. Select file: {video_path}
4. Paste title: {title}
5. Paste description (below)
6. Add tags: {', '.join(tags[:20])}
7. Set visibility: Public
8. Click "Publish"

================================================================================
"""
        
        instructions_file.parent.mkdir(parents=True, exist_ok=True)
        with open(instructions_file, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        print(f"\n📋 Manual upload instructions saved to: {instructions_file}")
        print(instructions)
        
        return {
            "status": "MANUAL_REQUIRED",
            "method": "manual_instructions",
            "instructions_file": str(instructions_file)
        }
    
    def authenticate(self) -> bool:
        """Authenticate with YouTube API"""
        if not YOUTUBE_API_AVAILABLE:
            return False
        
        try:
            # Load existing credentials
            if self.token_file.exists():
                with open(self.token_file, 'rb') as token:
                    self.credentials = pickle.load(token)
            
            # Refresh or get new credentials
            if not self.credentials or not self.credentials.valid:
                if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                    self.credentials.refresh(Request())
                else:
                    if not self.client_secrets_file.exists():
                        print("❌ client_secrets.json not found. See setup instructions above.")
                        return False
                    
                    flow = InstalledAppFlow.from_client_secrets_file(
                        str(self.client_secrets_file), self.SCOPES
                    )
                    self.credentials = flow.run_local_server(
                        port=8080,
                        prompt='consent',
                        success_message='Authentication successful! You can close this window.'
                    )
                
                # Save credentials
                with open(self.token_file, 'wb') as token:
                    pickle.dump(self.credentials, token)
            
            # Build YouTube service
            self.youtube = build(
                self.API_SERVICE_NAME,
                self.API_VERSION,
                credentials=self.credentials
            )
            
            return True
            
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return False
    
    def upload_video(
        self,
        video_path: str,
        title: str,
        description: str = "",
        tags: list = None
    ) -> Dict:
        """
        Upload video using multiple fallback methods
        
        Args:
            video_path: Path to video file
            title: Video title
            description: Video description
            tags: List of tags
        
        Returns:
            Dict with status, method, and URL/instructions
        """
        if tags is None:
            tags = ["shorts", "youtube shorts", "viral", "comedy"]
        
        print(f"\n📤 YouTube Upload: {Path(video_path).name}")
        print(f"   Title: {title[:60]}...")
        
        # Try methods in order
        methods = [
            ("YouTube API", self.try_youtube_api),
            ("yt-uploader", self.try_yt_uploader),
            ("yt-dlp", self.try_yt_dlp),
        ]
        
        for method_name, method_func in methods:
            print(f"\n   Trying {method_name}...")
            result = method_func(video_path, title, description, tags)
            
            if result.get("status") == "SUCCESS":
                print(f"   ✅ Success via {method_name}!")
                return result
            elif result.get("status") == "SKIPPED":
                print(f"   ⏭️  {method_name} skipped: {result.get('reason')}")
            else:
                print(f"   ❌ {method_name} failed: {result.get('reason')}")
        
        # All automated methods failed - generate manual instructions
        print("\n   ⚠️  All automated methods failed. Generating manual instructions...")
        return self.generate_manual_instructions(video_path, title, description, tags)


def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Enhanced YouTube Uploader')
    parser.add_argument('video', help='Path to video file')
    parser.add_argument('--title', required=True, help='Video title')
    parser.add_argument('--description', default='', help='Video description')
    parser.add_argument('--tags', nargs='+', default=['shorts'], help='Video tags')
    parser.add_argument('--test-auth', action='store_true', help='Test authentication only')
    
    args = parser.parse_args()
    
    uploader = YouTubeUploaderEnhanced()
    
    if args.test_auth:
        print("\n🔧 Testing YouTube Authentication")
        if uploader.authenticate():
            print("✅ Authentication successful!")
            # Get channel info
            try:
                request = uploader.youtube.channels().list(part='snippet,statistics', mine=True)
                response = request.execute()
                if response['items']:
                    channel = response['items'][0]
                    print(f"   Channel: {channel['snippet']['title']}")
                    print(f"   Subscribers: {channel['statistics'].get('subscriberCount', '0')}")
            except Exception as e:
                print(f"   ⚠️  Could not get channel info: {e}")
        else:
            print("❌ Authentication failed")
        sys.exit(0)
    
    if not Path(args.video).exists():
        print(f"❌ Video not found: {args.video}")
        sys.exit(1)
    
    result = uploader.upload_video(
        video_path=args.video,
        title=args.title,
        description=args.description,
        tags=args.tags
    )
    
    if result.get("status") == "SUCCESS":
        print(f"\n✅ Upload successful!")
        print(f"   URL: {result.get('url')}")
        sys.exit(0)
    elif result.get("status") == "MANUAL_REQUIRED":
        print(f"\n📋 Manual upload required. Instructions saved.")
        sys.exit(0)
    else:
        print(f"\n❌ Upload failed")
        sys.exit(1)


if __name__ == '__main__':
    main()
