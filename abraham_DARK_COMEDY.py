#!/usr/bin/env python3
"""
ABRAHAM LINCOLN - DARK SATIRICAL COMEDY ENGINE
Combines styles of: Pryor, Carlin, Chappelle, Bernie Mac, Dolemite, Robin Williams, Josh Johnson
NO SACRED COWS - Roasts EVERYONE (Dems, Republicans, rich, poor, left, right)
Darker, more observational, cutting social commentary
"""
import random

def generate_dark_satirical_script(headline):
    """
    Generate DARK SATIRICAL script - no cut cards, roast EVERYONE
    Style blend: Pryor's darkness + Carlin's cynicism + Chappelle's truth + Bernie Mac's anger
    """
    hl = headline.lower()
    
    # INTRO HOOKS (Dolemite/Bernie Mac energy - LOUD, commanding)
    intros = [
        "Abraham Lincoln! BACK from the DEAD! And I'm PISSED!",
        "It's ABE LINCOLN! Six foot four of RAW TRUTH!",
        "LINCOLN here! Died in 1865 but I STILL see your bullshit!",
        "Abraham MOTHERFUCKING Lincoln! Yeah I said it!",
    ]
    
    intro = random.choice(intros)
    
    # TOPIC-SPECIFIC ROASTS (Roast ALL sides - Carlin style)
    if "trump" in hl or "republican" in hl or "gop" in hl:
        body = f"""{headline}

REPUBLICANS! You worship a BILLIONAIRE who shits in a GOLD TOILET!

I grew up in a LOG CABIN eating CORNBREAD! This man's never worked a REAL day!

You POOR people defending him? That's like ROACHES voting for RAID!

George Carlin said it: "They got you by the balls!" And you're THANKING them!

But DEMOCRATS! You ain't off the hook! You got HOW MANY MILLIONAIRES crying about inequality?!

Nancy Pelosi worth $100 MILLION talking about "the people"? WHICH people? Your STOCK PORTFOLIO?!

Bernie Mac would say: I'm mad at ALL y'all! Both sides LYING! Both sides STEALING!

Pryor knew: The system ain't broken - it's working EXACTLY as designed! To fuck YOU!

I died to FREE people. You're all SLAVES again - to debt, to fear, to BULLSHIT!"""

    elif "democrat" in hl or "biden" in hl or "liberal" in hl:
        body = f"""{headline}

DEMOCRATS! You got more pronouns than POLICIES!

I fought a CIVIL WAR! You fight on TWITTER!

"Defund police" then cry when crime goes up! Robin Williams would call that WEAPONS-GRADE STUPIDITY!

But REPUBLICANS! You clutch pearls about "law and order" then STORM THE CAPITOL!

Josh Johnson style: Both sides got selective memory like a GOLDFISH with AMNESIA!

Rich liberals in gated communities preaching about walls! Chappelle clocked that hypocrisy YEARS ago!

Conservative Christians judging everyone! Jesus would FLIP YOUR TABLES again!

Carlin called it: "It's a big club and YOU AIN'T IN IT!" Left or right, you're getting ROBBED!

I preserved the Union. You idiots are DESTROYING it for LIKES and CLICKS!"""

    elif "police" in hl or "shooting" in hl or "law" in hl:
        body = f"""{headline}

POLICE! You got guns, badges, and QUALIFIED IMMUNITY! And you're SCARED of unarmed people?!

Pryor said it best: "Police scare ME and I ain't even done nothing!" Now they're KILLING people!

But "DEFUND" crowd! You think criminals gonna POLICE THEMSELVES?! That's DUMB!

Conservatives: "Back the Blue!" Until they're at YOUR door with a warrant!

Liberals: "ACAB!" Until someone's robbing YOUR house!

Bernie Mac energy: EVERYBODY'S WRONG! You want safety? FIX THE SYSTEM! Don't just YELL about it!

Robin Williams: "We militarized police then act surprised when they TREAT US like the enemy!"

I commanded ARMIES in war. These cops treat CITIZENS like combat zones!

Carlin knew: More prisons than schools! That's not a bug - it's THE BUSINESS MODEL!

ALL of you - left, right, black, white - getting PLAYED while they count the MONEY!"""

    elif "economy" in hl or "inflation" in hl or "stock" in hl or "market" in hl:
        body = f"""{headline}

THE ECONOMY! Rich people's feelings getting HURT!

Chappelle style: Stock market crashes, RICH people sad. Poor people? We been CRASHED!

Republicans: "Free market!" unless YOUR business fails - then it's BAILOUT time!

Democrats: "Tax the rich!" while BEING the rich! AOC at the Met Gala in a $30,000 dress!

Pryor observed: Poor people pay taxes. Rich people pay ACCOUNTANTS!

Carlin's ghost screaming: "They want obedient WORKERS! Just smart enough to run the machines!"

"Inflation"? That's code for "We're ROBBING you and calling it ECONOMICS!"

Bernie Mac would say: You work TWO JOBS and can't afford RENT! That's not capitalism - that's SLAVERY with extra steps!

I fought to end slavery. You brought it back with INTEREST RATES!

Both parties serving the SAME masters - Wall Street! And you arguing about which COLOR tie they wear!"""

    elif "education" in hl or "school" in hl or "student" in hl:
        body = f"""{headline}

EDUCATION SYSTEM! America's got money for BOMBS but not for BOOKS!

I taught MYSELF law by candlelight! Your kids got iPads and can't READ!

Republicans: "School choice!" Code for: "Poor kids can stay DUMB!"

Democrats: "Free college!" While charging $100K for a DEGREE in UNEMPLOYMENT!

Josh Johnson style: Student debt is SLAVERY you APPLY for! With a 7% interest rate!

Carlin warned us: "They don't want educated citizens! They want OBEDIENT WORKERS!"

Teachers need second jobs! CEOs need second YACHTS! Tell me that makes sense!

Robin Williams would say: We teach to the TEST instead of teaching kids to THINK!

"No Child Left Behind" became "Every Child LEFT BEHIND!"

Both parties talking about children's future while DESTROYING it! That's not policy - that's CHILD ABUSE!"""

    elif "climate" in hl or "environment" in hl or "weather" in hl:
        body = f"""{headline}

CLIMATE CHANGE! Rich people KNEW since the '70s and LIED!

Chappelle style: They sold the planet for QUARTERLY EARNINGS! That's not business - that's PSYCHOPATHY!

Republicans: "Climate hoax!" while buying BEACHFRONT PROPERTY INSURANCE!

Democrats: "Save Earth!" from private JETS! Greta crying while Kerry's flying!

Pryor would say: Poor people didn't cause this! But WE'RE the ones drowning!

Carlin called it: "The planet's FINE! The PEOPLE are fucked! The planet will shake us off like a bad case of FLEAS!"

"Green New Deal"? How about STOP SUBSIDIZING OIL COMPANIES for $20 BILLION a year!

Robin Williams: "We're killing the planet and arguing about whether it's HAPPENING!"

You ALL complicit! Rich people destroying it! Politicians enabling it! You consuming it!

I preserved forests. You paved them for PARKING LOTS!"""

    elif "war" in hl or "military" in hl or "conflict" in hl or "ukraine" in hl or "israel" in hl:
        body = f"""{headline}

WAR! America's favorite EXPORT!

I fought a Civil War to FREE people! You fight foreign wars to CONTROL people!

Republicans: "Support troops!" by sending them to die for OIL!

Democrats: "Peace!" while approving $800 BILLION war budgets!

Pryor observed: Poor kids fight. Rich kids get DEFERMENTS! Sound familiar?!

Bernie Mac energy: You send OTHER people's kids to die! Not YOUR kids!

Josh Johnson: We got money for missiles but not MEDICINE! Priorities!

Carlin's truth: "War is rich old men protecting their property by sending lower-class kids to die!"

"Defense" budget? You ain't DEFENDING! You're ATTACKING! Call it what it IS!

Both parties LOVE war! It's profitable! You think they'll STOP? That's cute!"""

    elif "tech" in hl or "ai" in hl or "zuckerberg" in hl or "musk" in hl or "bezos" in hl:
        body = f"""{headline}

TECH BILLIONAIRES! Modern day ROBBER BARONS!

Chappelle style: These nerds got RICH and now they think they're GODS!

Zuckerberg stole Facebook! Musk buying Twitter for $44 BILLION - that's "fuck you" money CUBED!

Bezos so rich he went to SPACE while his workers piss in BOTTLES!

Republicans: "Job creators!" Creating jobs in BANGLADESH at $2 an hour!

Democrats: "Regulate Big Tech!" while taking their CAMPAIGN DONATIONS!

Carlin predicted: "Garbage in, garbage out! They OWN you!"

Pryor knew: Technology was supposed to FREE us! Now we're ENSLAVED to phones!

Robin Williams: "We created AI to replace us! Because apparently we HATE ourselves!"

ALL of you - buying iPhones made by CHILD LABOR! But you post about JUSTICE! That's rich!"""

    elif "abortion" in hl or "roe" in hl or "women" in hl:
        body = f"""{headline}

ABORTION! Where MEN make laws about WOMEN'S bodies!

Republicans: "Pro-life!" Until that baby needs FOOD, then it's "bootstraps!"

No healthcare! No childcare! No maternity leave! But you MUST have that baby!

Democrats: "My body my choice!" Unless it's vaccines - then it's MANDATE!

Carlin said: "Pre-born you're fine! Pre-school you're FUCKED!"

Pryor observed: Rich women ALWAYS had access! This law's for POOR women!

Bernie Mac style: Y'all care about the fetus but not the CHILD! That's not pro-life - that's PRO-BIRTH!

Old men deciding what YOUNG women do! I'm a DEAD man and even I see that's WRONG!

Both sides using women's bodies as POLITICAL FOOTBALL! How about ask the WOMEN?!

This ain't about babies or choice - it's about CONTROL! And you're all falling for it!"""

    else:
        # GENERAL ROAST - Hit EVERYONE (Carlin's approach)
        body = f"""{headline}

Let me tell you about THIS bullshit!

Chappelle's law: "Every group's got problems but acts like they DON'T!"

Republicans want small government that fits in a WOMAN'S UTERUS!

Democrats want free everything but won't say who PAYS!

Rich people hoarding billions! "I earned it!" No you INHERITED it or STOLE it!

Poor people defending billionaires! That's like TURKEYS voting for THANKSGIVING!

Pryor's wisdom: "You know who's honest? KIDS and DRUNKS! Everyone else is LYING!"

Carlin observed: "It's called the American DREAM because you have to be ASLEEP to believe it!"

Bernie Mac would SCREAM: You got healthcare for CONGRESS but not for CITIZENS?!

Robin Williams: "Politicians are like diapers - need changing regularly and for the SAME reason!"

I died believing in democracy. You got OLIGARCHY with better MARKETING!

ALL of you complicit - voting for the same clowns expecting DIFFERENT results! That's INSANITY!"""

    # DARK ENDING (Pryor/Carlin darkness)
    endings = [
        "April 14, 1865. Booth shot me in the HEAD. Nine hours dying.\n\nI saw YOUR future. Thought I'd save it.\n\nI was WRONG. You don't WANT saving. You want DISTRACTIONS.\n\nProve me wrong. I DARE you.\n\nLook in mirrors.",
        
        "Died for this country. Freed the slaves.\n\nNow you're ALL slaves - to debt, to fear, to SCREENS!\n\nCarlin was right: \"You have OWNERS! They OWN you!\"\n\nWake UP or stay ASLEEP. I don't care anymore.\n\nLook in mirrors.",
        
        "Freed four million slaves. You enslaved THREE HUNDRED MILLION!\n\nCongratulations - you EVOLVED backwards!\n\nPryor laughing in heaven: \"Told you so!\"\n\nYou want change? Start with the MIRROR.\n\nLook in mirrors.",
        
        "Preserved the Union. You're DESTROYING it for PROFIT!\n\nBoth sides rob you blind while you FIGHT EACH OTHER!\n\nThat's the GAME! And you're losing!\n\nBernie Mac yelling from heaven: \"WAKE UP!\"\n\nLook in mirrors.",
    ]
    
    ending = random.choice(endings)
    
    return f"{intro}\n\n{body}\n\n{ending}"


