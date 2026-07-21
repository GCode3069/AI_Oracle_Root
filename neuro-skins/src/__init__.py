"""
NeuroSkins × Frequency Fusion: Adaptive Neural Interface
Main package initialization
"""

__version__ = "0.1.0"
__author__ = "GCode3069"
__license__ = "Proprietary"

from .core.system import NeuroSkinsSystem
from .core.config import SystemConfig, TierConfig

__all__ = [
    "NeuroSkinsSystem",
    "SystemConfig",
    "TierConfig",
]
