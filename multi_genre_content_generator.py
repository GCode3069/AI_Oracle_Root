#!/usr/bin/env python3
"""
Multi-Genre Content Generator
Generates scripts for ANY niche (horror, education, gaming, news, tech)
Works with existing SCARIFY pipeline
"""

import os
from typing import Dict, Optional
from pathlib import Path

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


class MultiGenreContentGenerator:
    """Generates scripts for any niche/language combination"""
    
    def __init__(self, api_key: Optional[str] = None):
        if api_key is None:
            api_key = os.getenv("ANTHROPIC_API_KEY", "")
        
        if ANTHROPIC_AVAILABLE and api_key:
            self.client = anthropic.Anthropic(api_key=api_key)
        else:
            self.client = None
            print("⚠️  Anthropic API not available. Using template fallback.")
        
        # Content templates by niche
        self.templates = {
            "horror": self.generate_horror_script,
            "education": self.generate_education_script,
            "gaming": self.generate_gaming_script,
            "news": self.generate_news_script,
            "tech": self.generate_tech_script
        }
    
    def generate_script(
        self,
        niche: str,
        topic: str,
        language: str = "en",
        duration: str = "short"  # "short" (15-60s) or "long" (3-10min)
    ) -> Dict:
        """Generate script for any niche"""
        
        generator_func = self.templates.get(niche)
        if not generator_func:
            raise ValueError(f"Unknown niche: {niche}. Available: {list(self.templates.keys())}")
        
        script = generator_func(topic, language, duration)
        
        return {
            "script": script,
            "niche": niche,
            "topic": topic,
            "language": language,
            "duration": duration,
            "word_count": len(script.split())
        }
    
    def generate_horror_script(self, topic: str, language: str, duration: str) -> str:
        """Generate horror content (like Abraham Lincoln)"""
        
        if self.client:
            prompt = f"""Create a {duration} horror script about: {topic}
            
            Style: Ominous, creepy, unsettling
            Format: {"15-30 seconds" if duration == "short" else "3-5 minutes"}
            Language: {language}
            Tone: Dark, foreboding, shocking
            
            Include:
            - Shocking hook (first 3 seconds)
            - Disturbing revelation
            - Ominous conclusion
            
            Script:"""
            
            try:
                response = self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1000,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text.strip()
            except Exception as e:
                print(f"⚠️  API error: {e}. Using template.")
        
        # Template fallback
        templates = [
            f"{topic}. The truth they don't want you to know. The system is rigged. You're being watched.",
            f"Behind {topic} lies a darker truth. They're hiding something. The evidence is everywhere.",
            f"{topic} is just the surface. Dig deeper. The real horror is what they're not telling you."
        ]
        import random
        return random.choice(templates)
    
    def generate_education_script(self, topic: str, language: str, duration: str) -> str:
        """Generate educational content"""
        
        if self.client:
            prompt = f"""Create a {duration} educational script about: {topic}
            
            Style: Clear, informative, engaging
            Format: {"30-60 seconds" if duration == "short" else "5-8 minutes"}
            Language: {language}
            Tone: Professional, authoritative, helpful
            
            Include:
            - Hook question (first 3 seconds)
            - 3-5 key facts
            - Practical application
            - Call to action
            
            Script:"""
            
            try:
                response = self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1000,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text.strip()
            except Exception as e:
                print(f"⚠️  API error: {e}. Using template.")
        
        # Template fallback
        return f"Ever wondered about {topic}? Here's what you need to know. First, [key fact]. Second, [key fact]. Third, [key fact]. Understanding {topic} helps you [practical application]. Want to learn more? Subscribe for daily facts."
    
    def generate_gaming_script(self, topic: str, language: str, duration: str) -> str:
        """Generate gaming commentary"""
        
        if self.client:
            prompt = f"""Create a {duration} gaming commentary script about: {topic}
            
            Style: Energetic, entertaining, informative
            Format: {"15-45 seconds" if duration == "short" else "3-7 minutes"}
            Language: {language}
            Tone: Excited, knowledgeable, relatable
            
            Include:
            - Attention-grabbing intro
            - Gaming tips or analysis
            - Community engagement
            
            Script:"""
            
            try:
                response = self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1000,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text.strip()
            except Exception as e:
                print(f"⚠️  API error: {e}. Using template.")
        
        # Template fallback
        return f"Yo gamers! Let's talk about {topic}. This is absolutely insane! Here's what you need to know: [tip 1]. Also, [tip 2]. Drop your thoughts in the comments!"
    
    def generate_news_script(self, topic: str, language: str, duration: str) -> str:
        """Generate news commentary"""
        
        if self.client:
            prompt = f"""Create a {duration} news script about: {topic}
            
            Style: Authoritative, balanced, informative
            Format: {"30-60 seconds" if duration == "short" else "3-5 minutes"}
            Language: {language}
            Tone: Professional, objective, engaging
            
            Include:
            - Headline hook
            - Key facts
            - Context
            - Implications
            
            Script:"""
            
            try:
                response = self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1000,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text.strip()
            except Exception as e:
                print(f"⚠️  API error: {e}. Using template.")
        
        # Template fallback
        return f"Breaking: {topic}. Here's what we know. [Fact 1]. [Fact 2]. This development has significant implications for [context]. Stay tuned for updates."
    
    def generate_tech_script(self, topic: str, language: str, duration: str) -> str:
        """Generate tech content"""
        
        if self.client:
            prompt = f"""Create a {duration} tech script about: {topic}
            
            Style: Analytical, detailed, helpful
            Format: {"30-60 seconds" if duration == "short" else "5-8 minutes"}
            Language: {language}
            Tone: Professional, informative, engaging
            
            Include:
            - Product/feature introduction
            - Key specifications
            - Pros and cons
            - Verdict/recommendation
            
            Script:"""
            
            try:
                response = self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1000,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text.strip()
            except Exception as e:
                print(f"⚠️  API error: {e}. Using template.")
        
        # Template fallback
        return f"Today we're reviewing {topic}. Here's what makes it special: [feature 1]. However, there are some drawbacks: [con]. Overall, [verdict]. Check the link in description for more details."


def main():
    """Test the generator"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Multi-Genre Content Generator')
    parser.add_argument('--niche', required=True, choices=['horror', 'education', 'gaming', 'news', 'tech'],
                       help='Content niche')
    parser.add_argument('--topic', required=True, help='Video topic')
    parser.add_argument('--language', default='en', help='Language code')
    parser.add_argument('--duration', default='short', choices=['short', 'long'], help='Video duration')
    
    args = parser.parse_args()
    
    generator = MultiGenreContentGenerator()
    
    result = generator.generate_script(
        niche=args.niche,
        topic=args.topic,
        language=args.language,
        duration=args.duration
    )
    
    print(f"\n{'='*80}")
    print(f"GENERATED SCRIPT: {args.niche.upper()}")
    print('='*80)
    print(f"\nTopic: {result['topic']}")
    print(f"Language: {result['language']}")
    print(f"Duration: {result['duration']}")
    print(f"Word Count: {result['word_count']}")
    print(f"\nScript:\n{result['script']}\n")


if __name__ == '__main__':
    main()