# GOOGLE SHEETS INTEGRATION
def log_to_google_sheets(episode_num, headline, script_length, video_path, youtube_url):
    """
    Track video generation in Google Sheets
    Sheet columns: Episode, Headline, Script Length, Views, Retention, Upload Date, YouTube URL
    """
    try:
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build
        from datetime import datetime
        
        # Your Google Sheets credentials (service account)
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        SERVICE_ACCOUNT_FILE = 'config/google_sheets_credentials.json'
        SPREADSHEET_ID = os.getenv('GOOGLE_SHEETS_ID', 'YOUR_SHEET_ID_HERE')
        
        if not Path(SERVICE_ACCOUNT_FILE).exists():
            print("[Google Sheets] Credentials not found - skipping tracking")
            return False
        
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        
        # Prepare row data
        row_data = [
            episode_num,
            headline,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            script_length,
            str(video_path),
            youtube_url if youtube_url else 'Pending',
            0,  # Views (will update later)
            0,  # Retention (will update later)
            'Active'  # Status
        ]
        
        # Append to sheet
        range_name = 'Sheet1!A:I'
        body = {'values': [row_data]}
        result = service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name,
            valueInputOption='USER_ENTERED',
            body=body
        ).execute()
        
        print(f"[Google Sheets] Logged episode #{episode_num}")
        return True
        
    except Exception as e:
        print(f"[Google Sheets] Error: {e}")
        return False


if __name__ == "__main__":
    # Test dark comedy generation
    test_headlines = [
        "Trump Indicted on 91 Charges",
        "Biden Forgets Name of Country He's President Of",
        "Police Shoot Unarmed Black Man",
        "Stock Market Crashes, Rich People Sad",
        "Climate Summit: Private Jets Discuss Carbon Footprint",
    ]
    
    print("\n" + "="*70)
    print("  DARK SATIRICAL COMEDY TEST")
    print("="*70 + "\n")
    
    for headline in test_headlines:
        print(f"\n{'='*70}")
        print(f"HEADLINE: {headline}")
        print(f"{'='*70}\n")
        script = generate_dark_satirical_script(headline)
        print(script)
        print(f"\nWord count: {len(script.split())}")
        print(f"Characters: {len(script)}")
        print("\n")

