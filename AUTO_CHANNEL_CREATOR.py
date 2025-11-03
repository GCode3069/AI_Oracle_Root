#!/usr/bin/env python3
"""
SCARIFY - Automatic YouTube Channel Creator
Creates 15 uniformly branded YouTube channels with consistent identity
"""

import os, sys, json, pickle, time
from pathlib import Path
from datetime import datetime

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from google.auth.transport.requests import Request
    YOUTUBE_AVAILABLE = True
except ImportError:
    print("[ERROR] Install: pip install google-api-python-client google-auth-oauthlib")
    YOUTUBE_AVAILABLE = False

BASE_DIR = Path("F:/AI_Oracle_Root/scarify")
CHANNELS_DIR = BASE_DIR / "channels"
CHANNELS_DIR.mkdir(exist_ok=True)

SCOPES = [
    'https://www.googleapis.com/auth/youtube',
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.force-ssl'
]

CLIENT_SECRETS = BASE_DIR / "config/credentials/youtube/client_secrets.json"

# ═══════════════════════════════════════════════════════════════════════
# UNIFIED BRAND TEMPLATES
# ═══════════════════════════════════════════════════════════════════════

BRAND_CONFIG = {
    "abraham": {
        "channels": [1, 2, 3, 4, 5],
        "names": [
            "Abraham's Warning",
            "Lincoln Speaks Truth",
            "Ford's Theatre Messages",
            "Honest Abe Uncensored",
            "The President's Ghost"
        ],
        "descriptions": [
            "Lincoln's ghost reveals truth about modern America. From Ford's Theatre, warnings echo through time. Support truth: bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt",
            "Abraham Lincoln speaks from beyond the grave. Horror shorts exposing corruption. Bitcoin: bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt",
            "The 16th President returns with prophecies. Dark truths revealed. Rebel Kit: trenchaikits.com/buy-rebel-$97",
            "Lincoln's assassination was a warning. Your future is a choice. BTC: bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt",
            "From Ford's Theatre, Lincoln watches America fall. Support the truth: bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"
        ],
        "keywords": "abraham lincoln horror truth government corruption political shorts",
        "banner_color": "#8B0000",  # Dark red
        "profile_theme": "Lincoln silhouette on dark red"
    },
    
    "oracle": {
        "channels": [6, 7, 8, 9],
        "names": [
            "Oracle Signals",
            "AI Truth Network",
            "Future Vision Daily",
            "The Digital Prophet"
        ],
        "descriptions": [
            "AI that sees tomorrow. Tech predictions that come true. Matrix green truth. BTC: bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt",
            "Artificial intelligence reveals hidden patterns. Cyber warnings. Support: bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt",
            "Future predictions from advanced AI. Market signals. Tech warnings. Bitcoin: bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt",
            "Digital prophecy in the age of AI. See what's coming. BTC: bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"
        ],
        "keywords": "ai artificial intelligence tech predictions future signals matrix",
        "banner_color": "#00FF41",  # Matrix green
        "profile_theme": "Digital eye with code rain"
    },
    
    "comedy": {
        "channels": [10, 11, 12],
        "names": [
            "Dark Josh Chronicles",
            "The Void Speaks Comedy",
            "Lincoln Roasts"
        ],
        "descriptions": [
            "Dark comedy from the void. Headline roasts. Truth wrapped in laughs. Bitcoin: bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt",
            "Comedy so dark you need night vision. Social commentary. BTC: bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt",
            "Lincoln roasts modern headlines. Dark humor. Truth comedy. Support: bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"
        ],
        "keywords": "dark comedy roasts social commentary humor shorts viral",
        "banner_color": "#FF6B35",  # Orange
        "profile_theme": "Bold orange text on dark background"
    },
    
    "scarify": {
        "channels": [13, 14, 15],
        "names": [
            "SCARIFY",
            "Psychological Warfare",
            "Cognitohazard Central"
        ],
        "descriptions": [
            "Psychological warfare in 60 seconds. Horror that sticks. BTC: bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt",
            "Mind games and fear. Cognitohazards unleashed. Support: bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt",
            "Psychological horror shorts. Fear targeting. Bitcoin: bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"
        ],
        "keywords": "horror psychological scarify fear cognitohazard shorts dark",
        "banner_color": "#FF0000",  # Red
        "profile_theme": "SCARIFY text with blood drip"
    }
}

