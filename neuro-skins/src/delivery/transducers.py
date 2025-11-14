"""
Frequency Delivery System
Bone conduction transducers and subwoofer control
"""

import numpy as np
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
import time

from ..core.config import TransducerLocation
from ..protocols.library import Protocol, FrequencyLayer


@dataclass
class TransducerState:
    """Current state of a transducer"""
    location: TransducerLocation
    frequency: float  # Hz
    amplitude: float  # 0.0 to 1.0
    phase: float  # degrees
    active: bool = False
    last_update: datetime = None


class FrequencyGenerator:
    """Generates frequency waveforms"""
    
    def __init__(self, sampling_rate: int = 44100):
        """
        Initialize frequency generator
        
        Args:
            sampling_rate: Audio sampling rate in Hz
        """
        self.sampling_rate = sampling_rate
    
    def generate_sine(self, frequency: float, duration: float,
                     amplitude: float = 1.0, phase: float = 0.0) -> np.ndarray:
        """
        Generate sine wave
        
        Args:
            frequency: Frequency in Hz
            duration: Duration in seconds
            amplitude: Amplitude (0.0 to 1.0)
            phase: Phase offset in degrees
            
        Returns:
            Waveform array
        """
        t = np.linspace(0, duration, int(self.sampling_rate * duration))
        phase_rad = np.deg2rad(phase)
        waveform = amplitude * np.sin(2 * np.pi * frequency * t + phase_rad)
        return waveform
    
    def generate_square(self, frequency: float, duration: float,
                       amplitude: float = 1.0) -> np.ndarray:
        """
        Generate square wave
        
        Args:
            frequency: Frequency in Hz
            duration: Duration in seconds
            amplitude: Amplitude (0.0 to 1.0)
            
        Returns:
            Waveform array
        """
        t = np.linspace(0, duration, int(self.sampling_rate * duration))
        waveform = amplitude * np.sign(np.sin(2 * np.pi * frequency * t))
        return waveform
    
    def generate_binaural(self, base_freq: float, beat_freq: float,
                         duration: float, amplitude: float = 1.0) -> tuple:
        """
        Generate binaural beat (stereo)
        
        Args:
            base_freq: Base frequency in Hz
            beat_freq: Beat frequency in Hz
            duration: Duration in seconds
            amplitude: Amplitude (0.0 to 1.0)
            
        Returns:
            (left_channel, right_channel) tuple
        """
        left = self.generate_sine(base_freq, duration, amplitude)
        right = self.generate_sine(base_freq + beat_freq, duration, amplitude)
        return left, right


class TransducerController:
    """Controls bone conduction transducers"""
    
    def __init__(self, response_time_ms: int = 50):
        """
        Initialize transducer controller
        
        Args:
            response_time_ms: Target response time in milliseconds
        """
        self.response_time_ms = response_time_ms
        self.response_time_sec = response_time_ms / 1000.0
        
        # Initialize transducer states
        self.transducers: Dict[TransducerLocation, TransducerState] = {
            location: TransducerState(
                location=location,
                frequency=0.0,
                amplitude=0.0,
                phase=0.0,
                active=False,
                last_update=datetime.now()
            )
            for location in TransducerLocation
        }
        
        self.generator = FrequencyGenerator()
        
        # Hardware interface (simulated)
        self.hardware_connected = False
    
    def connect_hardware(self) -> bool:
        """
        Connect to hardware transducers
        
        Returns:
            True if connection successful
        """
        # In production, this would connect to actual hardware
        # via Bluetooth, USB, or other interface
        print("[INFO] Connecting to transducer hardware...")
        time.sleep(0.1)
        self.hardware_connected = True
        print("[OK] Transducer hardware connected")
        return True
    
    def set_frequency(self, location: TransducerLocation,
                     frequency: float, amplitude: float,
                     phase: float = 0.0) -> bool:
        """
        Set frequency for a specific transducer
        
        Args:
            location: Transducer location
            frequency: Frequency in Hz
            amplitude: Amplitude (0.0 to 1.0)
            phase: Phase offset in degrees
            
        Returns:
            True if successful
        """
        if not self.hardware_connected:
            print("[WARN] Hardware not connected")
            return False
        
        start_time = time.time()
        
        # Update state
        state = self.transducers[location]
        state.frequency = frequency
        state.amplitude = amplitude
        state.phase = phase
        state.active = amplitude > 0
        state.last_update = datetime.now()
        
        # Send to hardware (simulated)
        self._send_to_hardware(location, frequency, amplitude, phase)
        
        # Check response time
        elapsed_ms = (time.time() - start_time) * 1000
        if elapsed_ms > self.response_time_ms:
            print(f"[WARN] Response time {elapsed_ms:.1f}ms exceeds target {self.response_time_ms}ms")
        
        return True
    
    def _send_to_hardware(self, location: TransducerLocation,
                         frequency: float, amplitude: float, phase: float):
        """Send command to hardware (simulated)"""
        # In production, this would send commands to actual hardware
        # For now, just simulate the delay
        time.sleep(0.001)  # 1ms simulated hardware delay
    
    def deploy_layer(self, layer: FrequencyLayer,
                    locations: List[TransducerLocation]) -> bool:
        """
        Deploy a frequency layer to multiple transducers
        
        Args:
            layer: Frequency layer to deploy
            locations: Target transducer locations
            
        Returns:
            True if successful
        """
        success = True
        
        for location in locations:
            result = self.set_frequency(
                location,
                layer.frequency,
                layer.amplitude,
                layer.phase_offset
            )
            success = success and result
        
        return success
    
    def deploy_protocol(self, protocol: Protocol) -> bool:
        """
        Deploy complete protocol to transducers
        
        Args:
            protocol: Protocol to deploy
            
        Returns:
            True if successful
        """
        print(f"[INFO] Deploying protocol: {protocol.name}")
        
        # Clear all transducers first
        self.stop_all()
        
        # Deploy each layer to its assigned transducers
        for layer_idx, layer in enumerate(protocol.layers):
            # Find transducers for this layer
            locations = []
            for location_str, layer_indices in protocol.transducer_routing.items():
                if layer_idx in layer_indices:
                    try:
                        location = TransducerLocation[location_str.upper()]
                        locations.append(location)
                    except KeyError:
                        print(f"[WARN] Unknown transducer location: {location_str}")
            
            if locations:
                self.deploy_layer(layer, locations)
        
        print(f"[OK] Protocol deployed to {len(protocol.layers)} layers")
        return True
    
    def adjust_amplitude(self, factor: float):
        """
        Adjust amplitude of all active transducers
        
        Args:
            factor: Multiplication factor (e.g., 0.5 = reduce by 50%)
        """
        for location, state in self.transducers.items():
            if state.active:
                new_amplitude = state.amplitude * factor
                self.set_frequency(location, state.frequency, new_amplitude, state.phase)
    
    def stop_all(self):
        """Stop all transducers"""
        for location in self.transducers:
            self.set_frequency(location, 0.0, 0.0, 0.0)
    
    def get_active_transducers(self) -> List[TransducerLocation]:
        """Get list of active transducers"""
        return [loc for loc, state in self.transducers.items() if state.active]
    
    def get_status(self) -> Dict:
        """Get status of all transducers"""
        return {
            'hardware_connected': self.hardware_connected,
            'response_time_ms': self.response_time_ms,
            'transducers': {
                loc.value: {
                    'active': state.active,
                    'frequency': state.frequency,
                    'amplitude': state.amplitude,
                    'phase': state.phase,
                }
                for loc, state in self.transducers.items()
            }
        }


