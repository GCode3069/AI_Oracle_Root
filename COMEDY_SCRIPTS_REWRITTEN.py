#!/usr/bin/env python3
"""
COMEDY SCRIPTS REWRITTEN - Actually Funny Edition
Fresh, modern comedy that doesn't rely on tired formulas
Multiple comedy styles for variety, not just angry roasts
"""

import random
from typing import Dict, List

class ModernComedyGenerator:
    """
    Generate genuinely funny scripts using modern comedy techniques:
    - Observational humor (Seinfeld, John Mulaney)
    - Absurdist comedy (Tim Robinson, Eric Andre)
    - Dry wit (Norm MacDonald, Steven Wright)
    - Self-deprecating humor (Mike Birbiglia, Pete Davidson)
    - Satirical commentary (John Oliver, Hasan Minhaj)
    - Deadpan delivery (Aubrey Plaza, Anthony Jeselnik)
    - Relatable millennial/Gen Z humor
    """
    
    def __init__(self):
        self.styles = {
            'observational': self.observational_comedy,
            'absurdist': self.absurdist_comedy,
            'dry_wit': self.dry_wit_comedy,
            'self_deprecating': self.self_deprecating_comedy,
            'satirical': self.satirical_comedy,
            'deadpan': self.deadpan_comedy,
            'relatable': self.relatable_comedy,
            'surreal': self.surreal_comedy
        }
    
    def observational_comedy(self, headline: str) -> str:
        """Seinfeld/Mulaney style observational humor"""
        topic = headline.split(':')[0] if ':' in headline else headline[:30]
        
        templates = [
            f"""So I'm reading about {topic.lower()}... and I'm thinking... 
            
            Have you noticed how news headlines are basically just Mad Libs now? 
            
            "{topic}" could literally be anything. "Cat learns Spanish." "Mayor fights cloud." 
            Same level of surprise at this point.
            
            We've reached peak news saturation where everything is equally shocking and boring.
            Like when your friend tells you the same story for the fifth time but changes one detail.
            
            "Oh, THIS time the government is concerned? Fascinating."
            
            Anyway, Bitcoin's still here. Unlike my will to read headlines.""",
            
            f"""You ever notice how {topic.lower()} always happens right when we collectively forget about the last {topic.lower()}?
            
            It's like the universe has a calendar reminder: "Time for another one of these!"
            
            And we all act surprised. Every. Single. Time.
            
            "Oh no! Not {topic}! Who could have predicted this completely predictable thing?"
            
            I'm starting to think we're all NPCs in someone's poorly written simulation.
            The dialogue never changes, just the graphics get slightly worse.
            
            Bitcoin below. It's the only consistent plot point.""",
            
            f"""Here's what kills me about {topic.lower()}...
            
            Everyone's got an opinion. Your uncle, your barista, that guy at the gym who only does bicep curls.
            
            Nobody knows what they're talking about, but boy do they have THOUGHTS.
            
            It's like watching toddlers argue about quantum physics.
            Adorable? Sure. Helpful? Absolutely not.
            
            Meanwhile, actual experts are screaming into the void while we listen to @TruthWarrior69.
            
            This is fine. Everything's fine. Bitcoin address below."""
        ]
        
        return random.choice(templates)
    
    def absurdist_comedy(self, headline: str) -> str:
        """Tim Robinson/Eric Andre style absurdist humor"""
        topic = headline.split(':')[0] if ':' in headline else headline[:30]
        
        templates = [
            f"""BREAKING: {topic} happened and my immediate response was to eat an entire sleeve of crackers.
            
            Not because I was hungry. Because that's what you do now.
            
            Crisis? Crackers.
            Good news? Crackers.
            Tuesday? Believe it or not, crackers.
            
            I've become a human parrot who processes world events through wheat products.
            
            This is journalism now. Me. Crackers. Existential dread.
            
            Anyway here's my Bitcoin address. Use it to buy crackers.""",
            
            f"""So {topic.lower()} is trending and I just want everyone to know:
            
            I once saw a pigeon steal a whole bagel and that was more organized than our response to literally anything.
            
            That pigeon had a PLAN. Goals. Direction.
            
            We have Twitter arguments and microwave dinners.
            
            The pigeon is winning. The pigeon has always been winning.
            
            I'm not saying invest in pigeons instead of Bitcoin, but... 
            Actually no, stick with Bitcoin. Address below.""",
            
            f"""{topic}? Cool. Cool cool cool.
            
            Yesterday I watched a YouTube video of a man reviewing different brands of dirt for 47 minutes.
            
            It had 3 million views.
            
            We're all just entertaining ourselves while the world does whatever it wants.
            
            Like those toy monkeys with cymbals. Clapping. Always clapping. 
            Even after the battery dies, the echo of clapping remains.
            
            That's us. That's humanity.
            
            Anyway, Bitcoin. It's like dirt but digital."""
        ]
        
        return random.choice(templates)
    
    def dry_wit_comedy(self, headline: str) -> str:
        """Norm MacDonald/Steven Wright style dry wit"""
        topic = headline.split(':')[0] if ':' in headline else headline[:30]
        
        templates = [
            f"""{topic}.
            
            You know what's funny about {topic.lower()}? Nothing. Absolutely nothing.
            
            But we'll pretend it matters for about 72 hours.
            Then something else will happen and we'll pretend THAT matters.
            
            It's like a very boring magic trick where the rabbit never appears but we keep clapping anyway.
            
            The real magic is convincing ourselves any of this affects our actual lives.
            
            Spoiler: It doesn't.
            
            Bitcoin address below. That also doesn't matter, but at least it's honest about it.""",
            
            f"""They say {topic.lower()} is important news.
            
            I say the most important news I got today was that my houseplant is still alive.
            
            That's a miracle. {topic}? That's Tuesday.
            
            We've normalized chaos to the point where stability is suspicious.
            
            "Everything's fine today."
            "What's the catch?"
            "No catch."
            "That's exactly what someone with a catch would say."
            
            Bitcoin below. No catch. Which means there's definitely a catch.""",
            
            f"""So {topic.lower()} happened.
            
            In related news, I had a sandwich for lunch.
            
            These two facts are equally relevant to your life.
            
            Actually, the sandwich might be more relevant. 
            At least you know what a sandwich is.
            
            Can anyone actually explain what {topic.lower()} means? 
            Without using the words "unprecedented" or "historic"?
            
            Didn't think so.
            
            Bitcoin address below. It's like a sandwich but for the internet."""
        ]
        
        return random.choice(templates)
    
    def self_deprecating_comedy(self, headline: str) -> str:
        """Mike Birbiglia/Pete Davidson style self-deprecating humor"""
        topic = headline.split(':')[0] if ':' in headline else headline[:30]
        
        templates = [
            f"""Look, I died in 1865 and even I think {topic.lower()} is depressing.
            
            I got shot in the head at a play. A COMEDY, by the way.
            Talk about reading the room wrong.
            
            But at least my assassination had style. Drama. A guy jumping from a balcony yelling Latin.
            
            {topic}? That's just... sad. No pageantry. No theatrical flair.
            
            We used to put effort into our disasters.
            
            Now it's just notifications and resignation.
            
            Here's my Bitcoin address. I don't know what Bitcoin is. I'M DEAD.""",
            
            f"""Abraham Lincoln here with breaking news about {topic.lower()}.
            
            Just kidding. I have no idea what's happening. 
            I've been dead for 159 years and honestly? 
            Best career move I ever made.
            
            You think YOUR job is stressful? 
            Try holding a country together with elmers glue and good intentions.
            
            At least you can quit. I had to get assassinated.
            One star. Would not recommend.
            
            Bitcoin below. It's probably less complicated than the Electoral College.""",
            
            f"""{topic} is trending and I'm supposed to have takes.
            
            Hot take: I'm 6'4" and still couldn't see this coming.
            
            Cold take: Being tall doesn't help you understand anything.
            It just means you hit your head on more things.
            
            Room temperature take: I freed the slaves and still got a C+ from historians.
            
            You can't win. Don't try.
            
            Bitcoin address below. At least it's not trying to impress anyone."""
        ]
        
        return random.choice(templates)
    
    def satirical_comedy(self, headline: str) -> str:
        """John Oliver/Hasan Minhaj style satirical commentary"""
        topic = headline.split(':')[0] if ':' in headline else headline[:30]
        
        templates = [
            f"""Oh good! {topic}! Just what we needed!
            
            You know what this reminds me of? 
            That time we all agreed to stop doing the thing that causes the problem.
            
            Then we immediately did that thing. 
            But harder. With more commitment.
            
            It's like we're speedrunning civilization collapse but keep hitting the wrong buttons.
            
            "Maybe if we press them HARDER?"
            
            No, Karen. That's not how buttons work.
            
            Bitcoin below. It's the only button that does something predictable.""",
            
            f"""BREAKING: {topic} shocks nation that has redefined shock to mean "mild surprise."
            
            Remember when shocking meant actually shocking?
            Now it means "thing that was inevitable happened on schedule."
            
            We've Stockholm Syndrome'd ourselves into accepting chaos as comfort.
            
            "At least it's familiar chaos!"
            
            That's not a silver lining. That's aluminum foil spray-painted silver.
            We know the difference but we're too tired to care.
            
            Bitcoin: For when you've given up but still want to participate.""",
            
            f"""Let me explain {topic.lower()} using a metaphor you'll understand:
            
            Imagine a house is on fire.
            Now imagine debating what color to paint the house.
            While it's on fire.
            And you're inside.
            
            That's {topic.lower()}.
            
            We're really good at solving the wrong problems with incredible efficiency.
            
            It's almost impressive. Like watching someone parallel park during an earthquake.
            Technically skillful. Practically useless.
            
            Bitcoin below. At least it's honest about being complicated."""
        ]
        
        return random.choice(templates)
    
    def deadpan_comedy(self, headline: str) -> str:
        """Aubrey Plaza/Anthony Jeselnik style deadpan delivery"""
        topic = headline.split(':')[0] if ':' in headline else headline[:30]
        
        templates = [
            f"""{topic}.
            
            Wow.
            
            I'm so surprised.
            
            This is my surprised face.
            
            You can't see it because I'm dead, but trust me.
            Very surprised.
            
            Anyway, Bitcoin address below.
            
            Act shocked.""",
            
            f"""News: {topic.lower()}.
            
            Me: Dead.
            
            You: Alive but wishing you weren't.
            
            The economy: Having a moment.
            
            My will to live: See line 2.
            
            Bitcoin: Still exists somehow.
            
            Address below.
            
            Use it or don't. 
            
            Nothing matters.""",
            
            f"""{topic} happened.
            
            Everyone's upset.
            
            I was already upset so this changes nothing.
            
            It's like being double-parked in hell.
            
            The second violation doesn't make it worse.
            
            You're already in hell.
            
            Bitcoin below.
            
            It's not hell but it's trying."""
        ]
        
        return random.choice(templates)
    
    def relatable_comedy(self, headline: str) -> str:
        """Millennial/Gen Z relatable humor"""
        topic = headline.split(':')[0] if ':' in headline else headline[:30]
        
        templates = [
            f"""POV: You're reading about {topic.lower()} while pretending to work.
            
            Your boss is in a meeting about meetings.
            You're on hour 3 of "quick sync" energy.
            
            The news is bad but your attention span is worse.
            
            You'll forget about {topic.lower()} by lunch.
            Unless it trends on TikTok.
            Then you'll have a very strong opinion for exactly 48 seconds.
            
            This is adult life now.
            We're all just winging it with WiFi.
            
            Bitcoin below. It's like a 401k but spicy.""",
            
            f"""{topic} is giving "season finale of democracy" vibes and honestly? 
            
            I'm too tired to care.
            
            I've been tired since 1865 and you've been tired since 2016.
            
            We're all running on anxiety and iced coffee.
            
            The planet's dying but my succulent is THRIVING.
            Small wins.
            
            Is this wellness? Is this self-care?
            No, this is a Wendy's.
            
            Bitcoin address below. No this is not financial advice.
            This is barely advice.""",
            
            f"""Nobody:
            
            Absolutely nobody:
            
            The news: {topic}!!!!
            
            Me: I just wanted to scroll in peace.
            
            But no. We can't have nice things.
            We can't even have mediocre things.
            We get {topic.lower()} and we'll like it.
            
            Except we won't like it.
            We'll tweet about it for a day then move on to the next thing.
            
            The cycle continues.
            Mercury is probably in retrograde.
            
            Bitcoin below. Mercury can't retrograde Bitcoin. 
            I think. I don't know. I'm dead."""
        ]
        
        return random.choice(templates)
    
    def surreal_comedy(self, headline: str) -> str:
        """Surreal, unexpected humor"""
        topic = headline.split(':')[0] if ':' in headline else headline[:30]
        
        templates = [
            f"""I had a dream where {topic.lower()} was actually just millions of bees in a trench coat.
            
            When I woke up, I realized that would make MORE sense than reality.
            
            At least bees have a purpose. A plan. A queen.
            
            What do we have? Headlines and heartburn.
            
            The bees are laughing at us.
            In their little bee language.
            Which is probably more sophisticated than Twitter.
            
            Bitcoin address below.
            The bees cannot use it but you can.""",
            
            f"""{topic} broke and honestly? 
            
            I'm more concerned about the fact that somewhere, right now, 
            a banana is becoming too ripe and someone will have to make banana bread.
            
            They don't want to make banana bread.
            Nobody WANTS to make banana bread.
            
            But the banana demands it.
            The banana always wins.
            
            {topic}? That's temporary.
            The banana bread obligation? Eternal.
            
            Bitcoin below. You can't make bread with it.""",
            
            f"""Scientists say {topic.lower()} is concerning.
            
            Scientists also say octopi have three hearts and can open jars.
            
            Which fact affects your life more?
            
            Be honest.
            
            When the octopi rise up, {topic.lower()} won't matter.
            
            They'll have all the jars.
            We'll have none.
            
            Game over.
            
            Bitcoin below. The octopi don't want it. Yet."""
        ]
        
        return random.choice(templates)
    
    def generate(self, headline: str, style: str = None, word_limit: int = 150) -> str:
        """Generate comedy script with specified style or random selection"""
        
        if style and style in self.styles:
            script = self.styles[style](headline)
        else:
            # Random selection for variety
            style = random.choice(list(self.styles.keys()))
            script = self.styles[style](headline)
        
        # Add Bitcoin address if not already present
        if "bitcoin" not in script.lower():
            script += "\n\nBitcoin: bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"
        
        # Trim to word limit if needed
        words = script.split()
        if len(words) > word_limit:
            script = ' '.join(words[:word_limit]) + '...\n\nBitcoin below.'
        
        return script, style


