"""
SCARIFY Advanced Suite (Single Module)
Features:
  - Energy-based highlight shorts extraction
  - FastAPI dashboard (fragments, metrics, retention summary)
  - ElevenLabs voice adapter scaffold
  - Retention scoring heuristic
  - Stego thumbnail extractor
  - Fragment chain reconstruction CLI

Usage (direct CLI):
  python -m scarify.utils.advanced_suite highlight --video path/to/long.mp4 --count 3
  python -m scarify.utils.advanced_suite chain
  python -m scarify.utils.advanced_suite stego --thumbnail scarify/Output/Thumbnails/THUMB_FRG-xxxxxx.png
  python -m scarify.utils.advanced_suite retention --meta scarify/Output/YouTubeReady/SCARIFY_xxx.json
  python -m scarify.utils.advanced_suite dashboard --host 0.0.0.0 --port 8055
  python -m scarify.utils.advanced_suite elevenlabs-test "Sample text"

Integrate in pipeline:
  from scarify.utils.advanced_suite import retention_score, create_highlight_shorts, reconstruct_chain, extract_stego_payload
"""

import os
import json
import math
import time
import uuid
import logging
import asyncio
import subprocess
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional

log = logging.getLogger("advanced_suite")
if not log.handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ---- CONSTANT PATHS ----
STATE_DIR = Path("scarify/state")
OUTPUT_DIR = Path("scarify/Output")
YT_DIR = OUTPUT_DIR / "YouTubeReady"
SHORTS_DIR = OUTPUT_DIR / "ShortsReady"
THUMB_DIR = OUTPUT_DIR / "Thumbnails"
PUZZLE_DIR = OUTPUT_DIR / "Puzzles"
METRICS_FILE = STATE_DIR / "metrics_history.json"
FRAGMENTS_FILE = STATE_DIR / "master_fragments.json"

for _d in (YT_DIR, SHORTS_DIR, THUMB_DIR, PUZZLE_DIR, STATE_DIR):
    _d.mkdir(parents=True, exist_ok=True)


# ================================================================
# 1. ENERGY-BASED HIGHLIGHT SHORTS EXTRACTION
# ================================================================
def _extract_temp_audio(video: Path, tmp_wav: Path) -> bool:
    """Extract mono WAV for analysis."""
    cmd = [
        "ffmpeg", "-y", "-i", str(video),
        "-vn", "-ac", "1", "-ar", "16000", "-f", "wav", str(tmp_wav)
    ]
    r = subprocess.run(cmd, capture_output=True)
    return r.returncode == 0


def _compute_energy_profile(wav_path: Path, frame_ms=500) -> Tuple[List[float], float]:
    """
    Compute RMS energy per frame of size frame_ms.
    Returns (energies, frame_duration_seconds).
    """
    import soundfile as sf
    import numpy as np
    data, sr = sf.read(str(wav_path))
    if data.ndim > 1:
        data = data[:,0]
    frame_len = int(sr * (frame_ms / 1000.0))
    energies = []
    for start in range(0, len(data), frame_len):
        frame = data[start:start+frame_len]
        if len(frame) == 0:
            break
        rms = math.sqrt((frame**2).mean()) if frame.size else 0.0
        energies.append(rms)
    return energies, frame_ms / 1000.0


