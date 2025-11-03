#!/usr/bin/env python3
"""
SCARIFY Complete Automation System
Generates scripts → Creates videos → Prepares for YouTube
"""

import os
import sys
import json
import subprocess
import random
from pathlib import Path
from datetime import datetime

# Configuration
VOICE_ID = '7aavy6c5cYIloDVj2JvH'
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY', '')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')

BASE_DIR = Path("F:/AI_Oracle_Root/scarify")

# ============================================================================
# SCRIPT GENERATION - MULTIPLE METHODS
# ============================================================================

class ScriptGenerator:
    """Generate horror story scripts using various methods"""
    
    def __init__(self):
        self.themes = [
            "abandoned asylum",
            "haunted forest",
            "cursed object",
            "paranormal investigation",
            "urban legends",
            "psychological horror",
            "supernatural encounters",
            "mysterious disappearance"
        ]
        
        self.story_structures = [
            "discovery_horror",
            "escalating_dread",
            "revelation_twist",
            "atmospheric_tension"
        ]
    
    def generate_with_openai(self, theme: str) -> dict:
        """Generate script using OpenAI API"""
        
        if not OPENAI_API_KEY:
            return None
        
        try:
            import requests
        except ImportError:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'requests', '--break-system-packages'], 
                          capture_output=True)
            import requests
        
        url = "https://api.openai.com/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""Create a compelling horror story script for YouTube with these requirements:

Theme: {theme}
Duration: 60-90 seconds of narration
Style: Atmospheric psychological horror
Structure: Hook in first 10 seconds, building tension, chilling conclusion
Tone: Professional, mysterious, keep viewers engaged
Goal: Maximum retention and emotional impact

Write ONLY the narration script. Make it vivid and immersive."""
        
        data = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "You are a professional horror writer specializing in YouTube content optimization."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 500,
            "temperature": 0.9
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                script_text = response.json()['choices'][0]['message']['content'].strip()
                
                return {
                    'script': script_text,
                    'theme': theme,
                    'method': 'openai',
                    'word_count': len(script_text.split()),
                    'generated_at': datetime.now().isoformat()
                }
            else:
                print(f"OpenAI API error: {response.status_code}")
                return None
        except Exception as e:
            print(f"OpenAI generation failed: {e}")
            return None
    
    def generate_with_anthropic(self, theme: str) -> dict:
        """Generate script using Anthropic Claude API"""
        
        if not ANTHROPIC_API_KEY:
            return None
        
        try:
            import requests
        except ImportError:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'requests', '--break-system-packages'], 
                          capture_output=True)
            import requests
        
        url = "https://api.anthropic.com/v1/messages"
        
        headers = {
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        prompt = f"""Create a horror story script about {theme}. Requirements:
- 60-90 seconds of narration
- Atmospheric and psychological
- Strong opening hook
- Building tension
- Memorable ending
- Professional tone for YouTube

Write only the narration script."""
        
        data = {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 500,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                script_text = response.json()['content'][0]['text'].strip()
                
                return {
                    'script': script_text,
                    'theme': theme,
                    'method': 'anthropic',
                    'word_count': len(script_text.split()),
                    'generated_at': datetime.now().isoformat()
                }
            else:
                print(f"Anthropic API error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Anthropic generation failed: {e}")
            return None
    
    def generate_template_based(self, theme: str) -> dict:
        """Generate script using templates (no API required)"""
        
        templates = {
            "abandoned_asylum": """They say the old asylum closed in 1987, but that's not the whole truth.
The patients didn't simply leave. Something kept them there.
Local urban explorers discovered why last October.
Their cameras captured footage that made investigators seal the building permanently.
The last message from their group chat was a single word: 'Run.'
But by then, the doors had already locked from the inside.
Some places are abandoned for a reason.
And some doors should never be reopened.""",
            
            "haunted_forest": """The forest has a rule: never enter after sunset.
Three hikers ignored that warning on a camping trip.
Their GPS devices showed them walking in perfect circles for hours.
By midnight, their phones captured sounds that shouldn't exist in nature.
Search and rescue found their campsite the next morning.
Tents still zipped from the inside. Food untouched.
The only clue: identical scratches on every nearby tree trunk.
Leading deeper into the woods where no paths exist.""",
            
            "cursed_object": """The antique store owner gave one warning: never bring it home.
