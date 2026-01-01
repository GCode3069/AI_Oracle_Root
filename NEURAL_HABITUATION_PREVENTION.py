"""
Advanced Content Optimization System - Neural Habituation Prevention
Prevents neural response decay through content variation and novelty protocols
"""

import json
import os
from typing import Dict, List, Optional, Set
from datetime import datetime, timedelta
from collections import defaultdict


class NeuralHabituationPrevention:
    """
    Prevents neural habituation through content variation.
    Monitors neural response decay curves and implements novelty protocols.
    """
    
    def __init__(self, history_file: str = "content_history.json"):
        self.history_file = history_file
        self.content_history = self._load_history()
        self.habituation_threshold = 0.3  # 30% similarity threshold
        self.decay_window_days = 7  # Days to consider for decay analysis
    
    def _load_history(self) -> Dict:
        """Load content history."""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {
                    "content_log": [],
                    "topic_frequency": {},
                    "style_frequency": {},
                    "neural_patterns": []
                }
        return {
            "content_log": [],
            "topic_frequency": {},
            "style_frequency": {},
            "neural_patterns": []
        }
    
    def _save_history(self):
        """Save content history."""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.content_history, f, indent=2, ensure_ascii=False)
    
    def check_habituation_risk(self, topic: str, content_type: str,
                               presentation_style: str, neural_settings: Dict) -> Dict:
        """
        Check if content risks neural habituation.
        Monitors neural response decay curves.
        Implements optimal novelty intervals.
        Prevents receptor downregulation through content variation.
        """
        # Calculate similarity to recent content
        similarity_score = self._calculate_similarity(
            topic, content_type, presentation_style, neural_settings
        )
        
        # Check topic frequency
        topic_frequency = self._get_topic_frequency(topic)
        
        # Check style frequency
        style_frequency = self._get_style_frequency(presentation_style)
        
        # Check neural pattern frequency
        neural_pattern_frequency = self._get_neural_pattern_frequency(neural_settings)
        
        # Determine habituation risk
        risk_level = self._assess_habituation_risk(
            similarity_score, topic_frequency, style_frequency, neural_pattern_frequency
        )
        
        # Generate recommendations
        recommendations = self._generate_habituation_recommendations(
            risk_level, topic_frequency, style_frequency, neural_pattern_frequency
        )
        
        return {
            "habituation_risk": risk_level,
            "similarity_score": similarity_score,
            "topic_frequency": topic_frequency,
            "style_frequency": style_frequency,
            "neural_pattern_frequency": neural_pattern_frequency,
            "recommendations": recommendations,
            "novelty_protocols": self._get_novelty_protocols(risk_level)
        }
    
    def _calculate_similarity(self, topic: str, content_type: str,
                             presentation_style: str, neural_settings: Dict) -> float:
        """Calculate similarity to recent content."""
        if not self.content_history["content_log"]:
            return 0.0
        
        # Get recent content (last 7 days)
        cutoff_date = datetime.now() - timedelta(days=self.decay_window_days)
        recent_content = [
            entry for entry in self.content_history["content_log"]
            if datetime.fromisoformat(entry.get("timestamp", "2000-01-01")) >= cutoff_date
        ]
        
        if not recent_content:
            return 0.0
        
        similarities = []
        topic_lower = topic.lower()
        
        for entry in recent_content:
            entry_topic = entry.get("topic", "").lower()
            entry_type = entry.get("content_type", "")
            entry_style = entry.get("presentation_style", "")
            entry_neural = entry.get("neural_settings", {})
            
            similarity = 0.0
            
            # Topic similarity
            topic_words = set(topic_lower.split())
            entry_words = set(entry_topic.split())
            if topic_words and entry_words:
                topic_overlap = len(topic_words & entry_words) / len(topic_words | entry_words)
                similarity += topic_overlap * 0.4
            
            # Content type similarity
            if content_type == entry_type:
                similarity += 0.2
            
            # Style similarity
            if presentation_style == entry_style:
                similarity += 0.2
            
            # Neural settings similarity
            gamma_match = (
                neural_settings.get("gamma_spikes", []) == entry_neural.get("gamma_spikes", [])
            )
            limbic_diff = abs(
                neural_settings.get("limbic_engagement", 0) - entry_neural.get("limbic_engagement", 0)
            )
            if gamma_match and limbic_diff < 0.1:
                similarity += 0.2
            
            similarities.append(similarity)
        
        # Return maximum similarity (worst case)
        return max(similarities) if similarities else 0.0
    
    def _get_topic_frequency(self, topic: str) -> Dict:
        """Get frequency of topic in recent content."""
        topic_lower = topic.lower()
        topic_keywords = set(topic_lower.split())
        
        # Count occurrences in recent content
        cutoff_date = datetime.now() - timedelta(days=self.decay_window_days)
        recent_content = [
            entry for entry in self.content_history["content_log"]
            if datetime.fromisoformat(entry.get("timestamp", "2000-01-01")) >= cutoff_date
        ]
        
        matches = 0
        for entry in recent_content:
            entry_topic = entry.get("topic", "").lower()
            entry_keywords = set(entry_topic.split())
            if topic_keywords & entry_keywords:  # Any overlap
                matches += 1
        
        frequency = matches / len(recent_content) if recent_content else 0.0
        
        return {
            "recent_occurrences": matches,
            "frequency": frequency,
            "risk_level": "high" if frequency > 0.3 else "medium" if frequency > 0.15 else "low"
        }
    
    def _get_style_frequency(self, style: str) -> Dict:
        """Get frequency of presentation style."""
        cutoff_date = datetime.now() - timedelta(days=self.decay_window_days)
        recent_content = [
            entry for entry in self.content_history["content_log"]
            if datetime.fromisoformat(entry.get("timestamp", "2000-01-01")) >= cutoff_date
        ]
        
        style_matches = sum(1 for entry in recent_content if entry.get("presentation_style") == style)
        frequency = style_matches / len(recent_content) if recent_content else 0.0
        
        return {
            "recent_occurrences": style_matches,
            "frequency": frequency,
            "risk_level": "high" if frequency > 0.4 else "medium" if frequency > 0.2 else "low"
        }
    
    def _get_neural_pattern_frequency(self, neural_settings: Dict) -> Dict:
        """Get frequency of neural pattern."""
        cutoff_date = datetime.now() - timedelta(days=self.decay_window_days)
        recent_content = [
            entry for entry in self.content_history["content_log"]
            if datetime.fromisoformat(entry.get("timestamp", "2000-01-01")) >= cutoff_date
        ]
        
        gamma_spikes = neural_settings.get("gamma_spikes", [])
        limbic_engagement = neural_settings.get("limbic_engagement", 0)
        
        matches = 0
        for entry in recent_content:
            entry_neural = entry.get("neural_settings", {})
            entry_gamma = entry_neural.get("gamma_spikes", [])
            entry_limbic = entry_neural.get("limbic_engagement", 0)
            
            if (gamma_spikes == entry_gamma and 
                abs(limbic_engagement - entry_limbic) < 0.1):
                matches += 1
        
        frequency = matches / len(recent_content) if recent_content else 0.0
        
        return {
            "recent_occurrences": matches,
            "frequency": frequency,
            "risk_level": "high" if frequency > 0.3 else "medium" if frequency > 0.15 else "low"
        }
    
    def _assess_habituation_risk(self, similarity: float, topic_freq: Dict,
                                style_freq: Dict, neural_freq: Dict) -> str:
        """Assess overall habituation risk level."""
        risk_factors = []
        
        if similarity > self.habituation_threshold:
            risk_factors.append("high_similarity")
        
        if topic_freq.get("risk_level") == "high":
            risk_factors.append("topic_overuse")
        
        if style_freq.get("risk_level") == "high":
            risk_factors.append("style_overuse")
        
        if neural_freq.get("risk_level") == "high":
            risk_factors.append("neural_pattern_overuse")
        
        if len(risk_factors) >= 3:
            return "high"
        elif len(risk_factors) >= 2:
            return "medium"
        elif len(risk_factors) >= 1:
            return "low"
        else:
            return "minimal"
    
    def _generate_habituation_recommendations(self, risk_level: str,
                                             topic_freq: Dict, style_freq: Dict,
                                             neural_freq: Dict) -> List[str]:
        """Generate recommendations to prevent habituation."""
        recommendations = []
        
        if risk_level == "high":
            recommendations.append(
                "HIGH RISK: Significant habituation risk detected. "
                "Consider changing topic, presentation style, or neural settings."
            )
        
        if topic_freq.get("risk_level") == "high":
            recommendations.append(
                f"Topic overused ({topic_freq['frequency']:.0%} frequency). "
                "Select a different topic or wait before reusing."
            )
        
        if style_freq.get("risk_level") == "high":
            recommendations.append(
                f"Presentation style overused ({style_freq['frequency']:.0%} frequency). "
                "Try a different presentation style."
            )
        
        if neural_freq.get("risk_level") == "high":
            recommendations.append(
                f"Neural pattern overused ({neural_freq['frequency']:.0%} frequency). "
                "Vary gamma spike timing or limbic engagement levels."
            )
        
        if not recommendations:
            recommendations.append(
                "Low habituation risk. Content variation is adequate."
            )
        
        return recommendations
    
    def _get_novelty_protocols(self, risk_level: str) -> Dict:
        """Get novelty protocols based on risk level."""
        protocols = {
            "minimal": {
                "action": "proceed",
                "variation_required": False,
                "novelty_boost": 0.0
            },
            "low": {
                "action": "proceed_with_caution",
                "variation_required": False,
                "novelty_boost": 0.1
            },
            "medium": {
                "action": "modify_content",
                "variation_required": True,
                "novelty_boost": 0.2,
                "suggestions": [
                    "Change presentation style",
                    "Adjust neural settings",
                    "Add novel elements"
                ]
            },
            "high": {
                "action": "significant_modification_required",
                "variation_required": True,
                "novelty_boost": 0.3,
                "suggestions": [
                    "Select different topic",
                    "Use different presentation style",
                    "Modify neural pattern significantly",
                    "Wait before publishing similar content"
                ]
            }
        }
        return protocols.get(risk_level, protocols["minimal"])
    
    def record_content(self, topic: str, content_type: str, presentation_style: str,
                      neural_settings: Dict):
        """Record content in history for habituation tracking."""
        entry = {
            "topic": topic,
            "content_type": content_type,
            "presentation_style": presentation_style,
            "neural_settings": neural_settings,
            "timestamp": datetime.now().isoformat()
        }
        
        self.content_history["content_log"].append(entry)
        
        # Update frequency tracking
        topic_key = topic.lower()
        self.content_history["topic_frequency"][topic_key] = \
            self.content_history["topic_frequency"].get(topic_key, 0) + 1
        
        self.content_history["style_frequency"][presentation_style] = \
            self.content_history["style_frequency"].get(presentation_style, 0) + 1
        
        # Keep only recent history (last 100 entries)
        if len(self.content_history["content_log"]) > 100:
            self.content_history["content_log"] = self.content_history["content_log"][-100:]
        
        self._save_history()


if __name__ == "__main__":
    # Example usage
    prevention = NeuralHabituationPrevention()
    
    # Check habituation risk
    risk_assessment = prevention.check_habituation_risk(
        topic="Education System Analysis",
        content_type="platform_features",
        presentation_style="charismatic_engagement",
        neural_settings={
            "gamma_spikes": [8, 12],
            "limbic_engagement": 0.82,
            "prefrontal_activation": "high"
        }
    )
    
    print("Habituation Risk Assessment:")
    print(json.dumps(risk_assessment, indent=2))
    
    # Record content
    prevention.record_content(
        topic="Education System Analysis",
        content_type="platform_features",
        presentation_style="charismatic_engagement",
        neural_settings={
            "gamma_spikes": [8, 12],
            "limbic_engagement": 0.82
        }
    )