def detect_highlight_segments(
    video_path: Path,
    target_count: int = 3,
    min_len: int = 8,
    max_len: int = 20
) -> List[Tuple[float, float]]:
    """
    Detect highlight segments based on energy peaks.
    Return list of (start_sec, end_sec).
    """
    tmp_wav = video_path.with_suffix(".analysis.wav")
    if not _extract_temp_audio(video_path, tmp_wav):
        log.error("Audio extraction failed for %s", video_path)
        return []
    energies, frame_sec = _compute_energy_profile(tmp_wav)
    tmp_wav.unlink(missing_ok=True)

    if not energies:
        return []

    import numpy as np
    arr = np.array(energies)
    # Normalize
    norm = (arr - arr.min()) / (arr.ptp() if arr.ptp() else 1.0)
    # Simple peak picking: pick frames above (mean + std*0.6)
    threshold = norm.mean() + norm.std() * 0.6
    candidate_indices = np.where(norm >= threshold)[0]

    if len(candidate_indices) == 0:
        # fallback pick top frames
        candidate_indices = np.argsort(-norm)[:target_count * 3]

    # Merge contiguous indices
    segments = []
    if candidate_indices.size:
        start = candidate_indices[0]
        prev = start
        for idx in candidate_indices[1:]:
            if idx == prev + 1:
                prev = idx
                continue
            segments.append((start, prev))
            start = idx
            prev = idx
        segments.append((start, prev))

    # Convert to time spans, enforce min/max, shrink if needed
    time_segments = []
    for s, e in segments:
        seg_start = s * frame_sec
        seg_end = (e + 1) * frame_sec
        length = seg_end - seg_start
        if length < min_len:
            # expand symmetrically if possible
            needed = min_len - length
            seg_start = max(0, seg_start - needed / 2)
            seg_end = seg_start + min_len
        if (seg_end - seg_start) > max_len:
            seg_end = seg_start + max_len
        time_segments.append((seg_start, seg_end))

    # Score by average normalized energy inside segment
    scored = []
    for (s, e) in time_segments:
        i1 = int(s / frame_sec)
        i2 = int(e / frame_sec)
        seg_energy = norm[i1:i2+1].mean() if i2 >= i1 else 0
        scored.append(((s, e), seg_energy))

    scored.sort(key=lambda x: x[1], reverse=True)
    top = [seg for (seg, _) in scored[:target_count]]
    return top


def create_highlight_shorts(
    video_path: Path,
    count: int = 3,
    target_len: int = 20,
    out_dir: Path = SHORTS_DIR
) -> List[Path]:
    """
    Based on energy detection, create highlight clips (horizontal).
    """
    segments = detect_highlight_segments(video_path, target_count=count, max_len=target_len)
    outputs = []
    for i, (start, end) in enumerate(segments, start=1):
        out = out_dir / f"HIGHLIGHT_{video_path.stem}_{i}.mp4"
        duration = end - start
        cmd = [
            "ffmpeg", "-y",
            "-ss", f"{start:.2f}",
            "-i", str(video_path),
            "-t", f"{duration:.2f}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "128k",
            "-movflags", "+faststart",
            str(out)
        ]
        subprocess.run(cmd, capture_output=True)
        outputs.append(out)
    return outputs


