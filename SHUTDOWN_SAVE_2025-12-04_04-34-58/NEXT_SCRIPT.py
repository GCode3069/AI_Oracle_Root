# VIDEO_LAYOUT.py
# THIS IS SCRIPT #5 - CREATE THIS NEXT!
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


# TO CREATE THIS FILE IN THE MORNING:
# Just ask Claude: "Create VIDEO_LAYOUT.py from NEXT_SCRIPT.py"
