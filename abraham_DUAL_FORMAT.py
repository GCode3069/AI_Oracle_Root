#!/usr/bin/env python3
"""
ABRAHAM LINCOLN - DUAL FORMAT GENERATOR
Creates BOTH sweet spot shorts (9-17s) AND long videos (60+ seconds)

SHORT FORMAT (9-17s):
- Optimized for retention (45%+ proven)
- Shorts feed algorithm (95.3% of traffic)
- Quick viral potential

LONG FORMAT (60-90s):
- Mid-roll ads enabled (100x better CPM)
- $3-8 per 1,000 views (vs $0.01-0.03 shorts)
- Better monetization once eligible

Usage:
python abraham_DUAL_FORMAT.py --short 10    # Generate 10 shorts (9-17s)
python abraham_DUAL_FORMAT.py --long 10     # Generate 10 long videos (60-90s)
python abraham_DUAL_FORMAT.py --both 10     # Generate 10 of EACH format
"""
import os
import sys
import random
from pathlib import Path
from datetime import datetime

# Import main system
sys.path.insert(0, str(Path(__file__).parent))
from abraham_MAX_HEADROOM import (
    generate_script,
    generate_voice,
    generate_lincoln_face_pollo,
    create_max_headroom_video,
    upload_to_youtube,
    get_headlines,
    log_to_google_sheets
)

BASE_DIR = Path("F:/AI_Oracle_Root/scarify/abraham_horror")

def generate_short_script(headline):
    """
    Generate SHORT script (9-17 seconds = 32-45 words)
    Optimized for 45% retention
    """
    # Use existing short script generator
    return generate_script(headline)

