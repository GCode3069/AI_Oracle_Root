#!/usr/bin/env python3
"""
MASS_GENERATE_100_VIDEOS.py - Generate 100 videos for 72-hour challenge

Strategy:
- 100 videos total
- Mixed styles (Cursor, Grok, ChatGPT)
- Mixed formats (30s short, 60-90s long)
- All with binaural beats, optimized tags
- Batch upload ready
"""

import sys
import time
import random
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path.cwd()))

from abraham_MAX_HEADROOM import generate_voice, generate_lincoln_face_pollo, BASE_DIR
from CLEAN_UP_MESSY_VISUALS import create_clean_max_headroom
from YOUTUBE_TAG_OPTIMIZATION import generate_optimized_tags
from MULTI_STYLE_SCRIPT_GENERATOR import ScriptStyleGenerator
from FEAR_OPTIMIZED_SCRIPTS import get_unique_script, ALL_UNIQUE_SCRIPTS
import hashlib

def scrape_trending_headlines(count=100):
    """Scrape 100 trending headlines"""
    headlines = []
    
    # Mix of RSS sources
    sources = [
        'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
        'https://feeds.bbci.co.uk/news/rss.xml',
        'https://www.reddit.com/r/news/.rss',
        'https://www.reddit.com/r/politics/.rss',
        'https://www.reddit.com/r/worldnews/.rss'
    ]
    
    try:
        import feedparser
        
        for source in sources:
            feed = feedparser.parse(source)
            for entry in feed.entries[:20]:  # 20 from each source
                headlines.append(entry.title)
                if len(headlines) >= count:
                    break
            if len(headlines) >= count:
                break
    except:
        pass
    
    # Fallback to template headlines if scraping fails
    if len(headlines) < count:
        templates = [
            "Government Shutdown Day {n}",
            "Market Crash Fears Rise",
            "Crypto Regulation Debate Heats Up",
            "AI Safety Summit Results",
            "Presidential Campaign Trail",
            "Economic Recession Warnings",
            "Social Media Algorithm Changes",
            "Climate Policy Controversy",
            "Tech Layoffs Continue",
            "Housing Market Concerns"
        ]
        
        while len(headlines) < count:
            template = random.choice(templates)
            headlines.append(template.format(n=random.randint(1, 100)))
    
    return headlines[:count]

