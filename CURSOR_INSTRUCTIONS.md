# CURSOR AI INSTRUCTIONS: SCARIFY PROJECT ENHANCEMENT

## 🎯 PROJECT CONTEXT

**Project Name**: SCARIFY - Abraham Lincoln VHS Broadcast System
**Current Status**: Development with multiple components, some working, some need fixes
**Goal**: Create viral Abraham Lincoln comedy videos in VHS TV broadcast style
**Target**: 50 videos/day for YouTube Shorts monetization

---

## 📋 IMMEDIATE TASKS FOR CURSOR AI

### TASK 1: CODE REVIEW & ERROR FIXING

**Priority**: CRITICAL

#### Files to Review:
1. `F:\AI_Oracle_Root\scarify\abraham_horror\abe_comedy.py`
2. `F:\AI_Oracle_Root\scarify\abraham_horror\abe_vhs_ultimate.py`
3. `F:\AI_Oracle_Root\scarify\abraham_horror\abe_vhs_multipass.py`
4. All files in `/scripts/` directory

#### Known Errors to Fix:

**Error 1: Missing Lincoln Portrait**
```
[WinError 433] A device which does not exist was specified: 
'assets\\lincoln_portrait.jpg'
```
**Fix Required**:
- Add automatic download of Lincoln portrait on first run
- Create fallback if download fails
- Verify file path is correct (Windows paths)

**Error 2: FFmpeg Timeout**
```
Command timed out after 120 seconds
```
**Fix Required**:
- Implement multi-pass rendering (already designed, needs testing)
- Add timeout retry logic
- Optimize filter chains

**Error 3: Encoding Errors**
```
UnicodeEncodeError: 'charmap' codec can't encode character
```
**Fix Required**:
- Add UTF-8 encoding to all file operations
- Use `encoding='utf-8'` in all `open()` calls
- Fix Windows CP1252 encoding issues

---

### TASK 2: API INTEGRATION VALIDATION

**Priority**: HIGH (Wasting $338/month!)

#### APIs to Validate:

**ElevenLabs (WORKING)**
```python
# Current implementation OK, but verify:
- API key is valid
- Voice ID exists
- Error handling is robust
```

**Pexels (WORKING)**
```python
# Current implementation OK, but add:
- Better error handling
- Caching mechanism
- Video quality selection
```

**Pollo.ai ($328/month - UNUSED!)**
```python
# URGENT: Implement or cancel!
# Required investigation:
1. Test API connectivity
2. Generate one sample video
3. Compare quality vs FFmpeg
4. If not better → RECOMMEND CANCELLATION
```

**Stability.ai ($10/month - UNUSED!)**
```python
# Required investigation:
1. Test API connectivity
2. Enhance Lincoln portrait
3. Evaluate quality improvement
4. If minimal → RECOMMEND CANCELLATION
```

#### Implementation Requirements:

