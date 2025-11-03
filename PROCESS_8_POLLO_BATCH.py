#!/usr/bin/env python3
"""Process 8 Pollo videos FAST"""
import sys, glob
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from abraham_MAX_HEADROOM import generate_voice, BASE_DIR
from CLEAN_UP_MESSY_VISUALS import create_clean_max_headroom
from YOUTUBE_TAG_OPTIMIZATION import generate_optimized_tags

# Find all Pollo videos
pollo_files = sorted(Path('.').glob('Image to video*.mp4'))[:8]
print(f"\nFound {len(pollo_files)} Pollo videos\n")

headlines = ["System Collapse", "Government Breakdown", "Market Manipulation", "AI Control Grid", "Digital Prison", "Surveillance State", "Economic Warfare", "Reality Corruption"]

for i, pf in enumerate(pollo_files):
    ep = 200000 + i
    headline = headlines[i]
    script = f"Listen. {headline} isn't theory - it's now. They don't hide it anymore. Left, right - same masters. Now you see it. Bitcoin below."
    title = f"Lincoln's WARNING #{ep}: {headline} #Shorts"
    
    print(f"[{i+1}/8] Processing Pollo video {i+1}...")
    
    # Generate audio
    audio = BASE_DIR / 'audio' / f'POLLO_BATCH_{ep}.mp3'
    audio.parent.mkdir(parents=True, exist_ok=True)
    generate_voice(script, audio)
    
    # Process video
    qr = BASE_DIR / 'qr_codes' / 'cashapp_qr.png'
    output = BASE_DIR / 'uploaded' / f'POLLO_BATCH_{ep}.mp4'
    
    # Use simplified processing for speed
    import subprocess
    cmd = ['ffmpeg', '-i', str(pf), '-i', str(audio), '-i', str(qr), 
           '-filter_complex', '[0:v]scale=1080:1920[v];[2:v]scale=400:400[qr];[v][qr]overlay=w-420:20',
           '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
           '-c:a', 'aac', '-movflags', '+faststart', '-y', str(output)]
    
    subprocess.run(cmd, capture_output=True, timeout=120)
    
    if output.exists():
        print(f"  [OK] {output.stat().st_size / (1024*1024):.1f} MB")
        
        # Upload
        try:
            import pickle
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaFileUpload
            
            token = BASE_DIR / "youtube_token.pickle"
            with open(token, 'rb') as f:
                creds = pickle.load(f)
            
            youtube = build('youtube', 'v3', credentials=creds)
            tags = generate_optimized_tags(title, script, 'short')
            
            body = {'snippet': {'title': title, 'description': f"{script}\n\nCash App: https://cash.app/$healthiwealthi/bitcoin", 'tags': tags, 'categoryId': '24'}, 'status': {'privacyStatus': 'public', 'selfDeclaredMadeForKids': False}}
            
            media = MediaFileUpload(str(output), resumable=True)
            request = youtube.videos().insert(part='snippet,status', body=body, media_body=media)
            response = None
            while response is None:
                status, response = request.next_chunk()
            
            print(f"  [UPLOADED] https://youtube.com/watch?v={response['id']}")
        except Exception as e:
            print(f"  [Upload Error] {e}")

print("\n[DONE] 8 Pollo videos processed and uploaded!")

