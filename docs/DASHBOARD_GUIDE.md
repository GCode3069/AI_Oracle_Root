# SCARIFY Dashboard Documentation

## 🚀 Desktop Dashboard Overview

The SCARIFY Dashboard is a comprehensive control center for managing your YouTube Shorts automation empire. It provides advanced batch operations, real-time monitoring, and system controls.

## 📊 Dashboard Features

### Batch Operations Panel (Left Side)
- **🧪 Test (1 Video)** - Generate 1 test video without upload
- **⚡ Small Batch (5)** - Generate 5 videos + upload to YouTube
- **🚀 Medium Batch (10)** - Generate 10 videos + upload to YouTube  
- **💥 Large Batch (20)** - Generate 20 videos + upload to YouTube
- **🔥 MAX BATCH (50)** - Generate 50 videos + upload to YouTube (daily limit)

### Custom Batch Controls
- **Custom Batch Size** - Set any number from 1-100 videos
- **Upload Toggle** - Choose whether to upload to YouTube or save locally
- **Run Custom** - Execute your custom batch configuration

### System Controls
- **📁 Open Videos** - Open the output folder in Windows Explorer
- **🔐 Test YouTube** - Test YouTube authentication and API connection
- **⚙️ Run Setup** - Launch the system setup verification script

### Status & Monitoring Panel (Right Side)
- **Real-time Status** - Live updates on system operations
- **Today's Statistics** - Video count, file sizes, quota usage
- **Progress Tracking** - Visual progress bars and status messages
- **Activity Log** - Detailed log of all operations

## 🎯 How to Use

### Quick Start
1. **Double-click** "SCARIFY Generator" desktop icon
2. **Choose** "🚀 FULL DASHBOARD" from the menu
3. **Click** any batch button to start generating videos
4. **Monitor** progress in the status panel

### Batch Operations
- **Test Mode**: Click "🧪 Test (1 Video)" for safe testing
- **Small Batches**: Use "⚡ Small Batch (5)" for daily content
- **Large Batches**: Use "💥 Large Batch (20)" for bulk creation
- **Custom**: Set your own batch size and upload preferences

### Monitoring
- **Status Box**: Shows real-time operation updates
- **Statistics**: Displays today's video count and file sizes
- **Progress Bar**: Visual indicator during batch operations
- **Refresh**: Click "🔄 Refresh" to update statistics

## ⚙️ System Requirements

- **Python 3.10+** installed
- **All dependencies** from requirements.txt installed
- **YouTube API credentials** configured (for uploads)
- **Internet connection** (for Pexels API)

## 🔧 Troubleshooting

### Dashboard Won't Open
```powershell
# Allow PowerShell scripts
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Bypass

# Run manually
.\scarify_dashboard.ps1
```

### Batch Operations Fail
- Check Python installation: `python --version`
- Install dependencies: `pip install -r requirements.txt`
- Run setup verification: `.\test_setup.ps1`

### YouTube Upload Issues
- Test authentication: Click "🔐 Test YouTube"
- Check credentials: `config/credentials/youtube/client_secrets.json`
- Verify quota: YouTube allows ~50 uploads/day

## 📈 Best Practices

### Daily Workflow
1. **Morning**: Run "⚡ Small Batch (5)" for daily content
2. **Afternoon**: Monitor YouTube Studio for performance
3. **Evening**: Run "💥 Large Batch (20)" if needed (watch quota)

### Batch Sizes
- **1-5 videos**: Quick content for testing
- **10-20 videos**: Standard daily production
- **50 videos**: Maximum daily batch (quota limit)

### Monitoring
- **Check status** regularly during batch operations
- **Monitor quota** to avoid hitting YouTube limits
- **Review statistics** to track daily production

## 🎬 Output Information

### Video Specifications
- **Duration**: 50 seconds
- **Format**: Vertical MP4 (1080x1920)
- **Audio**: Windows TTS narration
- **Content**: Pexels stock footage + pain point scripts

### File Locations
- **Videos**: `output/videos/`
- **Audio**: `output/audio/`
- **Logs**: `logs/`

### YouTube Uploads
- **Title Format**: "SCARIFY: {pain_point} - Ex-Vet $97 Kit"
- **Category**: People & Blogs (22)
- **Privacy**: Public
- **Tags**: shorts, business, entrepreneur, small business

## 🚀 Advanced Features

### Custom Batch Configuration
- Set any batch size from 1-100 videos
- Toggle YouTube upload on/off
- Real-time progress monitoring
- Automatic error handling

### System Integration
- Direct access to output folders
- YouTube authentication testing
- Setup verification tools
- Statistics tracking

### Monitoring & Logging
- Real-time status updates
- Detailed operation logs
- Progress tracking
- Error reporting

## 📞 Support

### Quick Help
- **Setup Issues**: Run `.\test_setup.ps1`
- **YouTube Issues**: Click "🔐 Test YouTube" in dashboard
- **Batch Problems**: Check status panel for error messages

### Documentation
- **QUICKSTART.md** - Basic setup guide
- **README_YOUTUBE_UPLOAD.md** - Complete system overview
- **YOUTUBE_SETUP_INSTRUCTIONS.md** - YouTube API setup

---

**The SCARIFY Dashboard is your command center for YouTube Shorts automation. Use it to efficiently manage batch operations, monitor system status, and scale your content creation empire!** 🔥
