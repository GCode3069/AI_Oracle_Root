#!/usr/bin/env python3
"""
Unified Video Production Pipeline
Integrates Channel Factory + Content Generator + Production Scheduler
Works with existing SCARIFY system
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict

from channel_factory import ChannelFactory, Channel
from multi_genre_content_generator import MultiGenreContentGenerator
from production_scheduler import ProductionScheduler


class UnifiedPipeline:
    """
    Unified pipeline that connects everything:
    - Channel management
    - Content generation
    - Video production
    - Multi-platform deployment
    """
    
    def __init__(self, root_path: Optional[Path] = None):
        self.factory = ChannelFactory(root_path)
        self.generator = MultiGenreContentGenerator()
        self.scheduler = ProductionScheduler(
            factory=self.factory,
            generator=self.generator,
            max_concurrent=5
        )
    
    def create_channel_setup(
        self,
        name: str,
        niche: str,
        language: str,
        platforms: list,
        youtube_channel_id: Optional[str] = None
    ) -> Channel:
        """Quick channel creation"""
        return self.factory.create_channel(
            name=name,
            niche=niche,
            language=language,
            platforms=platforms,
            youtube_channel_id=youtube_channel_id
        )
    
    def generate_single_video(
        self,
        channel_id: str,
        topic: str,
        duration: str = "short"
    ) -> Dict:
        """Generate a single video for a channel"""
        
        channel = self.factory.get_channel(channel_id)
        if not channel:
            raise ValueError(f"Channel {channel_id} not found")
        
        # Create job
        job = {
            "job_id": f"{channel_id}_{topic}_{duration}",
            "channel": channel,
            "topic": topic,
            "duration": duration,
            "scheduled_time": None,
            "priority": 100
        }
        
        # Process video
        result = self.scheduler.process_video_job(job)
        
        return result
    
    def generate_batch_for_channel(
        self,
        channel_id: str,
        count: int = 10
    ) -> list:
        """Generate multiple videos for a specific channel"""
        
        channel = self.factory.get_channel(channel_id)
        if not channel:
            raise ValueError(f"Channel {channel_id} not found")
        
        topics = self.scheduler.get_trending_topics(channel.niche)
        
        jobs = []
        for i in range(count):
            job = {
                "job_id": f"{channel_id}_batch_{i}",
                "channel": channel,
                "topic": topics[i % len(topics)],
                "duration": "short" if i % 2 == 0 else "long",
                "scheduled_time": None,
                "priority": 100 - i
            }
            jobs.append(job)
        
        results = self.scheduler.run_batch(jobs, parallel=True)
        return results
    
    def setup_default_channels(self) -> list:
        """Setup the default 10-channel system"""
        
        default_channels = [
            ("Dark Truth", "horror", "en", ["youtube", "tiktok"]),
            ("Verdades Oscuras", "horror", "es", ["youtube", "tiktok"]),
            ("Vérités Sombres", "horror", "fr", ["youtube"]),
            ("Quick Facts Daily", "education", "en", ["youtube", "instagram"]),
            ("Datos Rápidos", "education", "es", ["youtube"]),
            ("Game Breakdown", "gaming", "en", ["youtube", "tiktok"]),
            ("Análisis Gaming", "gaming", "es", ["tiktok"]),
            ("Tech Insights", "tech", "en", ["youtube"]),
            ("News Flash", "news", "en", ["youtube", "twitter"]),
            ("Noticias Flash", "news", "es", ["youtube"])
        ]
        
        channels = []
        for name, niche, lang, platforms in default_channels:
            channel = self.create_channel_setup(name, niche, lang, platforms)
            channels.append(channel)
        
        return channels
    
    def generate_daily_batch(self, target_count: int = 100) -> list:
        """Generate daily batch across all channels"""
        jobs = self.scheduler.generate_daily_batch(target_count=target_count)
        results = self.scheduler.run_batch(jobs, parallel=True)
        return results
    
    def get_status(self) -> Dict:
        """Get system status"""
        
        channels = self.factory.get_active_channels()
        
        # Count videos by channel
        video_counts = {}
        for channel in channels:
            channel_dir = self.factory.channels_dir / channel.id / "videos"
            shorts = len(list((channel_dir / "shorts").glob("*.mp4"))) if (channel_dir / "shorts").exists() else 0
            long_form = len(list((channel_dir / "long_form").glob("*.mp4"))) if (channel_dir / "long_form").exists() else 0
            video_counts[channel.id] = {"shorts": shorts, "long_form": long_form, "total": shorts + long_form}
        
        return {
            "total_channels": len(channels),
            "channels_by_niche": {
                niche: len(self.factory.get_channels_by_niche(niche))
                for niche in ["horror", "education", "gaming", "news", "tech"]
            },
            "channels_by_language": {
                lang: len(self.factory.get_channels_by_language(lang))
                for lang in ["en", "es", "fr", "de"]
            },
            "video_counts": video_counts,
            "total_videos": sum(v["total"] for v in video_counts.values())
        }


def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Unified Video Production Pipeline')
    parser.add_argument('--setup', action='store_true',
                       help='Setup default 10-channel system')
    parser.add_argument('--status', action='store_true',
                       help='Show system status')
    parser.add_argument('--generate', type=int, metavar='COUNT',
                       help='Generate N videos across all channels')
    parser.add_argument('--channel', type=str, metavar='CHANNEL_ID',
                       help='Generate videos for specific channel')
    parser.add_argument('--topic', type=str, metavar='TOPIC',
                       help='Topic for single video generation')
    
    args = parser.parse_args()
    
    pipeline = UnifiedPipeline()
    
    if args.setup:
        print("\n🏭 Setting up default channel system...")
        channels = pipeline.setup_default_channels()
        print(f"✅ Created {len(channels)} channels")
        pipeline.factory.list_channels()
    
    elif args.status:
        status = pipeline.get_status()
        print(f"\n{'='*80}")
        print("SYSTEM STATUS")
        print('='*80)
        print(f"Total Channels: {status['total_channels']}")
        print(f"Total Videos: {status['total_videos']}")
        print(f"\nBy Niche: {status['channels_by_niche']}")
        print(f"By Language: {status['channels_by_language']}")
        print(f"\nVideo Counts:")
        for channel_id, counts in status['video_counts'].items():
            print(f"  {channel_id}: {counts['total']} videos ({counts['shorts']} shorts, {counts['long_form']} long)")
    
    elif args.generate:
        print(f"\n🎬 Generating {args.generate} videos...")
        results = pipeline.generate_daily_batch(target_count=args.generate)
        successful = len([r for r in results if r.get("status") == "SUCCESS"])
        print(f"✅ Generated {successful}/{len(results)} videos successfully")
    
    elif args.channel and args.topic:
        print(f"\n🎬 Generating video for channel {args.channel}...")
        result = pipeline.generate_single_video(args.channel, args.topic)
        if result.get("status") == "SUCCESS":
            print(f"✅ Video created: {result.get('video_path')}")
        else:
            print(f"❌ Failed: {result.get('error')}")
    
    elif args.channel:
        print(f"\n🎬 Generating batch for channel {args.channel}...")
        results = pipeline.generate_batch_for_channel(args.channel, count=10)
        successful = len([r for r in results if r.get("status") == "SUCCESS"])
        print(f"✅ Generated {successful}/{len(results)} videos successfully")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
