"""
NeuroSkins Configuration System
Defines system tiers, hardware configs, and protocol settings
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class ProductTier(Enum):
    """Product tier levels"""
    LITE = "lite"
    PRO = "pro"
    ASCEND = "ascend"


class BrainWave(Enum):
    """Brain wave frequency bands"""
    DELTA = "delta"      # 0.5-4 Hz (deep sleep)
    THETA = "theta"      # 4-8 Hz (meditation)
    ALPHA = "alpha"      # 8-13 Hz (relaxation)
    BETA = "beta"        # 13-30 Hz (active thinking)
    GAMMA = "gamma"      # 30-100 Hz (peak cognition)


class TransducerLocation(Enum):
    """Bone conduction transducer placement locations"""
    CROWN = "crown"
    MASTOID_LEFT = "mastoid_left"
    MASTOID_RIGHT = "mastoid_right"
    C7 = "c7"
    CHEST = "chest"
    SACRUM = "sacrum"
    PUBIC = "pubic"


@dataclass
class TierConfig:
    """Configuration for a specific product tier"""
    tier: ProductTier
    price: int
    features: List[str]
    max_session_duration: int  # minutes
    protocols_available: List[str]
    sensors_included: List[str]
    transducers_included: List[TransducerLocation]
    age_restriction: int = 18


@dataclass
class SafetyLimits:
    """Safety limits and thresholds"""
    max_gamma_duration: int = 90  # minutes
    max_heart_rate: int = 185  # bpm
    min_age_sex_stacks: int = 18
    max_amplitude_db: float = 85.0
    emergency_shutoff_hr: int = 195
    data_encryption_required: bool = True
    on_device_only: bool = True


@dataclass
class HardwareConfig:
    """Hardware specifications"""
    ram_gb: int = 8
    battery_hours: int = 12
    ai_framework: str = "TensorFlow Lite"
    bluetooth_version: str = "5.2"
    max_frequency_hz: float = 200.0
    min_frequency_hz: float = 0.1
    response_time_ms: int = 50


@dataclass
class SystemConfig:
    """Main system configuration"""
    tier: ProductTier
    tier_config: TierConfig
    hardware: HardwareConfig = field(default_factory=HardwareConfig)
    safety: SafetyLimits = field(default_factory=SafetyLimits)
    
    # System settings
    sampling_rate: int = 256  # Hz for EEG
    buffer_size: int = 512
    update_interval: float = 0.02  # 50ms = 20 Hz update rate
    
    # AI settings
    model_path: Optional[str] = None
    confidence_threshold: float = 0.75
    
    # Data storage
    data_path: str = "./data"
    session_log_enabled: bool = True
    
    @classmethod
    def create_for_tier(cls, tier: ProductTier) -> 'SystemConfig':
        """Factory method to create config for specific tier"""
        tier_configs = {
            ProductTier.LITE: TierConfig(
                tier=ProductTier.LITE,
                price=299,
                features=[
                    "Basic 40 Hz gamma boost",
                    "Trauma pattern deletion",
                    "Morning fog protocol",
                ],
                max_session_duration=20,
                protocols_available=["gamma_40hz", "trauma_delete"],
                sensors_included=["eeg_basic"],
                transducers_included=[
                    TransducerLocation.CROWN,
                    TransducerLocation.MASTOID_LEFT,
                    TransducerLocation.MASTOID_RIGHT,
                ]
            ),
            ProductTier.PRO: TierConfig(
                tier=ProductTier.PRO,
                price=899,
                features=[
                    "Full Forge protocol suite",
                    "HRV monitoring",
                    "Cortisol tracking",
                    "Anxiety/stress protocols",
                    "Workout optimization",
                ],
                max_session_duration=90,
                protocols_available=[
                    "gamma_40hz", "trauma_delete", "vagus_overclock",
                    "anxiety_relief", "workout_prime", "berberine_alert"
                ],
                sensors_included=["eeg_full", "hrv", "skin_conductance"],
                transducers_included=[
                    TransducerLocation.CROWN,
                    TransducerLocation.MASTOID_LEFT,
                    TransducerLocation.MASTOID_RIGHT,
                    TransducerLocation.C7,
                    TransducerLocation.CHEST,
                ]
            ),
            ProductTier.ASCEND: TierConfig(
                tier=ProductTier.ASCEND,
                price=2499,
                features=[
                    "Everything in Pro",
                    "Kali/Shiva sex synchronization",
                    "Partner sync capability",
                    "Layer 7 ego death protocol",
                    "Float tank integration",
                    "Advanced cortisol monitoring",
                ],
                max_session_duration=180,
                protocols_available=[
                    "gamma_40hz", "trauma_delete", "vagus_overclock",
                    "anxiety_relief", "workout_prime", "berberine_alert",
                    "kali_shiva_sync", "ego_death_layer7", "float_tank_lock"
                ],
                sensors_included=[
                    "eeg_full", "hrv", "skin_conductance", "cortisol_saliva"
                ],
                transducers_included=list(TransducerLocation),
            ),
        }
        
        return cls(
            tier=tier,
            tier_config=tier_configs[tier]
        )


# Default configurations for each tier
LITE_CONFIG = SystemConfig.create_for_tier(ProductTier.LITE)
PRO_CONFIG = SystemConfig.create_for_tier(ProductTier.PRO)
ASCEND_CONFIG = SystemConfig.create_for_tier(ProductTier.ASCEND)
