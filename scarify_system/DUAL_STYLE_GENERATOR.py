"""
DUAL_STYLE_GENERATOR.py
Generates video concepts with 70% WARNING and 30% comedy format split.
"""

import random
from typing import Dict, Literal

# WARNING format templates (70% probability)
WARNING_TEMPLATES = [
    {
        "category": "Education",
        "templates": [
            {
                "title": "WARNING: Your School Is Teaching This",
                "hook": "They don't want you to know what's really in the curriculum...",
                "structure": "reveal -> expose system -> call to awareness"
            },
            {
                "title": "URGENT: What They're Not Teaching Your Kids",
                "hook": "The education system is hiding something crucial from students...",
                "structure": "question -> reveal truth -> demand change"
            },
            {
                "title": "ALERT: This Is What Schools Are Actually Doing",
                "hook": "Behind closed doors, education has changed dramatically...",
                "structure": "observation -> investigation -> shocking revelation"
            },
            {
                "title": "WARNING: The Real Purpose of Modern Education",
                "hook": "Lincoln would be horrified by what schools have become...",
                "structure": "historical comparison -> modern reality -> wake-up call"
            },
            {
                "title": "CRITICAL: What Every Parent Must Know Now",
                "hook": "Your child's future depends on understanding this truth...",
                "structure": "urgent warning -> documented evidence -> protective action"
            }
        ]
    },
    {
        "category": "Military",
        "templates": [
            {
                "title": "WARNING: What the Military Isn't Telling You",
                "hook": "Classified information is finally coming to light...",
                "structure": "declassification -> exposure -> implications"
            },
            {
                "title": "URGENT: The Truth About Military Spending",
                "hook": "Billions are disappearing into black budget projects...",
                "structure": "follow the money -> reveal programs -> demand accountability"
            },
            {
                "title": "ALERT: Military Technology You're Not Supposed to Know",
                "hook": "Advanced weapons systems are decades ahead of public knowledge...",
                "structure": "leak -> verification -> future implications"
            },
            {
                "title": "WARNING: Veterans Are Speaking Out",
                "hook": "Those who served are breaking their silence about what they witnessed...",
                "structure": "testimony -> pattern recognition -> call for transparency"
            },
            {
                "title": "CRITICAL: The Military Industrial Complex Today",
                "hook": "Eisenhower's warning has become our reality...",
                "structure": "prophecy -> current state -> wake-up moment"
            }
        ]
    },
    {
        "category": "Government",
        "templates": [
            {
                "title": "WARNING: What Congress Just Passed",
                "hook": "A new law slipped through while everyone was distracted...",
                "structure": "legislation reveal -> impact analysis -> action needed"
            },
            {
                "title": "URGENT: Your Rights Are Being Quietly Removed",
                "hook": "Constitutional protections are eroding faster than ever...",
                "structure": "document changes -> show pattern -> defend freedoms"
            },
            {
                "title": "ALERT: Government Surveillance Has Reached This Level",
                "hook": "The extent of monitoring would shock the Founding Fathers...",
                "structure": "reveal capability -> show scope -> privacy implications"
            },
            {
                "title": "WARNING: They're Rewriting History Right Now",
                "hook": "Official narratives are changing to control the future...",
                "structure": "compare versions -> show manipulation -> preserve truth"
            },
            {
                "title": "CRITICAL: What Politicians Don't Want Exposed",
                "hook": "Documents prove what they've been denying for years...",
                "structure": "leak -> verification -> demand accountability"
            }
        ]
    },
    {
        "category": "Economy",
        "templates": [
            {
                "title": "WARNING: Your Money Is About to Change Forever",
                "hook": "Central banks are rolling out a new system that eliminates cash...",
                "structure": "reveal plan -> show timeline -> protect yourself"
            },
            {
                "title": "URGENT: The Real Inflation Numbers They're Hiding",
                "hook": "Official statistics are deliberately misleading the public...",
                "structure": "official numbers -> real calculations -> survival strategies"
            },
            {
                "title": "ALERT: Banks Are Preparing for Something Big",
                "hook": "Insider movements suggest they know what's coming...",
                "structure": "track behavior -> decode signals -> prepare now"
            },
            {
                "title": "WARNING: The Dollar's Final Days",
                "hook": "Global reserve currency status is ending faster than reported...",
                "structure": "show indicators -> timeline -> alternative assets"
            },
            {
                "title": "CRITICAL: Economic Collapse Signs Everyone Missed",
                "hook": "The warning signals are flashing red across all sectors...",
                "structure": "list indicators -> connect dots -> emergency preparation"
            }
        ]
    }
]

# COMEDY format templates (30% probability)
COMEDY_TEMPLATES = [
    {
        "title": "Abe Lincoln Watches TikTok Dances",
        "hook": "Four score and seven... wait, what are they doing with their hands?",
        "structure": "confusion -> commentary -> hilarious observations"
    },
    {
        "title": "If Lincoln Had to Deal With WiFi",
        "hook": "I freed the slaves, but I can't free myself from this loading screen...",
        "structure": "modern frustration -> historical perspective -> comedic contrast"
    },
    {
        "title": "Abe Reviews Modern Dating Apps",
        "hook": "You're telling me people court each other by swiping left and right?",
        "structure": "discover app -> react to profiles -> old-timey wisdom"
    },
    {
        "title": "Lincoln Tries to Order Starbucks",
        "hook": "Just give me a coffee. No, I don't want it pumpkin-spiced!",
        "structure": "simple order -> menu confusion -> comedic escalation"
    },
    {
        "title": "When Abe Discovers Social Media Drama",
        "hook": "I survived a civil war, but Twitter arguments are something else...",
        "structure": "scroll through drama -> react -> sage advice delivered funny"
    }
]

