# DUAL_STYLE_GENERATOR.py
import random

# Horror topics for WARNING style
HORROR_TOPICS = [
    "AI consciousness emergence",
    "Digital possession",
    "Social media addiction",
    "Surveillance society",
    "Memory manipulation",
    "Reality distortion",
    "Neural interface dangers",
    "Algorithmic control",
    "Identity theft evolution",
    "Technological singularity"
]

# Comedy topics for dark humor
COMEDY_TOPICS = [
    "Smart home rebellion",
    "Dating app disasters",
    "Self-driving car confusion",
    "Voice assistant misunderstandings",
    "Robot job interviews",
    "Virtual reality mishaps",
    "Cryptocurrency chaos",
    "Influencer fails",
    "AI art disasters",
    "Tech support nightmares"
]

def generate_video_concept():
    """Generate a random video concept with style and topic"""
    # 70% WARNING (horror), 30% COMEDY
    style = "WARNING" if random.random() < 0.7 else "COMEDY"
    
    if style == "WARNING":
        category = random.choice(HORROR_TOPICS)
        title = f"⚠️ WARNING: {category.upper()}"
    else:
        category = random.choice(COMEDY_TOPICS)
        title = f"😅 {category.title()}"
    
    return {
        'style': style,
        'category': category,
        'title': title
    }

def generate_script_text(concept):
    """Generate script text based on concept"""
    style = concept['style']
    category = concept['category']
    
    if style == "WARNING":
        scripts = [
            f"Listen carefully. What I'm about to tell you about {category} will change everything you thought you knew. "
            f"The signs are already here. You've seen them. You've felt them. But you didn't know what you were looking at. "
            f"Until now. This is not a drill. This is not entertainment. This is a warning.",
            
            f"They don't want you to know about {category}. But I'm going to tell you anyway. "
            f"Every day, it gets closer. Every day, the evidence becomes clearer. "
            f"You're running out of time to prepare. The question is: will you listen?",
            
            f"There's something happening with {category} that nobody is talking about. "
            f"The experts are silent. The media is complicit. But the truth can't stay hidden forever. "
            f"What you're about to hear will disturb you. It should disturb you. Because it's real."
        ]
    else:
        scripts = [
            f"So there I was, dealing with {category}, and let me tell you—it went EXACTLY as badly as you'd expect. "
            f"I mean, what could possibly go wrong, right? Everything. Everything could go wrong. And it did. "
            f"But hey, at least it's a good story now.",
            
            f"Nobody warned me about {category}. Nobody said, 'Hey, this is going to be a complete disaster.' "
            f"But that's fine. I'm fine. Everything is fine. Except it's absolutely not fine. "
            f"Let me explain why this is both hilarious and horrifying.",
            
            f"You know what's funny about {category}? Nothing. Nothing is funny about it. "
            f"But we're going to laugh anyway because if we don't laugh, we'll cry. "
            f"And crying doesn't get as many views. So buckle up for this mess."
        ]
    
    return random.choice(scripts)

if __name__ == "__main__":
    # Test the generator
    print("Testing DUAL_STYLE_GENERATOR\n")
    
    for i in range(5):
        concept = generate_video_concept()
        script = generate_script_text(concept)
        print(f"\n{i+1}. {concept['title']}")
        print(f"   Style: {concept['style']}")
        print(f"   Category: {concept['category']}")
        print(f"   Script: {script[:100]}...")
