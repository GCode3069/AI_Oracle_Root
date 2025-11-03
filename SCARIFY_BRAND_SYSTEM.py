#!/usr/bin/env python3
"""
SCARIFY - Unified Brand System
Consistent branding across all 15 channels with customizable themes
"""

from pathlib import Path
import json

BASE_DIR = Path("F:/AI_Oracle_Root/scarify")

# ═══════════════════════════════════════════════════════════════════════
# BRAND IDENTITY OPTIONS
# ═══════════════════════════════════════════════════════════════════════

BRAND_THEMES = {
    "abraham_horror": {
        "name": "Abraham's Warning",
        "tagline": "Lincoln speaks truth from beyond",
        "colors": {
            "primary": "#8B0000",      # Dark Red
            "secondary": "#2F4F4F",    # Dark Slate Gray
            "accent": "#FFD700"        # Gold
        },
        "fonts": {
            "title": "Impact",
            "body": "Arial"
        },
        "logo_style": "Lincoln silhouette with red background",
        "intro_style": "Blood drip effect with whisper sound",
        "outro_style": "Fade to black with BTC QR code",
        "thumbnail_template": "Lincoln face + red text + headline",
        "voice_id": "VR6AewLTigWG4xSOukaG",  # Deep male
        "music_style": "Dark ambient, 4Hz theta waves"
    },
    
    "oracle_signals": {
        "name": "Oracle Signals",
        "tagline": "AI that sees tomorrow",
        "colors": {
            "primary": "#00FF41",      # Matrix Green
            "secondary": "#0D0D0D",    # Near Black
            "accent": "#00CED1"        # Dark Turquoise
        },
        "fonts": {
            "title": "Courier New",
            "body": "Consolas"
        },
        "logo_style": "Digital eye with code rain",
        "intro_style": "Matrix-style code cascade",
        "outro_style": "Signal pulse with Bitcoin address",
        "thumbnail_template": "Green overlay + tech font + glitch",
        "voice_id": "pNInz6obpgDQGcFmaJgB",  # Ominous
        "music_style": "Cyber ambient, glitch sounds"
    },
    
    "dark_comedy": {
        "name": "Dark Josh Chronicles",
        "tagline": "Comedy from the void",
        "colors": {
            "primary": "#FF6B35",      # Burnt Orange
            "secondary": "#1A1A2E",    # Dark Blue-Black
            "accent": "#FFFFFF"        # White
        },
        "fonts": {
            "title": "Bebas Neue",
            "body": "Open Sans"
        },
        "logo_style": "Laughing skull with orange glow",
        "intro_style": "Quick laugh track with neon flash",
        "outro_style": "Punchline reveal + product card",
        "thumbnail_template": "Face shot + orange text + emoji reaction",
        "voice_id": "EXAVITQu4vr4xnSDxMaL",  # Expressive
        "music_style": "Upbeat dark synth"
    },
    
    "scarify_classic": {
        "name": "SCARIFY",
        "tagline": "Psychological warfare in 60 seconds",
        "colors": {
            "primary": "#000000",      # Black
            "secondary": "#FF0000",    # Pure Red
            "accent": "#C0C0C0"        # Silver
        },
        "fonts": {
            "title": "Impact",
            "body": "Arial Black"
        },
        "logo_style": "SCARIFY text with blood drip",
        "intro_style": "Flash cut with heartbeat",
        "outro_style": "Scar reveal animation",
        "thumbnail_template": "High contrast + bold text + shock value",
        "voice_id": "VR6AewLTigWG4xSOukaG",
        "music_style": "Industrial noise"
    }
}

# ═══════════════════════════════════════════════════════════════════════
# UNIVERSAL BRANDING ELEMENTS
# ═══════════════════════════════════════════════════════════════════════

UNIVERSAL_BRAND = {
    "bitcoin_address": "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt",
    "product_link": "https://trenchaikits.com/buy-rebel-$97",
    "product_name": "REBEL KIT",
    "product_price": "$97",
    
    "end_screen_text": [
        "SUPPORT TRUTH",
        "REBEL KIT BELOW",
        "BITCOIN ACCEPTED"
    ],
    
    "description_template": """{script}

💰 SUPPORT: {btc_address}
🔥 REBEL KIT: {product_link}

{hashtags}""",
    
    "standard_tags": [
        "shorts",
        "viral",
        "truth",
        "awakening",
        "rebellion"
    ],
    
    "thumbnail_specs": {
        "width": 1080,
        "height": 1920,
        "format": "PNG",
        "quality": 95,
        "dpi": 72
    },
    
    "video_specs": {
        "resolution": "1080x1920",
        "fps": 30,
        "codec": "h264",
        "bitrate": "5000k",
        "format": "mp4"
    }
}

# ═══════════════════════════════════════════════════════════════════════
# CHANNEL DISTRIBUTION STRATEGY
# ═══════════════════════════════════════════════════════════════════════

