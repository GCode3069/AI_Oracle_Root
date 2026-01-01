#!/usr/bin/env python3
"""
Test script for Advanced Content Optimization System
Verifies all modules are working correctly
"""

import json
import sys
from datetime import datetime

def test_module(module_name, test_func):
    """Test a module and report results."""
    try:
        print(f"\n{'='*60}")
        print(f"Testing {module_name}")
        print('='*60)
        result = test_func()
        print(f"✓ {module_name} test passed")
        return True
    except Exception as e:
        print(f"✗ {module_name} test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_analytics():
    """Test NEURO_PERFORMANCE_ANALYTICS."""
    from NEURO_PERFORMANCE_ANALYTICS import NeuroPerformanceAnalytics
    analytics = NeuroPerformanceAnalytics()
    
    sample_data = [
        {
            "title": "Education System Analysis",
            "views": 1236,
            "engagement_rate": 0.0273,
            "topic": "education system",
            "content_type": "analysis"
        }
    ]
    
    results = analytics.analyze_with_biometric_correlation(sample_data)
    assert results.get("status") != "error"
    print(f"  Analyzed {len(sample_data)} content items")
    return True

def test_optimization():
    """Test COGNITIVE_CONTENT_OPTIMIZATION."""
    from COGNITIVE_CONTENT_OPTIMIZATION import NeuroContentOptimization
    optimizer = NeuroContentOptimization()
    
    optimizer.add_direct_topic("Test Topic", priority=5)
    topics = optimizer.select_with_neural_prediction(max_topics=5)
    assert len(topics) > 0
    print(f"  Selected {len(topics)} topics")
    return True

def test_platform_content():
    """Test SOCIAL_NEURO_PLATFORM_CONTENT."""
    from SOCIAL_NEURO_PLATFORM_CONTENT import SocialNeuroPlatformContent
    platform_content = SocialNeuroPlatformContent()
    
    content = platform_content.develop_neuro_platform_content(
        "Test Platform Topic",
        content_type="platform_features"
    )
    assert "content" in content
    assert "neural_settings" in content
    print(f"  Generated platform content with {len(content['platforms'])} platforms")
    return True

def test_selector():
    """Test NEURAL_PERFORMANCE_SELECTOR."""
    from NEURAL_PERFORMANCE_SELECTOR import NeuralPerformanceSelector
    selector = NeuralPerformanceSelector()
    
    candidates = [
        {"topic": "Education System", "source": "test"}
    ]
    selected = selector.select_with_neural_data(candidates)
    assert len(selected) > 0
    print(f"  Selected {len(selected)} topics with neural scoring")
    return True

def test_development():
    """Test NEURO_ENHANCED_CONTENT_DEVELOPMENT."""
    from NEURO_ENHANCED_CONTENT_DEVELOPMENT import NeuroEnhancedContentDevelopment
    developer = NeuroEnhancedContentDevelopment()
    
    adaptations = developer.create_neuro_adaptations("Test Topic")
    assert "enhanced_version" in adaptations
    assert "standard_version" in adaptations
    print(f"  Created enhanced and standard versions")
    return True

def test_tracking():
    """Test NEURO_PERFORMANCE_TRACKING."""
    from NEURO_PERFORMANCE_TRACKING import NeuroPerformanceTracking
    tracker = NeuroPerformanceTracking()
    
    content_data = {
        "title": "Test Content",
        "topic": "test topic",
        "content_type": "test",
        "presentation_style": "thematic_presentation",
        "neural_settings": {"gamma_spikes": [8], "limbic_engagement": 0.7},
        "platforms": ["YouTube"]
    }
    
    log_entry = tracker.log_with_neural_correlation("TEST_001", content_data)
    assert log_entry.get("tracking_id") == "TEST_001"
    print(f"  Logged content with neural correlation")
    return True

def test_learning():
    """Test NEURAL_CONTINUOUS_LEARNING."""
    from NEURAL_CONTINUOUS_LEARNING import NeuralStrategyLearner
    learner = NeuralStrategyLearner()
    
    sample_tracking = [
        {
            "content": {"topic": "Test", "content_type": "test", "presentation_style": "test"},
            "neural_settings": {"gamma_spikes": [8], "limbic_engagement": 0.7},
            "performance": {"views": 100, "engagement_rate": 0.05}
        }
    ]
    
    result = learner.learn_from_neural_performance(sample_tracking)
    assert result.get("status") != "error"
    print(f"  Completed learning cycle")
    return True

def test_habituation():
    """Test NEURAL_HABITUATION_PREVENTION."""
    from NEURAL_HABITUATION_PREVENTION import NeuralHabituationPrevention
    prevention = NeuralHabituationPrevention()
    
    risk = prevention.check_habituation_risk(
        topic="Test Topic",
        content_type="test",
        presentation_style="test",
        neural_settings={"gamma_spikes": [8], "limbic_engagement": 0.7}
    )
    assert "habituation_risk" in risk
    print(f"  Assessed habituation risk: {risk['habituation_risk']}")
    return True

def test_pipeline():
    """Test COMPLETE_NEURO_CONTENT_PIPELINE."""
    from COMPLETE_NEURO_CONTENT_PIPELINE import CompleteNeuroContentPipeline
    pipeline = CompleteNeuroContentPipeline()
    
    status = pipeline.get_system_status()
    assert status.get("pipeline_active") == True
    print(f"  Pipeline initialized successfully")
    print(f"  Modules loaded: {sum(status['modules_loaded'].values())}/8")
    return True

def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("Advanced Content Optimization System - Test Suite")
    print("="*60)
    
    tests = [
        ("NEURO_PERFORMANCE_ANALYTICS", test_analytics),
        ("COGNITIVE_CONTENT_OPTIMIZATION", test_optimization),
        ("SOCIAL_NEURO_PLATFORM_CONTENT", test_platform_content),
        ("NEURAL_PERFORMANCE_SELECTOR", test_selector),
        ("NEURO_ENHANCED_CONTENT_DEVELOPMENT", test_development),
        ("NEURO_PERFORMANCE_TRACKING", test_tracking),
        ("NEURAL_CONTINUOUS_LEARNING", test_learning),
        ("NEURAL_HABITUATION_PREVENTION", test_habituation),
        ("COMPLETE_NEURO_CONTENT_PIPELINE", test_pipeline),
    ]
    
    results = []
    for module_name, test_func in tests:
        passed = test_module(module_name, test_func)
        results.append((module_name, passed))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for module_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {module_name}")
    
    print(f"\nTotal: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n🎉 All tests passed! System is ready to use.")
        return 0
    else:
        print(f"\n⚠️  {total_count - passed_count} test(s) failed. Please review.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