class ComedyScriptPackage:
    """Pre-written comedy packages for different moods/topics"""
    
    def __init__(self):
        self.packages = {
            'politics': self.political_comedy,
            'tech': self.tech_comedy,
            'economy': self.economy_comedy,
            'social': self.social_comedy,
            'climate': self.climate_comedy
        }
    
    def political_comedy(self) -> List[Dict]:
        """Political comedy that's actually funny, not just angry"""
        return [
            {
                'title': 'Lincoln Reacts to Modern Politics',
                'script': """I was a lawyer who became president.
                
                Now you need to be a president to afford a lawyer.
                
                Progress!
                
                Both parties hate each other so much, they'd rather burn down the house than share it.
                And they're both holding matches wondering why it's getting hot.
                
                I united the country.
                You can't unite a Zoom call.
                
                The bar has fallen so low, it's technically a speed bump.
                
                Bitcoin below. It's bipartisan in that nobody understands it."""
            },
            {
                'title': 'Lincoln on Congressional Productivity',
                'script': """Congress passed 27 bills this year.
                
                I passed more bills having dysentery.
                
                These people took more vacation days than work days.
                Then complained about how hard their job is.
                
                That's like me complaining about hat hair.
                I CHOSE THE HAT, KAREN.
                
                They get paid $174,000 to argue on Twitter.
                You do that for free.
                
                Who's the real fool here?
                
                Bitcoin below. At least it actually does something."""
            }
        ]
    
    def tech_comedy(self) -> List[Dict]:
        """Tech humor that's relatable"""
        return [
            {
                'title': 'Lincoln vs AI',
                'script': """AI is going to take all our jobs.
                
                Bold of you to assume you had a job to begin with.
                
                We're worried about robots replacing us while we voluntarily talk to Alexa more than our families.
                
                "Alexa, what's the weather?"
                Look outside, Timothy. Use your human eyes.
                
                I wrote the Gettysburg Address with a pencil.
                You need ChatGPT to write an email.
                
                The robots already won. They're just being polite about it.
                
                Bitcoin below. It's like AI but with more math anxiety."""
            },
            {
                'title': 'Lincoln on Social Media',
                'script': """Everyone's an expert on Twitter.
                
                Yesterday's expert on Ukraine is today's expert on banking.
                Tomorrow they'll be an expert on whatever's trending.
                
                It's like watching someone speedrun the Dunning-Kruger effect.
                
                I had to actually know things to be president.
                Now you just need wifi and confidence.
                
                We've democratized stupidity.
                That's... actually very American.
                
                I'm proud? Concerned? Both?
                
                Bitcoin below. No expertise required."""
            }
        ]
    
    def economy_comedy(self) -> List[Dict]:
        """Economic humor without being preachy"""
        return [
            {
                'title': 'Lincoln on Inflation',
                'script': """Everything costs more but your salary stayed the same.
                
                It's like reverse evolution.
                We're getting worse at math while the math gets harder.
                
                A house costs 50 years of salary.
                My house was made of LOGS and it was still more affordable.
                
                "Just stop buying avocado toast!"
                Sure, that $12 is the difference between renting and owning.
                
                You solved poverty, Keith. Nobel Prize incoming.
                
                Bitcoin below. It's inflated too but at least it admits it."""
            },
            {
                'title': 'Lincoln on the Job Market',  
                'script': """Entry level job: Requires 10 years experience.
                
                That's like asking a baby to have references from the womb.
                
                "Nobody wants to work!"
                Nobody wants to work for less than rent costs, Bradley.
                
                There's a difference.
                
                I split rails for money.
                You split hairs for exposure.
                
                We are not the same.
                
                Bitcoin below. Mining it is somehow a more stable career path."""
            }
        ]
    
    def social_comedy(self) -> List[Dict]:
        """Social commentary that's clever, not cruel"""
        return [
            {
                'title': 'Lincoln on Modern Dating',
                'script': """Dating apps ruined romance.
                
                You swipe through humans like a deck of cards.
                "Nope, nope, maybe, nope, oh they're holding a fish, NOPE."
                
                I courted Mary Todd for years.
                You ghost someone after two texts.
                
                "They used the wrong emoji. Red flag!"
                
                The red flag is that you're evaluating humans based on emoji usage.
                
                We've gamified loneliness.
                
                Bitcoin below. At least it can't ghost you."""
            },
            {
                'title': 'Lincoln on Wellness Culture',
                'script': """Everyone's optimizing their morning routine.
                
                Cold plunge, meditation, journaling, gratitude, yoga, supplements...
                
                By the time you're done optimizing, it's noon.
                
                I woke up, went to work, tried not to die from consumption.
                Simple. Effective. No subscription required.
                
                You pay someone to tell you to breathe.
                BREATHING IS FREE, JENNIFER.
                
                The only thing you're optimizing is someone else's bank account.
                
                Bitcoin below. You can't optimize it but you'll try."""
            }
        ]
    
    def climate_comedy(self) -> List[Dict]:
        """Climate humor that's not depressing"""
        return [
            {
                'title': 'Lincoln on Climate Debates',
                'script': """We're debating if climate change is real while Miami develops gills.
                
                That's like debating if water is wet while drowning.
                
                "But it snowed today!"
                Congratulations, you've discovered weather.
                
                Next you'll discover that night happens after day.
                Revolutionary stuff.
                
                The planet will be fine. It survived dinosaurs.
                We're just the awkward phase between dinosaurs and whatever's next.
                
                Probably dolphins. Smart money's on dolphins.
                
                Bitcoin below. It uses more energy than Argentina but so does your Netflix habit."""
            }
        ]
    
    def get_random_package(self) -> Dict:
        """Get random comedy script from any package"""
        category = random.choice(list(self.packages.keys()))
        scripts = self.packages[category]()
        return random.choice(scripts)


