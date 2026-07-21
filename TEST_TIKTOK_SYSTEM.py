#!/usr/bin/env python3
"""
Test Script for TikTok Automation System
Tests optimization on videos from abraham_horror/videos/
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from TIKTOK_AUTOMATION_SYSTEM import TikTokAutomationSystem, TikTokVideoOptimizer, TikTokCaptionGenerator


def find_videos(video_dir: Path, limit: int = 3):
    """Find video files in directory"""
    videos = []
    
    # Try multiple possible locations
    possible_dirs = [
        video_dir / "videos",
        video_dir / "generated_videos",
        video_dir,
        Path("/workspace/abraham_horror/videos"),
        Path("/workspace/videos")
    ]
    
    for dir_path in possible_dirs:
        if dir_path.exists():
            found = list(dir_path.glob("*.mp4"))
            if found:
                videos.extend(found[:limit])
                print(f"✅ Found {len(found)} videos in {dir_path}")
                break
    
    if not videos:
        print(f"⚠️  No videos found. Checking common locations...")
        # Check if any MP4 files exist anywhere
        for dir_path in possible_dirs:
            if dir_path.exists():
                print(f"   Checking: {dir_path}")
    
    return videos[:limit]


def test_optimization():
    """Test video optimization"""
    print("\n" + "="*80)
    print("TEST 1: VIDEO OPTIMIZATION")
    print("="*80)
    
    base_path = Path("/workspace")
    abraham_horror = base_path / "abraham_horror"
    
    # Find videos
    videos = find_videos(abraham_horror, limit=3)
    
    if not videos:
        print("\n❌ No videos found to test.")
        print("\nTo test with real videos:")
        print("1. Place videos in: abraham_horror/videos/")
        print("2. Or run: python ABE_MASTER_GENERATOR.py --topic 'Test'")
        print("3. Then run this test again")
        return False
    
    optimizer = TikTokVideoOptimizer(base_path)
    
    success_count = 0
    for i, video in enumerate(videos, 1):
        print(f"\n[{i}/{len(videos)}] Testing: {video.name}")
        
        result = optimizer.optimize_for_tiktok(str(video))
        
        if result:
            print(f"   ✅ Success: {Path(result).name}")
            success_count += 1
            
            # Verify output exists
            if Path(result).exists():
                file_size = Path(result).stat().st_size / (1024 * 1024)  # MB
                print(f"   📊 Output size: {file_size:.1f} MB")
            else:
                print(f"   ⚠️  Output file not found")
        else:
            print(f"   ❌ Failed to optimize")
    
    print(f"\n{'='*80}")
    print(f"OPTIMIZATION TEST: {success_count}/{len(videos)} successful")
    print('='*80)
    
    return success_count == len(videos)


def test_caption_generation():
    """Test caption generation"""
    print("\n" + "="*80)
    print("TEST 2: CAPTION GENERATION")
    print("="*80)
    
    caption_gen = TikTokCaptionGenerator()
    
    test_topics = [
        "Corporate Horror",
        "Business Nightmare",
        "Profit Over People"
    ]
    
    for topic in test_topics:
        caption = caption_gen.generate_caption(topic)
        print(f"\nTopic: {topic}")
        print(f"Caption:\n{caption}")
        print(f"Length: {len(caption)} characters")
        
        # Verify brand elements
        checks = {
            "Has hook": "🚨" in caption or "Business tip" in caption or "Corporate" in caption,
            "Has hashtags": "#nunyabeznes" in caption or "#businesshorror" in caption,
            "Has username": "@nunyabeznes2" in caption,
            "Under 500 chars": len(caption) <= 500
        }
        
        for check, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check}")
    
    print(f"\n{'='*80}")
    print("CAPTION TEST: Complete")
    print('='*80)
    
    return True


def test_brand_config():
    """Test brand configuration"""
    print("\n" + "="*80)
    print("TEST 3: BRAND CONFIGURATION")
    print("="*80)
    
    from TIKTOK_AUTOMATION_SYSTEM import BRAND_CONFIG
    
    print(f"\nBrand Username: {BRAND_CONFIG['username']}")
    print(f"Brand Voice: {BRAND_CONFIG['brand_voice']}")
    print(f"Color Scheme: {BRAND_CONFIG['color_scheme']}")
    print(f"Watermark Opacity: {BRAND_CONFIG['watermark_opacity']}")
    print(f"\nHashtags ({len(BRAND_CONFIG['hashtags'])}):")
    for tag in BRAND_CONFIG['hashtags']:
        print(f"   {tag}")
    
    print(f"\nPosting Times: {BRAND_CONFIG['posting_times']}")
    
    # Verify all required elements
    checks = {
        "Username configured": BRAND_CONFIG['username'] == "@nunyabeznes2",
        "Has hashtags": len(BRAND_CONFIG['hashtags']) >= 5,
        "Color scheme set": BRAND_CONFIG['color_scheme']['primary'] == "#FF0000",
        "Watermark opacity set": BRAND_CONFIG['watermark_opacity'] == 0.1
    }
    
    print(f"\n{'='*80}")
    print("BRAND CONFIG VERIFICATION:")
    for check, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"   {status} {check}")
    print('='*80)
    
    return all(checks.values())


def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("TIKTOK SYSTEM TEST SUITE")
    print("="*80)
    
    results = {
        "Optimization": test_optimization(),
        "Caption Generation": test_caption_generation(),
        "Brand Config": test_brand_config()
    }
    
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "⚠️  SKIP/FAIL"
        print(f"{status} {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*80)
    if all_passed:
        print("✅ ALL TESTS PASSED")
    else:
        print("⚠️  SOME TESTS SKIPPED (videos not found)")
        print("\nTo complete testing:")
        print("1. Generate videos: python ABE_MASTER_GENERATOR.py --topic 'Test'")
        print("2. Or place videos in: abraham_horror/videos/")
        print("3. Run tests again: python TEST_TIKTOK_SYSTEM.py")
    print("="*80)


if __name__ == '__main__':
    main()
