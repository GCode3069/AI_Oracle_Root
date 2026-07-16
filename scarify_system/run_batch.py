#!/usr/bin/env python3
"""
run_batch.py
Quick batch runner for SCARIFY video generation.

Usage:
    python run_batch.py              # Generate 10 videos (default)
    python run_batch.py 25           # Generate 25 videos
    python run_batch.py 100 --fast   # Generate 100 videos with simple effects
"""

import sys
import argparse
from pathlib import Path

# Import SCARIFY pipeline
from SCARIFY_COMPLETE import ScarifyPipeline


def main():
    parser = argparse.ArgumentParser(
        description="SCARIFY Batch Video Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_batch.py              # Generate 10 videos
  python run_batch.py 25           # Generate 25 videos
  python run_batch.py 100 --fast   # Fast mode (skip heavy effects)
  python run_batch.py 50 --mock    # Test mode (no API calls)

Output:
  WARNING videos: D:/AI_Oracle_Projects/Output/Generated/Winners/
  COMEDY videos:  D:/AI_Oracle_Projects/Output/Generated/Comedy/
        """
    )
    
    parser.add_argument(
        'count',
        type=int,
        nargs='?',
        default=10,
        help='Number of videos to generate (default: 10)'
    )
    
    parser.add_argument(
        '--fast',
        action='store_true',
        help='Skip heavy VHS effects for faster processing'
    )
    
    parser.add_argument(
        '--mock',
        action='store_true',
        help='Use mock mode (no API calls, for testing)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='D:/AI_Oracle_Projects/Output/Generated',
        help='Output directory (default: D:/AI_Oracle_Projects/Output/Generated)'
    )
    
    parser.add_argument(
        '--cache',
        type=str,
        default='D:/AI_Oracle_Projects/Assets/Kling_Cache',
        help='Cache directory (default: D:/AI_Oracle_Projects/Assets/Kling_Cache)'
    )
    
    parser.add_argument(
        '--portraits',
        type=str,
        default='D:/AI_Oracle_Projects/Assets/Portraits',
        help='Portraits directory (default: D:/AI_Oracle_Projects/Assets/Portraits)'
    )
    
    args = parser.parse_args()
    
    # Print header
    print("=" * 60)
    print("SCARIFY BATCH VIDEO GENERATOR")
    print("=" * 60)
    print(f"Count: {args.count} videos")
    print(f"Mode: {'MOCK' if args.mock else 'PRODUCTION'}")
    print(f"Effects: {'SIMPLE (fast)' if args.fast else 'FULL (VHS)'}")
    print(f"Output: {args.output}")
    print("=" * 60)
    
    # Confirm if large batch
    if args.count > 50 and not args.mock:
        response = input(f"\n⚠️  You're about to generate {args.count} videos in PRODUCTION mode.\n"
                        f"Estimated cost: ${args.count * 0.02:.2f} - ${args.count * 0.04:.2f}\n"
                        f"Continue? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("Cancelled.")
            return
    
    # Initialize pipeline
    print("\n[INIT] Initializing SCARIFY pipeline...")
    try:
        pipeline = ScarifyPipeline(
            output_base_dir=args.output,
            cache_dir=args.cache,
            portraits_dir=args.portraits,
            use_mock_mode=args.mock
        )
        print(f"[INIT] ✅ Pipeline ready")
        print(f"  Portraits available: {len(pipeline._portraits)}")
    except Exception as e:
        print(f"[INIT] ❌ Failed to initialize pipeline: {e}")
        return
    
    # Generate batch
    print(f"\n[BATCH] Starting generation of {args.count} videos...")
    print("-" * 60)
    
    try:
        videos = pipeline.generate_batch(
            count=args.count,
            skip_effects=args.fast
        )
        
        print("\n" + "=" * 60)
        print("✅ BATCH GENERATION COMPLETE")
        print("=" * 60)
        print(f"Successfully generated: {len(videos)}/{args.count} videos")
        
        if len(videos) < args.count:
            print(f"⚠️  {args.count - len(videos)} videos failed")
        
        # Show sample output paths
        if videos:
            print("\nSample outputs:")
            for i, video in enumerate(videos[:3]):
                print(f"  {i+1}. {video['path']}")
            if len(videos) > 3:
                print(f"  ... and {len(videos) - 3} more")
        
        # Final stats
        print("\n" + "=" * 60)
        pipeline.print_stats()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Generation interrupted by user")
        print("Partial results:")
        pipeline.print_stats()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Batch generation error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
