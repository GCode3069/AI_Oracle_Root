"""
NEURAL_HABITUATION_PREVENTION.py

Purpose: Prevents neural response decay through optimal novelty intervals and content variation
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict

class NeuralHabituationPrevention:
    """
    Prevents neural response decay through monitoring and optimization
    """

    def __init__(self):
        self.topic_exposure_history = defaultdict(list)
        self.neural_decay_curves = {}
        self.novelty_intervals = {}
        self.variation_patterns = {}

    def monitor_topic_exposure(self, topic: str, exposure_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Monitor topic exposure and neural response decay
        """
        current_time = datetime.now()

        exposure_entry = {
            "timestamp": current_time.isoformat(),
            "engagement_rate": exposure_data.get("engagement_rate", 0.0),
            "views": exposure_data.get("views", 0),
            "platform": exposure_data.get("platform", "unknown"),
            "content_variation": exposure_data.get("variation_score", 1.0)
        }

        self.topic_exposure_history[topic].append(exposure_entry)

        # Analyze decay pattern
        decay_analysis = self._analyze_decay_pattern(topic)

        # Update prevention strategies
        prevention_update = self._update_prevention_strategy(topic, decay_analysis)

        return {
            "topic": topic,
            "exposure_logged": True,
            "decay_analysis": decay_analysis,
            "prevention_strategy": prevention_update,
            "next_safe_exposure": self._calculate_next_safe_exposure(topic)
        }

    def filter_habituated_topics(self, candidate_topics: List[str]) -> List[str]:
        """
        Filter out topics that have been over-exposed recently
        """
        filtered_topics = []

        for topic in candidate_topics:
            habituation_status = self._assess_habituation_risk(topic)

            if habituation_status["risk_level"] == "low":
                filtered_topics.append(topic)
            elif habituation_status["risk_level"] == "medium":
                # Allow with variation requirement
                if self._can_apply_variation(topic):
                    filtered_topics.append(topic)

        return filtered_topics

    def get_freshness_score(self, topic: str) -> float:
        """
        Calculate freshness score (higher = more novel)
        """
        if topic not in self.topic_exposure_history:
            return 1.0  # Completely fresh

        exposures = self.topic_exposure_history[topic]
        if not exposures:
            return 1.0

        # Calculate recency-weighted freshness
        current_time = datetime.now()
        total_freshness = 0.0
        total_weight = 0.0

        for exposure in exposures[-10:]:  # Last 10 exposures
            exposure_time = datetime.fromisoformat(exposure["timestamp"])
            days_since = (current_time - exposure_time).days

            # Exponential decay of freshness
            recency_weight = max(0, 1.0 - (days_since / 30.0))  # 30-day decay
            engagement_weight = exposure.get("engagement_rate", 0.05) / 0.05  # Normalize to baseline

            weight = recency_weight * engagement_weight
            total_freshness += weight
            total_weight += 1.0

        if total_weight == 0:
            return 1.0

        average_freshness = total_freshness / total_weight
        return min(average_freshness, 1.0)

    def generate_novelty_intervals(self, topic: str) -> Dict[str, Any]:
        """
        Generate optimal novelty intervals for topic rotation
        """
        exposure_history = self.topic_exposure_history.get(topic, [])

        if len(exposure_history) < 3:
            return {
                "recommended_interval": 7,  # Default 7 days
                "confidence": "low",
                "reason": "insufficient_data"
            }

        # Analyze engagement decay over time
        decay_rate = self._calculate_decay_rate(exposure_history)

        # Calculate optimal interval based on decay
        if decay_rate > 0.5:  # Fast decay
            optimal_interval = 14  # 2 weeks
        elif decay_rate > 0.3:  # Moderate decay
            optimal_interval = 10  # 10 days
        else:  # Slow decay
            optimal_interval = 7   # 1 week

        # Adjust for content variation
        variation_factor = self._calculate_variation_factor(topic)
        optimal_interval = int(optimal_interval * (1 - variation_factor * 0.3))

        self.novelty_intervals[topic] = {
            "interval_days": optimal_interval,
            "decay_rate": decay_rate,
            "variation_factor": variation_factor,
            "last_updated": datetime.now().isoformat()
        }

        return {
            "topic": topic,
            "recommended_interval": optimal_interval,
            "decay_rate": decay_rate,
            "variation_factor": variation_factor,
            "next_available": self._calculate_next_available(topic, optimal_interval)
        }

    def implement_content_variation(self, topic: str, base_content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Implement content variation to prevent habituation
        """
        variation_strategies = {
            "structural_variation": self._apply_structural_variation,
            "narrative_variation": self._apply_narrative_variation,
            "presentation_variation": self._apply_presentation_variation,
            "contextual_variation": self._apply_contextual_variation
        }

        # Determine variation needs
        habituation_risk = self._assess_habituation_risk(topic)
        variation_intensity = self._calculate_variation_intensity(habituation_risk)

        # Apply variations
        varied_content = base_content.copy()
        applied_variations = []

        for strategy_name, strategy_func in variation_strategies.items():
            if variation_intensity > 0.3:  # Apply variation if needed
                varied_content = strategy_func(varied_content, variation_intensity)
                applied_variations.append(strategy_name)

        # Track variation
        variation_score = len(applied_variations) / len(variation_strategies)

        return {
            "original_content": base_content,
            "varied_content": varied_content,
            "applied_variations": applied_variations,
            "variation_score": variation_score,
            "habituation_prevention": variation_intensity > 0.5
        }

    def get_habituation_status_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive habituation status report
        """
        report = {
            "total_topics_tracked": len(self.topic_exposure_history),
            "high_risk_topics": [],
            "fresh_topics": [],
            "decay_analysis": {},
            "prevention_effectiveness": {}
        }

        for topic in self.topic_exposure_history.keys():
            risk_assessment = self._assess_habituation_risk(topic)

            if risk_assessment["risk_level"] == "high":
                report["high_risk_topics"].append({
                    "topic": topic,
                    "risk_score": risk_assessment["risk_score"],
                    "last_exposed": risk_assessment["days_since_last_exposure"]
                })
            elif risk_assessment["risk_level"] == "low":
                report["fresh_topics"].append(topic)

            report["decay_analysis"][topic] = self._analyze_decay_pattern(topic)

        report["prevention_effectiveness"] = self._calculate_prevention_effectiveness()

        return report

    def _analyze_decay_pattern(self, topic: str) -> Dict[str, Any]:
        """
        Analyze neural decay pattern for a topic
        """
        exposures = self.topic_exposure_history.get(topic, [])

        if len(exposures) < 2:
            return {"decay_rate": 0.0, "pattern": "insufficient_data"}

        # Calculate engagement decay over time
        engagement_values = [exp["engagement_rate"] for exp in exposures[-10:]]  # Last 10

        if len(engagement_values) < 2:
            return {"decay_rate": 0.0, "pattern": "minimal_exposure"}

        # Simple linear decay calculation
        initial_engagement = engagement_values[0]
        final_engagement = engagement_values[-1]
        decay_rate = max(0, (initial_engagement - final_engagement) / initial_engagement)

        # Classify decay pattern
        if decay_rate > 0.5:
            pattern = "rapid_decay"
        elif decay_rate > 0.2:
            pattern = "moderate_decay"
        else:
            pattern = "slow_decay"

        return {
            "decay_rate": decay_rate,
            "pattern": pattern,
            "initial_engagement": initial_engagement,
            "final_engagement": final_engagement,
            "exposure_count": len(engagement_values)
        }

    def _update_prevention_strategy(self, topic: str, decay_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update prevention strategy based on decay analysis
        """
        strategy = {
            "topic": topic,
            "current_strategy": "standard_rotation",
            "adjustments_needed": []
        }

        decay_rate = decay_analysis.get("decay_rate", 0.0)

        if decay_rate > 0.5:
            strategy["current_strategy"] = "aggressive_variation"
            strategy["adjustments_needed"].extend([
                "increase_novelty_intervals",
                "apply_maximum_variation",
                "reduce_exposure_frequency"
            ])
        elif decay_rate > 0.2:
            strategy["current_strategy"] = "moderate_prevention"
            strategy["adjustments_needed"].extend([
                "apply_structural_variation",
                "monitor_engagement_closely"
            ])
        else:
            strategy["current_strategy"] = "maintenance_mode"
            strategy["adjustments_needed"].append("continue_current_approach")

        return strategy

    def _calculate_next_safe_exposure(self, topic: str) -> str:
        """
        Calculate next safe exposure time
        """
        interval_info = self.novelty_intervals.get(topic)
        if not interval_info:
            return "7 days (default)"

        interval_days = interval_info["interval_days"]
        last_exposure = self._get_last_exposure_time(topic)

        if last_exposure:
            next_exposure = last_exposure + timedelta(days=interval_days)
            return next_exposure.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return f"{interval_days} days from now"

    def _assess_habituation_risk(self, topic: str) -> Dict[str, Any]:
        """
        Assess habituation risk for a topic
        """
        exposures = self.topic_exposure_history.get(topic, [])

        if not exposures:
            return {"risk_level": "low", "risk_score": 0.0, "days_since_last_exposure": None}

        last_exposure = exposures[-1]
        last_exposure_time = datetime.fromisoformat(last_exposure["timestamp"])
        days_since = (datetime.now() - last_exposure_time).days

        # Calculate risk based on recency and engagement decay
        recency_risk = min(days_since / 30.0, 1.0)  # Lower risk if more recent
        decay_analysis = self._analyze_decay_pattern(topic)
        decay_risk = decay_analysis.get("decay_rate", 0.0)

        total_risk = (recency_risk * 0.4) + (decay_risk * 0.6)

        if total_risk > 0.7:
            risk_level = "high"
        elif total_risk > 0.4:
            risk_level = "medium"
        else:
            risk_level = "low"

        return {
            "risk_level": risk_level,
            "risk_score": total_risk,
            "days_since_last_exposure": days_since,
            "decay_contribution": decay_risk,
            "recency_contribution": recency_risk
        }

    def _can_apply_variation(self, topic: str) -> bool:
        """
        Check if variation can be applied to reduce habituation
        """
        # For now, assume variation is always possible
        # In practice, this would check content flexibility
        return True

    def _calculate_decay_rate(self, exposures: List[Dict[str, Any]]) -> float:
        """
        Calculate decay rate from exposure history
        """
        if len(exposures) < 2:
            return 0.0

        # Use engagement rate decay as proxy for neural decay
        engagement_rates = [exp["engagement_rate"] for exp in exposures]

        # Simple exponential decay model
        initial = engagement_rates[0]
        final = engagement_rates[-1]

        if initial == 0:
            return 0.0

        decay = (initial - final) / initial
        return max(0.0, decay)

    def _calculate_variation_factor(self, topic: str) -> float:
        """
        Calculate how much variation has been applied
        """
        # Simplified - in practice would analyze content differences
        exposures = self.topic_exposure_history.get(topic, [])
        variation_scores = [exp.get("content_variation", 1.0) for exp in exposures]

        if not variation_scores:
            return 0.0

        return sum(variation_scores) / len(variation_scores)

    def _calculate_next_available(self, topic: str, interval: int) -> str:
        """
        Calculate next available time for topic
        """
        last_time = self._get_last_exposure_time(topic)
        if last_time:
            next_time = last_time + timedelta(days=interval)
            return next_time.strftime("%Y-%m-%d")
        else:
            return "immediately"

    def _get_last_exposure_time(self, topic: str) -> Optional[datetime]:
        """
        Get last exposure time for topic
        """
        exposures = self.topic_exposure_history.get(topic, [])
        if exposures:
            return datetime.fromisoformat(exposures[-1]["timestamp"])
        return None

    def _calculate_variation_intensity(self, habituation_risk: Dict[str, Any]) -> float:
        """
        Calculate how much variation is needed
        """
        risk_score = habituation_risk.get("risk_score", 0.0)
        return min(risk_score * 1.5, 1.0)  # Scale up to maximum variation

    def _apply_structural_variation(self, content: Dict[str, Any], intensity: float) -> Dict[str, Any]:
        """Apply structural variation to content"""
        varied = content.copy()
        if intensity > 0.5:
            varied["structure"] = "non_linear"  # Change from default
        return varied

    def _apply_narrative_variation(self, content: Dict[str, Any], intensity: float) -> Dict[str, Any]:
        """Apply narrative variation to content"""
        varied = content.copy()
        if intensity > 0.4:
            varied["narrative_style"] = "story_based"  # Add storytelling elements
        return varied

    def _apply_presentation_variation(self, content: Dict[str, Any], intensity: float) -> Dict[str, Any]:
        """Apply presentation variation to content"""
        varied = content.copy()
        if intensity > 0.3:
            varied["presentation_style"] = "dynamic"  # More energetic delivery
        return varied

    def _apply_contextual_variation(self, content: Dict[str, Any], intensity: float) -> Dict[str, Any]:
        """Apply contextual variation to content"""
        varied = content.copy()
        if intensity > 0.6:
            varied["context"] = "timely_relevant"  # Tie to current events
        return varied

    def _calculate_prevention_effectiveness(self) -> Dict[str, float]:
        """
        Calculate overall prevention effectiveness
        """
        if not self.topic_exposure_history:
            return {"overall_effectiveness": 0.0}

        total_topics = len(self.topic_exposure_history)
        high_risk_topics = 0

        for topic in self.topic_exposure_history.keys():
            risk = self._assess_habituation_risk(topic)
            if risk["risk_level"] == "high":
                high_risk_topics += 1

        effectiveness = 1.0 - (high_risk_topics / total_topics)
        return {"overall_effectiveness": effectiveness, "high_risk_ratio": high_risk_topics / total_topics}

def monitor_topic_exposure(topic, exposure_data):
    """
    Main function interface for monitoring exposure
    """
    prevention = NeuralHabituationPrevention()
    return prevention.monitor_topic_exposure(topic, exposure_data)

def filter_habituated_topics(candidate_topics):
    """
    Main function interface for filtering topics
    """
    prevention = NeuralHabituationPrevention()
    return prevention.filter_habituated_topics(candidate_topics)

def get_freshness_score(topic):
    """
    Main function interface for freshness scoring
    """
    prevention = NeuralHabituationPrevention()
    return prevention.get_freshness_score(topic)

def generate_novelty_intervals(topic):
    """
    Main function interface for novelty intervals
    """
    prevention = NeuralHabituationPrevention()
    return prevention.generate_novelty_intervals(topic)

def implement_content_variation(topic, base_content):
    """
    Main function interface for content variation
    """
    prevention = NeuralHabituationPrevention()
    return prevention.implement_content_variation(topic, base_content)

def get_habituation_status_report():
    """
    Main function interface for status reports
    """
    prevention = NeuralHabituationPrevention()
    return prevention.get_habituation_status_report()

if __name__ == "__main__":
    # Example usage
    prevention = NeuralHabituationPrevention()

    # Monitor some topic exposures
    topics_data = [
        ("Social Media Algorithms", {"engagement_rate": 0.065, "views": 1200}),
        ("Content Creation Tips", {"engagement_rate": 0.045, "views": 800}),
        ("AI Technology Trends", {"engagement_rate": 0.055, "views": 950})
    ]

    for topic, data in topics_data:
        result = prevention.monitor_topic_exposure(topic, data)
        print(f"Monitored {topic}: Risk level - {result['decay_analysis']['pattern']}")

    # Check freshness scores
    for topic, _ in topics_data:
        freshness = prevention.get_freshness_score(topic)
        print(f"{topic} freshness: {freshness:.2f}")

    # Get status report
    report = prevention.get_habituation_status_report()
    print(f"\nTracking {report['total_topics_tracked']} topics")
    print(f"Prevention effectiveness: {report['prevention_effectiveness']['overall_effectiveness']:.2f}")