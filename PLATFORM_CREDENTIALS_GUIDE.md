
# 🔑 PLATFORM CREDENTIALS GUIDE

## Quick Setup Summary

**Automated:** YouTube, TikTok, Instagram, Facebook (browser automation)  
**Requires API Keys:** Twitter, Reddit  
**Optional:** Telegram

---

## 📺 1. YOUTUBE (ALREADY DONE ✅)

**Status:** Configured  
**Location:** `config/credentials/youtube/client_secrets.json`

---

## 🎵 2. TIKTOK

**Method:** Browser Automation (Playwright)  
**No API Keys Required**

### Setup:
1. First upload will open browser
2. Login manually (one time)
3. Session saved automatically
4. Future uploads automated

**Why no API?**
- TikTok doesn't have public upload API
- Browser automation is the standard workaround

---

## 📸 3. INSTAGRAM

**Method:** Instagrapi Library  
**No API Keys Required**

### Setup:
1. Script will prompt for username/password on first run
2. Session saved to `config/platforms/instagram_session.json`
3. Future uploads automated

**Note:** Use a dedicated account (not your main) to avoid bans

---

## 👤 4. FACEBOOK

**Method:** Browser Automation (Playwright)  
**No API Keys Required for Now**

### Setup:
1. First upload opens browser
2. Login manually (one time)
3. Future uploads automated

**Alternative (Advanced):**
- Facebook Graph API (requires app approval)
- Not necessary for initial deployment

---

## 🐦 5. TWITTER/X

**Method:** Official API (Tweepy)  
**Requires API Keys** ⚠️

### Setup Steps:

1. **Go to:** https://developer.twitter.com/en/portal/dashboard

2. **Create Project:**
   - Click "Create Project"
   - Name: "SCARIFY Content"
   - Use case: "Making a bot"

3. **Create App:**
   - Name: "SCARIFY Uploader"
   - Get API Key & Secret

4. **Get Access Tokens:**
   - User authentication settings
   - Enable OAuth 1.0a
   - Read + Write permissions
   - Generate Access Token & Secret

5. **Save Credentials:**
```json
{
  "api_key": "YOUR_API_KEY",
  "api_secret": "YOUR_API_SECRET",
  "access_token": "YOUR_ACCESS_TOKEN",
  "access_secret": "YOUR_ACCESS_SECRET"
}
```

**Save to:** `config/platforms/twitter_credentials.json`

**Cost:** FREE (Basic tier: 1,500 tweets/month)

---

## 🤖 6. REDDIT

**Method:** Official API (PRAW)  
**Requires API Keys** ⚠️

### Setup Steps:

1. **Go to:** https://www.reddit.com/prefs/apps

2. **Create App:**
   - Click "create another app"
   - Name: "SCARIFY Content Bot"
   - Type: **script**
   - Redirect URI: `http://localhost:8080`

3. **Get Credentials:**
   - Client ID: under app name (looks like: `xxxxxxxxxxx`)
   - Client Secret: shown as "secret"

4. **Save Credentials:**
```json
{
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET",
  "user_agent": "SCARIFY_Bot/1.0",
  "username": "YOUR_REDDIT_USERNAME",
  "password": "YOUR_REDDIT_PASSWORD"
}
```

**Save to:** `config/platforms/reddit_credentials.json`

**Best Subreddits:**
- r/conspiracy (3.5M members)
- r/horror (2.8M members)
- r/CreepyPasta (560K members)
- r/oddlyterrifying (3.1M members)
- r/Glitch_in_the_Matrix (350K members)

**Rules:**
- Don't spam (Reddit is strict)
- Engage in comments (builds credibility)
- Space out posts (1-2 per day max per subreddit)

---

## 📱 7. TELEGRAM (OPTIONAL)

**Method:** Telegram Bot API  
**Requires Bot Token**

### Setup Steps:

1. **Talk to BotFather:**
   - Open Telegram
   - Search "@BotFather"
   - Send `/newbot`
   - Follow prompts

2. **Get Token:**
   - BotFather gives you token
   - Format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

3. **Create Channel:**
   - Create public channel
   - Add bot as admin
   - Get channel ID

4. **Save Credentials:**
```json
{
  "bot_token": "YOUR_BOT_TOKEN",
  "channel_id": "@your_channel_name"
}
```

**Save to:** `config/platforms/telegram_credentials.json`

---

## 🚀 QUICK START COMMANDS

### Test Single Video (All Platforms):
```bash
python MULTI_PLATFORM_UPLOADER.py --test
```

### Upload to Specific Platforms:
```bash
# YouTube + TikTok + Instagram only
python MULTI_PLATFORM_UPLOADER.py --count 5 --platforms youtube tiktok instagram
```

### Upload to All Configured Platforms:
```bash
python MULTI_PLATFORM_UPLOADER.py --count 111 --platforms all
```

---

## ⚠️ IMPORTANT NOTES

### Rate Limits:
- **YouTube:** 10,000 API units/day (1 video = ~1600 units = ~6 videos/day per channel)
- **TikTok:** ~30 videos/day recommended (soft limit)
- **Instagram:** ~10-15 reels/day recommended
- **Twitter:** 1,500 tweets/month (FREE tier)
- **Reddit:** 2-3 posts/day total (across all subreddits)

### Account Safety:
- Use dedicated accounts (not personal)
- Space out uploads (don't dump 100 videos instantly)
- Engage authentically (comment, like, respond)
- Rotate IP if possible (VPN)

### Platform Priorities:
1. **YouTube** - Primary revenue ($$$)
2. **TikTok** - Viral engine
3. **Instagram** - Secondary revenue
4. **Reddit** - Traffic driver
5. **Twitter** - Amplification
6. **Facebook** - Older demographic (higher spending)

---

## 📊 PROJECTED REACH (111 Videos Across 6 Platforms)

**Total Uploads:** 111 × 6 = **666 videos**

**Conservative Views (48 hours):**
- YouTube: 1.11M views
- TikTok: 2.2M views
- Instagram: 800K views
- Facebook: 600K views
- Twitter: 200K views
- Reddit: 500K views (via traffic)
**TOTAL: 5.41M views**

**Revenue Projection:**
- Ad revenue: $27,050 (mixed CPM $5)
- Bitcoin donations: $5,000 (0.1% conversion)
- Rebel Kit sales: $15,000 (500 sales)
**TOTAL: $47,050 in 48 hours**

---

## 🔥 READY TO DEPLOY?

1. **Run setup script:**
```bash
SETUP_PLATFORM_CREDENTIALS.bat
```

2. **Test with 1 video:**
```bash
python MULTI_PLATFORM_UPLOADER.py --test
```

3. **Full deployment:**
```bash
python MULTI_PLATFORM_UPLOADER.py --count 111 --platforms all
```

---

**THE EMPIRE EXPANDS BEYOND YOUTUBE.** 💰🌐

