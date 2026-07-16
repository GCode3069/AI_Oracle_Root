"""
KLING_CACHE.py
MD5-based caching system for Kling video generations.
Saves $0.04 per cached video reuse!
"""

import os
import json
import hashlib
import shutil
from typing import Optional, Dict, Tuple
from pathlib import Path
from datetime import datetime


class KlingCache:
    """
    MD5-based caching system for Kling AI video generations.
    
    Cache structure:
    - D:/AI_Oracle_Projects/Assets/Kling_Cache/
      - cache_index.json (metadata)
      - {md5_hash}/
        - video.mp4
        - audio.mp3
        - image.jpg
        - metadata.json
    """
    
    def __init__(self, cache_dir: str = "./kling_cache"):
        """
        Initialize cache system.
        
        Args:
            cache_dir: Root directory for cache storage
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.index_file = self.cache_dir / "cache_index.json"
        self.index = self._load_index()
    
    def _load_index(self) -> Dict:
        """Load cache index from disk."""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[CACHE] Warning: Could not load index: {e}")
                return {}
        return {}
    
    def _save_index(self):
        """Save cache index to disk."""
        try:
            with open(self.index_file, 'w') as f:
                json.dump(self.index, f, indent=2)
        except Exception as e:
            print(f"[CACHE] Warning: Could not save index: {e}")
    
    def _compute_hash(self, audio_path: str, image_path: str) -> str:
        """
        Compute MD5 hash of audio and image files.
        
        Args:
            audio_path: Path to audio file
            image_path: Path to image file
            
        Returns:
            MD5 hash string
        """
        hasher = hashlib.md5()
        
        # Hash audio file
        with open(audio_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        
        # Hash image file
        with open(image_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        
        return hasher.hexdigest()
    
    def check_cache(self, audio_path: str, image_path: str) -> Optional[str]:
        """
        Check if video exists in cache.
        
        Args:
            audio_path: Path to audio file
            image_path: Path to image file
            
        Returns:
            Path to cached video if exists, None otherwise
        """
        try:
            cache_hash = self._compute_hash(audio_path, image_path)
            
            if cache_hash in self.index:
                cache_entry = self.index[cache_hash]
                video_path = cache_entry["video_path"]
                
                # Verify video file exists
                if os.path.exists(video_path):
                    # Update reuse count
                    cache_entry["reuse_count"] = cache_entry.get("reuse_count", 0) + 1
                    cache_entry["last_accessed"] = datetime.now().isoformat()
                    self._save_index()
                    
                    reuse_count = cache_entry["reuse_count"]
                    cost_saved = reuse_count * 0.04
                    
                    print(f"[CACHE] ✅ HIT! Hash: {cache_hash[:8]}...")
                    print(f"[CACHE] Reused {reuse_count} times (${cost_saved:.2f} saved)")
                    return video_path
                else:
                    # Entry exists but file missing - remove from index
                    print(f"[CACHE] Warning: Cache entry exists but file missing")
                    del self.index[cache_hash]
                    self._save_index()
                    return None
            
            print(f"[CACHE] ❌ MISS - Hash: {cache_hash[:8]}...")
            return None
            
        except Exception as e:
            print(f"[CACHE] Error checking cache: {e}")
            return None
    
    def save_to_cache(
        self,
        video_path: str,
        audio_path: str,
        image_path: str,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Save video and source files to cache.
        
        Args:
            video_path: Path to generated video
            audio_path: Path to source audio
            image_path: Path to source image
            metadata: Optional metadata dict
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            # Compute hash
            cache_hash = self._compute_hash(audio_path, image_path)
            
            # Create cache directory for this hash
            cache_item_dir = self.cache_dir / cache_hash
            cache_item_dir.mkdir(exist_ok=True)
            
            # Copy files to cache
            cached_video = cache_item_dir / "video.mp4"
            cached_audio = cache_item_dir / "audio.mp3"
            cached_image = cache_item_dir / "image.jpg"
            
            shutil.copy2(video_path, cached_video)
            shutil.copy2(audio_path, cached_audio)
            shutil.copy2(image_path, cached_image)
            
            # Save metadata
            cache_metadata = {
                "created": datetime.now().isoformat(),
                "video_path": str(cached_video),
                "audio_path": str(cached_audio),
                "image_path": str(cached_image),
                "hash": cache_hash,
                "reuse_count": 0,
                "last_accessed": datetime.now().isoformat()
            }
            
            if metadata:
                cache_metadata["custom"] = metadata
            
            metadata_file = cache_item_dir / "metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(cache_metadata, f, indent=2)
            
            # Update index
            self.index[cache_hash] = cache_metadata
            self._save_index()
            
            print(f"[CACHE] 💾 Saved - Hash: {cache_hash[:8]}...")
            return True
            
        except Exception as e:
            print(f"[CACHE] Error saving to cache: {e}")
            return False
    
    def get_stats(self) -> Dict:
        """Get cache statistics."""
        total_entries = len(self.index)
        total_reuses = sum(entry.get("reuse_count", 0) for entry in self.index.values())
        total_saved = total_reuses * 0.04
        
        # Calculate cache size
        cache_size_bytes = 0
        for entry in self.index.values():
            video_path = entry.get("video_path")
            if video_path and os.path.exists(video_path):
                cache_size_bytes += os.path.getsize(video_path)
        
        cache_size_mb = cache_size_bytes / (1024 * 1024)
        
        return {
            "total_entries": total_entries,
            "total_reuses": total_reuses,
            "cost_saved": total_saved,
            "cache_size_mb": cache_size_mb,
            "avg_reuses_per_entry": total_reuses / total_entries if total_entries > 0 else 0
        }
    
    def clear_cache(self, keep_index: bool = False):
        """
        Clear all cache entries.
        
        Args:
            keep_index: If True, keep index file with empty entries
        """
        for cache_hash, entry in self.index.items():
            cache_item_dir = self.cache_dir / cache_hash
            if cache_item_dir.exists():
                shutil.rmtree(cache_item_dir)
        
        if keep_index:
            self.index = {}
            self._save_index()
        else:
            if self.index_file.exists():
                self.index_file.unlink()
            self.index = {}
        
        print("[CACHE] Cache cleared")
    
    def prune_unused(self, min_reuse_count: int = 0):
        """
        Remove cache entries with low reuse counts.
        
        Args:
            min_reuse_count: Minimum reuse count to keep entry
        """
        to_remove = []
        
        for cache_hash, entry in self.index.items():
            if entry.get("reuse_count", 0) <= min_reuse_count:
                to_remove.append(cache_hash)
                
                # Remove files
                cache_item_dir = self.cache_dir / cache_hash
                if cache_item_dir.exists():
                    shutil.rmtree(cache_item_dir)
        
        # Update index
        for cache_hash in to_remove:
            del self.index[cache_hash]
        
        self._save_index()
        print(f"[CACHE] Pruned {len(to_remove)} entries")


if __name__ == "__main__":
    print("=== KLING Cache System Test ===\n")
    
    # Initialize cache
    cache = KlingCache(cache_dir="./test_cache")
    
    # Create test files
    os.makedirs("test_files", exist_ok=True)
    
    test_audio = "test_files/audio.mp3"
    test_image = "test_files/image.jpg"
    test_video = "test_files/video.mp4"
    
    Path(test_audio).write_text("test audio content")
    Path(test_image).write_text("test image content")
    Path(test_video).write_text("test video content")
    
    # Test cache miss
    print("Test 1: Check cache (should miss):")
    result = cache.check_cache(test_audio, test_image)
    print(f"Result: {result}\n")
    
    # Test save to cache
    print("Test 2: Save to cache:")
    success = cache.save_to_cache(
        video_path=test_video,
        audio_path=test_audio,
        image_path=test_image,
        metadata={"test": True}
    )
    print(f"Success: {success}\n")
    
    # Test cache hit
    print("Test 3: Check cache (should hit):")
    result = cache.check_cache(test_audio, test_image)
    print(f"Result: {result}\n")
    
    # Test multiple reuses
    print("Test 4: Multiple cache hits:")
    for i in range(3):
        cache.check_cache(test_audio, test_image)
    print()
    
    # Test stats
    print("Test 5: Cache statistics:")
    stats = cache.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    print()
    
    # Cleanup
    import shutil
    shutil.rmtree("test_cache", ignore_errors=True)
    shutil.rmtree("test_files", ignore_errors=True)
    
    print("✅ All tests complete!")
