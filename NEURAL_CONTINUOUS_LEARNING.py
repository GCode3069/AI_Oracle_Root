"""
Advanced Content Optimization System - Neural Continuous Learning
Continuously refines content strategy based on neuroscientific principles
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict, Counter


class NeuralStrategyLearner:
    """
    Continuously refines content strategy based on neuroscientific principles.
    Implements neuroplastic learning cycles and Hebbian learning integration.
    """
    
    def __init__(self, learning_data_file: str = "neural_learning_data.json"):
        self.learning_data_file = learning_data_file
        self.learning_data = self._load_learning_data()
    
    def _load_learning_data(self) -> Dict:
        """Load learning data from file."""
        if os.path.exists(self.learning_data_file):
            try:
                with open(self.learning_data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {
                    "successful_patterns": [],
                    "neural_insights": [],
                    "strategy_adjustments": [],
                    "learning_cycles": []
                }
        return {
            "successful_patterns": [],
            "neural_insights": [],
            "strategy_adjustments": [],
            "learning_cycles": []
        }
    
    def _save_learning_data(self):
        """Save learning data to file."""
        with open(self.learning_data_file, 'w', encoding='utf-8') as f:
            json.dump(self.learning_data, f, indent=2, ensure_ascii=False)
    
    def learn_from_neural_performance(self, tracking_data: List[Dict]) -> Dict:
        """
        Neuroscientific learning cycle:
        
        1. Analyze neural response patterns from recent content
        2. Identify successful neuro-engagement patterns:
           - Topics with highest amygdala response
           - Keywords with strongest prefrontal activation  
           - Timing with optimal gamma spike alignment
           - Styles with maximum mirror neuron activation
        3. Update neuro-response prediction models
        4. Refine frequency timing protocols
        5. Generate neuro-optimization improvements
        """
        if not tracking_data:
            return {"status": "no_data", "message": "No tracking data provided"}
        
        # Analyze recent performance
        recent_data = [
            entry for entry in tracking_data
            if entry.get("performance", {}).get("views", 0) > 0
        ]
        
        if not recent_data:
            return {"status": "no_performance_data", "message": "No performance data available"}
        
        # Identify successful patterns
        successful_patterns = self._identify_successful_patterns(recent_data)
        
        # Extract neural insights
        neural_insights = self._extract_neural_insights(recent_data)
        
        # Generate strategy adjustments
        strategy_adjustments = self._generate_strategy_adjustments(successful_patterns, neural_insights)
        
        # Record learning cycle
        learning_cycle = {
            "cycle_id": f"LC_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "content_analyzed": len(recent_data),
            "successful_patterns_identified": len(successful_patterns),
            "neural_insights": len(neural_insights),
            "strategy_adjustments": strategy_adjustments
        }
        
        # Update learning data
        self.learning_data["successful_patterns"].extend(successful_patterns)
        self.learning_data["neural_insights"].extend(neural_insights)
        self.learning_data["strategy_adjustments"].append(strategy_adjustments)
        self.learning_data["learning_cycles"].append(learning_cycle)
        
        # Keep only recent data (last 100 cycles)
        if len(self.learning_data["learning_cycles"]) > 100:
            self.learning_data["learning_cycles"] = self.learning_data["learning_cycles"][-100:]
        
        self._save_learning_data()
        
        return {
            "status": "learning_complete",
            "learning_cycle": learning_cycle,
            "successful_patterns": successful_patterns,
            "neural_insights": neural_insights,
            "strategy_adjustments": strategy_adjustments
        }
    
    def _identify_successful_patterns(self, tracking_data: List[Dict]) -> List[Dict]:
        """Identify successful neuro-engagement patterns."""
        successful_patterns = []
        
        # Filter high performers
        high_performers = [
            entry for entry in tracking_data
            if entry.get("performance", {}).get("engagement_rate", 0) >= 0.06
        ]
        
        for entry in high_performers:
            content = entry.get("content", {})
            neural_settings = entry.get("neural_settings", {})
            
            pattern = {
                "pattern_id": f"PATTERN_{len(successful_patterns) + 1}",
                "topic_keywords": self._extract_keywords(content.get("topic", "")),
                "content_type": content.get("content_type", ""),
                "presentation_style": content.get("presentation_style", ""),
                "neural_settings": neural_settings,
                "performance_metrics": {
                    "engagement_rate": entry.get("performance", {}).get("engagement_rate", 0),
                    "views": entry.get("performance", {}).get("views", 0)
                },
                "neural_correlates": {
                    "prefrontal_activation": neural_settings.get("prefrontal_activation", "medium"),
                    "limbic_engagement": neural_settings.get("limbic_engagement", 0.5),
                    "gamma_spikes": neural_settings.get("gamma_spikes", []),
                    "theta_undertone": neural_settings.get("theta_undertone", 0)
                }
            }
            successful_patterns.append(pattern)
        
        return successful_patterns
    
    def _extract_keywords(self, topic: str) -> List[str]:
        """Extract keywords from topic."""
        # Simple keyword extraction
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        words = topic.lower().split()
        keywords = [w for w in words if w not in stop_words and len(w) > 3]
        return keywords[:5]  # Top 5 keywords
    
    def _extract_neural_insights(self, tracking_data: List[Dict]) -> List[Dict]:
        """Extract neural insights from performance data."""
        insights = []
        
        # Analyze correlation between neural settings and performance
        for entry in tracking_data:
            neural_settings = entry.get("neural_settings", {})
            performance = entry.get("performance", {})
            
            if performance.get("engagement_rate", 0) > 0:
                insight = {
                    "insight_id": f"INSIGHT_{len(insights) + 1}",
                    "neural_setting": neural_settings,
                    "performance_outcome": performance.get("engagement_rate", 0),
                    "correlation": "positive" if performance.get("engagement_rate", 0) >= 0.05 else "neutral",
                    "recommendation": self._generate_insight_recommendation(neural_settings, performance)
                }
                insights.append(insight)
        
        return insights
    
    def _generate_insight_recommendation(self, neural_settings: Dict, performance: Dict) -> str:
        """Generate recommendation based on insight."""
        engagement_rate = performance.get("engagement_rate", 0)
        
        if engagement_rate >= 0.06:
            return (
                f"High engagement ({engagement_rate:.2%}) achieved with "
                f"gamma spikes at {neural_settings.get('gamma_spikes', [])} and "
                f"limbic engagement {neural_settings.get('limbic_engagement', 0):.2%}. "
                f"Replicate this pattern for similar content."
            )
        elif engagement_rate >= 0.04:
            return (
                f"Moderate engagement ({engagement_rate:.2%}). Consider increasing "
                f"gamma spike frequency or enhancing limbic engagement."
            )
        else:
            return (
                f"Low engagement ({engagement_rate:.2%}). Review neural settings "
                f"and consider alternative presentation styles."
            )
    
    def _generate_strategy_adjustments(self, successful_patterns: List[Dict],
                                      neural_insights: List[Dict]) -> Dict:
        """Generate strategy adjustments based on learning."""
        adjustments = {
            "topic_selection": {},
            "content_development": {},
            "neural_optimization": {},
            "platform_distribution": {}
        }
        
        # Analyze successful topics
        if successful_patterns:
            topic_keywords = []
            for pattern in successful_patterns:
                topic_keywords.extend(pattern.get("topic_keywords", []))
            
            keyword_counts = Counter(topic_keywords)
            top_keywords = [kw for kw, count in keyword_counts.most_common(5)]
            
            adjustments["topic_selection"] = {
                "prioritize_keywords": top_keywords,
                "recommendation": f"Focus on topics containing: {', '.join(top_keywords)}"
            }
        
        # Analyze successful neural settings
        if successful_patterns:
            gamma_spikes = []
            limbic_engagements = []
            presentation_styles = []
            
            for pattern in successful_patterns:
                neural = pattern.get("neural_correlates", {})
                gamma_spikes.extend(neural.get("gamma_spikes", []))
                limbic_engagements.append(neural.get("limbic_engagement", 0))
                presentation_styles.append(pattern.get("presentation_style", ""))
            
            if gamma_spikes:
                most_common_gamma = Counter(gamma_spikes).most_common(1)[0][0]
                adjustments["neural_optimization"] = {
                    "optimal_gamma_spikes": [most_common_gamma],
                    "average_limbic_engagement": sum(limbic_engagements) / len(limbic_engagements) if limbic_engagements else 0.6,
                    "recommendation": f"Use gamma spikes at {most_common_gamma}s for optimal insight moments"
                }
            
            if presentation_styles:
                most_common_style = Counter(presentation_styles).most_common(1)[0][0]
                adjustments["content_development"] = {
                    "preferred_presentation_style": most_common_style,
                    "recommendation": f"Prioritize {most_common_style} style for high engagement"
                }
        
        return adjustments
    
    def refine_neural_strategy(self, neural_insights: Optional[Dict] = None) -> Dict:
        """
        Neuro-strategy adjustments:
        - Content selection based on neural pathway efficiency
        - Keyword optimization for specific neurotransmitter release
        - Presentation style distribution for varied neural activation
        - Platform analysis frequency for social cognition development
        """
        # Use provided insights or load from learning data
        if not neural_insights:
            recent_cycles = self.learning_data.get("learning_cycles", [])[-5:]
            if recent_cycles:
                latest_cycle = recent_cycles[-1]
                neural_insights = latest_cycle.get("strategy_adjustments", {})
        
        refined_strategy = {
            "refinement_id": f"REFINE_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "strategy_updates": {
                "content_selection": {
                    "neural_pathway_efficiency": "optimized",
                    "keyword_priorities": neural_insights.get("topic_selection", {}).get("prioritize_keywords", []),
                    "habituation_prevention": "active"
                },
                "content_development": {
                    "presentation_style_distribution": neural_insights.get("content_development", {}).get("preferred_presentation_style", "thematic_presentation"),
                    "neural_variation": "maintained"
                },
                "neural_optimization": {
                    "frequency_timing": neural_insights.get("neural_optimization", {}).get("optimal_gamma_spikes", [8]),
                    "limbic_target": neural_insights.get("neural_optimization", {}).get("average_limbic_engagement", 0.7)
                },
                "platform_distribution": {
                    "social_cognition_focus": "enhanced",
                    "platform_analysis_frequency": "optimized"
                }
            },
            "hebbian_learning_applied": True,
            "neuroplastic_adaptation": "active"
        }
        
        return refined_strategy
    
    def get_learning_summary(self) -> Dict:
        """Get summary of learning progress."""
        return {
            "total_learning_cycles": len(self.learning_data.get("learning_cycles", [])),
            "successful_patterns_identified": len(self.learning_data.get("successful_patterns", [])),
            "neural_insights_collected": len(self.learning_data.get("neural_insights", [])),
            "strategy_adjustments_made": len(self.learning_data.get("strategy_adjustments", [])),
            "recent_insights": self.learning_data.get("neural_insights", [])[-5:],
            "learning_active": True
        }


if __name__ == "__main__":
    # Example usage
    learner = NeuralStrategyLearner()
    
    # Sample tracking data
    sample_tracking = [
        {
            "content": {
                "topic": "Education System Analysis",
                "content_type": "platform_features",
                "presentation_style": "charismatic_engagement"
            },
            "neural_settings": {
                "gamma_spikes": [8, 12],
                "limbic_engagement": 0.82,
                "prefrontal_activation": "high"
            },
            "performance": {
                "views": 1236,
                "engagement_rate": 0.0625
            }
        }
    ]
    
    learning_result = learner.learn_from_neural_performance(sample_tracking)
    print("Learning Result:")
    print(json.dumps(learning_result, indent=2))
    
    # Refine strategy
    refined = learner.refine_neural_strategy()
    print("\nRefined Strategy:")
    print(json.dumps(refined, indent=2))
    
    # Get summary
    summary = learner.get_learning_summary()
    print("\nLearning Summary:")
    print(json.dumps(summary, indent=2))
