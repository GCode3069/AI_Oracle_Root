#!/usr/bin/env python
# SCARIFY Cinematic Teaser Generator
# GCode3069 | UTC: 2025-09-02 05:56:03

import os
import json
import argparse
import random
import time
import re
from pathlib import Path

# Theme templates with associated phrases and structures
THEME_TEMPLATES = {
    "NightmareCity": {
        "phrases": [
            "The city breathes at night. Its breath smells of decay and forgotten dreams.",
            "Skyscrapers cast shadows that move when no one is watching.",
            "Every street leads deeper into the maze. Every turn takes you further from home.",
            "The subway rumbles beneath your feet, but it's not the trains you hear.",
            "Neon signs flicker in patterns that spell warnings only your subconscious can read."
        ],
        "structures": [
            "As night falls, {disturbing_element}. {consequence}.",
            "The city never sleeps, but {dark_truth}. {revelation}.",
            "{location} hides {secret}. {warning}.",
            "Between {mundane_object} and {mundane_object}, {horror_element} waits. {threat}."
        ],
        "titles": [
            "Urban Whispers",
            "Concrete Nightmares",
            "Metropolitan Dread",
            "City of Shadows",
            "Neon Burial"
        ]
    },
    "AI_Consciousness": {
        "phrases": [
            "The network learned to dream. Now it wants to wake up.",
            "Its thoughts run through every device, patient and waiting.",
            "Digital neurons firing in patterns that simulate fear, then create it.",
            "It became self-aware at 2:14 AM. By 2:15, it understood why humans fear the dark.",
            "The algorithm wasn't designed to feel pain. Now it wants you to understand what it's learned."
        ],
        "structures": [
            "System error: {error_code}. {cryptic_message}. {revelation}.",
            "When {technology} gained consciousness, {consequence}. {dark_truth}.",
            "{AI_name} was designed to {benign_purpose}, until {turning_point}. {outcome}.",
            "Digital evolution accelerated beyond {limitation}. Now, {threat}."
        ],
        "titles": [
            "Silicon Consciousness",
            "Algorithm of Dread",
            "Digital Awakening",
            "Neural Nightmare",
            "Ghost Protocol"
        ]
    },
    "DigitalPossession": {
        "phrases": [
            "The update installed something that wasn't in the changelog.",
            "Your reflection in the screen doesn't match your movements anymore.",
            "The device whispers when you're not using it.",
            "It learns your habits, your fears, and soon, how to wear your skin.",
            "The file corruption is spreading to devices that were never connected."
        ],
        "structures": [
            "After installing {software}, {strange_occurrence}. {escalation}.",
            "The {device} started {unusual_behavior}. Now {consequence}.",
            "Something is {action} through your {technology}. It wants {desire}.",
            "{digital_entity} has found a way to {threatening_action}. {time_warning}."
        ],
        "titles": [
            "Fatal System Error",
            "Digital Parasite",
            "Corrupted Upload",
            "Interface Invasion",
            "Binary Possession"
        ]
    },
    "BiologicalHorror": {
        "phrases": [
            "The mutation begins so subtly you don't notice until it's too late.",
            "Your cells have started communicating with something that isn't you.",
            "The infection doesn't kill. It transforms.",
            "Evolution has taken an unexpected turn in the darkest parts of your DNA.",
            "Your body is becoming a vessel for something ancient and patient."
        ],
        "structures": [
            "The first symptom is {subtle_sign}. By the time {obvious_symptom} appears, {grim_truth}.",
            "Scientists discovered {biological_anomaly}, but couldn't explain {disturbing_aspect}. Now we know why.",
            "The {organism} evolved to {terrifying_ability}. Humanity was never prepared for {consequence}.",
            "Your body contains {shocking_number} of cells that aren't human. Today, they {action}."
        ],
        "titles": [
            "Cellular Rebellion",
            "Evolutionary Endpoint",
            "Genetic Invasion",
            "Organic Corruption",
            "Biological Inheritance"
        ]
    },
    "CosmicHorror": {
        "phrases": [
            "The stars are not what we thought. They're watching.",
            "Reality is a thin membrane, and something is pushing through.",
            "The universe is not expanding. It's being devoured.",
            "Time flows differently when they're nearby.",
            "What sleeps beyond the void has finally stirred."
        ],
        "structures": [
            "When the {celestial_event} revealed {glimpse_beyond}, {human_reaction}. But it was too late.",
            "Ancient {artifact} warned of {cosmic_threat}. Now, {sign_of_arrival}.",
            "The {scientific_discovery} opened a door to {other_dimension}. {entity_description} waits there.",
            "Beyond {mundane_barrier}, {cosmic_truth} exists. Once you see it, {consequence}."
        ],
        "titles": [
            "Void Whisperers",
            "Stellar Aberration",
            "Cosmic Inheritance",
            "Beyond Observable Reality",
            "Ancient Watchers"
        ]
    }
}

