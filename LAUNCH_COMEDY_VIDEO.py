#!/usr/bin/env python3
"""
LAUNCH COMEDY VIDEO - Creates and prepares video for immediate upload
Generates a high-quality comedy video with the new system
"""

import json
import random
import subprocess
from pathlib import Path
from datetime import datetime

# Import new comedy system
from COMEDY_SCRIPTS_REWRITTEN import ModernComedyGenerator, ComedyScriptPackage

def launch_comedy_video():
    """Create and launch a comedy video"""
    
    print("\n" + "="*70)
    print("🚀 LAUNCHING COMEDY VIDEO")
    print("="*70)
    
    # Breaking news style headlines for maximum engagement
    hot_headlines = [
        "BREAKING: Millennials Discover They're Actually Old Now",
        "Scientists Confirm: Monday Still Worst Day of Week",
        "Study: Your Phone Knows You Better Than You Do",
        "Breaking: Coffee Prices Rise, Productivity Falls", 
        "Alert: Everyone Pretending to Understand Cryptocurrency",
        "Update: Social Media Still Making Everyone Miserable",
        "News: AI Promises Not to Take Over (Wink Wink)",
        "Report: Nobody Actually Reads Terms and Conditions"
    ]
    
    headline = random.choice(hot_headlines)
    comedy_gen = ModernComedyGenerator()
    
    # Rotate through styles for variety
    styles_by_engagement = [
        'relatable',      # Highest engagement with younger audiences
        'observational',  # Classic, always works
        'absurdist',      # Great for virality
        'dry_wit',        # Good for shares
        'surreal'         # Memorable, unique
    ]
    
    style = random.choice(styles_by_engagement)
    
    # Generate script
    script, used_style = comedy_gen.generate(headline, style, word_limit=80)
    
    # Episode number
    episode = random.randint(40000, 49999)
    
    # Create viral-optimized title
    viral_titles = [
        f"Lincoln Reacts to {headline[:30]}... 😂 #{episode}",
        f"Abraham Lincoln: {headline[:35]} (MUST WATCH) #{episode}",
        f"Dead President Reacts: {headline[:30]} #{episode} #Shorts",
        f"Lincoln's HOT TAKE on {headline[:28]} 🔥 #{episode}",
        f"You Won't Believe Lincoln's Take on {headline[:25]} #{episode}"
    ]
    
    title = random.choice(viral_titles)
    
    print(f"\n📰 Headline: {headline}")
    print(f"🎭 Comedy Style: {used_style.replace('_', ' ').title()}")
    print(f"📝 Episode: #{episode}")
    print(f"🔥 Title: {title}")
    
    print(f"\n📜 Script ({len(script.split())} words):")
    print("-" * 50)
    print(script)
    print("-" * 50)
    
    # Create output directory
    output_dir = Path.cwd() / "videos" / "youtube_ready"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate video filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    video_file = output_dir / f"LAUNCH_COMEDY_{episode}_{timestamp}.mp4"
    
    # Calculate duration
    duration = max(15, int(len(script.split()) / 2.3))  # Slightly slower pace for clarity
    
    print(f"\n🎥 Creating {duration}-second video...")
    
    # Create more dynamic video with gradient background
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', f'color=c=0x0a0a0a:s=1080x1920:d={duration}',
        '-f', 'lavfi', '-i', f'color=c=0x1a1a2e:s=1080x1920:d={duration}',
        '-filter_complex',
        f"[0][1]blend=all_expr='A*(1-X/W)+B*(X/W)'[bg];" +
        f"[bg]drawtext=text='🎩 LINCOLN REACTS 🎩':fontcolor=white:fontsize=64:x=(w-text_w)/2:y=150:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:" +
        f"enable='between(t,0,3)'[v1];" +
        f"[v1]drawtext=text='Episode \\#{episode}':fontcolor=gold:fontsize=48:x=(w-text_w)/2:y=280:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:" +
        f"enable='between(t,0,3)'[v2];" +
        f"[v2]drawtext=text='{used_style.upper().replace('_', ' ')} COMEDY':fontcolor=cyan:fontsize=40:x=(w-text_w)/2:y=900:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf[v3];" +
        f"[v3]drawtext=text='SUBSCRIBE FOR MORE':fontcolor=red:fontsize=36:x=(w-text_w)/2:y=1700:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:" +
        f"enable='between(t,{duration-3},{duration})'[out]",
        '-map', '[out]',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-preset', 'fast',
        '-crf', '23',
        str(video_file)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        # Fallback to simpler video if complex one fails
        print("⚠️ Complex video failed, creating simple version...")
        cmd = [
            'ffmpeg', '-y',
            '-f', 'lavfi', '-i', f'color=c=0x1a1a2e:s=1080x1920:d={duration}',
            '-vf',
            f"drawtext=text='LINCOLN COMEDY':fontcolor=white:fontsize=72:x=(w-text_w)/2:y=200:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf," +
            f"drawtext=text='Episode {episode}':fontcolor=yellow:fontsize=48:x=(w-text_w)/2:y=350:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-preset', 'ultrafast',
            str(video_file)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0 or not video_file.exists():
        print(f"❌ Video creation failed: {result.stderr[:200]}")
        return None
    
    size_mb = video_file.stat().st_size / (1024 * 1024)
    print(f"✅ Video created: {size_mb:.2f} MB")
    
    # Generate viral description
    description = f"""{script}

🎩 ABRAHAM LINCOLN REACTS - Episode #{episode}
🎭 Comedy Style: {used_style.replace('_', ' ').title()}

{headline}

This is what happens when you give a dead president access to modern news.
Using our NEW COMEDY SYSTEM - actually funny, not just angry!

👉 SUBSCRIBE for daily Lincoln reactions
🔔 Hit the bell for notifications
💬 Comment your favorite part

Bitcoin: bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt

#shorts #comedy #lincolnreacts #funny #viral #{used_style.replace('_', '')} #abrahamlincoln #reaction #trending #youtube #youtubeshorts #funnyshorts #comedyshorts #memes #relatable #satire"""
    
    # Optimized tags for algorithm
    tags = [
        'shorts', 'comedy', 'funny', 'lincolnreacts', 'viral',
        'trending', 'abrahamlincoln', 'reaction', 'reactionvideo',
        used_style.replace('_', ''), 'comedyshorts', 'funnyshorts',
        'youtubeshorts', 'memes', 'relatable', 'satire', 'humor',
        'lol', 'hilarious', 'mustwatch', 'fyp', 'foryou'
    ]
    
    # Save metadata
    metadata = {
        'file': str(video_file),
        'title': title,
        'episode': episode,
        'style': used_style,
        'headline': headline,
        'script': script,
        'description': description,
        'tags': tags[:30],  # YouTube limit
        'duration_seconds': duration,
        'size_mb': size_mb,
        'timestamp': timestamp,
        'upload_time': 'Best times: 2-4 PM EST or 8-10 PM EST',
        'category': 'Comedy (23)',
        'visibility': 'Public',
        'audience': 'Not made for kids'
    }
    
    metadata_file = output_dir / f"launch_metadata_{episode}_{timestamp}.json"
    metadata_file.write_text(json.dumps(metadata, indent=2))
    
    # Create upload script for convenience
    upload_script = output_dir / f"upload_{episode}.txt"
    upload_content = f"""YOUTUBE UPLOAD INSTRUCTIONS FOR VIDEO {episode}
{'='*60}

FILE TO UPLOAD:
{video_file}

TITLE (copy this):
{title}

DESCRIPTION (copy all):
{description}

TAGS (copy all, comma-separated):
{', '.join(tags[:30])}

SETTINGS:
- Visibility: Public
- Category: Comedy
- Not made for kids: Yes
- Add to Shorts shelf: Yes
- Language: English

THUMBNAIL:
- Use auto-generated or create one with Lincoln image

BEST UPLOAD TIMES:
- Weekday: 2-4 PM EST or 8-10 PM EST
- Weekend: 12-2 PM EST or 7-9 PM EST
"""
    
    upload_script.write_text(upload_content)
    
    print(f"\n📁 Video saved: {video_file}")
    print(f"📋 Metadata saved: {metadata_file}")
    print(f"📝 Upload guide: {upload_script}")
    
    # Display final instructions
    print("\n" + "="*70)
    print("🚀 VIDEO READY TO LAUNCH!")
    print("="*70)
    
    print(f"\n📺 VIDEO: {video_file.name}")
    print(f"⏱️ Duration: {duration} seconds")
    print(f"💾 Size: {size_mb:.2f} MB")
    print(f"🎭 Style: {used_style.replace('_', ' ').title()}")
    
    print("\n📋 QUICK COPY FOR YOUTUBE STUDIO:")
    print("-" * 60)
    print(f"TITLE:\n{title}\n")
    print(f"TOP TAGS:\n{', '.join(tags[:15])}")
    print("-" * 60)
    
    print("\n🎯 LAUNCH CHECKLIST:")
    print("[ ] 1. Open YouTube Studio: https://studio.youtube.com")
    print("[ ] 2. Click CREATE → Upload videos")
    print(f"[ ] 3. Select: {video_file.name}")
    print("[ ] 4. Paste title and description from above")
    print("[ ] 5. Add to Shorts shelf")
    print("[ ] 6. Set to Public")
    print("[ ] 7. LAUNCH! 🚀")
    
    print(f"\n💡 PRO TIP: Upload now for {datetime.now().strftime('%A')} evening engagement!")
    
    return video_file


if __name__ == "__main__":
    print("""
    🚀 COMEDY VIDEO LAUNCHER 
    ========================
    
    Features:
    ✨ Viral-optimized titles
    🎭 Rotating comedy styles
    📈 Algorithm-friendly tags
    ⚡ Ready for immediate upload
    """)
    
    video = launch_comedy_video()
    
    if video:
        print("\n" + "="*70)
        print("✅ VIDEO LAUNCH READY!")
        print("="*70)
        print(f"\n🎬 {video.name}")
        print("🚀 Upload NOW for maximum reach!")
    else:
        print("\n❌ Launch preparation failed. Check errors above.")