Of course, the price was too good to pass up.
That night, shadows moved differently in the house.
Photographs on the walls showed people who weren't there before.
By morning, the mirrors reflected rooms that didn't match.
When they tried to return it, the store was gone.
Just an empty lot where it had stood for decades.
And the object? Still sitting in their living room."""
        }
        
        # Select template based on theme
        template_key = theme.replace(" ", "_")
        
        if template_key in templates:
            script_text = templates[template_key]
        else:
            # Use a random template
            script_text = random.choice(list(templates.values()))
        
        return {
            'script': script_text,
            'theme': theme,
            'method': 'template',
            'word_count': len(script_text.split()),
            'generated_at': datetime.now().isoformat()
        }
    
    def generate_script(self, method: str = "auto") -> dict:
        """Generate script using specified method"""
        
        theme = random.choice(self.themes)
        
        print(f"🎬 Generating script...")
        print(f"   Theme: {theme}")
        print(f"   Method: {method}")
        
        if method == "auto":
            # Try methods in order of preference
            if OPENAI_API_KEY:
                result = self.generate_with_openai(theme)
                if result:
                    print(f"   ✅ Generated with OpenAI")
                    return result
            
            if ANTHROPIC_API_KEY:
                result = self.generate_with_anthropic(theme)
                if result:
                    print(f"   ✅ Generated with Anthropic")
                    return result
            
            # Fallback to template
            print(f"   ✅ Using template (no API keys)")
            return self.generate_template_based(theme)
        
        elif method == "openai":
            return self.generate_with_openai(theme)
        
        elif method == "anthropic":
            return self.generate_with_anthropic(theme)
        
        elif method == "template":
            return self.generate_template_based(theme)
        
        else:
            return self.generate_template_based(theme)

# ============================================================================
# VOICE GENERATION
# ============================================================================

def generate_voice(text: str, output_path: Path) -> bool:
    """Generate voice with ElevenLabs"""
    
    if not ELEVENLABS_API_KEY:
        print("❌ ElevenLabs API key not set!")
        return False
    
    try:
        import requests
    except ImportError:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'requests', '--break-system-packages'], 
                      capture_output=True)
        import requests
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.75,
            "style": 0.6,
            "use_speaker_boost": True
        }
    }
    
    print(f"🎙️ Generating voice narration...")
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=120)
        
        if response.status_code == 200:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            size_kb = output_path.stat().st_size / 1024
            print(f"   ✅ Voice generated: {size_kb:.2f} KB")
            return True
        else:
            print(f"   ❌ API Error {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

# ============================================================================
# VIDEO CREATION
# ============================================================================

def create_video(audio_path: Path, output_path: Path, metadata: dict) -> bool:
    """Create video with FFmpeg"""
    
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except:
        print("❌ FFmpeg not found!")
        return False
    
    print(f"🎬 Creating video...")
    
    # Get audio duration
    try:
        probe_cmd = [
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            str(audio_path)
        ]
        result = subprocess.run(probe_cmd, capture_output=True, text=True, check=True)
        duration = float(result.stdout.strip())
    except:
        duration = 60
    
    # Create video with dark background
    cmd = [
        'ffmpeg',
        '-f', 'lavfi',
        '-i', f'color=c=#0a0a0a:s=1920x1080:d={duration}',
        '-i', str(audio_path),
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-b:v', '5000k',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-shortest',
        '-y',
        str(output_path)
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, check=True)
        
        if output_path.exists():
            size_mb = output_path.stat().st_size / (1024 * 1024)
            print(f"   ✅ Video created: {size_mb:.2f} MB, {duration:.1f}s")
            return True
        else:
            print("   ❌ Video creation failed")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

# ============================================================================
# YOUTUBE PREPARATION
# ============================================================================

def prepare_for_youtube(video_path: Path, script_data: dict) -> Path:
    """Prepare video for YouTube upload"""
    
    youtube_dir = BASE_DIR / "videos/youtube_ready"
    youtube_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    youtube_file = youtube_dir / f"SCARIFY_{timestamp}.mp4"
    
    # Copy video
    import shutil
    shutil.copy2(video_path, youtube_file)
    
    # Create metadata for YouTube
    title = f"SCARIFY: {script_data['theme'].title()} | True Horror Story"
    
    description = f"""A chilling tale of {script_data['theme']}.

