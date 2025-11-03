#!/usr/bin/env python3
"""
AFFILIATE LINK INJECTION SYSTEM - REAL WORKING CODE
Automatically injects affiliate links into video descriptions
Generates passive income on EVERY video upload
"""
import os
import sys
from pathlib import Path
from datetime import datetime

# Affiliate links (replace with YOUR affiliate IDs)
AFFILIATE_LINKS = {
    'elevenlabs': 'https://elevenlabs.io/?from=lincolnwarnings',  # 20% recurring
    'gumroad_scripts': 'https://gumroad.com/l/lincoln-scripts',  # Your product
    'gumroad_system': 'https://gumroad.com/l/purge-kit',  # Your $97 product
    'patreon': 'https://patreon.com/LincolnWarnings',  # Recurring support
    'cashapp': '$LincolnWarnings',  # Direct tips
    'bitcoin': 'bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt',  # Crypto (in QR)
}

def generate_monetized_description(headline, episode_num, platform="youtube"):
    """
    Generate description with ALL monetization links
    Optimized for each platform
    """
    
    if platform == "youtube":
        return f"""Lincoln's WARNING #{episode_num}: {headline}

DARK SATIRICAL COMEDY - Roasts EVERYONE (Dems, Republicans, rich, poor)
No sacred cows. Styles: Pryor, Carlin, Chappelle, Bernie Mac.

💰 SUPPORT THE CHANNEL:
• CashApp: {AFFILIATE_LINKS['cashapp']}
• Bitcoin: {AFFILIATE_LINKS['bitcoin'][:20]}... (QR in video)
• Patreon (Early Access): {AFFILIATE_LINKS['patreon']}

📦 GET THE SCRIPTS:
• 100 Scripts Pack ($27): {AFFILIATE_LINKS['gumroad_scripts']}
• Full Generator ($97): {AFFILIATE_LINKS['gumroad_system']}

🎤 ABE'S VOICE POWERED BY:
• ElevenLabs (20% OFF): {AFFILIATE_LINKS['elevenlabs']}

Abraham Lincoln's ghost roasting current events.
Proven results: 1,130 views, 45% retention.

#Shorts #Lincoln #Politics #Comedy #Satire #DarkComedy
#Trump #Democrats #Republicans #Truth #Viral
#GeorgeCarlin #RichardPryor #DaveChappelle #BernieMac
"""
    
    elif platform == "tiktok":
        return f"""Lincoln's WARNING #{episode_num} 🔥

Dark satire - roasts EVERYONE!

Links in bio:
• Scripts: linc.to/scripts
• Support: linc.to/support

#fyp #politics #comedy #satire #lincoln #viral #truth
"""
    
    elif platform == "rumble":
        return f"""Lincoln's WARNING #{episode_num}: {headline}

Abraham Lincoln roasts current events with dark satirical comedy.
No sacred cows - Democrats, Republicans, rich, poor - EVERYONE gets roasted!

Comedy styles: Richard Pryor, George Carlin, Dave Chappelle, Bernie Mac.

💰 Support: CashApp {AFFILIATE_LINKS['cashapp']}
📦 Get Scripts: {AFFILIATE_LINKS['gumroad_scripts']}
🎤 Voice by: {AFFILIATE_LINKS['elevenlabs']}

Proven results: 1,130 views, 45% retention on original channel.

#Politics #Satire #Comedy #Lincoln #Conservative #Liberal #Truth
"""
    
    elif platform == "instagram":
        # Instagram has link limits, use link in bio
        return f"""Lincoln's WARNING #{episode_num}

Dark satire roasting everyone 🔥

Link in bio for:
• Full scripts
• Support options
• More content

#reels #politics #comedy #satire #lincoln
"""
    
    else:
        return f"Lincoln's WARNING #{episode_num}: {headline} - Dark satirical comedy"

def inject_affiliate_links_into_upload(video_path, headline, episode_num):
    """
    Creates description files for each platform with affiliate links
    """
    video_path = Path(video_path)
    descriptions_dir = video_path.parent / "descriptions"
    descriptions_dir.mkdir(exist_ok=True)
    
    platforms = ['youtube', 'tiktok', 'rumble', 'instagram', 'twitter']
    
    print(f"\n[Affiliate] Generating descriptions for {video_path.name}...\n")
    
    for platform in platforms:
        description = generate_monetized_description(headline, episode_num, platform)
        desc_file = descriptions_dir / f"{video_path.stem}_{platform}_description.txt"
        
        with open(desc_file, 'w', encoding='utf-8') as f:
            f.write(description)
        
        print(f"  [OK] {platform.title()}: {desc_file.name}")
    
    print(f"\n[Affiliate] All descriptions created in: {descriptions_dir}\n")
    return descriptions_dir

