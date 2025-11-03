#!/usr/bin/env python3
"""
USE_DARK_JOSH_SCRIPTS.py
Use Dark Josh's EXCELLENT scripts with MAX_HEADROOM generator (best of both!)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

from abraham_MAX_HEADROOM import generate_voice, generate_lincoln_face_pollo, BASE_DIR
from CLEAN_UP_MESSY_VISUALS import create_clean_max_headroom
from YOUTUBE_TAG_OPTIMIZATION import generate_optimized_tags

# DARK JOSH SCRIPTS (the good ones!)
DARK_JOSH_SCRIPTS = [
    {
        'headline': 'Clocks fall back Sunday',
        'script': "Clocks fall back Sunday with an 'extra hour' - but Congress remains split on time change. Listen... while you ARGUE about daylight, they're printing money in the dark. Literal dark. That 'extra hour'? They use it to rob you blind. Democrats want permanent daylight - sounds nice. Republicans want standard time - sounds traditional. BOTH want you distracted while the Federal Reserve runs 24/7 creating inflation. That clock on your wall? It's a cage. Bitcoin doesn't care what time it is. Scan the QR."
    },
    {
        'headline': 'LA Dodgers World Series',
        'script': "LA Dodgers retain World Series after thrilling Game 7 win over Toronto Blue Jays. Cool story. Know what else happened during that game? 47 new bills passed while you watched bases. They LOVE when you're distracted. Sports, celebrity drama, literally ANYTHING to keep your eyes off the robbery. That 'thrilling' game? Cost you $3,847 in inflation per household. But hey, Dodgers won. Bread and circuses for the modern peasant. Bitcoin doesn't play games. Scan the QR."
    },
    {
        'headline': 'Tech Layoffs Continue',
        'script': "Tech layoffs continue as companies 'restructure' for AI efficiency. Translation: humans fired, profits kept. They sell you 'innovation' while your neighbor loses everything. Classic move - destroy the middle class, call it progress. CEOs get bonuses for cutting you. Stocks rise when you're fired. System working exactly as designed. But they'll tweet about 'difficult decisions' from their third yacht. This ain't reform - it's organized elimination. Bitcoin doesn't fire you. Scan the QR."
    },
    {
        'headline': 'Climate Summit Ends',
        'script': "Climate summit ends in deadlock after two weeks of 'intense negotiations'. Let me translate elite-speak: They flew private jets to discuss YOUR carbon footprint. Ate $500 steaks to debate YOUR consumption. Stayed in luxury hotels to lecture YOU about sustainability. Then accomplished NOTHING except photo ops and empty promises. Meanwhile, you're taxed for breathing. They sell guilt, you buy compliance. Real climate solution? Decentralize power. Bitcoin runs on renewable energy increasingly. Scan the QR."
    },
    {
        'headline': 'Government Shutdown Month 2',
        'script': "Government shutdown enters month two as partisan gridlock continues. Meanwhile, THEIR paychecks never stop. Funny how that works. You can't pay rent during shutdown - they're still collecting six figures. Both parties blame each other on TV, then have drinks together after. It's theater. Controlled opposition. They want you thinking there's a fight when they're on the same team - Team Rich. Only thing shutting down is your opportunity. Bitcoin stays open 24/7. Scan the QR."
    }
]

def generate_with_dark_josh_script(script_data, episode):
    """Use Dark Josh script with MAX_HEADROOM generator"""
    
    headline = script_data['headline']
    script = script_data['script']
    title = f"Lincoln's WARNING #{episode}: {headline} | Dark Josh Style #Shorts"
    
    print(f"\n[Episode #{episode}] {headline}")
    print(f"Script: {script[:100]}...")
    
    # Generate voice with binaural beats
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    audio_path = BASE_DIR / 'audio' / f'DARKJOSH_{episode}_{timestamp}.mp3'
    audio_path.parent.mkdir(parents=True, exist_ok=True)
    
    if not generate_voice(script, audio_path):
        print("  [FAILED] Voice generation")
        return None
    
    # Get Lincoln
    lincoln = generate_lincoln_face_pollo()
    
    # Get QR
    qr = BASE_DIR / 'qr_codes' / 'cashapp_qr.png'
    
    # Create video with ALL features
    output = BASE_DIR / 'uploaded' / f'DARKJOSH_{episode}_{timestamp}.mp4'
    output.parent.mkdir(parents=True, exist_ok=True)
    
    video = create_clean_max_headroom(lincoln, audio_path, output, qr)
    
    if not video or not Path(video).exists():
        print("  [FAILED] Video creation")
        return None
    
    size_mb = Path(video).stat().st_size / (1024*1024)
    print(f"  [VIDEO] {size_mb:.1f} MB")
    
    # Upload to YouTube
    try:
        import pickle
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        
        token_file = BASE_DIR / "youtube_token.pickle"
        
        with open(token_file, 'rb') as f:
            creds = pickle.load(f)
        
        youtube = build('youtube', 'v3', credentials=creds)
        
        # Generate optimized tags
        tags = generate_optimized_tags(title, script, 'short')
        
        description = f"""{script}

ABRAHAM LINCOLN'S DARK JOSH STYLE OBSERVATIONS
Best script quality + All visual effects!

Cash App: https://cash.app/$healthiwealthi/bitcoin"""
        
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
        
        print(f'\n  [UPLOADED] {url}')
        
        return url
        
    except Exception as e:
        print(f"  [Upload Error] {e}")
        return None

def generate_all_dark_josh():
    """Generate all 5 Dark Josh scripts with working generator"""
    
    print("="*70)
    print("  DARK JOSH SCRIPTS + MAX_HEADROOM GENERATOR")
    print("="*70)
    print("\nBest of both worlds:")
    print("  ✅ Dark Josh's excellent scripts")
    print("  ✅ MAX_HEADROOM's all features (QR, effects, binaural)\n")
    
    results = []
    
    for i, script_data in enumerate(DARK_JOSH_SCRIPTS):
        episode = 400000 + i
        url = generate_with_dark_josh_script(script_data, episode)
        if url:
            results.append({'episode': episode, 'url': url})
    
    print("\n" + "="*70)
    print("  DARK JOSH VIDEOS COMPLETE")
    print("="*70 + "\n")
    
    print(f"Generated: {len(results)}/5\n")
    
    for r in results:
        print(f"  #{r['episode']}: {r['url']}")
    
    print("\nThese have EVERYTHING:")
    print("  ✅ Dark Josh's excellent scripts")
    print("  ✅ Visual Abe Lincoln")
    print("  ✅ QR code overlay")
    print("  ✅ Binaural beats")
    print("  ✅ 24 optimized tags")
    print("  ✅ Max Headroom effects")
    print("  ✅ NO Bitcoin address recitation")
    
    return results

if __name__ == "__main__":
    generate_all_dark_josh()


