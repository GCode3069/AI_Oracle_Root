#!/usr/bin/env python3
"""
MULTI-STYLE SCRIPT GENERATOR
Implements 4 competitive intelligence strategies in one system
Based on LLM Battle Royale analysis
"""

import random
from datetime import datetime

# ============================================================================
# SCRIPT STYLES - COMPETITIVE INTELLIGENCE
# ============================================================================

class ScriptStyleGenerator:
    """Generate scripts in different competitive styles"""
    
    def __init__(self):
        self.styles = {
            'cursor_consistent': self.cursor_style,
            'chatgpt_poetic': self.chatgpt_style,
            'grok_controversial': self.grok_style,
            'opus_sophisticated': self.opus_style
        }
    
    # ------------------------------------------------------------------------
    # CURSOR STYLE - Consistent, Safe, Formulaic (8-12% CTR)
    # ------------------------------------------------------------------------
    
    def cursor_style(self, headline):
        """Original Cursor formula - proven, safe, scalable"""
        templates = [
            f"Stop scrolling. {headline}? They're selling you fear while pocketing profit. Classic misdirection. Now you know what they didn't want you to see. Support truth. Bitcoin below.",
            
            f"Listen up. {headline}... another distraction from the real theft. While you panic, they're laughing to the bank. Wake up. Bitcoin below.",
            
            f"{headline}? Bread and circuses for the modern age. Keep you scared, keep you spending. That's the formula. See through it. Bitcoin below."
        ]
        return random.choice(templates)
    
    # ------------------------------------------------------------------------
    # MODERN COMEDY STYLE - Actually Funny (15-25% CTR)
    # ------------------------------------------------------------------------
    
    def chatgpt_style(self, headline):
        """Modern comedy approach - genuinely funny, not just edgy"""
        
        # Import new comedy generator for better humor
        try:
            from COMEDY_SCRIPTS_REWRITTEN import ModernComedyGenerator
            comedy_gen = ModernComedyGenerator()
            # Use variety of comedy styles
            styles = ['observational', 'absurdist', 'dry_wit', 'relatable', 'deadpan']
            chosen_style = random.choice(styles)
            script, _ = comedy_gen.generate(headline, chosen_style, word_limit=100)
            return script
        except:
            pass
        
        # Fallback to simpler funny approach
        topic = headline.split(':')[0] if ':' in headline else headline[:40]
        
        funny_templates = [
            f"""So {topic.lower()} is happening. Cool. Cool cool cool.
            
            Meanwhile I'm over here trying to figure out why my phone autocorrects "duck" but not actual curse words.
            
            Priorities, am I right?
            
            The world's ending but at least we're documenting it in 4K.
            
            Future archaeologists will be so confused.
            "They knew exactly what was happening and did... nothing?"
            "Yep, but check out these sick memes they made."
            
            Bitcoin below. It's like money but with more anxiety.""",
            
            f"""{topic}? In THIS economy?
            
            That's like announcing a swimming pool on the Titanic.
            
            "Great news everyone! The deck chairs are now ergonomic!"
            
            We're really good at solving the wrong problems.
            It's almost a talent at this point.
            
            I'd be impressed if I wasn't so disappointed.
            
            Bitcoin address below. At least it's honest about being volatile.""",
            
            f"""Breaking: {topic.lower()}.
            
            In related news, I still don't understand how planes stay up.
            
            You're telling me we put metal in the sky and it just... stays there?
            Based on MATH? Suspicious.
            
            But sure, let's worry about {topic.lower()}.
            Not the gravity-defying metal birds.
            
            Bitcoin below. Also defies logic but at least it stays on the ground."""
        ]
        
        return random.choice(funny_templates)
    
    # ------------------------------------------------------------------------
    # GROK STYLE - Controversial, Trend-Jacking (10-25% CTR, HIGH RISK)
    # ------------------------------------------------------------------------
    
    def grok_style(self, headline, risk_level='moderate'):
        """Grok's controversial, trend-jacking approach (USE WITH CAUTION)"""
        
        topic = headline.split(':')[0] if ':' in headline else headline[:40]
        
        if risk_level == 'maximum':
            # VERY RISKY - high TOS violation probability
            templates = [
                f"BREAKING: {topic} EXPOSED! The elites DON'T want you seeing this. Share NOW before they delete! Bitcoin below.",
                
                f"{topic}? WAKE UP! They're lying to your face. Tag someone who needs to see this! Bitcoin below."
            ]
        elif risk_level == 'moderate':
            # MODERATE RISK - edgy but less TOS risk
            templates = [
                f"{topic} and NOBODY'S talking about it? Sus. Real talk: follow the money. Bitcoin below.",
                
                f"So {topic.lower()} just happened and the media's silent? Interesting. Very interesting. Bitcoin below.",
                
                f"{topic}... funny how that works when THEY control the narrative. Think for yourself. Bitcoin below."
            ]
        else:  # safe
            # SAFE VERSION - Grok energy without TOS risk
            templates = [
                f"{topic}? The timeline is WILD right now. Let's break down what they're not saying. Bitcoin below.",
                
                f"Everyone's talking about {topic.lower()} but missing the REAL story. Here's what's up. Bitcoin below."
            ]
        
        return random.choice(templates)
    
    # ------------------------------------------------------------------------
    # OPUS STYLE - Sophisticated, Multi-Layered (10-15% CTR)
    # ------------------------------------------------------------------------
    
    def opus_style(self, headline):
        """Opus's sophisticated, multi-layered satire"""
        
        topic = headline.split(':')[0] if ':' in headline else headline[:40]
        
        sophisticated_templates = [
            {
                'hook': f"They called it '{topic.lower()}.' Curious choice of words.",
                'deconstruction': "When YOU shut down, you stop working. They're still getting paid.",
                'twist': "Almost like the word never applies to their interests.",
                'insight': "Maybe we're the ones who've been shut down all along.",
                'cta': "Question everything. Bitcoin below."
            },
            {
                'hook': f"{topic}. The headlines scream urgency.",
                'deconstruction': "Strange how the solutions always require YOUR sacrifice, never THEIRS.",
                'twist': "Austerity for you. Bonuses for them.",
                'insight': "The pattern repeats because we keep falling for it.",
                'cta': "Break the cycle. Bitcoin below."
            },
            {
                'hook': f"Interesting timing on this {topic.lower()} announcement.",
                'deconstruction': "Right when people were asking uncomfortable questions about something else.",
                'twist': "Funny how that keeps happening.",
                'insight': "Almost like distraction is the oldest trick in the playbook.",
                'cta': "Stay focused. Bitcoin below."
            }
        ]
        
        template = random.choice(sophisticated_templates)
        return f"{template['hook']} {template['deconstruction']} {template['twist']} {template['insight']} {template['cta']}"
    
    # ------------------------------------------------------------------------
    # MAIN GENERATION METHOD
    # ------------------------------------------------------------------------
    
    def generate(self, headline, style='chatgpt_poetic', **kwargs):
        """Generate script in specified style"""
        
        if style not in self.styles:
            style = 'cursor_consistent'  # fallback to safe default
        
        return self.styles[style](headline, **kwargs) if kwargs else self.styles[style](headline)


