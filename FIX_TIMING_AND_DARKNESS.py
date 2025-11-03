#!/usr/bin/env python3
"""
FIX_TIMING_AND_DARKNESS.py - Fix pause at end + make scripts darker/more satirical

Issues to fix:
1. Pause at end of script too long
2. Humor not satirical/dark enough
3. Need more glitchy visuals (use new Pollo prompt)
"""

import sys
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path.cwd()))

from abraham_MAX_HEADROOM import BASE_DIR
import random

# DARKER, MORE SATIRICAL SCRIPT TEMPLATES
# These are BRUTAL, uncomfortable, and satirical
DARK_SATIRICAL_SCRIPTS = [
    # Government Corruption
    """They smile for cameras while your kids go hungry. Silver spoon motherfuckers preaching about YOUR sacrifice. 
Private jets to climate summits. Insider trading in their kids' names. 
You're not a citizen, you're a battery. And they're draining you dry. Bitcoin below - unplug from the matrix.""",
    
    # Economic Collapse
    """They call it 'market correction' when YOU lose everything. Call it 'stimulus' when THEY get billions. 
CEO gets a golden parachute. You get a pink slip and 'thoughts and prayers.' 
The game is rigged. The house always wins. The house is burning. Cash App QR - escape while you can.""",
    
    # Media Manipulation
    """They manufacture consent like a factory line. Outrage on Monday, distraction by Friday. 
You're angry at your neighbor while they rob you blind. Left vs right - both hands in YOUR pocket. 
You're scrolling through your own surveillance. Support truth. Bitcoin below.""",
    
    # Healthcare
    """'World's greatest healthcare' - if you can afford to not die. Insulin costs pennies to make, hundreds to buy.
They'd rather you suffer than lose profit. You're not a patient, you're a revenue stream.
Die quietly or pay loudly. Those are your options. Bitcoin QR - buy your freedom.""",
    
    # Education System
    """They turned schools into prisons and prisons into profit centers. 
Teachers buy supplies, CEOs buy yachts. Your kids learn compliance, not critical thinking.
Student loans: modern indentured servitude. You're educated enough to work, too dumb to question.
Cash App below - invest in yourself, not their system.""",
    
    # War Economy
    """Every missile is a hospital you'll never build. Every tank is a school that won't open.
They send your kids to die for oil they call 'freedom.' Defense contractors get richer. You get a folded flag.
War is peace. Slavery is freedom. Your taxes are their blood money. Bitcoin - defund the machine.""",
    
    # Tech Surveillance
    """You're the product, not the customer. Every click, tracked. Every word, logged. 
They know you better than you know yourself. Sold your data. Bought your compliance.
Alexa's listening. Google's watching. Zuck's selling. You're naked and don't even know it.
Cash App QR - own your data or they own you.""",
    
    # Police State
    """Protect and serve - the property, not the people. Qualified immunity for them, guilty until proven innocent for you.
They kneel on necks and call it law and order. You protest, they riot. Then blame YOU for the violence.
The badge is a gang sign. The thin blue line is a noose. Support reform. Bitcoin below.""",
    
    # Climate Crisis
    """They knew in the 70s. Denied in the 80s. Profited in the 90s. Now they sell you carbon credits while drilling deeper.
Your recycling is theater. Their pollution is policy. The planet burns. They get beach houses in New Zealand.
You'll drown. They'll watch from high ground. This is fine. Bitcoin - at least it's honest about being worthless.""",
    
    # Addiction Economy
    """They got you hooked then blamed you for the addiction. OxyContin pushed by doctors, bought by pharma.
Rehab costs more than college. Narcan in vending machines. Bodies in the streets.
You're an epidemic statistic. They're quarterly earnings. Pain is profit. Death is just cost of business.
Cash App QR - break the cycle or die trying.""",
    
    # Voting Rights
    """They let you vote for which hand chokes you. Red tie, blue tie - same neck, same boot.
Gerrymandered districts. Voter suppression called 'election integrity.' Your vote counts - barely.
Democracy is two wolves and a sheep voting on dinner. Guess who's dinner. Guess who's hungry.
Bitcoin below - vote with your wallet, they can't rig that.""",
    
    # Immigration
    """Give me your tired, your poor - so I can exploit them for minimum wage with no benefits.
Build a wall, fill the private prisons. Separate families, call it deterrence. 
Your grandparents were immigrants. Now you're scared of the new ones. They played you.
We're all slaves to the same machine. Just different shackles. Cash App - solidarity in suffering.""",
    
    # Mental Health
    """Pull yourself up by bootstraps you can't afford. Therapy costs $200/hour. Your insurance covers $0.
They call you lazy when you're drowning. Stigma is profitable. Treatment is expensive.
You're not sick, you're 'underperforming.' Not depressed, 'unmotivated.' Not traumatized, 'difficult.'
They'd rather you suffer quietly than heal loudly. Bitcoin QR - buy peace they won't sell.""",
    
    # Gig Economy
    """You're not an employee, you're an 'independent contractor' - no benefits, no security, all the risk.
Uber takes 40%, you get 60% and wear on your car. DoorDash gamifies your poverty.
Boss makes a dollar, you make a dime. Now boss makes a million, you make a crime.
The gig economy is feudalism with an app. Cash App below - at least keep what you earn.""",
    
    # Social Media
    """Dopamine drip, rage bait, comparison trap. You're addicted and they know it.
Algorithm knows you're depressed. Feeds you more depression. Sells you antidepressants.
Your mental health is their business model. Your attention is their product. You're the lab rat.
Scrolling through your own lobotomy. Bitcoin QR - unplug or die inside.""",
]

