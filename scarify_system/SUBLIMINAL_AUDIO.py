"""
SUBLIMINAL_AUDIO.py
Generate and mix subliminal audio layers (binaural beats, attention tones, VHS hiss).
"""

import os
import numpy as np
from scipy.io import wavfile
from pathlib import Path
import subprocess
from typing import Optional


class SubliminalAudioMixer:
    """
    Create subliminal audio layers and mix with voice.
    
    Layers:
    - Binaural beat (10Hz alpha wave) at -20dB
    - Attention tone (528Hz Solfeggio) at -25dB
    - VHS tape hiss at -30dB
    - Voice at 0dB (reference)
    """
    
    def __init__(self, sample_rate: int = 44100):
        """
        Initialize audio mixer.
        
        Args:
            sample_rate: Audio sample rate in Hz (default: 44100)
        """
        self.sample_rate = sample_rate
    
    def generate_binaural_beat(
        self,
        duration: float,
        base_freq: float = 200.0,
        beat_freq: float = 10.0,
        amplitude: float = 0.1
    ) -> np.ndarray:
        """
        Generate binaural beat (alpha wave).
        
        Args:
            duration: Duration in seconds
            base_freq: Base frequency in Hz (default: 200Hz)
            beat_freq: Beat frequency in Hz (default: 10Hz for alpha wave)
            amplitude: Amplitude 0-1 (default: 0.1 for -20dB)
            
        Returns:
            Stereo audio array (samples, 2)
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        # Left ear: base frequency
        left = amplitude * np.sin(2 * np.pi * base_freq * t)
        
        # Right ear: base + beat frequency
        right = amplitude * np.sin(2 * np.pi * (base_freq + beat_freq) * t)
        
        # Combine to stereo
        stereo = np.column_stack((left, right))
        return stereo
    
    def generate_attention_tone(
        self,
        duration: float,
        freq: float = 528.0,
        amplitude: float = 0.056
    ) -> np.ndarray:
        """
        Generate attention tone (528Hz Solfeggio frequency).
        
        Args:
            duration: Duration in seconds
            freq: Frequency in Hz (default: 528Hz)
            amplitude: Amplitude 0-1 (default: 0.056 for -25dB)
            
        Returns:
            Stereo audio array (samples, 2)
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        # Pure sine wave
        tone = amplitude * np.sin(2 * np.pi * freq * t)
        
        # Convert to stereo
        stereo = np.column_stack((tone, tone))
        return stereo
    
    def generate_vhs_hiss(
        self,
        duration: float,
        amplitude: float = 0.032
    ) -> np.ndarray:
        """
        Generate VHS tape hiss (filtered white noise).
        
        Args:
            duration: Duration in seconds
            amplitude: Amplitude 0-1 (default: 0.032 for -30dB)
            
        Returns:
            Stereo audio array (samples, 2)
        """
        samples = int(self.sample_rate * duration)
        
        # Generate white noise
        noise = np.random.normal(0, amplitude, (samples, 2))
        
        # Apply simple high-pass filter to simulate tape hiss
        # (real implementation would use scipy.signal)
        return noise
    
    def save_wav(self, audio: np.ndarray, output_path: str):
        """
        Save audio array as WAV file.
        
        Args:
            audio: Audio array
            output_path: Output file path
        """
        # Ensure audio is in correct range
        audio = np.clip(audio, -1.0, 1.0)
        
        # Convert to int16
        audio_int16 = (audio * 32767).astype(np.int16)
        
        # Save
        wavfile.write(output_path, self.sample_rate, audio_int16)
    
    def mix_subliminal_audio(
        self,
        voice_path: str,
        duration: float,
        output_path: Optional[str] = None
    ) -> str:
        """
        Mix voice with subliminal audio layers using FFmpeg.
        
        Args:
            voice_path: Path to voice audio file
            duration: Duration in seconds
            output_path: Output path (default: voice_path with _mixed suffix)
            
        Returns:
            Path to mixed audio file
        """
        if output_path is None:
            base = Path(voice_path).stem
            output_path = str(Path(voice_path).parent / f"{base}_mixed.mp3")
        
        # Create temp directory for layers
        temp_dir = Path("temp_audio_layers")
        temp_dir.mkdir(exist_ok=True)
        
        print("[SUBLIMINAL] Generating audio layers...")
        
        # Generate all layers
        binaural = self.generate_binaural_beat(duration)
        attention = self.generate_attention_tone(duration)
        hiss = self.generate_vhs_hiss(duration)
        
        # Save temporary WAV files
        binaural_path = temp_dir / "binaural.wav"
        attention_path = temp_dir / "attention.wav"
        hiss_path = temp_dir / "hiss.wav"
        
        self.save_wav(binaural, str(binaural_path))
        self.save_wav(attention, str(attention_path))
        self.save_wav(hiss, str(hiss_path))
        
        print("[SUBLIMINAL] Mixing with FFmpeg...")
        
        # Mix using FFmpeg with proper volume levels
        # Voice: 0dB (1.0)
        # Binaural: -20dB (0.1)
        # Attention: -25dB (0.056)
        # Hiss: -30dB (0.032)
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', voice_path,
            '-i', str(binaural_path),
            '-i', str(attention_path),
            '-i', str(hiss_path),
            '-filter_complex',
            '[0:a]volume=1.0[v];'
            '[1:a]volume=0.1[b];'
            '[2:a]volume=0.056[a];'
            '[3:a]volume=0.032[h];'
            '[v][b][a][h]amix=inputs=4:duration=first:dropout_transition=2',
            '-ac', '2',
            '-y',
            output_path
        ]
        
        try:
            result = subprocess.run(
                ffmpeg_cmd,
                capture_output=True,
                text=True,
                check=True
            )
            print(f"[SUBLIMINAL] ✅ Mixed audio saved: {output_path}")
            
            # Cleanup temp files
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
            
            return output_path
            
        except subprocess.CalledProcessError as e:
            print(f"[SUBLIMINAL] ❌ FFmpeg error: {e.stderr}")
            raise
        except FileNotFoundError:
            print("[SUBLIMINAL] ❌ FFmpeg not found. Please install FFmpeg.")
            print("Download from: https://ffmpeg.org/download.html")
            raise
    
    def mix_subliminal_audio_simple(
        self,
        voice_path: str,
        duration: float,
        output_path: Optional[str] = None
    ) -> str:
        """
        Simple mixing without FFmpeg (for testing/fallback).
        Loads voice, adds subliminal layers, saves as WAV.
        
        Args:
            voice_path: Path to voice audio file (must be WAV)
            duration: Duration in seconds
            output_path: Output path (default: voice_path with _mixed suffix)
            
        Returns:
            Path to mixed audio file
        """
        if output_path is None:
            base = Path(voice_path).stem
            output_path = str(Path(voice_path).parent / f"{base}_mixed.wav")
        
        print("[SUBLIMINAL] Generating layers (simple mode)...")
        
        # Load voice audio
        try:
            voice_rate, voice_audio = wavfile.read(voice_path)
            
            # Resample if needed
            if voice_rate != self.sample_rate:
                print(f"[SUBLIMINAL] Warning: Voice sample rate mismatch ({voice_rate} vs {self.sample_rate})")
            
            # Convert to float
            voice_audio = voice_audio.astype(np.float32) / 32767.0
            
            # Ensure stereo
            if voice_audio.ndim == 1:
                voice_audio = np.column_stack((voice_audio, voice_audio))
            
        except Exception as e:
            print(f"[SUBLIMINAL] Error loading voice: {e}")
            raise
        
        # Generate subliminal layers
        actual_duration = len(voice_audio) / voice_rate
        binaural = self.generate_binaural_beat(actual_duration)
        attention = self.generate_attention_tone(actual_duration)
        hiss = self.generate_vhs_hiss(actual_duration)
        
        # Ensure all arrays have same length
        min_len = min(len(voice_audio), len(binaural), len(attention), len(hiss))
        voice_audio = voice_audio[:min_len]
        binaural = binaural[:min_len]
        attention = attention[:min_len]
        hiss = hiss[:min_len]
        
        # Mix all layers
        mixed = voice_audio + binaural + attention + hiss
        
        # Normalize to prevent clipping
        max_val = np.max(np.abs(mixed))
        if max_val > 1.0:
            mixed = mixed / max_val
        
        # Save
        self.save_wav(mixed, output_path)
        print(f"[SUBLIMINAL] ✅ Mixed audio saved: {output_path}")
        
        return output_path


