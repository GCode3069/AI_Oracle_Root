"""
Advanced Content Optimization System - Complete Neuro Content Pipeline
End-to-end neuroscientific content system integration
"""

import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional

# Import all neuro modules
from NEURO_PERFORMANCE_ANALYTICS import NeuroPerformanceAnalytics
from COGNITIVE_CONTENT_OPTIMIZATION import NeuroContentOptimization
from SOCIAL_NEURO_PLATFORM_CONTENT import SocialNeuroPlatformContent
from NEURAL_PERFORMANCE_SELECTOR import NeuralPerformanceSelector
from NEURO_ENHANCED_CONTENT_DEVELOPMENT import NeuroEnhancedContentDevelopment
from NEURO_PERFORMANCE_TRACKING import NeuroPerformanceTracking
from NEURAL_CONTINUOUS_LEARNING import NeuralStrategyLearner
from NEURAL_HABITUATION_PREVENTION import NeuralHabituationPrevention


class CompleteNeuroContentPipeline:
    """
    Complete neuroscientific content system.
    Integrates all neuro-optimization modules for end-to-end content generation.
    """
    
    def __init__(self, config_file: str = "neuro_pipeline_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
        
        # Initialize all modules
        self.analytics = NeuroPerformanceAnalytics(self.config.get("performance_data_file", "performance_data.json"))
        self.optimizer = NeuroContentOptimization(self.config.get("direct_input_file", "direct_input_topics.json"))
        self.platform_content = SocialNeuroPlatformContent()
        self.selector = NeuralPerformanceSelector()
        self.developer = NeuroEnhancedContentDevelopment()
        self.tracker = NeuroPerformanceTracking(self.config.get("tracking_file", "neuro_performance_tracking.json"))
        self.learner = NeuralStrategyLearner(self.config.get("learning_data_file", "neural_learning_data.json"))
        self.habituation = NeuralHabituationPrevention(self.config.get("history_file", "content_history.json"))
    
    def _load_config(self) -> Dict:
        """Load pipeline configuration."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self._default_config()
        return self._default_config()
    
    def _default_config(self) -> Dict:
        """Default configuration."""
        return {
            "performance_data_file": "performance_data.json",
            "direct_input_file": "direct_input_topics.json",
            "tracking_file": "neuro_performance_tracking.json",
            "learning_data_file": "neural_learning_data.json",
            "history_file": "content_history.json",
            "output_directory": "neuro_content_output",
            "default_quantity": 50,
            "modes": {
                "neuro_automated": True,
                "neuro_direct_input": True,
                "neuro_platform_focus": True,
                "neuro_performance_focus": True
            }
        }
    
    def generate_neuro_optimized_collection(self, quantity: int = 50, 
                                          mode: str = "neuro_automated",
                                          direct_topics: Optional[List[str]] = None) -> Dict:
        """
        Complete neuroscientific content system:
        
        1. NEURO-ANALYSIS: Review neural performance correlations
        2. TOPIC GATHERING: Collect topics with neural response prediction
        3. NEURAL SELECTION: Neuro-optimized topic selection
        4. CONTENT DEVELOPMENT: Create versions with frequency protocols
        5. NEURO-OPTIMIZATION: Apply complete engagement science
        6. PRODUCTION: Generate final neuro-enhanced content
        7. NEURAL DISTRIBUTION: Route to neurologically appropriate platforms
        8. PUBLICATION: Multi-platform deployment with circadian alignment
        9. NEURO-TRACKING: Log with biometric correlation
        10. NEURO-LEARNING: Update neural strategy insights
        """
        results = {
            "pipeline_run_id": f"PIPELINE_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "mode": mode,
            "quantity_requested": quantity,
            "generated_content": [],
            "summary": {}
        }
        
        # Step 1: Neuro-Analysis
        print("Step 1: Analyzing neural performance correlations...")
        performance_insights = self.analytics.get_neural_insights()
        
        # Step 2: Topic Gathering
        print("Step 2: Gathering topics with neural response prediction...")
        platform_topics = []
        if mode in ["neuro_platform_focus", "neuro_automated"]:
            # Generate platform analysis topics
            platform_topics = [
                "Content Creator Engagement Strategies",
                "Platform Recommendation Systems",
                "Social Media Algorithm Optimization"
            ]
        
        # Add direct topics if provided
        if direct_topics:
            for topic in direct_topics:
                self.optimizer.add_direct_topic(topic, priority=5)
        
        # Step 3: Neural Selection
        print("Step 3: Selecting topics with neural optimization...")
        selected_topics = self.optimizer.select_with_neural_prediction(
            performance_insights=performance_insights,
            platform_analysis=platform_topics,
            max_topics=quantity
        )
        
        # Further refine with neural selector
        neural_selected = self.selector.select_with_neural_data(
            selected_topics,
            performance_insights
        )
        
        # Step 4-6: Content Development and Optimization
        print("Step 4-6: Developing and optimizing content...")
        generated_count = 0
        
        for topic_data in neural_selected[:quantity]:
            topic = topic_data.get("topic", "")
            if not topic:
                continue
            
            # Check habituation risk
            habituation_check = self.habituation.check_habituation_risk(
                topic=topic,
                content_type=topic_data.get("source", "auto"),
                presentation_style="thematic_presentation",
                neural_settings={"gamma_spikes": [8], "limbic_engagement": 0.7}
            )
            
            if habituation_check["habituation_risk"] == "high":
                print(f"  Skipping {topic} due to high habituation risk")
                continue
            
            # Develop platform content
            platform_content = self.platform_content.develop_neuro_platform_content(
                topic=topic,
                content_type=topic_data.get("source", "auto")
            )
            
            # Create enhanced versions
            adaptations = self.developer.create_neuro_adaptations(
                topic=topic,
                content_type=platform_content.get("content_type", "auto")
            )
            
            # Generate tracking ID
            tracking_id = f"TRACK_{uuid.uuid4().hex[:8].upper()}"
            
            # Prepare content data for tracking
            enhanced_content_data = {
                "title": f"{topic} - Neuro-Optimized",
                "topic": topic,
                "content_type": platform_content.get("content_type", "auto"),
                "presentation_style": adaptations.get("enhanced_version", {}).get("style", "thematic_presentation"),
                "version": "enhanced",
                "neural_settings": adaptations.get("enhanced_version", {}).get("neural_settings", {}),
                "platforms": adaptations.get("enhanced_version", {}).get("platforms", ["YouTube"]),
                "content_location": f"{self.config['output_directory']}/{tracking_id}.txt"
            }
            
            # Step 9: Neuro-Tracking
            log_entry = self.tracker.log_with_neural_correlation(tracking_id, enhanced_content_data)
            
            # Record in habituation prevention
            self.habituation.record_content(
                topic=topic,
                content_type=platform_content.get("content_type", "auto"),
                presentation_style=enhanced_content_data["presentation_style"],
                neural_settings=enhanced_content_data["neural_settings"]
            )
            
            # Save content
            content_output = {
                "tracking_id": tracking_id,
                "topic": topic,
                "enhanced_content": adaptations.get("enhanced_version", {}).get("content", ""),
                "standard_content": adaptations.get("standard_version", {}).get("content", ""),
                "platform_content": platform_content.get("content", ""),
                "neural_settings": enhanced_content_data["neural_settings"],
                "platforms": enhanced_content_data["platforms"],
                "habituation_risk": habituation_check["habituation_risk"],
                "neural_score": topic_data.get("neural_engagement_score", 0)
            }
            
            # Save to file
            self._save_content_output(content_output)
            
            results["generated_content"].append(content_output)
            generated_count += 1
            
            if generated_count >= quantity:
                break
        
        # Step 10: Neuro-Learning
        print("Step 10: Updating neural strategy insights...")
        tracking_summary = self.tracker.get_neural_performance_summary()
        learning_result = self.learner.learn_from_neural_performance(
            self.tracker.tracking_data.get("content_log", [])
        )
        
        # Generate summary
        results["summary"] = {
            "content_generated": generated_count,
            "neural_insights_applied": len(performance_insights.get("successful_patterns", [])),
            "habituation_prevented": sum(1 for c in results["generated_content"] 
                                        if c.get("habituation_risk") != "high"),
            "average_neural_score": sum(c.get("neural_score", 0) for c in results["generated_content"]) / max(generated_count, 1),
            "learning_cycle_completed": learning_result.get("status") == "learning_complete"
        }
        
        return results
    
    def _save_content_output(self, content_output: Dict):
        """Save content output to file."""
        output_dir = self.config.get("output_directory", "neuro_content_output")
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, f"{content_output['tracking_id']}.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(content_output, f, indent=2, ensure_ascii=False)
    
    def update_performance_and_learn(self, tracking_id: str, performance_data: Dict):
        """Update performance data and trigger learning cycle."""
        # Update tracking
        update_result = self.tracker.update_performance_with_neural_adaptation(
            tracking_id, performance_data
        )
        
        # Trigger learning
        tracking_summary = self.tracker.get_neural_performance_summary()
        learning_result = self.learner.learn_from_neural_performance(
            self.tracker.tracking_data.get("content_log", [])
        )
        
        return {
            "tracking_update": update_result,
            "learning_result": learning_result
        }
    
    def get_system_status(self) -> Dict:
        """Get current system status."""
        return {
            "pipeline_active": True,
            "modules_loaded": {
                "analytics": True,
                "optimizer": True,
                "platform_content": True,
                "selector": True,
                "developer": True,
                "tracker": True,
                "learner": True,
                "habituation": True
            },
            "tracking_summary": self.tracker.get_neural_performance_summary(),
            "learning_summary": self.learner.get_learning_summary(),
            "config": self.config
        }


if __name__ == "__main__":
    # Example usage
    pipeline = CompleteNeuroContentPipeline()
    
    # Check system status
    status = pipeline.get_system_status()
    print("System Status:")
    print(json.dumps(status, indent=2))
    
    # Generate neuro-optimized content collection
    print("\n" + "="*50)
    print("Generating Neuro-Optimized Content Collection")
    print("="*50 + "\n")
    
    results = pipeline.generate_neuro_optimized_collection(
        quantity=5,
        mode="neuro_automated",
        direct_topics=["Student Financial Aid System", "Education Platform Analysis"]
    )
    
    print("\nPipeline Results:")
    print(json.dumps(results["summary"], indent=2))
    print(f"\nGenerated {results['summary']['content_generated']} content pieces")
    print(f"Average neural score: {results['summary']['average_neural_score']:.3f}")
