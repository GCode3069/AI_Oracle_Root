# 🚀 SCARIFY Setup Guide

Complete setup instructions for the SCARIFY multi-platform content automation system.

## 📋 Prerequisites

- Python 3.10 or higher
- FFmpeg installed and in PATH
- API keys for:
  - ElevenLabs (TTS)
  - Stability AI (Image generation)
  - Anthropic Claude (Script generation)
  - Google Cloud (YouTube API - optional)

## 🔧 Installation Steps

### 1. Install Python Dependencies

```bash
cd /workspace  # or F:\AI_Oracle_Root\scarify on Windows
pip install -r requirements.txt
```

### 2. Install Playwright Browsers (for TikTok automation)

```bash
playwright install
```

### 3. Verify FFmpeg Installation

```bash
ffmpeg -version
```

If not installed:
- **Windows:** Download from https://ffmpeg.org/download.html
- **Linux:** `sudo apt-get install ffmpeg`
- **macOS:** `brew install ffmpeg`

### 4. Configure API Keys

Create `config/api_config.json`:

```json
{
  "elevenlabs_api_key": "YOUR_ELEVENLABS_KEY",
  "stability_api_key": "YOUR_STABILITY_KEY",
  "anthropic_api_key": "YOUR_ANTHROPIC_KEY",
  "openai_api_key": "YOUR_OPENAI_KEY"
}
```

Or set environment variables:

```bash
export ELEVENLABS_API_KEY="your_key"
export STABILITY_API_KEY="your_key"
export ANTHROPIC_API_KEY="your_key"
```

### 5. YouTube API Setup (Optional)

1. Go to https://console.cloud.google.com/
2. Create a new project
3. Enable YouTube Data API v3
4. Create OAuth 2.0 credentials (Desktop app)
5. Download `client_secrets.json`
6. Save to `config/credentials/youtube/client_secrets.json`

### 6. TikTok Setup (First Time)

1. Run TikTok uploader (will prompt for manual login):
```bash
python TIKTOK_AUTOMATION_SYSTEM.py --upload video.mp4 --topic "Business Horror"
```

2. Log in manually when browser opens
3. Cookies will be saved for future uploads

## 🎬 Usage Examples

### Generate Single Video

```bash
# Generate video only
python ABE_MASTER_GENERATOR.py --topic "Corporate Horror"

# Generate + Upload to YouTube
python ABE_MASTER_GENERATOR.py --topic "Business Nightmare" --youtube

# Generate + Upload to TikTok
python ABE_MASTER_GENERATOR.py --topic "Corporate Greed" --tiktok

# Generate + Upload to Both
python ABE_MASTER_GENERATOR.py --topic "Profit Over People" --both
```

### Batch Generation

```bash
# Generate 10 videos
python ABE_MASTER_GENERATOR.py --batch 10

# Generate 5 videos and upload to both platforms
python ABE_MASTER_GENERATOR.py --batch 5 --both
```

### TikTok-Specific Operations

```bash
# Optimize existing video for TikTok
python TIKTOK_AUTOMATION_SYSTEM.py --optimize video.mp4

# Upload optimized video
python TIKTOK_AUTOMATION_SYSTEM.py --upload tiktok_content/ready_to_upload/video.mp4 --topic "Business Horror"

# Full pipeline (optimize + upload)
python TIKTOK_AUTOMATION_SYSTEM.py --full video.mp4 --topic "Corporate Nightmare"

# Batch process directory
python TIKTOK_AUTOMATION_SYSTEM.py --batch ./videos --limit 5
```

### YouTube Upload

```bash
# Test authentication
python upload/youtube_upload_enhanced.py --test-auth

# Upload video
python upload/youtube_upload_enhanced.py video.mp4 --title "My Video Title" --description "Description" --tags shorts viral
```

## 📁 Directory Structure

```
/workspace/
├── ABE_MASTER_GENERATOR.py          # Master generator
├── TIKTOK_AUTOMATION_SYSTEM.py      # TikTok automation
├── upload/
│   └── youtube_upload_enhanced.py   # YouTube uploader
├── abraham_horror/
│   ├── generated_videos/            # YouTube videos
│   ├── audio/                       # Generated audio files
│   └── images/                      # Generated images
├── tiktok_content/
│   ├── ready_to_upload/             # Optimized TikTok videos
│   ├── uploaded/                    # Posted videos
│   └── analytics/                    # Performance tracking
└── config/
    ├── api_config.json              # API keys
    └── credentials/
        └── youtube/
            └── client_secrets.json  # YouTube OAuth
```

## 🔍 Troubleshooting

### FFmpeg Timeout Issues

**Problem:** FFmpeg times out when processing large images

**Solution:** Images are automatically optimized before video creation. If issues persist:
- Check image file size (should be < 5MB)
- Ensure FFmpeg is latest version
- Check available disk space

### YouTube Upload Fails

**Problem:** YouTube upload returns errors

**Solution:**
1. Check credentials: `python upload/youtube_upload_enhanced.py --test-auth`
2. Verify API quota not exceeded
3. Check video file size (< 256MB)
4. Manual upload instructions will be generated as fallback

### TikTok Login Issues

**Problem:** TikTok uploader can't log in

**Solution:**
1. Run uploader with `headless=False` (visible browser)
2. Log in manually first time
3. Cookies will be saved automatically
4. Subsequent uploads will be automated

### Playwright Not Found

**Problem:** `playwright` command not found

**Solution:**
```bash
pip install playwright
playwright install
```

### Module Import Errors

**Problem:** `ModuleNotFoundError` when running scripts

**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

## ✅ Verification Checklist

- [ ] Python 3.10+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] FFmpeg installed and in PATH
- [ ] Playwright browsers installed (`playwright install`)
- [ ] API keys configured (`config/api_config.json`)
- [ ] YouTube credentials set up (if using YouTube upload)
- [ ] Tested single video generation
- [ ] Tested TikTok optimization
- [ ] Tested YouTube upload (if using)

## 🎯 Next Steps

1. **Generate Test Video:**
   ```bash
   python ABE_MASTER_GENERATOR.py --topic "Test Video"
   ```

2. **Optimize for TikTok:**
   ```bash
   python TIKTOK_AUTOMATION_SYSTEM.py --optimize abraham_horror/generated_videos/ABRAHAM_*.mp4
   ```

3. **Upload to TikTok:**
   ```bash
   python TIKTOK_AUTOMATION_SYSTEM.py --upload tiktok_content/ready_to_upload/*.mp4 --topic "Business Horror"
   ```

4. **Scale Production:**
   ```bash
   python ABE_MASTER_GENERATOR.py --batch 10 --both
   ```

## 📊 System Status

View the complete system map:
- Open `SYSTEM_MAP.html` in your browser
- Or visit: `http://localhost:8000/SYSTEM_MAP.html` (if running local server)

## 🆘 Support

For issues or questions:
1. Check `SYSTEM_MAP.html` for system overview
2. Review error messages in console output
3. Check log files in `tiktok_content/analytics/`
4. Verify all prerequisites are met

---

**Status:** ✅ Production Ready
**Last Updated:** 2025-01-XX
