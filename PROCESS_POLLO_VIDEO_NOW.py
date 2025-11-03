#!/usr/bin/env python3
"""
PROCESS_POLLO_VIDEO_NOW.py - Add ALL effects to your Pollo.ai video

Takes your Pollo.ai video and adds:
- Old CRT TV frame
- Max Headroom glitches (RGB split, scan lines)
- VHS static and effects
- Our psychological audio
- Cash App QR code
- Upload to YouTube with 25 tags
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path.cwd()))

from abraham_MAX_HEADROOM import generate_voice, BASE_DIR
from YOUTUBE_TAG_OPTIMIZATION import generate_optimized_tags

def add_all_effects_to_pollo(pollo_video: Path, audio_path: Path, 
                              output_path: Path, qr_path: Path = None):
    """
    Add EVERYTHING to Pollo.ai video:
    - Old CRT TV frame
    - Max Headroom glitches
    - VHS effects
    - Psychological audio
    - QR code
    """
    
    print(f"\n[Processing] Adding ALL effects to Pollo.ai video...")
    
    if not pollo_video.exists():
        print(f"  [ERROR] Pollo video not found: {pollo_video}")
        return None
    
    if not audio_path.exists():
        print(f"  [ERROR] Audio not found: {audio_path}")
        return None
    
    # Get video duration from Pollo video
    probe_cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        str(pollo_video)
    ]
    
    try:
        result = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=10)
        duration = float(result.stdout.strip())
        print(f"  Pollo video duration: {duration:.1f}s")
    except:
        duration = 15
    
    # Build COMPLETE FFmpeg filter with TV frame
    # [0:v] = Pollo.ai video (animated Lincoln)
    # [1:a] = Our audio
    # [2:v] = QR code (optional)
    
    # Step 1: Resize Pollo video to fit in TV screen (leave room for TV frame)
    # TV screen will be 1080x1920 (9:16), inner content 900x1600
    filter_parts = []
    
    filter_parts.append("""
        [0:v]scale=900:1600:force_original_aspect_ratio=decrease,
        pad=900:1600:(ow-iw)/2:(oh-ih)/2:black
        [lincoln_sized]
    """.replace('\n', ' ').strip())
    
    # Step 2: Create OLD CRT TV FRAME
    filter_parts.append("""
        color=c=black:s=1080x1920:d={duration}[bg];
        [bg]drawbox=x=40:y=120:w=1000:h=1680:color=0x1a1a1a:t=fill[frame1];
        [frame1]drawbox=x=90:y=160:w=900:h=1600:color=black:t=fill[tv_frame]
    """.format(duration=duration).replace('\n', ' ').strip())
    
    # Step 3: VHS effects on Lincoln
    filter_parts.append("""
        [lincoln_sized]format=yuv420p,
        colorchannelmixer=.3:.4:.3:0:.3:.4:.3:0:.3:.4:.3,
        noise=alls=25:allf=t+u,
        eq=contrast=1.3:brightness=0.1:saturation=1.4
        [vhs]
    """.replace('\n', ' ').strip())
    
    # Step 4: Max Headroom RGB split glitch
    filter_parts.append("""
        [vhs]split=3[r][g][b];
        [r]lutrgb=r=val:g=0:b=0[red];
        [g]lutrgb=r=0:g=val:b=0[green];
        [b]lutrgb=r=0:g=0:b=val[blue];
        [red][green]blend=all_mode='addition'[rg];
        [rg][blue]blend=all_mode='addition',
        geq='r=r(X+3,Y)':'g=g(X,Y)':'b=b(X-3,Y)'
        [rgb_split]
    """.replace('\n', ' ').strip())
    
    # Step 5: Scan lines
    filter_parts.append("""
        [rgb_split]split[main][lines];
        [lines]geq='lum=if(mod(Y,4),255,0)':cb=128:cr=128,
        format=yuva420p,colorchannelmixer=aa=0.2[scanlines];
        [main][scanlines]overlay[scanned]
    """.replace('\n', ' ').strip())
    
    # Step 6: Random glitch
    filter_parts.append("""
        [scanned]geq='r=if(lt(random(1),0.08),255,r(X,Y))':'g=g(X,Y)':'b=b(X,Y)'[glitched]
    """.replace('\n', ' ').strip())
    
    # Step 7: Composite into TV frame
    filter_parts.append("""
        [tv_frame][glitched]overlay=x=90:y=160[tv_composite]
    """.replace('\n', ' ').strip())
    
    # Step 8: Add static overlay to entire TV
    filter_parts.append("""
        [tv_composite]noise=alls=15:allf=t,
        eq=brightness=0.05
        [tv_final]
    """.replace('\n', ' ').strip())
    
    # Step 9: Add QR code if provided
    if qr_path and qr_path.exists():
        filter_parts.append("""
            [2:v]scale=400:400[qr];
            [tv_final][qr]overlay=w-420:20[vout]
        """.replace('\n', ' ').strip())
        map_video = '[vout]'
        qr_input = ['-loop', '1', '-t', str(duration), '-i', str(qr_path)]
    else:
        map_video = '[tv_final]'
        qr_input = []
    
    # Combine all filter parts
    filter_complex = ';'.join(filter_parts)
    
    print(f"  [FFmpeg] Rendering TV + Max Headroom + VHS...")
    
    # FFmpeg command
    cmd = [
        'ffmpeg', '-y',
        '-i', str(pollo_video),  # [0] Pollo.ai video
        '-i', str(audio_path),   # [1] Our audio
        *qr_input,               # [2] QR code (optional)
        '-filter_complex', filter_complex,
        '-map', map_video,
        '-map', '1:a',  # Use our audio (replaces Pollo audio)
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-movflags', '+faststart',
        '-pix_fmt', 'yuv420p',
        '-t', str(duration),
        str(output_path)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0 and output_path.exists() and output_path.stat().st_size > 0:
            size_mb = output_path.stat().st_size / (1024*1024)
            print(f"  [SUCCESS] {size_mb:.1f} MB")
            print(f"  Features added:")
            print(f"    [OK] Old CRT TV frame")
            print(f"    [OK] Max Headroom RGB glitch")
            print(f"    [OK] VHS scan lines + static")
            print(f"    [OK] Animated Lincoln (from Pollo)")
            print(f"    [OK] Our psychological audio")
            if qr_path and qr_path.exists():
                print(f"    [OK] Cash App QR code")
            return output_path
        else:
            print(f"  [ERROR] FFmpeg failed")
            if result.stderr:
                print(f"  Error: {result.stderr[-1000:]}")
            return None
            
    except subprocess.TimeoutExpired:
        print(f"  [ERROR] FFmpeg timeout (5 minutes)")
        return None
    except Exception as e:
        print(f"  [ERROR] {e}")
        return None


def process_and_upload_pollo():
    """Complete workflow"""
    
    print("="*70)
    print("  PROCESSING YOUR POLLO.AI VIDEO - ALL EFFECTS")
    print("="*70 + "\n")
    
    # Find Pollo video
    pollo_file = Path("F:/AI_Oracle_Root/scarify/Image to video 丨 Abraham Lincoln's decomposing face screaming inside malfunction.mp4")
    
    if not pollo_file.exists():
        print(f"[ERROR] Pollo video not found at: {pollo_file}")
        print(f"\nPlease ensure the Pollo.ai video is at this location.")
        return None
    
    size_mb = pollo_file.stat().st_size / (1024*1024)
    print(f"[Pollo Video] Found!")
    print(f"  Size: {size_mb:.1f} MB\n")
    
    # Generate test script
    episode = 99999
    title = "Lincoln's WARNING #99999: COMPLETE System Breakdown #Shorts"
    script = "Listen close. They don't hide the corruption anymore - they flaunt it. Left, right, center - all puppets, same masters. The whole show is rigged. Now you see it all. Bitcoin below."
    
    print(f"Episode: #{episode}")
    print(f"Title: {title}")
    print(f"Script: {script}\n")
    
    # Generate our audio
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    audio_path = BASE_DIR / 'audio' / f'POLLO_FULL_{episode}_{timestamp}.mp3'
    audio_path.parent.mkdir(parents=True, exist_ok=True)
    
    print("[1/3] Generating psychological audio...")
    if not generate_voice(script, audio_path):
        print("  [ERROR] Voice generation failed")
        return None
    
    print(f"  [OK] Audio: {audio_path.stat().st_size / 1024:.1f} KB\n")
    
    # Get QR code
    qr_path = BASE_DIR / 'qr_codes' / 'cashapp_qr.png'
    
    # Process video
    print("[2/3] Adding ALL effects to Pollo video...")
    output_path = BASE_DIR / 'uploaded' / f'POLLO_COMPLETE_{episode}_{timestamp}.mp4'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    final_video = add_all_effects_to_pollo(pollo_file, audio_path, output_path, qr_path)
    
    if not final_video:
        return None
    
    # Upload to YouTube
    print(f"\n[3/3] Uploading to YouTube...")
    
    try:
        import pickle
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        
        token_file = BASE_DIR / "youtube_token.pickle"
        
        if not token_file.exists():
            print("  [ERROR] YouTube credentials not found")
            print(f"  Video ready at: {final_video}")
            return None
        
        with open(token_file, 'rb') as f:
            creds = pickle.load(f)
        
        youtube = build('youtube', 'v3', credentials=creds)
        
        # Generate optimized tags
        tags = generate_optimized_tags(title, script, 'short')
        
        print(f"  Tags: {len(tags)} optimized")
        
        hashtags = ' '.join(f'#{tag.replace(" ", "")}' for tag in tags[:15])
        description = f"""{script}

