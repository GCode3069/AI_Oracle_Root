#!/usr/bin/env python3
"""
Test ABRAHAM_STUDIO features to verify operational status
"""
import sys
from pathlib import Path

BASE = Path("F:/AI_Oracle_Root/scarify")

def test_imports():
    """Test all required imports"""
    print("[TEST] Checking imports...")
    
    try:
        import tkinter
        print("  [OK] tkinter")
    except ImportError as e:
        print(f"  [FAIL] tkinter: {e}")
        return False
    
    try:
        import requests
        print("  [OK] requests")
    except ImportError as e:
        print(f"  [FAIL] requests: {e}")
        return False
    
    try:
        import subprocess
        print("  [OK] subprocess")
    except ImportError as e:
        print(f"  [FAIL] subprocess: {e}")
        return False
    
    return True

def test_api_keys():
    """Test API keys are set"""
    print("\n[TEST] Checking API keys...")
    
    studio_file = BASE / "ABRAHAM_STUDIO (1).pyw"
    if not studio_file.exists():
        print(f"  [FAIL] Studio file not found: {studio_file}")
        return False
    
    content = studio_file.read_text(encoding='utf-8', errors='ignore')
    
    keys = {
        'ELEVENLABS_API_KEY': '3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa',
        'STABILITY_API_KEY': 'sk-sP9EO0Ybb3L7SfGbpEtfrmOIhXVf8DdK9eSaTSBuTcNhjpQi'
    }
    
    for key_name, key_value in keys.items():
        if key_value in content:
            print(f"  [OK] {key_name}")
        else:
            print(f"  [WARN] {key_name} not found in file")
    
    return True

def test_directories():
    """Test directories exist"""
    print("\n[TEST] Checking directories...")
    
    studio_dir = BASE / "abraham_studio"
    dirs = ['audio', 'videos', 'youtube_ready']
    
    for d in dirs:
        dir_path = studio_dir / d
        if dir_path.exists():
            print(f"  [OK] {d}/")
        else:
            print(f"  [WARN] {d}/ does not exist (will be created)")
    
    return True

def test_ffmpeg():
    """Test FFmpeg is available"""
    print("\n[TEST] Checking FFmpeg...")
    
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, timeout=5)
        if result.returncode == 0:
            print("  [OK] FFmpeg installed")
            return True
        else:
            print("  [WARN] FFmpeg not working properly")
            return False
    except FileNotFoundError:
        print("  [WARN] FFmpeg not found (video generation may fail)")
        return False
    except Exception as e:
        print(f"  [WARN] FFmpeg check error: {e}")
        return False

def test_syntax():
    """Test studio file syntax"""
    print("\n[TEST] Checking syntax...")
    
    studio_file = BASE / "ABRAHAM_STUDIO (1).pyw"
    
    try:
        import py_compile
        py_compile.compile(str(studio_file), doraise=True)
        print("  [OK] Syntax valid")
        return True
    except py_compile.PyCompileError as e:
        print(f"  [FAIL] Syntax error: {e}")
        return False
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False

def main():
    """Run all tests"""
    print("="*70)
    print("ABRAHAM STUDIO - FEATURE TEST")
    print("="*70)
    
    results = {
        'imports': test_imports(),
        'api_keys': test_api_keys(),
        'directories': test_directories(),
        'ffmpeg': test_ffmpeg(),
        'syntax': test_syntax()
    }
    
    print("\n" + "="*70)
    print("TEST RESULTS")
    print("="*70)
    
    for test_name, result in results.items():
        status = "[PASS]" if result else "[FAIL/WARN]"
        print(f"{status} {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*70)
    if all_passed:
        print("[OK] ALL TESTS PASSED - Studio is operational!")
    else:
        print("[WARN] Some tests failed/warned - check above")
    print("="*70)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

