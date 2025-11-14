"""
AI Brain State Classifier
Uses edge AI to match brain states to protocols
"""

import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from ..core.models import (
    EEGReading, HRVReading, CortisolReading, 
    SkinConductanceReading, SensorData,
    BrainState, BrainStateClassification
)
from ..protocols.library import Protocol, get_protocol, get_protocols_for_tier


@dataclass
class FeatureVector:
    """Feature vector for ML classification"""
    # EEG band powers (normalized)
    delta_power: float
    theta_power: float
    alpha_power: float
    beta_power: float
    gamma_power: float
    
    # Ratios
    theta_beta_ratio: float
    alpha_theta_ratio: float
    
    # HRV features
    heart_rate: float
    rmssd: float
    lf_hf_ratio: float
    
    # Stress indicators
    cortisol_level: float
    skin_conductance: float
    
    def to_array(self) -> np.ndarray:
        """Convert to numpy array"""
        return np.array([
            self.delta_power,
            self.theta_power,
            self.alpha_power,
            self.beta_power,
            self.gamma_power,
            self.theta_beta_ratio,
            self.alpha_theta_ratio,
            self.heart_rate,
            self.rmssd,
            self.lf_hf_ratio,
            self.cortisol_level,
            self.skin_conductance,
        ])


class BrainStateClassifier:
    """Classifies brain states using ML"""
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize classifier
        
        Args:
            model_path: Path to TensorFlow Lite model (optional)
        """
        self.model_path = model_path
        self.model = None
        
        # Feature normalization parameters
        self.feature_means = None
        self.feature_stds = None
        
        # Load model if path provided
        if model_path:
            self._load_model(model_path)
        else:
            # Use rule-based classifier
            self.use_rules = True
    
    def _load_model(self, model_path: str):
        """Load TensorFlow Lite model"""
        try:
            import tensorflow as tf
            self.model = tf.lite.Interpreter(model_path=model_path)
            self.model.allocate_tensors()
            self.use_rules = False
        except Exception as e:
            print(f"[WARN] Could not load model: {e}. Using rule-based classifier.")
            self.use_rules = True
    
    def extract_features(self, sensor_data: SensorData) -> FeatureVector:
        """
        Extract features from sensor data
        
        Args:
            sensor_data: Combined sensor readings
            
        Returns:
            Feature vector
        """
        # EEG features
        if sensor_data.eeg:
            eeg = sensor_data.eeg
            total_power = (eeg.delta_power + eeg.theta_power + 
                          eeg.alpha_power + eeg.beta_power + eeg.gamma_power)
            
            # Normalize band powers
            delta = eeg.delta_power / total_power if total_power > 0 else 0
            theta = eeg.theta_power / total_power if total_power > 0 else 0
            alpha = eeg.alpha_power / total_power if total_power > 0 else 0
            beta = eeg.beta_power / total_power if total_power > 0 else 0
            gamma = eeg.gamma_power / total_power if total_power > 0 else 0
            
            # Compute ratios
            theta_beta = theta / beta if beta > 0 else 1.0
            alpha_theta = alpha / theta if theta > 0 else 1.0
        else:
            delta = theta = alpha = beta = gamma = 0.0
            theta_beta = alpha_theta = 1.0
        
        # HRV features
        if sensor_data.hrv:
            hr = sensor_data.hrv.heart_rate
            rmssd = sensor_data.hrv.rmssd
            lf_hf = sensor_data.hrv.lf_hf_ratio
        else:
            hr = 70.0  # Default
            rmssd = 30.0
            lf_hf = 1.0
        
        # Cortisol
        if sensor_data.cortisol:
            cortisol = sensor_data.cortisol.level_ng_ml / 1000.0  # Normalize
        else:
            cortisol = 0.2
        
        # Skin conductance
        if sensor_data.skin_conductance:
            gsr = sensor_data.skin_conductance.conductance_microsiemens / 20.0  # Normalize
        else:
            gsr = 0.25
        
        return FeatureVector(
            delta_power=delta,
            theta_power=theta,
            alpha_power=alpha,
            beta_power=beta,
            gamma_power=gamma,
            theta_beta_ratio=theta_beta,
            alpha_theta_ratio=alpha_theta,
            heart_rate=hr / 200.0,  # Normalize
            rmssd=rmssd / 100.0,
            lf_hf_ratio=lf_hf / 5.0,
            cortisol_level=cortisol,
            skin_conductance=gsr,
        )
    
    def classify_rule_based(self, features: FeatureVector) -> BrainStateClassification:
        """
        Rule-based classification (fallback)
        
        Args:
            features: Feature vector
            
        Returns:
            Brain state classification
        """
        scores = {}
        
        # Morning fog: high delta, low gamma, moderate cortisol
        scores[BrainState.MORNING_FOG] = (
            features.delta_power * 2.0 +
            (1.0 - features.gamma_power) * 1.5 +
            features.cortisol_level * 0.5
        )
        
        # Anxiety spike: high beta, high HR, high cortisol, high GSR
        scores[BrainState.ANXIETY_SPIKE] = (
            features.beta_power * 2.0 +
            (features.heart_rate - 0.35) * 3.0 +  # >70 bpm
            features.cortisol_level * 2.0 +
            features.skin_conductance * 1.5 +
            features.lf_hf_ratio * 1.0
        )
        
        # Workout mode: high beta, high HR, low alpha
        scores[BrainState.WORKOUT_MODE] = (
            features.beta_power * 2.0 +
            (features.heart_rate - 0.5) * 3.0 +  # >100 bpm
            (1.0 - features.alpha_power) * 1.5
        )
        
        # Relaxed: high alpha, low beta, low HR
        scores[BrainState.RELAXED] = (
            features.alpha_power * 3.0 +
            (1.0 - features.beta_power) * 1.5 +
            (0.35 - features.heart_rate) * 2.0 +  # <70 bpm
            (1.0 - features.lf_hf_ratio / 5.0) * 1.0
        )
        
        # Focused: high gamma, high beta, moderate HR
        scores[BrainState.FOCUSED] = (
            features.gamma_power * 2.5 +
            features.beta_power * 2.0 +
            abs(features.heart_rate - 0.4) * (-2.0) +  # Around 80 bpm
            (1.0 - features.cortisol_level) * 0.5
        )
        
        # Stressed: high beta, high cortisol, high LF/HF
        scores[BrainState.STRESSED] = (
            features.beta_power * 2.0 +
            features.cortisol_level * 2.5 +
            features.lf_hf_ratio * 2.0 +
            (1.0 - features.rmssd) * 1.5
        )
        
        # Sex mode: high alpha, high theta, elevated HR, high GSR
        scores[BrainState.SEX_MODE] = (
            features.alpha_power * 1.5 +
            features.theta_power * 2.0 +
            (features.heart_rate - 0.45) * 2.0 +  # >90 bpm
            features.skin_conductance * 2.5
        )
        
        # Meditation: high theta, high alpha, low beta, low HR
        scores[BrainState.MEDITATION] = (
            features.theta_power * 3.0 +
            features.alpha_power * 2.0 +
            (1.0 - features.beta_power) * 2.0 +
            (0.3 - features.heart_rate) * 2.0  # <60 bpm
        )
        
        # Normalize scores to probabilities
        total = sum(max(0, score) for score in scores.values())
        if total == 0:
            probabilities = {state: 1.0/len(scores) for state in scores}
        else:
            probabilities = {state: max(0, score)/total for state, score in scores.items()}
        
        # Get top prediction
        predicted_state = max(probabilities, key=probabilities.get)
        confidence = probabilities[predicted_state]
        
        # Feature importance (simplified)
        dominant_features = {
            'gamma': features.gamma_power,
            'beta': features.beta_power,
            'alpha': features.alpha_power,
            'theta': features.theta_power,
            'heart_rate': features.heart_rate,
            'cortisol': features.cortisol_level,
        }
        
        return BrainStateClassification(
            timestamp=datetime.now(),
            predicted_state=predicted_state,
            confidence=confidence,
            probabilities=probabilities,
            dominant_features=dominant_features
        )
    
    def classify(self, sensor_data: SensorData) -> BrainStateClassification:
        """
        Classify brain state from sensor data
        
        Args:
            sensor_data: Combined sensor readings
            
        Returns:
            Brain state classification
        """
        features = self.extract_features(sensor_data)
        
        if self.use_rules or self.model is None:
            return self.classify_rule_based(features)
        else:
            # Use TensorFlow Lite model
            return self._classify_with_model(features)
    
    def _classify_with_model(self, features: FeatureVector) -> BrainStateClassification:
        """Classify using TensorFlow Lite model"""
        # Get input/output tensors
        input_details = self.model.get_input_details()
        output_details = self.model.get_output_details()
        
        # Prepare input
        input_data = features.to_array().reshape(1, -1).astype(np.float32)
        
        # Run inference
        self.model.set_tensor(input_details[0]['index'], input_data)
        self.model.invoke()
        
        # Get output
        output_data = self.model.get_tensor(output_details[0]['index'])[0]
        
        # Map to brain states
        state_mapping = [
            BrainState.MORNING_FOG,
            BrainState.ANXIETY_SPIKE,
            BrainState.WORKOUT_MODE,
            BrainState.RELAXED,
            BrainState.FOCUSED,
            BrainState.STRESSED,
            BrainState.SEX_MODE,
            BrainState.MEDITATION,
        ]
        
        probabilities = {
            state: float(prob) 
            for state, prob in zip(state_mapping, output_data)
        }
        
        predicted_state = max(probabilities, key=probabilities.get)
        confidence = probabilities[predicted_state]
        
        return BrainStateClassification(
            timestamp=datetime.now(),
            predicted_state=predicted_state,
            confidence=confidence,
            probabilities=probabilities,
            dominant_features={}  # Would need SHAP or similar for model interpretation
        )


class ProtocolSelector:
    """Selects optimal protocol based on brain state"""
    
    def __init__(self, tier: str = "lite"):
        """
        Initialize protocol selector
        
        Args:
            tier: Product tier
        """
        self.tier = tier
        self.available_protocols = get_protocols_for_tier(tier)
        
        # State to protocol mapping
        self.state_protocol_map = {
            BrainState.MORNING_FOG: ["gamma_40hz"],
            BrainState.ANXIETY_SPIKE: ["anxiety_relief", "vagus_overclock"],
            BrainState.WORKOUT_MODE: ["workout_prime", "berberine_alert"],
            BrainState.RELAXED: ["trauma_delete"],
            BrainState.FOCUSED: ["gamma_40hz"],
            BrainState.STRESSED: ["anxiety_relief", "vagus_overclock"],
            BrainState.SEX_MODE: ["kali_shiva_sync"],
            BrainState.MEDITATION: ["float_tank_lock", "ego_death_layer7"],
            BrainState.SLEEP_PREP: ["trauma_delete"],
        }
    
    def select_protocol(self, 
                       classification: BrainStateClassification,
                       user_days: int = 0) -> Optional[Protocol]:
        """
        Select optimal protocol for brain state
        
        Args:
            classification: Brain state classification
            user_days: Days since user started (for Layer 7 restriction)
            
        Returns:
            Selected protocol or None
        """
        state = classification.predicted_state
        
        # Get candidate protocols
        candidate_names = self.state_protocol_map.get(state, [])
        
        # Filter by tier availability
        available_names = [p.name.lower().replace(" ", "_").replace("/", "_") 
                          for p in self.available_protocols]
        
        candidates = []
        for name in candidate_names:
            protocol = get_protocol(name)
            if protocol and name in available_names:
                # Check day restriction for ego death
                if name == "ego_death_layer7" and user_days < 23:
                    continue
                candidates.append(protocol)
        
        if not candidates:
            # Fallback to gamma boost
            return get_protocol("gamma_40hz")
        
        # Select first candidate (could be more sophisticated)
        return candidates[0]
    
    def get_recommendations(self, 
                           classification: BrainStateClassification,
                           n: int = 3) -> List[Tuple[Protocol, float]]:
        """
        Get top N protocol recommendations with confidence scores
        
        Args:
            classification: Brain state classification
            n: Number of recommendations
            
        Returns:
            List of (protocol, score) tuples
        """
        recommendations = []
        
        # Score each available protocol
        for protocol in self.available_protocols:
            score = 0.0
            
            # Match against classification probabilities
            for state, prob in classification.probabilities.items():
                if state in self.state_protocol_map:
                    protocol_names = self.state_protocol_map[state]
                    protocol_key = protocol.name.lower().replace(" ", "_").replace("/", "_")
                    if protocol_key in protocol_names:
                        score += prob
            
            if score > 0:
                recommendations.append((protocol, score))
        
        # Sort by score
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        return recommendations[:n]
