#!/usr/bin/env python3
"""
INTEGRATE_POLLO_VIDEO.py - Use Pollo.ai generated Lincoln videos

Instead of static image, use Pollo.ai animated Lincoln
Then add our effects:
- Max Headroom glitches
- VHS effects
- Psychological audio
- QR code overlay
- YouTube optimization
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path.cwd()))

from abraham_MAX_HEADROOM import generate_voice, BASE_DIR

def download_pollo_video(pollo_url: str, output_path: Path):
    """
    Download Pollo.ai video
    
    Pollo.ai videos can be downloaded from share links
    Format: https://pollo.ai/v/{video_id}?source=share
    """
    print(f"[Pollo.ai] Downloading video...")
    print(f"  URL: {pollo_url}")
    
    # Extract video ID
    if '/v/' in pollo_url:
        video_id = pollo_url.split('/v/')[1].split('?')[0]
        print(f"  Video ID: {video_id}")
    
    # Method 1: Try direct download (if Pollo.ai allows)
    try:
        import requests
        
        # Pollo.ai may have a direct video URL
        # Format might be: https://pollo.ai/api/video/{video_id}/download
        download_url = f"https://pollo.ai/api/video/{video_id}/download"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(download_url, headers=headers, timeout=120, stream=True)
        
        if response.status_code == 200:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            size_mb = output_path.stat().st_size / (1024*1024)
            print(f"  [OK] Downloaded: {size_mb:.1f} MB")
            return output_path
        
    except Exception as e:
        print(f"  [Download Failed] {e}")
    
    # Method 2: Manual download instructions
    print("\n" + "="*70)
    print("  MANUAL DOWNLOAD REQUIRED")
    print("="*70)
    print("\nPollo.ai videos must be downloaded manually:")
    print(f"\n1. Open: {pollo_url}")
    print("2. Click download button")
    print("3. Save to: {output_path}")
    print("4. Run this script again\n")
    
    return None


def add_max_headroom_effects_to_pollo(pollo_video: Path, audio_path: Path, 
                                       output_path: Path, qr_path: Path = None):
    """
    Take Pollo.ai Lincoln video and add:
    - Max Headroom glitches (RGB split, scan lines)
    - VHS effects (static, chromatic aberration)
    - Audio overlay (our narration + psychological audio)
    - QR code overlay
    """
    
    print(f"\n[Max Headroom FX] Adding effects to Pollo.ai video...")
    
    if not pollo_video.exists():
        print(f"  [ERROR] Pollo video not found: {pollo_video}")
        return None
    
    if not audio_path.exists():
        print(f"  [ERROR] Audio not found: {audio_path}")
        return None
    
    # Get Pollo video info
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
        duration = 15  # default
    
    # Build FFmpeg filter for Max Headroom effects
    # Input [0] = Pollo.ai video
    # Input [1] = Our audio
    # Input [2] = QR code (optional)
    
    vf_filters = []
    
    # 1. VHS effects
    vf_filters.append("""
        [0:v]format=yuv420p,
        colorchannelmixer=.3:.4:.3:0:.3:.4:.3:0:.3:.4:.3,
        noise=alls=20:allf=t+u,
        eq=contrast=1.2:brightness=0.05:saturation=1.3
        [vhs]
    """.replace('\n', '').replace('  ', ''))
    
    # 2. Max Headroom RGB split glitch
    vf_filters.append("""
        [vhs]split=3[r][g][b];
        [r]lutrgb=r=val:g=0:b=0[red];
        [g]lutrgb=r=0:g=val:b=0[green];
        [b]lutrgb=r=0:g=0:b=val[blue];
        [red][green]blend=all_mode='addition'[rg];
        [rg][blue]blend=all_mode='addition',
        geq='r=r(X+2,Y)':'g=g(X,Y)':'b=b(X-2,Y)'
        [rgb_split]
    """.replace('\n', '').replace('  ', ''))
    
    # 3. Scan lines
    vf_filters.append("""
        [rgb_split]split[main][lines];
        [lines]geq='lum=if(mod(Y,4),255,0)':cb=128:cr=128,
        format=yuva420p,colorchannelmixer=aa=0.15[scanlines];
        [main][scanlines]overlay[scanned]
    """.replace('\n', '').replace('  ', ''))
    
    # 4. Random glitch effect (time-based)
    vf_filters.append("""
        [scanned]split[a][b];
        [a]geq='r=if(lt(random(1),0.05),255,r(X,Y))':'g=g(X,Y)':'b=b(X,Y)'[glitched];
        [glitched][b]blend=all_expr='if(lt(random(1),0.95),A,B)'[final_glitch]
    """.replace('\n', '').replace('  ', ''))
    
    # 5. Add QR code if provided
    if qr_path and qr_path.exists():
        vf_filters.append(f"""
            [final_glitch][2:v]scale2ref=400:400[qr][base];
            [base][qr]overlay=w-420:20[vout]
        """.replace('\n', '').replace('  ', ''))
        map_video = '[vout]'
        qr_input = ['-loop', '1', '-i', str(qr_path)]
    else:
        map_video = '[final_glitch]'
        qr_input = []
    
    # Combine all filters
    filter_complex = ';'.join(vf_filters)
    
    # FFmpeg command
    cmd = [
        'ffmpeg', '-y',
        '-i', str(pollo_video),  # [0] Pollo.ai video
        '-i', str(audio_path),   # [1] Our audio
        *qr_input,               # [2] QR code (optional)
        '-filter_complex', filter_complex,
        '-map', map_video,
        '-map', '1:a',  # Use our audio
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
    
    print(f"  [FFmpeg] Rendering Max Headroom effects...")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0 and output_path.exists() and output_path.stat().st_size > 0:
            size_mb = output_path.stat().st_size / (1024*1024)
            print(f"  [SUCCESS] Max Headroom Pollo: {size_mb:.1f} MB")
            return output_path
        else:
            print(f"  [ERROR] FFmpeg failed")
            if result.stderr:
                print(f"  {result.stderr[-500:]}")
            return None
            
    except subprocess.TimeoutExpired:
        print(f"  [ERROR] FFmpeg timeout")
        return None
    except Exception as e:
        print(f"  [ERROR] {e}")
        return None


def create_pollo_max_headroom_video(pollo_url: str, script: str, 
                                     episode: int, title: str):
    """
    Complete workflow:
    1. Download Pollo.ai video (or use manual download)
    2. Generate our audio (voice + psychological)
    3. Add Max Headroom effects
    4. Upload to YouTube
    """
    
    print("="*70)
    print("  POLLO.AI + MAX HEADROOM PIPELINE")
    print("="*70 + "\n")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Step 1: Download Pollo video
    pollo_dir = BASE_DIR / 'pollo_videos'
    pollo_dir.mkdir(parents=True, exist_ok=True)
    
    pollo_video = pollo_dir / f'pollo_{timestamp}.mp4'
    
    downloaded = download_pollo_video(pollo_url, pollo_video)
    
    if not downloaded:
        print("\n" + "="*70)
        print("  NEXT STEPS:")
        print("="*70)
        print(f"\n1. Manually download Pollo.ai video")
        print(f"2. Save to: {pollo_video}")
        print(f"3. Run this command:\n")
        print(f"   python INTEGRATE_POLLO_VIDEO.py --manual {pollo_video} \"{script}\" {episode} \"{title}\"")
        return None
    
    # Step 2: Generate our audio
    print(f"\n[Audio] Generating narration...")
    audio_path = BASE_DIR / 'audio' / f'POLLO_{episode}_{timestamp}.mp3'
    audio_path.parent.mkdir(parents=True, exist_ok=True)
    
    if not generate_voice(script, audio_path):
        print(f"  [ERROR] Voice generation failed")
        return None
    
    # Step 3: Add Max Headroom effects
    qr_path = BASE_DIR / 'qr_codes' / 'cashapp_qr.png'
    
    output_path = BASE_DIR / 'uploaded' / f'POLLO_MAXHEAD_{episode}_{timestamp}.mp4'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    final_video = add_max_headroom_effects_to_pollo(
        pollo_video, audio_path, output_path, qr_path
    )
    
    if not final_video:
        return None
    
    # Step 4: Upload to YouTube
    print(f"\n[Upload] Uploading to YouTube...")
    
    try:
        import pickle
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        from YOUTUBE_TAG_OPTIMIZATION import generate_optimized_tags
        
        token_file = BASE_DIR / "youtube_token.pickle"
        
        if token_file.exists():
            with open(token_file, 'rb') as f:
                creds = pickle.load(f)
            
            youtube = build('youtube', 'v3', credentials=creds)
            
            # Generate optimized tags
            tags = generate_optimized_tags(title, script, 'short')
            
            hashtags = ' '.join(f'#{tag.replace(" ", "")}' for tag in tags[:15])
            description = f"""{script}

