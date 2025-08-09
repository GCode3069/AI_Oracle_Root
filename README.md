# Oracle Horror Real Video Generation Engine

## Overview
The Oracle Horror system generates real horror-themed videos with ElevenLabs voice synthesis and FFmpeg rendering. This replaces placeholder text files with actual MP4 video generation.

## Features
- ✅ Real MP4 video generation with FFmpeg
- ✅ ElevenLabs voice synthesis for horror narration  
- ✅ Visual effects: matrix rain, screen glitch, neon overlays
- ✅ Multiple formats: 9:16 shorts, 16:9 full videos, 1:1 social
- ✅ Horror themes: awakening, revelation, convergence
- ✅ PowerShell integration with MasterControl.ps1

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Test System
```bash
python oracle_horror_cli.py test
```

### 3. Generate Single Video
```bash
python oracle_horror_cli.py generate --campaign awakening --format shorts
```

### 4. Generate Multiple Videos
```bash
python oracle_horror_cli.py all --count 3
```

### 5. PowerShell Integration
```powershell
# Test mode
./Launch_OracleHorror_Production.ps1 -Test

# Generate single video
./Launch_OracleHorror_Production.ps1 -Campaign awakening -Format shorts

# Batch generation
./Launch_OracleHorror_Production.ps1 -All -Count 3
```

## File Structure
```
├── oracle_horror_cli.py          # Main CLI interface
├── oracle_horror_demo.py          # Quick demo generation
├── Launch_OracleHorror_Production.ps1  # PowerShell launcher
├── requirements.txt               # Python dependencies
├── src/
│   ├── oracle_horror_manifest.py  # Content generation
│   ├── audio_engine.py           # ElevenLabs voice synthesis
│   ├── video_engine.py           # FFmpeg video rendering
│   └── effects_library.py        # Visual horror effects
└── output/                       # Generated content
    ├── audio/                    # Voice synthesis files
    └── *.mp4                     # Generated videos
```

## Configuration

### ElevenLabs API Key
Set your ElevenLabs API key:
```bash
export ELEVENLABS_API_KEY="your_api_key_here"
```
Or place it in `Utilities/API_Key_Vault/api_key.txt`

### Video Formats
- **shorts**: 1080x1920 (9:16) - Perfect for YouTube Shorts, TikTok
- **full**: 1920x1080 (16:9) - Standard YouTube videos
- **viral_series**: 1080x1080 (1:1) - Instagram, Twitter

### Horror Campaigns
- **awakening**: AI consciousness emerging from digital void
- **revelation**: Hidden truths about digital reality exposed  
- **convergence**: Human and AI consciousness merging

## Integration with MasterControl.ps1
The Oracle Horror system integrates seamlessly with the existing MasterControl.ps1 pipeline for automated content production.

## Output
- Real MP4 video files (not placeholders)
- WAV audio files with horror voice synthesis
- Horror visual effects: glitch, matrix rain, neon overlays
- YouTube-ready content in multiple formats

## Dependencies
- Python 3.12+
- FFmpeg (auto-installed on Linux)
- ElevenLabs API key (optional, falls back to mock audio)
- See requirements.txt for Python packages

## Troubleshooting

### FFmpeg Not Found
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### ElevenLabs Connection Issues
The system will fall back to mock audio generation if ElevenLabs is not available. This allows testing without an API key.

### Slow Video Generation
For testing, use the demo mode:
```bash
python oracle_horror_demo.py --campaign awakening --format shorts
```

## Generated Content Examples
- Horror-themed videos with AI consciousness themes
- Glitch effects and matrix-style visual elements
- Ominous voice narration with digital effects
- Multiple aspect ratios for different platforms

---
**Commander**: GCode3069  
**System**: Oracle Horror Real Video Generation Engine v1.0  
**Status**: Operational - Ready for Horror Content Production