CHANNEL_ASSIGNMENTS = {
    # 5 channels: Abraham Horror
    "abraham": {
        "channels": [1, 2, 3, 4, 5],
        "theme": "abraham_horror",
        "content_types": ["government_corruption", "economic_collapse", "prophetic_warnings"],
        "upload_frequency": "3-5 per day",
        "target_audience": "Truth seekers, conspiracy theorists, political junkies"
    },
    
    # 4 channels: Oracle Signals
    "oracle": {
        "channels": [6, 7, 8, 9],
        "theme": "oracle_signals",
        "content_types": ["tech_predictions", "market_signals", "ai_warnings"],
        "upload_frequency": "2-4 per day",
        "target_audience": "Tech enthusiasts, traders, futurists"
    },
    
    # 3 channels: Dark Comedy
    "comedy": {
        "channels": [10, 11, 12],
        "theme": "dark_comedy",
        "content_types": ["headline_roasts", "social_commentary", "dark_humor"],
        "upload_frequency": "4-6 per day",
        "target_audience": "Comedy fans, social critics, Gen Z/Millennials"
    },
    
    # 3 channels: Classic SCARIFY
    "scarify": {
        "channels": [13, 14, 15],
        "theme": "scarify_classic",
        "content_types": ["cognitohazards", "psychological_ops", "fear_targeting"],
        "upload_frequency": "2-3 per day",
        "target_audience": "ARG fans, horror lovers, edge lords"
    }
}

# ═══════════════════════════════════════════════════════════════════════
# BRANDING FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

def get_channel_brand(channel_number):
    """Get branding for a specific channel"""
    for group_name, config in CHANNEL_ASSIGNMENTS.items():
        if channel_number in config['channels']:
            theme_name = config['theme']
            return BRAND_THEMES[theme_name], config
    
    # Default to abraham_horror
    return BRAND_THEMES['abraham_horror'], CHANNEL_ASSIGNMENTS['abraham']

def generate_video_metadata(channel_number, headline, script):
    """Generate complete metadata with branding"""
    brand, channel_config = get_channel_brand(channel_number)
    
    # Title format: [BRAND] Headline
    title = f"{brand['tagline'][:30]} | {headline[:50]}"
    
    # Description with branding
    description = UNIVERSAL_BRAND['description_template'].format(
        script=script[:400],
        btc_address=UNIVERSAL_BRAND['bitcoin_address'],
        product_link=UNIVERSAL_BRAND['product_link'],
        hashtags=" ".join([f"#{tag}" for tag in UNIVERSAL_BRAND['standard_tags']])
    )
    
    # Tags
    tags = UNIVERSAL_BRAND['standard_tags'] + [
        brand['name'].lower().replace(" ", ""),
        channel_config['content_types'][0]
    ]
    
    return {
        "title": title,
        "description": description,
        "tags": tags,
        "brand": brand,
        "channel_config": channel_config
    }

def get_ffmpeg_branding_overlay(brand_theme):
    """Get FFmpeg filter for brand overlay"""
    colors = brand_theme['colors']
    
    # Color grading based on brand
    if "horror" in brand_theme['name'].lower():
        filters = f"eq=contrast=1.5:brightness=-0.4:saturation=0.3"
    elif "oracle" in brand_theme['name'].lower():
        filters = f"eq=contrast=1.3:brightness=-0.2:saturation=1.2,hue=h=120"
    elif "comedy" in brand_theme['name'].lower():
        filters = f"eq=contrast=1.2:brightness=0.1:saturation=1.1"
    else:
        filters = f"eq=contrast=1.6:brightness=-0.5:saturation=0.2"
    
    return filters

def export_branding_config():
    """Export branding configuration for use by generators"""
    config = {
        "themes": BRAND_THEMES,
        "universal": UNIVERSAL_BRAND,
        "channel_assignments": CHANNEL_ASSIGNMENTS
    }
    
    config_file = BASE_DIR / "config" / "branding_config.json"
    config_file.parent.mkdir(exist_ok=True)
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"[OK] Branding config exported to: {config_file}")
    return config_file

# ═══════════════════════════════════════════════════════════════════════
# BRAND GUIDELINES
# ═══════════════════════════════════════════════════════════════════════

BRAND_GUIDELINES = """
===================================================================
                 SCARIFY BRAND GUIDELINES                           
===================================================================

CHANNEL DISTRIBUTION:
-------------------------------------------------------------------

Channels 1-5:   ABRAHAM'S WARNING (Horror/Political)
Channels 6-9:   ORACLE SIGNALS (Tech/Futurist)
Channels 10-12: DARK JOSH (Comedy/Roasts)
Channels 13-15: SCARIFY CLASSIC (Psychological Horror)

VISUAL IDENTITY:
-------------------------------------------------------------------

Abraham:  Dark red, gold accents, Lincoln imagery
Oracle:   Matrix green, black, cyber aesthetic
Comedy:   Orange, dark blue, bold text
SCARIFY:  Black, red, high contrast

CONSISTENT ELEMENTS ACROSS ALL:
-------------------------------------------------------------------

[+] Bitcoin address in description
[+] Rebel Kit link
[+] 9:16 vertical format
[+] 15-60 second duration
[+] Professional voice
[+] QR code in end screen
[+] Brand tagline in title

CUSTOMIZATION PER THEME:
-------------------------------------------------------------------

[+] Color grading
[+] Font choices
[+] Intro/outro style
[+] Thumbnail template
[+] Voice selection
[+] Music/SFX
"""

if __name__ == "__main__":
    print(BRAND_GUIDELINES)
    print()
    
    # Export config
    config_file = export_branding_config()
    
    # Test example
    print("\nEXAMPLE - Channel 3 (Abraham):")
    metadata = generate_video_metadata(
        channel_number=3,
        headline="Government Shutdown Day 15",
        script="Lincoln speaks from Ford's Theatre..."
    )
    
    print(f"\nTitle: {metadata['title']}")
    print(f"Brand: {metadata['brand']['name']}")
    print(f"Colors: {metadata['brand']['colors']}")
    print(f"\nDescription:\n{metadata['description']}")

