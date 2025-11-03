#!/usr/bin/env python3
"""
QUALITY_CHECK_BEFORE_BATCH.py
Generate 5 test videos with quality verification BEFORE batch of 70
"""

import sys
from pathlib import Path
from datetime import datetime
import hashlib

sys.path.insert(0, str(Path.cwd()))

from abraham_MAX_HEADROOM import generate_voice, generate_lincoln_face_pollo, BASE_DIR
from CLEAN_UP_MESSY_VISUALS import create_clean_max_headroom
from YOUTUBE_TAG_OPTIMIZATION import generate_optimized_tags
from MULTI_STYLE_SCRIPT_GENERATOR import ScriptStyleGenerator

# Track used scripts to prevent duplicates
USED_SCRIPTS_FILE = BASE_DIR / 'used_scripts.txt'

def load_used_scripts():
    """Load previously used scripts"""
    if USED_SCRIPTS_FILE.exists():
        with open(USED_SCRIPTS_FILE, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def save_used_script(script):
    """Save script hash to prevent duplicates"""
    script_hash = hashlib.md5(script.encode()).hexdigest()
    used = load_used_scripts()
    used.add(script_hash)
    with open(USED_SCRIPTS_FILE, 'w', encoding='utf-8') as f:
        for h in used:
            f.write(h + '\n')
    return script_hash

def is_script_unique(script):
    """Check if script is unique"""
    script_hash = hashlib.md5(script.encode()).hexdigest()
    used = load_used_scripts()
    return script_hash not in used

def generate_unique_script(headline, style, max_attempts=10):
    """Generate unique script with retry"""
    style_gen = ScriptStyleGenerator()
    
    for attempt in range(max_attempts):
        if style == 'chatgpt':
            script = style_gen.chatgpt_style(headline)
        elif style == 'grok':
            script = style_gen.grok_style(headline)
        elif style == 'opus':
            script = style_gen.opus_style(headline)
        else:
            script = style_gen.cursor_style(headline)
        
        if is_script_unique(script):
            save_used_script(script)
            return script
        
        print(f"  [Attempt {attempt+1}] Duplicate script, regenerating...")
    
    # After 10 attempts, modify headline and try again
    script = style_gen.cursor_style(f"{headline} - New Angle")
    save_used_script(script)
    return script

def quality_check_video(video_path, metadata):
    """Verify video quality"""
    issues = []
    
    # Check file size
    if not video_path.exists():
        issues.append("Video file doesn't exist")
        return issues
    
    size_mb = video_path.stat().st_size / (1024*1024)
    
    if size_mb < 0.5:
        issues.append(f"File too small ({size_mb:.1f}MB) - may be corrupted")
    
    if size_mb > 200:
        issues.append(f"File too large ({size_mb:.1f}MB) - may have encoding issue")
    
    # Check script for Bitcoin address (should NOT be there!)
    script = metadata.get('script', '')
    
    if 'bc1q' in script.lower() or 'bitcoin address' in script.lower():
        issues.append("Script contains Bitcoin address recitation (SHOULD BE REMOVED!)")
    
    # Check for comedian names (should NOT be there!)
    comedian_names = ['pryor', 'chappelle', 'carlin', 'williams', 'katt', 'youngboy']
    for name in comedian_names:
        if name in script.lower():
            issues.append(f"Script mentions comedian name: {name}")
    
    # Check for QR code (should be there!)
    if 'qr' not in metadata.get('title', '').lower() and 'bitcoin below' not in script.lower():
        issues.append("No QR code call-to-action in script")
    
    # Check tags
    tags = metadata.get('tags', [])
    if len(tags) < 15:
        issues.append(f"Only {len(tags)} tags (should have 20-25)")
    
    return issues

def generate_quality_test_batch(count=5):
    """Generate 5 test videos with quality checks"""
    
    print("="*70)
    print("  QUALITY TEST BATCH - 5 VIDEOS")
    print("="*70 + "\n")
    
    print("Testing system BEFORE batch of 70...\n")
    
    # Test headlines
    headlines = [
        "Government Shutdown Enters Month 2",
        "AI Regulation Bill Passes Senate",
        "Market Volatility Spikes",
        "Climate Summit Ends in Deadlock",
        "Tech Layoffs Continue"
    ]
    
    styles = ['chatgpt', 'cursor', 'grok', 'opus', 'cursor']
    
    test_dir = BASE_DIR / 'quality_test'
    test_dir.mkdir(parents=True, exist_ok=True)
    
    results = []
    
    for i, (headline, style) in enumerate(zip(headlines, styles)):
        episode = 999990 + i
        
        print(f"\n[{i+1}/5] Testing Episode #{episode}")
        print(f"  Headline: {headline}")
        print(f"  Style: {style}")
        
        # Generate UNIQUE script
        script = generate_unique_script(headline, style)
        
        print(f"  Script: {script[:100]}...")
        print(f"  Unique: [OK]")
        
        # Generate title
        title = f"Lincoln's WARNING #{episode}: {headline[:40]} #Shorts"
        
        # Generate voice
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        audio_path = BASE_DIR / 'audio' / f'TEST_{episode}_{timestamp}.mp3'
        audio_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not generate_voice(script, audio_path):
            print(f"  [FAILED] Voice generation")
            continue
        
        # Get Lincoln
        lincoln = generate_lincoln_face_pollo()
        
        # Get QR
        qr = BASE_DIR / 'qr_codes' / 'cashapp_qr.png'
        
        # Create video
        output = test_dir / f'TEST_{episode}_{timestamp}.mp4'
        
        video = create_clean_max_headroom(lincoln, audio_path, output, qr)
        
        if not video or not Path(video).exists():
            print(f"  [FAILED] Video creation")
            continue
        
        # Generate metadata
        tags = generate_optimized_tags(title, script, 'short')
        
        metadata = {
            'episode': episode,
            'title': title,
            'script': script,
            'tags': tags,
            'style': style,
            'video_path': str(video)
        }
        
        # QUALITY CHECK
        issues = quality_check_video(Path(video), metadata)
        
        if issues:
            print(f"  [ISSUES FOUND]")
            for issue in issues:
                print(f"    ❌ {issue}")
        else:
            print(f"  [QUALITY] PASSED")
        
        size_mb = Path(video).stat().st_size / (1024*1024)
        print(f"  [VIDEO] {size_mb:.1f} MB, {len(tags)} tags")
        
        results.append({
            'episode': episode,
            'video': video,
            'issues': issues,
            'passed': len(issues) == 0
        })
    
    # Summary
    print("\n" + "="*70)
    print("  QUALITY TEST RESULTS")
    print("="*70 + "\n")
    
    passed = sum(1 for r in results if r['passed'])
    total = len(results)
    
    print(f"Passed: {passed}/{total} ({passed/total*100:.0f}%)\n")
    
    if passed == total:
        print("[OK] ALL TESTS PASSED!")
        print("Safe to run batch of 70 videos!\n")
        print("Command: python MASS_GENERATE_100_VIDEOS.py --total 70 --pollo 0")
    else:
        print("[WARNING] SOME TESTS FAILED!")
        print("Review issues above before batch generation.\n")
        for r in results:
            if not r['passed']:
                print(f"  Episode #{r['episode']}: {len(r['issues'])} issues")
    
    print("="*70 + "\n")
    print(f"Test videos saved to: {test_dir}\n")
    
    return passed == total

if __name__ == "__main__":
    success = generate_quality_test_batch(5)
    sys.exit(0 if success else 1)

