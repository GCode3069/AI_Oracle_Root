# YouTube API Setup Instructions for SCARIFY

This guide will help you set up YouTube OAuth 2.0 credentials so SCARIFY can automatically upload videos.

## Overview

To upload videos to YouTube, you need:
1. A Google Cloud project
2. YouTube Data API v3 enabled
3. OAuth 2.0 credentials (client_secrets.json)

## Step-by-Step Setup

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **Select a project** → **NEW PROJECT**
3. Project name: `SCARIFY YouTube Uploader` (or any name)
4. Click **CREATE**
5. Wait for project to be created (notification will appear)

### 2. Enable YouTube Data API v3

1. In your project, go to **APIs & Services** → **Library**
2. Search for: `YouTube Data API v3`
3. Click on **YouTube Data API v3**
4. Click **ENABLE**
5. Wait for API to be enabled

### 3. Configure OAuth Consent Screen

1. Go to **APIs & Services** → **OAuth consent screen**
2. Select **External** (unless you have a Google Workspace account)
3. Click **CREATE**

**Fill in the form:**
- **App name:** `SCARIFY Video Uploader`
- **User support email:** Your email
- **Developer contact email:** Your email
- Click **SAVE AND CONTINUE**

**Scopes:**
- Click **ADD OR REMOVE SCOPES**
- Search for: `youtube.upload`
- Check the box for `https://www.googleapis.com/auth/youtube.upload`
- Click **UPDATE**
- Click **SAVE AND CONTINUE**

**Test users:**
- Click **ADD USERS**
- Enter your YouTube channel email
- Click **ADD**
- Click **SAVE AND CONTINUE**

### 4. Create OAuth 2.0 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **+ CREATE CREDENTIALS** → **OAuth client ID**
3. Application type: **Desktop app**
4. Name: `SCARIFY Desktop Client`
5. Click **CREATE**
6. Click **DOWNLOAD JSON** on the popup
7. Save the file as `client_secrets.json`

### 5. Install the Credentials File

**Save the downloaded file to:**
```
F:\AI_Oracle_Root\scarify\config\credentials\youtube\client_secrets.json
```

**Full path structure:**
```
scarify/
├── config/
│   └── credentials/
│       └── youtube/
│           └── client_secrets.json  ← Put your file here
├── scarify_master.py
├── youtube_uploader.py
└── ...
```

### 6. First Authentication

The first time you run SCARIFY with `--upload`, it will:

1. Open your web browser automatically
2. Ask you to sign in to your Google/YouTube account
3. Show a consent screen asking for permission
4. Click **Continue** and **Allow**
5. You'll see "Authentication successful! You can close this window."

**After first authentication:**
- A `token.pickle` file is created
- You won't need to authenticate again (unless token expires)
- The token is saved in: `config/credentials/youtube/token.pickle`

## Testing Your Setup

### Test Authentication Only
```powershell
python youtube_uploader.py --test-auth
```

This will verify your credentials without uploading any videos.

### Test Upload
```powershell
python scarify_master.py --count 1 --test
python youtube_uploader.py output\videos\scarify_XXXXXXXX_XXXXXX.mp4 --pain-point "Test upload"
```

### Full Test
```powershell
python scarify_master.py --count 1 --upload
```

## Troubleshooting

### "Client secrets file not found"
- Make sure `client_secrets.json` is in the exact path:
  `F:\AI_Oracle_Root\scarify\config\credentials\youtube\client_secrets.json`
- Check that the file is named exactly `client_secrets.json` (not `client_secret_xxx.json`)

### "Access blocked: This app isn't verified"
- Click **Advanced** → **Go to SCARIFY (unsafe)**
- This warning appears because your app isn't verified by Google
- It's safe to proceed for your own project

### "The OAuth client was deleted"
- Download the credentials file again from Google Cloud Console
- Replace your old `client_secrets.json`

### "Quota exceeded"
- YouTube allows ~50 uploads per day per account
- Wait 24 hours or use a different account
- Check quota: [Google Cloud Console → APIs & Services → Quotas](https://console.cloud.google.com/iam-admin/quotas)

### Browser doesn't open for authentication
- The script will print a URL
- Copy and paste it into your browser manually
- Complete the authentication
- Copy the authorization code back to the terminal

## YouTube Quota Limits

**Daily quotas (per account):**
- **Video uploads:** ~50 per day
- **API quota:** 10,000 units per day
  - One upload = 1,600 units
  - You can do ~6 uploads before hitting the quota

**To increase quota:**
- Apply for quota increase: [YouTube API Services - Audit and Quota Extension Form](https://support.google.com/youtube/contact/yt_api_form)
- Usually approved within 1-2 weeks for legitimate use cases

## Security Notes

**Keep these files PRIVATE:**
- `client_secrets.json` - Your OAuth credentials
- `token.pickle` - Your authentication token

**Never commit to Git:**
- Both files are already in `.gitignore`
- If exposed, delete them in Google Cloud Console and create new ones

## Need Help?

**Official Documentation:**
- [YouTube Data API Overview](https://developers.google.com/youtube/v3/getting-started)
- [Upload Videos Guide](https://developers.google.com/youtube/v3/guides/uploading_a_video)
- [OAuth 2.0 Setup](https://developers.google.com/youtube/registering_an_application)

**Common Issues:**
- [YouTube API Forum](https://support.google.com/youtube/community)
- [Stack Overflow - YouTube API](https://stackoverflow.com/questions/tagged/youtube-api)

---

## Quick Start Checklist

- [ ] Created Google Cloud project
- [ ] Enabled YouTube Data API v3
- [ ] Configured OAuth consent screen
- [ ] Created OAuth 2.0 credentials
- [ ] Downloaded `client_secrets.json`
- [ ] Saved to: `config/credentials/youtube/client_secrets.json`
- [ ] Ran test authentication: `python youtube_uploader.py --test-auth`
- [ ] Successfully authenticated in browser
- [ ] Tested upload with: `python scarify_master.py --count 1 --upload`

Once all boxes are checked, you're ready to auto-upload videos! 🚀


