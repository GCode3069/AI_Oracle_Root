#!/usr/bin/env python3
"""
Oracle Horror CLI - Real Video Generation Engine
Generates horror-themed videos with ElevenLabs voice synthesis and FFmpeg rendering
"""

import argparse
import sys
import os
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from oracle_horror_manifest import OracleHorrorManifest
    from video_engine import VideoEngine
    from audio_engine import AudioEngine
    from effects_library import EffectsLibrary
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("🔧 Please ensure all dependencies are installed: pip install -r requirements.txt")
    sys.exit(1)

def test_system():
    """Test all Oracle Horror components"""
    print("🧪 Oracle Horror System Test")
    print("=" * 50)
    
    # Test manifest generation
    print("📋 Testing manifest generation...")
    try:
        manifest = OracleHorrorManifest()
        test_manifest = manifest.generate_manifest("awakening", "shorts")
        print("✅ Manifest generation: PASSED")
    except Exception as e:
        print(f"❌ Manifest generation: FAILED - {e}")
        return False
    
    # Test audio engine
    print("🔊 Testing audio engine...")
    try:
        audio = AudioEngine()
        test_result = audio.test_connection()
        if test_result:
            print("✅ Audio engine: PASSED")
        else:
            print("❌ Audio engine: FAILED - ElevenLabs connection")
            return False
    except Exception as e:
        print(f"❌ Audio engine: FAILED - {e}")
        return False
    
    # Test video engine
    print("🎥 Testing video engine...")
    try:
        video = VideoEngine()
        test_result = video.test_ffmpeg()
        if test_result:
            print("✅ Video engine: PASSED")
        else:
            print("❌ Video engine: FAILED - FFmpeg not available")
            return False
    except Exception as e:
        print(f"❌ Video engine: FAILED - {e}")
        return False
    
    # Test effects library
    print("🌟 Testing effects library...")
    try:
        effects = EffectsLibrary()
        test_result = effects.test_effects()
        if test_result:
            print("✅ Effects library: PASSED")
        else:
            print("❌ Effects library: FAILED")
            return False
    except Exception as e:
        print(f"❌ Effects library: FAILED - {e}")
        return False
    
    print("=" * 50)
    print("🎯 All tests PASSED - Oracle Horror ready for production!")
    return True

def generate_single_video(campaign, format_type, output_dir="output"):
    """Generate a single horror video"""
    print(f"🎬 Generating Oracle Horror video: {campaign} ({format_type})")
    print("=" * 60)
    
    try:
        # Initialize components
        manifest = OracleHorrorManifest()
        audio = AudioEngine()
        video = VideoEngine()
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
        
        # Generate video with effects
        print("🎥 Rendering horror video with effects...")
        video_file = video.render_horror_video(
            horror_manifest, 
            audio_file, 
            format_type,
            output_dir
        )
        print(f"✅ Video generated: {video_file}")
        
        print("=" * 60)
        print(f"🌟 Horror video generated successfully: {video_file}")
        return video_file
        
    except Exception as e:
        print(f"❌ Video generation failed: {e}")
        return None

def generate_multiple_videos(count, output_dir="output"):
    """Generate multiple horror videos"""
    print(f"🎬 Generating {count} Oracle Horror videos")
    print("=" * 60)
    
    campaigns = ["awakening", "revelation", "convergence"]
    formats = ["shorts", "full", "viral_series"]
    
    generated_videos = []
    
    for i in range(count):
        campaign = campaigns[i % len(campaigns)]
        format_type = formats[i % len(formats)]
        
        print(f"\n🎥 Video {i+1}/{count}: {campaign} - {format_type}")
        video_file = generate_single_video(campaign, format_type, output_dir)
        
        if video_file:
            generated_videos.append(video_file)
        else:
            print(f"❌ Failed to generate video {i+1}")
    
    print("=" * 60)
    print(f"🎯 Generated {len(generated_videos)}/{count} videos successfully")
    
    for video in generated_videos:
        print(f"📁 {video}")
    
    return generated_videos

def main():
    parser = argparse.ArgumentParser(
        description="Oracle Horror Real Video Generation Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python oracle_horror_cli.py test
  python oracle_horror_cli.py generate --campaign awakening --format shorts
  python oracle_horror_cli.py all --count 3
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Test all system components')
    
    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate single horror video')
    generate_parser.add_argument('--campaign', 
                               choices=['awakening', 'revelation', 'convergence'],
                               default='awakening',
                               help='Horror campaign type')
    generate_parser.add_argument('--format',
                               choices=['shorts', 'full', 'viral_series'],
                               default='shorts',
                               help='Video format')
    generate_parser.add_argument('--output', default='output', help='Output directory')
    
    # All command
    all_parser = subparsers.add_parser('all', help='Generate multiple horror videos')
    all_parser.add_argument('--count', type=int, default=3, help='Number of videos to generate')
    all_parser.add_argument('--output', default='output', help='Output directory')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    print("🔮 Oracle Horror Real Video Generation Engine")
    print("   Generating actual MP4 files with ElevenLabs voice synthesis")
    print()
    
    if args.command == 'test':
        success = test_system()
        sys.exit(0 if success else 1)
    
    elif args.command == 'generate':
        video_file = generate_single_video(args.campaign, args.format, args.output)
        sys.exit(0 if video_file else 1)
    
    elif args.command == 'all':
        videos = generate_multiple_videos(args.count, args.output)
        sys.exit(0 if videos else 1)

if __name__ == "__main__":
    main()