# KLING_CACHE.py
import hashlib
import json
import shutil
from pathlib import Path

CACHE_DIR = Path("D:/AI_Oracle_Projects/Assets/Kling_Cache")
CACHE_INDEX = CACHE_DIR / "cache_index.json"

def get_cache_key(audio_path, image_path):
    """Generate MD5 hash for cache key"""
    with open(audio_path, 'rb') as af, open(image_path, 'rb') as imf:
        audio_hash = hashlib.md5(af.read()).hexdigest()[:16]
        image_hash = hashlib.md5(imf.read()).hexdigest()[:16]
    return f"kling_{audio_hash}_{image_hash}.mp4"

def load_cache_index():
    """Load cache index"""
    if CACHE_INDEX.exists():
        with open(CACHE_INDEX, 'r') as f:
            return json.load(f)
    return {}

def save_cache_index(index):
    """Save cache index"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with open(CACHE_INDEX, 'w') as f:
        json.dump(index, f, indent=2)

def check_cache(audio_path, image_path):
    """Check if video exists in cache"""
    key = get_cache_key(audio_path, image_path)
    cache_file = CACHE_DIR / key
    
    if cache_file.exists():
        print(f"🔍 Cache HIT! Reusing: {key}")
        
        # Update index
        index = load_cache_index()
        if key in index:
            index[key]['reuse_count'] += 1
        else:
            index[key] = {'reuse_count': 1}
        save_cache_index(index)
        
        return str(cache_file)
    
    print(f"🔍 Cache MISS. Will generate new video.")
    return None

def save_to_cache(video_path, audio_path, image_path):
    """Save video to cache"""
    key = get_cache_key(audio_path, image_path)
    cache_file = CACHE_DIR / key
    
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy(video_path, cache_file)
    
    # Update index
    index = load_cache_index()
    index[key] = {
        'reuse_count': 0,
        'original_video': str(video_path),
        'created': str(Path(video_path).stat().st_mtime)
    }
    save_cache_index(index)
    
    print(f"💾 Saved to cache: {key}")
    return str(cache_file)

def get_cache_stats():
    """Get cache statistics"""
    index = load_cache_index()
    total_videos = len(index)
    total_reuses = sum(v['reuse_count'] for v in index.values())
    savings = total_reuses * 0.04  # $0.04 saved per reuse
    
    print(f"\n📊 CACHE STATISTICS:")
    print(f"   Cached videos: {total_videos}")
    print(f"   Total reuses: {total_reuses}")
    print(f"   Money saved: ${savings:.2f}")
    
    return {'videos': total_videos, 'reuses': total_reuses, 'savings': savings}
