#!/usr/bin/env python3
"""
SCRIPTS WITH REAL EDGE - Pryor, Chappelle, Dolemite, Katt Williams Energy
NO REPETITION. ACTUAL ROAST. RAW TRUTH.
"""

import random

def generate_edgy_script(headline):
    """
    Generate scripts with REAL EDGE
    Styles: Pryor's truth-telling, Chappelle's social commentary, 
    Dolemite's raw energy, Katt Williams' observational fury,
    K-Dot's layered metaphors, NBA YoungBoy's unfiltered rawness
    
    WITHOUT naming them - just using their ENERGY
    """
    
    topic = headline.lower()
    
    # ========================================================================
    # PRYOR-STYLE: Raw truth, uncomfortable honesty, personal angles
    # ========================================================================
    
    pryor_energy = [
        # Government/Politics
        f"{headline}? Man, I'm DEAD and I got more life than these politicians! They out here playing dress-up in suits, pocket full of lobby money, telling YOU to tighten your belt while their stomachs touching their KNEES! Bitcoin below.",
        
        f"Look at this: {headline}. These muhfuckas got HEALTHCARE while telling you 'we can't afford it!' They work 90 days a year for $174,000! YOU work 365 for $40k! And THEY broke?! Scan that QR.",
        
        # Economic
        f"{headline}... AGAIN?! They crash the market, get BONUSES. You lose your job, get LECTURES about 'personal responsibility!' Personal responsibility?! FROM THE MUHFUCKAS WHO GOT BAILED OUT?! Bitcoin below.",
    ]
    
    # ========================================================================
    # CHAPPELLE-STYLE: Layered social commentary, builds then HITS
    # ========================================================================
    
    chappelle_energy = [
        f"{headline}. Now watch this shit. Poor people defending billionaires is like CHICKENS campaigning for KFC! And the billionaires LOVE IT - 'Look at these dumb muhfuckas!' Both parties robbing you, but you picking TEAMS like it's a sport! Wake up. QR below.",
        
        f"So {headline}. Lemme get this straight - they defund schools, fund bombs. Can't afford books, but got $800 BILLION for missiles! Kids reading at 2nd grade level, but we TOP OF THE WORLD in blowing shit up! Priorities. Bitcoin below.",
        
        f"{headline}? Here's the game: Keep you MAD at the wrong people. Mexicans took your job? Nah, your BOSS took it to China! But they got you fighting your neighbor while billionaires sipping wine like 'this shit WORKS!' Scan QR.",
    ]
    
    # ========================================================================
    # DOLEMITE-STYLE: Aggressive, in-your-face, no filter
    # ========================================================================
    
    dolemite_energy = [
        f"LINCOLN! And I got some shit to say! {headline}?! These RAT SOUP-EATING MUHFUCKAS! Silver spoon-sucking, two-faced, bribe-taking, lying-ass POLITICIANS! Talking about 'public service' while servicing themselves! Bitcoin below before I RISE UP!",
        
        f"{headline}! Let me tell you something - I seen a lot of BULLSHIT in my time, but THIS?! These clowns got mansions talking about YOUR privilege! Private jets preaching about YOUR carbon! THE NERVE! The muhfuckin AUDACITY! QR code NOW!",
        
        f"Yo! {headline}?! They playing YOU like a FIDDLE! Selling fear like crack! 'Be scared! Be TERRIFIED!' - meanwhile THEY buying beach houses! Stop being a SUCKER! Scan that QR!",
    ]
    
    # ========================================================================
    # KATT WILLIAMS-STYLE: Observational fury, expose the game
    # ========================================================================
    
    katt_energy = [
        f"{headline}. Now let's talk about what's REALLY happening. They want you broke, distracted, and FIGHTING EACH OTHER. Why? Broke people don't ask questions! Distracted people don't organize! Divided people can't revolt! It's CHESS, not checkers! Bitcoin below.",
        
        f"Check this out: {headline}. They do this EVERY time! Create a crisis, offer the 'solution,' and somehow billionaires end up RICHER! It's a MAGIC TRICK! 'Pick a card, any card - OH LOOK, WE RICH AGAIN!' Stop falling for it! QR below.",
        
        f"{headline}? Let me explain the CON: They got you arguing about CRUMBS while they eating the whole CAKE! Left vs Right? That's the SHOW! Real fight is UP vs DOWN, but they keep you fighting LEFT vs RIGHT! WAKE UP! Bitcoin below.",
    ]
    
    # ========================================================================
    # K-DOT-STYLE: Layered metaphors, uncomfortable truths, wordplay
    # ========================================================================
    
    kdot_energy = [
        f"{headline}. Democracy's a ghost in the machine now, algorithms feeding you outrage for engagement. They monetize your anger, package your pain, sell it back as content. You the product, the consumer, and the consumed. All at once. Bitcoin below.",
        
        f"They say {headline.lower()}. But who's 'they'? The ones who profit when you panic. Fear merchants moving weight like pharmaceutical reps. Your anxiety's their quarterly earnings. Break the cycle. Scan QR.",
        
        f"{headline}... Another headline, another cycle. Bread and circuses for the digital age. Feed 'em outrage, keep 'em scrolling, harvest the data, sell it to the highest bidder. You ain't the customer, you the CROP. Bitcoin below.",
    ]
    
    # ========================================================================
    # NBA YOUNGBOY-STYLE: Unfiltered, raw, no pretense
    # ========================================================================
    
    youngboy_energy = [
        f"{headline}?! Man, fuck all that! They lying to your FACE and you just accepting it! These old ass politicians ain't NEVER struggled a day! Never missed a meal! Never chose between rent and food! But THEY know what's best for YOU?! Bullshit! Bitcoin QR!",
        
        f"Real talk: {headline}. While you worrying about THIS, they passing laws that fuck you SIDEWAYS! They WANT you distracted! Want you poor! Want you STUPID! Don't give 'em what they want! Wake up! QR below!",
        
        f"{headline} - same shit, different day. They keep you broke so you desperate. Desperate people don't fight back. Desperate people take ANYTHING. Break that chain! Bitcoin!",
    ]
    
    # ========================================================================
    # SELECT RANDOM STYLE FOR VARIETY
    # ========================================================================
    
    all_styles = (
        pryor_energy + chappelle_energy + dolemite_energy + 
        katt_energy + kdot_energy + youngboy_energy
    )
    
    return random.choice(all_styles)

# ============================================================================
# TEST THE VARIETY
# ============================================================================

if __name__ == "__main__":
    test_headlines = [
        "Government Shutdown Day 15",
        "Market Crash Imminent", 
        "Crypto Regulation Bill Passes",
        "Healthcare Costs Surge",
        "Education Budget Slashed"
    ]
    
    print("\n" + "="*80)
    print("  SCRIPTS WITH REAL EDGE - VARIETY TEST")
    print("="*80 + "\n")
    
    for headline in test_headlines:
        print(f"\nHEADLINE: {headline}")
        print("-" * 80)
        script = generate_edgy_script(headline)
        print(script)
        print(f"\nWords: {len(script.split())}")
        print(f"Characters: {len(script)}")