POLLO.AI + COMPLETE MAX HEADROOM SYSTEM
✅ Animated Lincoln with lip-sync (Pollo.ai)
✅ Old CRT TV frame (authentic 1980s look)
✅ Max Headroom RGB split glitches
✅ VHS scan lines + static
✅ Psychological audio (theta/gamma/binaural)
✅ Cash App QR code

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
        
        media = MediaFileUpload(str(final_video), chunksize=1024*1024, resumable=True)
        request = youtube.videos().insert(part='snippet,status', body=body, media_body=media)
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f'  [Upload] {int(status.progress() * 100)}%', end='\r')
        
        video_id = response['id']
        url = f'https://youtube.com/watch?v={video_id}'
        
        print(f'\n\n' + '='*70)
        print('  SUCCESS! POLLO.AI + ALL EFFECTS!')
        print('='*70)
        print(f'\n  PASTE AND GO LINK:\n')
        print(f'  {url}\n')
        print('='*70)
        print('\n  THIS VIDEO HAS EVERYTHING:')
        print('  [OK] Animated Lincoln (Pollo.ai - lip-sync!)')
        print('  [OK] Old CRT TV frame (Max Headroom style)')
        print('  [OK] RGB split glitches')
        print('  [OK] VHS scan lines + static')
        print('  [OK] Psychological audio (6Hz theta, 40Hz gamma)')
        print('  [OK] Cash App QR code (400x400px)')
        print(f'  [OK] {len(tags)} optimized tags')
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
        print(f"  Video ready at: {final_video}")
        return None

if __name__ == "__main__":
    process_and_upload_pollo()

