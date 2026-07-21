#!/usr/bin/env python3
"""
SCARIFY Master Generator
Complete pipeline: Script → Audio → Video → YouTube → TikTok
"""

import os
import sys
import json
import random
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List

# Import components
try:
    from upload.youtube_upload_enhanced import YouTubeUploaderEnhanced
    YOUTUBE_UPLOADER_AVAILABLE = True
except ImportError:
    YOUTUBE_UPLOADER_AVAILABLE = False
    print("⚠️  YouTube uploader not available")

try:
    from TIKTOK_AUTOMATION_SYSTEM import TikTokAutomationSystem
    TIKTOK_SYSTEM_AVAILABLE = True
except ImportError:
    TIKTOK_SYSTEM_AVAILABLE = False
    print("⚠️  TikTok system not available")


class ABEMasterGenerator:
    """Master generator that orchestrates the entire pipeline"""
    
    def __init__(self, base_path: Optional[Path] = None):
        """Initialize master generator"""
        if base_path is None:
            # Auto-detect project root
            current = Path(__file__).parent
            if (current / "abraham_horror").exists():
                base_path = current
            else:
                base_path = Path("/workspace")
        
        self.base_path = Path(base_path)
        self.abraham_horror_dir = self.base_path / "abraham_horror"
        self.output_dir = self.abraham_horror_dir / "generated_videos"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        if YOUTUBE_UPLOADER_AVAILABLE:
            self.youtube_uploader = YouTubeUploaderEnhanced(base_path)
        else:
            self.youtube_uploader = None
        
        if TIKTOK_SYSTEM_AVAILABLE:
            self.tiktok_system = TikTokAutomationSystem(base_path)
        else:
            self.tiktok_system = None
        
        # Load config
        self._load_config()
    
    def _load_config(self):
        """Load API keys and configuration"""
        config_file = self.base_path / "config" / "api_config.json"
        
        if config_file.exists():
            with open(config_file, 'r') as f:
                self.config = json.load(f)
        else:
            # Default config
            self.config = {
                "elevenlabs_api_key": os.getenv("ELEVENLABS_API_KEY", ""),
                "stability_api_key": os.getenv("STABILITY_API_KEY", ""),
                "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY", ""),
                "openai_api_key": os.getenv("OPENAI_API_KEY", "")
            }
        
        # Set API keys
        self.elevenlabs_key = self.config.get("elevenlabs_api_key", "")
        self.stability_key = self.config.get("stability_api_key", "")
        self.anthropic_key = self.config.get("anthropic_api_key", "")
    
    def generate_script(self, topic: Optional[str] = None) -> Dict:
        """
        Generate script using Claude API or fallback
        
        Args:
            topic: Optional topic/headline
        
        Returns:
            Dict with script text and metadata
        """
        print("\n" + "="*80)
        print("STEP 1: GENERATING SCRIPT")
        print("="*80)
        
        if topic is None:
            # Get topic from headlines or use default
            topic = self._get_topic()
        
        print(f"   Topic: {topic}")
        
        # Try Claude API first
        if self.anthropic_key:
            try:
                import anthropic
                client = anthropic.Anthropic(api_key=self.anthropic_key)
                
                prompt = f"""Generate a dark satirical script in the style of Abraham Lincoln as Max Headroom, commenting on: {topic}

Style requirements:
- Horror aesthetic (slasher, supernatural, psychological)
- Political/social commentary
- 45-60 seconds when read aloud
- Max Headroom glitch aesthetic
- Anti-establishment messaging
- Dark comedy tone

Format: Just the script text, no meta-commentary."""

                response = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1000,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                script_text = response.content[0].text.strip()
                print(f"   ✅ Script generated via Claude API")
                
                return {
                    "script": script_text,
                    "topic": topic,
                    "source": "claude_api",
                    "word_count": len(script_text.split())
                }
                
            except Exception as e:
                print(f"   ⚠️  Claude API failed: {e}")
        
        # Fallback: Use template-based generation
        return self._generate_template_script(topic)
    
    def _get_topic(self) -> str:
        """Get topic from various sources"""
        # Try to read from Google Sheets or headlines
        try:
            # This would integrate with your existing headline system
            topics = [
                "Corporate America's profit obsession",
                "Government shutdown day 15",
                "Market crash warnings",
                "Digital apocalypse",
                "Major cyber attack",
                "Recession signals",
                "Corporate greed exposed"
            ]
            return random.choice(topics)
        except:
            return "Corporate horror story"
    
    def _generate_template_script(self, topic: str) -> Dict:
        """Generate script using templates (fallback)"""
        templates = [
            f"Abraham Lincoln. Digitized. Corrupted. Reading: {topic}.",
            f"I led a civil war. You led a comment section. I freed slaves. You freed influencers.",
            f"This news cycle is a broken tape— rewind, play, distort, repeat.",
            f"I died in 1865. Your democracy died in a tweet thread.",
            f"Funding truth: Bitcoin below."
        ]
        
        script = " ".join(templates)
        
        return {
            "script": script,
            "topic": topic,
            "source": "template",
            "word_count": len(script.split())
        }
    
    def generate_audio(self, script: str, output_path: Optional[Path] = None) -> Optional[Path]:
        """
        Generate audio using ElevenLabs
        
        Args:
            script: Script text
            output_path: Optional output path
        
        Returns:
            Path to audio file or None
        """
        print("\n" + "="*80)
        print("STEP 2: GENERATING AUDIO")
        print("="*80)
        
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.abraham_horror_dir / "audio" / f"audio_{timestamp}.mp3"
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.elevenlabs_key:
            print("   ❌ ElevenLabs API key not configured")
            return None
        
        try:
            import requests
            
            # Use Jiminex voice ID (or your preferred voice)
            voice_id = "VR6AewLTigWG4xSOukaG"  # Deep male voice
            
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.elevenlabs_key
            }
            
            data = {
                "text": script,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.35,
                    "similarity_boost": 0.85,
                    "style": 0.9,
                    "use_speaker_boost": True
                }
            }
            
            print(f"   Generating audio with ElevenLabs...")
            response = requests.post(url, json=data, headers=headers, timeout=240)
            
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                print(f"   ✅ Audio generated: {output_path.name}")
                return output_path
            else:
                print(f"   ❌ ElevenLabs failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ Audio generation failed: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def generate_image(self, topic: str, output_path: Optional[Path] = None) -> Optional[Path]:
        """
        Generate image using Stability AI
        
        Args:
            topic: Image topic/description
            output_path: Optional output path
        
        Returns:
            Path to image file or None
        """
        print("\n" + "="*80)
        print("STEP 3: GENERATING IMAGE")
        print("="*80)
        
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.abraham_horror_dir / "images" / f"image_{timestamp}.png"
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.stability_key:
            print("   ⚠️  Stability API key not configured. Using placeholder image.")
            return self._get_placeholder_image(output_path)
        
        try:
            import requests
            
            prompt = f"Abraham Lincoln as Max Headroom, glitch aesthetic, horror, {topic}, dark, CRT TV, VHS degradation, analog horror"
            
            url = "https://api.stability.ai/v2beta/stable-image/generate/core"
            
            headers = {
                "Authorization": f"Bearer {self.stability_key}",
                "Accept": "image/png"
            }
            
            data = {
                "prompt": prompt,
                "aspect_ratio": "9:16",
                "output_format": "png"
            }
            
            print(f"   Generating image with Stability AI...")
            response = requests.post(url, headers=headers, data=data, timeout=60)
            
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                print(f"   ✅ Image generated: {output_path.name}")
                return output_path
            else:
                print(f"   ⚠️  Stability AI failed: {response.status_code}. Using placeholder.")
                return self._get_placeholder_image(output_path)
                
        except Exception as e:
            print(f"   ⚠️  Image generation failed: {e}. Using placeholder.")
            return self._get_placeholder_image(output_path)
    
    def _get_placeholder_image(self, output_path: Path) -> Path:
        """Get or create placeholder image"""
        # Try to find existing Lincoln image
        lincoln_images = list(self.abraham_horror_dir.glob("**/*lincoln*.jpg")) + \
                        list(self.abraham_horror_dir.glob("**/*lincoln*.png"))
        
        if lincoln_images:
            import shutil
            shutil.copy2(lincoln_images[0], output_path)
            print(f"   ✅ Using existing image: {lincoln_images[0].name}")
            return output_path
        
        # Create simple placeholder
        try:
            from PIL import Image, ImageDraw
            img = Image.new('RGB', (1080, 1920), color=(10, 5, 15))
            draw = ImageDraw.Draw(img)
            draw.text((540, 960), "ABRAHAM LINCOLN", fill=(255, 0, 0), anchor="mm")
            img.save(output_path)
            print(f"   ✅ Created placeholder image")
            return output_path
        except:
            return output_path
    
    def create_video(
        self,
        audio_path: Path,
        image_path: Path,
        output_path: Optional[Path] = None
    ) -> Optional[Path]:
        """
        Create video using FFmpeg
        
        Args:
            audio_path: Path to audio file
            image_path: Path to image file
            output_path: Optional output path
        
        Returns:
            Path to video file or None
        """
        print("\n" + "="*80)
        print("STEP 4: CREATING VIDEO")
        print("="*80)
        
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"ABRAHAM_{timestamp}.mp4"
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Optimize image first (prevents FFmpeg timeout)
        optimized_image = self._optimize_image(image_path)
        
        try:
            # Get audio duration
            import subprocess
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)],
                capture_output=True,
                text=True,
                timeout=10
            )
            duration = float(result.stdout.strip())
            
            print(f"   Audio duration: {duration:.1f}s")
            print(f"   Creating video with FFmpeg...")
            
            # Create video with FFmpeg
            cmd = [
                "ffmpeg", "-y",
                "-loop", "1",
                "-i", str(optimized_image),
                "-i", str(audio_path),
                "-c:v", "libx264",
                "-tune", "stillimage",
                "-c:a", "aac",
                "-b:a", "192k",
                "-pix_fmt", "yuv420p",
                "-shortest",
                "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
                "-r", "30",
                "-movflags", "+faststart",  # Faststart for web playback
                str(output_path)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=300,  # 5 minute timeout
                text=True
            )
            
            if result.returncode == 0 and output_path.exists():
                print(f"   ✅ Video created: {output_path.name}")
                return output_path
            else:
                print(f"   ❌ FFmpeg failed: {result.stderr[:200]}")
                return None
                
        except subprocess.TimeoutExpired:
            print(f"   ❌ FFmpeg timeout (image may be too large)")
            return None
        except Exception as e:
            print(f"   ❌ Video creation failed: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _optimize_image(self, image_path: Path) -> Path:
        """Pre-optimize image to prevent FFmpeg timeout"""
        optimized_path = image_path.parent / f"optimized_{image_path.name}"
        
        try:
            cmd = [
                "ffmpeg", "-y",
                "-i", str(image_path),
                "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease",
                "-q:v", "2",
                str(optimized_path)
            ]
            
            subprocess.run(cmd, capture_output=True, timeout=30)
            
            if optimized_path.exists():
                return optimized_path
        except:
            pass
        
        return image_path  # Return original if optimization fails
    
    def generate_complete_video(
        self,
        topic: Optional[str] = None,
        upload_youtube: bool = False,
        upload_tiktok: bool = False
    ) -> Dict:
        """
        Complete pipeline: Script → Audio → Image → Video → Upload
        
        Args:
            topic: Optional topic
            upload_youtube: Upload to YouTube after generation
            upload_tiktok: Upload to TikTok after generation
        
        Returns:
            Dict with all results
        """
        results = {
            "topic": topic,
            "script": None,
            "audio": None,
            "image": None,
            "video": None,
            "youtube_url": None,
            "tiktok_url": None,
            "success": False
        }
        
        try:
            # Step 1: Generate script
            script_data = self.generate_script(topic)
            results["script"] = script_data["script"]
            results["topic"] = script_data["topic"]
            
            # Step 2: Generate audio
            audio_path = self.generate_audio(script_data["script"])
            if not audio_path:
                return {**results, "error": "Audio generation failed"}
            results["audio"] = str(audio_path)
            
            # Step 3: Generate image
            image_path = self.generate_image(script_data["topic"])
            if not image_path:
                return {**results, "error": "Image generation failed"}
            results["image"] = str(image_path)
            
            # Step 4: Create video
            video_path = self.create_video(audio_path, image_path)
            if not video_path:
                return {**results, "error": "Video creation failed"}
            results["video"] = str(video_path)
            
            # Step 5: Upload to YouTube (if requested)
            if upload_youtube and self.youtube_uploader:
                print("\n" + "="*80)
                print("STEP 5: UPLOADING TO YOUTUBE")
                print("="*80)
                
                title = f"{script_data['topic']} | Abraham Lincoln Horror #Shorts"
                description = script_data["script"][:500]
                tags = ["shorts", "youtube shorts", "horror", "abraham lincoln", "max headroom"]
                
                upload_result = self.youtube_uploader.upload_video(
                    video_path=str(video_path),
                    title=title,
                    description=description,
                    tags=tags
                )
                
                if upload_result.get("status") == "SUCCESS":
                    results["youtube_url"] = upload_result.get("url")
            
            # Step 6: Upload to TikTok (if requested)
            if upload_tiktok and self.tiktok_system:
                print("\n" + "="*80)
                print("STEP 6: UPLOADING TO TIKTOK")
                print("="*80)
                
                tiktok_result = self.tiktok_system.process_video(
                    input_video=str(video_path),
                    topic=script_data["topic"],
                    auto_upload=True
                )
                
                if tiktok_result.get("uploaded"):
                    results["tiktok_url"] = tiktok_result.get("url")
            
            results["success"] = True
            return results
            
        except Exception as e:
            return {**results, "error": str(e)}
    
    def batch_generate(
        self,
        count: int = 5,
        upload_youtube: bool = False,
        upload_tiktok: bool = False
    ) -> List[Dict]:
        """Generate multiple videos"""
        print(f"\n🎬 BATCH GENERATION: {count} videos")
        
        results = []
        for i in range(count):
            print(f"\n{'='*80}")
            print(f"VIDEO {i+1}/{count}")
            print('='*80)
            
            result = self.generate_complete_video(
                upload_youtube=upload_youtube,
                upload_tiktok=upload_tiktok
            )
            results.append(result)
            
            if result.get("success"):
                print(f"\n✅ Video {i+1} complete!")
            else:
                print(f"\n❌ Video {i+1} failed: {result.get('error')}")
            
            # Wait between videos
            if i < count - 1:
                import time
                wait_time = 30
                print(f"\n⏳ Waiting {wait_time}s before next video...")
                time.sleep(wait_time)
        
        successful = sum(1 for r in results if r.get("success"))
        print(f"\n{'='*80}")
        print(f"BATCH COMPLETE: {successful}/{count} successful")
        print('='*80)
        
        return results


def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='SCARIFY Master Generator')
    parser.add_argument('--batch', type=int, help='Generate batch of videos', metavar='COUNT')
    parser.add_argument('--topic', help='Video topic/headline')
    parser.add_argument('--youtube', action='store_true', help='Upload to YouTube')
    parser.add_argument('--tiktok', action='store_true', help='Upload to TikTok')
    parser.add_argument('--both', action='store_true', help='Upload to both platforms')
    
    args = parser.parse_args()
    
    generator = ABEMasterGenerator()
    
    if args.batch:
        upload_youtube = args.youtube or args.both
        upload_tiktok = args.tiktok or args.both
        
        results = generator.batch_generate(
            count=args.batch,
            upload_youtube=upload_youtube,
            upload_tiktok=upload_tiktok
        )
        
        print(f"\n✅ Generated {len(results)} videos")
    else:
        upload_youtube = args.youtube or args.both
        upload_tiktok = args.tiktok or args.both
        
        result = generator.generate_complete_video(
            topic=args.topic,
            upload_youtube=upload_youtube,
            upload_tiktok=upload_tiktok
        )
        
        if result.get("success"):
            print(f"\n✅ Video generated successfully!")
            if result.get("youtube_url"):
                print(f"   YouTube: {result['youtube_url']}")
            if result.get("tiktok_url"):
                print(f"   TikTok: {result['tiktok_url']}")
        else:
            print(f"\n❌ Generation failed: {result.get('error')}")
            sys.exit(1)


if __name__ == '__main__':
    main()
