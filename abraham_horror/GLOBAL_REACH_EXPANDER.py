"""
GLOBAL REACH EXPANSION SYSTEM
Adds multi-language subtitles, international topics, and global appeal
Current: 62% US → Goal: Worldwide audience
"""
import os, sys, json, requests, subprocess, time
from pathlib import Path
from datetime import datetime

BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")

# Target languages for global reach (based on YouTube demographics)
GLOBAL_LANGUAGES = {
    "es": "Spanish",  # 500M+ speakers
    "hi": "Hindi",    # 600M+ speakers
    "pt": "Portuguese",  # 250M+ speakers
    "fr": "French",   # 280M+ speakers
    "de": "German",   # 130M+ speakers
    "ja": "Japanese", # 125M+ speakers
    "ko": "Korean",   # 80M+ speakers
    "ar": "Arabic",   # 400M+ speakers
    "ru": "Russian",  # 250M+ speakers
    "zh": "Chinese"   # 1B+ speakers
}

# Universal fear/comedy topics that work globally
UNIVERSAL_TOPICS = [
    "Technology addiction (everyone has smartphones)",
    "Cost of living crisis (global inflation)",
    "Climate change anxiety (worldwide concern)",
    "AI job replacement (universal fear)",
    "Government corruption (every country)",
    "Social media manipulation (global issue)",
    "Privacy invasion (worldwide surveillance)",
    "Wealth inequality (international problem)",
    "War and conflict (timeless fear)",
    "Health system failures (universal frustration)"
]

def log(msg, status="INFO"):
    icons = {"INFO": "[🌍]", "SUCCESS": "[✅]", "ERROR": "[❌]", "PROCESS": "[⚙️]"}
    print(f"{icons.get(status, '[INFO]')} {msg}")

def translate_text(text, target_lang):
    """Translate text using Google Translate (free, no API key needed)"""
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl={target_lang}&dt=t&q={requests.utils.quote(text)}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            result = r.json()
            if result and len(result) > 0 and len(result[0]) > 0:
                return result[0][0][0]
    except:
        pass
    return None

def generate_srt_subtitles(script, output_path, language="en"):
    """Generate SRT subtitle file"""
    log(f"Generating {GLOBAL_LANGUAGES.get(language, language)} subtitles...", "PROCESS")
    
    # Split script into subtitle chunks (every ~40 characters)
    words = script.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        current_chunk.append(word)
        current_length += len(word) + 1
        if current_length > 40:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    # Translate if not English
    if language != "en":
        translated_chunks = []
        for chunk in chunks:
            translated = translate_text(chunk, language)
            translated_chunks.append(translated if translated else chunk)
        chunks = translated_chunks
    
    # Generate SRT format
    srt_content = []
    duration_per_chunk = 3.0  # seconds per subtitle
    
    for i, chunk in enumerate(chunks, 1):
        start_time = (i-1) * duration_per_chunk
        end_time = i * duration_per_chunk
        
        start_h = int(start_time // 3600)
        start_m = int((start_time % 3600) // 60)
        start_s = int(start_time % 60)
        start_ms = int((start_time % 1) * 1000)
        
        end_h = int(end_time // 3600)
        end_m = int((end_time % 3600) // 60)
        end_s = int(end_time % 60)
        end_ms = int((end_time % 1) * 1000)
        
        srt_content.append(f"{i}")
        srt_content.append(f"{start_h:02d}:{start_m:02d}:{start_s:02d},{start_ms:03d} --> {end_h:02d}:{end_m:02d}:{end_s:02d},{end_ms:03d}")
        srt_content.append(chunk)
        srt_content.append("")
    
    # Save SRT file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(srt_content))
    
    log(f"Subtitles saved: {output_path.name}", "SUCCESS")
    return output_path

def burn_subtitles_into_video(video_path, srt_path, output_path):
    """Burn subtitles into video using FFmpeg"""
    log("Burning subtitles into video...", "PROCESS")
    
    try:
        # Escape path for FFmpeg
        srt_path_str = str(srt_path).replace('\\', '/')
        srt_path_str = srt_path_str.replace(':', '\\:')
        
        subprocess.run([
            "ffmpeg", "-y",
            "-i", str(video_path),
            "-vf", f"subtitles='{srt_path_str}'",
            "-c:a", "copy",
            str(output_path)
        ], capture_output=True, timeout=300)
        
        if output_path.exists():
            log("Subtitles burned successfully", "SUCCESS")
            return True
    except Exception as e:
        log(f"Subtitle burning failed: {e}", "ERROR")
    
    return False

def create_multi_language_video(source_video, script):
    """Create versions with different language subtitles"""
    log("\n🌍 CREATING MULTI-LANGUAGE VERSIONS", "PROCESS")
    log("="*70)
    
    results = []
    priority_langs = ["es", "hi", "pt", "fr", "ar"]  # Top 5 for reach
    
    for lang_code in priority_langs:
        lang_name = GLOBAL_LANGUAGES[lang_code]
        log(f"\nProcessing {lang_name}...", "PROCESS")
        
        # Generate SRT
        srt_path = BASE / f"temp/subtitles_{lang_code}.srt"
        generate_srt_subtitles(script, srt_path, lang_code)
        
        # Create subtitled version
        output_path = BASE / f"videos_global/{source_video.stem}_{lang_code}.mp4"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if burn_subtitles_into_video(source_video, srt_path, output_path):
            results.append({
                'language': lang_name,
                'code': lang_code,
                'file': str(output_path),
                'target_audience': f"{lang_name}-speaking countries"
            })
    
    log(f"\n✅ Created {len(results)} language variants", "SUCCESS")
    return results

if __name__ == "__main__":
    log("\n" + "="*70)
    log("GLOBAL REACH EXPANSION SYSTEM")
    log("="*70)
    log("Current: 62% US audience")
    log("Goal: Worldwide reach with multi-language support")
    log("="*70 + "\n")
    
    log("🎯 TARGET EXPANSION:")
    for code, name in list(GLOBAL_LANGUAGES.items())[:5]:
        log(f"  • {name} - Massive untapped audience")
    
    log("\n🌍 UNIVERSAL TOPICS FOR GLOBAL APPEAL:")
    for topic in UNIVERSAL_TOPICS[:5]:
        log(f"  • {topic}")
    
    log("\n📊 STRATEGY:")
    log("  1. Generate video with English audio")
    log("  2. Add subtitles in 5 major languages")
    log("  3. Post language variants to reach global audiences")
    log("  4. Target: 10x current reach")
    
    log("\n✅ SYSTEM READY FOR DEPLOYMENT")


