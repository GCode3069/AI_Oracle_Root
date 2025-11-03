#!/usr/bin/env python3
"""
GENERATE_GROK_ROUND2.py - Grok's updated Round 1 with TAG OPTIMIZATION

Grok submitted NEW scripts (different from first batch)
Enhancing with 20-25 OPTIMIZED tags (not just 5!)
"""

import sys
from pathlib import Path
from datetime import datetime
import time

sys.path.insert(0, str(Path.cwd()))

from abraham_MAX_HEADROOM import generate_voice, generate_lincoln_face_pollo, BASE_DIR
from CLEAN_UP_MESSY_VISUALS import create_clean_max_headroom
from YOUTUBE_TAG_OPTIMIZATION import generate_optimized_tags

# Grok's UPDATED Round 1 submissions
GROK_ROUND2_EPISODES = [
    {
        'episode': 60000,
        'title': "Lincoln's WARNING #60000: Twitter Algorithm SECRET Exposed #Shorts",
        'script': "Stop scrolling. Elon's Twitter algorithm isn't about free speech - it's about data harvesting. They're training AI on your rage. Now you know why they want you angry. Bitcoin below.",
        'base_tags': ['twitter', 'elon', 'algorithm', 'exposed', 'viral']
    },
    {
        'episode': 60001,
        'title': "Lincoln's WARNING #60001: AI Safety Summit DECEPTION #Shorts",
        'script': "The AI safety summit? Theater. They're not scared of AI - they're scared of YOU having AI. Classic power consolidation. Now you see the game. Bitcoin below.",
        'base_tags': ['AI', 'safety', 'summit', 'exposed', 'viral']
    },
    {
        'episode': 60002,
        'title': "Lincoln's WARNING #60002: Presidential Debates ILLUSION #Shorts",
        'script': "Presidential debates? Scripted reality TV. Both sides work for the same bankers. The real election happens in Bitcoin markets. Now you know where power really is. Bitcoin below.",
        'base_tags': ['debate', 'president', 'election', 'exposed', 'viral']
    },
    {
        'episode': 60003,
        'title': "Lincoln's WARNING #60003: Federal Reserve LIE Exposed #Shorts",
        'script': "The Fed 'pausing rates'? They're not controlling inflation - they're controlling YOU. Your savings are being systematically erased. Now you know the truth. Bitcoin below.",
        'base_tags': ['fed', 'inflation', 'rates', 'exposed', 'viral']
    },
    {
        'episode': 60004,
        'title': "Lincoln's WARNING #60004: Climate Summit HYPOCRISY #Shorts",
        'script': "Climate summit private jets? They don't care about the planet - they care about control. Carbon credits are the new indulgences. Now you see the scam. Bitcoin below.",
        'base_tags': ['climate', 'summit', 'hypocrisy', 'exposed', 'viral']
    }
]

def generate_grok_video_with_tags(episode_data: dict):
    """Generate Grok video with 20-25 OPTIMIZED tags"""
    
    episode = episode_data['episode']
    title = episode_data['title']
    script = episode_data['script']
    base_tags = episode_data['base_tags']
    
    print(f"\n[Grok #{episode}] Generating...")
    print(f"  Title: {title}")
    print(f"  Script: {len(script.split())} words")
    
    # Generate OPTIMIZED tags (20-25)
    optimized_tags = generate_optimized_tags(title, script, 'short')
    
    # Merge Grok's base tags with optimization
    all_tags = list(set(base_tags + optimized_tags))[:25]
    
    print(f"  Tags: {len(all_tags)} OPTIMIZED (was 5)")
    
    # Generate voice
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    audio_path = BASE_DIR / 'audio' / f'GROK2_{episode}_{timestamp}.mp3'
    audio_path.parent.mkdir(parents=True, exist_ok=True)
    
    if not generate_voice(script, audio_path):
        return None
    
    # Get Lincoln
    lincoln = generate_lincoln_face_pollo()
    
    # Get QR
    qr = BASE_DIR / 'qr_codes' / 'cashapp_qr.png'
    
    # Create video
    output = BASE_DIR / 'uploaded' / f'GROK2_{episode}_{timestamp}.mp4'
    output.parent.mkdir(parents=True, exist_ok=True)
    
    video = create_clean_max_headroom(lincoln, audio_path, output, qr)
    
    if not video or not Path(video).exists():
        return None
    
    size_mb = Path(video).stat().st_size / (1024*1024)
    print(f"  [OK] Video: {size_mb:.1f} MB")
    
    # Upload with OPTIMIZED TAGS
    print(f"  [Upload] With {len(all_tags)} tags...")
    
    try:
        import pickle
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        
        token_file = BASE_DIR / "youtube_token.pickle"
        
        if token_file.exists():
            with open(token_file, 'rb') as f:
                creds = pickle.load(f)
            
            youtube = build('youtube', 'v3', credentials=creds)
            
            hashtags = ' '.join(f'#{tag.replace(" ", "")}' for tag in all_tags[:15])
            description = f"""{script}

ABRAHAM LINCOLN'S MAX HEADROOM BROADCAST

Cash App: https://cash.app/$healthiwealthi/bitcoin

{hashtags}"""
            
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': all_tags,  # 20-25 OPTIMIZED TAGS!
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
            
            print(f'\n  [UPLOADED] {url}')
            print(f'  [TAGS] {len(all_tags)} tags applied!')
            
            return {
                'episode': episode,
                'url': url,
                'tags': all_tags,
                'tag_count': len(all_tags)
            }
    except Exception as e:
        print(f"  [ERROR] {e}")
    
    return None

def generate_all_grok_round2():
    """Generate all 5 Grok Round 2 videos"""
    
    print("="*70)
    print("  GROK ROUND 2 - WITH TAG OPTIMIZATION")
    print("="*70 + "\n")
    
    print("These are DIFFERENT scripts than Grok's first batch!")
    print("Focus: Current events (Twitter, AI Summit, Debates, Fed, Climate)\n")
    print("Grok original: 5 tags per video")
    print("Our optimization: 20-25 tags per video")
    print("Result: 5x more discoverable!\n")
    
    results = []
    
    for i, ep_data in enumerate(GROK_ROUND2_EPISODES):
        print(f"\n[{i+1}/5] Processing...")
        
        result = generate_grok_video_with_tags(ep_data)
        if result:
            results.append(result)
        
        if i < len(GROK_ROUND2_EPISODES) - 1:
            print(f"\n  Waiting 30 seconds...")
            time.sleep(30)
    
    print("\n" + "="*70)
    print("  GROK ROUND 2 COMPLETE")
    print("="*70 + "\n")
    
    print(f"Videos generated: {len(results)}/5\n")
    
    if results:
        print("All Grok Round 2 videos:")
        for r in results:
            print(f"  #{r['episode']}: {r['url']} ({r['tag_count']} tags)")
    
    print(f"\nGrok now has 10 TOTAL videos (5 + 5)!")
    
    return results

if __name__ == "__main__":
    generate_all_grok_round2()


