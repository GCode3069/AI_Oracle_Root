# 🔥 SCARIFY Bootstrap - Single File Deployment

## Overview

`scarify_bootstrap.ps1` is a **self-contained, single-file deployment script** that contains everything needed to deploy and run the SCARIFY video generation system. No external dependencies required - everything is embedded inline.

## Features

✅ **Self-Deploying** - Contains all code inline  
✅ **Zero External Dependencies** - Python scripts embedded  
✅ **Automatic Setup** - Creates all directories and configs  
✅ **Prerequisite Checking** - Validates Python, FFmpeg, etc.  
✅ **One-Click Generation** - Can generate videos immediately  
✅ **Full Logging** - Tracks everything to log files  
✅ **Multiple Archetypes** - Rebel, Mystic, Sage, Hero, Guardian  

## Quick Start

### Option 1: Quick Test (No Video Generation)
```powershell
.\scarify_bootstrap.ps1 -QuickTest
```

### Option 2: Generate 1 Test Video
```powershell
.\scarify_bootstrap.ps1 -VideoCount 1 -Archetype "Mystic"
```

### Option 3: Full Deployment + Generate 5 Videos
```powershell
.\scarify_bootstrap.ps1 -VideoCount 5 -FullDeploy
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `-VideoCount` | Integer | 1 | Number of videos to generate |
| `-FullDeploy` | Switch | False | Auto-launch generator after setup |
| `-QuickTest` | Switch | False | Skip video generation (test only) |
| `-Archetype` | String | "Mystic" | Content archetype to use |

## Archetypes

- **Rebel** - Revolutionary, gritty, challenges status quo
- **Mystic** - Ethereal, spiritual, consciousness exploration
- **Sage** - Wisdom, knowledge, contemplative
- **Hero** - Inspirational, courageous, transformational
- **Guardian** - Protective, strong, vigilant

## What Gets Created

```
scarify/
├── output/
│   ├── videos/          # Generated MP4 files
│   ├── audio/           # TTS audio files
│   └── scripts/         # Script text files
├── logs/                # Bootstrap logs
├── config/              # Configuration files
├── assets/              # Asset storage
├── scarify_bootstrap_generator.py  # Embedded Python script
└── requirements_bootstrap.txt      # Python dependencies
```

## Manual Video Generation

After bootstrap, you can generate videos directly:

```bash
# Single video
python scarify_bootstrap_generator.py Mystic 1

# Multiple videos
python scarify_bootstrap_generator.py Rebel 10

# Different archetype
python scarify_bootstrap_generator.py Sage 5
```

## Dependencies

### Required
- **Python 3.8+** - For video generation
- **pip** - For installing packages

### Recommended
- **FFmpeg** - For advanced video processing
- **Internet Connection** - For downloading packages

### Auto-Installed Python Packages
- `gtts` - Text-to-speech
- `moviepy` - Video editing
- `Pillow` - Image processing
- `numpy` - Numerical operations
- `requests` - HTTP requests
- `imageio` - Image/video I/O

## Troubleshooting

### "Python not found"
Install Python 3.8+ from python.org and ensure it's in PATH.

### "FFmpeg not found"
Videos will still generate, but with limited features. Install FFmpeg:
```powershell
winget install ffmpeg
```

### "Package installation failed"
Manually install packages:
```bash
pip install -r requirements_bootstrap.txt
```

### "Video generation failed"
Check logs in `logs/` directory for detailed error messages.

## Advanced Usage

### Custom Root Directory
Edit the script to change `$SCARIFY_ROOT`:
```powershell
$SCARIFY_ROOT = "C:\MyCustomPath\scarify"
```

### Batch Processing
Generate multiple archetypes:
```powershell
foreach ($arch in @("Rebel", "Mystic", "Sage")) {
    python scarify_bootstrap_generator.py $arch 3
}
```

### Scheduled Generation
Use Task Scheduler to run automatically:
```powershell
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" `
    -Argument "-File C:\path\to\scarify_bootstrap.ps1 -VideoCount 5"
$trigger = New-ScheduledTaskTrigger -Daily -At 3am
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "SCARIFY Daily"
```

## Output Examples

### Video Specs
- **Resolution**: 1080x1920 (9:16 vertical)
- **Duration**: 15 seconds
- **FPS**: 24
- **Format**: MP4 (H.264 + AAC)
- **Audio**: TTS narration

### File Naming
```
scarify_Mystic_20251027_143022.mp4
scarify_Rebel_20251027_143045.mp4
scarify_Sage_20251027_143108.mp4
```

## Integration

This bootstrap script can integrate with:
- YouTube upload automation
- Social media posting
- Content scheduling systems
- Analytics platforms

## License

Part of the SCARIFY project. See main project README for details.

## Support

For issues or questions, check:
1. Log files in `logs/` directory
2. Generated files in `output/` directory
3. Configuration in `config/bootstrap_config.json`

---

**Created**: 2025-10-27  
**Version**: 2.0-Bootstrap  
**Status**: Production Ready ✅

