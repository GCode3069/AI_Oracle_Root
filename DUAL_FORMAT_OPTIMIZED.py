#!/usr/bin/env python3
"""
DUAL_FORMAT_OPTIMIZED.py - Optimal length strategy for YouTube algorithm

Based on SCARIFY success: Generate BOTH short and long formats
- SHORT (15-45s): Viral algorithm boost, high CTR
- LONG (90-180s): Watch time optimization, higher revenue

This maximizes both virality AND monetization.
"""

import sys
from pathlib import Path
from datetime import datetime
import time

sys.path.insert(0, str(Path.cwd()))

from abraham_MAX_HEADROOM import generate_voice, generate_lincoln_face_pollo, upload_to_youtube, BASE_DIR, get_headlines
from DARKER_ETHICAL_SCRIPTS import get_darker_roast
from CLEAN_UP_MESSY_VISUALS import create_clean_max_headroom

class DualFormatGenerator:
    """
    Generate optimal short AND long videos for algorithm domination
    
    SHORT (15-45s):
    - Viral spread
    - High CTR
    - More impressions
    - Shorts algorithm boost
    
    LONG (90-180s):
    - Watch time
    - Higher RPM
    - More ad revenue
    - Deeper engagement
    """
    
    def __init__(self):
        self.base_dir = BASE_DIR
        self.shorts_dir = self.base_dir / "shorts"
        self.long_dir = self.base_dir / "long_form"
        self.shorts_dir.mkdir(parents=True, exist_ok=True)
        self.long_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_short(self, headline: str, episode_num: int) -> dict:
        """
        Generate SHORT format (15-45 seconds)
        
        Optimized for:
        - YouTube Shorts algorithm
        - TikTok viral potential
        - Instagram Reels
        - Quick consumption
        """
        
        print(f"\n[SHORT #{episode_num}] Generating...")
        
        # Get SHORT script (15-30 words = 15-25 seconds)
        script = get_darker_roast(headline)
        
        # Trim to short length
        words = script.split()
        if len(words) > 35:
            script = ' '.join(words[:35]) + "! Scan QR!"
        
        print(f"  Script: {len(script.split())} words")
        print(f"  Target: 15-45 seconds")
        
        # Generate voice
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        audio_path = self.base_dir / 'audio' / f'SHORT_{episode_num}_{timestamp}.mp3'
        audio_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not generate_voice(script, audio_path):
            return None
        
        # Get Lincoln
        lincoln = generate_lincoln_face_pollo()
        
        # Get QR
        qr = self.base_dir / 'qr_codes' / 'cashapp_qr.png'
        
        # Create video
        output = self.shorts_dir / f'SHORT_{episode_num}_{timestamp}.mp4'
        video = create_clean_max_headroom(lincoln, audio_path, output, qr)
        
        if video and Path(video).exists():
            duration = Path(video).stat().st_size / (1024*1024)
            print(f"  [OK] SHORT created: {duration:.1f} MB")
            
            # Upload
            url = upload_to_youtube(Path(video), headline, episode_num)
            
            return {
                'type': 'short',
                'episode': episode_num,
                'video': str(video),
                'url': url,
                'script_words': len(script.split())
            }
        
        return None
    
    def generate_long(self, headline: str, episode_num: int) -> dict:
        """
        Generate LONG format (90-180 seconds)
        
        Optimized for:
        - Watch time algorithm boost
        - Higher RPM/revenue
        - Deeper engagement
        - More comprehensive roast
        """
        
        print(f"\n[LONG #{episode_num}] Generating...")
        
        # Get LONG script by combining multiple roasts
        scripts = []
        for _ in range(3):  # Combine 3 roasts for longer content
            scripts.append(get_darker_roast(headline))
        
        # Join with transitions
        long_script = f"""LINCOLN! Multiple angles on {headline}!

ANGLE ONE: {scripts[0]}

ANGLE TWO: {scripts[1]}

FINAL ANGLE: {scripts[2]}

The system is RIGGED at EVERY level! Scan QR to break free!"""
        
        print(f"  Script: {len(long_script.split())} words")
        print(f"  Target: 90-180 seconds")
        
        # Generate voice
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        audio_path = self.base_dir / 'audio' / f'LONG_{episode_num}_{timestamp}.mp3'
        audio_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not generate_voice(long_script, audio_path):
            return None
        
        # Get Lincoln
        lincoln = generate_lincoln_face_pollo()
        
        # Get QR
        qr = self.base_dir / 'qr_codes' / 'cashapp_qr.png'
        
        # Create video
        output = self.long_dir / f'LONG_{episode_num}_{timestamp}.mp4'
        video = create_clean_max_headroom(lincoln, audio_path, output, qr)
        
        if video and Path(video).exists():
            duration = Path(video).stat().st_size / (1024*1024)
            print(f"  [OK] LONG created: {duration:.1f} MB")
            
            # Upload
            url = upload_to_youtube(Path(video), headline, episode_num)
            
            return {
                'type': 'long',
                'episode': episode_num,
                'video': str(video),
                'url': url,
                'script_words': len(long_script.split())
            }
        
        return None
    
    def generate_dual_batch(self, count_per_format=5, start_episode=5000):
        """
        Generate batch of BOTH formats
        
        Args:
            count_per_format: How many of each format (default: 5)
            start_episode: Starting episode number
        
        Results:
            5 SHORT + 5 LONG = 10 videos total
        """
        
        print("="*70)
        print("  DUAL FORMAT BATCH GENERATION")
        print("="*70 + "\n")
        
        print(f"Generating {count_per_format} SHORT + {count_per_format} LONG")
        print(f"Starting at episode #{start_episode}\n")
        
        results = {
            'shorts': [],
            'longs': []
        }
        
        headlines = []
        # Get enough headlines
        for _ in range(count_per_format * 2):
            from abraham_MAX_HEADROOM import get_headlines
            headlines.extend(get_headlines())
        
        # Generate shorts
        print("\n" + "="*70)
        print("  GENERATING SHORTS (15-45 seconds)")
        print("="*70)
        
        for i in range(count_per_format):
            episode = start_episode + i
            headline = headlines[i] if i < len(headlines) else "Breaking News"
            
            result = self.generate_short(headline, episode)
            if result:
                results['shorts'].append(result)
            
            # Delay to prevent API rate limits
            if i < count_per_format - 1:
                print("  Waiting 30 seconds...")
                time.sleep(30)
        
        # Generate longs
        print("\n" + "="*70)
        print("  GENERATING LONG-FORM (90-180 seconds)")
        print("="*70)
        
        for i in range(count_per_format):
            episode = start_episode + 1000 + i  # Different episode range
            headline = headlines[count_per_format + i] if count_per_format + i < len(headlines) else "Breaking News"
            
            result = self.generate_long(headline, episode)
            if result:
                results['longs'].append(result)
            
            # Delay to prevent API rate limits
            if i < count_per_format - 1:
                print("  Waiting 30 seconds...")
                time.sleep(30)
        
        # Summary
        print("\n" + "="*70)
        print("  DUAL FORMAT BATCH COMPLETE")
        print("="*70 + "\n")
        
        print(f"SHORT videos: {len(results['shorts'])}/{count_per_format}")
        print(f"LONG videos: {len(results['longs'])}/{count_per_format}")
        print(f"TOTAL: {len(results['shorts']) + len(results['longs'])} videos\n")
        
        print("SHORT videos (viral potential):")
        for s in results['shorts']:
            print(f"  #{s['episode']}: {s['url']}")
        
        print("\nLONG videos (watch time):")
        for l in results['longs']:
            print(f"  #{l['episode']}: {l['url']}")
        
        return results

if __name__ == "__main__":
    generator = DualFormatGenerator()
    
    print("""
╔═══════════════════════════════════════════════════════════════╗
║         DUAL FORMAT OPTIMIZATION STRATEGY                     ║
╚═══════════════════════════════════════════════════════════════╝

Based on SCARIFY success:

SHORT FORM (15-45s):
  - Viral algorithm boost
  - High CTR potential
  - More impressions
  - YouTube Shorts priority
  - TikTok/Instagram Reels ready

LONG FORM (90-180s):
  - Watch time signal
  - Higher RPM (revenue per mille)
  - Mid-roll ads possible
  - Deeper engagement
  - Algorithm recommends more

STRATEGY:
  Generate BOTH for maximum algorithm coverage
  Short: Quick viral spread
  Long: Monetization optimization
  
USAGE:
  python DUAL_FORMAT_OPTIMIZED.py
  
  Will generate 5 SHORT + 5 LONG = 10 videos total
""")
    
    confirmation = input("\nGenerate dual format batch? (yes/no): ")
    
    if confirmation.lower() == 'yes':
        generator.generate_dual_batch(count_per_format=5, start_episode=5000)


