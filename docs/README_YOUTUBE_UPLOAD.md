# SCARIFY YouTube Auto-Upload System

Complete YouTube Shorts video generation and auto-upload system.

## ✅ What's Included

### 1. YouTube Uploader (`youtube_uploader.py`)
- OAuth 2.0 authentication
- Automatic upload to YouTube Shorts
- Proper title/description formatting
- Error handling and quota management
- Daily upload tracking (50/day limit)

### 2. Updated Master Script (`scarify_master.py`)
- New `--upload` flag for automatic uploads
- Progress tracking for uploads
- Graceful error handling (videos saved even if upload fails)
- Final summary with YouTube URLs

### 3. GUI Launcher (`scarify_launcher.ps1`)
- Beautiful PowerShell GUI with 3 buttons:
  - **Generate 1 Test** (no upload)
  - **Generate 5 + Upload**
  - **Generate 20 + Upload**
- Real-time progress in separate window
- One-click folder access

### 4. Desktop Shortcut Creator (`create_desktop_shortcut.ps1`)
- Creates desktop icon for easy access
- Launch SCARIFY with one double-click

## 🚀 Quick Start

### First Time Setup

#### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

#### 2. Set Up YouTube API Credentials
**See detailed guide:** `YOUTUBE_SETUP_INSTRUCTIONS.md`

**Quick summary:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project and enable YouTube Data API v3
3. Create OAuth 2.0 credentials (Desktop app)
4. Download `client_secrets.json`
5. Save to: `config/credentials/youtube/client_secrets.json`

#### 3. Create Desktop Shortcut
```powershell
.\create_desktop_shortcut.ps1
```

This creates a "SCARIFY Generator" icon on your desktop.

### Using the GUI (Easiest)

**Double-click** the desktop shortcut or run:
```powershell
.\scarify_launcher.ps1
```

**Three big buttons:**
- 📹 **Generate 1 Test Video** - Test without uploading
- 🚀 **Generate 5 Videos + Upload** - Create and upload 5 videos
- 💥 **Generate 20 Videos + Upload** - Bulk generate 20 videos

### Using Command Line

#### Generate test video (no upload)
```powershell
python scarify_master.py --count 1 --test
```

#### Generate and upload 1 video
```powershell
python scarify_master.py --count 1 --upload
```

#### Generate and upload 5 videos
```powershell
python scarify_master.py --count 5 --upload
```

#### Generate and upload 20 videos
```powershell
python scarify_master.py --count 20 --upload
```

## 📋 File Structure

```
scarify/
├── youtube_uploader.py           # YouTube upload logic
├── scarify_master.py             # Updated main script
├── scarify_launcher.ps1          # GUI launcher
├── create_desktop_shortcut.ps1   # Desktop shortcut creator
├── requirements.txt              # Python dependencies
│
├── config/
│   └── credentials/
│       └── youtube/
│           ├── client_secrets.json    # Your OAuth credentials (you create this)
│           └── token.pickle           # Auto-generated after first auth
│
├── output/
│   ├── audio/                    # Generated audio files
│   └── videos/                   # Generated video files
│
├── audio_generator.py            # Audio generation (Windows TTS)
├── video_generator.py            # Video generation (Pexels)
└── YOUTUBE_SETUP_INSTRUCTIONS.md # Detailed setup guide
```

## 🔑 Authentication Flow

**First time you upload:**
1. Script opens browser automatically
2. Sign in to your YouTube account
3. Click "Allow" on permission screen
4. Done! Token saved for future use

**Subsequent uploads:**
- Uses saved token (no browser needed)
- Token auto-refreshes when expired

## 📊 YouTube Shorts Metadata

### Title Format
```
SCARIFY: {pain_point} - Ex-Vet $97 Kit
```

Example:
```
SCARIFY: Chicago garage supply meltdown – 48hr $50k fix - Ex-Vet $97 Kit
```

### Description Format
```
{full_pain_point}

Ex-vet emergency kit: https://gumroad.com/l/buy-rebel-97

#Shorts #Business #Entrepreneur #SmallBusiness
```

### Video Settings
- **Category:** 22 (People & Blogs)
- **Privacy:** Public
- **Tags:** shorts, business, entrepreneur, small business, startup
- **Format:** Vertical MP4 (1080x1920)
- **Duration:** ~50 seconds

## ⚠️ Quota Limits

**YouTube API Quotas:**
- **Daily uploads:** ~50 videos per day
- **API quota:** 10,000 units/day (1 upload = 1,600 units)

