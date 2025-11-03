#!/usr/bin/env python3
"""
SCARIFY - MULTI-CHANNEL YOUTUBE SETUP
Creates and manages 15 YouTube channels for content distribution
"""

import os, json, pickle, random, time
from pathlib import Path
from datetime import datetime

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from google.auth.transport.requests import Request
    YOUTUBE_AVAILABLE = True
except ImportError:
    print("[WARNING] YouTube API not available. Install: pip install google-api-python-client google-auth-oauthlib")
    YOUTUBE_AVAILABLE = False

BASE_DIR = Path("F:/AI_Oracle_Root/scarify")
CHANNELS_DIR = BASE_DIR / "channels"
CHANNELS_DIR.mkdir(exist_ok=True)

SCOPES = ['https://www.googleapis.com/auth/youtube.upload', 
          'https://www.googleapis.com/auth/youtube']

CLIENT_SECRETS = BASE_DIR / "config/credentials/youtube/client_secrets.json"

# Channel name templates
CHANNEL_NAMES = [
    "Abraham Speaks Truth",
    "Lincoln's Warning",
    "Honest Abe Uncensored", 
    "The Lincoln Chronicles",
    "President's Ghost",
    "Ford Theatre Truth",
    "Lincoln Unfiltered",
    "Abe's Prophecy",
    "The Great Emancipator",
    "Lincoln Decoded",
    "Whispers from Ford's",
    "Abraham's Testament",
    "Lincoln Reborn",
    "The President Speaks",
    "Truth from Beyond"
]

# Channel descriptions
CHANNEL_DESC_TEMPLATES = [
    "Abraham Lincoln's ghost speaks truth to power. Horror shorts exposing modern corruption. Bitcoin: bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt",
    "From Ford's Theatre, Lincoln warns of America's fall. Support the truth: bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt",
    "The 16th President returns with warnings for 2025. Rebel Kit: trenchaikits.com/buy-rebel-$97",
    "Lincoln's assassination was a warning. Yours is a choice. BTC: bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt",
    "Horror shorts featuring Abraham Lincoln's ghostly warnings about modern America. Support: bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"
]

def create_channel_config(channel_id, name):
    """Create configuration for a single channel"""
    return {
        "id": channel_id,
        "name": name,
        "description": random.choice(CHANNEL_DESC_TEMPLATES),
        "created_at": datetime.now().isoformat(),
        "oauth_token_file": f"channel_{channel_id}_token.pickle",
        "upload_count": 0,
        "last_upload": None,
        "performance": {
            "total_views": 0,
            "total_videos": 0,
            "avg_ctr": 0.0,
            "avg_retention": 0.0
        }
    }

def authenticate_channel(channel_num):
    """Authenticate a YouTube channel and save credentials"""
    token_file = CHANNELS_DIR / f"channel_{channel_num}_token.pickle"
    
    creds = None
    
    # Load existing credentials
    if token_file.exists():
        with open(token_file, 'rb') as f:
            creds = pickle.load(f)
    
    # Refresh or get new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                print(f"[{channel_num}] Refreshed existing token")
            except:
                creds = None
        
        if not creds:
            if not CLIENT_SECRETS.exists():
                print(f"[ERROR] Client secrets not found: {CLIENT_SECRETS}")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRETS), 
                SCOPES
            )
            
            print(f"\n[Channel #{channel_num}] Opening browser for authentication...")
            print(f"Please log in with channel account #{channel_num}")
            
            creds = flow.run_local_server(
                port=8080 + channel_num,  # Different port for each channel
                prompt='consent',
                authorization_prompt_message=f'Authenticating SCARIFY Channel #{channel_num}'
            )
        
        # Save credentials
        with open(token_file, 'wb') as f:
            pickle.dump(creds, f)
        
        print(f"[{channel_num}] Token saved: {token_file.name}")
    
    return creds

def get_channel_info(creds):
    """Get channel ID and details"""
    try:
        youtube = build('youtube', 'v3', credentials=creds)
        request = youtube.channels().list(
            part='snippet,statistics',
            mine=True
        )
        response = request.execute()
        
        if response['items']:
            channel = response['items'][0]
            return {
                'id': channel['id'],
                'title': channel['snippet']['title'],
                'subscribers': channel['statistics'].get('subscriberCount', '0'),
                'views': channel['statistics'].get('viewCount', '0'),
                'videos': channel['statistics'].get('videoCount', '0')
            }
    except Exception as e:
        print(f"[ERROR] Failed to get channel info: {e}")
    
    return None

