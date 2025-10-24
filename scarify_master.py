#!/usr/bin/env python3
import argparse
import os
import sys
import time
from pathlib import Path

# Optional .env loader
try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

# Prefer ElevenLabs helper if available
try:
    from scarify.elevenlabs_config import generate_elevenlabs_tts as eleven_tts
    HAVE_ELEVEN = True
except Exception:
    HAVE_ELEVEN = False
    eleven_tts = None


def ensure_output_dirs() -> dict:
    repo_root = Path(__file__).resolve().parent
    base_out = repo_root / "scarify" / "Output"
    yt_dir = base_out / "YouTubeReady"
    tmp_dir = base_out / "Temp"
    yt_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir.mkdir(parents=True, exist_ok=True)
    return {"repo_root": repo_root, "yt": yt_dir, "tmp": tmp_dir}


def try_elevenlabs_tts(text: str, out_audio: Path, voice: str) -> bool:
    if not HAVE_ELEVEN or eleven_tts is None:
        return False
    try:
        return bool(eleven_tts(text, str(out_audio), voice=voice))
    except Exception:
        return False


def try_gtts(text: str, out_audio: Path) -> bool:
    try:
        from gtts import gTTS
        tts = gTTS(text)
        out_audio.parent.mkdir(parents=True, exist_ok=True)
        tts.save(str(out_audio))
        return True
    except Exception:
        return False


def write_silent_wav(duration_sec: int, out_audio: Path) -> bool:
    try:
        import numpy as np
        import soundfile as sf
        sr = 22050
        num_samples = int(sr * max(1, duration_sec))
        data = np.zeros((num_samples,), dtype=np.float32)
        out_audio.parent.mkdir(parents=True, exist_ok=True)
        sf.write(str(out_audio), data, sr)
        return True
    except Exception:
        return False


def build_text(index: int, total: int, theme: str, test: bool) -> str:
    base = f"SCARIFY Transmission {index}/{total}. Theme: {theme}. "
    if test:
        return base + "This is a short test of the pipeline."
    return base + "The Oracle speaks. Systems synchronized. Rendering cinematic sequence."


def compose_video(audio_path: Path, duration: int, out_path: Path) -> None:
    """Compose a simple black video with the given audio using ffmpeg."""
    import subprocess
    out_path.parent.mkdir(parents=True, exist_ok=True)
    # Build ffmpeg command using a black color source and the audio track
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"color=c=black:s=1920x1080:r=24:d={max(1,duration)}",
        "-i", str(audio_path),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-shortest",
        str(out_path)
    ]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.decode("utf-8", errors="ignore")[:4000])


def main(argv=None):
    parser = argparse.ArgumentParser(description="SCARIFY Master generator")
    parser.add_argument("--count", type=int, default=1, help="Number of videos to generate")
    parser.add_argument("--test", action="store_true", help="Generate short test videos")
    parser.add_argument("--duration", type=int, default=45, help="Target duration (seconds)")
    parser.add_argument("--voice", default="jiminex", help="Voice id for ElevenLabs")
    parser.add_argument("--theme", default="tech_mystery", help="Content theme")
    args = parser.parse_args(argv)

    if load_dotenv is not None:
        # Load from repo-local .env first, then default path
        cred_env = Path("config/credentials/.env")
        if cred_env.exists():
            load_dotenv(str(cred_env))
        else:
            load_dotenv()

    paths = ensure_output_dirs()

    total = max(1, args.count)
    for i in range(1, total + 1):
        text = build_text(i, total, args.theme, args.test)
        # Audio targets
        ts = time.strftime("%Y%m%d_%H%M%S")
        tmp_mp3 = paths["tmp"] / f"scarify_audio_{ts}_{i}.mp3"
        tmp_wav = paths["tmp"] / f"scarify_audio_{ts}_{i}.wav"

        print(f"[SCARIFY] Generating audio {i}/{total} ...")
        audio_ok = False
        # 1) ElevenLabs
        if try_elevenlabs_tts(text, tmp_mp3, args.voice):
            audio_path = tmp_mp3
            audio_ok = True
        else:
            # 2) gTTS fallback
            if try_gtts(text, tmp_mp3):
                audio_path = tmp_mp3
                audio_ok = True
            else:
                # 3) Silent WAV fallback
                d = 10 if args.test else args.duration
                if write_silent_wav(d, tmp_wav):
                    audio_path = tmp_wav
                    audio_ok = True
                else:
                    print("[SCARIFY] ERROR: Failed to produce audio; skipping video.")
                    continue

        # Compose video
        print(f"[SCARIFY] Composing video {i}/{total} ...")
        out_name = f"SCARIFY_{'TEST_' if args.test else ''}{ts}_{i}.mp4"
        out_path = paths["yt"] / out_name
        try:
            target_duration = 10 if args.test else args.duration
            compose_video(audio_path, target_duration, out_path)
            print(f"[SCARIFY] ✅ Wrote: {out_path}")
        except Exception as ex:
            print(f"[SCARIFY] ❌ Video composition failed: {ex}")


if __name__ == "__main__":
    main()
