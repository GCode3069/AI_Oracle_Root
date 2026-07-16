# KLING_CACHE.py
import json
import hashlib
from pathlib import Path

CACHE_FILE = Path("kling_cache.json")

def _get_cache_key(voice_path, portrait_path):
    """Generate cache key from voice and portrait paths"""
    combined = f"{voice_path}:{portrait_path}"
    return hashlib.md5(combined.encode()).hexdigest()

def check_cache(voice_path, portrait_path):
    """Check if video exists in cache"""
    if not CACHE_FILE.exists():
        return None
    
    try:
        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)
    except (json.JSONDecodeError, IOError):
        return None
    
    cache_key = _get_cache_key(voice_path, portrait_path)
    
    if cache_key in cache:
        video_path = cache[cache_key]
        if Path(video_path).exists():
            return video_path
    
    return None

def save_to_cache(video_path, voice_path, portrait_path):
    """Save video to cache"""
    cache = {}
    
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, 'r') as f:
                cache = json.load(f)
        except (json.JSONDecodeError, IOError):
            cache = {}
    
    cache_key = _get_cache_key(voice_path, portrait_path)
    cache[cache_key] = video_path
    
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache, f, indent=2)
        print(f"✅ Cached: {cache_key[:8]}...")
    except IOError as e:
        print(f"⚠️ Cache save failed: {e}")

def clear_cache():
    """Clear the entire cache"""
    if CACHE_FILE.exists():
        CACHE_FILE.unlink()
        print("✅ Cache cleared")
    else:
        print("ℹ️ Cache already empty")

def get_cache_stats():
    """Get cache statistics"""
    if not CACHE_FILE.exists():
        return {'entries': 0, 'valid': 0, 'invalid': 0}
    
    try:
        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)
    except (json.JSONDecodeError, IOError):
        return {'entries': 0, 'valid': 0, 'invalid': 0}
    
    valid = sum(1 for v in cache.values() if Path(v).exists())
    invalid = len(cache) - valid
    
    return {
        'entries': len(cache),
        'valid': valid,
        'invalid': invalid
    }

if __name__ == "__main__":
    print("🗄️ KLING CACHE SYSTEM\n")
    
    stats = get_cache_stats()
    print(f"Cache entries: {stats['entries']}")
    print(f"Valid: {stats['valid']}")
    print(f"Invalid: {stats['invalid']}")
    
    print("\nTest cache operations:")
    save_to_cache("test_video.mp4", "test_voice.mp3", "test_portrait.jpg")
    result = check_cache("test_voice.mp3", "test_portrait.jpg")
    print(f"Cache check result: {result}")
