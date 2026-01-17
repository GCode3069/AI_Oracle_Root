#!/usr/bin/env python3
"""
FINAL VIDEO UPLOAD - Creates comedy video and prepares for upload
Generates video with new comedy system ready for YouTube
"""

import json
import random
import subprocess
from pathlib import Path
from datetime import datetime

# Import new comedy system
from COMEDY_SCRIPTS_REWRITTEN import ModernComedyGenerator

def create_final_comedy_video():
    """Create the final comedy video for upload"""
    
    print("\n" + "="*70)
    print("🎬 CREATING FINAL COMEDY VIDEO FOR UPLOAD")
    print("="*70)
    
    # Hot topics for Saturday, Jan 17, 2026
    current_topics = [
        "Breaking: Weekend Exists, People Still Stressed",
        "Study Shows Water Is Wet, Scientists Baffled",
        "Politicians Promise Things, Nobody Believes Them",
        "Tech Company Does Tech Thing, Stock Goes Up",
        "Weather Continues to Be Weather Despite Complaints"
    ]
    
    headline = random.choice(current_topics)
    comedy_gen = ModernComedyGenerator()
    
    # Use variety of styles
    styles = ['observational', 'dry_wit', 'absurdist', 'deadpan', 'relatable']
    style = random.choice(styles)
    
    # Generate script
    script, used_style = comedy_gen.generate(headline, style, word_limit=90)
    
    # Episode number
    episode = random.randint(30000, 39999)
    
    # Create title
    title = f"Lincoln Reacts #{episode}: {headline[:35]}... #Shorts"
    
    print(f"\n📰 Topic: {headline}")
    print(f"🎭 Comedy Style: {used_style}")
    print(f"📝 Episode: #{episode}")
    print(f"\n📜 Script ({len(script.split())} words):")
    print("-" * 50)
    print(script)
    print("-" * 50)
    
    # Create output directory
    output_dir = Path.cwd() / "videos" / "youtube_ready"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate video filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    video_file = output_dir / f"LINCOLN_COMEDY_{episode}_{timestamp}.mp4"
    
    # Create video with FFmpeg (black screen with text)
    print("\n🎥 Creating video...")
    
    # Calculate duration based on words (2.5 words per second + 2 seconds buffer)
    duration = int(len(script.split()) / 2.5) + 2
    
    # Create video with text overlay
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', f'color=c=black:s=1080x1920:d={duration}',
        '-vf', 
        f"drawtext=text='LINCOLN COMEDY #{episode}':fontcolor=white:fontsize=72:x=(w-text_w)/2:y=100:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf," +
        f"drawtext=text='{used_style.upper().replace('_', ' ')}':fontcolor=yellow:fontsize=48:x=(w-text_w)/2:y=250:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf," +
        f"drawtext=text='New Comedy System':fontcolor=cyan:fontsize=36:x=(w-text_w)/2:y=1700:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-preset', 'ultrafast',
        str(video_file)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0 or not video_file.exists():
        print(f"❌ Video creation failed")
        if result.stderr:
            print(result.stderr[:500])
        return None
    
    size_mb = video_file.stat().st_size / (1024 * 1024)
    print(f"✅ Video created: {size_mb:.2f} MB")
    
    # Create metadata file for YouTube
    metadata = {
        'file': str(video_file),
        'title': title,
        'episode': episode,
        'style': used_style,
        'headline': headline,
        'script': script,
        'description': f"""{script}

🎭 ABRAHAM LINCOLN COMEDY - Episode #{episode}
Comedy Style: {used_style.replace('_', ' ').title()}
Topic: {headline}

This video uses our NEW COMEDY SYSTEM with actually funny scripts!
No more tired roast formulas - just genuine humor in multiple styles.

Bitcoin: bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt

#comedy #shorts #lincolnreacts #funny #{used_style.replace('_', '')} #abrahamlincoln #satire #humor #comedyshorts #viral""",
        'tags': [
            'comedy', 'shorts', 'lincolnreacts', 'funny', 
            used_style.replace('_', ''), 'abrahamlincoln',
            'satire', 'humor', 'comedyshorts', 'viral',
            'trending', 'youtube', 'youtubeshorts', 'funnymemes'
        ],
        'category': 'Comedy',
        'timestamp': timestamp,
        'duration_seconds': duration
    }
    
    # Save metadata
    metadata_file = output_dir / f"metadata_{episode}_{timestamp}.json"
    metadata_file.write_text(json.dumps(metadata, indent=2))
    
    print(f"\n📁 Video saved: {video_file}")
    print(f"📋 Metadata saved: {metadata_file}")
    
    # Create upload instructions
    print("\n" + "="*70)
    print("📤 READY FOR YOUTUBE UPLOAD")
    print("="*70)
    
    print("\n📺 VIDEO DETAILS FOR UPLOAD:")
    print(f"File: {video_file.name}")
    print(f"Title: {title}")
    print(f"Duration: {duration} seconds")
    print(f"Size: {size_mb:.2f} MB")
    
    print("\n📝 COPY THIS FOR YOUTUBE:")
    print("-" * 50)
    print(f"TITLE:\n{title}\n")
    print(f"DESCRIPTION:\n{metadata['description']}\n")
    print(f"TAGS:\n{', '.join(metadata['tags'])}")
    print("-" * 50)
    
    print("\n🚀 TO UPLOAD:")
    print("1. Go to YouTube Studio: https://studio.youtube.com")
    print("2. Click 'CREATE' → 'Upload videos'")
    print(f"3. Select file: {video_file}")
    print("4. Copy/paste the title, description, and tags above")
    print("5. Set to 'Shorts' shelf")
    print("6. Publish!")
    
    return video_file


if __name__ == "__main__":
    print("""
    🎬 FINAL VIDEO CREATOR FOR YOUTUBE
    ===================================
    
    Creates a comedy video with:
    ✅ New actually funny comedy system
    ✅ Multiple comedy styles for variety
    ✅ Optimized for YouTube Shorts
    ✅ Complete metadata for upload
    """)
    
    video = create_final_comedy_video()
    
    if video:
        print("\n" + "="*70)
        print("✅ VIDEO READY FOR UPLOAD!")
        print("="*70)
        print(f"📁 Location: {video}")
        print("\n💡 TIP: Upload during peak hours (2-4 PM or 8-10 PM EST) for best reach!")
    else:
        print("\n❌ Video creation failed. Check errors above.")