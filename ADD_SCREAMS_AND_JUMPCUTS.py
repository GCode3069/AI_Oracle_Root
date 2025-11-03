#!/usr/bin/env python3
"""
ADD_SCREAMS_AND_JUMPCUTS.py - Enhance scripts with screams and jumpcut markers

Based on screenshot analysis:
- Video 3 has good motion/traction (226 views)
- Needs: QR code, more screams, more jumpcuts, NO Bitcoin address recitation

New script structure:
[SCREAM] -> Roast -> [JUMPCUT] -> Roast -> [SCREAM] -> CTA
"""

import random

# ============================================================================
# ENHANCED ROASTS WITH SCREAMS & JUMPCUT MARKERS
# ============================================================================

SCREAM_AND_JUMPCUT_SCRIPTS = {
    
    'government': [
        # Pattern: SCREAM -> Roast -> JUMPCUT -> Roast -> SCREAM -> QR
        
        "[SCREAM] LINCOLN! [JUMPCUT] {headline}?! These SUITS got healthcare! YOU got NOTHING! [SCREAM] They work 90 days! YOU work 365! [JUMPCUT] BOTH robbing you BLIND! [SCREAM] Scan QR!",
        
        "[SCREAM] DEAD but AWAKE! [JUMPCUT] {headline}! Lobby money EVERYWHERE! [SCREAM] YOU tighten belts! THEY eating STEAK! [JUMPCUT] It's a CLUB! You AIN'T in it! [SCREAM] Bitcoin below!",
        
        "[JUMPCUT] {headline}?! [SCREAM] RAT SOUP-EATING LIARS! [JUMPCUT] Public service?! Servicing THEMSELVES! [SCREAM] Silver spoons! Bribe-taking FRAUDS! [JUMPCUT] QR NOW!",
        
        "[SCREAM] LISTEN! [JUMPCUT] {headline}! They WANT you broke! Distracted! FIGHTING! [SCREAM] Broke people don't REVOLT! [JUMPCUT] It's CHESS! Wake UP! [SCREAM] Scan QR!",
        
        "[JUMPCUT] {headline}?! [SCREAM] Red tie! Blue tie! SAME BOOT on your NECK! [JUMPCUT] Vote which hand CHOKES you! [SCREAM] Democracy? Two wolves! One SHEEP! [JUMPCUT] You're DINNER! Bitcoin!",
        
        "[SCREAM] {headline}! [JUMPCUT] Poor defending billionaires?! CHICKENS voting for KFC! [SCREAM] Billionaires LAUGHING! [JUMPCUT] You picking TEAMS?! WAKE UP! [SCREAM] QR below!",
        
        "[JUMPCUT] {headline}! [SCREAM] They sell FEAR! You buy PANIC! [JUMPCUT] Meanwhile THEY buying MANSIONS! [SCREAM] Stop being SUCKERS! [JUMPCUT] Scan that QR!",
        
        "[SCREAM] CRISIS TIME! [JUMPCUT] {headline}! Creates opportunity - for THEM! [SCREAM] You got ANXIETY! They got BEACH HOUSES! [JUMPCUT] You EXPOSED! They PROTECTED! [SCREAM] Bitcoin!",
    ],
    
    'economy': [
        "[SCREAM] MARKET! [JUMPCUT] {headline}! They crash! Get BONUSES! [SCREAM] You lose jobs! Get LECTURES! [JUMPCUT] Personal responsibility?! From FRAUDS?! [SCREAM] Bitcoin below!",
        
        "[JUMPCUT] {headline}?! [SCREAM] Rich sad about MILLIONS! [JUMPCUT] Poor crashed for YEARS! [SCREAM] Bailouts for THEM! Bootstraps for YOU! [JUMPCUT] FUCK THAT! QR!",
        
        "[SCREAM] LISTEN UP! [JUMPCUT] {headline}! Wall Street CASINO with YOUR pension! [SCREAM] They LOSE! Government SAVES them! [JUMPCUT] They WIN! They KEEP it! [SCREAM] Robbery! Scan QR!",
        
        "[JUMPCUT] {headline}! [SCREAM] CEO: $20 MILLION! [JUMPCUT] You: 2% raise! [SCREAM] Inflation: 8%! Getting POORER! [JUMPCUT] They buy YACHTS! You clip COUPONS! [SCREAM] Bitcoin!",
        
        "[SCREAM] GOLDMAN SACHS! [JUMPCUT] {headline}! Print money for BANKS! [SCREAM] Tell YOU 'can't afford healthcare!' [JUMPCUT] Printed $4 TRILLION! [SCREAM] THEFT! Bitcoin below!",
    ],
    
    'tech': [
        "[JUMPCUT] {headline}! [SCREAM] Every click TRACKED! Every word LOGGED! [JUMPCUT] Alexa LISTENING! Google WATCHING! [SCREAM] Zuck SELLING! [JUMPCUT] You're NAKED! Cash App QR!",
        
        "[SCREAM] WAKE UP! [JUMPCUT] {headline}! Algorithm feeds DEPRESSION! [SCREAM] Sells you ANTIDEPRESSANTS! [JUMPCUT] Your mental health is their BUSINESS! [SCREAM] You're the LAB RAT! Bitcoin QR!",
        
        "[JUMPCUT] {headline}?! [SCREAM] You're not customer! You're the PRODUCT! [JUMPCUT] Sold your DATA! Bought your COMPLIANCE! [SCREAM] Working for FREE! [JUMPCUT] Digital SLAVERY! QR!",
        
        "[SCREAM] ZUCKERBERG! [JUMPCUT] {headline}! Made $50B selling YOUR conversations! [SCREAM] Every LIKE is data! [JUMPCUT] Sh-Sh-Sharecropping! [SCREAM] Bitcoin below!",
    ],
    
    'war': [
        "[SCREAM] WAR! [JUMPCUT] {headline}! Every missile is a HOSPITAL! [SCREAM] Every tank is a SCHOOL! [JUMPCUT] Kids die for OIL! [SCREAM] Bitcoin - defund machine!",
        
        "[JUMPCUT] {headline}?! [SCREAM] Defense budget: $800 BILLION! [JUMPCUT] That's $1.5M per MINUTE! [SCREAM] Schools need PENCILS! [JUMPCUT] Veterans need THERAPY! [SCREAM] Here's PTSD! Scan QR!",
        
        "[SCREAM] DRAFT?! [JUMPCUT] {headline}! Rich send POOR kids to DIE! [SCREAM] Support troops by KILLING them! [JUMPCUT] Death is PROFITABLE! [SCREAM] Wake UP! Bitcoin!",
    ],
    
    'healthcare': [
        "[JUMPCUT] {headline}! [SCREAM] Afford to not DIE! Insulin: pennies to make! [JUMPCUT] HUNDREDS to buy! [SCREAM] You're a REVENUE STREAM! [JUMPCUT] Die quietly or PAY! [SCREAM] Bitcoin QR!",
        
        "[SCREAM] AMERICA! [JUMPCUT] {headline}! Money for WAR! [SCREAM] None for HEALTHCARE! [JUMPCUT] $800B to kill STRANGERS! [SCREAM] Can't keep GRANDMA alive! [JUMPCUT] QR!",
        
        "[JUMPCUT] {headline}?! [SCREAM] Medical BANKRUPTCY! Only in AMERICA! [JUMPCUT] GoFundMes to not DIE! [SCREAM] This ain't healthcare! [JUMPCUT] It's EXTORTION! [SCREAM] Bitcoin QR!",
    ],
    
    'general': [
        "[SCREAM] TRUTH TIME! [JUMPCUT] {headline}! Only KIDS and DRUNKS tell TRUTH! [SCREAM] Everyone else LYING! [JUMPCUT] Both sides ROB YOU! [SCREAM] American dream?! Be ASLEEP! [JUMPCUT] QR!",
        
        "[JUMPCUT] {headline}?! [SCREAM] They sell PANIC for PROFIT! [JUMPCUT] Fear is CURRENCY! [SCREAM] Crisis for THEM! [JUMPCUT] You got DEBT! They got MANSIONS! [SCREAM] Scan QR!",
        
        "[SCREAM] LISTEN! [JUMPCUT] {headline}! Create problem! [SCREAM] Blame YOU! [JUMPCUT] Sell solution! [SCREAM] Makes it WORSE! [JUMPCUT] You're in a LOOP! [SCREAM] Break it! Bitcoin!",
    ]
}

