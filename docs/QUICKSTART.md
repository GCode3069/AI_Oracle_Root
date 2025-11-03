# SCARIFY - Quick Start Guide

Get up and running in 5 minutes!

## 📦 What You Got

✅ Complete YouTube auto-upload system  
✅ Beautiful GUI launcher  
✅ Desktop shortcut creator  
✅ Full documentation  

## 🚀 5-Minute Setup

### Step 1: Verify Setup (1 min)
```powershell
.\test_setup.ps1
```

This checks if everything is ready to go.

### Step 2: Install Dependencies (1 min)
```powershell
pip install -r requirements.txt
```

### Step 3: Test Video Generation (2 min)
```powershell
python scarify_master.py --count 1 --test
```

This generates 1 test video WITHOUT uploading. Check `output/videos/` for the result.

### Step 4: Create Desktop Shortcut (30 sec)
```powershell
.\create_desktop_shortcut.ps1
```

Now you have a "SCARIFY Generator" icon on your desktop!

### Step 5: Set Up YouTube Upload (Optional, 5 min)
See: `YOUTUBE_SETUP_INSTRUCTIONS.md` for complete guide.

**TL;DR:**
1. Go to [console.cloud.google.com](https://console.cloud.google.com/)
2. Create project → Enable YouTube Data API v3
3. Create OAuth credentials (Desktop app)
4. Download → Save as `config/credentials/youtube/client_secrets.json`

## 🎮 Using the GUI

**Double-click** the desktop icon or run:
```powershell
.\scarify_launcher.ps1
```

### Three Buttons:

**📹 Generate 1 Test Video (No Upload)**
- Perfect for testing
- Creates one video locally
- No YouTube needed

**🚀 Generate 5 Videos + Upload to YouTube**
- Good for daily batches
- Auto-uploads to YouTube Shorts
- ~30 minutes total time

**💥 Generate 20 Videos + Upload to YouTube**
- Maximum daily batch
- Bulk content creation
- ~2 hours total time

## 💻 Command Line Usage

### Test (no upload)
```powershell
python scarify_master.py --count 1 --test
```

### Generate + Upload
```powershell
python scarify_master.py --count 5 --upload
```

## 📁 Output Location

Your videos will be saved to:
```
F:\AI_Oracle_Root\scarify\output\videos\
```

Click "📁 Open Output Folder" in the GUI for quick access.

## 🎯 Video Details

**Each video:**
- 50 seconds long
- Vertical format (1080x1920)
- Windows TTS audio
- Pexels stock footage
- Auto-titled: "SCARIFY: {pain_point} - Ex-Vet $97 Kit"
- Auto-uploaded as YouTube Short

**Pain points (cycles through 5):**
1. Chicago garage supply meltdown
2. Mechanic deadweight employees
3. Barber no-show clients
4. Plumber emergency call drought
5. Welder material waste

## ⚠️ Important Notes

### YouTube Quota
- **50 uploads per day** maximum
- Script tracks and warns you
- Resets at midnight Pacific Time

### First Upload
- Browser opens automatically
- Sign in to YouTube account
- Click "Allow"
- Token saved for future (no login needed again)

### If Upload Fails
- Video STILL saved locally
- You can retry upload later
- Check `output/videos/` folder

## 🆘 Troubleshooting

### "Python not found"
```powershell
# Check Python is installed
python --version

# If not, download from python.org
```

### "Module not found"
```powershell
pip install -r requirements.txt
```

### "YouTube credentials not found"
- See `YOUTUBE_SETUP_INSTRUCTIONS.md`
- You need `client_secrets.json` from Google Cloud

### GUI won't open
```powershell
# Allow PowerShell scripts
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Bypass

# Then try again
.\scarify_launcher.ps1
```

### Video generation fails
- Check internet connection (needs Pexels API)
- Verify audio is working (Windows TTS)
- Try test mode first: `--count 1 --test`

## 📚 Full Documentation

- **README_YOUTUBE_UPLOAD.md** - Complete system overview
- **YOUTUBE_SETUP_INSTRUCTIONS.md** - YouTube API setup (detailed)
- **test_setup.ps1** - Verify your setup
- **requirements.txt** - Python dependencies

## 🎯 Typical Workflow

### Daily Routine

**Morning:**
```powershell
# Generate 20 videos for the day
python scarify_master.py --count 20 --upload
```

**Or use GUI:**
1. Double-click "SCARIFY Generator" 
2. Click "💥 Generate 20 Videos + Upload"
3. Get coffee ☕
4. Come back to 20 uploaded videos!

**Afternoon:**
- Check YouTube Studio for views
- Monitor which pain points perform best

**Evening:**
- Generate more if needed (watch 50/day limit)

## ✅ Checklist

**Before first run:**
- [ ] Ran `test_setup.ps1`
- [ ] Installed requirements: `pip install -r requirements.txt`
- [ ] Tested generation: `python scarify_master.py --count 1 --test`
- [ ] Created desktop shortcut: `.\create_desktop_shortcut.ps1`

**For YouTube upload:**
- [ ] Set up Google Cloud project
- [ ] Enabled YouTube Data API v3
- [ ] Downloaded `client_secrets.json`
- [ ] Saved to `config/credentials/youtube/`
- [ ] Tested authentication: `python youtube_uploader.py --test-auth`
- [ ] Uploaded test video: `python scarify_master.py --count 1 --upload`

## 🚀 You're Ready!

Everything is set up and ready to go:

```powershell
# Quick test
python scarify_master.py --count 1 --test

# First real upload
python scarify_master.py --count 1 --upload

# Full batch
python scarify_master.py --count 20 --upload
```

Or just double-click the desktop icon! 🔥

---

**Questions?**
- Check `README_YOUTUBE_UPLOAD.md` for details
- See `YOUTUBE_SETUP_INSTRUCTIONS.md` for YouTube setup
- Run `.\test_setup.ps1` to diagnose issues

**Happy creating! 🎬**

