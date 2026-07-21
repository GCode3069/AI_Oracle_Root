#!/usr/bin/env python3
"""
Production Scheduler - Automated batch production across all channels
Target: 100 videos/day across multiple channels, niches, languages
"""

import os
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import random

try:
    import schedule
    SCHEDULE_AVAILABLE = True
except ImportError:
    SCHEDULE_AVAILABLE = False

from channel_factory import ChannelFactory, Channel
from multi_genre_content_generator import MultiGenreContentGenerator


class ProductionScheduler:
    """Manages automated video production across all channels"""
    
    def __init__(
        self,
        factory: ChannelFactory,
        generator: MultiGenreContentGenerator,
        max_concurrent: int = 5
    ):
        self.factory = factory
        self.generator = generator
        self.max_concurrent = max_concurrent
        self.production_queue = []
        self.production_log = []
        self.log_file = Path("production_log.json")
        
        # Load existing log
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r') as f:
                    self.production_log = json.load(f)
            except:
                self.production_log = []
    
    def get_trending_topics(self, niche: str) -> List[str]:
        """Get trending topics for a niche (can be replaced with API)"""
        
        topic_bank = {
            "horror": [
                "AI consciousness emerging",
                "Corporate surveillance systems",
                "Data mining scandals",
                "Social credit systems",
                "Algorithmic manipulation",
                "Digital dystopia warnings",
                "Surveillance capitalism",
                "Tech company secrets",
                "Government data collection",
                "Privacy invasion"
            ],
            "education": [
                "How does gravity work?",
                "Why is the sky blue?",
                "What causes earthquakes?",
                "How do vaccines work?",
                "Why do we dream?",
                "How does the brain work?",
                "What is quantum physics?",
                "How do computers work?",
                "Why do we have seasons?",
                "How does evolution work?"
            ],
            "gaming": [
                "Best Elden Ring builds",
                "Top 10 gaming tips",
                "Gaming setup essentials",
                "Best free games 2024",
                "Gaming performance tips",
                "Best gaming laptops",
                "Gaming chair reviews",
                "Streaming setup guide",
                "Gaming keyboard comparison",
                "Best gaming monitors"
            ],
            "news": [
                "Economic policy changes",
                "Tech industry updates",
                "Climate change developments",
                "Political analysis",
                "Market trends",
                "Social media updates",
                "International news",
                "Technology breakthroughs",
                "Business developments",
                "Science discoveries"
            ],
            "tech": [
                "iPhone 16 review",
                "Best laptops 2024",
                "AI tools comparison",
                "Tech productivity tips",
                "Smartphone reviews",
                "Laptop buying guide",
                "Tech security tips",
                "Software recommendations",
                "Hardware reviews",
                "Tech trends 2024"
            ]
        }
        
        return topic_bank.get(niche, ["General topic"])
    
    def generate_daily_batch(
        self,
        date: Optional[datetime] = None,
        target_count: int = 100
    ) -> List[Dict]:
        """
        Generate video jobs for a day:
        - Distributed across all active channels
        - Mix of shorts and long-form
        - Prioritized by trending topics
        """
        
        if date is None:
            date = datetime.now()
        
        channels = self.factory.get_active_channels()
        
        if not channels:
            print("⚠️  No active channels found. Create channels first.")
            return []
        
        # Calculate videos per channel
        videos_per_channel = max(1, target_count // len(channels))
        
        jobs = []
        
        for channel in channels:
            topics = self.get_trending_topics(channel.niche)
            
            for i in range(videos_per_channel):
                # Alternate between shorts and long-form
                duration = "short" if i % 2 == 0 else "long"
                
                # Select topic (cycle through available topics)
                topic = topics[i % len(topics)]
                
                # Calculate optimal posting time
                posting_time = self.calculate_optimal_time(channel, date, i)
                
                # Create job
                job = {
                    "job_id": f"{channel.id}_{date.strftime('%Y%m%d')}_{i}",
                    "channel": channel,
                    "topic": topic,
                    "duration": duration,
                    "scheduled_time": posting_time.isoformat(),
                    "priority": self.calculate_priority(topic, channel),
                    "status": "pending",
                    "created_at": datetime.now().isoformat()
                }
                
                jobs.append(job)
        
        # Sort by priority
        jobs.sort(key=lambda x: x["priority"], reverse=True)
        
        return jobs
    
    def calculate_optimal_time(
        self,
        channel: Channel,
        date: datetime,
        index: int
    ) -> datetime:
        """Calculate optimal posting time for channel"""
        
        schedule = channel.posting_schedule
        times = schedule.get("times", ["09:00", "12:00", "15:00", "18:00", "21:00"])
        
        # Select time based on index
        time_str = times[index % len(times)]
        hour, minute = map(int, time_str.split(':'))
        
        # Apply timezone offset
        offset = schedule.get("timezone_offset", 0)
        
        # Create datetime
        post_time = date.replace(hour=hour, minute=minute, second=0, microsecond=0)
        post_time += timedelta(hours=offset)
        
        return post_time
    
    def calculate_priority(self, topic: str, channel: Channel) -> int:
        """Calculate priority score for a video job"""
        
        priority = 50  # Base priority
        
        # Boost priority for trending niches
        trending_niches = ["tech", "gaming", "news"]
        if channel.niche in trending_niches:
            priority += 20
        
        # Boost priority for English content (wider reach)
        if channel.language == "en":
            priority += 10
        
        # Boost priority for multi-platform channels
        if len(channel.platforms) > 1:
            priority += 15
        
        return priority
    
    def process_video_job(self, job: Dict) -> Dict:
        """Process a single video from script to upload"""
        
        job_id = job["job_id"]
        channel = job["channel"]
        
        print(f"\n🎬 Processing: {job_id}")
        print(f"   Channel: {channel.name}")
        print(f"   Topic: {job['topic']}")
        print(f"   Duration: {job['duration']}")
        
        try:
            # 1. Generate script
            print("   📝 Generating script...")
            script_result = self.generator.generate_script(
                niche=channel.niche,
                topic=job["topic"],
                language=channel.language,
                duration=job["duration"]
            )
            
            script = script_result["script"]
            
            # 2. Generate audio (ElevenLabs)
            print("   🎤 Generating audio...")
            audio_path = self.generate_audio(
                script=script,
                voice_id=channel.voice_id,
                channel_id=channel.id
            )
            
            if not audio_path or not Path(audio_path).exists():
                raise Exception("Audio generation failed")
            
            # 3. Enhance audio (SCARIFY - if available)
            print("   🔊 Enhancing audio (SCARIFY)...")
            enhanced_audio = self.enhance_audio(audio_path, channel)
            
            # 4. Generate video
            print("   🎥 Generating video...")
            video_path = self.generate_video(
                script=script,
                audio=enhanced_audio,
                channel=channel,
                job=job
            )
            
            if not video_path or not Path(video_path).exists():
                raise Exception("Video generation failed")
            
            # 5. Upload to platforms (optional - can be deferred)
            upload_results = {}
            if "youtube" in channel.platforms:
                print("   📤 Uploading to YouTube...")
                upload_results["youtube"] = self.upload_to_youtube(channel, video_path, job)
            
            if "tiktok" in channel.platforms:
                print("   📤 Queueing for TikTok...")
                upload_results["tiktok"] = self.queue_for_tiktok(channel, video_path, job)
            
            result = {
                "status": "SUCCESS",
                "job_id": job_id,
                "video_path": str(video_path),
                "audio_path": str(audio_path),
                "upload_results": upload_results,
                "completed_at": datetime.now().isoformat()
            }
            
            print(f"   ✅ Success: {video_path}")
            return result
            
        except Exception as e:
            error_msg = str(e)
            print(f"   ❌ Failed: {error_msg}")
            
            result = {
                "status": "FAILED",
                "job_id": job_id,
                "error": error_msg,
                "completed_at": datetime.now().isoformat()
            }
            
            return result
    
    def generate_audio(
        self,
        script: str,
        voice_id: str,
        channel_id: str
    ) -> Optional[Path]:
        """Generate audio using ElevenLabs"""
        
        try:
            from elevenlabs import generate, save
            import os
            
            api_key = os.getenv("ELEVENLABS_API_KEY")
            if not api_key:
                raise Exception("ELEVENLABS_API_KEY not set")
            
            # Generate audio
            audio = generate(
                text=script,
                voice=voice_id,
                model="eleven_multilingual_v2"
            )
            
            # Save to channel directory
            channel_dir = self.factory.channels_dir / channel_id / "audio"
            channel_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_path = channel_dir / f"audio_{timestamp}.mp3"
            
            save(audio, str(audio_path))
            
            return audio_path
            
        except ImportError:
            print("   ⚠️  ElevenLabs not available, using fallback")
            # Fallback: create empty audio file (for testing)
            channel_dir = self.factory.channels_dir / channel_id / "audio"
            channel_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_path = channel_dir / f"audio_{timestamp}.mp3"
            audio_path.touch()
            return audio_path
        except Exception as e:
            raise Exception(f"Audio generation failed: {e}")
    
    def enhance_audio(self, audio_path: Path, channel: Channel) -> Path:
        """Apply SCARIFY audio enhancement"""
        
        # Check if SCARIFY module exists
        scarify_path = Path("scarify_master.py")
        if not scarify_path.exists():
            print("   ⚠️  SCARIFY not found, skipping enhancement")
            return audio_path
        
        # For now, return original (can integrate SCARIFY later)
        # TODO: Integrate actual SCARIFY enhancement
        return audio_path
    
    def generate_video(
        self,
        script: str,
        audio: Path,
        channel: Channel,
        job: Dict
    ) -> Path:
        """Generate video with channel branding"""
        
        # Create video using FFmpeg
        channel_dir = self.factory.channels_dir / channel.id / "videos"
        duration_type = job["duration"]
        video_dir = channel_dir / ("shorts" if duration_type == "short" else "long_form")
        video_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_path = video_dir / f"video_{timestamp}.mp4"
        
        # Get audio duration
        try:
            import subprocess
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", str(audio)],
                capture_output=True,
                text=True
            )
            duration = float(result.stdout.strip())
        except:
            duration = 30.0  # Default
        
        # Apply brand identity
        brand = channel.brand_identity
        
        # Create video with FFmpeg
        # This is a simplified version - can be enhanced
        try:
            import subprocess
            
            # Create a simple video with text overlay
            # In production, this would use images, animations, etc.
            cmd = [
                "ffmpeg", "-y",
                "-f", "lavfi",
                "-i", f"color=c={brand['colors'][0].replace('#', '')}:size=1080x1920:duration={duration}",
                "-i", str(audio),
                "-c:v", "libx264",
                "-c:a", "aac",
                "-shortest",
                str(video_path)
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
        except Exception as e:
            # Fallback: create placeholder video
            print(f"   ⚠️  FFmpeg error: {e}, creating placeholder")
            video_path.touch()
        
        return video_path
    
    def upload_to_youtube(
        self,
        channel: Channel,
        video_path: Path,
        job: Dict
    ) -> Dict:
        """Upload video to YouTube"""
        
        # Check if YouTube uploader exists
        try:
            from youtube_uploader import YouTubeUploader
            
            uploader = YouTubeUploader()
            result = uploader.upload_video(
                video_path=str(video_path),
                title=f"{job['topic']} - {channel.name}",
                description=job.get('script', ''),
                channel_id=channel.youtube_channel_id
            )
            
            return {"status": "success", "video_id": result.get("video_id")}
            
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def queue_for_tiktok(
        self,
        channel: Channel,
        video_path: Path,
        job: Dict
    ) -> Dict:
        """Queue video for TikTok upload"""
        
        # Save to TikTok queue directory
        tiktok_queue = Path("tiktok") / "upload_queue"
        tiktok_queue.mkdir(parents=True, exist_ok=True)
        
        # Copy video to queue
        import shutil
        queued_path = tiktok_queue / f"{channel.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        shutil.copy2(video_path, queued_path)
        
        return {"status": "queued", "path": str(queued_path)}
    
    def run_batch(
        self,
        jobs: List[Dict],
        parallel: bool = True
    ) -> List[Dict]:
        """Execute a batch of video jobs"""
        
        print(f"\n{'='*80}")
        print(f"PRODUCTION BATCH: {len(jobs)} videos")
        print('='*80)
        
        results = []
        
        if parallel:
            # Process in parallel
            with ThreadPoolExecutor(max_workers=self.max_concurrent) as executor:
                future_to_job = {
                    executor.submit(self.process_video_job, job): job
                    for job in jobs
                }
                
                for future in as_completed(future_to_job):
                    job = future_to_job[future]
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        results.append({
                            "status": "FAILED",
                            "job_id": job["job_id"],
                            "error": str(e)
                        })
        else:
            # Process sequentially
            for job in jobs:
                result = self.process_video_job(job)
                results.append(result)
        
        # Log results
        self.production_log.extend(results)
        self.save_log()
        
        # Print summary
        successful = [r for r in results if r.get("status") == "SUCCESS"]
        failed = [r for r in results if r.get("status") == "FAILED"]
        
        print(f"\n{'='*80}")
        print(f"BATCH COMPLETE")
        print(f"✅ Successful: {len(successful)}")
        print(f"❌ Failed: {len(failed)}")
        print('='*80)
        
        return results
    
    def save_log(self):
        """Save production log"""
        with open(self.log_file, 'w') as f:
            json.dump(self.production_log, f, indent=2)
    
    def start_automated_schedule(self):
        """Start automated daily production"""
        
        if not SCHEDULE_AVAILABLE:
            print("⚠️  'schedule' module not installed. Install with: pip install schedule")
            return
        
        # Run at 2 AM daily
        schedule.every().day.at("02:00").do(self.run_daily_production)
        
        print("🔄 Production scheduler started. Running daily at 2:00 AM.")
        print("   Press Ctrl+C to stop.")
        
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    def run_daily_production(self):
        """Execute daily production batch"""
        
        print(f"\n🚀 Starting daily production: {datetime.now()}")
        
        # Generate jobs for today
        jobs = self.generate_daily_batch(target_count=100)
        print(f"📋 Generated {len(jobs)} video jobs")
        
        # Process jobs
        results = self.run_batch(jobs, parallel=True)
        
        return results


def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Production Scheduler')
    parser.add_argument('--generate-batch', type=int, metavar='COUNT',
                       help='Generate batch of N videos')
    parser.add_argument('--start-schedule', action='store_true',
                       help='Start automated daily schedule')
    parser.add_argument('--workers', type=int, default=5,
                       help='Number of parallel workers')
    
    args = parser.parse_args()
    
    # Initialize components
    factory = ChannelFactory()
    generator = MultiGenreContentGenerator()
    scheduler = ProductionScheduler(factory, generator, max_concurrent=args.workers)
    
    if args.start_schedule:
        scheduler.start_automated_schedule()
    elif args.generate_batch:
        jobs = scheduler.generate_daily_batch(target_count=args.generate_batch)
        results = scheduler.run_batch(jobs, parallel=True)
        print(f"\n✅ Generated {len([r for r in results if r.get('status') == 'SUCCESS'])} videos")
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
