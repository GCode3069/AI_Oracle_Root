# 🤖 **GITHUB COPILOT INSTRUCTIONS FOR SCARIFY PROJECT**

## **PROJECT CONTEXT**

**Name**: SCARIFY - Abraham Lincoln VHS Broadcast Video Generator  
**Goal**: Generate viral YouTube Shorts with Max Headroom-style glitchy Abe Lincoln  
**Tech Stack**: Python, FFmpeg, ElevenLabs API, YouTube API  
**Current Status**: Production-ready, generating 50-100 videos/day

---

## **CODE STYLE GUIDELINES**

### **Python:**
```python
# Use pathlib for paths
from pathlib import Path
BASE_DIR = Path("F:/AI_Oracle_Root/scarify")

# Always use UTF-8 encoding
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Error handling is MANDATORY
try:
    result = risky_operation()
except Exception as e:
    print(f"[ERROR] {e}")
    # Always log errors
```

### **FFmpeg Commands:**
```python
# Always use timeout
subprocess.run(cmd, timeout=120, capture_output=True)

# Always check output exists
if not output_path.exists() or output_path.stat().st_size == 0:
    print(f"[ERROR] Output failed: {output_path}")
```

---

## **KEY PATTERNS TO FOLLOW**

### **1. Video Generation Flow:**
```
Headline → Script → Voice → Lincoln Image → Video Effects → Upload
```

### **2. Script Generation:**
- **SHORT**: 32-45 words (9-17s videos)
- **LONG**: 150-225 words (60-90s videos)
- **Style**: Dark satirical comedy (Pryor, Carlin, Chappelle)
- **Rule**: Roast EVERYONE (no political favorites)

### **3. VHS Effects Stack:**
```
Base video → RGB split → Scan lines → Static → TV frame → Audio degradation
```

### **4. Cost Awareness:**
- ElevenLabs: $22/month (KEEP - essential)
- Pexels: FREE (KEEP - working great)
- Pollo: $328/month (TEST - may cancel)
- Stability: $10/month (TEST - may keep)

---

## **COMMON TASKS**

### **When Adding New Features:**
1. Update `abraham_MAX_HEADROOM.py` (main system)
2. Update `abraham_ULTIMATE_COMBINED.py` (dual-format)
3. Update `ABRAHAM_STUDIO_VHS.pyw` (desktop GUI)
4. Test with `python abraham_ULTIMATE_COMBINED.py --short 1`
5. Document in relevant `.md` file

### **When Fixing Bugs:**
1. Check encoding (`encoding='utf-8'` everywhere)
2. Check file paths (use `Path` objects)
3. Check FFmpeg timeouts (increase if needed)
4. Test on Windows (target platform)

### **When Optimizing:**
1. Multi-pass rendering for long videos
2. Pre-generate static assets (scanlines, QR codes)
3. Use `stream_loop -1` with `-c copy` for B-roll
4. Target <60s for shorts, <90s for long

---

## **FILES TO KNOW**

### **Core Generators:**
- `abraham_MAX_HEADROOM.py` - Main system (all features)
- `abraham_ULTIMATE_COMBINED.py` - Dual-format generator
- `abraham_MAX_HEADROOM_OPTIMIZED.py` - Fast rendering for 60+ second videos

### **Desktop App:**
- `ABRAHAM_STUDIO_VHS.pyw` - GUI generator

### **Utilities:**
- `youtube_channel_analyzer.py` - Analytics
- `google_sheets_tracker.py` - Tracking
- `automated_channel_analyzer.py` - Auto-optimization

### **Documentation:**
- `STYLE_COMPARISON_AND_ULTIMATE_MIX.md` - All styles explained
- `ULTIMATE_SYSTEM_FINAL.md` - Complete system docs
- `API_TEST_RESULTS.md` - API cost analysis

---

## **NEVER DO THIS**

❌ Don't use `print()` with unicode arrows (→) - causes CP1252 errors  
❌ Don't forget `encoding='utf-8'` on file operations  
❌ Don't create long FFmpeg commands without timeouts  
❌ Don't generate videos without Bitcoin QR code  
❌ Don't let Abe recite Bitcoin address in audio  
❌ Don't skip error handling  
❌ Don't use emojis in print statements (Windows console)  

---

## **ALWAYS DO THIS**

✅ Use ASCII characters in print statements (`->` not `→`)  
✅ Add `encoding='utf-8'` to all file operations  
✅ Set FFmpeg timeout to 120s minimum  
✅ Include Bitcoin QR in all videos (visible, top-right)  
✅ Remove Bitcoin address from scripts (visual only)  
✅ Wrap risky code in try/except  
✅ Use `[OK]`, `[ERROR]`, `[INFO]` for status messages  

---

## **EXAMPLE: GOOD CODE**

```python
def generate_video(episode_num):
    """Generate video with all safety checks"""
    try:
        # Get headline
        headlines = get_headlines()
        headline = random.choice(headlines)
        print(f"[INFO] Processing: {headline[:50]}...")
        
        # Generate script (SHORT format)
        script = generate_script(headline)
        word_count = len(script.split())
        print(f"[OK] Script: {word_count} words")
        
        # Generate audio
        audio_path = Path(f"audio/ep_{episode_num}.mp3")
        if not generate_voice(script, audio_path):
            print(f"[ERROR] Voice generation failed")
            return None
        
        # Create video
        video_path = Path(f"videos/ep_{episode_num}.mp4")
        cmd = [
            'ffmpeg', '-y',
            '-i', str(audio_path),
            # ... filters ...
            str(video_path)
        ]
        
        result = subprocess.run(
            cmd,
            timeout=120,
            capture_output=True,
            text=True
        )
        
        if not video_path.exists() or video_path.stat().st_size == 0:
            print(f"[ERROR] Video creation failed")
            print(f"[DEBUG] {result.stderr}")
            return None
        
        print(f"[OK] Video created: {video_path.name}")
        return str(video_path)
        
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return None
```

---

## **WHEN SUGGESTING CODE**

1. **Always check** if feature already exists in `abraham_MAX_HEADROOM.py`
2. **Always test** suggestions work on Windows
3. **Always consider** API costs in recommendations
4. **Always maintain** existing VHS aesthetic
5. **Always preserve** dark satirical comedy style

---

## **PROJECT PRIORITIES**

1. **Quality** > Speed (but both are important)
2. **Cost optimization** (save $3,936/year by canceling Pollo)
3. **Automation** (50-100 videos/day without intervention)
4. **Monetization** (optimize for YouTube Shorts algorithm)
5. **Brand consistency** (VHS aesthetic, dark comedy)

---

## **USEFUL COMMANDS**

```bash
# Generate SHORT video (9-17s)
python abraham_ULTIMATE_COMBINED.py --short 1

# Generate LONG video (60-90s)
python abraham_ULTIMATE_COMBINED.py --long 1

# Generate BOTH formats
python abraham_ULTIMATE_COMBINED.py --both 1

# Run channel analysis
python automated_channel_analyzer.py --auto-run

# Launch desktop generator
python ABRAHAM_STUDIO_VHS.pyw
```

---

## **HELP ME WITH**

- Optimizing FFmpeg filters for faster rendering
- Improving dark comedy script generation
- Cost-saving API alternatives
- YouTube algorithm optimization
- Multi-platform distribution (TikTok, Rumble)
- Automated A/B testing
- Revenue tracking and analytics

---

**Last Updated**: October 31, 2025  
**Project Lead**: GCode3069  
**AI Assistants**: Cursor AI, GitHub Copilot

