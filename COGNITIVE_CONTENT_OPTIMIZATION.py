"""
COGNITIVE_CONTENT_OPTIMIZATION.py

Purpose: Manage topic selection through neural response prediction modeling

Content Sources with Neural Pathway Mapping:
1. Trend Analysis (default mode network activation)
2. Direct Input (executive function engagement)
3. Platform Analysis (social cognition activation)

Topic Selection with Neural Response Scoring
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

class NeuroContentOptimization:
    """
    Manages topic selection through neural response prediction modeling
    """

    def __init__(self):
        self.content_sources = {
            "trend_analysis": {
                "neural_pathway": "default_mode_network",
                "activation_type": "novelty_response_prediction",
                "weight": 0.3
            },
            "direct_input": {
                "neural_pathway": "executive_function",
                "activation_type": "conscious_processing",
                "weight": 0.4
            },
            "platform_analysis": {
                "neural_pathway": "social_cognition",
                "activation_type": "mirror_neuron_stimulation",
                "weight": 0.3
            }
        }

        self.habituation_tracker = HabituationPreventionSystem()

    def select_with_neural_prediction(self, performance_insights: Dict[str, Any]) -> Dict[str, Any]:
        """
        Multi-factor neurological scoring:

        1. Similarity to successful neural patterns (+ prefrontal activation)
        2. Inclusion of high-performing frequency keywords (+ amygdala response)
        3. Content freshness (avoiding habituation response)
        4. Temporal relevance (circadian rhythm alignment)
        5. Direct input priority (+ dopamine response prediction)
        6. Platform-relevant themes (+ social cognition activation)

        Returns topics with highest predicted neural engagement scores
        """
        candidates = self._gather_topic_candidates(performance_insights)

        scored_topics = []
        for candidate in candidates:
            score = self._calculate_neural_score(candidate, performance_insights)
            scored_topics.append({
                "topic": candidate,
                "neural_score": score,
                "neural_breakdown": self._get_score_breakdown(candidate, performance_insights)
            })

        # Sort by neural score descending
        scored_topics.sort(key=lambda x: x["neural_score"], reverse=True)

        return {
            "selected_topics": scored_topics[:10],  # Top 10
            "neural_predictions": self._generate_predictions(scored_topics[:10]),
            "habituation_status": self.habituation_tracker.get_status()
        }

    def _gather_topic_candidates(self, performance_insights: Dict[str, Any]) -> List[str]:
        """
        Gather topics from all neural pathway sources
        """
        candidates = []

        # Trend analysis topics
        trend_topics = self._analyze_trends(performance_insights)
        candidates.extend(trend_topics)

        # Direct input topics
        direct_topics = self._get_direct_input()
        candidates.extend(direct_topics)

        # Platform analysis topics
        platform_topics = self._analyze_platforms(performance_insights)
        candidates.extend(platform_topics)

        # Remove duplicates and filter habituated topics
        unique_candidates = list(set(candidates))
        filtered_candidates = self.habituation_tracker.filter_habituated(unique_candidates)

        return filtered_candidates

    def _analyze_trends(self, performance_insights: Dict[str, Any]) -> List[str]:
        """
        Trend Analysis (default mode network activation)
        - Monitors current topics of discussion
        - Predicts neural novelty response
        """
        trends = []

        # Extract successful topics from performance insights
        successful_patterns = performance_insights.get("successful_patterns", [])
        for pattern in successful_patterns:
            topic = pattern.get("topic", "")
            if topic:
                trends.append(f"Trend: {topic}")

        # Add current discussion topics (simulated)
        current_trends = [
            "AI Technology Trends",
            "Social Media Algorithms",
            "Content Creation Strategies",
            "Digital Marketing Evolution"
        ]
        trends.extend(current_trends)

        return trends

    def _get_direct_input(self) -> List[str]:
        """
        Direct Input (executive function engagement)
        - Reads from designated input channels
        - Leverages conscious cognitive processing
        """
        # In a real implementation, this would read from input channels
        # For now, return some example direct inputs
        direct_inputs = [
            "Platform Recommendation Systems",
            "Content Visibility Strategies",
            "Educational Content Providers",
            "Social Media Habit Formation"
        ]

        return direct_inputs

    def _analyze_platforms(self, performance_insights: Dict[str, Any]) -> List[str]:
        """
        Platform Analysis (social cognition activation)
        - Platform feature discussions (theory of mind engagement)
        - Creator ecosystem observations (mirror neuron stimulation)
        - Algorithm performance observations (pattern recognition activation)
        - Social media trend observations (social reward anticipation)
        """
        platform_topics = [
            "YouTube Algorithm Changes",
            "TikTok Content Strategy",
            "Instagram Reels Optimization",
            "Creator Monetization Trends",
            "Social Media Engagement Patterns",
            "Content Discovery Systems",
            "Platform Feature Updates",
            "Algorithm Performance Analysis"
        ]

        return platform_topics

    def _calculate_neural_score(self, candidate: str, performance_insights: Dict[str, Any]) -> float:
        """
        Calculate neural engagement score based on multiple factors
        """
        score = 0.0

        # Factor 1: Similarity to successful patterns
        similarity_score = self._calculate_similarity_score(candidate, performance_insights)
        score += similarity_score * 0.25

        # Factor 2: High-performing keywords
        keyword_score = self._calculate_keyword_score(candidate)
        score += keyword_score * 0.20

        # Factor 3: Content freshness
        freshness_score = self.habituation_tracker.get_freshness_score(candidate)
        score += freshness_score * 0.15

        # Factor 4: Temporal relevance
        temporal_score = self._calculate_temporal_score(candidate)
        score += temporal_score * 0.15

        # Factor 5: Direct input priority
        direct_score = 1.0 if "Direct:" in candidate else 0.0
        score += direct_score * 0.15

        # Factor 6: Platform relevance
        platform_score = self._calculate_platform_score(candidate)
        score += platform_score * 0.10

        return min(score, 1.0)  # Cap at 1.0

    def _calculate_similarity_score(self, candidate: str, performance_insights: Dict[str, Any]) -> float:
        """
        Similarity to successful neural patterns
        """
        successful_patterns = performance_insights.get("successful_patterns", [])
        candidate_lower = candidate.lower()

        for pattern in successful_patterns:
            pattern_topic = pattern.get("topic", "").lower()
            if pattern_topic in candidate_lower or candidate_lower in pattern_topic:
                return 0.9

        # Partial matches
        keywords = ["education", "system", "military", "service", "financial", "student"]
        for keyword in keywords:
            if keyword in candidate_lower:
                return 0.7

        return 0.3

    def _calculate_keyword_score(self, candidate: str) -> float:
        """
        High-performing frequency keywords
        """
        high_performing_keywords = [
            "system", "algorithm", "platform", "content", "strategy",
            "optimization", "engagement", "performance", "analysis"
        ]

        candidate_lower = candidate.lower()
        matches = sum(1 for keyword in high_performing_keywords if keyword in candidate_lower)

        return min(matches * 0.2, 1.0)

    def _calculate_temporal_score(self, candidate: str) -> float:
        """
        Temporal relevance (circadian rhythm alignment)
        """
        # Simulate time-based relevance
        current_hour = datetime.now().hour

        # Peak engagement times (assuming)
        if 8 <= current_hour <= 12 or 18 <= current_hour <= 22:
            return 0.9
        else:
            return 0.6

    def _calculate_platform_score(self, candidate: str) -> float:
        """
        Platform-relevant themes
        """
        platform_keywords = ["youtube", "tiktok", "instagram", "platform", "algorithm", "social media"]
        candidate_lower = candidate.lower()

        matches = sum(1 for keyword in platform_keywords if keyword in candidate_lower)
        return min(matches * 0.3, 1.0)

    def _get_score_breakdown(self, candidate: str, performance_insights: Dict[str, Any]) -> Dict[str, float]:
        """
        Get detailed breakdown of neural score components
        """
        return {
            "similarity_score": self._calculate_similarity_score(candidate, performance_insights),
            "keyword_score": self._calculate_keyword_score(candidate),
            "freshness_score": self.habituation_tracker.get_freshness_score(candidate),
            "temporal_score": self._calculate_temporal_score(candidate),
            "platform_score": self._calculate_platform_score(candidate)
        }

    def _generate_predictions(self, selected_topics: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate neural response predictions for selected topics
        """
        predictions = {}

        for topic_data in selected_topics:
            topic = topic_data["topic"]
            score = topic_data["neural_score"]

            predictions[topic] = {
                "predicted_engagement": score * 6.25,  # Based on 6.25% target
                "neural_pathways": self._predict_neural_pathways(topic),
                "optimization_recommendations": self._get_optimization_recs(topic, score)
            }

        return predictions

    def _predict_neural_pathways(self, topic: str) -> List[str]:
        """
        Predict which neural pathways will be activated
        """
        pathways = []
        topic_lower = topic.lower()

        if "education" in topic_lower or "system" in topic_lower:
            pathways.extend(["prefrontal_cortex", "amygdala"])
        if "service" in topic_lower or "social" in topic_lower:
            pathways.extend(["mirror_neurons", "social_cognition"])
        if "financial" in topic_lower or "strategy" in topic_lower:
            pathways.extend(["limbic_system", "dopamine_response"])

        return pathways

    def _get_optimization_recs(self, topic: str, score: float) -> List[str]:
        """
        Get optimization recommendations based on topic and score
        """
        recs = []

        if score > 0.8:
            recs.append("High neural potential - maintain current approach")
        elif score > 0.6:
            recs.append("Good potential - enhance emotional elements")
        else:
            recs.append("Moderate potential - add novelty and relevance")

        if "platform" in topic.lower():
            recs.append("Include social neuroscience elements")
        if "content" in topic.lower():
            recs.append("Optimize for cognitive load and attention")

        return recs