def setup_channels(count=15, start_from=1):
    """Setup multiple YouTube channels"""
    
    if not YOUTUBE_AVAILABLE:
        print("[ERROR] YouTube API libraries not installed")
        return False
    
    if not CLIENT_SECRETS.exists():
        print(f"[ERROR] Client secrets file not found: {CLIENT_SECRETS}")
        print("Please download from Google Cloud Console")
        return False
    
    print(f"\n{'='*70}")
    print(f"SCARIFY - MULTI-CHANNEL SETUP")
    print(f"{'='*70}")
    print(f"Setting up {count} YouTube channels...")
    print(f"Starting from channel #{start_from}")
    print(f"\nNOTE: You'll need to log in {count} times with different YouTube accounts")
    print(f"{'='*70}\n")
    
    channels_config = []
    
    for i in range(start_from, start_from + count):
        print(f"\n{'='*70}")
        print(f"CHANNEL {i}/{start_from + count - 1}")
        print(f"{'='*70}")
        
        # Authenticate
        creds = authenticate_channel(i)
        if not creds:
            print(f"[ERROR] Authentication failed for channel {i}")
            continue
        
        # Get channel info
        info = get_channel_info(creds)
        if not info:
            print(f"[ERROR] Could not retrieve channel info for #{i}")
            continue
        
        # Create config
        config = create_channel_config(info['id'], info['title'])
        config['channel_number'] = i
        config['statistics'] = info
        
        channels_config.append(config)
        
        print(f"\n[SUCCESS] Channel {i} configured:")
        print(f"  Name: {info['title']}")
        print(f"  ID: {info['id']}")
        print(f"  Subscribers: {info['subscribers']}")
        print(f"  Videos: {info['videos']}")
        print(f"  Token: {config['oauth_token_file']}")
        
        # Save individual config
        config_file = CHANNELS_DIR / f"channel_{i}_config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        time.sleep(2)
    
    # Save master config
    master_config = {
        "total_channels": len(channels_config),
        "setup_date": datetime.now().isoformat(),
        "channels": channels_config
    }
    
    master_file = CHANNELS_DIR / "channels_master.json"
    with open(master_file, 'w') as f:
        json.dump(master_config, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"SETUP COMPLETE")
    print(f"{'='*70}")
    print(f"Configured {len(channels_config)}/{count} channels")
    print(f"Master config: {master_file}")
    print(f"{'='*70}\n")
    
    return True

def load_channels():
    """Load all configured channels"""
    master_file = CHANNELS_DIR / "channels_master.json"
    
    if not master_file.exists():
        print("[WARNING] No channels configured yet")
        return []
    
    with open(master_file, 'r') as f:
        data = json.load(f)
    
    return data.get('channels', [])

def get_channel_credentials(channel_num):
    """Load credentials for a specific channel"""
    token_file = CHANNELS_DIR / f"channel_{channel_num}_token.pickle"
    
    if not token_file.exists():
        print(f"[ERROR] No token found for channel {channel_num}")
        return None
    
    with open(token_file, 'rb') as f:
        creds = pickle.load(f)
    
    # Refresh if needed
    if creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            # Save refreshed token
            with open(token_file, 'wb') as f:
                pickle.dump(creds, f)
        except Exception as e:
            print(f"[WARNING] Token refresh failed for channel {channel_num}: {e}")
    
    return creds

def list_channels():
    """Display all configured channels"""
    channels = load_channels()
    
    if not channels:
        print("No channels configured")
        return
    
    print(f"\n{'='*70}")
    print(f"SCARIFY CHANNELS ({len(channels)} total)")
    print(f"{'='*70}\n")
    
    for ch in channels:
        print(f"[{ch['channel_number']}] {ch['name']}")
        print(f"    ID: {ch['id']}")
        print(f"    Videos: {ch['statistics'].get('videos', 0)}")
        print(f"    Subscribers: {ch['statistics'].get('subscribers', 0)}")
        print(f"    Token: {ch['oauth_token_file']}")
        print()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "list":
            list_channels()
        elif sys.argv[1] == "setup":
            count = int(sys.argv[2]) if len(sys.argv) > 2 else 15
            start = int(sys.argv[3]) if len(sys.argv) > 3 else 1
            setup_channels(count, start)
        else:
            print("Usage:")
            print("  python MULTI_CHANNEL_SETUP.py setup [count] [start_from]")
            print("  python MULTI_CHANNEL_SETUP.py list")
    else:
        print("""
SCARIFY MULTI-CHANNEL SETUP

Usage:
  python MULTI_CHANNEL_SETUP.py setup 15     # Setup 15 channels
  python MULTI_CHANNEL_SETUP.py setup 5 1    # Setup 5 channels, starting from #1
  python MULTI_CHANNEL_SETUP.py list         # List configured channels

Note: You'll need 15 different YouTube/Google accounts
""")


