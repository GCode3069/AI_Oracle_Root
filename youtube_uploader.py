#!/usr/bin/env python3
"""
SCARIFY YouTube Uploader - Crash-Resistant Upload System
Handles YouTube uploads with comprehensive error handling, retries, and timeouts
"""

import os
import sys
import pickle
import time
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scarify/Output/upload_log.txt'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class YouTubeUploader:
    """Crash-resistant YouTube uploader with retry logic and timeout handling"""
    
    def __init__(self, credentials_path: str, token_path: Optional[str] = None):
        self.credentials_path = credentials_path
        self.token_path = token_path or os.path.join(os.path.expanduser('~'), '.scarify_youtube_token.pickle')
        self.scopes = ['https://www.googleapis.com/auth/youtube.upload']
        self.youtube_service = None
        self.max_retries = 3
        self.upload_timeout = 300  # 5 minutes
        self.chunk_size = 1024 * 1024  # 1MB chunks
        
    def authenticate(self) -> bool:
        """Authenticate with YouTube API with retry logic"""
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Authentication attempt {attempt + 1}/{self.max_retries}")
                
                creds = None
                if os.path.exists(self.token_path):
                    with open(self.token_path, 'rb') as token:
                        creds = pickle.load(token)
                
                if not creds or not creds.valid:
                    if creds and creds.expired and creds.refresh_token:
                        try:
                            creds.refresh(Request())
                        except RefreshError:
                            logger.warning("Token refresh failed, re-authenticating")
                            creds = None
                    
                    if not creds:
                        if not os.path.exists(self.credentials_path):
                            logger.error(f"Credentials file not found: {self.credentials_path}")
                            return False
                        
                        flow = InstalledAppFlow.from_client_secrets_file(
                            self.credentials_path, self.scopes
                        )
                        creds = flow.run_local_server(port=8080, timeout=60)
                    
                    # Save credentials
                    with open(self.token_path, 'wb') as token:
                        pickle.dump(creds, token)
                
                self.youtube_service = build('youtube', 'v3', credentials=creds)
                logger.info("✅ YouTube authentication successful")
                return True
                
            except Exception as e:
                logger.error(f"Authentication attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(5)
                else:
                    logger.error("❌ All authentication attempts failed")
                    return False
        
        return False
    
    def upload_video(self, video_path: str, title: str, description: str = "", 
                    tags: list = None, privacy_status: str = "public") -> Optional[str]:
        """Upload video to YouTube with comprehensive error handling"""
        
        if not self.youtube_service:
            logger.error("Not authenticated. Call authenticate() first.")
            return None
        
        if not os.path.exists(video_path):
            logger.error(f"Video file not found: {video_path}")
            return None
        
        video_id = None
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Upload attempt {attempt + 1}/{self.max_retries} for: {title}")
                
                # Prepare video metadata
                body = {
                    'snippet': {
                        'title': title,
                        'description': description,
                        'tags': tags or ['scarify', 'ai', 'horror', 'mystery'],
                        'categoryId': '22'  # People & Blogs
                    },
                    'status': {
                        'privacyStatus': privacy_status,
                        'selfDeclaredMadeForKids': False
                    }
                }
                
                # Create media upload
                media = MediaFileUpload(
                    video_path, 
                    chunksize=self.chunk_size, 
                    resumable=True
                )
                
                # Start upload
                request = self.youtube_service.videos().insert(
                    part='snippet,status',
                    body=body,
                    media_body=media
                )
                
                # Execute upload with timeout
                response = None
                start_time = time.time()
                
                while response is None:
                    if time.time() - start_time > self.upload_timeout:
                        raise TimeoutError(f"Upload timeout after {self.upload_timeout} seconds")
                    
                    try:
                        status, response = request.next_chunk()
                        if status:
                            progress = int(status.progress() * 100)
                            logger.info(f"Upload progress: {progress}%")
                    except Exception as chunk_error:
                        logger.warning(f"Chunk error: {chunk_error}")
                        time.sleep(2)
                        continue
                
                if response and 'id' in response:
                    video_id = response['id']
                    video_url = f"https://youtube.com/watch?v={video_id}"
                    logger.info(f"✅ Upload successful: {video_url}")
                    return video_id
                else:
                    raise Exception("Upload completed but no video ID returned")
                    
            except TimeoutError as e:
                logger.error(f"Upload timeout: {e}")
                if attempt < self.max_retries - 1:
                    logger.info("Retrying upload...")
                    time.sleep(10)
                else:
                    logger.error("❌ Upload failed after all retries")
                    return None
                    
            except Exception as e:
                logger.error(f"Upload attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    logger.info("Retrying upload...")
                    time.sleep(10)
                else:
                    logger.error("❌ Upload failed after all retries")
                    return None
        
        return video_id

def main():
    """Main function for command line usage"""
    if len(sys.argv) < 3:
        print("Usage: python youtube_uploader.py <video_path> <title> [description]")
        sys.exit(1)
    
    video_path = sys.argv[1]
    title = sys.argv[2]
    description = sys.argv[3] if len(sys.argv) > 3 else ""
    
    # Configuration
    credentials_path = "credentials/client_secrets.json"
    
    # Create uploader
    uploader = YouTubeUploader(credentials_path)
    
    # Authenticate
    if not uploader.authenticate():
        logger.error("❌ Authentication failed")
        sys.exit(1)
    
    # Upload video
    video_id = uploader.upload_video(
        video_path=video_path,
        title=title,
        description=description,
        tags=['scarify', 'ai', 'horror', 'mystery', 'exvet', 'rebel']
    )
    
    if video_id:
        print(f"✅ SUCCESS: https://youtube.com/watch?v={video_id}")
        sys.exit(0)
    else:
        print("❌ Upload failed")
        sys.exit(1)

if __name__ == "__main__":
    main()