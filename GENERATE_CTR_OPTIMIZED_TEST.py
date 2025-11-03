#!/usr/bin/env python3
"""
CTR-OPTIMIZED TEST VIDEO - ALL FEATURES ENABLED
Generates 1 video with:
- Lip sync
- Jumpscare
- Max Headroom glitch
- TV screen effects
- YouTube-optimized encoding (prevents "Processing abandoned")
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from abraham_MAX_HEADROOM import (
    generate_script, generate_voice, generate_lincoln_face_pollo,
    create_max_headroom_video, upload_to_youtube, get_headlines, BASE_DIR
)

def generate_ctr_test():
    """Generate single CTR-optimized test video with ALL features"""
    
    episode = 120000
    
    print("\n" + "="*80)
    print("  CTR-OPTIMIZED TEST VIDEO - ALL FEATURES ENABLED")
    print("="*80 + "\n")
    
    # 1. Get headline
    headlines = get_headlines()
    headline = headlines[0] if headlines else "Government Shutdown Crisis"
    print(f"[1/6] Headline: {headline}")
    
    # 2. Generate ChatGPT-style script (best CTR)
    print(f"[2/6] Generating ChatGPT poetic script...")
    script = generate_script(headline, style='chatgpt_poetic', ctr_level='moderate')
    print(f"  Script: {script[:80]}...")
    print(f"  Words: {len(script.split())}")
    
    # 3. Generate voice
    print(f"[3/6] Generating voice with psychological audio...")
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    audio_path = BASE_DIR / "audio" / f"CTR_TEST_{episode}_{timestamp}.mp3"
    audio_path.parent.mkdir(parents=True, exist_ok=True)
    
    if not generate_voice(script, audio_path):
        print("  [!] Voice generation failed")
        return None
    print(f"  [OK] Voice: {audio_path.name}")
    
    # 4. Get Lincoln image
    print(f"[4/6] Getting Lincoln face...")
    lincoln_face = generate_lincoln_face_pollo()
    print(f"  [OK] Lincoln: {lincoln_face}")
    
    # 5. Create video with ALL FEATURES
    print(f"[5/6] Creating video with ALL FEATURES:")
    print(f"  ✅ Lip Sync: ENABLED")
    print(f"  ✅ Jumpscare: ENABLED")
    print(f"  ✅ Max Headroom Glitch: ENABLED")
    print(f"  ✅ VHS TV Screen: ENABLED")
    print(f"  ✅ Cash App QR: ENABLED")
    print(f"  ✅ Psychological Audio: ENABLED")
    print(f"  ✅ YouTube Encoding: OPTIMIZED (prevents processing errors)")
    
    video_output = BASE_DIR / "uploaded" / f"CTR_TEST_ALL_FEATURES_{episode}_{timestamp}.mp4"
    video_output.parent.mkdir(parents=True, exist_ok=True)
    
    video_path = create_max_headroom_video(
        lincoln_image=lincoln_face,
        audio_path=audio_path,
        output_path=video_output,
        headline=headline,
        use_lipsync=True,     # LIP SYNC ENABLED
        use_jumpscare=True    # JUMPSCARE ENABLED
    )
    
    if not video_path:
        print("  [!] Video creation failed")
        return None
    
    video_path = Path(video_path)
    size_mb = video_path.stat().st_size / (1024 * 1024)
    print(f"  [OK] Video: {video_path.name} ({size_mb:.1f}MB)")
    
    # 6. Upload to YouTube
    print(f"[6/6] Uploading to YouTube...")
    youtube_url = upload_to_youtube(video_path, headline, episode)
    
    print(f"\n" + "="*80)
    print(f"  ✅ TEST COMPLETE")
    print(f"="*80)
    print(f"\nVideo: {video_path}")
    print(f"Size: {size_mb:.1f}MB")
    print(f"Episode: #{episode}")
    print(f"Style: ChatGPT Poetic (12-18% CTR)")
    print(f"\nFeatures Enabled:")
    print(f"  ✅ Lip Sync")
    print(f"  ✅ Jumpscare")
    print(f"  ✅ Max Headroom Glitch")
    print(f"  ✅ VHS TV Screen")
    print(f"  ✅ Cash App QR")
    print(f"\nYouTube:")
    if youtube_url:
        print(f"  {youtube_url}")
    else:
        print(f"  Check: https://studio.youtube.com/channel/UCyC-xdkPR39mqhh7fW_DYJQ/videos")
    print(f"\n" + "="*80 + "\n")
    
    return video_path

if __name__ == "__main__":
    generate_ctr_test()


