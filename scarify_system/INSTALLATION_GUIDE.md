# SCARIFY Installation Guide

Complete setup guide for SCARIFY video generation system on Windows.

## 📋 Prerequisites

### 1. Python 3.9 or higher
Check your Python version:
```cmd
python --version
```

Download from: https://www.python.org/downloads/

### 2. FFmpeg (Required for video processing)

**Windows Installation:**

**Option A: Chocolatey (Recommended)**
```cmd
choco install ffmpeg
```

**Option B: Manual Installation**
1. Download from: https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg`
3. Add to PATH:
   - Right-click "This PC" → Properties
   - Advanced system settings → Environment Variables
   - Edit "Path" variable
   - Add: `C:\ffmpeg\bin`
4. Verify installation:
   ```cmd
   ffmpeg -version
   ```

### 3. Git (Optional, for version control)
Download from: https://git-scm.com/downloads

## 🚀 Installation Steps

### Step 1: Create Project Directory

```cmd
# Navigate to your projects folder
cd D:\
mkdir AI_Oracle_Projects
cd AI_Oracle_Projects

# Create required directories
mkdir Active\Scripts
mkdir Assets\Kling_Cache
mkdir Assets\Portraits
mkdir Output\Generated\Winners
mkdir Output\Generated\Comedy
```

### Step 2: Copy SCARIFY Files

Copy all Python scripts to:
```
D:\AI_Oracle_Projects\Active\Scripts\
```

Files to copy:
- ✅ DUAL_STYLE_GENERATOR.py
- ✅ KLING_CLIENT.py
- ✅ KLING_CACHE.py
- ✅ SUBLIMINAL_AUDIO.py
- ✅ VIDEO_LAYOUT.py
- ✅ SCARIFY_COMPLETE.py
- ✅ API_KEYS.py
- ✅ requirements.txt

### Step 3: Install Python Dependencies

```cmd
cd D:\AI_Oracle_Projects\Active\Scripts
pip install -r requirements.txt
```

Expected packages:
- requests
- numpy
- scipy
- Pillow
- ffmpeg-python
- elevenlabs

### Step 4: Configure API Keys

Edit `D:\AI_Oracle_Projects\Active\Scripts\API_KEYS.py`:

```python
# Kling AI API Key
KLING_API_KEY = "your_actual_kling_key_here"

# ElevenLabs API Key  
ELEVENLABS_API_KEY = "your_actual_elevenlabs_key_here"
```

**Get your API keys:**
- Kling AI: https://klingai.com/ (Sign up → API Keys)
- ElevenLabs: https://elevenlabs.io/ (Account → API Keys)

### Step 5: Add Portrait Images

Add 5-10 Abraham Lincoln portraits to:
```
D:\AI_Oracle_Projects\Assets\Portraits\
```

**Portrait requirements:**
- Format: JPG or PNG
- Resolution: 512x512 or higher
- Face clearly visible
- Variety: Different angles, expressions

**Where to find portraits:**
- Public domain images: commons.wikimedia.org
- AI-generated: Midjourney, Stable Diffusion
- Historical archives: Library of Congress

### Step 6: Verify Installation

Test all components:

```cmd
cd D:\AI_Oracle_Projects\Active\Scripts

# Test concept generator
python DUAL_STYLE_GENERATOR.py

# Test cache system
python KLING_CACHE.py

# Test audio mixer (requires FFmpeg)
python SUBLIMINAL_AUDIO.py

# Validate API keys
python API_KEYS.py
```

### Step 7: Test Complete System

Run a test generation (mock mode):

```cmd
python SCARIFY_COMPLETE.py
```

This will test the full pipeline without making API calls.

## 🎯 First Real Video Generation

Once installation is verified:

```python
from SCARIFY_COMPLETE import ScarifyPipeline

# Initialize pipeline
pipeline = ScarifyPipeline(
    output_base_dir="D:/AI_Oracle_Projects/Output/Generated",
    cache_dir="D:/AI_Oracle_Projects/Assets/Kling_Cache",
    portraits_dir="D:/AI_Oracle_Projects/Assets/Portraits",
    use_mock_mode=False  # Set to False for production
)

# Generate first video
video = pipeline.generate_complete_video(skip_effects=True)

if video:
    print(f"✅ Video saved: {video['path']}")
else:
    print("❌ Generation failed - check error messages")
