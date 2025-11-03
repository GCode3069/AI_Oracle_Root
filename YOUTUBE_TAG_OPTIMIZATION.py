#!/usr/bin/env python3
"""
YOUTUBE_TAG_OPTIMIZATION.py - Scientific tag optimization for maximum reach

Tags are SUPER IMPORTANT for:
1. Search discovery (80% of views)
2. Suggested videos sidebar
3. Algorithm categorization
4. Recommended feed placement

Research-based tag strategy for Lincoln videos.
"""

import random
from typing import List

# ============================================================================
# TAG SCIENCE: What Actually Works on YouTube
# ============================================================================

"""
TAG EFFECTIVENESS RESEARCH:

1. QUANTITY: 15-30 tags optimal (not max 500 characters, but 15-30 distinct)
2. SPECIFICITY MIX: 30% broad + 40% medium + 30% niche
3. COMPETITION: Mix high-volume (competitive) + low-volume (easy rank)
4. RELEVANCE: Must match content (algorithm detects spam)
5. TRENDING: 20-30% trending tags boost initial push
6. LONG-TAIL: Multi-word phrases (less competition)

PRIORITY ORDER:
1. Primary keywords (what video is about)
2. Trending topics (current events)
3. Channel branding (lincoln, max headroom, horror)
4. Audience intent (scary, viral, exposed)
5. Platform tags (#shorts, #viral)
"""

# ============================================================================
# OPTIMIZED TAG CATEGORIES
# ============================================================================

TAG_SYSTEM = {
    # PRIMARY (Always include - defines content)
    'primary': [
        'abraham lincoln',
        'lincoln horror',
        'max headroom',
        'political satire',
        'dark comedy',
        'glitch aesthetic'
    ],
    
    # TRENDING (Rotate based on headlines)
    'trending': {
        'government': ['government shutdown', 'congress', 'senate', 'politics 2025', 'trump', 'biden'],
        'economy': ['market crash', 'recession', 'inflation', 'economy', 'stock market', 'bitcoin'],
        'tech': ['ai', 'artificial intelligence', 'tech layoffs', 'big tech', 'surveillance', 'privacy'],
        'social': ['social media', 'tiktok', 'instagram', 'algorithm', 'viral', 'trending'],
        'health': ['healthcare', 'insurance', 'pharma', 'medical', 'covid', 'vaccine'],
        'climate': ['climate change', 'environment', 'pollution', 'global warming', 'green energy'],
        'war': ['ukraine', 'israel', 'military', 'defense', 'war', 'conflict'],
        'crypto': ['cryptocurrency', 'blockchain', 'nft', 'web3', 'defi']
    },
    
    # AUDIENCE INTENT (What viewers search for)
    'intent': [
        'scary',
        'creepy',
        'horror',
        'exposed',
        'truth',
        'revealed',
        'warning',
        'shocking',
        'conspiracy',
        'wake up'
    ],
    
    # PLATFORM SPECIFIC (Algorithm triggers)
    'platform': [
        'shorts',
        'youtube shorts',
        'viral shorts',
        'trending',
        'fyp',
        'for you'
    ],
    
    # LONG-TAIL (Low competition, high conversion)
    'long_tail': [
        'abraham lincoln ghost',
        'max headroom style video',
        'glitchy tv broadcast',
        'political horror satire',
        'dark comedy news',
        'scary lincoln',
        'haunted presidential',
        'vhs horror aesthetic'
    ],
    
    # ENGAGEMENT (Emotional hooks)
    'emotional': [
        'mind blowing',
        'cant unsee',
        'disturbing',
        'uncomfortable truth',
        'reality check',
        'wake up call'
    ]
}

def generate_optimized_tags(headline: str, script: str, video_type='short') -> List[str]:
    """
    Generate 20-25 optimized tags for maximum discoverability
    
    Args:
        headline: News headline
        script: Video script
        video_type: 'short' or 'long'
    
    Returns:
        List of 20-25 optimized tags
    """
    
    tags = []
    
    # Step 1: PRIMARY (all videos get these)
    tags.extend(TAG_SYSTEM['primary'])
    
    # Step 2: TRENDING (match to headline topic)
    hl = headline.lower()
    
    for topic, trend_tags in TAG_SYSTEM['trending'].items():
        if any(word in hl for word in topic.split()):
            tags.extend(random.sample(trend_tags, min(3, len(trend_tags))))
            break
    
    # If no match, use general trending
    if len(tags) == len(TAG_SYSTEM['primary']):
        tags.extend(random.sample(TAG_SYSTEM['trending']['government'], 2))
    
    # Step 3: AUDIENCE INTENT (2-3 tags)
    tags.extend(random.sample(TAG_SYSTEM['intent'], 3))
    
    # Step 4: PLATFORM SPECIFIC (critical for Shorts)
    if video_type == 'short':
        tags.extend(TAG_SYSTEM['platform'][:4])
    else:
        tags.extend(TAG_SYSTEM['platform'][:2])
    
    # Step 5: LONG-TAIL (2-3 low-competition phrases)
    tags.extend(random.sample(TAG_SYSTEM['long_tail'], 3))
    
    # Step 6: EMOTIONAL (1-2 engagement hooks)
    tags.extend(random.sample(TAG_SYSTEM['emotional'], 2))
    
    # Step 7: Extract keywords from headline
    headline_words = headline.lower().split()
    important_words = [w for w in headline_words if len(w) > 4 and w not in ['that', 'with', 'from', 'this']]
    tags.extend(important_words[:3])
    
    # Remove duplicates while preserving order
    seen = set()
    unique_tags = []
    for tag in tags:
        tag_lower = tag.lower()
        if tag_lower not in seen:
            seen.add(tag_lower)
            unique_tags.append(tag)
    
    # Limit to 25 tags (optimal)
    return unique_tags[:25]

