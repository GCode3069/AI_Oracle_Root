#!/usr/bin/env python3
"""Process batch of Pollo videos from pollo_videos/batch_1/"""
import sys, subprocess
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from abraham_MAX_HEADROOM import generate_voice, BASE_DIR
from YOUTUBE_TAG_OPTIMIZATION import generate_optimized_tags
from MULTI_STYLE_SCRIPT_GENERATOR import ScriptStyleGenerator

batch_dir = Path('pollo_videos/batch_1')
if not batch_dir.exists():
    print(f"Create folder: {batch_dir}")
    batch_dir.mkdir(parents=True)
    print("Download 30 Pollo videos there, then run this script again!")
    sys.exit(0)

pollo_videos = sorted(batch_dir.glob('*.mp4'))
print(f"\nFound {len(pollo_videos)} Pollo videos\n")

style_gen = ScriptStyleGenerator()
styles = ['chatgpt'] * 15 + ['cursor'] * 10 + ['grok'] * 3 + ['opus'] * 2

for i, pf in enumerate(pollo_videos[:30]):
    ep = 300000 + i
    style = styles[i] if i < len(styles) else 'cursor'
    
    print(f"[{i+1}/{len(pollo_videos)}] Episode #{ep} ({style})...")
    
    # Generate script
    headline = f"Breaking News Update {i+1}"
    if style == 'chatgpt':
        script = style_gen.chatgpt_style(headline)
    elif style == 'grok':
        script = style_gen.grok_style(headline)
    elif style == 'opus':
        script = style_gen.opus_style(headline)
    else:
        script = style_gen.cursor_style(headline)
    
    title = f"Lincoln's WARNING #{ep}: {headline} #Shorts"
    
    # Audio
    audio = BASE_DIR / 'audio' / f'POLLO30_{ep}.mp3'
    audio.parent.mkdir(parents=True, exist_ok=True)
    generate_voice(script, audio)
    
    # Process
    qr = BASE_DIR / 'qr_codes' / 'cashapp_qr.png'
    output = BASE_DIR / 'uploaded' / f'POLLO30_{ep}.mp4'
    
    cmd = ['ffmpeg', '-i', str(pf), '-i', str(audio), '-i', str(qr),
           '-filter_complex', '[0:v]scale=1080:1920[v];[2:v]scale=400:400[qr];[v][qr]overlay=w-420:20',
           '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'fast',
           '-c:a', 'aac', '-movflags', '+faststart', '-y', str(output)]
    
    subprocess.run(cmd, capture_output=True, timeout=120)
    
    if output.exists():
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
                _, response = request.next_chunk()
            
            print(f"  [OK] https://youtube.com/watch?v={response['id']}\n")
        except Exception as e:
            print(f"  [Upload Error] {e}\n")

print(f"\n[DONE] Processed {len(pollo_videos)} Pollo videos!")