```python
# Create: scripts/api_integration_test.py

import requests
import json
from pathlib import Path

class APITester:
    """Test all paid APIs and evaluate ROI"""
    
    def __init__(self):
        self.config = self.load_config()
        self.results = {}
    
    def load_config(self):
        config_path = Path("F:/AI_Oracle_Root/scarify/abraham_horror/config/api_keys.json")
        with open(config_path, encoding='utf-8') as f:
            return json.load(f)
    
    def test_elevenlabs(self):
        """Test ElevenLabs (currently working)"""
        api_key = self.config['elevenlabs']['api_key']
        headers = {"xi-api-key": api_key}
        
        try:
            response = requests.get(
                "https://api.elevenlabs.io/v1/voices",
                headers=headers,
                timeout=10
            )
            self.results['elevenlabs'] = {
                'status': 'SUCCESS' if response.status_code == 200 else 'FAIL',
                'cost': 22,
                'using': True,
                'verdict': 'KEEP'
            }
        except Exception as e:
            self.results['elevenlabs'] = {
                'status': 'ERROR',
                'error': str(e)
            }
    
    def test_pollo(self):
        """Test Pollo.ai - $328/month!"""
        api_key = self.config['pollo']['api_key']
        
        # TODO: Implement actual Pollo API test
        # Endpoints to try:
        # - https://api.pollo.ai/v1/status
        # - https://api.pollo.ai/v1/models
        # - https://api.pollo.ai/v1/generate
        
        try:
            # Test connection
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get(
                "https://api.pollo.ai/v1/status",  # Verify actual endpoint
                headers=headers,
                timeout=10
            )
            
            self.results['pollo'] = {
                'status': 'SUCCESS' if response.status_code == 200 else 'FAIL',
                'cost': 328,
                'using': False,
                'verdict': 'TEST REQUIRED - CANCELLATION RECOMMENDED IF NOT BETTER THAN FFMPEG'
            }
        except Exception as e:
            self.results['pollo'] = {
                'status': 'ERROR',
                'error': str(e),
                'verdict': 'CANNOT TEST - RECOMMEND IMMEDIATE CANCELLATION'
            }
    
    def test_stability(self):
        """Test Stability.ai - $10/month"""
        api_key = self.config.get('stability', {}).get('api_key', 'NOT_SET')
        
        if api_key == 'NOT_SET' or api_key == 'YOUR_STABILITY_KEY_HERE':
            self.results['stability'] = {
                'status': 'NOT_CONFIGURED',
                'cost': 10,
                'using': False,
                'verdict': 'CANCEL IF NOT CONFIGURED'
            }
            return
        
        try:
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get(
                "https://api.stability.ai/v1/user/account",
                headers=headers,
                timeout=10
            )
            
            self.results['stability'] = {
                'status': 'SUCCESS' if response.status_code == 200 else 'FAIL',
                'cost': 10,
                'using': False,
                'verdict': 'TEST IMAGE ENHANCEMENT - CANCEL IF NO VISIBLE IMPROVEMENT'
            }
        except Exception as e:
            self.results['stability'] = {
                'status': 'ERROR',
                'error': str(e)
            }
    
    def generate_report(self):
        """Generate cost optimization report"""
        total_cost = sum(r.get('cost', 0) for r in self.results.values())
        wasted_cost = sum(
            r.get('cost', 0) 
            for r in self.results.values() 
            if not r.get('using', True)
        )
        
        print("\n" + "="*80)
        print("API COST ANALYSIS")
        print("="*80)
        print(f"\nTotal Monthly Cost: ${total_cost}")
        print(f"Potentially Wasted: ${wasted_cost}")
        print(f"Annual Waste: ${wasted_cost * 12}")
        print("\nAPI STATUS:")
        
        for api, result in self.results.items():
            print(f"\n{api.upper()}:")
            print(f"  Status: {result.get('status', 'UNKNOWN')}")
            print(f"  Cost: ${result.get('cost', 0)}/month")
            print(f"  Using: {result.get('using', False)}")
            print(f"  Verdict: {result.get('verdict', 'REVIEW REQUIRED')}")

if __name__ == "__main__":
    tester = APITester()
    tester.test_elevenlabs()
    tester.test_pollo()
    tester.test_stability()
    tester.generate_report()
```

---

### TASK 3: DESKTOP GENERATOR INTEGRATION

**Priority**: HIGH

#### Current Desktop Generator Location:
- Visible in screenshot: Multiple Python files in project
- Need to consolidate into ONE master script

#### Requirements:

```python
# Create: F:\AI_Oracle_Root\scarify\DESKTOP_GENERATOR.py

"""
SCARIFY Desktop Generator
One-click video generation with GUI progress tracking
Integrates ALL components
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent / "abraham_horror"))

from scripts.abe_generator import VideoGenerator
from scripts.api_manager import APIManager

class DesktopGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SCARIFY - Abraham Lincoln VHS Generator")
        self.root.geometry("800x600")
        
        self.setup_ui()
        self.generator = None
    
    def setup_ui(self):
        """Create desktop UI"""
        
        # Header
        header = tk.Label(
            self.root, 
            text="SCARIFY - Abraham Lincoln VHS Broadcast",
            font=("Arial", 16, "bold"),
            bg="#1a1a1a",
            fg="#00ff00",
            pady=10
        )
        header.pack(fill=tk.X)
        
        # Settings Frame
        settings_frame = ttk.LabelFrame(self.root, text="Generation Settings", padding=10)
        settings_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Number of videos
        ttk.Label(settings_frame, text="Number of Videos:").grid(row=0, column=0, sticky=tk.W)
        self.video_count = tk.IntVar(value=10)
        ttk.Spinbox(
            settings_frame, 
            from_=1, 
            to=100, 
            textvariable=self.video_count,
            width=10
        ).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # Start number
        ttk.Label(settings_frame, text="Start Episode #:").grid(row=1, column=0, sticky=tk.W)
        self.start_number = tk.IntVar(value=1000)
        ttk.Spinbox(
            settings_frame,
            from_=1,
            to=10000,
            textvariable=self.start_number,
            width=10
        ).grid(row=1, column=1, sticky=tk.W, padx=5)
        
        # Voice mode
        ttk.Label(settings_frame, text="Voice Mode:").grid(row=2, column=0, sticky=tk.W)
        self.voice_mode = tk.StringVar(value="comedic")
        ttk.Combobox(
            settings_frame,
            textvariable=self.voice_mode,
            values=["comedic", "serious", "angry"],
            width=15
        ).grid(row=2, column=1, sticky=tk.W, padx=5)
        
        # Use B-roll
        self.use_broll = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            settings_frame,
            text="Use Pexels B-roll",
            variable=self.use_broll
        ).grid(row=3, column=0, columnspan=2, sticky=tk.W)
        
        # Buttons Frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(
            button_frame,
            text="Generate Videos",
            command=self.start_generation
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Test APIs",
            command=self.test_apis
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Open Output Folder",
            command=self.open_output_folder
        ).pack(side=tk.LEFT, padx=5)
        
        # Progress Frame
        progress_frame = ttk.LabelFrame(self.root, text="Progress", padding=10)
        progress_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='determinate',
            maximum=100
        )
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(
            progress_frame,
            height=15,
            bg="#1a1a1a",
            fg="#00ff00",
            font=("Consolas", 9)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
    
    def log(self, message):
        """Add message to log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def start_generation(self):
        """Start video generation in background thread"""
        def generate():
            try:
                self.log("[START] Beginning video generation...")
                
                # Initialize generator
                from scripts.abe_generator import generate_videos
                
                success_count = generate_videos(
                    count=self.video_count.get(),
                    start=self.start_number.get(),
                    voice_mode=self.voice_mode.get(),
                    use_broll=self.use_broll.get(),
                    progress_callback=self.update_progress,
                    log_callback=self.log
                )
                
                self.log(f"[COMPLETE] Generated {success_count} videos successfully!")
                
            except Exception as e:
                self.log(f"[ERROR] {str(e)}")
        
        thread = threading.Thread(target=generate, daemon=True)
        thread.start()
    
    def update_progress(self, current, total):
        """Update progress bar"""
        progress = (current / total) * 100
        self.progress_bar['value'] = progress
        self.root.update()
    
    def test_apis(self):
        """Test all API connections"""
        def test():
            self.log("[TEST] Testing API connections...")
            # Run API tests
            from api_integration_test import APITester
            tester = APITester()
            # ... test and log results
        
        thread = threading.Thread(target=test, daemon=True)
        thread.start()
    
    def open_output_folder(self):
        """Open output folder in explorer"""
        import os
        output_path = Path("F:/AI_Oracle_Root/scarify/abraham_horror/uploaded")
        os.startfile(output_path)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = DesktopGenerator()
    app.run()
```

---

### TASK 4: CODE IMPROVEMENTS

#### Improvements Needed:

**1. Error Handling**
```python
# Add to ALL functions:
try:
    # existing code
except Exception as e:
    logging.error(f"Error in {function_name}: {e}")
    # Attempt recovery or graceful failure
```

**2. Logging System**
```python
# Add: scripts/logger.py

import logging
from pathlib import Path
from datetime import datetime

def setup_logger():
    log_dir = Path("F:/AI_Oracle_Root/scarify/abraham_horror/logs")
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"scarify_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger('SCARIFY')
```