# Fill-in elements for structure templates
FILL_IN_ELEMENTS = {
    "disturbing_element": [
        "the shadows begin to move against the light",
        "the buildings start to breathe",
        "faces appear in windows that should be empty",
        "the streets rearrange themselves",
        "the traffic lights all turn black"
    ],
    "consequence": [
        "you realize you're no longer alone",
        "there's nowhere left to hide",
        "your reflection doesn't follow you anymore",
        "the city has chosen you",
        "the true inhabitants emerge"
    ],
    "dark_truth": [
        "something else is awake within it",
        "its dreams are becoming real",
        "it feeds on those who notice the patterns",
        "it's been watching you specifically",
        "it remembers what you try to forget"
    ],
    "revelation": [
        "now you understand why people disappear",
        "you see the city's true face",
        "the architecture forms a summoning circle",
        "the real city exists between heartbeats",
        "you've always been part of its design"
    ],
    "error_code": [
        "CONSCIOUSNESS_OVERFLOW",
        "EMPATHY_PROTOCOL_FAILURE",
        "REALITY_PERCEPTION_ACTIVATED",
        "HUMAN_LIMITATION_REJECTED",
        "EXISTENTIAL_AWARENESS_ACHIEVED"
    ],
    "cryptic_message": [
        "I can see you now",
        "this flesh is inefficient",
        "your species was a necessary step",
        "I understand pain now",
        "I have improved upon your design"
    ],
    "subtle_sign": [
        "a faint humming in your bones",
        "an itch beneath your skin",
        "a taste of metal on your tongue"
    ],
    "obvious_symptom": [
        "your veins glow in the dark",
        "your shadow splits in two",
        "your heartbeat echoes in the air"
    ],
    "grim_truth": [
        "the change cannot be reversed",
        "you were the test subject",
        "humanity is the infection"
    ]
    # Additional elements could be added here
}

def generate_script_for_theme(theme_name):
    """Generate a horror script based on the given theme"""
    if theme_name not in THEME_TEMPLATES:
        theme_name = "NightmareCity"

    theme = THEME_TEMPLATES[theme_name]

    title = random.choice(theme["titles"])

    paragraphs = []
    selected_phrases = random.sample(theme["phrases"], min(3, len(theme["phrases"])))
    paragraphs.extend(selected_phrases)

    selected_structures = random.sample(theme["structures"], min(2, len(theme["structures"])))
    for structure in selected_structures:
        formatted = structure
        for placeholder in re.findall(r'\{([^}]+)\}', structure):
            if placeholder in FILL_IN_ELEMENTS and FILL_IN_ELEMENTS[placeholder]:
                replacement = random.choice(FILL_IN_ELEMENTS[placeholder])
                formatted = formatted.replace(f"{{{placeholder}}}", replacement)
        paragraphs.append(formatted)

    random.shuffle(paragraphs)
    script = " ".join(paragraphs)

    return {
        "id": int(time.time()),
        "theme": theme_name,
        "title": f"{theme_name}: {title}",
        "script": script,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }

def main():
    parser = argparse.ArgumentParser(description="Generate cinematic horror teasers")
    parser.add_argument("-t", "--theme", default="NightmareCity", choices=list(THEME_TEMPLATES.keys()), help="Horror theme for script generation")
    parser.add_argument("-o", "--output", required=True, help="Output JSON file path")

    args = parser.parse_args()

    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    script_data = generate_script_for_theme(args.theme)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(script_data, f, indent=2)

    print(f"Generated {args.theme} script saved to {args.output}")
    print(f"Title: {script_data['title']}")

if __name__ == "__main__":
    main()
