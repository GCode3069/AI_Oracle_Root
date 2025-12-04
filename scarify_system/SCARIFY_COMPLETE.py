"""
SCARIFY_COMPLETE.py
Complete 9-step video generation pipeline for Abraham Lincoln AI videos.
"""

import os
import time
import json
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime

# Import our custom modules
from DUAL_STYLE_GENERATOR import generate_video_concept, get_style_distribution
from KLING_CLIENT import KlingClient, MockKlingClient
from KLING_CACHE import KlingCache
from SUBLIMINAL_AUDIO import SubliminalAudioMixer
from VIDEO_LAYOUT import VideoLayoutCreator

# Try to import API keys
try:
    import sys
    # Add Scripts directory to path if running from there
    scripts_dir = Path(__file__).parent
    if scripts_dir not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    
    from API_KEYS import KLING_API_KEY, ELEVENLABS_API_KEY
except ImportError:
    print("[WARNING] Could not import from API_KEYS.py")
    print("Using environment variables or mock mode")
    KLING_API_KEY = os.getenv("KLING_API_KEY", "mock_key")
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "mock_key")


class ScarifyPipeline:
    """
    Complete SCARIFY video generation pipeline.
    
    Pipeline steps:
    1. Generate concept (70/30 WARNING/comedy split)
    2. Generate script text
    3. Synthesize voice with ElevenLabs
    4. Add subliminal audio layers
    5. Get/reuse portrait (80% reuse rate)
    6. Check Kling cache, then generate lip-sync if needed
    7. Create picture-in-picture layout
    8. Apply VHS effects
    9. Save to appropriate output directory
    """
    
    def __init__(
        self,
        output_base_dir: str = "./scarify_output",
        cache_dir: str = "./kling_cache",
        portraits_dir: str = "./portraits",
        use_mock_mode: bool = False
    ):
        """
        Initialize SCARIFY pipeline.
        
        Args:
            output_base_dir: Base directory for output videos
            cache_dir: Directory for Kling cache
            portraits_dir: Directory containing portrait images
            use_mock_mode: Use mock clients for testing without API calls
        """
        self.output_base_dir = Path(output_base_dir)
        self.cache_dir = Path(cache_dir)
        self.portraits_dir = Path(portraits_dir)
        
        # Create directories
        self.output_base_dir.mkdir(parents=True, exist_ok=True)
        (self.output_base_dir / "Winners").mkdir(exist_ok=True)
        (self.output_base_dir / "Comedy").mkdir(exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.portraits_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.cache = KlingCache(cache_dir=str(self.cache_dir))
        self.audio_mixer = SubliminalAudioMixer()
        self.layout_creator = VideoLayoutCreator()
        
        # Initialize Kling client
        if use_mock_mode or KLING_API_KEY == "mock_key":
            print("[SCARIFY] Using MOCK mode (no API calls)")
            self.kling_client = MockKlingClient()
            self.use_mock_mode = True
        else:
            self.kling_client = KlingClient(KLING_API_KEY)
            self.use_mock_mode = False
        
        # Statistics
        self.stats = {
            "total_generated": 0,
            "warning_count": 0,
            "comedy_count": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "total_cost": 0.0,
            "total_time": 0.0
        }
        
        # Load portrait list
        self._portrait_index = 0
        self._portraits = self._get_portrait_list()
    
    def _get_portrait_list(self) -> List[str]:
        """Get list of available portrait images."""
        portraits = []
        for ext in ['*.jpg', '*.jpeg', '*.png']:
            portraits.extend(self.portraits_dir.glob(ext))
        
        if not portraits:
            print(f"[SCARIFY] Warning: No portraits found in {self.portraits_dir}")
            # Create a dummy portrait for testing
            dummy = self.portraits_dir / "lincoln_dummy.jpg"
            dummy.touch()
            portraits = [dummy]
        
        return [str(p) for p in portraits]
    
    def _get_portrait(self, reuse_probability: float = 0.80) -> str:
        """
        Get portrait image with reuse strategy.
        
        Args:
            reuse_probability: Probability of reusing previous portrait (default: 0.80)
            
        Returns:
            Path to portrait image
        """
        import random
        
        if random.random() > reuse_probability or self._portrait_index == 0:
            # Use new portrait
            self._portrait_index = (self._portrait_index + 1) % len(self._portraits)
        
        return self._portraits[self._portrait_index]
    
    def _synthesize_voice(self, script: str, output_path: str) -> bool:
        """
        Synthesize voice using ElevenLabs API.
        
        Args:
            script: Text to synthesize
            output_path: Output audio file path
            
        Returns:
            True if successful, False otherwise
        """
        if self.use_mock_mode:
            print("[SCARIFY] Mock voice synthesis...")
            # Create dummy audio file
            Path(output_path).touch()
            time.sleep(0.5)
            return True
        
        try:
            from elevenlabs import generate, save, Voice
            
            print("[SCARIFY] Synthesizing voice with ElevenLabs...")
            
            audio = generate(
                text=script,
                voice=Voice(voice_id="21m00Tcm4TlvDq8ikWAM"),  # Rachel voice
                model="eleven_monolingual_v1"
            )
            
            save(audio, output_path)
            return True
            
        except Exception as e:
            print(f"[SCARIFY] Voice synthesis error: {e}")
            return False
    
    def generate_complete_video(
        self,
        force_style: Optional[str] = None,
        skip_effects: bool = False
    ) -> Optional[Dict]:
        """
        Generate complete video through entire pipeline.
        
        Args:
            force_style: Force specific style ("WARNING" or "COMEDY")
            skip_effects: Skip heavy VHS effects for faster processing
            
        Returns:
            Dict with video info, or None if failed
        """
        start_time = time.time()
        
        print("\n" + "="*60)
        print("SCARIFY VIDEO GENERATION PIPELINE")
        print("="*60)
        
        # Step 1: Generate concept
        print("\n[STEP 1/9] Generating concept...")
        concept = generate_video_concept(force_style=force_style)
        print(f"  Style: {concept['style']}")
        print(f"  Title: {concept['title']}")
        print(f"  Category: {concept['category']}")
        
        # Step 2: Script is already in concept
        print("\n[STEP 2/9] Script ready")
        script = concept['script']
        print(f"  Length: {len(script)} chars")
        
        # Create temp directory for this video
        video_id = f"scarify_{int(time.time())}"
        temp_dir = Path("temp") / video_id
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Step 3: Synthesize voice
            print("\n[STEP 3/9] Synthesizing voice...")
            voice_path = temp_dir / "voice.mp3"
            if not self._synthesize_voice(script, str(voice_path)):
                print("[SCARIFY] ❌ Voice synthesis failed")
                return None
            
            # Get audio duration
            duration = concept['duration_target']  # Use target for now
            
            # Step 4: Add subliminal audio
            print("\n[STEP 4/9] Adding subliminal audio layers...")
            try:
                mixed_audio_path = self.audio_mixer.mix_subliminal_audio(
                    voice_path=str(voice_path),
                    duration=duration
                )
            except Exception as e:
                print(f"[SCARIFY] Warning: Subliminal mixing failed: {e}")
                print("[SCARIFY] Continuing with original voice...")
                mixed_audio_path = str(voice_path)
            
            # Step 5: Get portrait
            print("\n[STEP 5/9] Selecting portrait...")
            portrait_path = self._get_portrait()
            print(f"  Portrait: {Path(portrait_path).name}")
            
            # Step 6: Check cache, then generate lip-sync
            print("\n[STEP 6/9] Checking Kling cache...")
            cached_video = self.cache.check_cache(mixed_audio_path, portrait_path)
            
            if cached_video:
                print("[SCARIFY] ✅ Using cached video!")
                lipsync_video = cached_video
                self.stats["cache_hits"] += 1
            else:
                print("[SCARIFY] Cache miss - generating new lip-sync video...")
                self.stats["cache_misses"] += 1
                self.stats["total_cost"] += 0.04  # $0.04 per generation
                
                lipsync_video = self.kling_client.generate_talking_head(
                    audio_path=mixed_audio_path,
                    image_path=portrait_path,
                    output_dir=str(temp_dir)
                )
                
                if not lipsync_video:
                    print("[SCARIFY] ❌ Lip-sync generation failed")
                    return None
                
                # Save to cache
                self.cache.save_to_cache(
                    video_path=lipsync_video,
                    audio_path=mixed_audio_path,
                    image_path=portrait_path,
                    metadata={"concept": concept}
                )
            
            # Step 7: Create layout
            print("\n[STEP 7/9] Creating picture-in-picture layout...")
            if skip_effects:
                layout_video = self.layout_creator.create_simple_layout(
                    video_path=lipsync_video,
                    title=concept['title'],
                    style=concept['style'],
                    output_path=str(temp_dir / "layout.mp4")
                )
            else:
                layout_video = self.layout_creator.create_pip_layout(
                    video_path=lipsync_video,
                    title=concept['title'],
                    style=concept['style'],
                    output_path=str(temp_dir / "layout.mp4")
                )
            
            # Step 8: VHS effects already applied in layout
            print("\n[STEP 8/9] VHS effects applied ✅")
            
            # Step 9: Save to output directory
            print("\n[STEP 9/9] Saving final video...")
            if concept['style'] == "WARNING":
                output_dir = self.output_base_dir / "Winners"
                self.stats["warning_count"] += 1
            else:
                output_dir = self.output_base_dir / "Comedy"
                self.stats["comedy_count"] += 1
            
            # Create safe filename
            safe_title = "".join(c for c in concept['title'] if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_title = safe_title[:50]  # Limit length
            
            final_path = output_dir / f"{video_id}_{safe_title}.mp4"
            
            # Copy final video
            import shutil
            shutil.copy2(layout_video, final_path)
            
            # Update stats
            elapsed = time.time() - start_time
            self.stats["total_generated"] += 1
            self.stats["total_time"] += elapsed
            
            print(f"\n[SCARIFY] ✅ VIDEO COMPLETE!")
            print(f"  Output: {final_path}")
            print(f"  Time: {elapsed:.1f}s")
            print(f"  Cost: ${self.stats['total_cost']:.4f}")
            
            # Return video info
            return {
                "video_id": video_id,
                "path": str(final_path),
                "concept": concept,
                "duration": duration,
                "generation_time": elapsed,
                "cached": cached_video is not None
            }
            
        except Exception as e:
            print(f"\n[SCARIFY] ❌ Pipeline error: {e}")
            import traceback
            traceback.print_exc()
            return None
        
        finally:
            # Cleanup temp directory
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def generate_batch(
        self,
        count: int,
        skip_effects: bool = False
    ) -> List[Dict]:
        """
        Generate multiple videos in batch.
        
        Args:
            count: Number of videos to generate
            skip_effects: Skip heavy effects for faster processing
            
        Returns:
            List of video info dicts
        """
        print("\n" + "="*60)
        print(f"SCARIFY BATCH GENERATION - {count} VIDEOS")
        print("="*60)
        
        videos = []
        
        for i in range(count):
            print(f"\n\n{'='*60}")
            print(f"VIDEO {i+1}/{count}")
            print(f"{'='*60}")
            
            video = self.generate_complete_video(skip_effects=skip_effects)
            
            if video:
                videos.append(video)
            else:
                print(f"[BATCH] Warning: Video {i+1} failed")
            
            # Show progress
            print(f"\n[BATCH] Progress: {len(videos)}/{count} successful")
        
        # Final report
        self.print_stats()
        
        return videos
    
    def print_stats(self):
        """Print generation statistics."""
        print("\n" + "="*60)
        print("SCARIFY GENERATION STATISTICS")
        print("="*60)
        print(f"Total videos: {self.stats['total_generated']}")
        print(f"  WARNING format: {self.stats['warning_count']} ({self.stats['warning_count']/max(1,self.stats['total_generated'])*100:.1f}%)")
        print(f"  COMEDY format: {self.stats['comedy_count']} ({self.stats['comedy_count']/max(1,self.stats['total_generated'])*100:.1f}%)")
        print(f"\nCache performance:")
        print(f"  Hits: {self.stats['cache_hits']}")
        print(f"  Misses: {self.stats['cache_misses']}")
        if self.stats['cache_hits'] + self.stats['cache_misses'] > 0:
            hit_rate = self.stats['cache_hits'] / (self.stats['cache_hits'] + self.stats['cache_misses']) * 100
            print(f"  Hit rate: {hit_rate:.1f}%")
        print(f"\nCosts:")
        print(f"  Total: ${self.stats['total_cost']:.2f}")
        print(f"  Per video: ${self.stats['total_cost']/max(1,self.stats['total_generated']):.3f}")
        print(f"\nCache savings: ${self.stats['cache_hits'] * 0.04:.2f}")
        print(f"\nTime:")
        print(f"  Total: {self.stats['total_time']:.1f}s")
        print(f"  Per video: {self.stats['total_time']/max(1,self.stats['total_generated']):.1f}s")
        print("="*60)
        
        # Cache stats
        cache_stats = self.cache.get_stats()
        print(f"\nCache statistics:")
        print(f"  Total entries: {cache_stats['total_entries']}")
        print(f"  Total reuses: {cache_stats['total_reuses']}")
        print(f"  Cost saved: ${cache_stats['cost_saved']:.2f}")
        print(f"  Cache size: {cache_stats['cache_size_mb']:.1f} MB")


if __name__ == "__main__":
    print("="*60)
    print("SCARIFY COMPLETE VIDEO GENERATION SYSTEM")
    print("="*60)
    
    # Initialize pipeline
    pipeline = ScarifyPipeline(
        output_base_dir="./scarify_output",
        cache_dir="./kling_cache",
        portraits_dir="./portraits",
        use_mock_mode=True  # Set to False for production
    )
    
    print("\n[SCARIFY] Pipeline initialized!")
    print(f"  Output: {pipeline.output_base_dir}")
    print(f"  Cache: {pipeline.cache_dir}")
    print(f"  Portraits: {len(pipeline._portraits)} available")
    print(f"  Mode: {'MOCK' if pipeline.use_mock_mode else 'PRODUCTION'}")
    
    # Generate single test video
    print("\n\n" + "="*60)
    print("GENERATING TEST VIDEO")
    print("="*60)
    
    video = pipeline.generate_complete_video(skip_effects=True)
    
    if video:
        print("\n✅ Test video generated successfully!")
        print(f"   Path: {video['path']}")
    else:
        print("\n❌ Test video generation failed")
    
    # Print final stats
    pipeline.print_stats()