**3. Configuration Management**
```python
# Improve: scripts/config_manager.py

import json
from pathlib import Path
from typing import Dict, Any

class ConfigManager:
    """Centralized configuration management"""
    
    def __init__(self):
        self.config_dir = Path("F:/AI_Oracle_Root/scarify/abraham_horror/config")
        self.config_dir.mkdir(exist_ok=True)
        
        self.api_keys = self.load_json("api_keys.json")
        self.settings = self.load_json("settings.json")
    
    def load_json(self, filename: str) -> Dict[str, Any]:
        """Load JSON config file"""
        path = self.config_dir / filename
        
        if not path.exists():
            return {}
        
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_json(self, filename: str, data: Dict[str, Any]):
        """Save JSON config file"""
        path = self.config_dir / filename
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get config value"""
        # Check settings first, then API keys
        return self.settings.get(key, self.api_keys.get(key, default))
```

**4. Performance Optimization**
```python
# Add caching for expensive operations:
from functools import lru_cache

@lru_cache(maxsize=10)
def fetch_broll_cached(query: str) -> str:
    """Cached B-roll fetching"""
    return fetch_broll(query)
```

---

### TASK 5: TESTING REQUIREMENTS

#### Create Test Suite:

```python
# Create: tests/test_generation.py

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "abraham_horror"))

from scripts.abe_generator import VideoGenerator
from scripts.api_manager import APIManager

class TestVideoGeneration(unittest.TestCase):
    
    def setUp(self):
        self.generator = VideoGenerator()
    
    def test_api_connectivity(self):
        """Test all API connections"""
        api_manager = APIManager()
        
        # ElevenLabs
        self.assertTrue(api_manager.test_elevenlabs())
        
        # Pexels
        self.assertTrue(api_manager.test_pexels())
    
    def test_lincoln_portrait_download(self):
        """Test Lincoln portrait download"""
        portrait_path = Path("F:/AI_Oracle_Root/scarify/abraham_horror/assets/lincoln_portrait.jpg")
        
        if not portrait_path.exists():
            # Should auto-download
            self.generator.ensure_assets()
        
        self.assertTrue(portrait_path.exists())
    
    def test_video_generation(self):
        """Test single video generation"""
        output = self.generator.generate_one(
            episode_num=9999,
            test_mode=True
        )
        
        self.assertTrue(Path(output).exists())
    
    def test_ffmpeg_timeout_handling(self):
        """Test FFmpeg timeout doesn't crash"""
        # Should handle gracefully
        try:
            self.generator.generate_with_timeout(duration=1000)
        except TimeoutError:
            pass  # Expected
        except Exception as e:
            self.fail(f"Unexpected exception: {e}")

if __name__ == '__main__':
    unittest.main()
```

---

## 📊 DELIVERABLES REQUIRED FROM CURSOR

### 1. Fixed Code
- All syntax errors resolved
- All import errors fixed
- All path issues corrected
- UTF-8 encoding everywhere

### 2. API Integration Report
```
Report Format:
- Pollo.ai: [TESTED/NOT_TESTED] - [KEEP/CANCEL]
- Stability.ai: [TESTED/NOT_TESTED] - [KEEP/CANCEL]
- Cost savings potential: $XXX/month
```

### 3. Desktop Generator
- Working GUI application
- Progress tracking
- Error display
- One-click generation

### 4. Test Results
- All unit tests passing
- End-to-end test successful
- Performance benchmarks

---

## 🎯 SUCCESS CRITERIA

1. ✅ Generate 1 video end-to-end without errors
2. ✅ Desktop GUI launches and works
3. ✅ All APIs tested and evaluated
4. ✅ Cost optimization recommendations provided
5. ✅ Code is clean, documented, and maintainable

---

## 📝 NOTES FOR CURSOR

- Use Windows file paths (backslashes)
- UTF-8 encoding for all text operations
- Add error handling to EVERYTHING
- Log all operations
- Test before committing
- Document all changes

---

**Priority Order**:
1. Fix critical errors (portrait download, encoding)
2. Test APIs (especially Pollo - $328/month!)
3. Build desktop generator
4. Optimize and document