POLLO.AI + MAX HEADROOM GLITCH BROADCAST

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
            
            print(f'\n  [UPLOADED] {url}')
            
            return {
                'episode': episode,
                'url': url,
                'pollo_source': pollo_url,
                'method': 'pollo_ai_max_headroom'
            }
            
    except Exception as e:
        print(f"  [Upload Error] {e}")
        print(f"  Video ready at: {final_video}")
    
    return None


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='Pollo.ai video URL')
    parser.add_argument('--manual', help='Path to manually downloaded Pollo video')
    parser.add_argument('--script', help='Script text')
    parser.add_argument('--episode', type=int, help='Episode number')
    parser.add_argument('--title', help='Video title')
    
    args = parser.parse_args()
    
    if args.manual:
        # Use manually downloaded Pollo video
        pollo_video = Path(args.manual)
        
        if not pollo_video.exists():
            print(f"ERROR: Pollo video not found: {pollo_video}")
            sys.exit(1)
        
        script = args.script or "Default script"
        episode = args.episode or 99999
        title = args.title or f"Lincoln's WARNING #{episode}"
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Generate audio
        audio_path = BASE_DIR / 'audio' / f'POLLO_{episode}_{timestamp}.mp3'
        audio_path.parent.mkdir(parents=True, exist_ok=True)
        generate_voice(script, audio_path)
        
        # Add effects
        qr_path = BASE_DIR / 'qr_codes' / 'cashapp_qr.png'
        output_path = BASE_DIR / 'uploaded' / f'POLLO_MAXHEAD_{episode}_{timestamp}.mp4'
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        add_max_headroom_effects_to_pollo(pollo_video, audio_path, output_path, qr_path)
        
    elif args.url:
        # Try automatic download
        script = args.script or "Default script"
        episode = args.episode or 99999
        title = args.title or f"Lincoln's WARNING #{episode}"
        
        create_pollo_max_headroom_video(args.url, script, episode, title)
        
    else:
        print("Usage:")
        print("  Auto: python INTEGRATE_POLLO_VIDEO.py --url <pollo_url> --script \"text\" --episode 123 --title \"Title\"")
        print("  Manual: python INTEGRATE_POLLO_VIDEO.py --manual <path> --script \"text\" --episode 123 --title \"Title\"")


