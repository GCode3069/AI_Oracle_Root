#!/usr/bin/env python3
"""
SCARIFY Halloween Blitzkrieg - 72-Hour Psychological Operation
Combines Chapman 2025 fears with Lincoln's ghost train narrative
$10K revenue target via 15-channel YouTube deployment
"""

import random
import yaml
import os
import time
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    from moviepy.editor import (
        VideoFileClip, AudioFileClip, CompositeVideoClip, 
        CompositeAudioClip, TextClip
    )
    from moviepy.audio.fx.all import audio_fadein, audio_fadeout, audio_loop
    from moviepy.video.fx.all import colorx, freeze, fadein, fadeout
except ImportError:
    print("⚠️  MoviePy not installed. Installing...")
    os.system(f"{sys.executable} -m pip install moviepy -q")
    from moviepy.editor import (
        VideoFileClip, AudioFileClip, CompositeVideoClip, 
        CompositeAudioClip, TextClip
    )

# Configuration
BASE_DIR = Path(__file__).parent.parent
CONFIGS_DIR = BASE_DIR / "configs"
AUDIO_DIR = BASE_DIR / "audio"
ASSETS_DIR = BASE_DIR / "assets"
OUTPUTS_DIR = BASE_DIR / "outputs"
ACCOUNTS_DIR = BASE_DIR / "accounts"

# Ensure directories exist
for dir_path in [OUTPUTS_DIR, AUDIO_DIR / "generated"]:
    dir_path.mkdir(parents=True, exist_ok=True)


class ElevenLabsWrapper:
    """Wrapper for ElevenLabs TTS with fallback"""
    
    def __init__(self):
        self.api_key = os.getenv('ELEVENLABS_API_KEY')
        self.available = self.api_key is not None
        
        if self.available:
            try:
                from elevenlabs import generate, set_api_key
                set_api_key(self.api_key)
                self.generate = generate
            except ImportError:
                print("⚠️  ElevenLabs not installed, using fallback")
                self.available = False
    
    def generate_audio(self, text, voice='Adam', model='eleven_monolingual_v1'):
        """Generate audio with ElevenLabs or fallback"""
        output_path = AUDIO_DIR / "generated" / f"tts_{int(time.time())}.mp3"
        
        if self.available:
            try:
                audio = self.generate(
                    text=text,
                    voice=voice,
                    model=model
                )
                with open(output_path, 'wb') as f:
                    f.write(audio)
                return str(output_path)
            except Exception as e:
                print(f"⚠️  ElevenLabs error: {e}, using fallback")
        
        # Fallback: Create silent audio placeholder
        print("📝 Using silent audio placeholder")
        return self._create_silent_audio(str(output_path), duration=5.0)
    
    def _create_silent_audio(self, output_path, duration=5.0):
        """Create silent audio file as fallback"""
        from moviepy.editor import AudioClip
        import numpy as np
        
        def make_frame(t):
            return np.array([0, 0])  # Stereo silence
        
        audio = AudioClip(make_frame, duration=duration, fps=44100)
        audio.write_audiofile(output_path, fps=44100, verbose=False, logger=None)
        return output_path


