#!/usr/bin/env python3
"""
TikTok Brand Integration Engine for @nunyabeznes2
Integrates dark satirical business horror branding with Lincoln content
"""

import json
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class NunyaBeznes2Brand:
    """Brand integration for @nunyabeznes2 TikTok channel"""
    
    def __init__(self):
        self.brand_assets = {
            'username': '@nunyabeznes2',
            'brand_voice': 'dark_satirical_business',
            'color_palette': ['#FF0000', '#000000', '#FFFFFF'],  # Red, Black, White
            'hashtags': [
                '#nunyabeznes',
                '#businesshorror',
                '#corporatenightmare',
                '#profitsoverpeople',
                '#corporategreed',
                '#capitalismexposed',
                '#darkbusiness',
                '#corporatehorror',
                '#businessnightmare',
                '#corporatetruth'
            ],
            'signature_effects': ['glitch_transitions', 'red_black_filter', 'corporate_logo_stings']
        }
        
        self.branded_content_themes = [
            "Corporate Horror Stories",
            "Business Truth Bombs", 
            "Profit Over People Exposed",
            "Capitalism Nightmares",
            "Corporate Slavery Revealed"
        ]
    
    def inject_brand_voice(self, script: str, horror_style: str) -> str:
        """Adapt Lincoln content to @nunyabeznes2 brand voice"""
        
        brand_adaptations = {
            'slasher': [
                "Corporate America is the real slasher",
                "They're not cutting costs - they're cutting throats",
                "The boardroom body count keeps rising"
            ],
            'supernatural': [
                "The ghost in the corporate machine",
                "Haunted by quarterly earnings", 
                "The phantom profits that haunt workers"
            ],
            'psychological': [
                "The psychological warfare of corporate culture",
                "Gaslighting you into thinking this is normal",
                "The corporate mind games they play"
            ]
        }
        
        adaptation = random.choice(brand_adaptations.get(horror_style, brand_adaptations['psychological']))
        
        # Inject brand voice into script
        branded_script = f"{adaptation}. {script}"
        
        return branded_script
    
    def generate_tiktok_caption(self, topic: str, horror_style: str = 'psychological') -> str:
        """Generate brand-optimized TikTok captions"""
        
        base_captions = [
            f"🚨 {topic} but make it corporate horror 🚨",
            f"Business tip: Stop the {topic} madness",
            f"Corporate America's {topic} secret exposed",
            f"They don't teach this {topic} in business school",
            f"The {topic} they don't want you to know about"
        ]
        
        caption = random.choice(base_captions)
        
        # Add brand hashtags (use top 6)
        hashtag_string = " ".join(self.brand_assets['hashtags'][:6])
        
        full_caption = f"{caption}\n\n{hashtag_string}\n{self.brand_assets['username']}"
        
        # Ensure under 500 characters (TikTok optimal)
        if len(full_caption) > 500:
            full_caption = full_caption[:497] + "..."
        
        return full_caption
    
    def create_brand_visuals(self, base_video_path: str, output_path: str) -> Dict:
        """Add @nunyabeznes2 branding to videos"""
        
        brand_elements = {
            'watermark': 'nunyabeznes2_logo.png (bottom right, 10% opacity)',
            'color_filter': 'Red/black color grade',
            'intro_sting': 'Corporate glitch transition (first 2 seconds)',
            'outro_card': 'Follow @nunyabeznes2 for more corporate horror'
        }
        
        return {
            'branded_video_path': output_path,
            'brand_elements_applied': brand_elements,
            'instructions': f"Apply brand elements to {base_video_path} -> {output_path}"
        }


