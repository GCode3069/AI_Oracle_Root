#!/usr/bin/env python3
"""
Oracle Horror CLI - Demo Version
Quick video generation for testing
"""

import argparse
import sys
import os
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from oracle_horror_manifest import OracleHorrorManifest
from audio_engine import AudioEngine
from effects_library import EffectsLibrary

def generate_demo_video(campaign, format_type, output_dir="output"):
    """Generate a demo horror video (static image + audio)"""
    print(f"🎬 Generating DEMO Oracle Horror video: {campaign} ({format_type})")
    print("=" * 60)
    
    try:
        # Initialize components
        manifest = OracleHorrorManifest()
        audio = AudioEngine()
        effects = EffectsLibrary()
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate manifest
        print("📋 Generating horror manifest...")
        horror_manifest = manifest.generate_manifest(campaign, format_type)
        print(f"✅ Generated: {horror_manifest['title']}")
        
        # Generate audio
        print("🔊 Synthesizing horror narration...")
        audio_file = audio.generate_horror_narration(
            horror_manifest['script'], 
            style="ominous_whisper"
        )
        print(f"✅ Audio generated: {audio_file}")
        
        # Generate static image (instead of full video for demo)
        print("🎥 Creating horror visual...")
        specs = horror_manifest['specs']
        resolution = (1080, 1920) if format_type == "shorts" else (1920, 1080) if format_type == "full" else (1080, 1080)
        
        # Create horror image
        background = effects.generate_background(resolution, horror_manifest['theme']['color_scheme'])
        background = effects.add_matrix_rain(background, "medium")
        background = effects.add_horror_text(background, horror_manifest['script'], "glitch_neon")
        
        # Save image
        video_id = horror_manifest.get("id", "oracle_horror_demo")
        image_file = Path(output_dir) / f"{video_id}_demo.png"
        background.save(image_file, "PNG")
        print(f"✅ Horror image generated: {image_file}")
        
        # Create demo info file
        demo_info = {
            "type": "Oracle Horror Demo",
            "campaign": campaign,
            "format": format_type,
            "title": horror_manifest['title'],
            "script": horror_manifest['script'],
            "audio_file": audio_file,
            "image_file": str(image_file),
            "note": "This is a demo version. Full video generation is available with more time."
        }
        
        info_file = Path(output_dir) / f"{video_id}_demo.json"
        import json
        with open(info_file, 'w') as f:
            json.dump(demo_info, f, indent=2)
        
        print(f"✅ Demo info saved: {info_file}")
        print("=" * 60)
        print(f"🌟 Demo horror content generated successfully!")
        return str(info_file)
        
    except Exception as e:
        print(f"❌ Demo generation failed: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Oracle Horror Demo CLI")
    parser.add_argument('--campaign', 
                       choices=['awakening', 'revelation', 'convergence'],
                       default='awakening',
                       help='Horror campaign type')
    parser.add_argument('--format',
                       choices=['shorts', 'full', 'viral_series'],
                       default='shorts',
                       help='Video format')
    parser.add_argument('--output', default='output', help='Output directory')
    
    args = parser.parse_args()
    
    print("🔮 Oracle Horror Demo Generation Engine")
    print("   Quick demo with static image + audio")
    print()
    
    demo_file = generate_demo_video(args.campaign, args.format, args.output)
    sys.exit(0 if demo_file else 1)

if __name__ == "__main__":
    main()