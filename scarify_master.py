#!/usr/bin/env python3
"""
SCARIFY Master Script - Main entry point for video generation
Supports count-based generation and test mode
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, Any

# Add the scarify directory to the path
sys.path.append(str(Path(__file__).parent / "scarify"))

def load_config() -> Dict[str, Any]:
    """Load configuration from various sources"""
    config = {}
    
    # Try to load from .env file
    env_file = Path("config/credentials/.env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    config[key] = value
    
    # Load ElevenLabs config
    elevenlabs_config = Path("config/elevenlabs_config.py")
    if elevenlabs_config.exists():
        with open(elevenlabs_config, 'r') as f:
            content = f.read()
            # Extract API key from the file
            if "ELEVENLABS_API_KEY" in content:
                import re
                match = re.search(r"ELEVENLABS_API_KEY\s*=\s*['\"]([^'\"]+)['\"]", content)
                if match:
                    config['ELEVENLABS_API_KEY'] = match.group(1)
    
    return config

def generate_video(theme: str = "NightmareCity", test_mode: bool = False) -> Dict[str, Any]:
    """Generate a single video using the cinematic teaser generator"""
    try:
        from scarify.cinematic_teaser import generate_script_for_theme
        
        # Generate script
        script_data = generate_script_for_theme(theme)
        
        if test_mode:
            print(f"🧪 TEST MODE: Generated script for theme '{theme}'")
            print(f"📝 Title: {script_data['title']}")
            print(f"📄 Script: {script_data['script'][:200]}...")
            return {
                "success": True,
                "test_mode": True,
                "script": script_data,
                "video_path": None
            }
        
        # In production mode, we would generate actual video here
        # For now, we'll create a placeholder
        output_dir = Path("scarify/Output/ShortsReady")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save script as JSON
        script_file = output_dir / f"script_{int(time.time())}.json"
        with open(script_file, 'w') as f:
            json.dump(script_data, f, indent=2)
        
        print(f"✅ Generated video script: {script_file}")
        print(f"📝 Title: {script_data['title']}")
        
        return {
            "success": True,
            "test_mode": False,
            "script": script_data,
            "script_file": str(script_file),
            "video_path": None  # Placeholder for actual video generation
        }
        
    except Exception as e:
        print(f"❌ Error generating video: {e}")
        return {
            "success": False,
            "error": str(e)
        }

def main():
    parser = argparse.ArgumentParser(description="SCARIFY Master Video Generator")
    parser.add_argument("--count", type=int, default=1, help="Number of videos to generate")
    parser.add_argument("--test", action="store_true", help="Run in test mode (no actual video generation)")
    parser.add_argument("--theme", default="NightmareCity", 
                       choices=["NightmareCity", "AI_Consciousness", "DigitalPossession", 
                               "BiologicalHorror", "CosmicHorror"],
                       help="Theme for video generation")
    
    args = parser.parse_args()
    
    print(f"🎬 SCARIFY Master Generator")
    print(f"📊 Count: {args.count}")
    print(f"🧪 Test Mode: {args.test}")
    print(f"🎭 Theme: {args.theme}")
    print("-" * 50)
    
    # Load configuration
    config = load_config()
    if not config.get('ELEVENLABS_API_KEY') or config['ELEVENLABS_API_KEY'] == 'your_elevenlabs_api_key':
        print("⚠️  Warning: ElevenLabs API key not configured")
        print("   Please set ELEVENLABS_API_KEY in config/credentials/.env")
    
    # Generate videos
    results = []
    for i in range(args.count):
        print(f"\n🎥 Generating video {i+1}/{args.count}...")
        result = generate_video(args.theme, args.test)
        results.append(result)
        
        if not result['success']:
            print(f"❌ Failed to generate video {i+1}")
            break
        
        if not args.test:
            time.sleep(1)  # Small delay between generations
    
    # Summary
    successful = sum(1 for r in results if r['success'])
    print(f"\n📊 Generation Summary:")
    print(f"   ✅ Successful: {successful}/{args.count}")
    print(f"   ❌ Failed: {args.count - successful}/{args.count}")
    
    if args.test:
        print("\n🧪 Test mode completed - no actual videos generated")
    else:
        print(f"\n📁 Check scarify/Output/ShortsReady/ for generated content")

if __name__ == "__main__":
    main()