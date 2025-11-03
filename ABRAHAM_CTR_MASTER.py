#!/usr/bin/env python3
"""
ABRAHAM CTR MASTER - MAXIMUM CLICK-THROUGH RATE OPTIMIZER
Engineered to outsmart YouTube's algorithm with proven CTR tactics
"""

import os
import sys
import random
from pathlib import Path
from datetime import datetime

# Import our working base system
sys.path.insert(0, str(Path(__file__).parent))
from abraham_MAX_HEADROOM import (
    generate_voice, create_max_headroom_video, upload_to_youtube,
    get_headlines, generate_lincoln_face_pollo, BASE_DIR
)

# ============================================================================
# CTR OPTIMIZATION FORMULAS - PROVEN TO GET CLICKS
# ============================================================================

CTR_TITLE_PATTERNS = [
    "This {topic} Secret SHOCKED Everyone",
    "They DON'T Want You Knowing This About {topic}",
    "The {topic} Truth They're Hiding",
    "What {topic} REALLY Means (Scary)",
    "I Tried {topic} For 30 Days...",
    "The {topic} Industry Doesn't Want This Out",
    "Why {topic} Is Actually Terrifying",
    "{topic}: What Nobody Tells You",
    "The Dark Side of {topic} (Revealed)",
    "How {topic} Controls Everything"
]

SHOCK_HOOKS = [
    "Listen... what I'm about to tell you...",
    "Stop scrolling. You need to hear this.",
    "They said I couldn't say this...",
    "This is the part they don't show you...",
    "Before you scroll away, watch this...",
    "I'm risking everything telling you this...",
    "You've been lied to about this...",
    "This is what they're hiding...",
]

PAYOFF_ENDINGS = [
    "Now you know what they didn't want you to see.",
    "That's the truth they're hiding.",
    "And that's why everything's different now.",
    "Wake up. Share this before it's deleted.",
    "Don't let them bury this truth.",
    "The question is... what will YOU do?",
    "Still think it's just a coincidence?",
    "And THAT'S the real story."
]

# ============================================================================
# SCRIPT GENERATOR - CTR OPTIMIZED (12-15 SECONDS)
# ============================================================================

def generate_ctr_script(headline):
    """
    Generate 12-15 second script optimized for:
    - Immediate hook (0-3s)
    - Curiosity gap
    - Pattern interrupt
    - Satisfying payoff
    - Call-to-action
    """
    
    # Extract topic from headline
    topic = headline.split(':')[0].strip() if ':' in headline else headline[:30]
    
    # Structure: HOOK (3s) + REVELATION (6s) + PAYOFF (3s)
    hook = random.choice(SHOCK_HOOKS)
    
    # Core revelation (dark satirical truth)
    revelations = [
        f"{topic}? Lincoln's corpse knows better. They're selling you fear while pocketing the profit.",
        f"While you panic about {topic}, they're laughing all the way to the bank. Classic misdirection.",
        f"{topic} is just the headline. The real horror? Nobody's asking WHO benefits from your fear.",
        f"You think {topic} is the story? That's what they WANT you focused on. Look deeper.",
        f"{topic} - another circus for the masses. Meanwhile, the real theft happens in the fine print."
    ]
    
    revelation = random.choice(revelations)
    payoff = random.choice(PAYOFF_ENDINGS)
    
    script = f"{hook} {revelation} {payoff}"
    
    # Add Bitcoin CTA (subtle)
    script += " Support truth. Bitcoin below."
    
    return script

# ============================================================================
# TITLE GENERATOR - MAXIMUM CTR
# ============================================================================

def generate_ctr_title(headline, episode_num):
    """
    Generate titles engineered for maximum click-through rate
    
    Proven elements:
    - Numbers (increase CTR 36%)
    - Capitals for emphasis (not ALL CAPS)
    - Curiosity gap
    - Urgency
    - Specificity
    """
    
    # Extract topic
    topic = headline.split(':')[0].strip() if ':' in headline else headline[:30]
    
    # Select pattern
    pattern = random.choice(CTR_TITLE_PATTERNS)
    title_base = pattern.format(topic=topic)
    
    # Add episode number for series effect
    title = f"Lincoln #{episode_num}: {title_base}"
    
    # Add urgency tag
    urgency_tags = ["#MustWatch", "#Viral", "#Truth", "#Exposed", "#Shocking"]
    title += f" {random.choice(urgency_tags)}"
    
    return title

# ============================================================================
# DESCRIPTION GENERATOR - ALGORITHM OPTIMIZED
# ============================================================================

def generate_ctr_description(headline, script):
    """
    Generate description that:
    - Front-loads keywords
    - Creates curiosity gap
    - Includes CTAs
    - Optimizes for search
    """
    
    topic = headline.split(':')[0].strip() if ':' in headline else headline[:30]
    
    description = f"""Abraham Lincoln reveals the TRUTH about {topic} that mainstream media won't cover.

This is what they don't want you to know...

🔴 SHOCKING REVELATION inside
🔴 Everything changes after watching this
🔴 Share before it's deleted

The truth about {topic} is darker than you think. Lincoln's ghost breaks it down in 15 seconds.

━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 SUPPORT TRUTH - Bitcoin/Cash App in video
━━━━━━━━━━━━━━━━━━━━━━━━━━

Subscribe for daily truth bombs that expose the real story behind the headlines.

#Lincoln #Truth #{topic.replace(' ', '')} #Exposed #Viral #MustWatch #Shorts

━━━━━━━━━━━━━━━━━━━━━━━━━━
Script: {script[:100]}...
━━━━━━━━━━━━━━━━━━━━━━━━━━

AI-generated historical satire. For entertainment purposes.
"""
    
    return description

