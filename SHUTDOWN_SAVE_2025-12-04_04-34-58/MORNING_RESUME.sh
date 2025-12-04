#!/bin/bash
# SCARIFY - MORNING RESUME
# Run this when you wake up!

echo ""
echo "🌅 GOOD MORNING! LET'S FINISH SCARIFY!"
echo ""
echo "📊 STATUS:"
echo "  ✅ 4 of 6 scripts complete (67%)"
echo "  ⏳ 2 scripts remaining (30 minutes)"
echo ""
echo "🎯 NEXT STEPS:"
echo "  1. Create VIDEO_LAYOUT.py (15 min)"
echo "  2. Create SCARIFY_COMPLETE.py (15 min)"
echo "  3. Test system (10 min)"
echo "  4. Generate first video! (5 min)"
echo ""
echo "💪 TOTAL TIME: 45 minutes to working system!"
echo ""
echo "📋 TELL CLAUDE:"
echo ""
echo "Create VIDEO_LAYOUT.py with this code:"
echo ""
cat << 'EOF'
# VIDEO_LAYOUT.py
import subprocess
from pathlib import Path

def create_pip_layout(video_path, title, output_path):
    """Create 1080x1920 picture-in-picture with title"""
    print(f"📺 Creating picture-in-picture layout...")
    
    cmd = [
        'ffmpeg', '-y',
        '-i', video_path,
        '-vf',
        (
            "scale=720:1280,pad=1080:1920:(1080-720)/2:320:black,"
            f"drawtext=text='{title}':fontsize=44:fontcolor=white:"
            "x=(w-text_w)/2:y=50:box=1:boxcolor=black@0.6:boxborderw=10"
        ),
        output_path
    ]
    
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"✅ Layout created: {output_path}")
    return output_path
EOF
echo ""
echo "🚀 THEN ASK FOR SCRIPT 6 (SCARIFY_COMPLETE.py)!"
echo ""