class SubwooferController:
    """Controls subwoofer pads for felt vibration"""
    
    def __init__(self, min_freq: float = 0.1, max_freq: float = 200.0):
        """
        Initialize subwoofer controller
        
        Args:
            min_freq: Minimum frequency in Hz
            max_freq: Maximum frequency in Hz
        """
        self.min_freq = min_freq
        self.max_freq = max_freq
        
        self.current_frequency = 0.0
        self.current_amplitude = 0.0
        self.active = False
        
        self.generator = FrequencyGenerator(sampling_rate=2000)  # Lower rate for sub
    
    def set_vibration(self, frequency: float, amplitude: float) -> bool:
        """
        Set subwoofer vibration
        
        Args:
            frequency: Frequency in Hz
            amplitude: Amplitude (0.0 to 1.0)
            
        Returns:
            True if successful
        """
        # Clamp to valid range
        frequency = max(self.min_freq, min(frequency, self.max_freq))
        amplitude = max(0.0, min(amplitude, 1.0))
        
        self.current_frequency = frequency
        self.current_amplitude = amplitude
        self.active = amplitude > 0
        
        # Send to hardware (simulated)
        time.sleep(0.001)
        
        return True
    
    def stop(self):
        """Stop subwoofer"""
        self.set_vibration(0.0, 0.0)
    
    def get_status(self) -> Dict:
        """Get subwoofer status"""
        return {
            'active': self.active,
            'frequency': self.current_frequency,
            'amplitude': self.current_amplitude,
            'frequency_range': [self.min_freq, self.max_freq],
        }


class DeliverySystem:
    """Complete frequency delivery system"""
    
    def __init__(self, response_time_ms: int = 50):
        """
        Initialize delivery system
        
        Args:
            response_time_ms: Target response time in milliseconds
        """
        self.transducers = TransducerController(response_time_ms)
        self.subwoofer = SubwooferController()
        
        self.current_protocol: Optional[Protocol] = None
        self.active = False
    
    def initialize(self) -> bool:
        """Initialize hardware"""
        return self.transducers.connect_hardware()
    
    def deploy_protocol(self, protocol: Protocol) -> bool:
        """
        Deploy protocol to delivery system
        
        Args:
            protocol: Protocol to deploy
            
        Returns:
            True if successful
        """
        self.current_protocol = protocol
        
        # Deploy to transducers
        success = self.transducers.deploy_protocol(protocol)
        
        # Check if protocol uses subwoofer (very low frequencies)
        for layer in protocol.layers:
            if layer.frequency < 10.0:  # Sub-bass range
                self.subwoofer.set_vibration(layer.frequency, layer.amplitude * 0.5)
                break
        
        self.active = success
        return success
    
    def adjust_intensity(self, factor: float):
        """
        Adjust overall intensity
        
        Args:
            factor: Multiplication factor
        """
        self.transducers.adjust_amplitude(factor)
        if self.subwoofer.active:
            new_amp = self.subwoofer.current_amplitude * factor
            self.subwoofer.set_vibration(self.subwoofer.current_frequency, new_amp)
    
    def emergency_stop(self):
        """Emergency stop all outputs"""
        print("[EMERGENCY] Stopping all frequency delivery")
        self.transducers.stop_all()
        self.subwoofer.stop()
        self.active = False
    
    def get_status(self) -> Dict:
        """Get complete delivery system status"""
        return {
            'active': self.active,
            'current_protocol': self.current_protocol.name if self.current_protocol else None,
            'transducers': self.transducers.get_status(),
            'subwoofer': self.subwoofer.get_status(),
        }
