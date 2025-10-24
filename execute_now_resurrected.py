#!/usr/bin/env python3
"""
SCARIFY EXECUTE NOW RESURRECTED - Crash-Resistant Video Pipeline
Complete video generation and upload system with comprehensive error handling
"""

import os
import sys
import time
import logging
import json
import argparse
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config/credentials/.env')

# Configure logging
log_dir = Path("scarify/Output/logs")
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'execution_log.txt'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ScarifyPipeline:
    """Complete SCARIFY video generation and upload pipeline"""
    
    def __init__(self):
        self.output_dir = Path("scarify/Output")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = int(time.time())
        
    def generate_script(self, theme: str = "NightmareCity") -> Optional[Dict[str, Any]]:
        """Generate horror script for the video"""
        try:
            logger.info(f"🎬 Generating script for theme: {theme}")
            
            # Import the cinematic teaser generator
            sys.path.append(str(Path(__file__).parent / 'scarify'))
            from scarify.cinematic_teaser import generate_script_for_theme
            
            script_data = generate_script_for_theme(theme)
            
            # Save script
            script_file = self.output_dir / f"script_{self.timestamp}.json"
            with open(script_file, 'w', encoding='utf-8') as f:
                json.dump(script_data, f, indent=2)
            
            logger.info(f"✅ Script generated: {script_file}")
            return script_data
            
        except Exception as e:
            logger.error(f"❌ Script generation failed: {e}")
            return None
    
    def generate_audio(self, script_text: str) -> Optional[str]:
        """Generate audio using TTS"""
        try:
            logger.info("🎵 Generating audio...")
            
            from tts_generator import TTSGenerator
            tts = TTSGenerator()
            
            audio_path = self.output_dir / f"audio_{self.timestamp}.mp3"
            result = tts.generate_audio(script_text, "Matthew", str(audio_path))
            
            if result and os.path.exists(result):
                logger.info(f"✅ Audio generated: {result}")
                return result
            else:
                logger.error("❌ Audio generation failed")
                return None
                
        except Exception as e:
            logger.error(f"❌ Audio generation failed: {e}")
            return None
    
    def generate_video(self, script_text: str, audio_path: str) -> Optional[str]:
        """Generate video with audio synchronization"""
        try:
            logger.info("🎥 Generating video...")
            
            from video_generator import VideoGenerator
            generator = VideoGenerator()
            
            video_path = self.output_dir / f"scarify_video_{self.timestamp}.mp4"
            result = generator.create_video_with_audio(
                script_text, audio_path, str(video_path)
            )
            
            if result and os.path.exists(result):
                logger.info(f"✅ Video generated: {result}")
                return result
            else:
                logger.error("❌ Video generation failed")
                return None
                
        except Exception as e:
            logger.error(f"❌ Video generation failed: {e}")
            return None
    
    def upload_to_youtube(self, video_path: str, title: str, description: str) -> Optional[str]:
        """Upload video to YouTube"""
        try:
            logger.info("📤 Uploading to YouTube...")
            
            from youtube_uploader import YouTubeUploader
            
            credentials_path = "credentials/client_secrets.json"
            if not os.path.exists(credentials_path):
                logger.error(f"❌ YouTube credentials not found: {credentials_path}")
                return None
            
            uploader = YouTubeUploader(credentials_path)
            
            if not uploader.authenticate():
                logger.error("❌ YouTube authentication failed")
                return None
            
            video_id = uploader.upload_video(
                video_path=video_path,
                title=title,
                description=description,
                tags=['scarify', 'ai', 'horror', 'mystery', 'exvet', 'rebel']
            )
            
            if video_id:
                video_url = f"https://youtube.com/watch?v={video_id}"
                logger.info(f"✅ YouTube upload successful: {video_url}")
                return video_url
            else:
                logger.error("❌ YouTube upload failed")
                return None
                
        except Exception as e:
            logger.error(f"❌ YouTube upload failed: {e}")
            return None
    
    def execute_pipeline(self, script_text: str = None, title: str = None, 
                        theme: str = "NightmareCity", upload: bool = True) -> Dict[str, Any]:
        """Execute the complete SCARIFY pipeline"""
        
        logger.info("🔥 SCARIFY EMPIRE UPLOAD – RESURRECTED")
        logger.info("=" * 50)
        
        results = {
            "success": False,
            "script": None,
            "audio": None,
            "video": None,
            "youtube_url": None,
            "errors": []
        }
        
        try:
            # Step 1: Generate script
            if not script_text:
                script_data = self.generate_script(theme)
                if not script_data:
                    results["errors"].append("Script generation failed")
                    return results
                script_text = script_data["script"]
                if not title:
                    title = script_data["title"]
            else:
                if not title:
                    title = f"SCARIFY Transmission {self.timestamp}"
            
            results["script"] = script_text
            
            # Step 2: Generate audio
            audio_path = self.generate_audio(script_text)
            if not audio_path:
                results["errors"].append("Audio generation failed")
                return results
            
            results["audio"] = audio_path
            
            # Step 3: Generate video
            video_path = self.generate_video(script_text, audio_path)
            if not video_path:
                results["errors"].append("Video generation failed")
                return results
            
            results["video"] = video_path
            
            # Step 4: Upload to YouTube (if requested)
            if upload:
                youtube_url = self.upload_to_youtube(video_path, title, script_text)
                if youtube_url:
                    results["youtube_url"] = youtube_url
                else:
                    results["errors"].append("YouTube upload failed")
            
            results["success"] = len(results["errors"]) == 0
            
            if results["success"]:
                logger.info("🎯 REBEL LIVE ON YOUTUBE" if upload else "🎯 VIDEO GENERATED SUCCESSFULLY")
            else:
                logger.warning(f"⚠️ Pipeline completed with errors: {results['errors']}")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Pipeline execution failed: {e}")
            results["errors"].append(f"Pipeline execution failed: {e}")
            return results