# ═══════════════════════════════════════════════════════════════════════
# CHANNEL CREATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

def authenticate_new_channel(channel_num):
    """Authenticate a new YouTube channel"""
    
    if not CLIENT_SECRETS.exists():
        print(f"[ERROR] Client secrets not found: {CLIENT_SECRETS}")
        print("Download from: https://console.cloud.google.com/apis/credentials")
        return None
    
    token_file = CHANNELS_DIR / f"channel_{channel_num}_token.pickle"
    
    print(f"\n{'='*70}")
    print(f"AUTHENTICATING CHANNEL #{channel_num}")
    print(f"{'='*70}\n")
    
    flow = InstalledAppFlow.from_client_secrets_file(
        str(CLIENT_SECRETS),
        SCOPES
    )
    
    print(f"Opening browser for authentication...")
    print(f"Please log in with the Google account for Channel #{channel_num}")
    print(f"\nIMPORTANT: Use a DIFFERENT Google account for each channel!")
    print()
    
    try:
        creds = flow.run_local_server(
            port=8080 + channel_num,
            prompt='consent',
            authorization_prompt_message=f'SCARIFY Channel #{channel_num} - Please authorize'
        )
        
        # Save credentials
        with open(token_file, 'wb') as f:
            pickle.dump(creds, f)
        
        print(f"\n[OK] Authentication successful!")
        print(f"[OK] Token saved: {token_file.name}\n")
        
        return creds
        
    except Exception as e:
        print(f"\n[ERROR] Authentication failed: {e}\n")
        return None

def get_channel_details(creds):
    """Get authenticated channel details"""
    try:
        youtube = build('youtube', 'v3', credentials=creds)
        
        request = youtube.channels().list(
            part='snippet,brandingSettings,statistics',
            mine=True
        )
        response = request.execute()
        
        if response['items']:
            channel = response['items'][0]
            return {
                'id': channel['id'],
                'title': channel['snippet']['title'],
                'description': channel['snippet'].get('description', ''),
                'custom_url': channel['snippet'].get('customUrl', ''),
                'subscribers': channel['statistics'].get('subscriberCount', '0'),
                'views': channel['statistics'].get('viewCount', '0'),
                'videos': channel['statistics'].get('videoCount', '0')
            }
    except Exception as e:
        print(f"[ERROR] Failed to get channel details: {e}")
    
    return None

def update_channel_branding(creds, channel_num, brand_theme, theme_name):
    """Update channel with uniform branding"""
    
    youtube = build('youtube', 'v3', credentials=creds)
    
    # Get current channel
    channel_response = youtube.channels().list(
        part='snippet,brandingSettings',
        mine=True
    ).execute()
    
    if not channel_response['items']:
        print("[ERROR] No channel found")
        return False
    
    channel = channel_response['items'][0]
    channel_id = channel['id']
    
    # Determine which name/description to use
    brand_index = brand_theme['channels'].index(channel_num)
    new_title = brand_theme['names'][brand_index]
    new_description = brand_theme['descriptions'][brand_index]
    keywords = brand_theme['keywords']
    
    print(f"\n[UPDATE] Applying branding...")
    print(f"  Theme: {theme_name}")
    print(f"  Title: {new_title}")
    print(f"  Keywords: {keywords}")
    
    try:
        # Update channel metadata
        youtube.channels().update(
            part='brandingSettings',
            body={
                'id': channel_id,
                'brandingSettings': {
                    'channel': {
                        'title': new_title,
                        'description': new_description,
                        'keywords': keywords,
                        'defaultLanguage': 'en',
                        'country': 'US'
                    }
                }
            }
        ).execute()
        
        print(f"[OK] Branding applied successfully!\n")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to update branding: {e}\n")
        return False

