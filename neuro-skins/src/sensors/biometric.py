"""
Biometric Sensor Integration
HRV, cortisol, and skin conductance monitoring
"""

import numpy as np
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass

from ..core.models import HRVReading, CortisolReading, SkinConductanceReading


class HRVMonitor:
    """Heart Rate Variability monitoring"""
    
    def __init__(self, sampling_rate: int = 250):
        """
        Initialize HRV monitor
        
        Args:
            sampling_rate: ECG sampling rate in Hz
        """
        self.sampling_rate = sampling_rate
        self.rr_intervals: List[float] = []
    
    def detect_r_peaks(self, ecg_signal: np.ndarray) -> np.ndarray:
        """
        Detect R-peaks in ECG signal
        
        Args:
            ecg_signal: Raw ECG signal
            
        Returns:
            Array of R-peak indices
        """
        # Simple threshold-based R-peak detection
        # In production, use more sophisticated algorithms (Pan-Tompkins, etc.)
        
        # High-pass filter to remove baseline wander
        from scipy import signal
        b, a = signal.butter(4, 0.5 / (self.sampling_rate/2), 'high')
        filtered = signal.filtfilt(b, a, ecg_signal)
        
        # Square to emphasize peaks
        squared = filtered ** 2
        
        # Moving average
        window = int(0.12 * self.sampling_rate)  # 120ms window
        integrated = np.convolve(squared, np.ones(window)/window, mode='same')
        
        # Find peaks
        from scipy.signal import find_peaks
        peaks, _ = find_peaks(integrated, distance=int(0.3 * self.sampling_rate))
        
        return peaks
    
    def compute_rr_intervals(self, r_peaks: np.ndarray) -> np.ndarray:
        """
        Compute RR intervals from R-peaks
        
        Args:
            r_peaks: Array of R-peak indices
            
        Returns:
            RR intervals in milliseconds
        """
        rr_samples = np.diff(r_peaks)
        rr_ms = (rr_samples / self.sampling_rate) * 1000
        return rr_ms
    
    def compute_hrv_metrics(self, rr_intervals: np.ndarray) -> HRVReading:
        """
        Compute HRV metrics from RR intervals
        
        Args:
            rr_intervals: RR intervals in milliseconds
            
        Returns:
            HRVReading with computed metrics
        """
        # Heart rate
        mean_rr = np.mean(rr_intervals)
        heart_rate = 60000 / mean_rr  # bpm
        
        # Time-domain metrics
        sdnn = np.std(rr_intervals, ddof=1)  # Standard deviation of NN intervals
        
        # RMSSD (Root mean square of successive differences)
        successive_diffs = np.diff(rr_intervals)
        rmssd = np.sqrt(np.mean(successive_diffs ** 2))
        
        # pNN50 (Percentage of successive intervals > 50ms)
        nn50 = np.sum(np.abs(successive_diffs) > 50)
        pnn50 = (nn50 / len(successive_diffs)) * 100
        
        # Frequency-domain metrics
        lf_hf_ratio = self._compute_lf_hf_ratio(rr_intervals)
        
        return HRVReading(
            timestamp=datetime.now(),
            heart_rate=heart_rate,
            rmssd=rmssd,
            sdnn=sdnn,
            pnn50=pnn50,
            lf_hf_ratio=lf_hf_ratio
        )
    
    def _compute_lf_hf_ratio(self, rr_intervals: np.ndarray) -> float:
        """
        Compute LF/HF ratio from RR intervals
        
        Args:
            rr_intervals: RR intervals in milliseconds
            
        Returns:
            LF/HF ratio
        """
        from scipy import signal
        from scipy.interpolate import interp1d
        
        # Resample to uniform time series (4 Hz)
        time = np.cumsum(rr_intervals) / 1000  # seconds
        f = interp1d(time, rr_intervals, kind='cubic', fill_value='extrapolate')
        
        fs = 4.0  # 4 Hz resampling
        time_uniform = np.arange(time[0], time[-1], 1/fs)
        rr_uniform = f(time_uniform)
        
        # Compute power spectral density
        freqs, psd = signal.welch(rr_uniform, fs=fs, nperseg=min(256, len(rr_uniform)))
        
        # LF: 0.04-0.15 Hz, HF: 0.15-0.4 Hz
        lf_mask = (freqs >= 0.04) & (freqs < 0.15)
        hf_mask = (freqs >= 0.15) & (freqs < 0.4)
        
        lf_power = np.trapz(psd[lf_mask], freqs[lf_mask])
        hf_power = np.trapz(psd[hf_mask], freqs[hf_mask])
        
        return lf_power / hf_power if hf_power > 0 else 2.0
    
    def process_ecg(self, ecg_signal: np.ndarray) -> HRVReading:
        """
        Process ECG signal and compute HRV metrics
        
        Args:
            ecg_signal: Raw ECG signal
            
        Returns:
            HRVReading
        """
        r_peaks = self.detect_r_peaks(ecg_signal)
        rr_intervals = self.compute_rr_intervals(r_peaks)
        return self.compute_hrv_metrics(rr_intervals)