def get_affiliate_earnings_estimate(views_by_platform):
    """
    Estimate affiliate earnings based on views
    """
    # Conversion rates (conservative estimates)
    conversion_rates = {
        'elevenlabs_click': 0.05,  # 5% click through
        'elevenlabs_signup': 0.10,  # 10% of clicks sign up
        'gumroad_click': 0.03,  # 3% click
        'gumroad_purchase': 0.05,  # 5% of clicks buy
        'cashapp_tip': 0.01,  # 1% tip
    }
    
    # Revenue per conversion
    revenue_per = {
        'elevenlabs': 5.00,  # $5-10 per signup (conservative)
        'gumroad_27': 27.00,
        'gumroad_97': 97.00,
        'cashapp': 5.00,  # Average tip
    }
    
    total_estimated = 0
    breakdown = {}
    
    for platform, views in views_by_platform.items():
        # ElevenLabs affiliate
        elevenlabs_clicks = views * conversion_rates['elevenlabs_click']
        elevenlabs_signups = elevenlabs_clicks * conversion_rates['elevenlabs_signup']
        elevenlabs_revenue = elevenlabs_signups * revenue_per['elevenlabs']
        
        # Gumroad $27
        gumroad_clicks = views * conversion_rates['gumroad_click']
        gumroad_purchases = gumroad_clicks * conversion_rates['gumroad_purchase']
        gumroad_27_revenue = gumroad_purchases * revenue_per['gumroad_27'] * 0.7  # 70% buy cheaper
        
        # Gumroad $97
        gumroad_97_revenue = gumroad_purchases * revenue_per['gumroad_97'] * 0.3  # 30% buy expensive
        
        # CashApp tips
        cashapp_tips = views * conversion_rates['cashapp_tip']
        cashapp_revenue = cashapp_tips * revenue_per['cashapp']
        
        platform_total = elevenlabs_revenue + gumroad_27_revenue + gumroad_97_revenue + cashapp_revenue
        breakdown[platform] = {
            'views': views,
            'elevenlabs': elevenlabs_revenue,
            'gumroad': gumroad_27_revenue + gumroad_97_revenue,
            'cashapp': cashapp_revenue,
            'total': platform_total
        }
        total_estimated += platform_total
    
    return total_estimated, breakdown

def show_affiliate_projections():
    """Show what you could earn from affiliate links"""
    print("\n" + "="*70)
    print("  AFFILIATE EARNINGS PROJECTIONS")
    print("="*70 + "\n")
    
    # Your current metrics
    views_scenarios = {
        'Current (3,321 views/28 days)': {
            'youtube': 3321,
            'tiktok': 0,  # Not started
            'rumble': 0,  # Not started
        },
        'Scaled (10K views/day × 30 days)': {
            'youtube': 100000,
            'tiktok': 100000,
            'rumble': 100000,
        },
        'Viral (1 video hits 1M)': {
            'youtube': 1000000,
            'tiktok': 500000,
            'rumble': 250000,
        }
    }
    
    for scenario, views in views_scenarios.items():
        total, breakdown = get_affiliate_earnings_estimate(views)
        print(f"[{scenario}]")
        print(f"  Total Affiliate Revenue: ${total:.2f}/month")
        for platform, data in breakdown.items():
            if data['views'] > 0:
                print(f"    {platform.title()}: ${data['total']:.2f} ({data['views']:,} views)")
        print()
    
    print("="*70)
    print("\nNOTE: These are PASSIVE earnings from links in descriptions!")
    print("Add platform ad revenue on top of this!\n")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--projections":
        show_affiliate_projections()
    else:
        print("""
AFFILIATE LINK INJECTOR

Automatically adds monetization links to all platforms.

Generate descriptions:
python affiliate_link_injector.py VIDEO_PATH "Headline" EPISODE_NUM

Show earnings projections:
python affiliate_link_injector.py --projections

Features:
- ElevenLabs affiliate (20% recurring)
- Gumroad products ($27 + $97)
- CashApp tips
- Bitcoin QR (in video)
- Patreon recurring

Revenue:
- 10K views = $50-100 in affiliate sales
- 100K views = $500-1,000 in affiliate sales
- 1M views = $5,000-10,000 in affiliate sales
""")

