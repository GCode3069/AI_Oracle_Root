# 🎙️ WAV2LIP + FFMPEG ZOOM - COMPLETE SETUP GUIDE

## **WHAT YOU NEED:**

Two options for lip-sync:
1. **Wav2Lip** (realistic, AI-powered) - BEST QUALITY
2. **FFmpeg Zoom** (simple animation) - FASTER

---

## **OPTION 1: WAV2LIP LOCAL SETUP**

### **Step 1: Run Setup Script**
```powershell
.\SETUP_WAV2LIP_LOCAL.ps1
```

This will:
- Clone Wav2Lip repository
- Install Python dependencies
- Download pre-trained models (~700MB)
- Create helper scripts

**Time:** 20-40 minutes (depending on internet speed)

---

### **Step 2: Test Wav2Lip**
```powershell
cd F:\AI_Oracle_Root\scarify\wav2lip
python wav2lip_helper.py ../assets/master_images/lincoln_optimized.jpg ../audio/test.mp3 test_lipsync.mp4
```

**Expected Result:**
- `test_lipsync.mp4` created
- Lincoln's mouth moves with audio
- Realistic lip movements

---

### **Step 3: Integrate into Generator**

Update `abraham_MAX_HEADROOM.py`:

```python
# Around line 740
def generate_lipsync_wav2lip_local(lincoln_image, audio_path, output_path):
    """Generate lip-sync using local Wav2Lip installation"""
    wav2lip_dir = BASE_DIR.parent / "wav2lip"
    
    if not wav2lip_dir.exists():
        print("[Wav2Lip] Not installed, run SETUP_WAV2LIP_LOCAL.ps1")
        return None
    
    checkpoint = wav2lip_dir / "checkpoints" / "wav2lip_gan.pth"
    if not checkpoint.exists():
        print("[Wav2Lip] Model not found")
        return None
    
    print("[Wav2Lip] Generating with local installation...")
    try:
        subprocess.run([
            'python', str(wav2lip_dir / 'inference.py'),
            '--checkpoint_path', str(checkpoint),
            '--face', str(lincoln_image),
            '--audio', str(audio_path),
            '--outfile', str(output_path),
            '--resize_factor', '1',
            '--fps', '25',
            '--pads', '0', '10', '0', '0'
        ], timeout=300, check=True, capture_output=True)
        
        if output_path.exists() and output_path.stat().st_size > 1000:
            print(f"[Wav2Lip] Success: {output_path.name}")
            return output_path
    except Exception as e:
        print(f"[Wav2Lip] Error: {e}")
    
    return None
```

Then in `generate_lipsync_fallback`, add before Option 3:

```python
# Option 2.5: Local Wav2Lip
lipsync = generate_lipsync_wav2lip_local(lincoln_image, audio_path, output_path)
if lipsync:
    return lipsync
```

---

## **OPTION 2: FIX FFMPEG ZOOM**

### **Step 1: Diagnose Issue**
```powershell
.\FIX_FFMPEG_ZOOM.ps1
```

This will:
- Test 4 different zoom scenarios
- Identify what works and what doesn't
- Create test videos for verification

---

### **Step 2: Review Test Results**

**If All Tests Pass:**
- Issue is timeout or path problem
- Fix in main code

**If Tests Fail:**
- FFmpeg zoom syntax issue
- Use Wav2Lip instead

---

### **Step 3: Apply Fix (if tests pass)**

Update `abraham_MAX_HEADROOM.py` around line 784:

