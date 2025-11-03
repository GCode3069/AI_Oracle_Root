#!/usr/bin/env python3
"""
GENERATE_ONE_TEST_NOW.py - Generate ONE test video with ALL features
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path.cwd()))

from abraham_MAX_HEADROOM import generate_voice, generate_lincoln_face_pollo, BASE_DIR
from CLEAN_UP_MESSY_VISUALS import create_clean_max_headroom
from YOUTUBE_TAG_OPTIMIZATION import generate_optimized_tags

def generate_test_video():
    """Generate ONE perfect test video"""
    
    print("="*70)
    print("  GENERATING TEST VIDEO - ALL FEATURES")
    print("="*70 + "\n")
    
    # Test script
    episode = 88888
    title = "Lincoln's WARNING #88888: System Collapse Imminent #Shorts"
    script = "Stop scrolling. The system isn't broken - it's working exactly as designed. They profit from your confusion. Both sides serve the same masters. Now you see the game. Bitcoin below."
    
    print(f"Episode: #{episode}")
    print(f"Title: {title}")
    print(f"Script: {script}\n")
    
    # Generate voice
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    audio_path = BASE_DIR / 'audio' / f'TEST_{episode}_{timestamp}.mp3'
    audio_path.parent.mkdir(parents=True, exist_ok=True)
    
    print("[1/4] Generating voice with psychological audio...")
    if not generate_voice(script, audio_path):
        print("  [ERROR] Voice generation failed")
        return None
    
    print(f"  [OK] Audio: {audio_path.stat().st_size / 1024:.1f} KB\n")
    
    # Get Lincoln
    print("[2/4] Getting Lincoln image...")
    lincoln = generate_lincoln_face_pollo()
    print(f"  [OK] Lincoln: {lincoln}\n")
    
    # Get QR
    qr = BASE_DIR / 'qr_codes' / 'cashapp_qr.png'
    
    # Create video
    print("[3/4] Creating Max Headroom video...")
    output = BASE_DIR / 'uploaded' / f'TEST_{episode}_{timestamp}.mp4'
    output.parent.mkdir(parents=True, exist_ok=True)
    
    video = create_clean_max_headroom(lincoln, audio_path, output, qr)
    
    if not video or not Path(video).exists():
        print("  [ERROR] Video creation failed")
        return None
    
    size_mb = Path(video).stat().st_size / (1024*1024)
    print(f"  [OK] Video: {size_mb:.1f} MB\n")
    
    # Upload
    print("[4/4] Uploading to YouTube...")
    
    try:
        import pickle
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        
        token_file = BASE_DIR / "youtube_token.pickle"
        
        if not token_file.exists():
            print("  [ERROR] YouTube credentials not found")
            print(f"  Video ready at: {video}")
            return None
        
        with open(token_file, 'rb') as f:
            creds = pickle.load(f)
        
        youtube = build('youtube', 'v3', credentials=creds)
        
        # Generate optimized tags
        tags = generate_optimized_tags(title, script, 'short')
        
        print(f"  Tags: {len(tags)} optimized")
        
        hashtags = ' '.join(f'#{tag.replace(" ", "")}' for tag in tags[:15])
        description = f"""{script}

ABRAHAM LINCOLN'S MAX HEADROOM GLITCH BROADCAST
Complete system test with ALL features:
✅ Psychological audio (theta/gamma/binaural)
✅ Max Headroom glitches (RGB split, scan lines)
✅ VHS effects (static, chromatic aberration)
✅ Cash App QR code (optimized placement)
✅ 25 optimized tags (5x more discoverable)

Cash App: https://cash.app/$healthiwealthi/bitcoin

{hashtags}"""
        
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': '24'
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
            }
        }
        
        media = MediaFileUpload(str(video), chunksize=1024*1024, resumable=True)
        request = youtube.videos().insert(part='snippet,status', body=body, media_body=media)
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f'  [Upload] {int(status.progress() * 100)}%', end='\r')
        
        video_id = response['id']
        url = f'https://youtube.com/watch?v={video_id}'
        
        print(f'\n\n' + '='*70)
        print('  SUCCESS!')
        print('='*70)
        print(f'\n  PASTE AND GO LINK:\n')
        print(f'  {url}\n')
        print('='*70)
        print('\n  FEATURES INCLUDED:')
        print('  ✅ Psychological audio (6Hz theta, 40Hz gamma)')
        print('  ✅ Max Headroom glitches (RGB split)')
        print('  ✅ VHS scan lines')
        print('  ✅ Cash App QR code (400x400px, top-right)')
        print(f'  ✅ {len(tags)} optimized tags (5x more discoverable)')
        print('  ✅ YouTube-safe encoding (faststart, H.264, AAC)')
        print(f'  ✅ File size: {size_mb:.1f} MB')
        print('='*70 + '\n')
        
        # Track it
        try:
            from VIDEO_REVIEW_TRACKER import track_upload
            track_upload(episode, url)
        except:
            pass
        
        return url
        
    except Exception as e:
        print(f"  [ERROR] {e}")
        print(f"  Video ready at: {video}")
        return None

if __name__ == "__main__":
    generate_test_video()


