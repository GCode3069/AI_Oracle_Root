"""
Data models for NeuroSkins system
Brain states, sensor readings, and session data
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
import numpy as np


class BrainState(Enum):
    """Detected brain states"""
    MORNING_FOG = "morning_fog"
    ANXIETY_SPIKE = "anxiety_spike"
    WORKOUT_MODE = "workout_mode"
    RELAXED = "relaxed"
    FOCUSED = "focused"
    STRESSED = "stressed"
    SEX_MODE = "sex_mode"
    MEDITATION = "meditation"
    SLEEP_PREP = "sleep_prep"
    UNKNOWN = "unknown"


class SessionPhase(Enum):
    """Session execution phases"""
    CALIBRATION = "calibration"
    ACTIVE = "active"
    COOLDOWN = "cooldown"
    COMPLETE = "complete"
    EMERGENCY_STOP = "emergency_stop"


@dataclass
class EEGReading:
    """EEG sensor data"""
    timestamp: datetime
    channels: Dict[str, np.ndarray]  # Channel name -> signal data
    sampling_rate: int
    
    # Computed band powers (μV²)
    delta_power: float = 0.0
    theta_power: float = 0.0
    alpha_power: float = 0.0
    beta_power: float = 0.0
    gamma_power: float = 0.0
    
    # Quality metrics
    signal_quality: float = 1.0  # 0.0 to 1.0
    artifacts_detected: bool = False
    
    def get_dominant_band(self) -> str:
        """Get the dominant frequency band"""
        bands = {
            'delta': self.delta_power,
            'theta': self.theta_power,
            'alpha': self.alpha_power,
            'beta': self.beta_power,
            'gamma': self.gamma_power,
        }
        return max(bands, key=bands.get)


@dataclass
class HRVReading:
    """Heart Rate Variability data"""
    timestamp: datetime
    heart_rate: float  # bpm
    rmssd: float  # Root mean square of successive differences
    sdnn: float  # Standard deviation of NN intervals
    pnn50: float  # Percentage of successive intervals >50ms
    lf_hf_ratio: float  # Low frequency / High frequency ratio
    
    def is_stressed(self) -> bool:
        """Detect stress from HRV metrics"""
        return self.lf_hf_ratio > 2.0 or self.rmssd < 20


@dataclass
class CortisolReading:
    """Cortisol level measurement"""
    timestamp: datetime
    level_ng_ml: float  # Cortisol level in ng/mL
    sample_type: str = "saliva"
    
    def is_elevated(self) -> bool:
        """Check if cortisol is elevated"""
        # Normal morning: 100-750 ng/mL
        # Normal evening: 50-200 ng/mL
        hour = self.timestamp.hour
        if 6 <= hour < 12:  # Morning
            return self.level_ng_ml > 750
        else:  # Afternoon/evening
            return self.level_ng_ml > 200


@dataclass
class SkinConductanceReading:
    """Galvanic Skin Response data"""
    timestamp: datetime
    conductance_microsiemens: float
    
    def is_aroused(self) -> bool:
        """Detect autonomic arousal"""
        return self.conductance_microsiemens > 10.0


@dataclass
class SensorData:
    """Combined sensor readings"""
    timestamp: datetime
    eeg: Optional[EEGReading] = None
    hrv: Optional[HRVReading] = None
    cortisol: Optional[CortisolReading] = None
    skin_conductance: Optional[SkinConductanceReading] = None
    
    # Aggregate metrics
    stress_score: float = 0.0  # 0.0 to 1.0
    focus_score: float = 0.0
    energy_score: float = 0.0


@dataclass
class ProtocolState:
    """Current protocol execution state"""
    protocol_name: str
    start_time: datetime
    duration_minutes: int
    frequencies: List[float]
    amplitudes: Dict[str, float]  # Transducer location -> amplitude
    phase: SessionPhase = SessionPhase.CALIBRATION
    
    # Real-time adjustments
    current_frequency: float = 0.0
    current_amplitude: float = 0.0
    adaptation_factor: float = 1.0


@dataclass
class SessionData:
    """Complete session record"""
    session_id: str
    user_id: str
    tier: str
    start_time: datetime
    end_time: Optional[datetime] = None
    
    # Initial state
    initial_brain_state: BrainState = BrainState.UNKNOWN
    target_state: BrainState = BrainState.UNKNOWN
    
    # Protocol execution
    protocol: Optional[ProtocolState] = None
    
    # Data streams
    sensor_readings: List[SensorData] = field(default_factory=list)
    
    # Outcomes
    final_brain_state: BrainState = BrainState.UNKNOWN
    effectiveness_score: float = 0.0  # 0.0 to 1.0
    user_rating: Optional[int] = None  # 1-5 stars
    
    # Safety events
    safety_warnings: List[str] = field(default_factory=list)
    emergency_stops: int = 0
    
    def duration_seconds(self) -> float:
        """Calculate session duration"""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return (datetime.now() - self.start_time).total_seconds()
    
    def add_sensor_reading(self, reading: SensorData):
        """Add a new sensor reading"""
        self.sensor_readings.append(reading)
    
    def add_safety_warning(self, warning: str):
        """Log a safety warning"""
        self.safety_warnings.append(f"{datetime.now()}: {warning}")


@dataclass
class BrainStateClassification:
    """AI classification result"""
    timestamp: datetime
    predicted_state: BrainState
    confidence: float  # 0.0 to 1.0
    probabilities: Dict[BrainState, float]
    
    # Feature importance
    dominant_features: Dict[str, float]
    
    def is_confident(self, threshold: float = 0.75) -> bool:
        """Check if prediction is confident enough"""
        return self.confidence >= threshold