def generate_long_script(headline):
    """
    Generate LONG script (60-90 seconds = 150-225 words)
    Includes multiple roasts, more depth, better monetization
    """
    hl = headline.lower()
    
    # LONG FORMAT: 3-act structure for engagement
    if "trump" in hl or "republican" in hl or "gop" in hl:
        return f"""Lincoln here! BACK from the dead! And BOY do I have things to say!

{headline}

ACT 1: THE RICH
Let's talk about Trump. BILLIONAIRE! Born with gold spoon! Never worked a REAL day!

But he convinced POOR people he's "one of them"! That's like ROACHES voting for RAID!

Chappelle said it: "He's a white Kanye!" And you're buying it!

ACT 2: THE DEMOCRATS  
But wait! Democrats ain't innocent!

Pelosi worth $100 MILLION preaching about inequality! AOC at Met Gala in designer dress!

Bernie screaming about billionaires while owning THREE HOUSES!

Pryor laughing: "They ALL lying to you!"

ACT 3: THE SYSTEM
Carlin's truth: "It's a BIG CLUB and you AIN'T in it!"

Republicans serve the rich! Democrats serve the rich! They're the SAME PARTY wearing different TIES!

You're ALL getting robbed! Left voters! Right voters! Non-voters!

The game is RIGGED! The house ALWAYS wins! And you keep PLAYING!

I died believing in democracy. You got OLIGARCHY with better marketing!

Wake UP! Or stay ASLEEP! I don't care anymore!

Look in mirrors. Bitcoin QR in video. Support if you're smart enough to see the con.

This is Lincoln. Transmission ends. *static*"""

    elif "police" in hl or "shooting" in hl:
        return f"""Abraham Lincoln here! Let me tell you about LAW and ORDER!

{headline}

THE POLICE PROBLEM
Cops got GUNS! BADGES! QUALIFIED IMMUNITY! And they're scared of UNARMED people?!

Pryor said it BEST: "Police scare ME and I ain't even done nothing!"

Now they're KILLING people! With phones! With wallets! With NOTHING!

I commanded ARMIES in war! My soldiers had ACCOUNTABILITY! What do cops have? PAID LEAVE!

THE DEFUND PROBLEM  
But "Defund Police" crowd - you think criminals gonna police THEMSELVES?!

That's the DUMBEST thing I ever heard! And I've been DEAD for 160 years!

Robin Williams would say: "That's weapons-grade STUPIDITY!"

THE CONSERVATIVE HYPOCRISY
"Back the Blue!" you scream! Until they're at YOUR door with a warrant!

Then it's "Government tyranny!" Which IS it?!

THE LIBERAL HYPOCRISY
You want police reform! But you VOTE for the same politicians who INCREASE police budgets!

Bernie Mac energy: EVERYBODY wrong! Cops wrong! Defund wrong! Politicians wrong! YOU wrong!

THE REAL SOLUTION
Fix the SYSTEM! Training! Accountability! Community policing!

But nobody wants SOLUTIONS! You want OUTRAGE! You want to YELL!

Carlin knew: "They keep you fighting about FLAGS and PRONOUNS so you don't notice they're ROBBING you!"

I died for justice. You got INJUSTICE incorporated! With stock options!

Look in mirrors. This is Lincoln. *static*"""

    else:
        # General long roast
        return f"""Abraham Lincoln! Dead president! Live broadcast from the afterlife!

{headline}

PART 1: REPUBLICANS
You want small government that fits in a WOMAN's uterus!

You scream "Freedom!" while banning BOOKS! Explain that logic!

"Family values!" from three-time divorcees! "Fiscal responsibility!" while exploding the debt!

PART 2: DEMOCRATS  
You preach tolerance while CANCELING everyone! You want diversity of EVERYTHING except THOUGHT!

"Tax the rich!" scream the MILLIONAIRE politicians! 

You're solving racism with MORE racism! Sexism with MORE sexism! That's not progress - that's a LOOP!

PART 3: THE RICH
Billionaires hoarding DRAGONS' HOARDS of wealth! 

Bezos in SPACE while workers piss in BOTTLES! Musk buying Twitter for EGO! Zuckerberg stealing privacy!

Pryor observed: "Rich people problems: Which yacht to take!" Poor people problems: "Which MEAL to skip!"

PART 4: THE POOR
You defend billionaires! "They earned it!" No they INHERITED it! Or STOLE it!

You vote AGAINST your own interests! Every. Single. Election!

Bernie Mac screaming from heaven: "STOP being STUPID!"

PART 5: EVERYONE
Carlin's final word: "Garbage in! Garbage out! They OWN you!"

Left! Right! Rich! Poor! Black! White! You're ALL getting PLAYED!

The American dream? More like American SCHEME!

I preserved the Union! You're destroying it for LIKES and RETWEETS!

April 14, 1865. Booth shot me. Nine hours dying. I saw YOUR future.

I was WRONG to believe in you.

Prove me wrong. I DARE you!

Look in mirrors. Lincoln out. *static burst*"""