class CortisolMonitor:
    """Cortisol level monitoring"""
    
    def __init__(self):
        self.calibration_offset = 0.0
        self.last_reading = None
    
    def calibrate(self, known_value: float, sensor_reading: float):
        """
        Calibrate sensor against known cortisol value
        
        Args:
            known_value: Known cortisol level (ng/mL)
            sensor_reading: Raw sensor reading
        """
        self.calibration_offset = known_value - sensor_reading
    
    def process_reading(self, raw_value: float, 
                       sample_type: str = "saliva") -> CortisolReading:
        """
        Process raw cortisol sensor reading
        
        Args:
            raw_value: Raw sensor value
            sample_type: Type of sample (saliva, blood, etc.)
            
        Returns:
            CortisolReading
        """
        # Apply calibration
        calibrated_value = raw_value + self.calibration_offset
        
        # Clamp to physiological range
        calibrated_value = max(0, min(calibrated_value, 1000))
        
        reading = CortisolReading(
            timestamp=datetime.now(),
            level_ng_ml=calibrated_value,
            sample_type=sample_type
        )
        
        self.last_reading = reading
        return reading
    
    def get_trend(self, history: List[CortisolReading]) -> str:
        """
        Analyze cortisol trend over time
        
        Args:
            history: List of historical readings
            
        Returns:
            Trend description
        """
        if len(history) < 2:
            return "insufficient_data"
        
        recent = history[-5:]  # Last 5 readings
        levels = [r.level_ng_ml for r in recent]
        
        # Linear regression
        x = np.arange(len(levels))
        slope = np.polyfit(x, levels, 1)[0]
        
        if slope > 20:
            return "rising"
        elif slope < -20:
            return "falling"
        else:
            return "stable"


class SkinConductanceMonitor:
    """Galvanic Skin Response (GSR) monitoring"""
    
    def __init__(self, sampling_rate: int = 10):
        """
        Initialize GSR monitor
        
        Args:
            sampling_rate: Sampling rate in Hz
        """
        self.sampling_rate = sampling_rate
        self.baseline = None
    
    def establish_baseline(self, readings: np.ndarray):
        """
        Establish baseline skin conductance
        
        Args:
            readings: Array of baseline readings
        """
        self.baseline = np.median(readings)
    
    def process_reading(self, raw_value: float) -> SkinConductanceReading:
        """
        Process raw GSR reading
        
        Args:
            raw_value: Raw conductance value
            
        Returns:
            SkinConductanceReading
        """
        # Convert to microsiemens if needed
        conductance = raw_value
        
        reading = SkinConductanceReading(
            timestamp=datetime.now(),
            conductance_microsiemens=conductance
        )
        
        return reading
    
    def detect_arousal_events(self, signal: np.ndarray, 
                             threshold: float = 0.05) -> List[int]:
        """
        Detect arousal events in GSR signal
        
        Args:
            signal: GSR signal
            threshold: Threshold for event detection
            
        Returns:
            List of event indices
        """
        if self.baseline is None:
            self.establish_baseline(signal[:int(len(signal)*0.1)])
        
        # Compute rapid changes
        diff = np.diff(signal)
        
        # Find peaks above threshold
        from scipy.signal import find_peaks
        peaks, _ = find_peaks(diff, height=threshold)
        
        return peaks.tolist()


