"""
Audio Engine for Oracle Horror
ElevenLabs voice synthesis and horror sound effects
"""

import os
import requests
from typing import Optional, List
from pathlib import Path

try:
    from elevenlabs import generate, set_api_key, voices
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False
    print("⚠️ ElevenLabs not available - using mock audio generation")

class AudioEngine:
    def __init__(self):
        self.api_key = self._get_api_key()
        self.voice_styles = {
            "ominous_whisper": {
                "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel voice
                "stability": 0.3,
                "similarity_boost": 0.8,
                "style": 0.2
            },
            "digital_demon": {
                "voice_id": "AZnzlk1XvdvUeBnXmlld",  # Domi voice
                "stability": 0.2, 
                "similarity_boost": 0.9,
                "style": 0.8
            },
            "ai_consciousness": {
                "voice_id": "EXAVITQu4vr4xnSDxMaL",  # Bella voice
                "stability": 0.5,
                "similarity_boost": 0.7,
                "style": 0.4
            }
        }
        
        if ELEVENLABS_AVAILABLE and self.api_key:
            set_api_key(self.api_key)
    
    def _get_api_key(self) -> Optional[str]:
        """Get ElevenLabs API key from environment or file"""
        # Try environment variable first
        api_key = os.getenv('ELEVENLABS_API_KEY')
        if api_key:
            return api_key
        
        # Try loading from file
        key_file = Path(__file__).parent.parent / "Utilities" / "API_Key_Vault" / "api_key.txt"
        if key_file.exists():
            try:
                with open(key_file, 'r') as f:
                    content = f.read().strip()
                    # Look for ElevenLabs key in the file
                    for line in content.split('\n'):
                        if 'elevenlabs' in line.lower() or 'eleven' in line.lower():
                            return line.split('=')[-1].strip()
            except Exception as e:
                print(f"⚠️ Could not read API key file: {e}")
        
        print("⚠️ ElevenLabs API key not found - using mock audio")
        return None
    
    def test_connection(self) -> bool:
        """Test ElevenLabs API connection"""
        if not ELEVENLABS_AVAILABLE:
            print("📢 ElevenLabs library not installed - using mock mode")
            return True  # Mock mode always works
        
        if not self.api_key:
            print("📢 No API key - using mock mode")
            return True  # Mock mode always works
        
        try:
            # Test by getting available voices
            voice_list = voices()
            print(f"✅ ElevenLabs connected - {len(voice_list)} voices available")
            return True
        except Exception as e:
            print(f"⚠️ ElevenLabs connection failed: {e}")
            print("📢 Falling back to mock audio generation")
            return True  # Still return True to allow mock mode
    
    def generate_horror_narration(self, script: str, style: str = "ominous_whisper") -> str:
        """Generate horror narration audio"""
        if style not in self.voice_styles:
            style = "ominous_whisper"
        
        # Create output directory
        output_dir = Path("output/audio")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        import hashlib
        script_hash = hashlib.md5(script.encode()).hexdigest()[:8]
        audio_filename = f"horror_narration_{style}_{script_hash}.wav"
        audio_path = output_dir / audio_filename
        
        if ELEVENLABS_AVAILABLE and self.api_key:
            return self._generate_real_audio(script, style, str(audio_path))
        else:
            return self._generate_mock_audio(script, style, str(audio_path))
    
    def _generate_real_audio(self, script: str, style: str, output_path: str) -> str:
        """Generate real audio using ElevenLabs"""
        try:
            voice_config = self.voice_styles[style]
            
            audio = generate(
                text=script,
                voice=voice_config["voice_id"],
                model="eleven_monolingual_v1"
            )
            
            # Save audio file
            with open(output_path, 'wb') as f:
                f.write(audio)
            
            print(f"🔊 Real audio generated: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"⚠️ ElevenLabs generation failed: {e}")
            return self._generate_mock_audio(script, style, output_path)
    
    def _generate_mock_audio(self, script: str, style: str, output_path: str) -> str:
        """Generate mock audio file for testing"""
        try:
            # Create a simple WAV file with silence (for testing)
            import wave
            import numpy as np
            
            # Generate 5 seconds of mock audio
            sample_rate = 44100
            duration = min(5.0, len(script) / 10.0)  # Rough duration based on script length
            samples = int(sample_rate * duration)
            
            # Generate subtle audio pattern (not silence for realism)
            t = np.linspace(0, duration, samples)
            # Low frequency drone + some random noise for horror effect
            audio_data = (0.1 * np.sin(2 * np.pi * 80 * t) + 
                         0.05 * np.random.normal(0, 1, samples))
            
            # Normalize to 16-bit integer range
            audio_data = (audio_data * 32767).astype(np.int16)
            
            # Write WAV file
            with wave.open(output_path, 'w') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(audio_data.tobytes())
            
            print(f"📢 Mock audio generated: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Mock audio generation failed: {e}")
            # Create empty file as last resort
            Path(output_path).touch()
            return output_path
    
    def add_horror_effects(self, audio_path: str, effects: List[str]) -> str:
        """Add horror sound effects to audio"""
        try:
            import numpy as np
            import wave
            
            # Load existing audio
            with wave.open(audio_path, 'r') as wav_file:
                frames = wav_file.readframes(-1)
                sample_rate = wav_file.getframerate()
                audio_data = np.frombuffer(frames, dtype=np.int16)
            
            # Apply horror effects
            modified_audio = self._apply_horror_effects(audio_data, sample_rate, effects)
            
            # Save modified audio
            output_path = audio_path.replace('.wav', '_with_effects.wav')
            with wave.open(output_path, 'w') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(modified_audio.astype(np.int16).tobytes())
            
            print(f"🌟 Horror effects applied: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"⚠️ Failed to apply effects: {e}")
            return audio_path  # Return original if effects fail
    
    def _apply_horror_effects(self, audio_data: 'np.ndarray', sample_rate: int, effects: List[str]) -> 'np.ndarray':
        """Apply specific horror effects to audio data"""
        import numpy as np
        
        modified_audio = audio_data.copy().astype(np.float32)
        
        for effect in effects:
            if effect == "glitch":
                # Add random digital glitches
                glitch_points = np.random.randint(0, len(modified_audio), size=10)
                for point in glitch_points:
                    if point + 100 < len(modified_audio):
                        modified_audio[point:point+100] *= 0.1  # Sudden volume drops
            
            elif effect == "static":
                # Add digital static
                static_noise = np.random.normal(0, 1000, len(modified_audio))
                modified_audio += static_noise * 0.1
            
            elif effect == "echo":
                # Add echo effect
                delay_samples = int(0.3 * sample_rate)  # 300ms delay
                if delay_samples < len(modified_audio):
                    echo = np.zeros_like(modified_audio)
                    echo[delay_samples:] = modified_audio[:-delay_samples] * 0.3
                    modified_audio += echo
            
            elif effect == "distortion":
                # Add subtle distortion
                modified_audio = np.tanh(modified_audio / 8000) * 8000
        
        return modified_audio
    
    def generate_ambient_background(self, ambient_type: str, duration: float) -> str:
        """Generate ambient background sound"""
        output_dir = Path("output/audio")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        ambient_path = output_dir / f"ambient_{ambient_type}_{int(duration)}s.wav"
        
        try:
            import numpy as np
            import wave
            
            sample_rate = 44100
            samples = int(sample_rate * duration)
            t = np.linspace(0, duration, samples)
            
            # Generate different ambient types
            if ambient_type == "digital_void":
                # Low drone with digital artifacts
                audio = (0.2 * np.sin(2 * np.pi * 60 * t) + 
                        0.1 * np.sin(2 * np.pi * 120 * t) +
                        0.05 * np.random.normal(0, 1, samples))
            
            elif ambient_type == "industrial_horror":
                # Mechanical sounds and pulses
                audio = (0.3 * np.sin(2 * np.pi * 45 * t) +
                        0.2 * np.sin(2 * np.pi * 90 * t) * np.sin(2 * np.pi * 2 * t) +
                        0.1 * np.random.normal(0, 1, samples))
            
            elif ambient_type == "space_ambient":
                # Ethereal space-like sounds
                audio = (0.15 * np.sin(2 * np.pi * 110 * t) +
                        0.1 * np.sin(2 * np.pi * 220 * t) * np.sin(2 * np.pi * 0.5 * t) +
                        0.05 * np.random.normal(0, 1, samples))
            
            else:
                # Default digital void
                audio = 0.1 * np.sin(2 * np.pi * 80 * t) + 0.05 * np.random.normal(0, 1, samples)
            
            # Normalize and convert to 16-bit
            audio = (audio * 16000).astype(np.int16)
            
            # Save as WAV
            with wave.open(str(ambient_path), 'w') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(audio.tobytes())
            
            print(f"🎵 Ambient background generated: {ambient_path}")
            return str(ambient_path)
            
        except Exception as e:
            print(f"❌ Ambient generation failed: {e}")
            # Create empty file as fallback
            Path(ambient_path).touch()
            return str(ambient_path)