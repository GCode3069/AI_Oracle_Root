# SCARIFY Quick Start Guide

Get generating videos in 5 minutes!

## ⚡ Quick Installation

```cmd
# 1. Navigate to project directory
cd D:\AI_Oracle_Projects\Active\Scripts

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API keys (edit file)
notepad API_KEYS.py

# 4. Add portraits
# Copy 5-10 Abraham Lincoln images to:
# D:\AI_Oracle_Projects\Assets\Portraits\
```

## 🚀 Generate Your First Video

### Option 1: Single Video (Python)

```python
from SCARIFY_COMPLETE import ScarifyPipeline

pipeline = ScarifyPipeline()
video = pipeline.generate_complete_video()

if video:
    print(f"✅ Video: {video['path']}")
```

### Option 2: Batch Generation (Command Line)

```cmd
# Generate 10 videos
python run_batch.py

# Generate 25 videos
python run_batch.py 25

# Generate 100 videos (fast mode)
python run_batch.py 100 --fast
```

## 📁 Output Locations

Videos are saved to:
```
D:\AI_Oracle_Projects\Output\Generated\
├── Winners\    ← WARNING format videos (70%)
└── Comedy\     ← COMEDY format videos (30%)
```

## 🎯 Common Commands

### Generate Specific Style

```python
from SCARIFY_COMPLETE import ScarifyPipeline

pipeline = ScarifyPipeline()

# Force WARNING format
video = pipeline.generate_complete_video(force_style="WARNING")

# Force COMEDY format
video = pipeline.generate_complete_video(force_style="COMEDY")
```

### Fast Generation (Skip VHS Effects)

```python
video = pipeline.generate_complete_video(skip_effects=True)
```

### Daily Batch (50 videos)

```cmd
python run_batch.py 50
```

## 📊 Check Statistics

```python
from SCARIFY_COMPLETE import ScarifyPipeline

pipeline = ScarifyPipeline()
pipeline.generate_batch(10)  # Generate some videos
pipeline.print_stats()       # Show statistics
```

## 💰 Monitor Costs

```python
from KLING_CACHE import KlingCache

cache = KlingCache("D:/AI_Oracle_Projects/Assets/Kling_Cache")
stats = cache.get_stats()

print(f"Cost saved: ${stats['cost_saved']:.2f}")
print(f"Cache entries: {stats['total_entries']}")
```

## 🔧 Test Mode (No API Calls)

```python
# Test without using API credits
pipeline = ScarifyPipeline(use_mock_mode=True)
video = pipeline.generate_complete_video()
```

Or via command line:
```cmd
python run_batch.py 5 --mock
```

## ⚙️ Configuration

### Change Output Directory

```python
pipeline = ScarifyPipeline(
    output_base_dir="E:/MyVideos",
    cache_dir="E:/Cache",
    portraits_dir="E:/Portraits"
)
```

### Adjust Generation Ratios

Edit `API_KEYS.py`:
```python
CONFIG = {
    "generation": {
        "warning_ratio": 0.80,  # 80% WARNING
        "comedy_ratio": 0.20,   # 20% COMEDY
        "portrait_reuse_rate": 0.90  # 90% reuse
    }
}
```

## 🚨 Troubleshooting

### "FFmpeg not found"
```cmd
# Install FFmpeg
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
# Add to PATH environment variable
```

### "API key not configured"
```cmd
# Edit API_KEYS.py with your actual keys
notepad API_KEYS.py

# Test configuration
python API_KEYS.py
```

### "No portraits found"
```
# Add portrait images to:
D:\AI_Oracle_Projects\Assets\Portraits\

# Supported: .jpg, .jpeg, .png
# Minimum: 1 image
# Recommended: 5-10 images
```

## 📈 Production Workflow

### Daily Generation Schedule

Create `daily_generation.bat`:
```batch
@echo off
cd /d D:\AI_Oracle_Projects\Active\Scripts
python run_batch.py 25
pause
```

Run via Windows Task Scheduler:
- Open Task Scheduler
- Create Basic Task
- Schedule: Daily, 8:00 AM
- Action: Run `daily_generation.bat`

### Weekly Cost Report

Create `weekly_report.py`:
```python
from KLING_CACHE import KlingCache

cache = KlingCache("D:/AI_Oracle_Projects/Assets/Kling_Cache")
stats = cache.get_stats()

print("\n=== WEEKLY SCARIFY REPORT ===")
print(f"Videos cached: {stats['total_entries']}")
print(f"Total reuses: {stats['total_reuses']}")
print(f"Cost saved: ${stats['cost_saved']:.2f}")
print(f"Cache size: {stats['cache_size_mb']:.1f} MB")
```

## 🎬 Content Strategy

### Optimal Mix
- **70% WARNING**: Education, Military, Government, Economy
- **30% COMEDY**: Entertainment, observational humor

### Posting Schedule
- 3-5 videos per day
- Consistent upload times
- Mix formats throughout day
- Monitor which topics perform best

### A/B Testing
```python
# Generate 10 of each style for testing
for _ in range(10):
    pipeline.generate_complete_video(force_style="WARNING")
    
for _ in range(10):
    pipeline.generate_complete_video(force_style="COMEDY")

# Compare performance on YouTube
```

## 💡 Pro Tips

1. **Start small**: Test with 5-10 videos before scaling
2. **Check cache**: Monitor cache hit rate (aim for 50%+)
3. **Portrait variety**: Use 5-10 different portraits
4. **Fast mode**: Use `--fast` during development/testing
5. **Backup cache**: Copy cache directory weekly
6. **Monitor costs**: Check API usage daily
7. **Adjust ratios**: Based on what performs best

## 🔗 Important Files

- `SCARIFY_COMPLETE.py` - Main pipeline
- `run_batch.py` - Batch runner (easiest to use)
- `API_KEYS.py` - API configuration
- `README.md` - Full documentation
- `INSTALLATION_GUIDE.md` - Detailed setup
- `TEST_RESULTS.md` - Test validation

## 📞 Quick Help

**Issue?** Run individual component tests:
```cmd
python DUAL_STYLE_GENERATOR.py  # Test concepts
python KLING_CACHE.py            # Test cache
python API_KEYS.py               # Validate keys
```

**Still stuck?** Check:
1. FFmpeg installed? `ffmpeg -version`
2. API keys set? `python API_KEYS.py`
3. Portraits added? Check `Assets/Portraits/` folder
4. Python version? `python --version` (need 3.9+)

---

## 🎯 Your First Day Checklist

- [ ] Install FFmpeg
- [ ] Install Python dependencies
- [ ] Configure API keys
- [ ] Add 5+ portrait images
- [ ] Test with mock mode: `python run_batch.py 3 --mock`
- [ ] Generate first real video: `python run_batch.py 1`
- [ ] Check output in `Output/Generated/`
- [ ] Generate first batch: `python run_batch.py 10`
- [ ] Review statistics
- [ ] Set up daily generation schedule

## 🎉 Ready to Scale?

Once comfortable:
```cmd
# Generate 50 videos per day
python run_batch.py 50

# Monitor performance
python weekly_report.py

# Adjust strategy based on results
```

---

**Need more details?** See `README.md` for complete documentation.

**Installation issues?** See `INSTALLATION_GUIDE.md` for troubleshooting.

**System validation?** See `TEST_RESULTS.md` for test details.