def format_tags_for_youtube(tags: List[str]) -> str:
    """Format tags for YouTube API"""
    return ','.join(tags)

def format_tags_for_display(tags: List[str]) -> str:
    """Format tags for display/documentation"""
    return ', '.join(f'#{tag.replace(" ", "")}' for tag in tags)

# ============================================================================
# TAG EFFECTIVENESS SCORING
# ============================================================================

def score_tag_quality(tags: List[str]) -> dict:
    """
    Score tag quality based on research
    
    Returns metrics:
    - Quantity score (15-25 is optimal)
    - Diversity score (different categories)
    - Competition score (mix of broad/niche)
    - Trending score (current relevance)
    """
    
    quantity_score = min(len(tags) / 20.0, 1.0) * 100  # Optimal is 20
    
    # Check diversity (how many categories represented)
    categories_present = 0
    if any(tag in TAG_SYSTEM['primary'] for tag in tags):
        categories_present += 1
    if any(tag in TAG_SYSTEM['intent'] for tag in tags):
        categories_present += 1
    if any(tag in TAG_SYSTEM['platform'] for tag in tags):
        categories_present += 1
    if any(tag in TAG_SYSTEM['long_tail'] for tag in tags):
        categories_present += 1
    
    diversity_score = (categories_present / 4.0) * 100
    
    # Long-tail score (multi-word tags = less competition)
    long_tail_count = sum(1 for tag in tags if ' ' in tag)
    long_tail_score = min(long_tail_count / 5.0, 1.0) * 100
    
    return {
        'quantity': quantity_score,
        'diversity': diversity_score,
        'long_tail': long_tail_score,
        'overall': (quantity_score + diversity_score + long_tail_score) / 3
    }

if __name__ == "__main__":
    print("\n" + "="*70)
    print("  YOUTUBE TAG OPTIMIZATION - RESEARCH-BASED")
    print("="*70 + "\n")
    
    # Test tag generation
    test_headline = "Government Shutdown Day 15"
    test_script = "Government shutdown continues..."
    
    tags = generate_optimized_tags(test_headline, test_script, 'short')
    score = score_tag_quality(tags)
    
    print(f"HEADLINE: {test_headline}\n")
    print(f"GENERATED TAGS ({len(tags)}):")
    for i, tag in enumerate(tags, 1):
        print(f"  {i:2d}. {tag}")
    
    print(f"\nFORMATTED FOR YOUTUBE:")
    print(f"  {format_tags_for_youtube(tags[:50])[:100]}...")
    
    print(f"\nFORMATTED FOR DESCRIPTION:")
    print(f"  {format_tags_for_display(tags)[:100]}...")
    
    print(f"\nQUALITY SCORE:")
    print(f"  Quantity: {score['quantity']:.1f}%")
    print(f"  Diversity: {score['diversity']:.1f}%")
    print(f"  Long-tail: {score['long_tail']:.1f}%")
    print(f"  OVERALL: {score['overall']:.1f}%")
    
    if score['overall'] >= 80:
        print(f"\n  ✅ EXCELLENT tag optimization!")
    elif score['overall'] >= 60:
        print(f"\n  ⚠️ GOOD but can improve")
    else:
        print(f"\n  ❌ NEEDS WORK")
    
    print("\n" + "="*70)
    print("TAG IMPORTANCE:")
    print("="*70)
    print("""
1. SEARCH: 80% of YouTube views come from search
   - Tags help videos appear in search results
   - More tags = more search queries matched

2. SUGGESTED: Sidebar recommendations
   - Tags tell algorithm which videos are similar
   - Appear next to viral videos with same tags

3. CATEGORIZATION: Algorithm understanding
   - Tags help YouTube understand content
   - Better recommendations to right audience

4. BROWSE FEATURES: Home feed, trending
   - Tags influence home feed placement
   - Trending tags boost initial push

OPTIMAL STRATEGY:
- 20-25 tags (not 3-5, not 50+)
- Mix broad + niche
- Include trending topics
- Add long-tail phrases
- Update based on performance

TAGS ARE SUPER IMPORTANT! ⭐⭐⭐⭐⭐
""")