🔔 Subscribe for more psychological horror content
👍 Like if this gave you chills
💬 Share your own experiences in the comments

{script_data['script'][:100]}...

#horror #scary #creepy #scarystories #horrortok #scarify #{script_data['theme'].replace(' ', '')}"""
    
    tags = [
        'horror',
        'scary',
        'creepy',
        'true horror',
        'scary stories',
        'horror stories',
        'creepypasta',
        'scarify',
        script_data['theme'].replace(' ', '')
    ]
    
    metadata = {
        'file_path': str(youtube_file),
        'title': title,
        'description': description,
        'tags': tags,
        'category': '24',  # Entertainment
        'privacy': 'public',
        'made_for_kids': False,
        'script_data': script_data,
        'created_at': datetime.now().isoformat()
    }
    
    # Save metadata
    metadata_file = youtube_file.with_suffix('.json')
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"📤 YouTube ready: {youtube_file}")
    print(f"   Title: {title}")
    print(f"   Metadata: {metadata_file}")
    
    return youtube_file

# ============================================================================
# COMPLETE AUTO-GENERATION PIPELINE
# ============================================================================

def auto_generate_video(method: str = "auto") -> dict:
    """Complete pipeline: Script → Voice → Video → YouTube Ready"""
    
    print("\n" + "="*60)
    print(f"🔥 SCARIFY AUTO-GENERATION")
    print("="*60)
    
    # Setup directories
    (BASE_DIR / "scripts/generated").mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "audio").mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "videos/generated").mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Step 1: Generate script
    generator = ScriptGenerator()
    script_data = generator.generate_script(method)
    
    if not script_data:
        print("❌ Script generation failed")
        return None
    
    # Save script
    script_file = BASE_DIR / "scripts/generated" / f"script_{timestamp}.json"
    with open(script_file, 'w') as f:
        json.dump(script_data, f, indent=2)
    
    print(f"   ✅ Script saved: {script_file}")
    print(f"   Words: {script_data['word_count']}")
    
    # Step 2: Generate voice
    audio_file = BASE_DIR / "audio" / f"narration_{timestamp}.mp3"
    
    if not generate_voice(script_data['script'], audio_file):
        print("❌ Voice generation failed")
        return None
    
    # Step 3: Create video
    video_file = BASE_DIR / "videos/generated" / f"SCARIFY_{timestamp}.mp4"
    
    if not create_video(audio_file, video_file, script_data):
        print("❌ Video creation failed")
        return None
    
    # Step 4: Prepare for YouTube
    youtube_file = prepare_for_youtube(video_file, script_data)
    
    print("\n" + "="*60)
    print("✅ AUTO-GENERATION COMPLETE!")
    print("="*60)
    print(f"📁 YouTube Ready: {youtube_file}")
    print(f"📄 Metadata: {youtube_file.with_suffix('.json')}")
    print("="*60 + "\n")
    
    return {
        'script_file': str(script_file),
        'audio_file': str(audio_file),
        'video_file': str(video_file),
        'youtube_file': str(youtube_file),
        'metadata_file': str(youtube_file.with_suffix('.json')),
        'script_data': script_data
    }

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    method = sys.argv[1] if len(sys.argv) > 1 else "auto"
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    
    results = []
    
    for i in range(count):
        print(f"\n{'='*60}")
        print(f"VIDEO {i+1}/{count}")
        print(f"{'='*60}")
        
        result = auto_generate_video(method)
        
        if result:
            results.append(result)
        
        if i < count - 1:
            print("\nWaiting 5 seconds before next generation...")
            import time
            time.sleep(5)
    
    print(f"\n{'='*60}")
    print(f"BATCH COMPLETE: {len(results)}/{count} videos generated")
    print(f"{'='*60}")
    print(f"\nAll videos ready in: {BASE_DIR / 'videos/youtube_ready'}")