# ================================================================
# 2. FASTAPI DASHBOARD
# ================================================================
def start_fastapi_dashboard(host: str = "127.0.0.1", port: int = 8055):
    """
    Launch FastAPI dashboard showing fragments, metrics, retention summary.
    """
    try:
        from fastapi import FastAPI
        from fastapi.responses import HTMLResponse, JSONResponse
        import uvicorn
    except ImportError:
        log.error("FastAPI / uvicorn not installed. pip install fastapi uvicorn")
        return

    app = FastAPI(title="SCARIFY Dashboard")

    def load_fragments():
        if FRAGMENTS_FILE.exists():
            try:
                return json.loads(FRAGMENTS_FILE.read_text(encoding="utf-8"))
            except:
                return {}
        return {}

    def load_metrics():
        if METRICS_FILE.exists():
            try:
                return json.loads(METRICS_FILE.read_text(encoding="utf-8"))
            except:
                return []
        return []

    @app.get("/", response_class=HTMLResponse)
    def root():
        return '''
        <html>
          <head>
            <title>SCARIFY Dashboard</title>
            <style>
              body { font-family: Arial; background:#111;color:#eee; margin:20px;}
              .card { background:#1d1d1d; padding:16px; margin:10px 0; border-radius:8px;}
              h1 {color:#c33;}
              pre {background:#222; padding:10px; border-radius:6px;}
              .grid {display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px;}
            </style>
          </head>
          <body>
            <h1>SCARIFY Live Dashboard</h1>
            <div id="summary"></div>
            <div class="grid">
              <div class="card">
                <h3>Fragments</h3>
                <pre id="fragments">Loading...</pre>
              </div>
              <div class="card">
                <h3>Metrics</h3>
                <pre id="metrics">Loading...</pre>
              </div>
              <div class="card">
                <h3>Retention Stats</h3>
                <pre id="retention">Loading...</pre>
              </div>
            </div>
            <script>
              async function refresh() {
                const f = await fetch('/api/fragments').then(r=>r.json());
                const m = await fetch('/api/metrics').then(r=>r.json());
                const r = await fetch('/api/retention-summary').then(r=>r.json());
                document.getElementById('fragments').textContent = JSON.stringify(f, null, 2);
                document.getElementById('metrics').textContent = JSON.stringify(m.slice(-10), null, 2);
                document.getElementById('retention').textContent = JSON.stringify(r, null, 2);
                let summary = '';
                summary += '<div class="card"><b>Total Fragments:</b> ' + f.fragments.length + '</div>';
                summary += '<div class="card"><b>Scenes:</b> ' + m.length + '</div>';
                document.getElementById('summary').innerHTML = summary;
              }
              refresh();
              setInterval(refresh, 5000);
            </script>
          </body>
        </html>
        '''

    @app.get("/api/fragments")
    def api_fragments():
        data = load_fragments()
        return JSONResponse(data)

    @app.get("/api/metrics")
    def api_metrics():
        return JSONResponse(load_metrics())

    @app.get("/api/retention-summary")
    def api_retention():
        metrics = load_metrics()
        scores = []
        for entry in metrics:
            try:
                from math import log
                base = {
                    "narrator": entry.get("narrator"),
                    "content_type": entry.get("content_type"),
                    "duration_sec": entry.get("duration_sec",0),
                    "multi_voice": entry.get("multi_voice", False),
                    "uploaded": entry.get("uploaded", False),
                    "fragment_added": entry.get("fragment_added", False)
                }
                score = retention_score(base)
                scores.append(score)
            except Exception:
                pass
        avg = sum(s["score"] for s in scores)/len(scores) if scores else 0
        return {"count": len(scores), "average_score": round(avg,2), "samples": scores[:10]}

    log.info("Starting FastAPI dashboard on %s:%d", host, port)
    uvicorn.run(app, host=host, port=port)


# ================================================================
# 3. ELEVENLABS ADAPTER SCAFFOLD
# ================================================================
def elevenlabs_generate(
    text: str,
    voice_id: str = "Rachel",
    model: str = "eleven_monolingual_v1",
    out_path: Optional[Path] = None,
    api_key: Optional[str] = None,
    timeout: int = 40
) -> Optional[Path]:
    """
    Scaffold for ElevenLabs TTS.
    - No dependency on official client (uses httpx if available).
    - Returns path to generated audio MP3 or None on fallback.
    """
    if out_path is None:
        out_path = Path("scarify/temp") / f"eleven_{uuid.uuid4().hex}.mp3"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        log.warning("ELEVENLABS_API_KEY missing - returning None (fallback).")
        return None

    try:
        import httpx
    except ImportError:
        log.error("httpx not installed. pip install httpx")
        return None

    payload = {
        "text": text,
        "model_id": model,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "accept": "audio/mpeg",
        "content-type": "application/json"
    }

    try:
        with httpx.Client(timeout=timeout) as client:
            r = client.post(url, headers=headers, json=payload)
            if r.status_code != 200:
                log.error("ElevenLabs error %s: %s", r.status_code, r.text[:200])
                return None
            out_path.write_bytes(r.content)
            log.info("ElevenLabs TTS saved: %s", out_path)
            return out_path
    except Exception as e:
        log.error("ElevenLabs request failed: %s", e)
        return None


