# 📱 ABRAHAM STUDIO - iPhone Mobile Access Guide

## Quick Start

### Step 1: Start Web Server on Laptop
```powershell
.\START_WEB_SERVER.ps1
```

Or directly:
```bash
python STUDIO_WEB_SERVER.py
```

### Step 2: Find Your IP Address
The script will show your IP, or manually:
```powershell
ipconfig | findstr IPv4
```

### Step 3: Access from iPhone
1. Make sure iPhone is on **same WiFi network** as laptop
2. Open Safari or Chrome on iPhone
3. Go to: `http://[YOUR_IP]:5000`
   - Example: `http://192.168.1.100:5000`

## Features Available on Mobile

✅ **Region Selection** - 10 regions (USA, Spain, Mexico, UK, Brazil, Germany, etc.)
✅ **Batch Generation** - 1-50 videos
✅ **Engine Selection** - Stability AI / Pollo AI
✅ **Adult Gore Mode** - Toggle hardcore scripts
✅ **Real-time Progress** - See generation status
✅ **Live Logs** - Watch generation in real-time
✅ **Download Videos** - Download completed videos to iPhone

## Requirements

- Laptop must be running (web server active)
- iPhone and laptop on same WiFi network
- Flask installed: `pip install flask flask-cors`

## Troubleshooting

### Can't Access from iPhone
1. Check firewall - allow port 5000
2. Verify same WiFi network
3. Try laptop's IP instead of localhost
4. Check Windows Firewall settings

### Server Won't Start
```bash
pip install flask flask-cors
python STUDIO_WEB_SERVER.py
```

### Videos Not Generating
- Check API keys in ABRAHAM_STUDIO file
- Verify FFmpeg installed
- Check internet connection

## Alternative: Use SSH/VNC

If web interface doesn't work, you can use:
- **SSH**: `ssh user@your-ip` (if SSH enabled)
- **VNC**: Remote desktop to laptop
- **TeamViewer**: Remote control app
- **Chrome Remote Desktop**: Browser-based remote access

## Security Note

⚠️ The web server runs on `0.0.0.0` (all interfaces) for mobile access.
Make sure you're on a trusted network!

For security, you can:
- Only allow on local network
- Add authentication
- Use VPN