**The script tracks:**
- Upload count per session
- Warns when approaching limits
- Gracefully handles quota errors

**To check your quota:**
[Google Cloud Console → Quotas](https://console.cloud.google.com/iam-admin/quotas)

## 🛠️ Testing

### Test YouTube authentication only
```powershell
python youtube_uploader.py --test-auth
```

### Test single video upload
```powershell
# First generate a video
python scarify_master.py --count 1 --test

# Then test upload
python youtube_uploader.py output\videos\scarify_XXXXXXXX_XXXXXX.mp4 --pain-point "Test"
```

### Full end-to-end test
```powershell
python scarify_master.py --count 1 --upload
```

## 🐛 Troubleshooting

### "YouTube credentials not configured"
- See: `YOUTUBE_SETUP_INSTRUCTIONS.md`
- Make sure `client_secrets.json` is in `config/credentials/youtube/`

### "Authentication failed"
- Delete `token.pickle` and re-authenticate
- Check that YouTube Data API v3 is enabled
- Verify your Google account has YouTube channel access

### "Upload failed"
- Check internet connection
- Verify video file exists and is < 256 MB
- Check YouTube quota hasn't been exceeded
- Video is still saved locally in `output/videos/`

### GUI doesn't open
- Right-click `scarify_launcher.ps1` → Run with PowerShell
- Check PowerShell execution policy: `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Bypass`

### "Client secrets file not found"
- Make sure file is named exactly: `client_secrets.json`
- Check path: `F:\AI_Oracle_Root\scarify\config\credentials\youtube\client_secrets.json`
- Don't rename the downloaded file (some browsers add `(1)` or `.txt`)

## 📈 Typical Workflow

**Daily content creation:**

1. **Morning:** Generate and upload 20 videos
   ```powershell
   python scarify_master.py --count 20 --upload
   ```

2. **Afternoon:** Check YouTube Studio for analytics

3. **Evening:** Generate another batch if needed (watch quota)

**Or use GUI:**
1. Double-click "SCARIFY Generator" on desktop
2. Click "💥 Generate 20 Videos + Upload"
3. Wait for completion
4. Open output folder to verify

## 🔒 Security Notes

**Keep private:**
- `client_secrets.json` - Your OAuth credentials
- `token.pickle` - Your authentication token

**Already in .gitignore:**
- Both files won't be committed to Git
- Safe to work on the project

**If exposed:**
- Delete credentials in Google Cloud Console
- Create new ones
- Replace `client_secrets.json`

## 📞 Support

**Setup issues:**
- See: `YOUTUBE_SETUP_INSTRUCTIONS.md`
- [YouTube API Documentation](https://developers.google.com/youtube/v3)

**Quota increase:**
- [Request form](https://support.google.com/youtube/contact/yt_api_form)
- Usually approved in 1-2 weeks

**API errors:**
- [YouTube API Forum](https://support.google.com/youtube/community)

## ✨ Features

✅ One-click video generation  
✅ Automatic YouTube upload  
✅ OAuth 2.0 authentication  
✅ Quota tracking (50/day)  
✅ Error handling (videos saved if upload fails)  
✅ Progress tracking  
✅ Beautiful GUI  
✅ Desktop shortcut  
✅ Batch processing  
✅ Shorts optimization  

## 🎯 Video Format Specs

**Perfect for YouTube Shorts:**
- Resolution: 1080x1920 (9:16 vertical)
- Duration: ~50 seconds
- Format: MP4 (H.264)
- Audio: Windows TTS or ElevenLabs
- Visuals: Pexels stock footage
- Title: Includes "#Shorts" keyword
- Description: Product link + hashtags

---

## 🚀 Ready to Go!

You now have a complete YouTube auto-upload system:

1. ✅ `youtube_uploader.py` - Upload engine
2. ✅ `scarify_master.py` - Updated with `--upload`
3. ✅ `scarify_launcher.ps1` - Beautiful GUI
4. ✅ Desktop shortcut - One-click access
5. ✅ Complete documentation

**Next steps:**
1. Set up YouTube API credentials (see `YOUTUBE_SETUP_INSTRUCTIONS.md`)
2. Run `create_desktop_shortcut.ps1`
3. Double-click desktop icon
4. Click "📹 Generate 1 Test Video" to verify
5. Click "🚀 Generate 5 Videos + Upload" to go live!

**Happy uploading! 🔥**


