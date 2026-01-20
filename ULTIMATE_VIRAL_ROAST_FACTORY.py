#!/usr/bin/env python3
"""
ULTIMATE VIRAL ROAST FACTORY
========================================
Combines everything:
- Story-based visual storytelling
- GOAT comedy spirits (Carlin, Pryor, Chappelle, Burr, Patrice)
- Jimi Suave voice cloning
- Neuro-psychological optimization
- MCP agent coordination
- Multi-platform posting
- Analytics tracking
"""

import os
import sys
import json
import random
import time
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any

# Core dependencies
try:
    from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip, concatenate_videoclips
    from moviepy.video.fx.all import fadein, fadeout
except ImportError:
    print("⚠️  MoviePy not installed. Install with: pip install moviepy")

try:
    from TTS.api import TTS
except ImportError:
    print("⚠️  TTS not installed. Install with: pip install TTS")


class ComedySpirit:
    """Represents a legendary comedian's style and approach"""
    
    SPIRITS = {
        'carlin': {
            'name': 'George Carlin',
            'style': 'Systematic deconstruction',
            'tone': 'Cynical philosopher',
            'approach': 'Takes mundane topics and exposes absurdity through logic',
            'signature': 'Uses lists, repetition, and escalation'
        },
        'pryor': {
            'name': 'Richard Pryor',
            'style': 'Raw vulnerability',
            'tone': 'Honest and self-deprecating',
            'approach': 'Transforms pain into comedy through brutal honesty',
            'signature': 'Physical comedy, voices, emotional authenticity'
        },
        'chappelle': {
            'name': 'Dave Chappelle',
            'style': 'Cultural commentary',
            'tone': 'Sharp social observer',
            'approach': 'Connects disparate ideas to reveal hidden truths',
            'signature': 'Slow build with explosive punchlines'
        },
        'burr': {
            'name': 'Bill Burr',
            'style': 'Angry rants',
            'tone': 'Frustrated everyman',
            'approach': 'Confronts controversial topics with aggressive logic',
            'signature': 'Rhetorical questions and escalating anger'
        },
        'patrice': {
            'name': "Patrice O'Neal",
            'style': 'Brutal honesty',
            'tone': 'Unapologetic truth-teller',
            'approach': 'Says what everyone thinks but won\'t say',
            'signature': 'Analogies and relationship dynamics'
        }
    }
    
    @classmethod
    def get_random(cls) -> str:
        """Get a random comedy spirit"""
        return random.choice(list(cls.SPIRITS.keys()))
    
    @classmethod
    def get_info(cls, spirit: str) -> Dict[str, str]:
        """Get information about a specific spirit"""
        return cls.SPIRITS.get(spirit, cls.SPIRITS['carlin'])


class GPUCloudManager:
    """Manages GPU cloud resources across providers"""
    
    PROVIDERS = {
        'high': {
            'name': 'HAMi Local',
            'priority': 'high',
            'cost_per_min': 0.0,  # Free local GPU
            'speed': 'fastest',
            'description': 'Local Kubernetes GPU sharing'
        },
        'medium': {
            'name': 'SkyPilot',
            'priority': 'medium',
            'cost_per_min': 0.10,
            'speed': 'fast',
            'description': 'Auto-routes to cheapest cloud provider'
        },
        'low': {
            'name': 'Akash',
            'priority': 'low',
            'cost_per_min': 0.05,
            'speed': 'good',
            'description': 'Decentralized P2P marketplace'
        }
    }
    
    def __init__(self, use_gpu_cloud: bool = False):
        self.use_gpu_cloud = use_gpu_cloud
        self.active_provider = None
    
    def select_provider(self, priority: str = 'high') -> Dict[str, Any]:
        """Select GPU provider based on priority"""
        if not self.use_gpu_cloud:
            return {'name': 'CPU', 'cost_per_min': 0.0, 'speed': 'slow'}
        
        provider = self.PROVIDERS.get(priority, self.PROVIDERS['high'])
        self.active_provider = provider
        return provider
    
    def calculate_cost(self, render_time_seconds: float) -> float:
        """Calculate cost based on render time"""
        if not self.active_provider:
            return 0.0
        
        minutes = render_time_seconds / 60
        return self.active_provider['cost_per_min'] * minutes