```python
# BEFORE (problematic):
subprocess.run([
    'ffmpeg', '-loop', '1', '-i', str(lincoln_image),
    '-i', str(audio_path),
    '-filter_complex',
    f"[0:v]scale=1080:1080:force_original_aspect_ratio=decrease,"
    f"pad=1080:1080:(ow-iw)/2:(oh-ih)/2:black,"
    f"zoompan=z='1.0+0.2*sin(2*2*PI*t)':d=1:x='iw/2-(iw/zoom/2)':y='ih/1.5-(ih/zoom/2)':s=1080x1080,"
    f"eq=contrast=1.3:brightness=-0.1[v]",
    '-map', '[v]', '-map', '1:a',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
    '-c:a', 'aac', '-b:a', '256k',
    '-t', str(duration), '-shortest',
    '-y', str(output_path)
], capture_output=True, timeout=600)

# AFTER (fixed):
result = subprocess.run([
    'ffmpeg', '-loop', '1', '-i', str(lincoln_image),
    '-i', str(audio_path),
    '-filter_complex',
    f"[0:v]scale=1080:1080:force_original_aspect_ratio=decrease,"
    f"pad=1080:1080:(ow-iw)/2:(oh-ih)/2:black,"
    f"zoompan=z='1.0+0.2*sin(2*2*PI*t)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1080,"
    f"eq=contrast=1.3:brightness=-0.1[v]",
    '-map', '[v]', '-map', '1:a',
    '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '23',  # Changed preset
    '-c:a', 'aac', '-b:a', '128k',
    '-t', str(duration), '-shortest',
    '-movflags', '+faststart',  # ADDED: Ensure proper MP4 structure
    '-y', str(output_path)
], capture_output=True, text=True, timeout=900)  # Increased timeout

# ADDED: Verify file is valid before returning
if output_path.exists() and output_path.stat().st_size > 1000:
    # Verify with ffprobe
    probe = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'default=noprint_wrappers=1:nokey=1', str(output_path)],
        capture_output=True, text=True
    )
    if probe.returncode == 0 and probe.stdout.strip():
        print(f"[Wav2Lip] Fallback video created: {output_path.name}")
        return output_path
    else:
        print(f"[Wav2Lip] File corrupted, deleting: {probe.stderr}")
        output_path.unlink(missing_ok=True)
        return None
else:
    print(f"[Wav2Lip] File too small or missing")
    return None
```

---

## **COMPARISON:**

| Feature | Wav2Lip | FFmpeg Zoom |
|---------|---------|-------------|
| **Quality** | ⭐⭐⭐⭐⭐ Realistic | ⭐⭐⭐ Simple animation |
| **Speed** | 30-60s per video | 5-10s per video |
| **Setup** | Complex (20-40 min) | Already installed |
| **GPU** | Optional but faster | Not needed |
| **File Size** | Larger (~100MB) | Smaller (~60MB) |
| **Realism** | Actual lip-sync | Pulsing/breathing |

---

## **RECOMMENDATION:**

### **For Best Quality:**
1. Install Wav2Lip (run `.\SETUP_WAV2LIP_LOCAL.ps1`)
2. Enable in generator
3. First video will be slow (model loading)
4. Subsequent videos faster (~30s each)

### **For Speed:**
1. Fix FFmpeg zoom (run `.\FIX_FFMPEG_ZOOM.ps1`)
2. Apply code fixes above
3. Videos generate in 5-10 seconds
4. "Good enough" lip movement

### **For Scale (100+ videos):**
1. Use **FFmpeg zoom** for initial batch
2. Install Wav2Lip in parallel
3. Re-generate top 10 performers with Wav2Lip
4. Best of both worlds

---

## **QUICK START:**

```powershell
# Option A: Install Wav2Lip (best quality)
.\SETUP_WAV2LIP_LOCAL.ps1

# Option B: Fix FFmpeg zoom (faster)
.\FIX_FFMPEG_ZOOM.ps1

# Then generate test video
python abraham_MAX_HEADROOM.py 1
```

---

## **TROUBLESHOOTING:**

### **Wav2Lip Issues:**

**"CUDA out of memory":**
- Use CPU mode (slower but works)
- Add `--device cpu` to inference.py call

**"Model download failed":**
- Manual download from: https://github.com/Rudrabha/Wav2Lip#getting-the-weights
- Save to: `F:\AI_Oracle_Root\scarify\wav2lip\checkpoints\wav2lip_gan.pth`

**"Python 3.10 not compatible":**
- Install Python 3.9 separately
- Use virtual environment: `python3.9 -m venv wav2lip_env`

### **FFmpeg Zoom Issues:**

**"moov atom not found":**
- Add `-movflags '+faststart'` to command
- Increase timeout to 900 seconds
- Verify file with ffprobe before using

**"File too small":**
- Check FFmpeg stderr for errors
- Verify input files exist
- Test with simple 5-second video first

---

## **FILES CREATED:**

- `SETUP_WAV2LIP_LOCAL.ps1` - Automated Wav2Lip installation
- `FIX_FFMPEG_ZOOM.ps1` - Debug FFmpeg zoom issues
- `INTEGRATE_WAV2LIP_AND_ZOOM.md` - This guide

---

## **NEXT STEPS:**

1. **Choose your approach** (Wav2Lip OR FFmpeg zoom)
2. **Run setup script** (`.\SETUP_WAV2LIP_LOCAL.ps1` or `.\FIX_FFMPEG_ZOOM.ps1`)
3. **Test with 1 video:** `python abraham_MAX_HEADROOM.py 1`
4. **Verify lip-sync works**
5. **Scale to 10+ videos**

🎙️💀🔥