if __name__ == "__main__":
    print("=== Subliminal Audio Mixer Test ===\n")
    
    mixer = SubliminalAudioMixer()
    
    # Test layer generation
    print("Test 1: Generate individual layers")
    duration = 5.0
    
    binaural = mixer.generate_binaural_beat(duration)
    print(f"  Binaural beat: {binaural.shape} samples")
    
    attention = mixer.generate_attention_tone(duration)
    print(f"  Attention tone: {attention.shape} samples")
    
    hiss = mixer.generate_vhs_hiss(duration)
    print(f"  VHS hiss: {hiss.shape} samples")
    
    # Test WAV save
    print("\nTest 2: Save layers as WAV files")
    os.makedirs("test_audio_output", exist_ok=True)
    
    mixer.save_wav(binaural, "test_audio_output/binaural.wav")
    mixer.save_wav(attention, "test_audio_output/attention.wav")
    mixer.save_wav(hiss, "test_audio_output/hiss.wav")
    print("  ✅ Files saved to test_audio_output/")
    
    print("\n✅ Tests complete!")
    print("\nNote: For full mixing test with voice, use:")
    print("  mixer.mix_subliminal_audio('voice.mp3', duration=30.0)")
    
    # Cleanup
    import shutil
    shutil.rmtree("test_audio_output", ignore_errors=True)