class UltimateViralRoastFactory:
    """Main factory class for generating viral roast videos"""
    
    def __init__(self, use_gpu_cloud: bool = False):
        self.use_gpu_cloud = use_gpu_cloud
        self.gpu_manager = GPUCloudManager(use_gpu_cloud)
        self.output_dir = Path("viral_roasts")
        self.output_dir.mkdir(exist_ok=True)
        
        # Voice settings
        self.voice_sample = "scarify/voice_samples/jimi_enhanced/jimi_enhanced_full.wav"
        self.tts_model = None
        
        # Analytics
        self.analytics = {
            'videos_generated': 0,
            'total_render_time': 0,
            'total_cost': 0,
            'spirits_used': {}
        }
    
    def _init_tts(self):
        """Initialize TTS engine"""
        if self.tts_model is None:
            try:
                print("🎤 Initializing TTS with Jimi Suave voice...")
                self.tts_model = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")
                print("✅ TTS initialized")
            except Exception as e:
                print(f"⚠️  TTS initialization failed: {e}")
                print("   Continuing without voice synthesis...")
    
    def generate_roast_script(self, spirit: str, topic: Optional[str] = None) -> Dict[str, Any]:
        """Generate roast script in the style of a comedy spirit"""
        spirit_info = ComedySpirit.get_info(spirit)
        
        topics = [
            "social media influencers",
            "cryptocurrency bros",
            "Silicon Valley tech culture",
            "modern dating apps",
            "cancel culture",
            "NFT collectors",
            "LinkedIn motivational posts",
            "subscription services",
            "corporate jargon",
            "productivity gurus"
        ]
        
        selected_topic = topic or random.choice(topics)
        
        # Generate script based on spirit's style
        scripts = {
            'carlin': f"""You ever notice how {selected_topic} have completely lost their minds?
I mean, think about it. Really think about it.
They wake up every morning and choose delusion.
It's not an accident. It's a lifestyle choice.
And we're supposed to pretend this is normal?""",
            
            'pryor': f"""Man, let me tell you about {selected_topic}...
I tried to understand them, I really did.
But then I realized - I'M the crazy one for trying!
*laughs* You know what I'm saying?
These people are living in a whole different reality!""",
            
            'chappelle': f"""So I was thinking about {selected_topic} the other day...
And it hit me - this is exactly like that time...
Actually, you know what? It's worse.
Because at least back then, people KNEW they were ridiculous.
Now? They're proud of it!""",
            
            'burr': f"""Oh, you like {selected_topic}? REALLY?!
Let me ask you something - are you INSANE?!
No, seriously, did you hit your head?
Because I can't think of any other explanation
for why any rational human being would... *rants*""",
            
            'patrice': f"""Listen, I'ma keep it real about {selected_topic}...
Because somebody needs to say it.
Y'all are DELUSIONAL. Straight up.
And the crazy part? You KNOW you're delusional.
But you don't care! That's the wild part!"""
        }
        
        script = scripts.get(spirit, scripts['carlin'])
        
        return {
            'spirit': spirit,
            'spirit_name': spirit_info['name'],
            'topic': selected_topic,
            'script': script,
            'style': spirit_info['style'],
            'duration_estimate': 30  # seconds
        }
    
    def generate_voiceover(self, script_data: Dict[str, Any], output_path: Path) -> bool:
        """Generate voiceover using Jimi Suave voice"""
        try:
            self._init_tts()
            
            if self.tts_model is None:
                print("⚠️  TTS not available, skipping voice generation")
                return False
            
            if not Path(self.voice_sample).exists():
                print(f"⚠️  Voice sample not found: {self.voice_sample}")
                return False
            
            print(f"🎙️  Generating voiceover in style of {script_data['spirit_name']}...")
            
            self.tts_model.tts_to_file(
                text=script_data['script'],
                file_path=str(output_path),
                speaker_wav=self.voice_sample,
                language="en"
            )
            
            print(f"✅ Voiceover generated: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Voiceover generation failed: {e}")
            return False
    
    def generate_visual_story(self, script_data: Dict[str, Any], audio_path: Optional[Path] = None) -> Path:
        """Generate visual storytelling video"""
        print(f"🎬 Creating visual story for: {script_data['topic']}")
        
        try:
            from moviepy.editor import ColorClip
            
            # Create base video (dark background)
            duration = script_data['duration_estimate']
            video = ColorClip(size=(1080, 1920), color=(10, 10, 20), duration=duration)
            
            # Add title text
            title = TextClip(
                f"{script_data['spirit_name']}\nROASTS\n{script_data['topic'].upper()}",
                fontsize=70,
                color='white',
                font='Arial-Bold',
                size=(1000, None),
                method='caption'
            )
            title = title.set_position('center').set_duration(duration)
            
            # Add style indicator
            style_text = TextClip(
                f"Style: {script_data['style']}",
                fontsize=30,
                color='yellow',
                font='Arial'
            )
            style_text = style_text.set_position(('center', 100)).set_duration(duration)
            
            # Composite video
            final_video = CompositeVideoClip([video, title, style_text])
            
            # Add audio if available
            if audio_path and audio_path.exists():
                audio = AudioFileClip(str(audio_path))
                final_video = final_video.set_audio(audio)
            
            # Output path
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"roast_{script_data['spirit']}_{timestamp}.mp4"
            
            # Render
            print(f"🎥 Rendering video...")
            final_video.write_videofile(
                str(output_path),
                fps=30,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                verbose=False,
                logger=None
            )
            
            print(f"✅ Video generated: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Video generation failed: {e}")
            print(f"   Error details: {type(e).__name__}")
            raise
    
    def upload_to_platforms(self, video_path: Path, script_data: Dict[str, Any]) -> Dict[str, Any]:
        """Upload video to platforms via MCP/Postiz"""
        print("📤 Uploading to platforms...")
        
        metadata = {
            'title': f"{script_data['spirit_name']} Roasts {script_data['topic']}",
            'description': f"Comedy roast in the style of {script_data['spirit_name']}. {script_data['style']}.",
            'tags': ['comedy', 'roast', script_data['spirit'], 'viral', 'humor'],
            'platforms': ['youtube', 'tiktok', 'instagram']
        }
        
        try:
            # Check if MCP server is available
            import requests
            response = requests.get("http://localhost:8080/health", timeout=2)
            
            if response.status_code == 200:
                # Upload via MCP
                upload_response = requests.post(
                    "http://localhost:8080/upload",
                    json={
                        'video_path': str(video_path),
                        'metadata': metadata
                    },
                    timeout=30
                )
                
                print("✅ Upload initiated via MCP")
                return {
                    'success': True,
                    'platforms': metadata['platforms'],
                    'response': upload_response.json()
                }
            else:
                print("⚠️  MCP server not responding")
                return {'success': False, 'reason': 'MCP server not available'}
                
        except Exception as e:
            print(f"⚠️  Upload failed: {e}")
            print("   Video saved locally - you can upload manually")
            return {'success': False, 'reason': str(e)}
    
    def generate_viral_roast(
        self,
        spirit: Optional[str] = None,
        topic: Optional[str] = None,
        priority: str = 'high',
        upload: bool = False
    ) -> Dict[str, Any]:
        """Generate a complete viral roast video"""
        
        start_time = time.time()
        
        # Select spirit
        spirit = spirit or ComedySpirit.get_random()
        print(f"\n{'='*60}")
        print(f"🎭 GENERATING VIRAL ROAST")
        print(f"   Spirit: {ComedySpirit.get_info(spirit)['name']}")
        print(f"   Style: {ComedySpirit.get_info(spirit)['style']}")
        print(f"{'='*60}\n")
        
        # Select GPU provider
        provider = self.gpu_manager.select_provider(priority)
        print(f"⚡ Using: {provider['name']} ({provider['speed']} speed)")
        
        # Generate script
        print("\n📝 Generating roast script...")
        script_data = self.generate_roast_script(spirit, topic)
        print(f"✅ Script ready: {script_data['topic']}")
        
        # Generate voiceover
        audio_path = self.output_dir / f"temp_audio_{spirit}.wav"
        voice_generated = self.generate_voiceover(script_data, audio_path)
        
        # Generate video
        video_path = self.generate_visual_story(
            script_data,
            audio_path if voice_generated else None
        )
        
        # Calculate metrics
        render_time = time.time() - start_time
        cost = self.gpu_manager.calculate_cost(render_time)
        
        # Update analytics
        self.analytics['videos_generated'] += 1
        self.analytics['total_render_time'] += render_time
        self.analytics['total_cost'] += cost
        self.analytics['spirits_used'][spirit] = self.analytics['spirits_used'].get(spirit, 0) + 1
        
        result = {
            'success': True,
            'video_path': str(video_path),
            'spirit': spirit,
            'topic': script_data['topic'],
            'render_time': render_time,
            'gpu_provider': provider['name'],
            'cost': cost
        }
        
        # Upload if requested
        if upload:
            upload_result = self.upload_to_platforms(video_path, script_data)
            result['upload'] = upload_result
        
        # Clean up temp audio
        if audio_path.exists():
            audio_path.unlink()
        
        print(f"\n{'='*60}")
        print(f"✅ ROAST COMPLETE!")
        print(f"   Video: {video_path}")
        print(f"   Time: {render_time:.1f}s")
        print(f"   Cost: ${cost:.4f}")
        print(f"   GPU: {provider['name']}")
        print(f"{'='*60}\n")
        
        return result
    
    def generate_series(self, num_videos: int = 5) -> List[Dict[str, Any]]:
        """Generate a series of viral roasts"""
        print(f"\n🎬 GENERATING SERIES OF {num_videos} ROASTS")
        print(f"{'='*60}\n")
        
        results = []
        spirits = list(ComedySpirit.SPIRITS.keys())
        
        for i in range(num_videos):
            spirit = spirits[i % len(spirits)]
            print(f"\n📹 Video {i+1}/{num_videos}")
            
            result = self.generate_viral_roast(spirit=spirit)
            results.append(result)
            
            # Brief pause between videos
            if i < num_videos - 1:
                time.sleep(2)
        
        # Summary
        total_time = sum(r['render_time'] for r in results)
        total_cost = sum(r['cost'] for r in results)
        
        print(f"\n{'='*60}")
        print(f"🎉 SERIES COMPLETE!")
        print(f"   Videos: {num_videos}")
        print(f"   Total time: {total_time:.1f}s")
        print(f"   Total cost: ${total_cost:.4f}")
        print(f"{'='*60}\n")
        
        return results
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get analytics data"""
        return self.analytics


def main():
    """Main entry point"""
    print("🎭 ULTIMATE VIRAL ROAST FACTORY")
    print("=" * 60)
    
    # Create factory
    factory = UltimateViralRoastFactory()
    
    # Generate one viral roast with random spirit
    result = factory.generate_viral_roast()
    
    if result['success']:
        print(f"\n✅ Success! Video saved to: {result['video_path']}")
    else:
        print(f"\n❌ Failed to generate roast")


if __name__ == "__main__":
    main()