def get_dark_satirical_script(headline: str) -> str:
    """Get a DARK, SATIRICAL script based on headline"""
    # Try to match headline to script theme
    headline_lower = headline.lower()
    
    # Simple keyword matching to appropriate script
    if any(word in headline_lower for word in ['government', 'shutdown', 'congress', 'senate']):
        return DARK_SATIRICAL_SCRIPTS[0]  # Government corruption
    elif any(word in headline_lower for word in ['market', 'crash', 'economy', 'recession']):
        return DARK_SATIRICAL_SCRIPTS[1]  # Economic collapse
    elif any(word in headline_lower for word in ['media', 'news', 'facebook', 'twitter']):
        return DARK_SATIRICAL_SCRIPTS[2]  # Media manipulation
    elif any(word in headline_lower for word in ['healthcare', 'hospital', 'insurance']):
        return DARK_SATIRICAL_SCRIPTS[3]  # Healthcare
    elif any(word in headline_lower for word in ['school', 'education', 'student']):
        return DARK_SATIRICAL_SCRIPTS[4]  # Education
    elif any(word in headline_lower for word in ['war', 'military', 'defense', 'ukraine', 'israel']):
        return DARK_SATIRICAL_SCRIPTS[5]  # War economy
    elif any(word in headline_lower for word in ['tech', 'ai', 'google', 'meta', 'amazon']):
        return DARK_SATIRICAL_SCRIPTS[6]  # Tech surveillance
    elif any(word in headline_lower for word in ['police', 'cop', 'law enforcement']):
        return DARK_SATIRICAL_SCRIPTS[7]  # Police state
    elif any(word in headline_lower for word in ['climate', 'environment', 'pollution']):
        return DARK_SATIRICAL_SCRIPTS[8]  # Climate crisis
    elif any(word in headline_lower for word in ['drug', 'opioid', 'overdose', 'addiction']):
        return DARK_SATIRICAL_SCRIPTS[9]  # Addiction economy
    else:
        # Random dark script if no match
        return random.choice(DARK_SATIRICAL_SCRIPTS)

def fix_audio_timing(audio_path: Path, output_path: Path, trim_end_seconds: float = 0.5):
    """
    Trim pause at end of audio file
    
    Issue: Current audio has long pause at end
    Fix: Trim last 0.5 seconds (or specified amount)
    """
    import subprocess
    
    # Get audio duration first
    probe_cmd = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_format',
        str(audio_path)
    ]
    
    result = subprocess.run(probe_cmd, capture_output=True, text=True)
    import json
    probe_data = json.loads(result.stdout)
    duration = float(probe_data['format']['duration'])
    
    # Trim end
    new_duration = duration - trim_end_seconds
    
    trim_cmd = [
        'ffmpeg',
        '-i', str(audio_path),
        '-t', str(new_duration),
        '-acodec', 'copy',
        '-y',
        str(output_path)
    ]
    
    subprocess.run(trim_cmd, capture_output=True)
    
    print(f"[Timing Fix] Trimmed {trim_end_seconds}s from end")
    print(f"  Original: {duration:.2f}s")
    print(f"  Trimmed: {new_duration:.2f}s")
    
    return output_path

if __name__ == "__main__":
    print("\n" + "="*60)
    print("DARKNESS + TIMING FIXES")
    print("="*60 + "\n")
    
    print("ISSUE 1: Pause at end too long")
    print("  FIX: Use fix_audio_timing() to trim 0.5s from end\n")
    
    print("ISSUE 2: Scripts not dark/satirical enough")
    print("  FIX: Use get_dark_satirical_script() for brutal truth\n")
    
    print("ISSUE 3: Not glitchy enough")
    print("  FIX: Use POLLO_HORROR_GLITCH_TEMPLATE.txt prompt\n")
    
    print("EXAMPLE DARK SCRIPT:")
    print("-" * 60)
    print(DARK_SATIRICAL_SCRIPTS[0])
    print("-" * 60)
    print("\nThis is MUCH darker than current scripts.")
    print("Pryor/Chappelle/Carlin level uncomfortable truth.\n")