def generate_video_script(headline: str, style: str = None) -> Dict:
    """Main function to generate a comedy video script"""
    
    generator = ModernComedyGenerator()
    
    # Generate script with specified or random style
    script, used_style = generator.generate(headline, style)
    
    # Create title
    episode = random.randint(1000, 9999)
    title = f"Lincoln Reacts #{episode}: {headline[:40]}... #Shorts"
    
    return {
        'title': title,
        'script': script,
        'style': used_style,
        'episode': episode,
        'tags': generate_tags(headline, used_style)
    }


def generate_tags(headline: str, style: str) -> List[str]:
    """Generate relevant tags for YouTube"""
    
    base_tags = [
        'comedy', 'shorts', 'lincolnreacts', 'funnyshorts', 
        'comedyshorts', 'abraham', 'satire', 'humor'
    ]
    
    style_tags = {
        'observational': ['observationalcomedy', 'standup', 'seinfeld', 'mulaney'],
        'absurdist': ['absurdist', 'surreal', 'timrobinson', 'weirdcomedy'],
        'dry_wit': ['drywit', 'deadpan', 'normmaconald', 'darkhumor'],
        'self_deprecating': ['selfdeprecating', 'relatable', 'mikebirbiglia'],
        'satirical': ['satire', 'politicalhumor', 'johnoliver', 'socialcommentary'],
        'deadpan': ['deadpan', 'dryhumor', 'aubreyplaza', 'darkcomedy'],
        'relatable': ['relatable', 'millennial', 'genz', 'modernlife'],
        'surreal': ['surreal', 'weird', 'unexpected', 'absurd']
    }
    
    # Add style-specific tags
    if style in style_tags:
        base_tags.extend(style_tags[style])
    
    # Add topic-based tags from headline
    topic_words = headline.lower().split()[:5]
    base_tags.extend([word for word in topic_words if len(word) > 4])
    
    return list(set(base_tags))[:20]  # YouTube limit


if __name__ == "__main__":
    # Test the new comedy system
    test_headlines = [
        "Government Shutdown Day 15: No End in Sight",
        "Tech Billionaire Buys Another Company",
        "Climate Summit Ends Without Agreement",
        "New Study Shows People Are Stressed",
        "Congress Debates Something Irrelevant Again"
    ]
    
    print("=" * 70)
    print("COMEDY SCRIPTS - ACTUALLY FUNNY EDITION")
    print("=" * 70)
    
    generator = ModernComedyGenerator()
    package = ComedyScriptPackage()
    
    # Test different styles
    for headline in test_headlines[:2]:
        print(f"\nHeadline: {headline}")
        print("-" * 50)
        
        result = generate_video_script(headline)
        
        print(f"Style: {result['style'].upper()}")
        print(f"Title: {result['title']}")
        print(f"\nScript:\n{result['script']}")
        print(f"\nTags: {', '.join(result['tags'][:10])}")
        print("=" * 70)
    
    # Test pre-written package
    print("\n\nPRE-WRITTEN COMEDY PACKAGE")
    print("-" * 50)
    
    random_script = package.get_random_package()
    print(f"Title: {random_script['title']}")
    print(f"\nScript:\n{random_script['script']}")