class TikTokContentStrategy:
    """TikTok-optimized content strategy for @nunyabeznes2"""
    
    def __init__(self):
        self.tiktok_formats = {
            'educational_horror': self.create_educational_horror,
            'trend_jacking': self.create_trend_jacking,
            'story_time': self.create_story_time,
            'pov_content': self.create_pov_content,
            'green_screen': self.create_green_screen
        }
        
        self.trending_sounds = [
            "creepy_horror_sound", "corporate_music", "dark_synthwave",
            "glitch_effects", "suspense_build", "dramatic_drop"
        ]
    
    def create_educational_horror(self, topic: str) -> str:
        """TikTok's favorite: Educational but horrifying"""
        
        formats = [
            f"3 signs your company is {topic}",
            f"How {topic} is destroying your career",
            f"The dark truth about corporate {topic}",
            f"Nobody talks about {topic} in business"
        ]
        
        return random.choice(formats)
    
    def create_trend_jacking(self, topic: str) -> str:
        """Ride trending audio/video formats"""
        
        trends = [
            f"POV: You discover the {topic} secret",
            f"Me realizing {topic} is a scam 💀",
            f"That moment when {topic} hits different",
            f"Nobody: ... Corporate America: {topic}"
        ]
        
        return random.choice(trends)
    
    def create_story_time(self, topic: str) -> str:
        """Story format that performs well on TikTok"""
        
        stories = [
            f"Story time: How {topic} almost destroyed me",
            f"Let me tell you about the {topic} incident",
            f"The day I discovered the {topic} truth",
            f"My {topic} horror story (part 1)"
        ]
        
        return random.choice(stories)
    
    def create_pov_content(self, topic: str) -> str:
        """Point-of-view content for engagement"""
        
        povs = [
            f"POV: You're a CEO realizing {topic}",
            f"POV: You discover the {topic} conspiracy",
            f"POV: Your boss explains {topic} with a straight face",
            f"POV: You read the {topic} fine print"
        ]
        
        return random.choice(povs)
    
    def create_green_screen(self, topic: str) -> str:
        """Green screen trend format"""
        
        screens = [
            f"Reacting to {topic} statistics",
            f"Green screen: The {topic} timeline",
            f"Breaking down {topic} with receipts",
            f"The {topic} evidence board"
        ]
        
        return random.choice(screens)
    
    def select_trending_sound(self, horror_style: str) -> str:
        """Select appropriate sound for horror style"""
        
        sound_mapping = {
            'slasher': ['creepy_horror_sound', 'dramatic_drop'],
            'supernatural': ['dark_synthwave', 'suspense_build'],
            'psychological': ['corporate_music', 'glitch_effects']
        }
        
        return random.choice(sound_mapping.get(horror_style, ['creepy_horror_sound']))


class TikTokAutomation:
    """Complete TikTok automation system for @nunyabeznes2"""
    
    def __init__(self):
        self.brand = NunyaBeznes2Brand()
        self.strategy = TikTokContentStrategy()
        
    def adapt_youtube_content_for_tiktok(
        self,
        youtube_script: str,
        topic: str,
        horror_style: str = 'psychological'
    ) -> Dict:
        """Convert YouTube scripts to TikTok-optimized format"""
        
        # TikTok videos are shorter (15-30 seconds vs 45-60)
        # Need faster pacing, more hooks
        
        # Split script and take most impactful parts
        script_parts = youtube_script.split('.')
        tiktok_script = ". ".join(script_parts[:2])  # First two sentences
        
        # Add brand voice
        branded_script = self.brand.inject_brand_voice(tiktok_script, horror_style)
        
        # Generate TikTok caption
        caption = self.brand.generate_tiktok_caption(topic, horror_style)
        
        # Select content format
        content_format = random.choice(list(self.strategy.tiktok_formats.keys()))
        format_func = self.strategy.tiktok_formats[content_format]
        format_hook = format_func(topic)
        
        # Select sound
        sound = self.strategy.select_trending_sound(horror_style)
        
        return {
            'script': branded_script,
            'caption': caption,
            'content_format': content_format,
            'format_hook': format_hook,
            'sound': sound,
            'duration_target': '15-30 seconds',
            'platform': 'tiktok',
            'username': '@nunyabeznes2'
        }


if __name__ == '__main__':
    # Test the brand integration
    brand = NunyaBeznes2Brand()
    automation = TikTokAutomation()
    
    test_script = "Corporate greed is destroying lives. The system is rigged."
    test_topic = "student loan debt crisis"
    
    result = automation.adapt_youtube_content_for_tiktok(test_script, test_topic, 'psychological')
    
    print("TikTok Content Adaptation Test:")
    print(f"Script: {result['script']}")
    print(f"Caption: {result['caption']}")
    print(f"Format: {result['content_format']}")
    print(f"Sound: {result['sound']}")
