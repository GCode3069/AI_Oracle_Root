# SCARIFY Video Generation System

Complete automated Abraham Lincoln AI video system for YouTube Shorts monetization.

## 🎯 Project Overview

SCARIFY generates viral-ready vertical videos (1080x1920) featuring AI Abraham Lincoln delivering:
- **70% WARNING format**: Serious topics (Education, Military, Government, Economy)
- **30% COMEDY format**: Humorous observational content

**Target Economics:**
- Cost: $0.02-0.03 per video (with caching)
- Duration: 25-45 seconds
- Format: YouTube Shorts (9:16 vertical)

## 📁 System Architecture

```
SCARIFY_COMPLETE.py          Main pipeline orchestrator
├── DUAL_STYLE_GENERATOR.py  70/30 WARNING/comedy templates
├── KLING_CLIENT.py           Kling AI lip-sync API client
├── KLING_CACHE.py            MD5-based video caching
├── SUBLIMINAL_AUDIO.py       Binaural beats & audio mixing
├── VIDEO_LAYOUT.py           PiP layout + VHS effects
└── API_KEYS.py               API credentials (not in git)
```

## 🚀 Quick Start

### 1. Prerequisites

**Install FFmpeg:**
- Windows: Download from https://ffmpeg.org/download.html
- Linux: `sudo apt-get install ffmpeg`
- Mac: `brew install ffmpeg`

**Python Requirements:**
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Edit `API_KEYS.py`:
```python
KLING_API_KEY = "your_actual_key_here"
ELEVENLABS_API_KEY = "your_actual_key_here"
```

Get your keys:
- Kling AI: https://klingai.com/
- ElevenLabs: https://elevenlabs.io/

### 3. Add Portrait Images

Place Abraham Lincoln portrait images in:
```
D:\AI_Oracle_Projects\Assets\Portraits\
  - lincoln_1.jpg
  - lincoln_2.jpg
  - lincoln_3.jpg
  (Add 5-10 variations)
```

### 4. Generate Videos

**Single video:**
```bash
python SCARIFY_COMPLETE.py
```

**Batch generation (10 videos):**
```python
from SCARIFY_COMPLETE import ScarifyPipeline

pipeline = ScarifyPipeline(
    output_base_dir="D:/AI_Oracle_Projects/Output/Generated",
    cache_dir="D:/AI_Oracle_Projects/Assets/Kling_Cache"
)

videos = pipeline.generate_batch(count=10)
```

## 📊 Pipeline Steps

1. **Generate Concept** - 70% WARNING, 30% COMEDY split
2. **Generate Script** - Structured narrative with hooks
3. **Synthesize Voice** - ElevenLabs TTS (Rachel voice)
4. **Add Subliminal Audio** - Binaural beats, attention tones, VHS hiss
5. **Select Portrait** - 80% reuse rate for consistency
6. **Check Cache** - MD5-based, saves $0.04 per hit
7. **Generate Lip-Sync** - Kling AI (if not cached)
8. **Create Layout** - 1080x1920 PiP with title overlay
9. **Apply VHS Effects** - Scanlines, chromatic aberration, noise, vignette

## 💰 Cost Optimization

**Kling Cache System:**
- Saves $0.04 per cached video reuse
- MD5 hash-based matching
- Automatic tracking of reuse counts

**Expected costs with caching:**
- First 100 videos: ~$3.50
- Next 100 videos: ~$2.00 (50% cache hit rate)
- Long-term: ~$0.02-0.03 per video

## 🎨 Video Formats

### WARNING Format (70%)
- Categories: Education, Military, Government, Economy
- Style: White text on black box (60% opacity)
- Topics: Serious, urgent, attention-grabbing
- Example: "WARNING: Your School Is Teaching This"

### COMEDY Format (30%)
- Category: Entertainment
- Style: Yellow text on black box (50% opacity)
- Topics: Observational humor, modern life contrasts
- Example: "Abe Lincoln Watches TikTok Dances"

## 📂 Output Structure

```
D:\AI_Oracle_Projects\Output\Generated\
├── Winners\         (WARNING format videos)
│   ├── scarify_1234567890_WARNING_Your_School.mp4
│   └── ...
└── Comedy\          (COMEDY format videos)
    ├── scarify_1234567891_Abe_Lincoln_Watches.mp4
    └── ...
```

## 🔧 Configuration

Edit `API_KEYS.py` CONFIG dict:

```python
CONFIG = {
    "generation": {
        "warning_ratio": 0.70,        # 70% WARNING
        "comedy_ratio": 0.30,         # 30% COMEDY
        "portrait_reuse_rate": 0.80,  # 80% reuse
        "target_duration_min": 25,    # seconds
        "target_duration_max": 45     # seconds
    }
}
```

## 🧪 Testing

**Test individual modules:**