def create_channel_profile(channel_num, creds, details, theme_name, brand_theme):
    """Create complete channel profile"""
    
    config = {
        "channel_number": channel_num,
        "channel_id": details['id'],
        "theme": theme_name,
        "brand": brand_theme['names'][brand_theme['channels'].index(channel_num)],
        "created_at": datetime.now().isoformat(),
        "oauth_token_file": f"channel_{channel_num}_token.pickle",
        "statistics": {
            "subscribers": details['subscribers'],
            "views": details['views'],
            "videos": details['videos']
        },
        "upload_count": 0,
        "last_upload": None,
        "performance": {
            "total_views": 0,
            "avg_ctr": 0.0,
            "avg_retention": 0.0
        },
        "branding": {
            "color": brand_theme['banner_color'],
            "keywords": brand_theme['keywords'],
            "description_template": brand_theme['descriptions'][brand_theme['channels'].index(channel_num)]
        }
    }
    
    # Save individual config
    config_file = CHANNELS_DIR / f"channel_{channel_num}_config.json"
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    return config

def auto_create_all_channels():
    """Automatically create and brand all 15 channels"""
    
    if not YOUTUBE_AVAILABLE:
        print("[ERROR] YouTube API not available")
        return False
    
    print(f"\n{'='*70}")
    print(f"SCARIFY - AUTOMATIC CHANNEL CREATOR")
    print(f"{'='*70}\n")
    print(f"This will create 15 uniformly branded YouTube channels:\n")
    print(f"  Channels 1-5:   Abraham's Warning (Horror/Political)")
    print(f"  Channels 6-9:   Oracle Signals (Tech/AI)")
    print(f"  Channels 10-12: Dark Comedy (Roasts)")
    print(f"  Channels 13-15: SCARIFY (Psychological Horror)")
    print(f"\n{'='*70}\n")
    print(f"REQUIREMENTS:")
    print(f"  • 15 different Google accounts")
    print(f"  • You'll log in 15 times")
    print(f"  • Each gets uniform branding applied")
    print(f"\n{'='*70}\n")
    
    confirm = input("Continue with channel creation? (yes/no): ")
    if confirm.lower() != 'yes':
        print("\n[CANCELLED] Aborted by user\n")
        return False
    
    all_channels = []
    
    # Process each theme group
    for theme_name, brand_theme in BRAND_CONFIG.items():
        print(f"\n{'='*70}")
        print(f"CREATING {theme_name.upper()} CHANNELS")
        print(f"{'='*70}\n")
        
        for channel_num in brand_theme['channels']:
            print(f"\n[CHANNEL {channel_num}] Starting setup...")
            
            # Authenticate
            creds = authenticate_new_channel(channel_num)
            if not creds:
                print(f"[ERROR] Skipping channel {channel_num}")
                continue
            
            # Get channel details
            details = get_channel_details(creds)
            if not details:
                print(f"[ERROR] Could not retrieve channel details")
                continue
            
            print(f"\n[INFO] Connected to channel:")
            print(f"  Current Name: {details['title']}")
            print(f"  Channel ID: {details['id']}")
            print(f"  Subscribers: {details['subscribers']}")
            print(f"  Videos: {details['videos']}")
            
            # Apply uniform branding
            if update_channel_branding(creds, channel_num, brand_theme, theme_name):
                print(f"[OK] Channel {channel_num} branded as: {brand_theme['names'][brand_theme['channels'].index(channel_num)]}")
            
            # Create profile
            config = create_channel_profile(channel_num, creds, details, theme_name, brand_theme)
            all_channels.append(config)
            
            print(f"\n[SUCCESS] Channel {channel_num} complete!")
            
            # Pause between channels
            if channel_num < 15:
                print(f"\nPreparing for next channel...")
                time.sleep(3)
    
    # Save master config
    master_config = {
        "total_channels": len(all_channels),
        "setup_date": datetime.now().isoformat(),
        "bitcoin_address": "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt",
        "product_link": "https://trenchaikits.com/buy-rebel-$97",
        "channels": all_channels,
        "branding": {
            "abraham": {
                "channels": [1, 2, 3, 4, 5],
                "theme": "Horror/Political",
                "colors": ["#8B0000", "#FFD700"]
            },
            "oracle": {
                "channels": [6, 7, 8, 9],
                "theme": "Tech/AI",
                "colors": ["#00FF41", "#00CED1"]
            },
            "comedy": {
                "channels": [10, 11, 12],
                "theme": "Dark Comedy",
                "colors": ["#FF6B35", "#1A1A2E"]
            },
            "scarify": {
                "channels": [13, 14, 15],
                "theme": "Psychological Horror",
                "colors": ["#000000", "#FF0000"]
            }
        }
    }
    
    master_file = CHANNELS_DIR / "channels_master.json"
    with open(master_file, 'w') as f:
        json.dump(master_config, f, indent=2)
    
    # Print summary
    print(f"\n{'='*70}")
    print(f"CHANNEL CREATION COMPLETE")
    print(f"{'='*70}\n")
    print(f"Successfully configured: {len(all_channels)}/15 channels\n")
    
    print(f"CHANNEL BREAKDOWN:")
    for theme, brand in BRAND_CONFIG.items():
        theme_channels = [c for c in all_channels if c['channel_number'] in brand['channels']]
        print(f"\n{theme.upper()} ({len(theme_channels)} channels):")
        for ch in theme_channels:
            print(f"  [{ch['channel_number']}] {ch['brand']}")
            print(f"      ID: {ch['channel_id']}")
    
    print(f"\n{'='*70}")
    print(f"Master Config: {master_file}")
    print(f"{'='*70}\n")
    
    print(f"NEXT STEPS:")
    print(f"  1. Verify channels at: https://studio.youtube.com")
    print(f"  2. Upload channel art/banners (optional)")
    print(f"  3. Start uploading videos: python MULTI_CHANNEL_UPLOADER.py")
    print(f"\n{'='*70}\n")
    
    return True