def generate_short_video(episode_num):
    """Generate SHORT format video (9-17 seconds)"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    print(f"\n{'='*70}")
    print(f"GENERATING SHORT FORMAT - Episode #{episode_num}")
    print(f"{'='*70}\n")
    
    headlines = get_headlines()
    headline = random.choice(headlines)
    print(f"[Headline] {headline}")
    
    # SHORT script
    script = generate_short_script(headline)
    word_count = len(script.split())
    print(f"[Script] {word_count} words (target: 32-45 for 9-17s)")
    print(f"[Format] SHORT (optimized for retention)\n")
    
    # Generate audio
    audio_path = BASE_DIR / f"audio/SHORT_{episode_num}.mp3"
    if not generate_voice(script, audio_path):
        return None
    
    # Get Lincoln image
    lincoln_image = generate_lincoln_face_pollo()
    
    # Create video
    video_path = BASE_DIR / f"videos/SHORT_{episode_num}.mp4"
    if not create_max_headroom_video(lincoln_image, audio_path, video_path, headline, 
                                     use_lipsync=True, use_jumpscare=True):
        return None
    
    # Upload
    youtube_url = upload_to_youtube(video_path, headline, episode_num)
    
    # Track
    log_to_google_sheets(episode_num, headline, script, video_path, youtube_url or "")
    
    # Copy to uploaded
    uploaded_path = BASE_DIR / "uploaded" / f"SHORT_{episode_num}.mp4"
    import shutil
    shutil.copy2(video_path, uploaded_path)
    
    print(f"\n[SHORT] ✅ Complete: {uploaded_path.name}")
    if youtube_url:
        print(f"[YouTube] {youtube_url}")
    print()
    
    return str(uploaded_path)

def generate_long_video(episode_num):
    """Generate LONG format video (60-90 seconds)"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    print(f"\n{'='*70}")
    print(f"GENERATING LONG FORMAT - Episode #{episode_num}")
    print(f"{'='*70}\n")
    
    headlines = get_headlines()
    headline = random.choice(headlines)
    print(f"[Headline] {headline}")
    
    # LONG script
    script = generate_long_script(headline)
    word_count = len(script.split())
    print(f"[Script] {word_count} words (target: 150-225 for 60-90s)")
    print(f"[Format] LONG (mid-roll ads enabled)\n")
    
    # Generate audio
    audio_path = BASE_DIR / f"audio/LONG_{episode_num}.mp3"
    if not generate_voice(script, audio_path):
        return None
    
    # Get Lincoln image
    lincoln_image = generate_lincoln_face_pollo()
    
    # Create video (will use optimized path for 60+ seconds)
    video_path = BASE_DIR / f"videos/LONG_{episode_num}.mp4"
    if not create_max_headroom_video(lincoln_image, audio_path, video_path, headline, 
                                     use_lipsync=True, use_jumpscare=True):
        return None
    
    # Upload
    youtube_url = upload_to_youtube(video_path, headline, episode_num)
    
    # Track
    log_to_google_sheets(episode_num, headline, script, video_path, youtube_url or "")
    
    # Copy to uploaded
    uploaded_path = BASE_DIR / "uploaded" / f"LONG_{episode_num}.mp4"
    import shutil
    shutil.copy2(video_path, uploaded_path)
    
    print(f"\n[LONG] ✅ Complete: {uploaded_path.name}")
    if youtube_url:
        print(f"[YouTube] {youtube_url}")
    print()
    
    return str(uploaded_path)

if __name__ == "__main__":
    import sys
    
    mode = "short"  # Default
    count = 1
    start_ep = 2000
    
    # Parse arguments
    for arg in sys.argv[1:]:
        if arg.startswith("--short"):
            mode = "short"
            try:
                count = int(sys.argv[sys.argv.index(arg) + 1])
            except:
                count = 1
        elif arg.startswith("--long"):
            mode = "long"
            try:
                count = int(sys.argv[sys.argv.index(arg) + 1])
            except:
                count = 1
        elif arg.startswith("--both"):
            mode = "both"
            try:
                count = int(sys.argv[sys.argv.index(arg) + 1])
            except:
                count = 1
        elif arg.isdigit():
            continue  # Already handled
        elif arg.startswith("--episode"):
            start_ep = int(arg.split("=")[1])
    
    print(f"\n{'='*70}")
    print(f"  DUAL FORMAT GENERATOR")
    print(f"{'='*70}")
    print(f"\nMode: {mode.upper()}")
    print(f"Count: {count}")
    print(f"Starting Episode: {start_ep}\n")
    
    if mode == "short":
        for i in range(count):
            generate_short_video(start_ep + i)
    elif mode == "long":
        for i in range(count):
            generate_long_video(start_ep + i)
    elif mode == "both":
        for i in range(count):
            generate_short_video(start_ep + i * 2)
            generate_long_video(start_ep + i * 2 + 1)
    
    print(f"\n{'='*70}")
    print(f"  GENERATION COMPLETE")
    print(f"{'='*70}\n")

