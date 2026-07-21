#!/usr/bin/env python3
"""
Batch TikTok Optimization Script
Optimizes videos from abraham_horror/videos/ for TikTok
Handles both Windows (F:\AI_Oracle_Root\scarify) and Linux (/workspace) paths
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from TIKTOK_AUTOMATION_SYSTEM import TikTokVideoOptimizer


def find_video_directory():
    """Find video directory - handles both Windows and Linux paths"""
    current = Path(__file__).parent
    
    # Try Windows path first (if running on Windows or path exists)
    windows_paths = [
        Path("F:/AI_Oracle_Root/scarify/abraham_horror/videos"),
        Path("F:\\AI_Oracle_Root\\scarify\\abraham_horror\\videos"),
    ]
    
    # Try Linux/workspace paths
    linux_paths = [
        current / "abraham_horror" / "videos",
        current / "abraham_horror" / "generated_videos",
        current / "videos",
    ]
    
    # Check all possible paths
    all_paths = windows_paths + linux_paths
    
    for path in all_paths:
        if path.exists():
            return path
    
    # If none exist, return the most likely one
    return current / "abraham_horror" / "videos"


def main():
    """Batch optimize videos for TikTok"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Batch optimize videos for TikTok')
    parser.add_argument('--dir', help='Video directory (auto-detected if not specified)')
    parser.add_argument('--limit', type=int, default=3, help='Limit number of videos (default: 3)')
    parser.add_argument('--pattern', default='*.mp4', help='File pattern (default: *.mp4)')
    
    args = parser.parse_args()
    
    # Find video directory
    if args.dir:
        video_dir = Path(args.dir)
    else:
        video_dir = find_video_directory()
    
    print("\n" + "="*80)
    print("BATCH TIKTOK OPTIMIZATION")
    print("="*80)
    print(f"Video directory: {video_dir}")
    
    if not video_dir.exists():
        print(f"\n❌ Directory not found: {video_dir}")
        print("\nTrying to create directory...")
        video_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {video_dir}")
        print("\nPlease place videos in this directory and run again.")
        return
    
    # Find videos
    videos = list(video_dir.glob(args.pattern))
    
    if not videos:
        print(f"\n⚠️  No videos found matching pattern: {args.pattern}")
        print(f"   Searched in: {video_dir}")
        print("\nTo generate test videos:")
        print("  python ABE_MASTER_GENERATOR.py --topic 'Test Video'")
        return
    
    # Limit videos
    videos = videos[:args.limit]
    
    print(f"\nFound {len(videos)} video(s) to optimize:")
    for i, video in enumerate(videos, 1):
        print(f"  {i}. {video.name}")
    
    # Initialize optimizer
    base_path = Path(__file__).parent
    optimizer = TikTokVideoOptimizer(base_path)
    
    # Optimize each video
    print(f"\n{'='*80}")
    print("OPTIMIZING VIDEOS")
    print('='*80)
    
    successful = []
    failed = []
    
    for i, video in enumerate(videos, 1):
        print(f"\n[{i}/{len(videos)}] Processing: {video.name}")
        print("-" * 80)
        
        result = optimizer.optimize_for_tiktok(str(video))
        
        if result:
            output_path = Path(result)
            if output_path.exists():
                file_size = output_path.stat().st_size / (1024 * 1024)  # MB
                print(f"✅ Success!")
                print(f"   Output: {output_path.name}")
                print(f"   Size: {file_size:.1f} MB")
                print(f"   Location: {output_path.parent}")
                successful.append(output_path)
            else:
                print(f"⚠️  Optimization completed but file not found")
                failed.append(video)
        else:
            print(f"❌ Optimization failed")
            failed.append(video)
    
    # Summary
    print(f"\n{'='*80}")
    print("BATCH OPTIMIZATION COMPLETE")
    print('='*80)
    print(f"✅ Successful: {len(successful)}/{len(videos)}")
    
    if successful:
        print(f"\nOptimized videos saved to:")
        if successful:
            print(f"  {successful[0].parent}")
    
    if failed:
        print(f"\n❌ Failed: {len(failed)}")
        for video in failed:
            print(f"   - {video.name}")
    
    print(f"\n{'='*80}")
    print("NEXT STEPS:")
    print('='*80)
    print("1. Review optimized videos in: tiktok_content/ready_to_upload/")
    print("2. Upload to TikTok:")
    print("   python TIKTOK_AUTOMATION_SYSTEM.py --upload tiktok_content/ready_to_upload/video.mp4 --topic 'Business Horror'")
    print("3. Or use full pipeline:")
    print("   python TIKTOK_AUTOMATION_SYSTEM.py --full video.mp4 --topic 'Corporate Nightmare'")


if __name__ == '__main__':
    main()
