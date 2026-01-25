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


# Real hardware interfaces for biometric sensors
class HRVHardware:
    """Real HRV sensor via Bluetooth heart rate monitors"""
    
    def __init__(self, sampling_rate: int = 250):
        self.sampling_rate = sampling_rate
        self.device = None
        
    def connect(self) -> bool:
        """Connect to Bluetooth heart rate monitor"""
        try:
            from bleak import BleakScanner, BleakClient
            import asyncio
            
            async def scan_hr_device():
                print("[INFO] Scanning for heart rate monitor...")
                devices = await BleakScanner.discover()
                hr_devices = [d for d in devices if 'heart' in d.name.lower() or 'hrm' in d.name.lower()]
                
                if not hr_devices:
                    print("[ERROR] No heart rate monitor found")
                    return None
                
                device = hr_devices[0]
                client = BleakClient(device.address)
                await client.connect()
                
                if client.is_connected:
                    print(f"[OK] Connected to {device.name}")
                    return client
                
                return None
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            self.device = loop.run_until_complete(scan_hr_device())
            
            return self.device is not None
            
        except ImportError:
            print("[ERROR] bleak not installed. Run: pip install bleak")
            return False
        except Exception as e:
            print(f"[ERROR] HRV connection failed: {e}")
            return False
    
    def read_hr_data(self, duration: float = 10.0) -> np.ndarray:
        """Read RR intervals from heart rate monitor"""
        import asyncio
        
        # Standard Bluetooth Heart Rate Service UUID
        HR_SERVICE_UUID = "0000180D-0000-1000-8000-00805F9B34FB"
        HR_MEASUREMENT_UUID = "00002A37-0000-1000-8000-00805F9B34FB"
        
        rr_intervals = []
        
        async def read_hr():
            if not self.device or not self.device.is_connected:
                raise RuntimeError("Device not connected")
            
            def hr_callback(sender, data):
                # Parse Bluetooth HRM data format
                flags = data[0]
                hr_value = data[1]
                
                # Check if RR intervals present (bit 4 of flags)
                if flags & 0x10:
                    # RR intervals are 16-bit values in 1/1024 second units
                    idx = 2
                    while idx + 1 < len(data):
                        rr = int.from_bytes(data[idx:idx+2], 'little')
                        rr_ms = (rr / 1024.0) * 1000
                        rr_intervals.append(rr_ms)
                        idx += 2
            
            await self.device.start_notify(HR_MEASUREMENT_UUID, hr_callback)
            await asyncio.sleep(duration)
            await self.device.stop_notify(HR_MEASUREMENT_UUID)
        
        loop = asyncio.get_event_loop()
        loop.run_until_complete(read_hr())
        
        return np.array(rr_intervals)


class CortisolHardware:
    """Real cortisol sensor via electrochemical biosensor"""
    
    def __init__(self):
        self.sensor = None
        
    def connect(self) -> bool:
        """Connect to cortisol biosensor via USB/Serial"""
        try:
            import serial
            import serial.tools.list_ports
            
            ports = list(serial.tools.list_ports.comports())
            for port in ports:
                if 'cortisol' in port.description.lower() or 'biosensor' in port.description.lower():
                    self.sensor = serial.Serial(port.device, 115200, timeout=1)
                    print(f"[OK] Connected to cortisol sensor on {port.device}")
                    return True
            
            print("[ERROR] No cortisol sensor found")
            return False
            
        except ImportError:
            print("[ERROR] pyserial not installed. Run: pip install pyserial")
            return False
        except Exception as e:
            print(f"[ERROR] Cortisol sensor connection failed: {e}")
            return False
    
    def read_level(self) -> float:
        """Read cortisol level from electrochemical sensor"""
        if not self.sensor:
            raise RuntimeError("Sensor not connected")
        
        # Send read command
        self.sensor.write(b'READ\n')
        response = self.sensor.readline().decode('utf-8').strip()
        
        # Parse response (format: "CORTISOL:xxx.xx ng/mL")
        if response.startswith('CORTISOL:'):
            value_str = response.split(':')[1].replace(' ng/mL', '')
            return float(value_str)
        
        raise ValueError(f"Invalid sensor response: {response}")


class GSRHardware:
    """Real GSR sensor via galvanic skin response device"""
    
    def __init__(self, sampling_rate: int = 10):
        self.sampling_rate = sampling_rate
        self.sensor = None
        
    def connect(self) -> bool:
        """Connect to GSR sensor via USB"""
        try:
            import serial
            import serial.tools.list_ports
            
            ports = list(serial.tools.list_ports.comports())
            for port in ports:
                if 'gsr' in port.description.lower() or 'galvanic' in port.description.lower():
                    self.sensor = serial.Serial(port.device, 9600, timeout=1)
                    print(f"[OK] Connected to GSR sensor on {port.device}")
                    return True
            
            print("[ERROR] No GSR sensor found")
            return False
            
        except ImportError:
            print("[ERROR] pyserial not installed. Run: pip install pyserial")
            return False
        except Exception as e:
            print(f"[ERROR] GSR connection failed: {e}")
            return False
    
    def read_signal(self, duration: float = 10.0) -> np.ndarray:
        """Read GSR signal from sensor"""
        if not self.sensor:
            raise RuntimeError("Sensor not connected")
        
        n_samples = int(duration * self.sampling_rate)
        samples = []
        
        for _ in range(n_samples):
            self.sensor.write(b'R\n')
            response = self.sensor.readline().decode('utf-8').strip()
            
            try:
                # Parse microsiemens value
                value = float(response)
                samples.append(value)
            except ValueError:
                print(f"[WARN] Invalid GSR reading: {response}")
                samples.append(samples[-1] if samples else 0.0)
            
            time.sleep(1.0 / self.sampling_rate)
        
        return np.array(samples)