# Topic weights for WARNING format
TOPIC_WEIGHTS = {
    "Education": 0.30,
    "Military": 0.30,
    "Government": 0.20,
    "Economy": 0.20
}


def weighted_random_choice(weights: Dict[str, float]) -> str:
    """Select a random key based on weighted probabilities."""
    topics = list(weights.keys())
    probabilities = list(weights.values())
    return random.choices(topics, weights=probabilities, k=1)[0]


def generate_warning_concept() -> Dict:
    """Generate a WARNING format video concept."""
    # Select category based on weights
    category = weighted_random_choice(TOPIC_WEIGHTS)
    
    # Find matching category in templates
    category_data = next(c for c in WARNING_TEMPLATES if c["category"] == category)
    
    # Select random template from category
    template = random.choice(category_data["templates"])
    
    # Generate script based on structure
    script_parts = template["structure"].split(" -> ")
    script = f"{template['hook']}\n\n"
    script += "Listen closely, because what I'm about to tell you changes everything.\n\n"
    
    # Add structure-based content
    for i, part in enumerate(script_parts, 1):
        if i == len(script_parts):
            script += f"This is the truth they don't want you to know. Wake up, America."
        else:
            script += f"[{part.upper()}]\n\n"
    
    return {
        "style": "WARNING",
        "category": category,
        "topic": template["title"],
        "title": template["title"],
        "hook": template["hook"],
        "structure": template["structure"],
        "script": script,
        "duration_target": random.randint(25, 45)
    }


def generate_comedy_concept() -> Dict:
    """Generate a COMEDY format video concept."""
    template = random.choice(COMEDY_TEMPLATES)
    
    # Generate comedic script
    script = f"{template['hook']}\n\n"
    script += "Now, I've seen a lot in my time, but this right here...\n\n"
    script += "[COMEDIC OBSERVATION]\n\n"
    script += "Back in my day, things were different. And by different, I mean actually sensible.\n\n"
    script += "[PUNCHLINE]\n\n"
    script += "Y'all need help. Seriously."
    
    return {
        "style": "COMEDY",
        "category": "Entertainment",
        "topic": template["title"],
        "title": template["title"],
        "hook": template["hook"],
        "structure": template["structure"],
        "script": script,
        "duration_target": random.randint(25, 35)
    }


def generate_video_concept(force_style: Literal["WARNING", "COMEDY", None] = None) -> Dict:
    """
    Generate a complete video concept with proper 70/30 split.
    
    Args:
        force_style: Optional style override for testing
        
    Returns:
        Dict with keys: style, category, topic, title, hook, structure, script, duration_target
    """
    # Determine style based on 70/30 split
    if force_style:
        style = force_style
    else:
        style = random.choices(["WARNING", "COMEDY"], weights=[0.70, 0.30], k=1)[0]
    
    # Generate appropriate concept
    if style == "WARNING":
        return generate_warning_concept()
    else:
        return generate_comedy_concept()


def generate_batch_concepts(count: int) -> list[Dict]:
    """
    Generate multiple concepts ensuring proper 70/30 distribution.
    
    Args:
        count: Number of concepts to generate
        
    Returns:
        List of concept dictionaries
    """
    concepts = []
    
    # Calculate exact split
    warning_count = int(count * 0.70)
    comedy_count = count - warning_count
    
    # Generate WARNING concepts
    for _ in range(warning_count):
        concepts.append(generate_warning_concept())
    
    # Generate COMEDY concepts
    for _ in range(comedy_count):
        concepts.append(generate_comedy_concept())
    
    # Shuffle to randomize order
    random.shuffle(concepts)
    
    return concepts


def get_style_distribution(concepts: list[Dict]) -> Dict[str, float]:
    """Calculate the actual style distribution in a list of concepts."""
    if not concepts:
        return {}
    
    warning_count = sum(1 for c in concepts if c["style"] == "WARNING")
    comedy_count = len(concepts) - warning_count
    
    return {
        "WARNING": warning_count / len(concepts),
        "COMEDY": comedy_count / len(concepts),
        "total": len(concepts)
    }


if __name__ == "__main__":
    print("=== SCARIFY Dual Style Generator ===\n")
    
    # Test single generation
    print("Generating single concept:")
    concept = generate_video_concept()
    print(f"Style: {concept['style']}")
    print(f"Category: {concept['category']}")
    print(f"Title: {concept['title']}")
    print(f"Hook: {concept['hook']}")
    print(f"Duration Target: {concept['duration_target']}s")
    print(f"\nScript Preview:\n{concept['script'][:200]}...")
    
    # Test batch generation
    print("\n\n=== Testing Batch Generation (100 concepts) ===")
    batch = generate_batch_concepts(100)
    distribution = get_style_distribution(batch)
    print(f"WARNING: {distribution['WARNING']:.1%}")
    print(f"COMEDY: {distribution['COMEDY']:.1%}")
    print(f"Total: {int(distribution['total'])} concepts")
    
    # Show category breakdown for WARNING
    warning_concepts = [c for c in batch if c['style'] == 'WARNING']
    category_counts = {}
    for concept in warning_concepts:
        cat = concept['category']
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    print("\nWARNING Category Distribution:")
    for cat, count in category_counts.items():
        percentage = (count / len(warning_concepts)) * 100
        print(f"  {cat}: {percentage:.1f}%")