class ScarifyBlitz:
    """Main SCARIFY Halloween Blitzkrieg controller"""
    
    def __init__(self):
        self.load_config()
        self.tts = ElevenLabsWrapper()
        self.clips_generated = 0
        self.clips_uploaded = 0
        
    def load_config(self):
        """Load Chapman fears and channel configuration"""
        with open(CONFIGS_DIR / "chapman_2025.yaml", 'r') as f:
            config = yaml.safe_load(f)
            self.fears = config['top_fears']
            self.audio_specs = config['audio_specs']
            self.visual_specs = config['visual_specs']
            
        with open(ACCOUNTS_DIR / "channels.yaml", 'r') as f:
            channel_config = yaml.safe_load(f)
            self.channels = channel_config['channels']
            self.upload_strategy = channel_config['upload_strategy']
    
    def generate_phantom_train_clip(self, fear_key='corrupt_gov', base_clip=None):
        """
        Generate psychological warfare clip with Lincoln's ghost train narrative
        
        Args:
            fear_key: Which Chapman fear to target
            base_clip: Path to base video (optional)
            
        Returns:
            Path to generated clip
        """
        print(f"\n🎬 Generating {fear_key} phantom train clip...")
        
        fear = self.fears[fear_key]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = OUTPUTS_DIR / f"blitz_{fear_key}_{timestamp}.mp4"
        
        try:
            # Use base clip or create black background
            if base_clip and os.path.exists(base_clip):
                clip = VideoFileClip(base_clip).subclip(0, self.visual_specs['duration'])
            else:
                # Create black background clip
                from moviepy.editor import ColorClip
                clip = ColorClip(
                    size=(1080, 1920),
                    color=(0, 0, 0),
                    duration=self.visual_specs['duration']
                )
            
            # Visual effects: Silver-glitch-red color grade
            glitched = clip.fx(colorx, 1.2)
            
            # Add text overlay with fear prompt
            txt_clip = TextClip(
                fear['prompt'],
                fontsize=40,
                color='white',
                font='Arial-Bold',
                size=(1000, None),
                method='caption'
            ).set_position('center').set_duration(clip.duration)
            
            # Composite video
            video_with_text = CompositeVideoClip([glitched, txt_clip])
            
            # Audio: Theta rattle + TTS whisper
            audio_components = []
            
            # Base theta rattle (if exists)
            rattle_path = AUDIO_DIR / "heartbeat_rattle.wav"
            if rattle_path.exists():
                rattle = AudioFileClip(str(rattle_path))
                rattle = rattle.fx(audio_loop, n=int(clip.duration / rattle.duration) + 1)
                rattle = rattle.subclip(0, clip.duration).volumex(self.audio_specs['base_volume'])
                audio_components.append(rattle)
            
            # TTS generation
            print(f"   🎙️  Generating TTS: {fear['prompt'][:50]}...")
            tts_path = self.tts.generate_audio(fear['prompt'], voice='Adam')
            
            if os.path.exists(tts_path):
                tts_audio = AudioFileClip(tts_path)
                tts_audio = tts_audio.fx(audio_fadein, self.audio_specs['fade_in'])
                tts_audio = tts_audio.volumex(self.audio_specs['tts_volume'])
                tts_audio = tts_audio.set_start(self.audio_specs['spike_timing'])
                audio_components.append(tts_audio)
            
            # Composite audio
            if audio_components:
                final_audio = CompositeAudioClip(audio_components)
                final_clip = video_with_text.set_audio(final_audio)
            else:
                final_clip = video_with_text
            
            # Write output
            print(f"   💾 Writing to {output_path.name}...")
            final_clip.write_videofile(
                str(output_path),
                fps=self.visual_specs['fps'],
                codec='libx264',
                audio_codec='aac',
                temp_audiofile=str(OUTPUTS_DIR / 'temp_audio.m4a'),
                remove_temp=True,
                verbose=False,
                logger=None
            )
            
            self.clips_generated += 1
            print(f"   ✅ Generated: {output_path}")
            return str(output_path)
            
        except Exception as e:
            print(f"   ❌ Error generating clip: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def upload_to_youtube(self, video_path, fear_key, channel):
        """
        Upload clip to YouTube with optimized metadata
        
        Args:
            video_path: Path to video file
            fear_key: Fear type for metadata
            channel: Channel configuration dict
            
        Returns:
            YouTube URL or None
        """
        print(f"\n📤 Uploading to {channel['name']}...")
        
        fear = self.fears[fear_key]
        
        # Metadata optimization
        title = f"{fear['name']}: Don't Scroll Past #HalloweenPsyOp #Shorts"
        description = f"""{fear['prompt']}

Chapman 2025 Survey: {fear['prevalence']}% of Americans fear this.

{fear['retention_hook']}

💰 Support: bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh

#SCARIFYBLITZ #Halloween2025 #PsychologicalHorror #LincolnGhost
"""
        
        tags = [
            'halloween horror',
            'shorts',
            'psychological horror',
            'lincoln ghost',
            'government corruption',
            'cognitohazard',
            'scarify'
        ]
        
        # Try to use existing YouTube uploader
        try:
            sys.path.append(str(BASE_DIR.parent))
            from youtube_uploader import YouTubeUploader
            
            uploader = YouTubeUploader()
            url = uploader.upload(video_path, fear['prompt'])
            
            if url:
                self.clips_uploaded += 1
                print(f"   ✅ Uploaded: {url}")
                return url
        except Exception as e:
            print(f"   ⚠️  Upload error: {e}")
        
        print(f"   📝 Metadata prepared for manual upload:")
        print(f"   Title: {title}")
        print(f"   Description: {description[:100]}...")
        return None
    
    def run_blitz_cycle(self, duration_hours=72, clips_per_hour=5):
        """
        Run the 72-hour blitzkrieg cycle
        
        Args:
            duration_hours: Total duration of operation
            clips_per_hour: Number of clips to generate per hour
        """
        print("\n" + "="*80)
        print("🔥 SCARIFY HALLOWEEN BLITZKRIEG - 72 HOUR OPERATION")
        print("="*80)
        print(f"Duration: {duration_hours} hours")
        print(f"Clips/hour: {clips_per_hour}")
        print(f"Total clips: {duration_hours * clips_per_hour}")
        print(f"Channels: {len(self.channels)}")
        print("="*80)
        
        fear_keys = list(self.fears.keys())
        total_cycles = duration_hours
        
        for hour in range(total_cycles):
            print(f"\n⏰ HOUR {hour + 1}/{total_cycles}")
            
            # Generate clips for this hour
            for clip_num in range(clips_per_hour):
                # Rotate through fears
                fear_key = fear_keys[clip_num % len(fear_keys)]
                
                # Generate clip
                video_path = self.generate_phantom_train_clip(fear_key)
                
                if video_path:
                    # Select random channel
                    channel = random.choice(self.channels)
                    
                    # Upload
                    self.upload_to_youtube(video_path, fear_key, channel)
                
                # Brief pause between clips
                time.sleep(2)
            
            # Hourly summary
            print(f"\n📊 Hour {hour + 1} Summary:")
            print(f"   Generated: {self.clips_generated}")
            print(f"   Uploaded: {self.clips_uploaded}")
            
            # Wait until next hour (unless last hour)
            if hour < total_cycles - 1:
                print(f"\n⏳ Waiting for next hour...")
                time.sleep(3600)  # 1 hour
        
        # Final summary
        print("\n" + "="*80)
        print("🎯 BLITZKRIEG COMPLETE")
        print("="*80)
        print(f"Total clips generated: {self.clips_generated}")
        print(f"Total clips uploaded: {self.clips_uploaded}")
        print(f"Output directory: {OUTPUTS_DIR}")
        print("="*80)


def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='SCARIFY Halloween Blitzkrieg - Psychological Warfare Content Generator'
    )
    parser.add_argument(
        '--gen-only',
        action='store_true',
        help='Generate clips only (no upload)'
    )
    parser.add_argument(
        '--upload-only',
        action='store_true',
        help='Upload existing clips only'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test mode: generate 1 clip'
    )
    parser.add_argument(
        '--fear',
        choices=['corrupt_gov', 'loved_ones_dying', 'economic_collapse', 'cyber_terrorism', 'russia_nukes'],
        default='corrupt_gov',
        help='Fear type to generate'
    )
    parser.add_argument(
        '--duration',
        type=int,
        default=72,
        help='Operation duration in hours'
    )
    
    args = parser.parse_args()
    
    blitz = ScarifyBlitz()
    
    if args.test:
        # Test mode: generate single clip
        print("\n🧪 TEST MODE: Generating single clip")
        video_path = blitz.generate_phantom_train_clip(args.fear)
        if video_path:
            print(f"\n✅ Test clip generated: {video_path}")
        sys.exit(0)
    
    if args.gen_only:
        # Generation only mode
        print("\n🎬 GENERATION ONLY MODE")
        video_path = blitz.generate_phantom_train_clip(args.fear)
        sys.exit(0 if video_path else 1)
    
    # Full blitzkrieg mode
    blitz.run_blitz_cycle(duration_hours=args.duration)


if __name__ == '__main__':
    main()

