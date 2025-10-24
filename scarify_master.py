#!/usr/bin/env python3
"""
SCARIFY Master Script - Main entry point for video generation
Usage:
    python scarify_master.py --count 1 --test
    python scarify_master.py --count 5
"""

import os
import sys
import argparse
import json
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config/credentials/.env')

# Add the scarify directory to the path
sys.path.append(str(Path(__file__).parent / 'scarify'))

def check_api_keys():
    """Check if required API keys are configured"""
    elevenlabs_key = os.getenv('ELEVENLABS_API_KEY')
    pexels_key = os.getenv('PEXELS_API_KEY')
    
    if not elevenlabs_key or elevenlabs_key == 'your_elevenlabs_api_key_here':
        print("❌ ElevenLabs API key not configured!")
        print("   Please set ELEVENLABS_API_KEY in config/credentials/.env")
        return False
    
    if not pexels_key or pexels_key == 'your_pexels_api_key_here':
        print("❌ Pexels API key not configured!")
        print("   Please set PEXELS_API_KEY in config/credentials/.env")
        return False
    
    print("✅ API keys configured")
    return True

def generate_single_video(theme="NightmareCity", test_mode=False):
    """Generate a single SCARIFY video"""
    print(f"🎬 Generating SCARIFY video (theme: {theme}, test: {test_mode})")
    
    try:
        # Import the cinematic teaser generator
        from scarify.cinematic_teaser import generate_script_for_theme
        
        # Generate script
        script_data = generate_script_for_theme(theme)
        
        # Create output directory
        output_dir = Path("scarify/Output/ShortsReady")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save script
        script_file = output_dir / f"script_{int(time.time())}.json"
        with open(script_file, 'w', encoding='utf-8') as f:
            json.dump(script_data, f, indent=2)
        
        print(f"📝 Script generated: {script_file}")
        print(f"   Title: {script_data['title']}")
        print(f"   Theme: {script_data['theme']}")
        
        if test_mode:
            print("🧪 Test mode - skipping video generation")
            return True
        
        # TODO: Add actual video generation here
        # This would involve:
        # 1. Text-to-speech using ElevenLabs
        # 2. Stock footage from Pexels
        # 3. Video composition
        # 4. Audio/video synchronization
        
        print("⚠️  Video generation not yet implemented")
        print("   This would generate the actual video file")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating video: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="SCARIFY Master Video Generator")
    parser.add_argument("--count", type=int, default=1, help="Number of videos to generate")
    parser.add_argument("--test", action="store_true", help="Test mode (skip video generation)")
    parser.add_argument("--theme", default="NightmareCity", 
                       choices=["NightmareCity", "AI_Consciousness", "DigitalPossession", 
                               "BiologicalHorror", "CosmicHorror"],
                       help="Theme for video generation")
    
    args = parser.parse_args()
    
    print("🔮 SCARIFY Master Video Generator")
    print("=" * 40)
    
    # Check API keys
    if not check_api_keys():
        print("\n💡 To get API keys:")
        print("   1. ElevenLabs: https://elevenlabs.io/ (free tier)")
        print("   2. Pexels: https://www.pexels.com/api/ (free)")
        print("   3. Add keys to config/credentials/.env")
        return 1
    
    # Generate videos
    success_count = 0
    for i in range(args.count):
        print(f"\n🎬 Generating video {i+1}/{args.count}")
        if generate_single_video(args.theme, args.test):
            success_count += 1
        else:
            print(f"❌ Failed to generate video {i+1}")
    
    print(f"\n✅ Successfully generated {success_count}/{args.count} videos")
    
    if args.test:
        print("🧪 Test mode completed - no actual videos were generated")
    
    return 0 if success_count == args.count else 1

if __name__ == "__main__":
    sys.exit(main())