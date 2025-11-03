#!/usr/bin/env python3
"""SCARIFY Audio Generator - Professional TTS with SOVA (Neural), ElevenLabs, Windows TTS"""
import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Load .env with ABSOLUTE path
env_path = Path(__file__).parent / "config" / "credentials" / ".env"
load_dotenv(env_path)

class AudioGenerator:
    """Professional audio generator with multiple TTS fallbacks"""
    
    def __init__(self):
        self.elevenlabs_key = os.getenv('ELEVENLABS_API_KEY')
        self.sova_path = Path('sova-tts/run_sova_tts.py')
        self.sova_installed = self.sova_path.exists()
        
        # Voice settings
        self.sova_voice = 'Matthew'  # Professional male voice
        self.elevenlabs_voice_id = "EXAVITQu4vr4xnSDxMaL"  # Premium voice
        
        # Theta audio settings
        self.theta_enabled = True  # Enable Theta wave background
        self.theta_frequency = 6.0  # Theta frequency (4-8 Hz)
        self.theta_volume = 0.1  # Subtle background volume
        
    def generate(self, text: str, output_path: str) -> bool:
        """
        Generate professional audio with automatic fallback chain
        
        Priority: SOVA (Neural) → ElevenLabs (API) → Windows TTS (Fallback)
        
        Args:
            text: Text to convert to speech
            output_path: Where to save the audio file
            
        Returns:
            True if audio generated successfully
        """
        print(f"\n[AUDIO] AUDIO GENERATION (Professional)")
        print(f"   Text: {text[:60]}{'...' if len(text) > 60 else ''}")
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        # Method 1: SOVA TTS (Best Quality - Neural Network)
        if self.sova_installed:
            print("   [METHOD] SOVA TTS (Neural Network - Best Quality)")
            if self._generate_sova(text, output_path):
                self._print_audio_info(output_path, "SOVA Neural TTS")
                return True
            print("   [WARNING] SOVA failed, trying next method...")
        else:
            print("   [WARNING] SOVA TTS not installed (run install_sova_tts.ps1)")
        
        # Method 2: ElevenLabs API (High Quality - Cloud)
        if self.elevenlabs_key:
            print("   [METHOD] ElevenLabs API (Cloud TTS)")
            if self._generate_elevenlabs(text, output_path):
                self._print_audio_info(output_path, "ElevenLabs Cloud TTS")
                return True
            print("   [WARNING] ElevenLabs failed, trying next method...")
        else:
            print("   [WARNING] ElevenLabs API key not configured")
        
        # Method 3: Windows TTS (Fallback - System)
        print("   [METHOD] Windows TTS (System Fallback)")
        if self._generate_windows_tts(text, output_path):
            self._print_audio_info(output_path, "Windows System TTS")
            return True
        
        print("   [ERROR] All TTS methods failed!")
        return False
    
    def _generate_theta_background(self, duration: int = 50) -> str:
        """Generate Theta wave background audio"""
        try:
            import numpy as np
            import scipy.io.wavfile as wav
            
            sample_rate = 44100
            t = np.linspace(0, duration, int(sample_rate * duration))
            
            # Generate Theta wave (6 Hz)
            theta_wave = np.sin(2 * np.pi * self.theta_frequency * t)
            
            # Add subtle modulation for naturalness
            modulation = 0.1 * np.sin(2 * np.pi * 0.5 * t)
            theta_wave = theta_wave * (1 + modulation)
            
            # Apply volume
            theta_wave = theta_wave * self.theta_volume
            
            # Normalize and convert to int16
            theta_wave = np.int16(theta_wave * 32767)
            
            # Save theta background
            theta_path = "temp_theta_bg.wav"
            wav.write(theta_path, sample_rate, theta_wave)
            
            print(f"      Theta background generated")
            return theta_path
            
        except Exception as e:
            print(f"      Theta generation error: {e}")
            return None
    
    def _mix_audio_layers(self, main_audio_path: str, theta_path: str, output_path: str) -> bool:
        """Mix main TTS with Theta background"""
        try:
            from pydub import AudioSegment
            
            # Load audio files
            main_audio = AudioSegment.from_wav(main_audio_path)
            theta_audio = AudioSegment.from_wav(theta_path)
            
            # Match durations
            if len(theta_audio) < len(main_audio):
                theta_audio = theta_audio * (len(main_audio) // len(theta_audio) + 1)
            
            theta_audio = theta_audio[:len(main_audio)]
            
            # Mix audio layers
            mixed_audio = main_audio.overlay(theta_audio)
            
            # Export final audio
            mixed_audio.export(output_path, format="wav")
            
            print(f"      Audio layers mixed with Theta")
            return True
            
        except Exception as e:
            print(f"      Audio mixing error: {e}")
            return False
    
    def _print_audio_info(self, path: str, method: str):
        """Print audio file information"""
        if os.path.exists(path):
            size_kb = os.path.getsize(path) / 1024
            print(f"   [SUCCESS] {method} - Generated ({size_kb:.1f} KB)")
        else:
            print(f"   [ERROR] {method} - File not created")
    
    def _generate_sova(self, text: str, output_path: str) -> bool:
        """Generate audio using SOVA TTS (Neural Network)"""
        try:
            # Run SOVA TTS with proper arguments
            result = subprocess.run([
                sys.executable,  # Use same Python interpreter
                str(self.sova_path),
                '--text', text,
                '--voice', self.sova_voice,
                '--output', output_path
            ], capture_output=True, timeout=120, text=True)  # Increased timeout for neural processing
            
            # Check if successful
            if result.returncode == 0 and os.path.exists(output_path):
                # Verify file is not empty
                if os.path.getsize(output_path) > 1024:  # At least 1KB
                    return True
                else:
                    print(f"      Warning: Generated file too small")
                    return False
            
            # Print error if any
            if result.stderr:
                print(f"      SOVA stderr: {result.stderr[:200]}")
            
            return False
            
        except subprocess.TimeoutExpired:
            print(f"      SOVA timeout (neural processing too long)")
            return False
        except FileNotFoundError:
            print(f"      SOVA not found at: {self.sova_path}")
            return False
        except Exception as e:
            print(f"      SOVA exception: {type(e).__name__}: {str(e)[:100]}")
            return False
    
    def _generate_elevenlabs(self, text: str, output_path: str) -> bool:
        """Generate audio using ElevenLabs API (Cloud TTS)"""
        try:
            from elevenlabs import generate, save, Voice
            
            # Generate audio with ElevenLabs
            audio = generate(
                text=text,
                voice=Voice(voice_id=self.elevenlabs_voice_id),
                model="eleven_monolingual_v1"  # High quality model
            )
            
            # Save to file
            save(audio, output_path)
            
            # Verify file exists and is not empty
            if os.path.exists(output_path) and os.path.getsize(output_path) > 1024:
                return True
            
            return False
            
        except ImportError:
            print(f"      ElevenLabs library not installed (pip install elevenlabs)")
            return False
        except Exception as e:
            error_msg = str(e)[:200]
            print(f"      ElevenLabs exception: {error_msg}")
            return False
    
    def _generate_windows_tts(self, text: str, output_path: str) -> bool:
        """Generate audio using Windows System TTS (Fallback)"""
        if sys.platform != 'win32':
            print(f"      Windows TTS only available on Windows")
            return False
        
        try:
            # Escape quotes in text for PowerShell
            safe_text = text.replace('"', '`"').replace("'", "''")
            safe_path = output_path.replace('\\', '\\\\')
            
            # PowerShell script for TTS
            ps_script = f'''
Add-Type -AssemblyName System.Speech
$synthesizer = New-Object System.Speech.Synthesis.SpeechSynthesizer

# Try to use better voice if available
$voices = $synthesizer.GetInstalledVoices()
foreach ($voice in $voices) {{
    $name = $voice.VoiceInfo.Name
    if ($name -like "*David*" -or $name -like "*Mark*") {{
        $synthesizer.SelectVoice($name)
        break
    }}
}}

# Settings for better quality
$synthesizer.Rate = 0  # Normal speed (was -1, too fast)
$synthesizer.Volume = 100

# Generate audio
$synthesizer.SetOutputToWaveFile("{safe_path}")
$synthesizer.Speak("{safe_text}")
$synthesizer.Dispose()
'''
            
            # Run PowerShell
            result = subprocess.run(
                ['powershell', '-NoProfile', '-Command', ps_script],
                capture_output=True,
                timeout=60,
                text=True
            )
            
            # Verify output
            if os.path.exists(output_path) and os.path.getsize(output_path) > 1024:
                return True
            
            if result.stderr:
                print(f"      Windows TTS stderr: {result.stderr[:200]}")
            
            return False
            
        except subprocess.TimeoutExpired:
            print(f"      Windows TTS timeout")
            return False
        except Exception as e:
            print(f"      Windows TTS exception: {type(e).__name__}: {str(e)[:100]}")
            return False

if __name__ == '__main__':
    gen = AudioGenerator()
    gen.generate(sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else print("Usage: python audio_generator.py 'text' output.wav")
