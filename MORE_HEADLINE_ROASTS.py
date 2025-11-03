#!/usr/bin/env python3
"""
MORE_HEADLINE_ROASTS.py - Expanded headline roast templates

NO COMEDIAN NAMES - just pure roast energy
"""

import random

def roast_headline(headline: str) -> str:
    """
    Generate brutal headline roast with NO comedian names
    
    Pure roast energy inspired by their STYLES, never naming them
    """
    
    hl = headline.lower()
    
    # ========================================================================
    # GOVERNMENT/POLITICS ROASTS (10 variations)
    # ========================================================================
    
    if any(word in hl for word in ['government', 'shutdown', 'congress', 'senate', 'politician']):
        return random.choice([
            f"{headline}? Man, I'm DEAD and I got more life than these politicians! They out here playing dress-up in suits, pocket full of lobby money, telling YOU to tighten your belt while their stomachs touching their KNEES! Bitcoin below.",
            
            f"Look at this: {headline}. These muhfuckas got HEALTHCARE while telling you 'we can't afford it!' They work 90 days a year for $174,000! YOU work 365 for $40k! And THEY broke?! Scan that QR.",
            
            f"{headline}! Let me tell you something - I seen a lot of BULLSHIT in my time, but THIS?! These clowns got mansions talking about YOUR privilege! Private jets preaching about YOUR carbon! THE NERVE! The muhfuckin AUDACITY! QR code NOW!",
            
            f"{headline}. Now watch this shit. Poor people defending billionaires is like CHICKENS campaigning for KFC! And the billionaires LOVE IT - 'Look at these dumb muhfuckas!' Both parties robbing you, but you picking TEAMS like it's a sport! Wake up. QR below.",
            
            f"LINCOLN! And I got some shit to say! {headline}?! These RAT SOUP-EATING MUHFUCKAS! Silver spoon-sucking, two-faced, bribe-taking, lying-ass POLITICIANS! Talking about 'public service' while servicing themselves! Bitcoin below before I RISE UP!",
            
            f"{headline}. Now let's talk about what's REALLY happening. They want you broke, distracted, and FIGHTING EACH OTHER. Why? Broke people don't ask questions! Distracted people don't organize! Divided people can't revolt! It's CHESS, not checkers! Bitcoin below.",
            
            f"{headline} - same shit, different day. They keep you broke so you desperate. Desperate people don't fight back. Desperate people take ANYTHING. Break that chain! Bitcoin!",
            
            f"{headline}?! Man, fuck all that! They lying to your FACE and you just accepting it! These old ass politicians ain't NEVER struggled a day! Never missed a meal! Never chose between rent and food! But THEY know what's best for YOU?! Bullshit! Bitcoin QR!",
            
            f"{headline}? Here's the game: Keep you MAD at the wrong people. Mexicans took your job? Nah, your BOSS took it to China! But they got you fighting your neighbor while billionaires sipping wine like 'this shit WORKS!' Scan QR.",
            
            f"Yo! {headline}?! They playing YOU like a FIDDLE! Selling fear like crack! 'Be scared! Be TERRIFIED!' - meanwhile THEY buying beach houses! Stop being a SUCKER! Scan that QR!",
        ])
    
    # ========================================================================
    # ECONOMY/MARKET ROASTS (10 variations)
    # ========================================================================
    
    elif any(word in hl for word in ['market', 'economy', 'crash', 'recession', 'inflation', 'stock']):
        return random.choice([
            f"{headline}... AGAIN?! They crash the market, get BONUSES. You lose your job, get LECTURES about 'personal responsibility!' Personal responsibility?! FROM THE MUHFUCKAS WHO GOT BAILED OUT?! Bitcoin below.",
            
            f"So {headline}. Market crashes! Rich sad! Poor been CRASHED for YEARS! Wall Street: 'Oh no, lost millions!' - YOU: 'Lost my HOUSE!' They get bailouts! You get bootstraps! Fuck that! QR below.",
            
            f"{headline}. Lemme get this straight - they gamble with YOUR money, lose, then YOU bail THEM out?! Socialism for the rich, capitalism for the poor! That's not economics, that's ROBBERY! Bitcoin below.",
            
            f"Check this out: {headline}. They do this EVERY time! Create a crisis, offer the 'solution,' and somehow billionaires end up RICHER! It's a MAGIC TRICK! 'Pick a card, any card - OH LOOK, WE RICH AGAIN!' Stop falling for it! QR below.",
            
            f"{headline}. Democracy's a ghost in the machine now, algorithms feeding you outrage for engagement. They monetize your anger, package your pain, sell it back as content. You the product, the consumer, and the consumed. All at once. Bitcoin below.",
            
            f"{headline}? CEO gets a golden parachute. You get a pink slip and 'thoughts and prayers.' The game is rigged. The house always wins. The house is burning. Cash App QR - escape while you can.",
            
            f"Real talk: {headline}. CEO salary: $20 MILLION. Your raise: 2%. Inflation: 8%. You LOSING money while working HARDER! They buying yachts! You clipping COUPONS! This is madness! QR below!",
            
            f"{headline}... Another headline, another cycle. Bread and circuses for the digital age. Feed 'em outrage, keep 'em scrolling, harvest the data, sell it to the highest bidder. You ain't the customer, you the CROP. Bitcoin below.",
            
            f"{headline}?! Wall Street casinos with YOUR pension! Lose? GOVERNMENT saves them! Win? THEY keep it! You can't even bet on sports legally in half the states, but THEY bet the whole economy! Scan QR!",
            
            f"Listen: {headline}. They print money for BANKS. Tell YOU 'we can't afford healthcare!' Can't afford it?! You just PRINTED $4 TRILLION! Inflation? That's THEFT! Stealing from savers, giving to speculators! Bitcoin below!",
        ])
    
    # ========================================================================
    # TECH/AI/CRYPTO ROASTS (10 variations)
    # ========================================================================
    
    elif any(word in hl for word in ['tech', 'ai', 'crypto', 'bitcoin', 'google', 'facebook', 'meta', 'amazon']):
        return random.choice([
            f"{headline}. You're the product, not the customer. Every click, tracked. Every word, logged. They know you better than you know yourself. Sold your data. Bought your compliance. Alexa's listening. Google's watching. Zuck's selling. You're naked and don't even know it. Cash App QR - own your data or they own you.",
            
            f"{headline}? Let me explain the CON: They got you arguing about CRUMBS while they eating the whole CAKE! Left vs Right? That's the SHOW! Real fight is UP vs DOWN, but they keep you fighting LEFT vs RIGHT! WAKE UP! Bitcoin below.",
            
            f"They say {headline.lower()}. But who's 'they'? The ones who profit when you panic. Fear merchants moving weight like pharmaceutical reps. Your anxiety's their quarterly earnings. Break the cycle. Scan QR.",
            
            f"{headline}. Algorithm knows you're depressed. Feeds you more depression. Sells you antidepressants. Your mental health is their business model. Your attention is their product. You're the lab rat. Scrolling through your own lobotomy. Bitcoin QR - unplug or die inside.",
            
            f"{headline} - and who's regulating? The people they PAID TO GET ELECTED! Fox guarding the henhouse! Zuckerberg testifying to Congress about privacy - to people who don't know how email WORKS! This is THEATER! Scan QR!",
            
            f"So {headline}. They selling you the future while stealing your PRESENT! AI gonna take jobs? They ALREADY took them to China! Now blaming ROBOTS for what GREED did! Misdirection! Look HERE while they rob you THERE! Bitcoin below!",
            
            f"{headline}?! These tech billionaires: 'I'm gonna change the world!' - yeah, change it so YOU work 3 gigs with no benefits while THEY build SPACESHIPS! 'Gig economy' - that's POVERTY with an APP! Cash App QR!",
            
            f"{headline}. Crypto regulation? Translation: Banks scared! Can't control it, gotta CRUSH it! 'Protecting consumers' - you mean protecting YOUR monopoly! They print unlimited money, YOU can't have decentralized currency?! Scan QR!",
            
            f"Listen: {headline}. Mark Zuckerberg made $50 BILLION selling YOUR conversations! Every 'like' is DATA! Every post is PRODUCT! You're working for FREE making THEM rich! Digital sharecropping! Bitcoin below!",
            
            f"{headline}... Translation: The old guard trying to control the new! Can't ban the internet, can't ban crypto! They'll TRY! They always do! Power doesn't surrender, it has to be TAKEN! QR below!",
        ])
    
    # ========================================================================
    # HEALTHCARE ROASTS (5 variations)
    # ========================================================================
    
    elif any(word in hl for word in ['healthcare', 'hospital', 'insurance', 'medical', 'drug']):
        return random.choice([
            f"'{headline}' - if you can afford to not die. Insulin costs pennies to make, hundreds to buy. They'd rather you suffer than lose profit. You're not a patient, you're a revenue stream. Die quietly or pay loudly. Those are your options. Bitcoin QR - buy your freedom.",
            
            f"{headline}?! America: We got money for WAR! No money for HEALTHCARE! $800 BILLION to blow up STRANGERS overseas! Can't afford to keep GRANDMA alive?! Your LIFE ain't profitable! Your DEATH is cheap! That's the calculation! Scan QR!",
            
            f"So {headline}. Insurance companies: 'We'll cover you!' - until you NEED IT! Then it's pre-existing conditions, out-of-network, deductible! You pay IN for 40 years! Claim ONCE - they DROP you! Legal SCAM! Bitcoin below!",
            
            f"{headline}. Big Pharma got you HOOKED then blamed YOU for the addiction! OxyContin pushed by doctors, bought by pharma. Rehab costs more than college. Narcan in vending machines. Bodies in the streets. You're an epidemic statistic. They're quarterly earnings. Pain is profit. Death is just cost of business. Cash App QR - break the cycle or die trying.",
            
            f"{headline}?! Medical bankruptcy - ONLY in America! Richest country on EARTH! People starting GoFundMes to not DIE! This ain't healthcare, it's EXTORTION! 'Give us everything or PERISH!' That's the offer! Bitcoin QR!",
        ])
    
    # ========================================================================
    # WAR/MILITARY ROASTS (5 variations)
    # ========================================================================
    
    elif any(word in hl for word in ['war', 'military', 'draft', 'ukraine', 'israel', 'defense']):
        return random.choice([
            f"{headline}. Every missile is a hospital you'll never build. Every tank is a school that won't open. They send your kids to die for oil they call 'freedom.' Defense contractors get richer. You get a folded flag. War is peace. Slavery is freedom. Your taxes are their blood money. Bitcoin - defund the machine.",
            
            f"DRAFT?! {headline}. Didn't learn from VIETNAM?! Rich men send POOR kids to die for OIL! Republicans: 'Support troops!' - by killing them overseas! Democrats: '$800 BILLION war budgets!' while kids starve! BOTH love war! Death is PROFITABLE! Look in mirrors.",
            
            f"{headline}?! Defense budget: $800 BILLION! That's $1.5 MILLION per MINUTE! But school needs pencils! Veteran needs THERAPY! 'Thank you for your service' - here's PTSD and homelessness! They USE you, then FORGET you! Scan QR!",
            
            f"So {headline}. They wrap themselves in the FLAG while sending YOUR kids to die! 'Fighting for freedom' - whose freedom? Not YOURS! You can't afford RENT! Halliburton gets no-bid contracts! Soldiers get caskets! Wake up! Bitcoin below!",
            
            f"{headline}. Same play since Rome: Keep 'em fighting ABROAD so they don't fight at HOME! Wars fund campaigns! Death is business! Every bomb is a billionaire's bonus! They profit from YOUR pain! QR below!",
        ])
    
    # ========================================================================
    # DEFAULT/GENERAL ROASTS (10 variations for ANY headline)
    # ========================================================================
    
    else:
        return random.choice([
            f"{headline}. Only KIDS and DRUNKS tell the truth! Everyone else LYING to your FACE! Republicans: Small government in a UTERUS! Democrats: Free everything - who PAYS?! SPOILER: YOU! American DREAM? You gotta be ASLEEP to believe it! ALL getting PLAYED! Look in mirrors.",
            
            f"{headline}?! They manufacture consent like a factory line. Outrage on Monday, distraction by Friday. You're angry at your neighbor while they rob you blind. Left vs right - both hands in YOUR pocket. You're scrolling through your own surveillance. Support truth. Bitcoin below.",
            
            f"{headline}. They let you vote for which hand chokes you. Red tie, blue tie - same neck, same boot. Gerrymandered districts. Voter suppression called 'election integrity.' Your vote counts - barely. Democracy is two wolves and a sheep voting on dinner. Guess who's dinner. Guess who's hungry. Bitcoin below - vote with your wallet, they can't rig that.",
            
            f"Listen: {headline}. They sell panic for profit. Fear is their favorite currency. Crisis creates opportunity - for THEM! They got beach houses in New Zealand! You got anxiety and DEBT! Climate burns, wars rage, economy crashes - they're INSULATED! You're EXPOSED! Scan QR!",
            
            f"{headline}?! Pull yourself up by bootstraps you can't afford! Therapy costs $200/hour! Your insurance covers $0! They call you lazy when you're drowning! Stigma is profitable! Treatment is expensive! You're not sick, you're 'underperforming!' Bitcoin QR - buy peace they won't sell!",
            
            f"So {headline}. They got you HOOKED on outrage! Scroll, rage, scroll, rage! Dopamine drip! Algorithm knows you're miserable! Feeds you MORE misery! Sells antidepressants in the sidebar! Your mental breakdown is their BUSINESS MODEL! Unplug! Cash App below!",
            
            f"{headline}. Bread and circuses, digital edition! Feed 'em fear, keep 'em clicking, harvest the data, sell to the highest bidder! You ain't the customer, you the CROP! They farming YOUR attention! Reaping YOUR anxiety! Time to REVOLT! Bitcoin below!",
            
            f"{headline}?! They knew in the 70s! Denied in the 80s! Profited in the 90s! Now selling YOU carbon credits while drilling DEEPER! Your recycling is THEATER! Their pollution is POLICY! Planet burns, they got beach houses on high ground! You'll DROWN! They'll WATCH! Scan QR!",
            
            f"Real talk: {headline}. While you worrying about THIS, they passing laws that fuck you SIDEWAYS! They WANT you distracted! Want you poor! Want you STUPID! Don't give 'em what they want! Wake up! QR below!",
            
            f"{headline}?! Same playbook every time: Create the problem, blame YOU, sell the solution! Then the solution makes it WORSE! Rinse, repeat, PROFIT! You're stuck in a LOOP! They're cashing CHECKS! Break the cycle! Bitcoin below!",
        ])

# Test variety
if __name__ == "__main__":
    test_headlines = [
        "Government Shutdown Day 15",
        "Market Crash Imminent",
        "Healthcare Costs Surge",
        "War Funding Approved",
        "Climate Crisis Worsens",
        "Tech Layoffs Continue",
        "Police Brutality Case",
        "Education Budget Slashed",
        "Immigration Raids Begin",
        "Crypto Regulation Passes"
    ]
    
    print("\n" + "="*70)
    print("MORE HEADLINE ROASTS - NO COMEDIAN NAMES")
    print("="*70 + "\n")
    
    for headline in test_headlines:
        script = roast_headline(headline)
        
        # Verify NO names
        names = ['Pryor', 'Chappelle', 'Carlin', 'Bernie', 'Rudy', 'Katt', 'Williams', 'NBA', 'K-Dot', 'Josh']
        found = [n for n in names if n.lower() in script.lower()]
        
        print(f"HEADLINE: {headline}")
        print("-"*70)
        print(script)
        print(f"\nWords: {len(script.split())}")
        print(f"Names found: {found if found else 'NONE (CLEAN!)'}")
        print("="*70 + "\n")