# Simulator classes for testing
class BiometricSimulator:
    """Simulates biometric data for testing"""
    
    @staticmethod
    def generate_ecg(duration: float = 10.0, 
                    sampling_rate: int = 250,
                    heart_rate: float = 70.0) -> np.ndarray:
        """Generate simulated ECG signal"""
        n_samples = int(duration * sampling_rate)
        t = np.linspace(0, duration, n_samples)
        
        # Generate R-peaks at heart rate
        rr_interval = 60.0 / heart_rate  # seconds
        peak_times = np.arange(0, duration, rr_interval)
        
        # Create ECG-like signal
        ecg = np.zeros(n_samples)
        for peak_time in peak_times:
            peak_idx = int(peak_time * sampling_rate)
            if peak_idx < n_samples:
                # QRS complex
                width = int(0.1 * sampling_rate)
                start = max(0, peak_idx - width//2)
                end = min(n_samples, peak_idx + width//2)
                ecg[start:end] += np.exp(-((np.arange(len(ecg[start:end])) - width//2)**2) / (width/6)**2)
        
        # Add noise
        ecg += 0.05 * np.random.randn(n_samples)
        
        return ecg
    
    @staticmethod
    def generate_cortisol(time_of_day: int = 9) -> float:
        """
        Generate simulated cortisol level
        
        Args:
            time_of_day: Hour of day (0-23)
            
        Returns:
            Cortisol level in ng/mL
        """
        # Cortisol follows circadian rhythm
        # Peak in morning (6-8 AM), low in evening
        if 6 <= time_of_day <= 8:
            base = 400
        elif 9 <= time_of_day <= 12:
            base = 300
        elif 13 <= time_of_day <= 17:
            base = 150
        else:
            base = 75
        
        # Add random variation
        noise = np.random.normal(0, base * 0.2)
        return max(10, base + noise)
    
    @staticmethod
    def generate_gsr(duration: float = 10.0,
                    sampling_rate: int = 10,
                    arousal_level: str = "normal") -> np.ndarray:
        """
        Generate simulated GSR signal
        
        Args:
            duration: Duration in seconds
            sampling_rate: Sampling rate in Hz
            arousal_level: Level of arousal
            
        Returns:
            GSR signal array
        """
        n_samples = int(duration * sampling_rate)
        t = np.linspace(0, duration, n_samples)
        
        # Base conductance depends on arousal
        base_levels = {
            "low": 2.0,
            "normal": 5.0,
            "high": 10.0,
            "very_high": 15.0,
        }
        base = base_levels.get(arousal_level, 5.0)
        
        # Slow drift
        drift = base + 0.5 * np.sin(2 * np.pi * 0.05 * t)
        
        # Add random arousal events
        signal = drift.copy()
        n_events = np.random.randint(0, 3)
        for _ in range(n_events):
            event_time = np.random.uniform(0, duration)
            event_idx = int(event_time * sampling_rate)
            if event_idx < n_samples:
                # Add SCR (Skin Conductance Response)
                width = int(2 * sampling_rate)  # 2 second response
                start = event_idx
                end = min(n_samples, event_idx + width)
                signal[start:end] += np.exp(-np.arange(len(signal[start:end])) / (sampling_rate * 0.5))
        
        # Add noise
        signal += 0.1 * np.random.randn(n_samples)
        
        return signal