def list_created_channels():
    """List all created channels with branding"""
    
    master_file = CHANNELS_DIR / "channels_master.json"
    
    if not master_file.exists():
        print("\n[WARNING] No channels created yet")
        print("Run: python AUTO_CHANNEL_CREATOR.py create\n")
        return
    
    with open(master_file, 'r') as f:
        data = json.load(f)
    
    print(f"\n{'='*70}")
    print(f"SCARIFY EMPIRE - CHANNEL LIST")
    print(f"{'='*70}\n")
    print(f"Total Channels: {data['total_channels']}")
    print(f"Setup Date: {data['setup_date']}")
    print(f"Bitcoin: {data['bitcoin_address']}")
    print(f"\n{'='*70}\n")
    
    for theme, info in data['branding'].items():
        print(f"{theme.upper()} - {info['theme']}")
        print(f"  Channels: {', '.join(map(str, info['channels']))}")
        print(f"  Colors: {', '.join(info['colors'])}")
        print()
    
    print(f"{'='*70}\n")
    
    print(f"DETAILED LIST:\n")
    for ch in data['channels']:
        print(f"[{ch['channel_number']}] {ch['brand']}")
        print(f"    Theme: {ch['theme']}")
        print(f"    ID: {ch['channel_id']}")
        print(f"    Color: {ch['branding']['color']}")
        print(f"    OAuth: {ch['oauth_token_file']}")
        print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""
SCARIFY - Automatic Channel Creator

Usage:
  python AUTO_CHANNEL_CREATOR.py create    # Create & brand 15 channels
  python AUTO_CHANNEL_CREATOR.py list      # List created channels
  
Features:
  • Authenticates 15 YouTube channels
  • Applies uniform branding per theme group
  • Saves OAuth tokens for uploads
  • Creates master channel config
  
Example:
  python AUTO_CHANNEL_CREATOR.py create
""")
    else:
        command = sys.argv[1]
        
        if command == "create":
            auto_create_all_channels()
        elif command == "list":
            list_created_channels()
        else:
            print(f"[ERROR] Unknown command: {command}")
            print("Use: create or list")


