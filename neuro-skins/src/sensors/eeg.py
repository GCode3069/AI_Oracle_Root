"""
EEG Signal Processing
Handles brain wave detection and analysis
"""

import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from scipy import signal
from scipy.fft import fft, fftfreq

from ..core.models import EEGReading


class EEGProcessor:
    """Processes EEG signals and extracts brain wave features"""
    
    # Frequency band definitions (Hz)
    BANDS = {
        'delta': (0.5, 4),
        'theta': (4, 8),
        'alpha': (8, 13),
        'beta': (13, 30),
        'gamma': (30, 100),
    }
    
    def __init__(self, sampling_rate: int = 256, channels: List[str] = None):
        """
        Initialize EEG processor
        
        Args:
            sampling_rate: Sampling rate in Hz
            channels: List of channel names (default: standard 10-20 system)
        """
        self.sampling_rate = sampling_rate
        self.channels = channels or ['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'P3', 'P4']
        
        # Notch filter for 60Hz line noise
        self.notch_filter = self._create_notch_filter(60.0)
        
        # Bandpass filter (0.5-100 Hz)
        self.bandpass_filter = self._create_bandpass_filter(0.5, 100.0)
    
    def _create_notch_filter(self, freq: float, q: float = 30.0):
        """Create notch filter for line noise removal"""
        return signal.iirnotch(freq, q, self.sampling_rate)
    
    def _create_bandpass_filter(self, low: float, high: float, order: int = 4):
        """Create bandpass filter"""
        nyquist = self.sampling_rate / 2
        low_norm = low / nyquist
        high_norm = high / nyquist
        return signal.butter(order, [low_norm, high_norm], btype='band')
    
    def preprocess_signal(self, raw_signal: np.ndarray) -> np.ndarray:
        """
        Preprocess raw EEG signal
        
        Args:
            raw_signal: Raw EEG data
            
        Returns:
            Preprocessed signal
        """
        # Check if signal is long enough for filtering
        if len(raw_signal) < 20:
            # For very short signals, just return as-is
            return raw_signal
        
        # Apply notch filter
        filtered = signal.filtfilt(*self.notch_filter, raw_signal, padlen=min(9, len(raw_signal)//3))
        
        # Apply bandpass filter
        filtered = signal.filtfilt(*self.bandpass_filter, filtered, padlen=min(9, len(filtered)//3))
        
        return filtered
    
    def compute_band_power(self, signal_data: np.ndarray, 
                          band: Tuple[float, float]) -> float:
        """
        Compute power in a specific frequency band
        
        Args:
            signal_data: Preprocessed EEG signal
            band: (low_freq, high_freq) tuple
            
        Returns:
            Band power in μV²
        """
        # Compute FFT
        n = len(signal_data)
        fft_vals = fft(signal_data)
        fft_freq = fftfreq(n, 1/self.sampling_rate)
        
        # Get positive frequencies
        pos_mask = fft_freq >= 0
        fft_freq = fft_freq[pos_mask]
        fft_vals = np.abs(fft_vals[pos_mask])
        
        # Find indices for band
        band_mask = (fft_freq >= band[0]) & (fft_freq <= band[1])
        
        # Compute power (Parseval's theorem)
        band_power = np.sum(fft_vals[band_mask]**2) / n
        
        return band_power
    
    def detect_artifacts(self, signal_data: np.ndarray) -> bool:
        """
        Detect artifacts in EEG signal
        
        Args:
            signal_data: Preprocessed EEG signal
            
        Returns:
            True if artifacts detected
        """
        # Check for amplitude artifacts (> 100 μV is suspicious)
        if np.max(np.abs(signal_data)) > 100:
            return True
        
        # Check for flat signal
        if np.std(signal_data) < 0.5:
            return True
        
        # Check for high-frequency noise
        high_freq_power = self.compute_band_power(signal_data, (50, 100))
        total_power = np.sum(signal_data ** 2)
        
        if high_freq_power / total_power > 0.5:
            return True
        
        return False
    
    def compute_signal_quality(self, signal_data: np.ndarray) -> float:
        """
        Compute signal quality score (0.0 to 1.0)
        
        Args:
            signal_data: Preprocessed EEG signal
            
        Returns:
            Quality score
        """
        quality = 1.0
        
        # Penalize for high amplitude
        max_amp = np.max(np.abs(signal_data))
        if max_amp > 50:
            quality -= 0.3
        
        # Penalize for low variance
        std = np.std(signal_data)
        if std < 1.0:
            quality -= 0.3
        
        # Penalize for high noise
        high_freq_power = self.compute_band_power(signal_data, (50, 100))
        total_power = np.sum(signal_data ** 2)
        noise_ratio = high_freq_power / total_power
        quality -= noise_ratio * 0.4
        
        return max(0.0, min(1.0, quality))
    
    def process_epoch(self, raw_channels: Dict[str, np.ndarray]) -> EEGReading:
        """
        Process a single epoch of multi-channel EEG data
        
        Args:
            raw_channels: Dict mapping channel names to raw signal arrays
            
        Returns:
            EEGReading with computed band powers
        """
        processed_channels = {}
        band_powers = {band: [] for band in self.BANDS.keys()}
        signal_qualities = []
        artifacts = False
        
        # Process each channel
        for channel_name, raw_signal in raw_channels.items():
            # Preprocess
            processed = self.preprocess_signal(raw_signal)
            processed_channels[channel_name] = processed
            
            # Compute band powers
            for band_name, band_range in self.BANDS.items():
                power = self.compute_band_power(processed, band_range)
                band_powers[band_name].append(power)
            
            # Check quality
            quality = self.compute_signal_quality(processed)
            signal_qualities.append(quality)
            
            # Check for artifacts
            if self.detect_artifacts(processed):
                artifacts = True
        
        # Average band powers across channels
        avg_band_powers = {
            band: np.mean(powers) for band, powers in band_powers.items()
        }
        
        # Average signal quality
        avg_quality = np.mean(signal_qualities)
        
        return EEGReading(
            timestamp=datetime.now(),
            channels=processed_channels,
            sampling_rate=self.sampling_rate,
            delta_power=avg_band_powers['delta'],
            theta_power=avg_band_powers['theta'],
            alpha_power=avg_band_powers['alpha'],
            beta_power=avg_band_powers['beta'],
            gamma_power=avg_band_powers['gamma'],
            signal_quality=avg_quality,
            artifacts_detected=artifacts
        )


class EEGSimulator:
    """Simulates EEG data for testing"""
    
    def __init__(self, sampling_rate: int = 256):
        self.sampling_rate = sampling_rate
        self.time = 0.0
    
    def generate_epoch(self, duration: float = 1.0, 
                      state: str = "relaxed") -> Dict[str, np.ndarray]:
        """
        Generate simulated EEG data
        
        Args:
            duration: Duration in seconds
            state: Brain state to simulate
            
        Returns:
            Dict of channel data
        """
        n_samples = int(duration * self.sampling_rate)
        t = np.linspace(self.time, self.time + duration, n_samples)
        self.time += duration
        
        # State-dependent frequency compositions (increased amplitudes)
        state_profiles = {
            "relaxed": {'alpha': 8.0, 'theta': 3.0, 'beta': 1.5, 'delta': 2.0},
            "focused": {'beta': 6.0, 'gamma': 4.0, 'alpha': 2.0, 'theta': 1.0},
            "stressed": {'beta': 8.0, 'gamma': 5.0, 'alpha': 1.0, 'theta': 0.5},
            "meditation": {'theta': 7.0, 'alpha': 5.0, 'delta': 3.0, 'beta': 0.5},
        }
        
        profile = state_profiles.get(state, state_profiles["relaxed"])
        
        # Generate signal with multiple frequency components
        signal_data = np.zeros(n_samples)
        
        # Add frequency components with phase variation
        if 'delta' in profile:
            signal_data += profile['delta'] * np.sin(2 * np.pi * 2 * t + np.random.random())
        if 'theta' in profile:
            signal_data += profile['theta'] * np.sin(2 * np.pi * 6 * t + np.random.random())
        if 'alpha' in profile:
            signal_data += profile['alpha'] * np.sin(2 * np.pi * 10 * t + np.random.random())
        if 'beta' in profile:
            signal_data += profile['beta'] * np.sin(2 * np.pi * 20 * t + np.random.random())
        if 'gamma' in profile:
            signal_data += profile['gamma'] * np.sin(2 * np.pi * 40 * t + np.random.random())
        
        # Add realistic noise
        signal_data += 1.0 * np.random.randn(n_samples)
        
        # Simulate multiple channels with slight variations
        channels = {}
        for channel in ['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'P3', 'P4']:
            noise = 0.5 * np.random.randn(n_samples)
            channels[channel] = signal_data + noise
        
        return channels
