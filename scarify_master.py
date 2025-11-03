#!/usr/bin/env python3
"""
SCARIFY Master Script
Complete YouTube Shorts video generation system with auto-upload
"""

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

# Import our generators
from audio_generator import AudioGenerator
from video_generator import VideoGenerator

# Import YouTube uploader (optional - graceful degradation)
try:
    from youtube_uploader import YouTubeUploader
    YOUTUBE_AVAILABLE = True
except Exception as e:
    print(f"[WARNING] YouTube uploader not available: {e}")
    YOUTUBE_AVAILABLE = False


class ScarifyMaster:
    """Main orchestrator for video generation"""
    
    # Chapman Fear-Based Pain Points (Psychology-Optimized)
    PAIN_POINTS = [
        {
            "text": "Your garage bleeds $50k every day you wait. The crisis hits TOMORROW. Ex-vet emergency kit stops the bleeding.",
            "keywords": "emergency crisis urgent danger bleeding money",
            "hook": "BLEEDING $50K\nEVERY DAY?",
            "cta": "Stop the Bleeding\n$97 Kit →",
            "fear_level": "high",
            "urgency": "immediate",
            "psychology": "loss_aversion"
        },
        {
            "text": "While you sleep, competitors steal your customers. Wake up to empty parking lots. Veteran tactics fight back.",
            "keywords": "competition loss customers empty parking",
            "hook": "CUSTOMERS STOLEN\nWHILE YOU SLEEP?",
            "cta": "Fight Back\nEmergency Kit →",
            "fear_level": "medium",
            "urgency": "tonight",
            "psychology": "fomo"
        },
        {
            "text": "One bad review kills 10 customers. Your reputation dies in 24 hours. Ex-vet crisis protocols save you.",
            "keywords": "reputation crisis reviews damage reputation",
            "hook": "ONE REVIEW\nKILLS BUSINESS?",
            "cta": "Protect Reputation\n$97 Kit →",
            "fear_level": "high",
            "urgency": "today",
            "psychology": "social_proof"
        },
        {
            "text": "Cash flow stops flowing. Bills pile up. Bankruptcy court calls. Veteran emergency systems restore flow.",
            "keywords": "cash flow bankruptcy bills crisis",
            "hook": "CASH FLOW\nSTOPPED FLOWING?",
            "cta": "Restore Flow\nEmergency Kit →",
            "fear_level": "extreme",
            "urgency": "now",
            "psychology": "survival"
        },
        {
            "text": "Your family depends on this business. One mistake destroys everything. Ex-vet protocols protect your family.",
            "keywords": "family business mistake destroy protection",
            "hook": "FAMILY DEPENDS\nON THIS?",
            "cta": "Protect Family\n$97 Kit →",
            "fear_level": "extreme",
            "urgency": "immediate",
            "psychology": "family_protection"
        }
    ]
    
    def __init__(self, enable_upload: bool = False):
        self.audio_gen = AudioGenerator()
        self.video_gen = VideoGenerator()
        
        # YouTube uploader (optional)
        self.youtube_uploader = None
        self.enable_upload = enable_upload and YOUTUBE_AVAILABLE
        
        if enable_upload and not YOUTUBE_AVAILABLE:
            print("[WARNING] Upload requested but YouTube uploader not available")
        
        # Create output directories
        self.output_dir = Path("output")
        self.audio_dir = self.output_dir / "audio"
        self.video_dir = self.output_dir / "videos"
        
        for directory in [self.output_dir, self.audio_dir, self.video_dir]:
            directory.mkdir(exist_ok=True, parents=True)
    
    def generate_video(
        self,
        pain_index: int = 0,
        test_mode: bool = False
    ) -> dict:
        """
        Generate a single video
        
        Args:
            pain_index: Which pain point to use (0-4)
            test_mode: If True, skip upload
            
        Returns:
            Dict with success status and optional YouTube URL
        """
        result = {
            "success": False,
            "video_path": None,
            "youtube_url": None
        }
        
        # Get pain point
        pain = self.PAIN_POINTS[pain_index % len(self.PAIN_POINTS)]
        
        print("\n" + "="*80)
        print(f"[VIDEO] GENERATING VIDEO #{pain_index + 1}")
        print("="*80)
        print(f"Script: {pain['text']}")
        print(f"Keywords: {pain['keywords']}")
        print("="*80)
        
        # Generate timestamp for unique filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Paths
        audio_path = self.audio_dir / f"scarify_{timestamp}.wav"
        video_path = self.video_dir / f"scarify_{timestamp}.mp4"
        
        # Step 1: Generate audio
        print("\n[STEP 1/3] Audio Generation" if self.enable_upload else "\n[STEP 1/2] Audio Generation")
        if not self.audio_gen.generate(pain['text'], str(audio_path)):
            print("[ERROR] Audio generation failed")
            return result
        
        # Step 2: Generate video with professional text overlays
        print("\n[STEP 2/3] Video Generation (Professional)" if self.enable_upload else "\n[STEP 2/2] Video Generation (Professional)")
        if not self.video_gen.generate(
            pain['keywords'],
            str(audio_path),
            str(video_path),
            target_duration=50,
            hook_text=pain.get('hook'),  # Hook text at top (0-3s)
            cta_text=pain.get('cta')     # CTA text at bottom (last 5s)
        ):
            print("[ERROR] Video generation failed")
            return result
        
        # Success!
        result["success"] = True
        result["video_path"] = str(video_path)
        
        print("\n" + "="*80)
        print("[SUCCESS] VIDEO COMPLETE")
        print("="*80)
        print(f"[FILE] Video: {video_path}")
        print(f"[FILE] Audio: {audio_path}")
        
        # File info
        if os.path.exists(video_path):
            size_mb = os.path.getsize(video_path) / 1024 / 1024
            print(f"[SIZE] Size: {size_mb:.1f} MB")
        
        # Step 3: Upload to YouTube (if enabled)
        if self.enable_upload and not test_mode:
            print("\n[STEP 3/3] YouTube Upload")
            
            try:
                # Initialize uploader on first use
                if not self.youtube_uploader:
                    self.youtube_uploader = YouTubeUploader()
                
                # Upload video
                youtube_url = self.youtube_uploader.upload(
                    str(video_path),
                    pain['text']
                )
                
                if youtube_url:
                    result["youtube_url"] = youtube_url
                    print(f"[YOUTUBE] YouTube: {youtube_url}")
                else:
                    print("[WARNING] Upload failed, but video saved locally")
                    
            except Exception as e:
                print(f"[WARNING] Upload error (video saved locally): {e}")
        
        print("="*80)
        
        return result
    
    def batch_generate(
        self,
        count: int = 5,
        test_mode: bool = False
    ) -> dict:
        """
        Generate multiple videos
        
        Args:
            count: Number of videos to generate
            test_mode: If True, skip upload
            
        Returns:
            Dict with success/failure counts
        """
        print("\n" + "="*80)
        print(f"[SCARIFY] SCARIFY BATCH GENERATION: {count} VIDEOS")
        if self.enable_upload and not test_mode:
            print("[UPLOAD] Auto-upload to YouTube: ENABLED")
        print("="*80)
        
        results = {
            "generated": 0,
            "uploaded": 0,
            "failed": 0,
            "videos": [],
            "youtube_urls": []
        }
        
        for i in range(count):
            try:
                video_result = self.generate_video(i, test_mode)
                
                if video_result["success"]:
                    results["generated"] += 1
                    results["videos"].append(video_result["video_path"])
                    
                    if video_result["youtube_url"]:
                        results["uploaded"] += 1
                        results["youtube_urls"].append(video_result["youtube_url"])
                else:
                    results["failed"] += 1
                    
            except Exception as e:
                print(f"\n[ERROR] Video {i+1} exception: {e}")
                results["failed"] += 1
            
            # Don't spam APIs - wait between videos
            if i < count - 1:
                print(f"\n[WAIT] Waiting 10 seconds before next video...")
                import time
                time.sleep(10)
        
        # Final summary
        print("\n" + "="*80)
        print("[SUMMARY] BATCH GENERATION COMPLETE")
        print("="*80)
        print(f"[SUCCESS] Generated: {results['generated']}/{count}")
        
        if self.enable_upload and not test_mode:
            print(f"[UPLOAD] Uploaded: {results['uploaded']}/{results['generated']}")
            if results["youtube_urls"]:
                print(f"\n[YOUTUBE] YouTube URLs:")
                for url in results["youtube_urls"]:
                    print(f"   • {url}")
        
        if results["failed"] > 0:
            print(f"[ERROR] Failed: {results['failed']}")
        
        print(f"[OUTPUT] Output: {self.video_dir}")
        print("="*80)
        
        return results


