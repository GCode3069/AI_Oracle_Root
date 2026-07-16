# SUBLIMINAL_AUDIO.py
import subprocess
from pathlib import Path

def mix_subliminal_audio(voice_path, output_path):
    """Mix voice with subliminal audio layers using FFmpeg"""
    print(f"🎧 Adding subliminal audio...")
    
    # FFmpeg command: mix voice (0dB) with generated tones
    cmd = [
        'ffmpeg', '-y',
        '-i', voice_path,
        '-f', 'lavfi', '-i', f'sine=frequency=10:duration=30',  # 10Hz binaural
        '-f', 'lavfi', '-i', f'sine=frequency=528:duration=30',  # 528Hz attention
        '-f', 'lavfi', '-i', f'anoisesrc=duration=30:colour=white',  # VHS hiss
        '-filter_complex',
        '[0:a]volume=1.0[v];[1:a]volume=0.1[b];[2:a]volume=0.05[a];[3:a]volume=0.03[h];[v][b][a][h]amix=inputs=4[out]',
        '-map', '[out]',
        output_path
    ]
    
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"✅ Subliminal audio mixed: {output_path}")
    return output_path
