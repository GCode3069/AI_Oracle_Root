#!/usr/bin/env python3
"""
SCARIFY Channel Factory
Creates and manages multiple content channels across platforms
"""

import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class Channel:
    """Represents a single content channel"""
    id: str
    name: str
    niche: str  # "horror", "education", "gaming", "news", "tech"
    language: str  # "en", "es", "fr", "de", "ja", "ko"
    platforms: List[str]  # ["youtube", "tiktok", "instagram"]
    brand_identity: Dict  # colors, fonts, style
    voice_id: str  # ElevenLabs voice
    posting_schedule: Dict  # optimal times
    monetization: Dict  # affiliate links, products
    youtube_channel_id: Optional[str] = None
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()


class ChannelFactory:
    """Creates and manages multiple content channels"""
    
    def __init__(self, root_path: Optional[Path] = None):
        if root_path is None:
            # Auto-detect project root
            current = Path(__file__).parent
            if (current / "abraham_horror").exists():
                root_path = current
            else:
                root_path = Path("/workspace")
        
        self.root_path = Path(root_path)
        self.channels_db = self.root_path / "channels.json"
        self.channels_dir = self.root_path / "channels"
        self.channels_dir.mkdir(parents=True, exist_ok=True)
        
        self.channels = self.load_channels()
    
    def load_channels(self) -> List[Channel]:
        """Load channels from database"""
        if not self.channels_db.exists():
            return []
        
        try:
            with open(self.channels_db, 'r') as f:
                data = json.load(f)
                return [Channel(**channel) for channel in data.get('channels', [])]
        except Exception as e:
            print(f"Error loading channels: {e}")
            return []
    
    def save_channels(self):
        """Save channels to database"""
        data = {
            'channels': [asdict(channel) for channel in self.channels],
            'last_updated': datetime.now().isoformat()
        }
        
        with open(self.channels_db, 'w') as f:
            json.dump(data, f, indent=2)
    
    def create_channel(
        self,
        name: str,
        niche: str,
        language: str,
        platforms: List[str],
        youtube_channel_id: Optional[str] = None
    ) -> Channel:
        """
        Creates a new channel with complete setup:
        - Brand identity (colors, fonts, logo)
        - Content templates (niche-specific)
        - Voice selection (language-specific)
        - Upload credentials (platform-specific)
        - Posting schedule (timezone-optimized)
        """
        
        # Generate unique ID
        channel_id = f"{niche}_{language}_{len(self.channels)}"
        
        # Select brand identity
        brand = self.generate_brand_identity(niche, language)
        
        # Select voice
        voice_id = self.select_voice(language, niche)
        
        # Create channel object
        channel = Channel(
            id=channel_id,
            name=name,
            niche=niche,
            language=language,
            platforms=platforms,
            brand_identity=brand,
            voice_id=voice_id,
            posting_schedule=self.optimize_schedule(language),
            monetization=self.setup_monetization(niche),
            youtube_channel_id=youtube_channel_id
        )
        
        # Create directory structure
        self.setup_channel_directories(channel)
        
        # Add to channels list
        self.channels.append(channel)
        
        # Save to database
        self.save_channels()
        
        print(f"✅ Created channel: {channel.name} ({channel.id})")
        return channel
    
    def generate_brand_identity(self, niche: str, language: str) -> Dict:
        """Generate brand colors, fonts, style based on niche"""
        
        brand_templates = {
            "horror": {
                "colors": ["#8B0000", "#000000", "#FFFFFF"],
                "fonts": ["Creepster", "Nosifer"],
                "style": "dark_ominous",
                "visual_effects": ["VHS_glitch", "red_black_filter", "scanlines"]
            },
            "education": {
                "colors": ["#1E90FF", "#FFFFFF", "#2F4F4F"],
                "fonts": ["Roboto", "Open Sans"],
                "style": "clean_professional",
                "visual_effects": ["clean_transitions", "text_overlays", "diagrams"]
            },
            "gaming": {
                "colors": ["#FF1744", "#00E676", "#2979FF"],
                "fonts": ["Orbitron", "Press Start 2P"],
                "style": "energetic_bold",
                "visual_effects": ["gameplay_overlay", "bold_text", "colorful_transitions"]
            },
            "news": {
                "colors": ["#1565C0", "#D32F2F", "#FFFFFF"],
                "fonts": ["Merriweather", "PT Serif"],
                "style": "authoritative_serious",
                "visual_effects": ["news_banner", "professional_overlay", "breaking_news_sting"]
            },
            "tech": {
                "colors": ["#00BCD4", "#FFC107", "#212121"],
                "fonts": ["Rajdhani", "IBM Plex Mono"],
                "style": "modern_sleek",
                "visual_effects": ["tech_overlay", "smooth_transitions", "code_visualization"]
            }
        }
        
        return brand_templates.get(niche, brand_templates["education"])
    
    def select_voice(self, language: str, niche: str) -> str:
        """Select ElevenLabs voice based on language and niche"""
        
        voice_mapping = {
            "en": {
                "horror": "pNInz6obpgDQGcFmaJgB",  # Jiminex (creepy) - existing
                "education": "21m00Tcm4TlvDq8ikWAM",  # Rachel (professional)
                "gaming": "TX3LPaxmHKxFdv7VOQHJ",  # Adam (energetic)
                "news": "EXAVITQu4vr4xnSDxMaL",  # Bella (authoritative)
                "tech": "VR6AewLTigWG4xSOukaG"  # Arnold (analytical) - existing
            },
            "es": {
                "horror": "pNInz6obpgDQGcFmaJgB",  # Use multilingual voice
                "education": "21m00Tcm4TlvDq8ikWAM",
                "gaming": "TX3LPaxmHKxFdv7VOQHJ",
                "news": "EXAVITQu4vr4xnSDxMaL",
                "tech": "VR6AewLTigWG4xSOukaG"
            },
            "fr": {
                "horror": "pNInz6obpgDQGcFmaJgB",
                "education": "21m00Tcm4TlvDq8ikWAM",
                "gaming": "TX3LPaxmHKxFdv7VOQHJ",
                "news": "EXAVITQu4vr4xnSDxMaL",
                "tech": "VR6AewLTigWG4xSOukaG"
            },
            "de": {
                "horror": "pNInz6obpgDQGcFmaJgB",
                "education": "21m00Tcm4TlvDq8ikWAM",
                "gaming": "TX3LPaxmHKxFdv7VOQHJ",
                "news": "EXAVITQu4vr4xnSDxMaL",
                "tech": "VR6AewLTigWG4xSOukaG"
            }
        }
        
        # Default to existing voices (multilingual support)
        return voice_mapping.get(language, {}).get(niche, "pNInz6obpgDQGcFmaJgB")
    
    def optimize_schedule(self, language: str) -> Dict:
        """Optimize posting schedule based on language/timezone"""
        
        # Base optimal times (UTC)
        base_times = ["09:00", "12:00", "15:00", "18:00", "21:00"]
        
        # Timezone adjustments by language
        timezone_adjustments = {
            "en": 0,  # US/UK
            "es": -6,  # Latin America
            "fr": +1,  # Europe
            "de": +1,  # Europe
            "ja": +9,  # Japan
            "ko": +9,  # Korea
        }
        
        adjustment = timezone_adjustments.get(language, 0)
        
        return {
            "times": base_times,
            "timezone_offset": adjustment,
            "max_daily_posts": 5,
            "spacing_hours": 2
        }
    
    def setup_monetization(self, niche: str) -> Dict:
        """Setup monetization strategy for niche"""
        
        monetization_templates = {
            "horror": {
                "affiliate_categories": ["horror_books", "horror_movies", "streaming_services"],
                "email_capture": True,
                "digital_products": ["horror_script_pack", "horror_editing_templates"]
            },
            "education": {
                "affiliate_categories": ["online_courses", "educational_books", "learning_tools"],
                "email_capture": True,
                "digital_products": ["study_guides", "course_templates"]
            },
            "gaming": {
                "affiliate_categories": ["gaming_gear", "games", "streaming_equipment"],
                "email_capture": False,
                "digital_products": ["gaming_tips_guide", "streaming_setup_guide"]
            },
            "news": {
                "affiliate_categories": ["news_subscriptions", "books", "documentaries"],
                "email_capture": True,
                "digital_products": ["newsletter", "analysis_reports"]
            },
            "tech": {
                "affiliate_categories": ["tech_products", "software", "courses"],
                "email_capture": True,
                "digital_products": ["tech_reviews", "setup_guides"]
            }
        }
        
        return monetization_templates.get(niche, monetization_templates["education"])
    
    def setup_channel_directories(self, channel: Channel):
        """Create directory structure for channel"""
        
        channel_path = self.channels_dir / channel.id
        
        directories = [
            channel_path / "scripts",
            channel_path / "audio",
            channel_path / "videos" / "shorts",
            channel_path / "videos" / "long_form",
            channel_path / "analytics",
            channel_path / "assets" / "thumbnails",
            channel_path / "assets" / "overlays",
            channel_path / "uploaded"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def get_channel(self, channel_id: str) -> Optional[Channel]:
        """Get channel by ID"""
        for channel in self.channels:
            if channel.id == channel_id:
                return channel
        return None
    
    def get_channels_by_niche(self, niche: str) -> List[Channel]:
        """Get all channels for a specific niche"""
        return [c for c in self.channels if c.niche == niche]
    
    def get_channels_by_language(self, language: str) -> List[Channel]:
        """Get all channels for a specific language"""
        return [c for c in self.channels if c.language == language]
    
    def get_active_channels(self) -> List[Channel]:
        """Get all active channels"""
        return [c for c in self.channels if c.youtube_channel_id or "youtube" in c.platforms]
    
    def list_channels(self) -> None:
        """List all channels"""
        print(f"\n{'='*80}")
        print(f"CHANNEL FACTORY - {len(self.channels)} Channels")
        print('='*80)
        
        for channel in self.channels:
            print(f"\n📺 {channel.name}")
            print(f"   ID: {channel.id}")
            print(f"   Niche: {channel.niche} | Language: {channel.language}")
            print(f"   Platforms: {', '.join(channel.platforms)}")
            print(f"   Voice: {channel.voice_id[:20]}...")
            if channel.youtube_channel_id:
                print(f"   YouTube ID: {channel.youtube_channel_id}")


def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='SCARIFY Channel Factory')
    parser.add_argument('--create', nargs=4, metavar=('NAME', 'NICHE', 'LANGUAGE', 'PLATFORMS'),
                       help='Create new channel: name niche language platforms (comma-separated)')
    parser.add_argument('--list', action='store_true', help='List all channels')
    parser.add_argument('--setup-defaults', action='store_true',
                       help='Create default 10-channel setup')
    
    args = parser.parse_args()
    
    factory = ChannelFactory()
    
    if args.setup_defaults:
        print("\n🏭 Setting up default 10-channel system...")
        
        default_channels = [
            ("Dark Truth", "horror", "en", ["youtube", "tiktok"]),
            ("Verdades Oscuras", "horror", "es", ["youtube", "tiktok"]),
            ("Vérités Sombres", "horror", "fr", ["youtube"]),
            ("Quick Facts Daily", "education", "en", ["youtube", "instagram"]),
            ("Datos Rápidos", "education", "es", ["youtube"]),
            ("Game Breakdown", "gaming", "en", ["youtube", "tiktok"]),
            ("Análisis Gaming", "gaming", "es", ["tiktok"]),
            ("Tech Insights", "tech", "en", ["youtube"]),
            ("News Flash", "news", "en", ["youtube", "twitter"]),
            ("Noticias Flash", "news", "es", ["youtube"])
        ]
        
        for name, niche, lang, platforms in default_channels:
            factory.create_channel(name, niche, lang, platforms)
        
        print(f"\n✅ Created {len(default_channels)} channels!")
        factory.list_channels()
    
    elif args.create:
        name, niche, language, platforms_str = args.create
        platforms = platforms_str.split(',')
        factory.create_channel(name, niche, language, platforms)
        factory.list_channels()
    
    elif args.list:
        factory.list_channels()
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