# ================================================================
# 4. RETENTION SCORING HEURISTIC
# ================================================================
def retention_score(meta: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compute retention score (0-100). Heuristic:
      - Base: 40
      - Duration sweet spots:
          shorts: 45 ±10  => +15
          teaser: 30 ±8   => +12
          long/analysis: 420-540 => +18
      - Multi-voice layering: +6
      - Puzzle / stego presence (if keys): +4 each
      - Fragment added: +4
      - Uploaded: +5
      - Narrator balancing: oracle=+2, scholar=+1, herald=+1 (example weighting)

    meta keys used (safe if absent):
      duration_sec, content_type, multi_voice, puzzle, thumbnail, fragment_added, uploaded, narrator
    """
    duration = meta.get("duration_sec", 0) or meta.get("duration", 0)
    ctype = meta.get("content_type", "analysis_transmission")
    narrator = meta.get("narrator", "oracle")
    multi_voice = bool(meta.get("multi_voice") or meta.get("multi_voice_layered"))
    has_puzzle = "puzzle" in meta or meta.get("puzzle_path")
    has_stego = "thumbnail" in meta
    fragment_added = meta.get("fragment_added", False) or "fragment_id" in meta
    uploaded = meta.get("uploaded", False) or "youtube_id" in meta

    score = 40.0

    def in_range(val, lo, hi):
        return lo <= val <= hi

    if ctype in ("shorts_teaser","shorts","teaser_clue","teaser"):
        if in_range(duration, 35, 55):
            score += 15
    if ctype in ("analysis_transmission","analysis"):
        if in_range(duration, 420, 540):
            score += 18
    if ctype in ("major_revelation","long_form"):
        if in_range(duration, 450, 660):
            score += 18

    if multi_voice:
        score += 6
    if has_puzzle:
        score += 4
    if has_stego:
        score += 4
    if fragment_added:
        score += 4
    if uploaded:
        score += 5

    narrator_bonus = {"oracle":2,"scholar":1,"herald":1}
    score += narrator_bonus.get(narrator,0)

    # Slight normalization clamp
    score = max(0, min(100, score))
    return {
        "score": round(score,2),
        "narrator": narrator,
        "content_type": ctype,
        "duration_sec": duration,
        "multi_voice": multi_voice,
        "puzzle": has_puzzle,
        "stego": has_stego,
        "fragment_added": fragment_added,
        "uploaded": uploaded
    }


# ================================================================
# 5. STEGO THUMBNAIL EXTRACTOR
# ================================================================
def extract_stego_payload(thumbnail_path: Path, max_chars=128) -> str:
    """
    Extract payload from the R-channel LSB of first pixels.
    Stops if non-printable encountered or max_chars reached.
    """
    from PIL import Image
    img = Image.open(thumbnail_path)
    data = list(img.getdata())
    bits = []
    # 8 bits -> 1 char
    for pix in data:
        r = pix[0]
        bits.append(str(r & 1))
        if len(bits) >= max_chars * 8:
            break
    chars = []
    for i in range(0, len(bits), 8):
        bchunk = bits[i:i+8]
        if len(bchunk) < 8:
            break
        val = int(''.join(bchunk), 2)
        if val == 0: break
        if not 32 <= val < 127:
            break
        chars.append(chr(val))
    return ''.join(chars)


# ================================================================
# 6. FRAGMENT CHAIN RECONSTRUCTION
# ================================================================
def reconstruct_chain(frag_file: Path = FRAGMENTS_FILE) -> Dict[str, Any]:
    """
    Rebuild combined fragment_text chain (if available).
    If master_hash & chain_key present, verify integrity.
    """
    if not frag_file.exists():
        return {"status":"no_fragments_file"}
    try:
        data = json.loads(frag_file.read_text(encoding="utf-8"))
    except Exception as e:
        return {"status":"error","error":str(e)}

    frags = data.get("fragments", [])
    if not frags:
        return {"status":"empty"}

    ordered = sorted(frags, key=lambda x: x.get("position", 0))
    chain_plain = ''.join(f.get("fragment_text","") for f in ordered)
    import hashlib
    computed_hash = hashlib.sha256(chain_plain.encode()).hexdigest()
    master_hash = data.get("master_hash")
    chain_key = data.get("chain_key")

    result = {
        "status":"ok",
        "fragment_count": len(frags),
        "target": data.get("target"),
        "positions_collected": [f.get("position") for f in ordered],
        "master_hash_match": (master_hash == computed_hash) if master_hash else False,
        "master_hash_known": bool(master_hash),
        "master_hash_prefix": (master_hash or "")[:12],
        "computed_hash_prefix": computed_hash[:12],
        "chain_key": chain_key,
        "chain_key_prefix": (chain_key or "")[:12],
        "complete": bool(master_hash and chain_key and (master_hash == computed_hash))
    }
    return result


# ================================================================
# 7. COMMAND-LINE INTERFACE
# ================================================================
def _cli_highlight(args):
    video = Path(args.video)
    if not video.exists():
        print("Video not found:", video)
        return
    outs = create_highlight_shorts(video, count=args.count, target_len=args.maxlen)
    print("Highlights created:")
    for o in outs:
        print(" ", o)

def _cli_chain(_args):
    info = reconstruct_chain()
    print(json.dumps(info, indent=2))

def _cli_stego(args):
    thumb = Path(args.thumbnail)
    if not thumb.exists():
        print("Thumbnail not found:", thumb)
        return
    payload = extract_stego_payload(thumb)
    print("Extracted payload:", payload)

def _cli_retention(args):
    meta_file = Path(args.meta)
    if not meta_file.exists():
        print("Meta JSON not found:", meta_file)
        return
    meta = json.loads(meta_file.read_text(encoding="utf-8"))
    sc = retention_score(meta)
    print(json.dumps(sc, indent=2))

def _cli_elevenlabs(args):
    out = elevenlabs_generate(args.text, voice_id=args.voice, model=args.model)
    if out:
        print("Generated:", out)
    else:
        print("ElevenLabs generation failed or fallback used.")


def _cli_dashboard(args):
    start_fastapi_dashboard(host=args.host, port=args.port)

def main_cli():
    import argparse
    p = argparse.ArgumentParser(description="SCARIFY Advanced Suite")
    sp = p.add_subparsers(dest="cmd")

    hp = sp.add_parser("highlight", help="Energy-based highlight extraction")
    hp.add_argument("--video", required=True)
    hp.add_argument("--count", type=int, default=3)
    hp.add_argument("--maxlen", type=int, default=20)
    hp.set_defaults(func=_cli_highlight)

    cp = sp.add_parser("chain", help="Reconstruct fragment chain")
    cp.set_defaults(func=_cli_chain)

    spg = sp.add_parser("stego", help="Extract stego payload from thumbnail")
    spg.add_argument("--thumbnail", required=True)
    spg.set_defaults(func=_cli_stego)

    rp = sp.add_parser("retention", help="Compute retention score from meta JSON")
    rp.add_argument("--meta", required=True)
    rp.set_defaults(func=_cli_retention)

    ep = sp.add_parser("elevenlabs-test", help="Test ElevenLabs adapter")
    ep.add_argument("text")
    ep.add_argument("--voice", default="Rachel")
    ep.add_argument("--model", default="eleven_monolingual_v1")
    ep.set_defaults(func=_cli_elevenlabs)

    dp = sp.add_parser("dashboard", help="Start FastAPI live dashboard")
    dp.add_argument("--host", default="127.0.0.1")
    dp.add_argument("--port", type=int, default=8055)
    dp.set_defaults(func=_cli_dashboard)

    args = p.parse_args()
    if not args.cmd:
        p.print_help()
        return
    args.func(args)

if __name__ == "__main__":
    main_cli()