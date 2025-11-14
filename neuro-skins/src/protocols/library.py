"""
Protocol Library
Defines all frequency protocols for different brain states
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class ProtocolType(Enum):
    """Types of protocols available"""
    GAMMA_BOOST = "gamma_40hz"
    TRAUMA_DELETE = "trauma_delete"
    VAGUS_OVERCLOCK = "vagus_overclock"
    ANXIETY_RELIEF = "anxiety_relief"
    WORKOUT_PRIME = "workout_prime"
    BERBERINE_ALERT = "berberine_alert"
    IRISIN_PRIME = "irisin_prime"
    KALI_SHIVA_SYNC = "kali_shiva_sync"
    EGO_DEATH_LAYER7 = "ego_death_layer7"
    FLOAT_TANK_LOCK = "float_tank_lock"


@dataclass
class FrequencyLayer:
    """Single frequency layer in a protocol"""
    frequency: float  # Hz
    amplitude: float  # 0.0 to 1.0
    duration: Optional[int] = None  # seconds, None = continuous
    modulation: Optional[str] = None  # 'sine', 'square', 'binaural', etc.
    phase_offset: float = 0.0  # degrees


@dataclass
class Protocol:
    """Complete protocol definition"""
    name: str
    protocol_type: ProtocolType
    description: str
    
    # Target outcomes
    target_brain_state: str
    expected_duration: int  # minutes
    
    # Frequency layers
    layers: List[FrequencyLayer]
    
    # Transducer mapping
    transducer_routing: Dict[str, List[int]]  # location -> layer indices
    
    # Safety requirements
    max_duration: int  # minutes
    age_restriction: int = 18
    contraindications: List[str] = None
    
    # Tier access
    required_tier: str = "lite"
    
    def __post_init__(self):
        if self.contraindications is None:
            self.contraindications = []


# Protocol Library Definitions

GAMMA_40HZ = Protocol(
    name="40 Hz Gamma Boost",
    protocol_type=ProtocolType.GAMMA_BOOST,
    description="Entrains gamma oscillations for peak cognitive performance",
    target_brain_state="focused",
    expected_duration=20,
    layers=[
        FrequencyLayer(frequency=40.0, amplitude=0.7, modulation="sine"),
    ],
    transducer_routing={
        "crown": [0],
        "mastoid_left": [0],
        "mastoid_right": [0],
    },
    max_duration=90,
    required_tier="lite"
)

TRAUMA_DELETE = Protocol(
    name="Trauma Pattern Deletion",
    protocol_type=ProtocolType.TRAUMA_DELETE,
    description="Disrupts maladaptive neural patterns using targeted frequencies",
    target_brain_state="relaxed",
    expected_duration=15,
    layers=[
        FrequencyLayer(frequency=7.83, amplitude=0.5, modulation="sine"),  # Schumann
        FrequencyLayer(frequency=40.0, amplitude=0.3, modulation="binaural"),
    ],
    transducer_routing={
        "crown": [0, 1],
        "mastoid_left": [1],
        "mastoid_right": [1],
    },
    max_duration=30,
    required_tier="lite"
)

VAGUS_OVERCLOCK = Protocol(
    name="Vagus Nerve Overclock",
    protocol_type=ProtocolType.VAGUS_OVERCLOCK,
    description="Stimulates vagus nerve for parasympathetic activation",
    target_brain_state="relaxed",
    expected_duration=10,
    layers=[
        FrequencyLayer(frequency=0.618, amplitude=0.8, modulation="sine"),  # Golden ratio
        FrequencyLayer(frequency=40.0, amplitude=0.5, modulation="sine"),
    ],
    transducer_routing={
        "mastoid_left": [0],
        "mastoid_right": [0],
        "c7": [0],
        "crown": [1],
    },
    max_duration=30,
    required_tier="pro"
)

ANXIETY_RELIEF = Protocol(
    name="Anxiety Spike Relief",
    protocol_type=ProtocolType.ANXIETY_RELIEF,
    description="Rapid anxiety reduction through vagus + gamma combination",
    target_brain_state="relaxed",
    expected_duration=15,
    layers=[
        FrequencyLayer(frequency=40.0, amplitude=0.6, modulation="sine"),
        FrequencyLayer(frequency=0.618, amplitude=0.7, modulation="sine"),
        FrequencyLayer(frequency=7.83, amplitude=0.4, modulation="sine"),
    ],
    transducer_routing={
        "crown": [0],
        "mastoid_left": [1],
        "mastoid_right": [1],
        "c7": [1],
        "chest": [2],
    },
    max_duration=30,
    required_tier="pro"
)

WORKOUT_PRIME = Protocol(
    name="Workout Prime",
    protocol_type=ProtocolType.WORKOUT_PRIME,
    description="Pre-workout optimization with berberine alert + irisin prime",
    target_brain_state="workout_mode",
    expected_duration=10,
    layers=[
        FrequencyLayer(frequency=20.0, amplitude=0.8, modulation="square"),  # Beta high
        FrequencyLayer(frequency=40.0, amplitude=0.6, modulation="sine"),    # Gamma
        FrequencyLayer(frequency=8.0, amplitude=0.4, modulation="sine"),     # Low alpha
    ],
    transducer_routing={
        "crown": [1],
        "chest": [0],
        "sacrum": [2],
    },
    max_duration=20,
    required_tier="pro"
)

BERBERINE_ALERT = Protocol(
    name="Berberine Alert State",
    protocol_type=ProtocolType.BERBERINE_ALERT,
    description="Metabolic optimization alert state",
    target_brain_state="focused",
    expected_duration=15,
    layers=[
        FrequencyLayer(frequency=25.0, amplitude=0.7, modulation="sine"),
        FrequencyLayer(frequency=40.0, amplitude=0.5, modulation="sine"),
    ],
    transducer_routing={
        "crown": [1],
        "chest": [0],
    },
    max_duration=45,
    required_tier="pro"
)

KALI_SHIVA_SYNC = Protocol(
    name="Kali/Shiva Synchronization",
    protocol_type=ProtocolType.KALI_SHIVA_SYNC,
    description="Tantric frequency synchronization for sexual energy work",
    target_brain_state="sex_mode",
    expected_duration=30,
    layers=[
        FrequencyLayer(frequency=7.83, amplitude=0.6, modulation="sine"),   # Schumann
        FrequencyLayer(frequency=0.618, amplitude=0.8, modulation="sine"),  # Golden ratio
        FrequencyLayer(frequency=3.0, amplitude=0.5, modulation="sine"),    # Deep delta
        FrequencyLayer(frequency=40.0, amplitude=0.4, modulation="binaural"),
    ],
    transducer_routing={
        "crown": [3],
        "sacrum": [0, 1],
        "pubic": [1, 2],
        "chest": [0],
    },
    max_duration=60,
    age_restriction=18,
    required_tier="ascend",
    contraindications=[
        "Pacemaker",
        "Pregnancy",
        "Epilepsy"
    ]
)

EGO_DEATH_LAYER7 = Protocol(
    name="Layer 7 Ego Death",
    protocol_type=ProtocolType.EGO_DEATH_LAYER7,
    description="Deep ego dissolution for advanced consciousness work (Day 23+)",
    target_brain_state="meditation",
    expected_duration=45,
    layers=[
        FrequencyLayer(frequency=0.5, amplitude=0.3, modulation="sine"),    # Deep delta
        FrequencyLayer(frequency=4.0, amplitude=0.4, modulation="sine"),    # Theta
        FrequencyLayer(frequency=7.83, amplitude=0.5, modulation="sine"),   # Schumann
        FrequencyLayer(frequency=0.618, amplitude=0.6, modulation="sine"),  # Golden
        FrequencyLayer(frequency=40.0, amplitude=0.3, modulation="binaural"),
    ],
    transducer_routing={
        "crown": [4],
        "mastoid_left": [1, 2],
        "mastoid_right": [1, 2],
        "c7": [3],
        "sacrum": [0],
    },
    max_duration=90,
    age_restriction=21,
    required_tier="ascend",
    contraindications=[
        "Active psychosis",
        "Severe anxiety",
        "First 22 days of use",
        "Not for beginners"
    ]
)

FLOAT_TANK_LOCK = Protocol(
    name="Float Tank Lock",
    protocol_type=ProtocolType.FLOAT_TANK_LOCK,
    description="Optimized for sensory deprivation tank use",
    target_brain_state="meditation",
    expected_duration=60,
    layers=[
        FrequencyLayer(frequency=0.5, amplitude=0.2, modulation="sine"),
        FrequencyLayer(frequency=4.0, amplitude=0.3, modulation="sine"),
        FrequencyLayer(frequency=7.83, amplitude=0.4, modulation="sine"),
        FrequencyLayer(frequency=40.0, amplitude=0.2, modulation="binaural"),
    ],
    transducer_routing={
        "crown": [3],
        "mastoid_left": [1, 2],
        "mastoid_right": [1, 2],
        "sacrum": [0],
    },
    max_duration=120,
    required_tier="ascend"
)


# Protocol Registry
PROTOCOL_REGISTRY: Dict[str, Protocol] = {
    "gamma_40hz": GAMMA_40HZ,
    "trauma_delete": TRAUMA_DELETE,
    "vagus_overclock": VAGUS_OVERCLOCK,
    "anxiety_relief": ANXIETY_RELIEF,
    "workout_prime": WORKOUT_PRIME,
    "berberine_alert": BERBERINE_ALERT,
    "kali_shiva_sync": KALI_SHIVA_SYNC,
    "ego_death_layer7": EGO_DEATH_LAYER7,
    "float_tank_lock": FLOAT_TANK_LOCK,
}


def get_protocol(protocol_name: str) -> Optional[Protocol]:
    """Retrieve a protocol by name"""
    return PROTOCOL_REGISTRY.get(protocol_name)


def get_protocols_for_tier(tier: str) -> List[Protocol]:
    """Get all protocols available for a given tier"""
    tier_hierarchy = {
        "lite": ["lite"],
        "pro": ["lite", "pro"],
        "ascend": ["lite", "pro", "ascend"],
    }
    
    available_tiers = tier_hierarchy.get(tier.lower(), ["lite"])
    return [
        protocol for protocol in PROTOCOL_REGISTRY.values()
        if protocol.required_tier in available_tiers
    ]
