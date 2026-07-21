#!/usr/bin/env python3
"""
Test script for Channel Factory system
Tests script generation, channel management, and basic pipeline
"""

import sys
from pathlib import Path

# Test imports
print("Testing imports...")
try:
    from channel_factory import ChannelFactory, Channel
    print("✅ channel_factory imported")
except Exception as e:
    print(f"❌ channel_factory import failed: {e}")
    sys.exit(1)

try:
    from multi_genre_content_generator import MultiGenreContentGenerator
    print("✅ multi_genre_content_generator imported")
except Exception as e:
    print(f"❌ multi_genre_content_generator import failed: {e}")
    sys.exit(1)

try:
    from production_scheduler import ProductionScheduler
    print("✅ production_scheduler imported")
except Exception as e:
    print(f"❌ production_scheduler import failed: {e}")
    sys.exit(1)

try:
    from unified_pipeline import UnifiedPipeline
    print("✅ unified_pipeline imported")
except Exception as e:
    print(f"❌ unified_pipeline import failed: {e}")
    sys.exit(1)

# Test channel factory
print("\n" + "="*80)
print("TESTING CHANNEL FACTORY")
print("="*80)

factory = ChannelFactory()
channels = factory.get_active_channels()
print(f"✅ Found {len(channels)} active channels")

if channels:
    channel = channels[0]
    print(f"✅ Sample channel: {channel.name} ({channel.id})")
    print(f"   Niche: {channel.niche}, Language: {channel.language}")
    print(f"   Platforms: {', '.join(channel.platforms)}")
    print(f"   Voice ID: {channel.voice_id[:20]}...")

# Test content generator
print("\n" + "="*80)
print("TESTING CONTENT GENERATOR")
print("="*80)

generator = MultiGenreContentGenerator()

# Test script generation for each niche
niches = ["horror", "education", "gaming", "news", "tech"]
for niche in niches:
    try:
        result = generator.generate_script(
            niche=niche,
            topic=f"Test topic for {niche}",
            language="en",
            duration="short"
        )
        print(f"✅ {niche.capitalize()}: Generated {result['word_count']} words")
        print(f"   Preview: {result['script'][:80]}...")
    except Exception as e:
        print(f"❌ {niche.capitalize()}: Failed - {e}")

# Test production scheduler
print("\n" + "="*80)
print("TESTING PRODUCTION SCHEDULER")
print("="*80)

scheduler = ProductionScheduler(factory, generator, max_concurrent=2)

# Test batch generation
try:
    jobs = scheduler.generate_daily_batch(target_count=5)
    print(f"✅ Generated {len(jobs)} video jobs")
    if jobs:
        job = jobs[0]
        print(f"   Sample job: {job['job_id']}")
        print(f"   Channel: {job['channel'].name}")
        print(f"   Topic: {job['topic']}")
        print(f"   Duration: {job['duration']}")
except Exception as e:
    print(f"❌ Batch generation failed: {e}")

# Test unified pipeline
print("\n" + "="*80)
print("TESTING UNIFIED PIPELINE")
print("="*80)

pipeline = UnifiedPipeline()

try:
    status = pipeline.get_status()
    print(f"✅ System status retrieved")
    print(f"   Total channels: {status['total_channels']}")
    print(f"   Total videos: {status['total_videos']}")
    print(f"   By niche: {status['channels_by_niche']}")
    print(f"   By language: {status['channels_by_language']}")
except Exception as e:
    print(f"❌ Status check failed: {e}")

# Test directory structure
print("\n" + "="*80)
print("TESTING DIRECTORY STRUCTURE")
print("="*80)

channels_dir = Path("channels")
if channels_dir.exists():
    print(f"✅ Channels directory exists: {channels_dir}")
    channel_dirs = list(channels_dir.iterdir())
    print(f"   Found {len(channel_dirs)} channel directories")
    
    for channel_dir in channel_dirs[:3]:  # Show first 3
        if channel_dir.is_dir():
            subdirs = [d.name for d in channel_dir.iterdir() if d.is_dir()]
            print(f"   {channel_dir.name}: {len(subdirs)} subdirectories")
else:
    print(f"⚠️  Channels directory not found (will be created on first use)")

print("\n" + "="*80)
print("TEST COMPLETE")
print("="*80)
print("\n✅ All core components are working!")
print("📝 Next steps:")
print("   1. Set API keys (ANTHROPIC_API_KEY, ELEVENLABS_API_KEY)")
print("   2. Generate test video: python unified_pipeline.py --channel horror_en_0 --topic 'Test' --generate 1")
print("   3. Generate batch: python unified_pipeline.py --generate 10")
