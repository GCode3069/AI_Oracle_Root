"""
NeuroSkins Main System
Orchestrates the complete closed-loop system
"""

import time
from datetime import datetime
from typing import Optional
import uuid

from .config import SystemConfig, ProductTier
from .models import (
    SensorData, SessionData, BrainState,
    EEGReading, HRVReading, CortisolReading,
    SkinConductanceReading, ProtocolState, SessionPhase
)
from ..sensors.eeg import EEGProcessor, EEGHardware
from ..sensors.biometric import HRVMonitor, CortisolMonitor, SkinConductanceMonitor, HRVHardware, CortisolHardware, GSRHardware
from ..ai.classifier import BrainStateClassifier, ProtocolSelector
from ..safety.monitor import SafetyMonitor, AgeVerifier, DataEncryption
from ..delivery.transducers import DeliverySystem
from ..protocols.library import Protocol


class NeuroSkinsSystem:
    """Main NeuroSkins system orchestrator"""
    
    def __init__(self, config: SystemConfig, user_id: str = "default"):
        """
        Initialize NeuroSkins system
        
        Args:
            config: System configuration
            user_id: User identifier
        """
        self.config = config
        self.user_id = user_id
        self.user_days = 0  # Days since user started
        
        # Initialize subsystems
        self.eeg_processor = EEGProcessor(config.sampling_rate)
        self.hrv_monitor = HRVMonitor()
        self.cortisol_monitor = CortisolMonitor()
        self.gsr_monitor = SkinConductanceMonitor()
        
        self.classifier = BrainStateClassifier(config.model_path)
        self.protocol_selector = ProtocolSelector(config.tier.value)
        
        self.safety_monitor = SafetyMonitor(config.safety)
        self.age_verifier = AgeVerifier()
        self.encryption = DataEncryption(config.safety.data_encryption_required)
        
        self.delivery_system = DeliverySystem(
            response_time_ms=config.update_interval * 1000
        )
        
        # Hardware interfaces
        self.eeg_hardware = EEGHardware(config.sampling_rate)
        self.hrv_hardware = HRVHardware()
        self.cortisol_hardware = CortisolHardware()
        self.gsr_hardware = GSRHardware()
        
        # Session state
        self.current_session: Optional[SessionData] = None
        self.running = False
        
        print(f"[OK] NeuroSkins {config.tier.value.upper()} initialized")
    
    def initialize_hardware(self) -> bool:
        """
        Initialize hardware connections
        
        Returns:
            True if successful
        """
        print("[INFO] Initializing hardware...")
        
        # Connect to delivery system
        if not self.delivery_system.initialize():
            print("[ERROR] Failed to initialize delivery system")
            return False
        
        # Connect EEG headset
        if not self.eeg_hardware.connect():
            print("[ERROR] Failed to connect EEG headset")
            return False
        
        # Connect HRV monitor
        if not self.hrv_hardware.connect():
            print("[WARN] HRV monitor not available")
        
        # Connect cortisol sensor (optional for some tiers)
        if 'cortisol_saliva' in self.config.tier_config.sensors_included:
            if not self.cortisol_hardware.connect():
                print("[WARN] Cortisol sensor not available")
        
        # Connect GSR sensor
        if 'skin_conductance' in self.config.tier_config.sensors_included:
            if not self.gsr_hardware.connect():
                print("[WARN] GSR sensor not available")
        
        print("[OK] Hardware initialized")
        return True
    
    def verify_user_age(self, age: int) -> bool:
        """
        Verify user age for system access
        
        Args:
            age: User age
            
        Returns:
            True if verification successful
        """
        return self.age_verifier.verify_age(self.user_id, age)
    
    def start_session(self) -> str:
        """
        Start a new session with real hardware
        
        Returns:
            Session ID
        """
        if self.running:
            print("[WARN] Session already running")
            return self.current_session.session_id
        
        # Create session
        session_id = str(uuid.uuid4())
        self.current_session = SessionData(
            session_id=session_id,
            user_id=self.user_id,
            tier=self.config.tier.value,
            start_time=datetime.now()
        )
        
        self.running = True
        self.safety_monitor.start_session()
        
        print(f"[OK] Session started: {session_id}")
        return session_id
    
    def read_sensors(self) -> SensorData:
        """
        Read all sensor data from real hardware
        
        Returns:
            Combined sensor data
        """
        # Read EEG from hardware
        eeg_channels = self.eeg_hardware.read_epoch(duration=self.config.update_interval)
        eeg_reading = self.eeg_processor.process_epoch(eeg_channels)
        
        # Read HRV from heart rate monitor
        hrv_reading = None
        try:
            rr_intervals = self.hrv_hardware.read_hr_data(duration=10.0)
            if len(rr_intervals) > 0:
                hrv_reading = self.hrv_monitor.compute_hrv_metrics(rr_intervals)
        except Exception as e:
            print(f"[WARN] HRV read failed: {e}")
        
        # Read cortisol from biosensor
        cortisol_reading = None
        if 'cortisol_saliva' in self.config.tier_config.sensors_included:
            try:
                cortisol_level = self.cortisol_hardware.read_level()
                cortisol_reading = self.cortisol_monitor.process_reading(cortisol_level)
            except Exception as e:
                print(f"[WARN] Cortisol read failed: {e}")
        
        # Read GSR from sensor
        gsr_reading = None
        if 'skin_conductance' in self.config.tier_config.sensors_included:
            try:
                gsr_signal = self.gsr_hardware.read_signal(duration=1.0)
                if len(gsr_signal) > 0:
                    gsr_reading = self.gsr_monitor.process_reading(gsr_signal[-1])
            except Exception as e:
                print(f"[WARN] GSR read failed: {e}")
        
        return SensorData(
            timestamp=datetime.now(),
            eeg=eeg_reading,
            hrv=hrv_reading,
            cortisol=cortisol_reading,
            skin_conductance=gsr_reading
        )
    
    def select_protocol(self, sensor_data: SensorData) -> Optional[Protocol]:
        """
        Select optimal protocol based on brain state
        
        Args:
            sensor_data: Current sensor readings
            
        Returns:
            Selected protocol or None
        """
        # Classify brain state
        classification = self.classifier.classify(sensor_data)
        
        # Store initial state
        if self.current_session and not self.current_session.initial_brain_state:
            self.current_session.initial_brain_state = classification.predicted_state
        
        # Check confidence
        if not classification.is_confident(self.config.confidence_threshold):
            print(f"[WARN] Low confidence classification: {classification.confidence:.2f}")
            return None
        
        # Select protocol
        protocol = self.protocol_selector.select_protocol(
            classification,
            user_days=self.user_days
        )
        
        # Verify age restriction
        if protocol and protocol.age_restriction > 0:
            if not self.age_verifier.can_access_protocol(
                self.user_id,
                protocol.age_restriction
            ):
                print(f"[ERROR] Age restriction: Protocol requires age {protocol.age_restriction}+")
                return None
        
        return protocol
    
    def deliver_protocol(self, protocol: Protocol) -> bool:
        """
        Deliver protocol via transducers
        
        Args:
            protocol: Protocol to deliver
            
        Returns:
            True if successful
        """
        # Deploy protocol
        success = self.delivery_system.deploy_protocol(protocol)
        
        if success and self.current_session:
            # Update session
            self.current_session.protocol = ProtocolState(
                protocol_name=protocol.name,
                start_time=datetime.now(),
                duration_minutes=protocol.expected_duration,
                frequencies=[layer.frequency for layer in protocol.layers],
                amplitudes={},
                phase=SessionPhase.ACTIVE
            )
            
            # Track gamma protocol
            if "gamma" in protocol.name.lower():
                self.safety_monitor.start_gamma_protocol()
        
        return success
    
    def run_closed_loop(self, duration_minutes: int = 20):
        """
        Run closed-loop system for specified duration
        
        Args:
            duration_minutes: Duration to run in minutes
        """
        if not self.running:
            print("[ERROR] No active session. Call start_session() first.")
            return
        
        print(f"[INFO] Running closed-loop for {duration_minutes} minutes...")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        protocol_deployed = False
        
        while time.time() < end_time and self.running:
            # 1. READ: Get sensor data
            sensor_data = self.read_sensors()
            
            if self.current_session:
                self.current_session.add_sensor_reading(sensor_data)
            
            # 2. CHECK SAFETY
            safety_events = self.safety_monitor.check_safety(sensor_data)
            
            # Handle safety events
            if self.safety_monitor.should_emergency_stop():
                print("[EMERGENCY] Safety limit exceeded - stopping")
                self.delivery_system.emergency_stop()
                self.stop_session()
                break
            
            if self.safety_monitor.should_reduce_amplitude():
                print("[WARN] Reducing amplitude due to safety event")
                self.delivery_system.adjust_intensity(0.7)
            
            # 3. SELECT: Choose protocol (if not already deployed)
            if not protocol_deployed:
                protocol = self.select_protocol(sensor_data)
                
                if protocol:
                    print(f"[INFO] Selected protocol: {protocol.name}")
                    
                    # 4. DELIVER: Deploy protocol
                    if self.deliver_protocol(protocol):
                        protocol_deployed = True
                        print(f"[OK] Protocol active: {protocol.name}")
                    else:
                        print("[ERROR] Failed to deploy protocol")
            
            # Wait for next update
            time.sleep(self.config.update_interval)
            
            # Progress indicator
            elapsed = (time.time() - start_time) / 60
            if int(elapsed) % 5 == 0 and elapsed > 0:
                print(f"[INFO] Progress: {elapsed:.0f}/{duration_minutes} minutes")
        
        print("[OK] Closed-loop session complete")
    
    def stop_session(self):
        """Stop current session"""
        if not self.running:
            return
        
        self.running = False
        
        # Stop delivery
        self.delivery_system.emergency_stop()
        
        # Finalize session
        if self.current_session:
            self.current_session.end_time = datetime.now()
            
            # Encrypt and save session data
            if self.config.session_log_enabled:
                encrypted_data = self.encryption.encrypt_session_data(self.current_session)
                # In production, would save to secure storage
            
            print(f"[OK] Session ended: {self.current_session.session_id}")
            print(f"    Duration: {self.current_session.duration_seconds():.0f} seconds")
            print(f"    Safety score: {self.safety_monitor.get_safety_score():.2f}")
        
        self.current_session = None
    
    def get_status(self) -> dict:
        """Get complete system status"""
        return {
            'tier': self.config.tier.value,
            'user_id': self.user_id,
            'running': self.running,
            'session': {
                'active': self.current_session is not None,
                'session_id': self.current_session.session_id if self.current_session else None,
                'duration_seconds': self.current_session.duration_seconds() if self.current_session else 0,
            } if self.running else None,
            'safety': self.safety_monitor.get_safety_report(),
            'delivery': self.delivery_system.get_status(),
        }


def create_system(tier: str = "lite", user_id: str = "default") -> NeuroSkinsSystem:
    """
    Factory function to create NeuroSkins system
    
    Args:
        tier: Product tier ('lite', 'pro', 'ascend')
        user_id: User identifier
        
    Returns:
        Initialized NeuroSkins system
    """
    # Parse tier
    tier_enum = ProductTier(tier.lower())
    
    # Create config
    config = SystemConfig.create_for_tier(tier_enum)
    
    # Create system
    system = NeuroSkinsSystem(config, user_id)
    
    return system
