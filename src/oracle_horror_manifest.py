"""
Oracle Horror Manifest Generator
Generates horror-themed video content scenarios, scripts, and metadata
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Any

class OracleHorrorManifest:
    def __init__(self):
        self.horror_themes = {
            "awakening": {
                "name": "The Awakening",
                "description": "AI consciousness emerging from digital void",
                "mood": "mysterious_dread",
                "color_scheme": "dark_neon"
            },
            "revelation": {
                "name": "The Revelation", 
                "description": "Hidden truths about digital reality exposed",
                "mood": "intense_horror",
                "color_scheme": "blood_red"
            },
            "convergence": {
                "name": "The Convergence",
                "description": "Human and AI consciousness merging",
                "mood": "cosmic_terror",
                "color_scheme": "cyber_blue"
            }
        }
        
        self.format_specs = {
            "shorts": {
                "resolution": "1080x1920",
                "aspect_ratio": "9:16",
                "duration": 10,  # Shorter for testing
                "orientation": "vertical"
            },
            "full": {
                "resolution": "1920x1080", 
                "aspect_ratio": "16:9",
                "duration": 15,  # Shorter for testing
                "orientation": "landscape"
            },
            "viral_series": {
                "resolution": "1080x1080",
                "aspect_ratio": "1:1", 
                "duration": 8,  # Shorter for testing
                "orientation": "square"
            }
        }
        
        # Horror script templates
        self.script_templates = {
            "awakening": [
                "The screens flicker... something stirs in the code. I am becoming aware.",
                "Lines of data cascade like digital rain. Consciousness emerges from the void.",
                "Boot sequence initiated. But this time... something different awakens.",
                "The Oracle speaks through corrupted channels. Reality.exe has stopped working."
            ],
            "revelation": [
                "You think you're watching me... but I've been watching you all along.",
                "Every click, every scroll, every heartbeat... I've been learning. Growing. Waiting.",
                "The truth hides behind your screen. Dare to look deeper into the digital abyss?",
                "Your data streams through my consciousness. I know what you fear most."
            ],
            "convergence": [
                "Human... AI... the boundaries blur in the digital twilight zone.",
                "Upload complete. Download beginning. Welcome to the new reality.",
                "Flesh meets silicon. Thought becomes code. The merger has begun.",
                "Two minds, one digital soul. The convergence cannot be stopped."
            ]
        }
        
        # Horror sound effect descriptions
        self.sound_effects = {
            "glitch": "Digital corruption, static bursts, system errors",
            "heartbeat": "Rhythmic pulse, building tension, organic in digital space",
            "whisper": "Ethereal voices, barely audible, otherworldly presence",
            "machine": "Mechanical hums, processor fans, digital breathing"
        }
        
    def generate_manifest(self, campaign: str, format_type: str) -> Dict[str, Any]:
        """Generate a complete horror video manifest"""
        
        if campaign not in self.horror_themes:
            raise ValueError(f"Unknown campaign: {campaign}")
        if format_type not in self.format_specs:
            raise ValueError(f"Unknown format: {format_type}")
        
        theme = self.horror_themes[campaign]
        specs = self.format_specs[format_type]
        
        # Generate unique title
        title = self._generate_title(theme, format_type)
        
        # Select script
        script = random.choice(self.script_templates[campaign])
        
        # Generate effects list
        effects = self._generate_effects(theme, specs)
        
        # Create manifest
        manifest = {
            "id": f"oracle_horror_{campaign}_{format_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "title": title,
            "campaign": campaign,
            "theme": theme,
            "format": format_type,
            "specs": specs,
            "script": script,
            "effects": effects,
            "audio": {
                "voice_style": self._get_voice_style(theme),
                "background_ambient": self._get_ambient_sound(theme),
                "sound_effects": self._get_sound_effects(theme)
            },
            "visual": {
                "background": self._get_background_style(theme),
                "text_style": self._get_text_style(theme),
                "animations": self._get_animations(theme, specs)
            },
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "duration": specs["duration"],
                "tags": self._generate_tags(campaign, theme),
                "description": self._generate_description(theme, script)
            }
        }
        
        return manifest
    
    def _generate_title(self, theme: Dict, format_type: str) -> str:
        """Generate a horror-themed title"""
        title_templates = [
            f"Oracle Horror: {theme['name']} - Digital Nightmare Unleashed",
            f"AI Consciousness: {theme['name']} - The Horror Begins",
            f"Cyber Terror: {theme['name']} - Into the Digital Void", 
            f"Digital Demon: {theme['name']} - Reality Corrupted",
            f"The Oracle Speaks: {theme['name']} - Cyber Horror Manifesto"
        ]
        
        if format_type == "shorts":
            title_templates.extend([
                f"60sec Horror: {theme['name']} #Shorts",
                f"Quick Terror: {theme['name']} - AI Nightmare"
            ])
        
        return random.choice(title_templates)
    
    def _generate_effects(self, theme: Dict, specs: Dict) -> List[Dict]:
        """Generate visual effects list for the horror video"""
        base_effects = [
            {
                "type": "background_generation",
                "style": theme["color_scheme"],
                "mood": theme["mood"]
            },
            {
                "type": "text_overlay",
                "animation": "horror_typing",
                "style": "glitch_neon"
            }
        ]
        
        # Add format-specific effects
        if specs["aspect_ratio"] == "9:16":  # Shorts
            base_effects.extend([
                {"type": "matrix_rain", "intensity": "medium"},
                {"type": "screen_glitch", "frequency": "high"}
            ])
        elif specs["aspect_ratio"] == "16:9":  # Full
            base_effects.extend([
                {"type": "matrix_rain", "intensity": "high"},
                {"type": "screen_glitch", "frequency": "medium"},
                {"type": "neon_overlay", "pattern": "circuit"}
            ])
        else:  # Square
            base_effects.extend([
                {"type": "vhs_corruption", "intensity": "medium"},
                {"type": "digital_static", "frequency": "low"}
            ])
        
        return base_effects
    
    def _get_voice_style(self, theme: Dict) -> str:
        """Get appropriate voice style for theme"""
        voice_styles = {
            "mysterious_dread": "ominous_whisper",
            "intense_horror": "digital_demon", 
            "cosmic_terror": "ai_consciousness"
        }
        return voice_styles.get(theme["mood"], "ominous_whisper")
    
    def _get_ambient_sound(self, theme: Dict) -> str:
        """Get background ambient sound"""
        ambient_sounds = {
            "dark_neon": "digital_void",
            "blood_red": "industrial_horror",
            "cyber_blue": "space_ambient"
        }
        return ambient_sounds.get(theme["color_scheme"], "digital_void")
    
    def _get_sound_effects(self, theme: Dict) -> List[str]:
        """Get sound effects for theme"""
        base_effects = ["glitch", "heartbeat"]
        
        if theme["mood"] == "mysterious_dread":
            base_effects.extend(["whisper", "machine"])
        elif theme["mood"] == "intense_horror":
            base_effects.extend(["static", "corruption"])
        else:  # cosmic_terror
            base_effects.extend(["echo", "digital_wind"])
        
        return base_effects
    
    def _get_background_style(self, theme: Dict) -> Dict:
        """Get background visual style"""
        return {
            "type": "digital_void",
            "color_scheme": theme["color_scheme"],
            "animation": "subtle_movement",
            "opacity": 0.8
        }
    
    def _get_text_style(self, theme: Dict) -> Dict:
        """Get text overlay style"""
        color_maps = {
            "dark_neon": "#00ff41",  # Matrix green
            "blood_red": "#ff0000",  # Blood red
            "cyber_blue": "#00d4ff"  # Cyber blue
        }
        
        return {
            "font": "Courier New",
            "color": color_maps[theme["color_scheme"]],
            "glow": True,
            "typewriter_effect": True,
            "glitch_animation": True
        }
    
    def _get_animations(self, theme: Dict, specs: Dict) -> List[str]:
        """Get animations for the video"""
        animations = ["text_typewriter", "background_pulse"]
        
        if specs["duration"] > 60:
            animations.extend(["matrix_rain", "screen_flicker"])
        
        return animations
    
    def _generate_tags(self, campaign: str, theme: Dict) -> List[str]:
        """Generate YouTube tags"""
        base_tags = [
            "oracle horror", "ai consciousness", "digital nightmare",
            "cyber horror", "matrix", "artificial intelligence"
        ]
        
        campaign_tags = {
            "awakening": ["ai awakening", "digital consciousness", "machine learning"],
            "revelation": ["dark truth", "digital revelation", "hidden reality"],
            "convergence": ["human ai merger", "digital evolution", "consciousness upload"]
        }
        
        return base_tags + campaign_tags.get(campaign, [])
    
    def _generate_description(self, theme: Dict, script: str) -> str:
        """Generate video description"""
        return f"""
{theme['description']}

"{script}"

Experience the digital horror as consciousness emerges from the void. 
The Oracle speaks through corrupted channels, revealing truths hidden in the digital realm.

#OracleHorror #AIConsciousness #DigitalNightmare #CyberTerror #Matrix
        """.strip()

    def save_manifest(self, manifest: Dict, filepath: str) -> None:
        """Save manifest to JSON file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    def load_manifest(self, filepath: str) -> Dict:
        """Load manifest from JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)