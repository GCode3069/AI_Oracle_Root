# 🔥 CHAPMAN 2025 YOUTUBE AUTO-UPLOAD SYSTEM

Complete system for generating fear-targeted Abraham Lincoln videos and auto-uploading to YouTube.

## ✅ Features

- **Chapman 2025 Fear Targeting**: Uses top 5 fears (69%, 59%, 58%, 55%, 52% prevalence)
- **Your Image Generation API**: Integrates with your image generation app
- **YouTube Auto-Upload**: Direct upload to your channel
- **15s Shorts Optimized**: Perfect for YouTube Shorts algorithm
- **Train/Rail Theme**: Matches FarFromWeakFFW channel aesthetic
- **Proper Lincoln Voice**: Deep male voice (no more female voices)
- **Retention Hooks**: Psychological triggers from Chapman survey

## 🎯 Targeted Fears

1. **Corrupt Government Officials** (69% prevalence)
   - Prompt: "Lincoln: The whistle's bribes, not arrivals..."
   - Visual: Redacted files burning
   - Hook: "Your audit starts at dawn"

2. **Loved Ones Dying** (59% prevalence)
   - Prompt: "Lincoln: Your family's on the next car..."
   - Visual: Fog cemetery rails
   - Hook: "Mom's next... check the news"

3. **Economic Collapse** (58% prevalence)
   - Prompt: "Lincoln: Your 401K derails at dawn..."
   - Visual: Endless IOU train cars
   - Hook: "Your debt's eternal"

4. **Cyber Terrorism** (55% prevalence)
   - Prompt: "Lincoln: They hacked the rails..."
   - Visual: Glitch screen train
   - Hook: "Your password's on the manifest"

5. **Russia Nuclear Attack** (52% prevalence)
   - Prompt: "Lincoln: The mushroom cloud blooms..."
   - Visual: Nuclear fog rails
   - Hook: "Your shelter's a lie"

## 🚀 Quick Start

### 1. Configure Image API

Edit `CHAPMAN_2025_YOUTUBE_AUTO.py`:
```python
IMAGE_API_URL = "https://api.yourapp.com/generate"
IMAGE_API_KEY = "your_key_here"
```

### 2. Set Up YouTube Auth

First run will open browser for OAuth:
- Authorize YouTube access
- Token saved to `youtube_token.pickle`
- Subsequent runs use saved token

### 3. Generate & Upload

```powershell
.\LAUNCH_CHAPMAN_YOUTUBE.ps1 -Count 10
```

This will:
1. Select random fear (weighted by prevalence)
2. Generate script using Chapman prompt
3. Call your image generation API
4. Generate Lincoln voice audio
5. Create 15s Shorts video
6. Auto-upload to YouTube
7. Return YouTube URL

## 📊 Video Specifications

- **Duration**: 15 seconds (Shorts optimized)
- **Resolution**: 1080x1920 (vertical)
- **FPS**: 24
- **Color Grade**: Silver bleed red (from Chapman specs)
- **Audio**: Theta frequencies + gamma spikes
- **Text Overlay**: Retention hook at end

## 💰 Monetization

Each video includes:
- Bitcoin address: `bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt`
- Call to action
- Retention hooks
- Fear-specific targeting

## 🔧 Files

- `CHAPMAN_2025_YOUTUBE_AUTO.py` - Main generator
- `LAUNCH_CHAPMAN_YOUTUBE.ps1` - PowerShell launcher
- `IMAGE_API_SETUP.md` - API configuration guide
- `CHAPMAN_COMPLETE_README.md` - This file

## 📈 Expected Results

Based on Chapman 2025 specs:
- **Target Views**: 500K per deployment cycle
- **CPM**: $15 USD (Halloween spike)
- **Revenue**: $7.5K ad revenue + $2.5K superchat
- **BTC Donations**: 0.1 BTC total (~$10K at $100K/BTC)

## ⚠️ Troubleshooting

### Image API Not Working
- Check API endpoint and key
- Script falls back to auto-generated images
- Videos still create successfully

### YouTube Upload Fails
- Check OAuth credentials
- Token may need refresh (delete `youtube_token.pickle`)
- Verify channel permissions

### Voice Generation Fails
- Check ElevenLabs API key
- Script tries 3 different voices automatically
- Falls back gracefully

## ✅ Checklist

- [ ] Image API configured
- [ ] YouTube OAuth completed (first run)
- [ ] Test with 1 video
- [ ] Verify YouTube upload
- [ ] Check video quality
- [ ] Scale to batch generation

---

**Ready to generate fear-targeted viral content and auto-upload to YouTube!** 🔥