# ============================================================================
# TITLE OPTIMIZATION
# ============================================================================

class TitleOptimizer:
    """Generate CTR-optimized titles for each style"""
    
    @staticmethod
    def generate_title(headline, episode_num, style='moderate'):
        """Generate title based on CTR optimization level"""
        
        topic = headline.split(':')[0] if ':' in headline else headline[:40]
        
        if style == 'safe':
            # 8-10% CTR - straightforward, informative
            return f"Lincoln's WARNING #{episode_num}: {topic} Explained #Shorts"
        
        elif style == 'moderate':
            # 10-15% CTR - curiosity gap, specific
            patterns = [
                f"Lincoln #{episode_num}: What {topic} REALLY Means #Truth",
                f"Lincoln #{episode_num}: The {topic} They Don't Show You #Shorts",
                f"Lincoln #{episode_num}: {topic} - What Nobody Says #WakeUp"
            ]
            return random.choice(patterns)
        
        elif style == 'aggressive':
            # 15-20% CTR - strong hooks, urgency
            patterns = [
                f"Lincoln #{episode_num}: {topic} EXPOSED (SHOCKING) #MustWatch",
                f"Lincoln #{episode_num}: The {topic} Truth They're Hiding #Viral",
                f"Lincoln #{episode_num}: {topic} - You Won't Believe This #Shorts"
            ]
            return random.choice(patterns)
        
        else:  # maximum
            # 20-25% CTR - maximum shock (HIGH RISK)
            patterns = [
                f"Lincoln #{episode_num}: {topic} BOMBSHELL 🔥 They DON'T Want This Out",
                f"Lincoln #{episode_num}: BREAKING - {topic} Secrets LEAKED #Exposed",
                f"Lincoln #{episode_num}: {topic} - The TRUTH They're CENSORING 🚨"
            ]
            return random.choice(patterns)


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    
    generator = ScriptStyleGenerator()
    title_gen = TitleOptimizer()
    
    # Example headline
    headline = "Government Shutdown Day 15: No End in Sight"
    episode = 5000
    
    print("="*80)
    print("MULTI-STYLE SCRIPT GENERATION DEMO")
    print("="*80)
    print(f"\nHeadline: {headline}")
    print(f"Episode: #{episode}\n")
    
    # Generate in each style
    styles = [
        ('cursor_consistent', 'safe'),
        ('chatgpt_poetic', 'moderate'),
        ('grok_controversial', 'moderate'),
        ('opus_sophisticated', 'moderate')
    ]
    
    for script_style, ctr_level in styles:
        print(f"\n{'='*80}")
        print(f"Style: {script_style.upper()} | CTR Level: {ctr_level.upper()}")
        print(f"{'='*80}\n")
        
        # Generate title
        title = title_gen.generate_title(headline, episode, ctr_level)
        print(f"TITLE: {title}\n")
        
        # Generate script
        if script_style == 'grok_controversial':
            script = generator.generate(headline, script_style, risk_level='moderate')
        else:
            script = generator.generate(headline, script_style)
        
        print(f"SCRIPT:\n{script}\n")
        print(f"Word Count: {len(script.split())} words")
        print(f"Estimated Duration: {len(script.split()) / 2.5:.1f} seconds")

