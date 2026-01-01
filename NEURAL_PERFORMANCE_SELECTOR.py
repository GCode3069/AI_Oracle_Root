"""
NEURAL_PERFORMANCE_SELECTOR.py

Purpose: Select content topics based on neurological response data

Neural Selection Framework with performance-based scoring
"""

import json
from typing import Dict, List, Any, Optional

class NeuralPerformanceSelector:
    """
    Selects content topics based on neurological response data
    """

    def __init__(self):
        self.neural_weights = {
            "prefrontal_activation": 0.3,
            "amygdala_response": 0.4,
            "mirror_neuron_activation": 0.2,
            "theta_coherence": 0.1
        }

        self.successful_patterns = {
            "educational_themes": {
                "neural_response": {"prefrontal_activation": 0.40, "amygdala_response": 0.40},
                "performance": {"views": 1236, "engagement_rate": 2.73}
            },
            "service_related": {
                "neural_response": {"mirror_neuron_activation": 0.35, "theta_coherence": 0.70},
                "performance": {"views": 1194, "engagement_rate": 3.01}
            },
            "financial_discussion": {
                "neural_response": {"amygdala_response": 0.82, "theta_coherence": 0.75},
                "performance": {"views": 349, "engagement_rate": 6.25}
            }
        }

    def select_with_neural_data(self, candidates: List[str], performance_insights: Dict[str, Any]) -> Dict[str, Any]:
        """
        Neuroscientific scoring based on performance data:

        SUCCESSFUL NEURAL PATTERNS:
        - Educational themes: 1236 views → 40% prefrontal activation
        - Service-related themes: 1194 views → 35% mirror neuron activation
        - Financial discussion themes: 6.25% engagement → 82% limbic engagement

        HIGH-PERFORMING NEURAL TRIGGERS:
        - System-related terms → Pattern recognition circuit activation
        - Active process terms → Motor cortex engagement
        - Modern discussion terms → 82% limbic system engagement

        NEUROLOGICAL CONTENT PATTERNS:
        - Timely/relevant discussions → Circadian-aligned attention
        - Institutional discussion → Social hierarchy neural networks
        - Comparative analysis → Prefrontal executive function

        NEURAL HABITUATION RISKS:
        - General process updates → Lower limbic engagement potential
        - Topics recently addressed → Neural response decay observed
        """
        scored_candidates = []

        for candidate in candidates:
            neural_score = self._calculate_neural_engagement_score(candidate, performance_insights)
            pattern_match = self._find_pattern_match(candidate)
            habituation_risk = self._assess_habituation_risk(candidate, performance_insights)

            scored_candidates.append({
                "topic": candidate,
                "neural_engagement_score": neural_score,
                "pattern_match": pattern_match,
                "habituation_risk": habituation_risk,
                "selection_confidence": self._calculate_selection_confidence(neural_score, pattern_match, habituation_risk),
                "neural_breakdown": self._get_neural_breakdown(candidate)
            })

        # Sort by selection confidence
        scored_candidates.sort(key=lambda x: x["selection_confidence"], reverse=True)

        return {
            "selected_topics": scored_candidates[:5],  # Top 5 selections
            "neural_analysis": self._generate_neural_analysis(scored_candidates[:5]),
            "selection_criteria": self._get_selection_criteria()
        }

    def _calculate_neural_engagement_score(self, candidate: str, performance_insights: Dict[str, Any]) -> float:
        """
        Calculate NEURAL_ENGAGEMENT_SCORE using the formula:
        (Prefrontal Activation × 0.3) + (Amygdala Response × 0.4) +
        (Mirror Neuron Activation × 0.2) + (Theta Coherence × 0.1)
        """
        # Get neural metrics for this candidate
        neural_metrics = self._extract_neural_metrics(candidate, performance_insights)

        score = (
            neural_metrics["prefrontal_activation"] * self.neural_weights["prefrontal_activation"] +
            neural_metrics["amygdala_response"] * self.neural_weights["amygdala_response"] +
            neural_metrics["mirror_neuron_activation"] * self.neural_weights["mirror_neuron_activation"] +
            neural_metrics["theta_coherence"] * self.neural_weights["theta_coherence"]
        )

        return min(score, 1.0)  # Cap at 1.0

    def _extract_neural_metrics(self, candidate: str, performance_insights: Dict[str, Any]) -> Dict[str, float]:
        """
        Extract neural metrics for a candidate topic
        """
        candidate_lower = candidate.lower()

        # Base metrics
        metrics = {
            "prefrontal_activation": 0.0,
            "amygdala_response": 0.0,
            "mirror_neuron_activation": 0.0,
            "theta_coherence": 0.0
        }

        # Educational themes
        if any(word in candidate_lower for word in ["education", "system", "analysis", "strategy"]):
            metrics["prefrontal_activation"] = 0.40
            metrics["theta_coherence"] = 0.65

        # Service-related themes
        if any(word in candidate_lower for word in ["service", "military", "social", "community"]):
            metrics["mirror_neuron_activation"] = 0.35
            metrics["theta_coherence"] = 0.70

        # Financial/emotional themes
        if any(word in candidate_lower for word in ["financial", "crisis", "challenge", "emotional"]):
            metrics["amygdala_response"] = 0.82
            metrics["theta_coherence"] = 0.75

        # System-related terms
        if "system" in candidate_lower:
            metrics["prefrontal_activation"] += 0.2

        # Active process terms
        if any(word in candidate_lower for word in ["active", "process", "working", "engagement"]):
            metrics["mirror_neuron_activation"] += 0.15

        # Modern discussion terms
        if any(word in candidate_lower for word in ["modern", "current", "trending", "latest"]):
            metrics["amygdala_response"] += 0.1

        # Look for matches in performance insights
        successful_patterns = performance_insights.get("successful_patterns", [])
        for pattern in successful_patterns:
            pattern_topic = pattern.get("topic", "").lower()
            if pattern_topic in candidate_lower:
                pattern_neural = pattern.get("neural_correlation", {})
                metrics.update(pattern_neural)
                break

        return metrics

    def _find_pattern_match(self, candidate: str) -> Dict[str, Any]:
        """
        Find matching successful neural patterns
        """
        candidate_lower = candidate.lower()

        for pattern_name, pattern_data in self.successful_patterns.items():
            keywords = pattern_name.replace("_", " ").split()
            if any(keyword in candidate_lower for keyword in keywords):
                return {
                    "pattern": pattern_name,
                    "match_strength": 0.8,
                    "performance_correlation": pattern_data["performance"]
                }

        return {
            "pattern": "general",
            "match_strength": 0.3,
            "performance_correlation": {"views": 500, "engagement_rate": 2.0}
        }

    def _assess_habituation_risk(self, candidate: str, performance_insights: Dict[str, Any]) -> float:
        """
        Assess neural habituation risk (0.0 = no risk, 1.0 = high risk)
        """
        # Check if topic was recently covered
        recent_content = performance_insights.get("recent_content", [])
        candidate_lower = candidate.lower()

        for content in recent_content:
            content_topic = content.get("topic", "").lower()
            if content_topic in candidate_lower or candidate_lower in content_topic:
                days_since = content.get("days_since", 0)
                if days_since < 7:
                    return 0.8  # High risk if covered in last week
                elif days_since < 30:
                    return 0.4  # Moderate risk if covered in last month

        # General habituation based on topic type
        if any(word in candidate_lower for word in ["update", "change", "new"]):
            return 0.6  # Updates tend to habituate quickly

        return 0.1  # Low risk for novel topics

    def _calculate_selection_confidence(self, neural_score: float, pattern_match: Dict[str, Any], habituation_risk: float) -> float:
        """
        Calculate overall selection confidence
        """
        base_confidence = neural_score * 0.6
        pattern_bonus = pattern_match["match_strength"] * 0.3
        habituation_penalty = habituation_risk * 0.1

        confidence = base_confidence + pattern_bonus - habituation_penalty

        return max(0.0, min(1.0, confidence))

    def _get_neural_breakdown(self, candidate: str) -> Dict[str, float]:
        """
        Get detailed neural activation breakdown
        """
        # Simulate neural breakdown based on topic
        candidate_lower = candidate.lower()

        breakdown = {
            "prefrontal_cortex": 0.0,
            "amygdala": 0.0,
            "mirror_neurons": 0.0,
            "limbic_system": 0.0,
            "temporal_lobe": 0.0
        }

        if "education" in candidate_lower or "system" in candidate_lower:
            breakdown["prefrontal_cortex"] = 0.40
            breakdown["temporal_lobe"] = 0.35

        if "financial" in candidate_lower or "emotional" in candidate_lower:
            breakdown["amygdala"] = 0.82
            breakdown["limbic_system"] = 0.75

        if "service" in candidate_lower or "social" in candidate_lower:
            breakdown["mirror_neurons"] = 0.35
            breakdown["limbic_system"] = 0.45

        return breakdown

    def _generate_neural_analysis(self, selected_topics: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate comprehensive neural analysis for selected topics
        """
        analysis = {
            "top_performers": [],
            "neural_patterns": {},
            "engagement_predictions": {}
        }

        for topic_data in selected_topics:
            topic = topic_data["topic"]
            score = topic_data["neural_engagement_score"]

            analysis["top_performers"].append({
                "topic": topic,
                "predicted_engagement": score * 6.25,  # Based on 6.25% target
                "neural_activation": topic_data["neural_breakdown"]
            })

            analysis["engagement_predictions"][topic] = {
                "click_through_rate": score * 3.0,  # 3% target CTR
                "viewer_retention": 0.45 + (score * 0.3),  # 45% base retention
                "share_potential": score * 2.5
            }

        return analysis

    def _get_selection_criteria(self) -> Dict[str, Any]:
        """
        Get the criteria used for neural selection
        """
        return {
            "neural_weights": self.neural_weights,
            "pattern_types": list(self.successful_patterns.keys()),
            "habituation_threshold": 0.7,
            "minimum_confidence": 0.5,
            "selection_algorithm": "weighted_neural_engagement_scoring"
        }

def select_with_neural_data(candidates, performance_insights):
    """
    Main function interface for the module
    """
    selector = NeuralPerformanceSelector()
    return selector.select_with_neural_data(candidates, performance_insights)

if __name__ == "__main__":
    # Example usage
    candidates = [
        "Education System Updates",
        "Military Service Benefits",
        "Student Financial Aid",
        "Social Media Algorithms",
        "Content Creator Strategies"
    ]

    performance_insights = {
        "successful_patterns": [
            {"topic": "Education System", "neural_correlation": {"prefrontal_activation": 0.40}}
        ],
        "recent_content": [
            {"topic": "Social Media Updates", "days_since": 3}
        ]
    }

    results = select_with_neural_data(candidates, performance_insights)
    print(json.dumps(results, indent=2))