def generate_batch_videos(total_count=100, pollo_count=0):
    """
    Generate 100 videos in batch
    
    pollo_count: Number to reserve for Pollo.ai (you'll generate these manually)
    static_count: Total - pollo = videos to generate now
    """
    
    print("="*70)
    print("  MASS GENERATION - 100 VIDEOS FOR 72-HOUR CHALLENGE")
    print("="*70 + "\n")
    
    static_count = total_count - pollo_count
    
    print(f"Target: {total_count} total videos")
    print(f"  - {static_count} static videos (generating now)")
    print(f"  - {pollo_count} Pollo videos (manual generation on Pollo.ai)")
    print(f"\nGenerating {static_count} videos now...\n")
    
    # Scrape headlines
    print("[1/4] Scraping trending headlines...")
    headlines = scrape_trending_headlines(static_count)
    print(f"  Got {len(headlines)} headlines\n")
    
    # Initialize style generator
    style_gen = ScriptStyleGenerator()
    
    # Track used scripts (prevent duplicates!)
    used_script_hashes = set()
    
    # Style distribution (based on Battle Royale results)
    # 50% ChatGPT, 30% Cursor, 15% Grok, 5% Opus
    styles = []
    styles.extend(['chatgpt'] * int(static_count * 0.5))
    styles.extend(['cursor'] * int(static_count * 0.3))
    styles.extend(['grok'] * int(static_count * 0.15))
    styles.extend(['opus'] * int(static_count * 0.05))
    random.shuffle(styles)
    
    # Ensure we have enough
    while len(styles) < static_count:
        styles.append(random.choice(['chatgpt', 'cursor']))
    styles = styles[:static_count]
    
    # Format distribution (60% short, 40% long)
    formats = []
    formats.extend(['short'] * int(static_count * 0.6))
    formats.extend(['long'] * int(static_count * 0.4))
    random.shuffle(formats)
    formats = formats[:static_count]
    
    # Generate videos
    print(f"[2/4] Generating {static_count} videos...")
    print(f"  Styles: {styles.count('chatgpt')} ChatGPT, {styles.count('cursor')} Cursor, {styles.count('grok')} Grok, {styles.count('opus')} Opus")
    print(f"  Formats: {formats.count('short')} short, {formats.count('long')} long\n")
    
    batch_dir = BASE_DIR / 'batch_upload'
    batch_dir.mkdir(parents=True, exist_ok=True)
    
    success_count = 0
    failed_count = 0
    
    for i in range(static_count):
        episode = 100000 + i  # Start at 100000
        headline = headlines[i]
        style = styles[i]
        format_type = formats[i]
        
        print(f"\n[{i+1}/{static_count}] Episode #{episode}")
        print(f"  Headline: {headline}")
        print(f"  Style: {style}, Format: {format_type}")
        
        try:
            # Generate UNIQUE script (40% use fear-optimized, 60% use style generator)
            if random.random() < 0.4:
                # Use pre-written fear-optimized scripts (guaranteed unique!)
                script, script_hash = get_unique_script(used_script_hashes)
                print(f"  [FEAR-OPTIMIZED] Using pre-written horror script")
            else:
                # Generate with style (with uniqueness check)
                for attempt in range(5):
                    if style == 'chatgpt':
                        script = style_gen.chatgpt_style(headline)
                    elif style == 'grok':
                        script = style_gen.grok_style(headline)
                    elif style == 'opus':
                        script = style_gen.opus_style(headline)
                    else:  # cursor
                        script = style_gen.cursor_style(headline)
                    
                    script_hash = hashlib.md5(script.encode()).hexdigest()
                    if script_hash not in used_script_hashes:
                        used_script_hashes.add(script_hash)
                        break
                    print(f"  [RETRY {attempt+1}] Duplicate detected, regenerating...")
            
            # Adjust length based on format
            if format_type == 'long':
                # Expand script for long format
                script = script + " " + style_gen.cursor_style(headline)  # Double up
            
            # Generate title
            if format_type == 'short':
                title = f"Lincoln's WARNING #{episode}: {headline[:40]} #Shorts"
            else:
                title = f"Lincoln's WARNING #{episode}: {headline[:50]}"
            
            # Generate voice
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            audio_path = BASE_DIR / 'audio' / f'BATCH_{episode}_{timestamp}.mp3'
            audio_path.parent.mkdir(parents=True, exist_ok=True)
            
            if not generate_voice(script, audio_path):
                print(f"  [FAILED] Voice generation")
                failed_count += 1
                continue
            
            # Get Lincoln
            lincoln = generate_lincoln_face_pollo()
            
            # Get QR
            qr = BASE_DIR / 'qr_codes' / 'cashapp_qr.png'
            
            # Create video
            output = batch_dir / f'VIDEO_{episode}_{timestamp}.mp4'
            
            video = create_clean_max_headroom(lincoln, audio_path, output, qr)
            
            if not video or not Path(video).exists():
                print(f"  [FAILED] Video creation")
                failed_count += 1
                continue
            
            # Generate metadata for upload
            tags = generate_optimized_tags(title, script, format_type)
            
            metadata = {
                'episode': episode,
                'title': title,
                'script': script,
                'tags': tags,
                'format': format_type,
                'style': style,
                'video_path': str(video),
                'created': datetime.now().isoformat()
            }
            
            # Save metadata
            import json
            meta_file = batch_dir / f'VIDEO_{episode}_{timestamp}.json'
            with open(meta_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            size_mb = Path(video).stat().st_size / (1024*1024)
            print(f"  [OK] {size_mb:.1f} MB - {len(tags)} tags")
            
            success_count += 1
            
            # Brief pause to avoid API rate limits
            if i < static_count - 1:
                time.sleep(2)
                
        except Exception as e:
            print(f"  [ERROR] {e}")
            failed_count += 1
    
    print("\n" + "="*70)
    print("  BATCH GENERATION COMPLETE")
    print("="*70 + "\n")
    
    print(f"Success: {success_count}/{static_count}")
    print(f"Failed: {failed_count}/{static_count}")
    print(f"Success rate: {success_count/static_count*100:.1f}%\n")
    
    print(f"Videos saved to: {batch_dir}\n")
    
    if pollo_count > 0:
        print(f"[3/4] MANUAL STEP: Generate {pollo_count} Pollo.ai videos")
        print(f"  1. Go to Pollo.ai")
        print(f"  2. Use the 797-char horror prompt")
        print(f"  3. Generate {pollo_count} videos")
        print(f"  4. Download to: {BASE_DIR / 'pollo_videos' / 'batch_1'}")
        print(f"  5. Run: python PROCESS_POLLO_BATCH.py\n")
    
    print(f"[4/4] Next step: Upload to platforms")
    print(f"  Run: python DEPLOY_ALL_PLATFORMS.py\n")
    
    print("="*70)
    print(f"  {success_count} VIDEOS READY FOR 72-HOUR CHALLENGE!")
    print("="*70 + "\n")
    
    return success_count

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--total', type=int, default=100, help='Total videos to generate')
    parser.add_argument('--pollo', type=int, default=30, help='Videos to reserve for Pollo.ai (manual)')
    
    args = parser.parse_args()
    
    generate_batch_videos(args.total, args.pollo)