class HabituationPreventionSystem:
    """
    Monitors neural response decay curves
    Implements optimal novelty intervals
    Prevents receptor downregulation through content variation
    """

    def __init__(self):
        self.habituated_topics = {}
        self.novelty_intervals = {}

    def filter_habituated(self, candidates: List[str]) -> List[str]:
        """
        Filter out topics that have been overused recently
        """
        filtered = []
        current_time = datetime.now()

        for candidate in candidates:
            last_used = self.habituated_topics.get(candidate)
            if last_used is None:
                filtered.append(candidate)
            else:
                days_since = (current_time - last_used).days
                if days_since > 7:  # Allow reuse after 7 days
                    filtered.append(candidate)

        return filtered

    def get_freshness_score(self, topic: str) -> float:
        """
        Calculate freshness score (higher = more novel)
        """
        last_used = self.habituated_topics.get(topic)
        if last_used is None:
            return 1.0  # Completely fresh

        days_since = (datetime.now() - last_used).days
        # Decay over time - fresher topics score higher
        freshness = max(0, 1.0 - (days_since / 30.0))  # 30-day decay

        return freshness

    def mark_used(self, topic: str):
        """
        Mark topic as used to track habituation
        """
        self.habituated_topics[topic] = datetime.now()

    def get_status(self) -> Dict[str, Any]:
        """
        Get current habituation status
        """
        return {
            "habituated_count": len(self.habituated_topics),
            "recently_used": list(self.habituated_topics.keys())[:5],  # Last 5
            "freshness_distribution": "Available on demand"
        }

def select_with_neural_prediction(performance_insights):
    """
    Main function interface for the module
    """
    optimizer = NeuroContentOptimization()
    return optimizer.select_with_neural_prediction(performance_insights)

if __name__ == "__main__":
    # Example usage
    sample_insights = {
        "successful_patterns": [
            {"topic": "Education System", "engagement": 2.73},
            {"topic": "Military Service", "engagement": 3.01}
        ]
    }

    results = select_with_neural_prediction(sample_insights)
    print(json.dumps(results, indent=2))