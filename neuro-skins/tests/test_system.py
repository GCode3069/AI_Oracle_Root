"""
Unit tests for NeuroSkins system
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import numpy as np
from datetime import datetime

from src.core.system import create_system
from src.core.config import ProductTier, SystemConfig
from src.core.models import BrainState, SensorData, EEGReading
from src.protocols.library import get_protocol, GAMMA_40HZ
from src.sensors.eeg import EEGProcessor, EEGSimulator
from src.ai.classifier import BrainStateClassifier, FeatureVector


class TestSystemCreation:
    """Test system initialization"""
    
    def test_create_lite_system(self):
        """Test creating Lite tier system"""
        system = create_system(tier='lite')
        assert system.config.tier == ProductTier.LITE
        assert system.config.tier_config.price == 299
    
    def test_create_pro_system(self):
        """Test creating Pro tier system"""
        system = create_system(tier='pro')
        assert system.config.tier == ProductTier.PRO
        assert system.config.tier_config.price == 899
    
    def test_create_ascend_system(self):
        """Test creating Ascend tier system"""
        system = create_system(tier='ascend')
        assert system.config.tier == ProductTier.ASCEND
        assert system.config.tier_config.price == 2499


class TestProtocols:
    """Test protocol library"""
    
    def test_gamma_protocol_exists(self):
        """Test 40 Hz gamma protocol exists"""
        protocol = get_protocol('gamma_40hz')
        assert protocol is not None
        assert protocol.name == "40 Hz Gamma Boost"
        assert len(protocol.layers) > 0
    
    def test_protocol_frequencies(self):
        """Test protocol frequencies are correct"""
        gamma = get_protocol('gamma_40hz')
        assert gamma.layers[0].frequency == 40.0
    
    def test_tier_restrictions(self):
        """Test tier restrictions work"""
        gamma = get_protocol('gamma_40hz')
        assert gamma.required_tier == 'lite'
        
        kali_shiva = get_protocol('kali_shiva_sync')
        assert kali_shiva.required_tier == 'ascend'
        assert kali_shiva.age_restriction == 18


class TestEEGProcessing:
    """Test EEG signal processing"""
    
    def test_eeg_processor_init(self):
        """Test EEG processor initialization"""
        processor = EEGProcessor(sampling_rate=256)
        assert processor.sampling_rate == 256
        assert len(processor.channels) > 0
    
    def test_signal_preprocessing(self):
        """Test signal preprocessing"""
        processor = EEGProcessor()
        
        # Generate test signal
        t = np.linspace(0, 1, 256)
        signal = np.sin(2 * np.pi * 10 * t)  # 10 Hz signal
        
        # Preprocess
        filtered = processor.preprocess_signal(signal)
        assert len(filtered) == len(signal)
        assert not np.isnan(filtered).any()
    
    def test_band_power_computation(self):
        """Test band power computation"""
        processor = EEGProcessor(sampling_rate=256)
        
        # Generate 10 Hz signal (alpha band)
        t = np.linspace(0, 4, 1024)
        signal = np.sin(2 * np.pi * 10 * t)
        
        # Compute alpha power
        alpha_power = processor.compute_band_power(signal, (8, 13))
        assert alpha_power > 0
    
    def test_eeg_simulator(self):
        """Test EEG simulation"""
        simulator = EEGSimulator()
        
        # Generate epoch
        channels = simulator.generate_epoch(duration=1.0, state='relaxed')
        assert len(channels) > 0
        assert 'Fp1' in channels
        assert len(channels['Fp1']) > 0


class TestBrainStateClassification:
    """Test brain state classification"""
    
    def test_feature_extraction(self):
        """Test feature extraction from sensor data"""
        classifier = BrainStateClassifier()
        
        # Create mock EEG reading
        eeg = EEGReading(
            timestamp=datetime.now(),
            channels={},
            sampling_rate=256,
            delta_power=10.0,
            theta_power=15.0,
            alpha_power=30.0,
            beta_power=25.0,
            gamma_power=20.0,
            signal_quality=0.9
        )
        
        sensor_data = SensorData(timestamp=datetime.now(), eeg=eeg)
        
        # Extract features
        features = classifier.extract_features(sensor_data)
        assert isinstance(features, FeatureVector)
        assert 0 <= features.alpha_power <= 1.0
    
    def test_rule_based_classification(self):
        """Test rule-based classification"""
        classifier = BrainStateClassifier()
        
        # Create mock sensor data
        eeg = EEGReading(
            timestamp=datetime.now(),
            channels={},
            sampling_rate=256,
            delta_power=5.0,
            theta_power=10.0,
            alpha_power=40.0,  # High alpha = relaxed
            beta_power=15.0,
            gamma_power=10.0,
            signal_quality=0.9
        )
        
        sensor_data = SensorData(timestamp=datetime.now(), eeg=eeg)
        
        # Classify
        classification = classifier.classify(sensor_data)
        assert classification.predicted_state in BrainState
        assert 0 <= classification.confidence <= 1.0


class TestSafetyMonitor:
    """Test safety monitoring"""
    
    def test_heart_rate_limits(self):
        """Test heart rate safety limits"""
        from src.safety.monitor import SafetyMonitor
        from src.core.config import SafetyLimits
        
        limits = SafetyLimits()
        monitor = SafetyMonitor(limits)
        monitor.start_session()
        
        # Create mock sensor data with high HR
        from src.core.models import HRVReading
        hrv = HRVReading(
            timestamp=datetime.now(),
            heart_rate=200.0,  # Exceeds emergency limit
            rmssd=20.0,
            sdnn=40.0,
            pnn50=15.0,
            lf_hf_ratio=2.0
        )
        
        sensor_data = SensorData(timestamp=datetime.now(), hrv=hrv)
        
        # Check safety
        events = monitor.check_safety(sensor_data)
        assert len(events) > 0
        assert monitor.should_emergency_stop()
    
    def test_gamma_duration_limit(self):
        """Test gamma protocol duration limit"""
        from src.safety.monitor import SafetyMonitor
        from src.core.config import SafetyLimits
        
        limits = SafetyLimits(max_gamma_duration=1)  # 1 minute limit
        monitor = SafetyMonitor(limits)
        monitor.start_session()
        monitor.start_gamma_protocol()
        
        # Simulate time passing
        import time
        monitor.gamma_start = datetime.now()
        monitor.gamma_start = monitor.gamma_start.replace(
            minute=monitor.gamma_start.minute - 2  # 2 minutes ago
        )
        
        sensor_data = SensorData(timestamp=datetime.now())
        events = monitor.check_safety(sensor_data)
        
        # Should have critical event
        critical_events = [e for e in events if e.severity == 'critical']
        assert len(critical_events) > 0


class TestDeliverySystem:
    """Test frequency delivery"""
    
    def test_transducer_controller(self):
        """Test transducer controller"""
        from src.delivery.transducers import TransducerController
        from src.core.config import TransducerLocation
        
        controller = TransducerController()
        controller.connect_hardware()
        
        # Set frequency
        success = controller.set_frequency(
            TransducerLocation.CROWN,
            40.0,
            0.7
        )
        assert success
        
        # Check state
        state = controller.transducers[TransducerLocation.CROWN]
        assert state.frequency == 40.0
        assert state.amplitude == 0.7
        assert state.active
    
    def test_protocol_deployment(self):
        """Test protocol deployment"""
        from src.delivery.transducers import TransducerController
        
        controller = TransducerController()
        controller.connect_hardware()
        
        # Deploy gamma protocol
        success = controller.deploy_protocol(GAMMA_40HZ)
        assert success
        
        # Check active transducers
        active = controller.get_active_transducers()
        assert len(active) > 0


@pytest.mark.skip(reason="Requires real hardware connected")
def test_full_system_integration():
    """Integration test: full system workflow with real hardware"""
    # Create system
    system = create_system(tier='lite', user_id='test_user')
    
    # Verify age
    assert system.verify_user_age(25)
    
    # Initialize hardware (requires real devices)
    assert system.initialize_hardware()
    
    # Start session
    session_id = system.start_session()
    assert session_id is not None
    
    # Read sensors
    sensor_data = system.read_sensors()
    assert sensor_data.eeg is not None
    
    # Select protocol
    protocol = system.select_protocol(sensor_data)
    assert protocol is not None
    
    # Deliver protocol
    success = system.deliver_protocol(protocol)
    assert success
    
    # Check status
    status = system.get_status()
    assert status['running']
    assert status['session']['active']
    
    # Stop session
    system.stop_session()
    assert not system.running


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