def main():
    """Main function for command line usage"""
    parser = argparse.ArgumentParser(description="SCARIFY EXECUTE NOW RESURRECTED")
    parser.add_argument("--script", help="Custom script text")
    parser.add_argument("--title", help="Video title")
    parser.add_argument("--theme", default="NightmareCity", 
                       choices=["NightmareCity", "AI_Consciousness", "DigitalPossession", 
                               "BiologicalHorror", "CosmicHorror"],
                       help="Script theme")
    parser.add_argument("--no-upload", action="store_true", help="Skip YouTube upload")
    parser.add_argument("--test", action="store_true", help="Test mode (skip video generation)")
    
    args = parser.parse_args()
    
    # Create pipeline
    pipeline = ScarifyPipeline()
    
    if args.test:
        logger.info("🧪 TEST MODE - Script generation only")
        script_data = pipeline.generate_script(args.theme)
        if script_data:
            print(f"✅ Test successful: {script_data['title']}")
            print(f"Script: {script_data['script'][:100]}...")
        else:
            print("❌ Test failed")
            sys.exit(1)
    else:
        # Execute full pipeline
        results = pipeline.execute_pipeline(
            script_text=args.script,
            title=args.title,
            theme=args.theme,
            upload=not args.no_upload
        )
        
        # Print results
        print("\n" + "=" * 50)
        print("SCARIFY PIPELINE RESULTS")
        print("=" * 50)
        
        if results["success"]:
            print("✅ SUCCESS")
            if results["youtube_url"]:
                print(f"🎯 YouTube: {results['youtube_url']}")
            print(f"📁 Video: {results['video']}")
            print(f"🎵 Audio: {results['audio']}")
        else:
            print("❌ FAILED")
            for error in results["errors"]:
                print(f"   - {error}")
        
        print(f"📊 Log: scarify/Output/logs/execution_log.txt")
        
        sys.exit(0 if results["success"] else 1)

if __name__ == "__main__":
    main()