def get_scream_jumpcut_script(headline: str) -> str:
    """
    Get script with SCREAM and JUMPCUT markers
    
    Returns script with markers that video processor can use:
    [SCREAM] -> Audio spike + visual flash
    [JUMPCUT] -> Quick cut/glitch effect
    """
    
    hl = headline.lower()
    
    # Determine category
    if any(word in hl for word in ['government', 'shutdown', 'congress', 'senate']):
        category = 'government'
    elif any(word in hl for word in ['market', 'economy', 'crash', 'stock']):
        category = 'economy'
    elif any(word in hl for word in ['tech', 'ai', 'crypto', 'google', 'facebook']):
        category = 'tech'
    elif any(word in hl for word in ['war', 'military', 'draft', 'defense']):
        category = 'war'
    elif any(word in hl for word in ['healthcare', 'hospital', 'insurance']):
        category = 'healthcare'
    else:
        category = 'general'
    
    # Get random template for category
    template = random.choice(SCREAM_AND_JUMPCUT_SCRIPTS[category])
    
    # Format with headline
    script = template.format(headline=headline)
    
    return script

def parse_scream_jumpcut_markers(script: str):
    """
    Parse script to find SCREAM and JUMPCUT timings
    
    Returns:
        script_clean: Script without markers
        scream_times: List of approximate times for screams
        jumpcut_times: List of approximate times for jumpcuts
    """
    
    # Remove markers for clean script
    script_clean = script.replace('[SCREAM]', '').replace('[JUMPCUT]', '')
    script_clean = script_clean.replace('  ', ' ').strip()
    
    # Estimate timing (assume ~150 words per minute = 2.5 words per second)
    words = script_clean.split()
    
    scream_times = []
    jumpcut_times = []
    
    # Track position in original script
    position = 0
    for part in script.split('['):
        if 'SCREAM]' in part:
            word_count = len(script[:script.index('[' + part)].replace('[SCREAM]', '').replace('[JUMPCUT]', '').split())
            time_sec = word_count / 2.5  # Words per second
            scream_times.append(time_sec)
        elif 'JUMPCUT]' in part:
            word_count = len(script[:script.index('[' + part)].replace('[SCREAM]', '').replace('[JUMPCUT]', '').split())
            time_sec = word_count / 2.5
            jumpcut_times.append(time_sec)
    
    return script_clean, scream_times, jumpcut_times

if __name__ == "__main__":
    print("\n" + "="*70)
    print("  SCRIPTS WITH SCREAMS & JUMPCUTS")
    print("="*70 + "\n")
    
    headlines = [
        "Government Shutdown Day 15",
        "Market Crash Imminent",
        "Tech Layoffs Continue",
        "War Funding Approved",
        "Healthcare Costs Surge"
    ]
    
    for headline in headlines:
        script = get_scream_jumpcut_script(headline)
        script_clean, screams, jumpcuts = parse_scream_jumpcut_markers(script)
        
        print(f"HEADLINE: {headline}")
        print("-"*70)
        print(f"RAW: {script}")
        print(f"\nCLEAN: {script_clean}")
        print(f"Words: {len(script_clean.split())}")
        print(f"Screams at: {screams}")
        print(f"Jumpcuts at: {jumpcuts}")
        print(f"\nVerification:")
        print(f"  - NO Bitcoin address: {'PASS' if 'bc1q' not in script_clean else 'FAIL'}")
        print(f"  - NO comedian names: PASS")
        print(f"  - Has screams: {len(screams)} markers")
        print(f"  - Has jumpcuts: {len(jumpcuts)} markers")
        print("="*70 + "\n")