```bash
# Test concept generation
python DUAL_STYLE_GENERATOR.py

# Test Kling client (mock mode)
python KLING_CLIENT.py

# Test cache system
python KLING_CACHE.py

# Test audio mixing
python SUBLIMINAL_AUDIO.py

# Test video layout
python VIDEO_LAYOUT.py
```

**Test complete pipeline (mock mode):**
```python
pipeline = ScarifyPipeline(use_mock_mode=True)
video = pipeline.generate_complete_video(skip_effects=True)
```

## 📈 Monitoring

**Check statistics:**
```python
pipeline.print_stats()
```

**Output:**
```
SCARIFY GENERATION STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total videos: 100
  WARNING format: 70 (70.0%)
  COMEDY format: 30 (30.0%)

Cache performance:
  Hits: 45
  Misses: 55
  Hit rate: 45.0%

Costs:
  Total: $2.20
  Per video: $0.022

Cache savings: $1.80
```

## 🛠️ Advanced Features

### Custom Script Generation

```python
from DUAL_STYLE_GENERATOR import generate_warning_concept

concept = generate_warning_concept()
# Modify concept['script'] as needed
```

### Batch Processing with Custom Styles

```python
# Generate 20 WARNING videos
for _ in range(20):
    pipeline.generate_complete_video(force_style="WARNING")

# Generate 10 COMEDY videos
for _ in range(10):
    pipeline.generate_complete_video(force_style="COMEDY")
```

### Cache Management

```python
from KLING_CACHE import KlingCache

cache = KlingCache("./kling_cache")

# View stats
stats = cache.get_stats()
print(f"Total entries: {stats['total_entries']}")
print(f"Cost saved: ${stats['cost_saved']:.2f}")

# Prune unused entries
cache.prune_unused(min_reuse_count=0)

# Clear cache
cache.clear_cache()
```

## 🚨 Troubleshooting

**"FFmpeg not found":**
- Install FFmpeg and add to system PATH
- Verify: `ffmpeg -version`

**"API key not configured":**
- Edit `API_KEYS.py` with your actual keys
- Run: `python API_KEYS.py` to validate

**"No portraits found":**
- Add portrait images to `portraits/` directory
- Supported formats: JPG, PNG
- Recommended: 5-10 high-quality portraits

**"ElevenLabs quota exceeded":**
- Check your ElevenLabs account quota
- Consider upgrading plan for higher limits
- Use mock mode for testing: `use_mock_mode=True`

## 📝 File Locations

Update paths in your deployment:

```python
pipeline = ScarifyPipeline(
    output_base_dir="D:/AI_Oracle_Projects/Output/Generated",
    cache_dir="D:/AI_Oracle_Projects/Assets/Kling_Cache",
    portraits_dir="D:/AI_Oracle_Projects/Assets/Portraits"
)
```

## 🔒 Security

**Protect your API keys:**
1. Never commit `API_KEYS.py` to version control
2. Add to `.gitignore`:
   ```
   API_KEYS.py
   *.env
   credentials/
   ```
3. Use environment variables in production:
   ```python
   KLING_API_KEY = os.getenv("KLING_API_KEY")
   ```

## 📞 Support

For issues or questions:
1. Check troubleshooting section
2. Review test outputs from individual modules
3. Verify API key configuration
4. Ensure FFmpeg is installed and accessible

## 🎬 Production Workflow

**Daily batch generation:**
```python
# Generate 50 videos per day
pipeline = ScarifyPipeline(
    output_base_dir="D:/AI_Oracle_Projects/Output/Generated",
    cache_dir="D:/AI_Oracle_Projects/Assets/Kling_Cache"
)

# Morning batch: 25 videos
videos_morning = pipeline.generate_batch(25)

# Evening batch: 25 videos
videos_evening = pipeline.generate_batch(25)

# Review statistics
pipeline.print_stats()
```

## 📊 Performance Benchmarks

**Typical generation times:**
- Concept generation: < 0.1s
- Voice synthesis: 2-5s
- Lip-sync generation: 30-60s (or 0s if cached)
- Video layout: 10-20s
- VHS effects: 5-10s

**Total per video:**
- First generation: 50-90 seconds
- Cached reuse: 15-30 seconds

## 🎯 YouTube Shorts Optimization

Videos are automatically optimized for YouTube Shorts:
- ✅ 1080x1920 (9:16 aspect ratio)
- ✅ 25-45 seconds duration (ideal for Shorts)
- ✅ Engaging hook in first 3 seconds
- ✅ Clear title overlay for discoverability
- ✅ High contrast visuals (WARNING format)
- ✅ Trendy aesthetics (VHS effects)

## 📈 Monetization Strategy

1. **Content Mix**: 70% serious (educational value) + 30% comedy (engagement)
2. **Consistency**: Generate 3-5 videos daily
3. **A/B Testing**: Track which categories perform best
4. **Optimization**: Adjust ratios based on analytics
5. **Scaling**: Increase batch size as channel grows

---

**Generated by SCARIFY System v1.0**
*Automated Abraham Lincoln AI Video Generation*
