# SCARIFY Halloween Overlord

**72-Hour Psychological Operation for $10K Revenue Generation**

## Overview

SCARIFY Halloween Overlord combines immediate revenue generation with long-term psychological warfare content deployment across 15 YouTube channels. The system targets Chapman 2025 Survey fears using Lincoln's ghost train narrative for maximum viral potential.

## Features

- **15-Channel Deployment**: Automated content distribution across multiple YouTube channels
- **Chapman 2025 Fear Targeting**: Leverages top 5 American fears (corrupt government 69%, loved ones dying 59%, economic collapse 58%, cyber terrorism 55%, Russia nukes 52%)
- **Lincoln's Ghost Train Narrative**: Unique psychological anchor for viral content
- **Audio Warfare**: 4-8Hz theta waves + 40Hz gamma spikes for maximum retention
- **BTC Revenue Integration**: Direct donation pipeline with QR code overlays
- **Multi-Platform Deployment**: YouTube Shorts + X/Twitter flooding

## Quick Start

### Prerequisites

- Python 3.8+
- FFmpeg (optional but recommended)
- YouTube OAuth credentials
- ElevenLabs API key (optional)

### Installation

```powershell
# Navigate to project directory
cd scarify-halloween-2025

# Run test mode
.\scarify_halloween_overlord.ps1 -TestMode

# Run full blitzkrieg
.\scarify_halloween_overlord.ps1 -Duration 72
```

### Test Single Clip Generation

```powershell
python scripts/scarify_blitz.py --test --fear corrupt_gov
```

## Configuration

### Chapman 2025 Fears

Edit `configs/chapman_2025.yaml` to customize:
- Fear prompts and narratives
- Audio specifications (theta/gamma frequencies)
- Visual effects parameters
- Revenue projections

### YouTube Channels

Edit `accounts/channels.yaml` to configure:
- 15 channel accounts with OAuth tokens
- Proxy rotation settings
- Upload strategy and timing
- Daily limits and archetype assignments

## Architecture

### Content Generation Pipeline

1. **Fear Selection**: Rotate through Chapman 2025 top fears
2. **Visual Generation**: Black background + text overlays + color grading
3. **Audio Engineering**: Theta rattle + TTS whisper + gamma spikes
4. **Composition**: MoviePy compositing with psychological timing
5. **Export**: 1080x1920 vertical MP4 optimized for Shorts

### Deployment Strategy

- **5 clips/hour** across 15 channels
- **Staggered uploads** (23-minute intervals)
- **Proxy rotation** every 5 minutes
- **View threshold monitoring** (500 views/12 hours)
- **Auto-pruning** of underperforming channels

### Revenue Streams

1. **YouTube Ad Revenue**: $7,500 target (500K views @ $15 CPM)
2. **Superchats**: $2,500 target ($1-5 fear confessions)
3. **BTC Donations**: 0.1 BTC target (50 donations @ 0.0005 BTC)
4. **Total**: $10K+ in 72 hours

## Usage Examples

### Generate Single Clip

```bash
python scripts/scarify_blitz.py --gen-only --fear economic_collapse
```

### Test Mode (No Upload)

```powershell
.\scarify_halloween_overlord.ps1 -TestMode
```

### Generation Only (No Upload)

```powershell
.\scarify_halloween_overlord.ps1 -GenOnly
```

### Full 72-Hour Blitzkrieg

```powershell
.\scarify_halloween_overlord.ps1 -Duration 72
```

## File Structure

```
scarify-halloween-2025/
├── configs/
│   └── chapman_2025.yaml          # Fear configuration
├── accounts/
│   └── channels.yaml               # 15 YouTube channels
├── scripts/
│   └── scarify_blitz.py           # Main generation script
├── audio/
│   └── heartbeat_rattle.wav       # Theta audio base
├── assets/
│   └── (video assets)             # Base footage
├── outputs/
│   └── (generated clips)          # Export directory
├── scarify_halloween_overlord.ps1 # Main execution script
└── README.md                       # This file
```

## Advanced Configuration

### Audio Engineering

- **Theta Waves**: 4-8Hz for freeze-gut paralysis
- **Gamma Spikes**: 40Hz at 7-second mark for BDNF hijack
- **TTS Integration**: ElevenLabs with emotion tuning
- **Subliminal Embedding**: Reversed whispers at key frames

### Visual Effects

- **Color Grading**: Silver-bleed-red LUT
- **Glitch Timing**: 13-second mark for maximum impact
- **Freeze Frames**: 2-second duration on key imagery
- **Text Overlays**: Fear prompts with retention hooks

### Upload Optimization

- **Metadata**: Fear-optimized titles and descriptions
- **Tags**: Halloween + psychological + cognitohazard
- **Thumbnails**: Auto-generated from freeze frames
- **Timing**: Staggered for algorithm optimization

## Monitoring & Analytics

### View Tracking

- Monitor views/hour per clip
- Auto-prune channels <500 views in 12 hours
- A/B test fear types (50% corrupt_gov, 30% loved_ones, 20% economic)

### Revenue Tracking

- Gumroad sales dashboard
- YouTube analytics integration
- BTC wallet monitoring
- Real-time projections

## Troubleshooting

### MoviePy Errors

```bash
pip install --upgrade moviepy
```

### FFmpeg Not Found

Download from: https://ffmpeg.org/download.html

### YouTube Upload Fails

1. Check OAuth token validity
2. Verify API quota limits
3. Test proxy connectivity
4. Review channel daily limits

### Audio Generation Issues

- Fallback to silent audio placeholders
- Check ElevenLabs API key
- Verify audio file permissions

## Safety & Ethics

⚠️ **Warning**: This system generates psychological content designed for maximum engagement. Use responsibly and in compliance with platform guidelines.

- Respect YouTube Community Guidelines
- Avoid genuinely harmful content
- Monitor audience reactions
- Provide mental health resources in descriptions

## License

Proprietary - SCARIFY System

## Support

For issues or questions, review logs in `outputs/overlord_*.log`

---

**SCARIFY Halloween Overlord** - Psychological Warfare Content Generation System
*$10K in 72 Hours via Fear-Driven Viral Content*