```

## 🔧 Troubleshooting

### "python: command not found"
- Python not installed or not in PATH
- Try using `python3` instead of `python`
- Reinstall Python with "Add to PATH" option checked

### "ffmpeg: command not found"
- FFmpeg not installed or not in PATH
- Follow FFmpeg installation steps above
- Restart terminal after installation

### "ModuleNotFoundError: No module named 'X'"
- Dependencies not installed
- Run: `pip install -r requirements.txt`
- Check Python version (requires 3.9+)

### "API key not configured"
- Edit `API_KEYS.py` with your actual keys
- Verify keys are correct (no extra spaces/quotes)
- Test with: `python API_KEYS.py`

### "No portraits found"
- Add portrait images to `Assets/Portraits/` directory
- Supported formats: .jpg, .jpeg, .png
- Minimum: 1 portrait, Recommended: 5-10

### "ElevenLabs quota exceeded"
- Check your ElevenLabs usage limits
- Free tier: 10,000 characters/month
- Upgrade plan or wait for quota reset

### Video generation fails
- Check FFmpeg is working: `ffmpeg -version`
- Verify all directories exist
- Check API keys are valid
- Review error messages in console
- Try with `skip_effects=True` for faster debugging

## 📊 Directory Structure

After installation, your structure should look like:

```
D:\AI_Oracle_Projects\
├── Active\
│   └── Scripts\
│       ├── DUAL_STYLE_GENERATOR.py
│       ├── KLING_CLIENT.py
│       ├── KLING_CACHE.py
│       ├── SUBLIMINAL_AUDIO.py
│       ├── VIDEO_LAYOUT.py
│       ├── SCARIFY_COMPLETE.py
│       ├── API_KEYS.py
│       └── requirements.txt
├── Assets\
│   ├── Kling_Cache\
│   │   └── cache_index.json (auto-created)
│   └── Portraits\
│       ├── lincoln_1.jpg
│       ├── lincoln_2.jpg
│       └── ... (5-10 total)
└── Output\
    └── Generated\
        ├── Winners\    (WARNING format videos)
        └── Comedy\     (COMEDY format videos)
```

## 🎬 Production Deployment

### Create Batch Script

Create `D:\AI_Oracle_Projects\generate_daily_batch.bat`:

```batch
@echo off
cd /d D:\AI_Oracle_Projects\Active\Scripts
python SCARIFY_COMPLETE.py
pause
```

### Create Python Runner

Create `D:\AI_Oracle_Projects\Active\Scripts\run_batch.py`:

```python
from SCARIFY_COMPLETE import ScarifyPipeline

pipeline = ScarifyPipeline(
    output_base_dir="D:/AI_Oracle_Projects/Output/Generated",
    cache_dir="D:/AI_Oracle_Projects/Assets/Kling_Cache",
    portraits_dir="D:/AI_Oracle_Projects/Assets/Portraits"
)

# Generate 25 videos
videos = pipeline.generate_batch(count=25)

print(f"\n✅ Generated {len(videos)} videos")
pipeline.print_stats()
```

Run daily:
```cmd
python run_batch.py
```

### Schedule Daily Generation

**Windows Task Scheduler:**
1. Open Task Scheduler
2. Create Basic Task
3. Name: "SCARIFY Daily Generation"
4. Trigger: Daily at 8:00 AM
5. Action: Start a program
   - Program: `python`
   - Arguments: `D:\AI_Oracle_Projects\Active\Scripts\run_batch.py`
6. Finish

## 💰 Cost Tracking

Monitor your costs:

```python
from KLING_CACHE import KlingCache

cache = KlingCache("D:/AI_Oracle_Projects/Assets/Kling_Cache")
stats = cache.get_stats()

print(f"Total videos cached: {stats['total_entries']}")
print(f"Total reuses: {stats['total_reuses']}")
print(f"Cost saved: ${stats['cost_saved']:.2f}")
```

## 📈 Performance Optimization

### Speed up generation:
1. Use `skip_effects=True` for faster processing
2. Increase cache hits by reusing audio/portraits
3. Generate in batches (amortizes startup time)
4. Use SSD for cache storage

### Reduce costs:
1. Always check cache before Kling API calls (automatic)
2. Reuse portraits (80% reuse rate recommended)
3. Monitor ElevenLabs character usage
4. Batch generate to maximize cache efficiency

## 🔒 Security Best Practices

1. **Never commit API keys**
   ```cmd
   # Add to .gitignore
   echo API_KEYS.py >> .gitignore
   ```

2. **Backup your cache**
   ```cmd
   # Weekly backup
   xcopy D:\AI_Oracle_Projects\Assets\Kling_Cache D:\Backups\Kling_Cache\ /E /I /Y
   ```

3. **Monitor API usage**
   - Check Kling AI dashboard weekly
   - Check ElevenLabs usage daily
   - Set up billing alerts

## 📞 Support

If issues persist:
1. Check error messages carefully
2. Review troubleshooting section
3. Test each module individually
4. Verify all prerequisites installed
5. Check file paths are correct

## ✅ Installation Checklist

- [ ] Python 3.9+ installed
- [ ] FFmpeg installed and in PATH
- [ ] All directories created
- [ ] Python scripts copied to `Active/Scripts/`
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] API keys configured in `API_KEYS.py`
- [ ] Portrait images added (5-10 images)
- [ ] Test scripts run successfully
- [ ] Complete system test passed
- [ ] First video generated successfully

---

**Once complete, you're ready to generate videos at scale!**

Run your first batch:
```cmd
cd D:\AI_Oracle_Projects\Active\Scripts
python run_batch.py
```