# ============================================================================
# TAGS GENERATOR - SEARCH OPTIMIZED
# ============================================================================

def generate_ctr_tags(headline):
    """Generate tags optimized for YouTube search and discovery"""
    
    topic = headline.split(':')[0].strip() if ':' in headline else headline[:30]
    
    # Core tags (always included)
    core_tags = [
        "abraham lincoln",
        "shocking truth",
        "exposed",
        "viral shorts",
        "must watch"
    ]
    
    # Topic-specific tags
    topic_tag = topic.lower().replace(' ', '')
    topic_tags = [
        topic.lower(),
        f"{topic} exposed",
        f"{topic} truth",
        f"{topic} revealed"
    ]
    
    # Trending tags
    trending_tags = [
        "youtube shorts",
        "viral video",
        "truth exposed",
        "dark truth",
        "hidden truth",
        "conspiracy",
        "red pill",
        "wake up"
    ]
    
    all_tags = core_tags + topic_tags + trending_tags
    
    # Return first 15 (YouTube limit is ~500 chars)
    return all_tags[:15]

# ============================================================================
# MAIN CTR OPTIMIZER
# ============================================================================

def generate_ctr_optimized_video(episode_num=None):
    """
    Generate a single video optimized for maximum CTR
    
    Process:
    1. Get trending headline
    2. Generate CTR-optimized script (12-15s)
    3. Create video with all effects
    4. Upload with CTR-optimized metadata
    """
    
    if not episode_num:
        episode_num = int(os.getenv('EPISODE_NUM', str(random.randint(10000, 99999))))
    
    print(f"\n{'='*80}")
    print(f"  CTR MASTER - Episode #{episode_num}")
    print(f"  Optimizing for maximum click-through rate...")
    print(f"{'='*80}\n")
    
    # 1. Get headline
    print("[1/5] Getting trending headline...")
    headlines = get_headlines()
    headline = random.choice(headlines) if headlines else "Government Corruption Exposed"
    print(f"  Topic: {headline}")
    
    # 2. Generate CTR script
    print("\n[2/5] Generating CTR-optimized script...")
    script = generate_ctr_script(headline)
    print(f"  Script ({len(script.split())} words):")
    print(f"  {script[:100]}...")
    
    # 3. Generate voice
    print("\n[3/5] Generating voice...")
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    audio_path = BASE_DIR / "abraham_horror" / "audio" / f"CTR_{episode_num}_{timestamp}.mp3"
    audio_path.parent.mkdir(parents=True, exist_ok=True)
    
    if not generate_voice(script, audio_path):
        print("  [!] Voice generation failed, skipping...")
        return None
    
    # 4. Create video
    print("\n[4/5] Creating CTR-optimized video...")
    print("  - Max Headroom VHS effects")
    print("  - Cash App QR code")
    print("  - Pattern interrupts")
    print("  - Optimal pacing (12-15s)")
    
    video_path = create_max_headroom_video(
        audio_path=audio_path,
        episode_num=episode_num,
        use_lipsync=False,  # Speed over quality for CTR
        use_broll=True
    )
    
    if not video_path or not video_path.exists():
        print("  [!] Video creation failed")
        return None
    
    # 5. Upload with CTR-optimized metadata
    print("\n[5/5] Uploading with CTR-optimized metadata...")
    
    title = generate_ctr_title(headline, episode_num)
    description = generate_ctr_description(headline, script)
    tags = generate_ctr_tags(headline)
    
    print(f"  Title: {title}")
    print(f"  Tags: {', '.join(tags[:5])}...")
    
    # Custom upload with CTR metadata
    try:
        from youtube_uploader import upload_video_with_metadata
        
        video_url = upload_video_with_metadata(
            video_path=str(video_path),
            title=title,
            description=description,
            tags=tags,
            category="24",  # Entertainment
            privacy="public"
        )
        
        print(f"\n  [OK] Uploaded: {video_url}")
        
    except ImportError:
        # Fallback to standard upload
        video_url = upload_to_youtube(video_path, headline, episode_num)
    
    print(f"\n{'='*80}")
    print(f"  [OK] CTR MASTER COMPLETE")
    print(f"  Episode #{episode_num} optimized for maximum clicks")
    print(f"{'='*80}\n")
    
    return video_path

# ============================================================================
# BATCH CTR GENERATION
# ============================================================================

def generate_ctr_batch(count=10, start_episode=None):
    """Generate multiple CTR-optimized videos"""
    
    if not start_episode:
        start_episode = int(os.getenv('EPISODE_NUM', '20000'))
    
    print(f"\n{'='*80}")
    print(f"  CTR MASTER - BATCH MODE")
    print(f"  Generating {count} CTR-optimized videos")
    print(f"  Starting from Episode #{start_episode}")
    print(f"{'='*80}\n")
    
    successful = 0
    failed = 0
    
    for i in range(count):
        episode = start_episode + i
        
        print(f"\n--- Video {i+1}/{count} ---")
        
        try:
            result = generate_ctr_optimized_video(episode)
            if result:
                successful += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  [!] Error: {e}")
            failed += 1
    
    print(f"\n{'='*80}")
    print(f"  BATCH COMPLETE")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Success Rate: {(successful/count)*100:.1f}%")
    print(f"{'='*80}\n")

# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='CTR Master - Maximum Click-Through Rate Optimizer')
    parser.add_argument('count', type=int, nargs='?', default=1, help='Number of videos to generate')
    parser.add_argument('--episode', type=int, help='Starting episode number')
    
    args = parser.parse_args()
    
    if args.count == 1:
        generate_ctr_optimized_video(args.episode)
    else:
        generate_ctr_batch(args.count, args.episode)