def main():
    """CLI interface"""
    parser = argparse.ArgumentParser(
        description='SCARIFY - YouTube Shorts Video Generator with Auto-Upload',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate 1 test video (no upload):
  python scarify_master.py --count 1 --test
  
  # Generate 5 videos:
  python scarify_master.py --count 5
  
  # Generate 5 videos and upload to YouTube:
  python scarify_master.py --count 5 --upload
  
  # Generate 20 videos and upload:
  python scarify_master.py --count 20 --upload
"""
    )
    
    parser.add_argument(
        '--count',
        type=int,
        default=1,
        help='Number of videos to generate (default: 1)'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test mode (skip YouTube upload)'
    )
    
    parser.add_argument(
        '--upload',
        action='store_true',
        help='Upload videos to YouTube as Shorts'
    )
    
    args = parser.parse_args()
    
    # Validate count
    if args.count < 1:
        print("[ERROR] Count must be at least 1")
        sys.exit(1)
    
    if args.count > 50:
        print("[WARNING] Warning: Generating >50 videos may hit YouTube quota limits")
        print("   (YouTube allows ~50 uploads per day)")
        response = input("Continue? (y/n): ")
        if response.lower() != 'y':
            sys.exit(0)
    
    # Run generation
    try:
        master = ScarifyMaster(enable_upload=args.upload)
        
        if args.count == 1:
            # Single video
            result = master.generate_video(0, args.test)
            sys.exit(0 if result["success"] else 1)
        else:
            # Batch
            results = master.batch_generate(args.count, args.test)
            sys.exit(0 if results['generated'] > 0 else 1)
            
    except KeyboardInterrupt:
        print("\n\n[WARNING] Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
