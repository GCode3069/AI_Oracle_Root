#!/usr/bin/env python3
"""Check current professional pipeline status"""

import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check Python version"""
    try:
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        version = result.stdout.strip()
        print(f"🐍 Python Version: {version}")
        
        # Extract major.minor
        version_parts = version.split()[1].split('.')
        major, minor = int(version_parts[0]), int(version_parts[1])
        
        if 39 <= major * 10 + minor <= 311:
            print("✅ Python version compatible with Coqui TTS")
            return True
        else:
            print("❌ Python version must be 3.9-3.11 for Coqui TTS")
            return False
            
    except Exception as e:
        print(f"❌ Error checking Python version: {e}")
        return False

def check_ffmpeg():
    """Check FFmpeg installation"""
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, timeout=5)
        if "ffmpeg version" in result.stdout:
            print("✅ FFmpeg installed")
            return True
        else:
            print("❌ FFmpeg not installed")
            return False
    except:
        print("❌ FFmpeg not installed")
        return False

def check_imagemagick():
    """Check ImageMagick installation"""
    try:
        result = subprocess.run(["magick", "-version"], capture_output=True, text=True, timeout=5)
        if "Version:" in result.stdout:
            print("✅ ImageMagick installed")
            return True
        else:
            print("❌ ImageMagick not installed")
            return False
    except:
        print("❌ ImageMagick not installed")
        return False

def check_handbrake():
    """Check HandBrake installation"""
    try:
        result = subprocess.run(["HandBrakeCLI", "--version"], capture_output=True, text=True, timeout=5)
        if "HandBrake" in result.stdout:
            print("✅ HandBrake installed")
            return True
        else:
            print("❌ HandBrake not installed")
            return False
    except:
        print("❌ HandBrake not installed")
        return False

def check_movipy():
    """Check MoviePy installation"""
    try:
        import moviepy.editor
        print("✅ MoviePy installed")
        return True
    except ImportError:
        print("❌ MoviePy not installed")
        return False

def check_gtts():
    """Check gTTS installation"""
    try:
        from gtts import gTTS
        print("✅ gTTS installed")
        return True
    except ImportError:
        print("❌ gTTS not installed")
        return False

def check_coqui_tts():
    """Check Coqui TTS installation"""
    try:
        from TTS.api import TTS
        print("✅ Coqui TTS installed")
        return True
    except ImportError:
        print("❌ Coqui TTS not installed")
        return False

def check_musetalk():
    """Check MuseTalk installation"""
    musetalk_dir = Path("MuseTalk")
    if musetalk_dir.exists():
        print("✅ MuseTalk directory exists")
        requirements_file = musetalk_dir / "requirements.txt"
        if requirements_file.exists():
            print("✅ MuseTalk requirements file found")
            return True
        else:
            print("❌ MuseTalk requirements file missing")
            return False
    else:
        print("❌ MuseTalk directory not found")
        return False

def check_lincoln_headshot():
    """Check Lincoln headshot"""
    lincoln_dir = Path("lincoln_faces")
    if lincoln_dir.exists():
        files = list(lincoln_dir.glob("*.jpg")) + list(lincoln_dir.glob("*.png"))
        if files:
            print(f"✅ Lincoln headshots found: {len(files)} file(s)")
            for f in files:
                print(f"   - {f.name}")
            return True
        else:
            print("❌ No Lincoln headshots found in lincoln_faces directory")
            return False
    else:
        print("❌ lincoln_faces directory not found")
        return False

def main():
    print("🎬 Professional Video Pipeline Status Check")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("FFmpeg", check_ffmpeg),
        ("ImageMagick", check_imagemagick),
        ("HandBrake", check_handbrake),
        ("MoviePy", check_movipy),
        ("gTTS", check_gtts),
        ("Coqui TTS", check_coqui_tts),
        ("MuseTalk", check_musetalk),
        ("Lincoln Headshot", check_lincoln_headshot)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\nChecking {name}...")
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Error checking {name}: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("📊 Pipeline Status Summary")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\n✅ Passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tools ready! Professional pipeline is complete.")
    else:
        print("\n⚠️  Some tools are missing. Please check the errors above.")
        
        if not check_python_version():
            print("\n💡 To install Python 3.11 virtual environment:")
            print("   python -m venv coqui_env")
            print("   source coqui_env/bin/activate  # Linux/Mac")
            print("   coqui_env\\Scripts\\activate  # Windows")
            print("   pip install TTS")
        
        if not check_musetalk():
            print("\n💡 To install MuseTalk:")
            print("   git clone https://github.com/Fadi002/MuseTalk.git")
            print("   cd MuseTalk")
            print("   pip install -r requirements.txt")
            print("   python download_models.py")
        
        if not check_handbrake():
            print("\n💡 To install HandBrake CLI:")
            print("   Ubuntu/Debian: sudo apt install handbrake-cli")
            print("   macOS: brew install handbrake")
            print("   Windows: choco install handbrake")

if __name__ == "__main__":
    main()
