"""
Advanced Content Optimization System - Cognitive Content Optimization
Manages topic selection through neural response prediction modeling
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Set
from collections import defaultdict
import random


class NeuroContentOptimization:
    """
    Manages topic selection through neural response prediction modeling.
    Applies cognitive neuroscience principles to optimize content selection.
    """
    
    def __init__(self, direct_input_file: str = "direct_input_topics.json"):
        self.direct_input_file = direct_input_file
        self.direct_topics = self._load_direct_topics()
        self.recent_topics = []  # Track for habituation prevention
        self.max_recent_memory = 50
        
        # High-performing keywords with neural response scores
        self.neural_keywords = {
            "high_amygdala": ["financial", "service", "education", "military", "student", "system"],
            "high_prefrontal": ["analysis", "strategy", "process", "how", "why", "method"],
            "high_mirror": ["creator", "people", "community", "social", "shared", "together"],
            "high_theta": ["learn", "remember", "important", "key", "essential", "critical"]
        }
    
    def _load_direct_topics(self) -> List[Dict]:
        """Load direct input topics."""
        if os.path.exists(self.direct_input_file):
            try:
                with open(self.direct_input_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get("topics", [])
            except:
                return []
        return []
    
    def add_direct_topic(self, topic: str, priority: int = 5, notes: str = ""):
        """Add a direct input topic with priority."""
        topic_entry = {
            "topic": topic,
            "priority": priority,
            "notes": notes,
            "added_at": datetime.now().isoformat(),
            "neural_score": self._calculate_topic_neural_score(topic)
        }
        
        self.direct_topics.append(topic_entry)
        self._save_direct_topics()
    
    def _save_direct_topics(self):
        """Save direct topics to file."""
        data = {"topics": self.direct_topics}
        with open(self.direct_input_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _calculate_topic_neural_score(self, topic: str) -> float:
        """Calculate neural engagement score for a topic."""
        topic_lower = topic.lower()
        score = 0.0
        
        # Check for high-performing neural keywords
        for keyword_type, keywords in self.neural_keywords.items():
            if any(kw in topic_lower for kw in keywords):
                if keyword_type == "high_amygdala":
                    score += 0.4  # Highest weight for emotional engagement
                elif keyword_type == "high_prefrontal":
                    score += 0.3
                elif keyword_type == "high_mirror":
                    score += 0.2
                elif keyword_type == "high_theta":
                    score += 0.1
        
        return min(score, 1.0)
    
    def select_with_neural_prediction(self, performance_insights: Optional[Dict] = None, 
                                     platform_analysis: Optional[List[str]] = None,
                                     max_topics: int = 10) -> List[Dict]:
        """
        Multi-factor neurological scoring for topic selection:
        
        1. Similarity to successful neural patterns (+ prefrontal activation)
        2. Inclusion of high-performing frequency keywords (+ amygdala response)
        3. Content freshness (avoiding habituation response)
        4. Temporal relevance (circadian rhythm alignment)
        5. Direct input priority (+ dopamine response prediction)
        6. Platform-relevant themes (+ social cognition activation)
        """
        candidates = []
        
        # 1. Direct input topics (highest priority)
        for topic_entry in sorted(self.direct_topics, key=lambda x: x.get("priority", 5), reverse=True):
            if not self._is_recently_used(topic_entry["topic"]):
                candidates.append({
                    "topic": topic_entry["topic"],
                    "source": "direct_input",
                    "priority": topic_entry.get("priority", 5),
                    "neural_score": topic_entry.get("neural_score", 0.5),
                    "dopamine_prediction": "high"  # Direct input triggers dopamine
                })
        
        # 2. Platform analysis topics
        if platform_analysis:
            for topic in platform_analysis:
                if not self._is_recently_used(topic):
                    candidates.append({
                        "topic": topic,
                        "source": "platform_analysis",
                        "priority": 4,
                        "neural_score": self._calculate_topic_neural_score(topic),
                        "social_cognition": "high"
                    })
        
        # 3. Performance-informed topics
        if performance_insights:
            high_performers = performance_insights.get("high_performers", [])
            for performer in high_performers[:5]:  # Top 5 performers
                topic = performer.get("title", "")
                if topic and not self._is_recently_used(topic):
                    candidates.append({
                        "topic": topic,
                        "source": "performance_based",
                        "priority": 3,
                        "neural_score": performer.get("neural_score", 0.6),
                        "similarity_to_success": "high"
                    })
        
        # Score and rank candidates
        scored_candidates = []
        for candidate in candidates:
            final_score = self._calculate_final_neural_score(candidate, performance_insights)
            candidate["final_neural_score"] = final_score
            scored_candidates.append(candidate)
        
        # Sort by final score and return top candidates
        scored_candidates.sort(key=lambda x: x["final_neural_score"], reverse=True)
        
        selected = scored_candidates[:max_topics]
        
        # Update recent topics
        for item in selected:
            self._mark_as_recent(item["topic"])
        
        return selected
    
    def _is_recently_used(self, topic: str) -> bool:
        """Check if topic was recently used (habituation prevention)."""
        return topic.lower() in [t.lower() for t in self.recent_topics]
    
    def _mark_as_recent(self, topic: str):
        """Mark topic as recently used."""
        self.recent_topics.append(topic.lower())
        if len(self.recent_topics) > self.max_recent_memory:
            self.recent_topics.pop(0)
    
    def _calculate_final_neural_score(self, candidate: Dict, performance_insights: Optional[Dict]) -> float:
        """Calculate final neural engagement score."""
        base_score = candidate.get("neural_score", 0.5)
        priority_multiplier = candidate.get("priority", 3) / 5.0
        
        # Boost for direct input (dopamine prediction)
        if candidate.get("source") == "direct_input":
            base_score += 0.2
        
        # Boost for performance similarity
        if candidate.get("similarity_to_success") == "high":
            base_score += 0.15
        
        # Boost for social cognition activation
        if candidate.get("social_cognition") == "high":
            base_score += 0.1
        
        # Apply priority multiplier
        final_score = base_score * (0.7 + 0.3 * priority_multiplier)
        
        return min(final_score, 1.0)
    
    def get_topic_sources(self) -> Dict:
        """Get available topic sources."""
        return {
            "direct_input_count": len(self.direct_topics),
            "direct_topics": [t["topic"] for t in self.direct_topics[:10]],
            "recent_topics_count": len(self.recent_topics),
            "habituation_prevention": "active"
        }


if __name__ == "__main__":
    # Example usage
    optimizer = NeuroContentOptimization()
    
    # Add some direct topics
    optimizer.add_direct_topic("Student Financial Aid System", priority=5, notes="High engagement potential")
    optimizer.add_direct_topic("Education Platform Analysis", priority=4)
    
    # Select topics
    performance_insights = {
        "high_performers": [
            {"title": "Education System Analysis", "neural_score": 0.75}
        ]
    }
    
    selected = optimizer.select_with_neural_prediction(
        performance_insights=performance_insights,
        platform_analysis=["Content Creator Strategies", "Social Media Engagement"],
        max_topics=5
    )
    
    print(json.dumps(selected, indent=2))
