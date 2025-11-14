"""
Safety Monitoring System
Enforces limits and emergency shutoff
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, field

from ..core.models import SensorData, SessionData, SessionPhase
from ..core.config import SafetyLimits


@dataclass
class SafetyEvent:
    """Safety event record"""
    timestamp: datetime
    event_type: str
    severity: str  # 'warning', 'critical', 'emergency'
    message: str
    sensor_data: Optional[SensorData] = None
    action_taken: str = ""


class SafetyMonitor:
    """Monitors safety limits and triggers emergency stops"""
    
    def __init__(self, limits: SafetyLimits):
        """
        Initialize safety monitor
        
        Args:
            limits: Safety limit configuration
        """
        self.limits = limits
        self.events: List[SafetyEvent] = []
        
        # Session tracking
        self.session_start: Optional[datetime] = None
        self.gamma_start: Optional[datetime] = None
        self.gamma_duration: float = 0.0  # minutes
        
        # Alert state
        self.warning_count = 0
        self.critical_count = 0
        self.emergency_stop_triggered = False
    
    def start_session(self):
        """Start monitoring a new session"""
        self.session_start = datetime.now()
        self.gamma_start = None
        self.gamma_duration = 0.0
        self.warning_count = 0
        self.critical_count = 0
        self.emergency_stop_triggered = False
    
    def start_gamma_protocol(self):
        """Track gamma protocol start"""
        self.gamma_start = datetime.now()
    
    def check_safety(self, sensor_data: SensorData) -> List[SafetyEvent]:
        """
        Check all safety conditions
        
        Args:
            sensor_data: Current sensor readings
            
        Returns:
            List of safety events detected
        """
        events = []
        
        # Check heart rate
        if sensor_data.hrv:
            hr_events = self._check_heart_rate(sensor_data.hrv.heart_rate, sensor_data)
            events.extend(hr_events)
        
        # Check gamma duration
        if self.gamma_start:
            duration_events = self._check_gamma_duration(sensor_data)
            events.extend(duration_events)
        
        # Check signal quality
        if sensor_data.eeg and sensor_data.eeg.signal_quality < 0.3:
            events.append(SafetyEvent(
                timestamp=datetime.now(),
                event_type="poor_signal_quality",
                severity="warning",
                message="EEG signal quality degraded. Check sensor contact.",
                sensor_data=sensor_data
            ))
        
        # Store events
        self.events.extend(events)
        
        # Update counters
        for event in events:
            if event.severity == 'warning':
                self.warning_count += 1
            elif event.severity == 'critical':
                self.critical_count += 1
            elif event.severity == 'emergency':
                self.emergency_stop_triggered = True
        
        return events
    
    def _check_heart_rate(self, heart_rate: float, 
                         sensor_data: SensorData) -> List[SafetyEvent]:
        """Check heart rate limits"""
        events = []
        
        # Emergency shutoff
        if heart_rate > self.limits.emergency_shutoff_hr:
            events.append(SafetyEvent(
                timestamp=datetime.now(),
                event_type="heart_rate_emergency",
                severity="emergency",
                message=f"Heart rate {heart_rate:.0f} bpm exceeds emergency limit {self.limits.emergency_shutoff_hr} bpm. EMERGENCY STOP!",
                sensor_data=sensor_data,
                action_taken="emergency_stop"
            ))
        
        # Critical warning
        elif heart_rate > self.limits.max_heart_rate:
            events.append(SafetyEvent(
                timestamp=datetime.now(),
                event_type="heart_rate_critical",
                severity="critical",
                message=f"Heart rate {heart_rate:.0f} bpm exceeds safety limit {self.limits.max_heart_rate} bpm.",
                sensor_data=sensor_data,
                action_taken="reduce_amplitude"
            ))
        
        # Warning
        elif heart_rate > self.limits.max_heart_rate * 0.9:
            events.append(SafetyEvent(
                timestamp=datetime.now(),
                event_type="heart_rate_warning",
                severity="warning",
                message=f"Heart rate {heart_rate:.0f} bpm approaching safety limit.",
                sensor_data=sensor_data
            ))
        
        return events
    
    def _check_gamma_duration(self, sensor_data: SensorData) -> List[SafetyEvent]:
        """Check 40 Hz gamma protocol duration"""
        events = []
        
        if not self.gamma_start:
            return events
        
        # Calculate duration
        elapsed = (datetime.now() - self.gamma_start).total_seconds() / 60.0
        self.gamma_duration = elapsed
        
        # Check against limit
        if elapsed > self.limits.max_gamma_duration:
            events.append(SafetyEvent(
                timestamp=datetime.now(),
                event_type="gamma_duration_exceeded",
                severity="critical",
                message=f"40 Hz gamma protocol duration {elapsed:.0f} min exceeds limit {self.limits.max_gamma_duration} min.",
                sensor_data=sensor_data,
                action_taken="stop_gamma"
            ))
        
        # Warning at 80%
        elif elapsed > self.limits.max_gamma_duration * 0.8:
            events.append(SafetyEvent(
                timestamp=datetime.now(),
                event_type="gamma_duration_warning",
                severity="warning",
                message=f"40 Hz gamma protocol approaching duration limit ({elapsed:.0f}/{self.limits.max_gamma_duration} min).",
                sensor_data=sensor_data
            ))
        
        return events
    
    def should_emergency_stop(self) -> bool:
        """Check if emergency stop should be triggered"""
        return self.emergency_stop_triggered
    
    def should_reduce_amplitude(self) -> bool:
        """Check if amplitude should be reduced"""
        return self.critical_count > 0
    
    def get_safety_score(self) -> float:
        """
        Calculate overall safety score (0.0 to 1.0)
        
        Returns:
            Safety score (1.0 = perfectly safe, 0.0 = emergency)
        """
        if self.emergency_stop_triggered:
            return 0.0
        
        score = 1.0
        
        # Penalize for warnings
        score -= self.warning_count * 0.1
        
        # Penalize for critical events
        score -= self.critical_count * 0.3
        
        return max(0.0, min(1.0, score))
    
    def get_recent_events(self, minutes: int = 5) -> List[SafetyEvent]:
        """
        Get recent safety events
        
        Args:
            minutes: Time window in minutes
            
        Returns:
            List of recent events
        """
        cutoff = datetime.now() - timedelta(minutes=minutes)
        return [e for e in self.events if e.timestamp >= cutoff]
    
    def get_safety_report(self) -> Dict:
        """Generate safety report"""
        return {
            'safety_score': self.get_safety_score(),
            'warning_count': self.warning_count,
            'critical_count': self.critical_count,
            'emergency_stop_triggered': self.emergency_stop_triggered,
            'gamma_duration_minutes': self.gamma_duration,
            'recent_events': [
                {
                    'timestamp': e.timestamp.isoformat(),
                    'type': e.event_type,
                    'severity': e.severity,
                    'message': e.message,
                }
                for e in self.get_recent_events(5)
            ]
        }


class AgeVerifier:
    """Verifies user age for restricted protocols"""
    
    def __init__(self):
        self.verified_users: Dict[str, int] = {}  # user_id -> age
    
    def verify_age(self, user_id: str, age: int) -> bool:
        """
        Verify user age
        
        Args:
            user_id: User identifier
            age: User age
            
        Returns:
            True if verification successful
        """
        if age < 18:
            return False
        
        self.verified_users[user_id] = age
        return True
    
    def can_access_protocol(self, user_id: str, 
                           protocol_age_restriction: int) -> bool:
        """
        Check if user can access protocol
        
        Args:
            user_id: User identifier
            protocol_age_restriction: Minimum age for protocol
            
        Returns:
            True if access allowed
        """
        user_age = self.verified_users.get(user_id)
        
        if user_age is None:
            return False
        
        return user_age >= protocol_age_restriction


class DataEncryption:
    """Handles on-device data encryption"""
    
    def __init__(self, enabled: bool = True):
        """
        Initialize encryption
        
        Args:
            enabled: Whether encryption is enabled
        """
        self.enabled = enabled
        self.key = None
        
        if enabled:
            self._generate_key()
    
    def _generate_key(self):
        """Generate encryption key"""
        from cryptography.fernet import Fernet
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
    
    def encrypt_session_data(self, session: SessionData) -> bytes:
        """
        Encrypt session data
        
        Args:
            session: Session data to encrypt
            
        Returns:
            Encrypted data
        """
        if not self.enabled:
            return str(session).encode()
        
        import json
        
        # Convert to JSON
        data = {
            'session_id': session.session_id,
            'user_id': session.user_id,
            'tier': session.tier,
            'start_time': session.start_time.isoformat(),
            'end_time': session.end_time.isoformat() if session.end_time else None,
            'initial_brain_state': session.initial_brain_state.value,
            'final_brain_state': session.final_brain_state.value,
            'effectiveness_score': session.effectiveness_score,
        }
        
        json_data = json.dumps(data).encode()
        
        # Encrypt
        return self.cipher.encrypt(json_data)
    
    def decrypt_session_data(self, encrypted_data: bytes) -> Dict:
        """
        Decrypt session data
        
        Args:
            encrypted_data: Encrypted session data
            
        Returns:
            Decrypted data dictionary
        """
        if not self.enabled:
            return {}
        
        import json
        
        # Decrypt
        decrypted = self.cipher.decrypt(encrypted_data)
        
        # Parse JSON
        return json.loads(decrypted.decode())
