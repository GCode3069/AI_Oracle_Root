#!/usr/bin/env python3
"""
BATCH MIXED STRATEGY GENERATOR
Creates batches using multiple competitive styles for optimal performance

Strategy Mix:
- 50% ChatGPT Poetic (quality, consistent CTR)
- 30% Cursor Consistent (safe, scalable)
- 15% Opus Sophisticated (nuanced, premium audience)
- 5% Grok Controversial (viral experiments)
"""

import sys
from pathlib import Path
from datetime import datetime
import random

sys.path.insert(0, str(Path(__file__).parent))
from abraham_MAX_HEADROOM import (
    generate_script, generate_voice, create_max_headroom_video,
    upload_to_youtube, get_headlines, BASE_DIR
)

# ============================================================================
# MIXED STRATEGY CONFIGURATION
# ============================================================================

STRATEGY_MIX = {
    'chatgpt_poetic': 0.50,      # 50% - High quality, proven CTR
    'cursor_consistent': 0.30,    # 30% - Safe, scalable baseline
    'opus_sophisticated': 0.15,   # 15% - Premium audience
    'grok_controversial': 0.05    # 5% - Viral experiments
}

CTR_DISTRIBUTION = {
    'chatgpt_poetic': 'moderate',        # 10-15% target
    'cursor_consistent': 'safe',         # 8-10% target
    'opus_sophisticated': 'moderate',    # 10-15% target
    'grok_controversial': 'moderate'     # 10-15% (safe Grok, not maximum)
}

# ============================================================================
# BATCH GENERATOR
# ============================================================================

def generate_mixed_batch(count=20, start_episode=50000):
    """
    Generate batch with mixed competitive strategies
    
    Args:
        count: Total number of videos to generate
        start_episode: Starting episode number
    
    Returns:
        List of generated video paths
    """
    
    print(f"\n{'='*80}")
    print(f"  MIXED STRATEGY BATCH GENERATOR")
    print(f"  Total Videos: {count}")
    print(f"  Starting Episode: #{start_episode}")
    print(f"{'='*80}\n")
    
    # Calculate distribution
    distribution = {}
    for style, percentage in STRATEGY_MIX.items():
        num_videos = int(count * percentage)
        if num_videos > 0:
            distribution[style] = num_videos
    
    # Ensure we hit exact count
    total_assigned = sum(distribution.values())
    if total_assigned < count:
        # Add remainder to chatgpt (highest quality)
        distribution['chatgpt_poetic'] += (count - total_assigned)
    
    print("STRATEGY DISTRIBUTION:")
    for style, num in distribution.items():
        percentage = (num / count) * 100
        print(f"  {style}: {num} videos ({percentage:.0f}%)")
    print()
    
    # Create video sequence
    video_sequence = []
    for style, num in distribution.items():
        video_sequence.extend([style] * num)
    
    # Shuffle for variety
    random.shuffle(video_sequence)
    
    # Generate videos
    generated = []
    successful = 0
    failed = 0
    
    for i, style in enumerate(video_sequence):
        episode = start_episode + i
        ctr_level = CTR_DISTRIBUTION[style]
        
        print(f"\n--- Video {i+1}/{count} ---")
        print(f"Episode: #{episode}")
        print(f"Style: {style}")
        print(f"CTR Target: {ctr_level}")
        
        try:
            result = generate_single_video(episode, style, ctr_level)
            if result:
                generated.append(result)
                successful += 1
                print(f"  [OK] Generated: {result['video_path'].name}")
            else:
                failed += 1
                print(f"  [!] Generation failed")
        except Exception as e:
            failed += 1
            print(f"  [!] Error: {e}")
    
    print(f"\n{'='*80}")
    print(f"  BATCH COMPLETE")
    print(f"  Successful: {successful}/{count}")
    print(f"  Failed: {failed}/{count}")
    print(f"  Success Rate: {(successful/count)*100:.1f}%")
    print(f"{'='*80}\n")
    
    return generated

def generate_single_video(episode, style, ctr_level):
    """Generate a single video with specified style"""
    
    # 1. Get headline
    headlines = get_headlines()
    headline = random.choice(headlines)
    
    # 2. Generate script with style
    script = generate_script(headline, style=style, ctr_level=ctr_level)
    
    # 3. Generate voice
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    audio_path = BASE_DIR / "audio" / f"MIXED_{style[:4].upper()}_{episode}_{timestamp}.mp3"
    audio_path.parent.mkdir(parents=True, exist_ok=True)
    
    if not generate_voice(script, audio_path):
        return None
    
    # 4. Get Lincoln image
    from abraham_MAX_HEADROOM import generate_lincoln_face_pollo
    lincoln_face = generate_lincoln_face_pollo()
    
    # 5. Create video output path
    video_output = BASE_DIR / "uploaded" / f"MIXED_{style[:4].upper()}_{episode}_{timestamp}.mp4"
    video_output.parent.mkdir(parents=True, exist_ok=True)
    
    # 6. Create video with ALL FEATURES ENABLED
    video_path = create_max_headroom_video(
        lincoln_image=lincoln_face,
        audio_path=audio_path,
        output_path=video_output,
        headline=headline,
        use_lipsync=True,  # ENABLED for lip sync
        use_jumpscare=True  # ENABLED for jumpscares
    )
    
    if not video_path or not Path(video_path).exists():
        return None
    
    # 7. Upload
    youtube_url = upload_to_youtube(Path(video_path), headline, episode)
    
    return {
        'episode': episode,
        'style': style,
        'ctr_level': ctr_level,
        'headline': headline,
        'script': script,
        'video_path': video_path,
        'youtube_url': youtube_url
    }

# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Mixed Strategy Batch Generator')
    parser.add_argument('count', type=int, nargs='?', default=20, help='Number of videos')
    parser.add_argument('--start', type=int, default=50000, help='Starting episode number')
    parser.add_argument('--chatgpt', type=float, help='ChatGPT percentage (0.0-1.0)')
    parser.add_argument('--cursor', type=float, help='Cursor percentage (0.0-1.0)')
    parser.add_argument('--opus', type=float, help='Opus percentage (0.0-1.0)')
    parser.add_argument('--grok', type=float, help='Grok percentage (0.0-1.0)')
    
    args = parser.parse_args()
    
    # Allow custom mix
    if args.chatgpt or args.cursor or args.opus or args.grok:
        custom_mix = {}
        if args.chatgpt: custom_mix['chatgpt_poetic'] = args.chatgpt
        if args.cursor: custom_mix['cursor_consistent'] = args.cursor
        if args.opus: custom_mix['opus_sophisticated'] = args.opus
        if args.grok: custom_mix['grok_controversial'] = args.grok
        
        # Normalize to 100%
        total = sum(custom_mix.values())
        for style in custom_mix:
            custom_mix[style] /= total
        
        # Update global mix
        STRATEGY_MIX.clear()
        STRATEGY_MIX.update(custom_mix)
        
        print(f"\n[CUSTOM MIX APPLIED]")
        for style, pct in STRATEGY_MIX.items():
            print(f"  {style}: {pct*100:.0f}%")
        print()
    
    generate_mixed_batch(args.count, args.start)

