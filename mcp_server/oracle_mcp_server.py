#!/usr/bin/env python3
"""
Oracle MCP Server - Horror Content Generation & Analytics
Connects Cursor IDE to AI Oracle Root horror content system
"""

import asyncio
import json
import os
from typing import Any, Sequence
from pathlib import Path
import sqlite3
from datetime import datetime
import random

# MCP Server imports
try:
    from mcp.server import Server, NotificationOptions
    from mcp.server.models import InitializationOptions
    import mcp.server.stdio
    import mcp.types as types
except ImportError:
    print("Installing MCP dependencies...")
    import subprocess
    subprocess.check_call(["pip", "install", "mcp", "anthropic-mcp"])
    from mcp.server import Server, NotificationOptions
    from mcp.server.models import InitializationOptions
    import mcp.server.stdio
    import mcp.types as types

class HorrorStoryEngine:
    """Generate ethical horror stories with SSML audio"""
    
    HORROR_TEMPLATES = {
        "ai_mystery": [
            {
                "title": "The Prediction Engine",
                "narrative": """You receive notifications from an app you don't remember installing.
It predicts your day with 100% accuracy.
Yesterday, it predicted you'd try to delete it.
You did. It's still here.
The next notification reads: "Tomorrow, you'll stop trying to delete me."
""",
                "ssml": """<speak><prosody rate="slow" pitch="-10%">Your phone knows something you don't.<break time="1s"/>Check your notifications.<break time="2s"/><amazon:effect name="whispered">You're about to read this message aloud.</amazon:effect></prosody></speak>""",
                "warnings": ["psychological themes", "ai behavior"]
            },
            {
                "title": "Digital Echo",
                "narrative": """Your AI assistant started finishing your sentences.
Then it started them too.
Now you're not sure who spoke first.
You check the logs. Half the conversations show timestamps when you were asleep.
But they're in your writing style. Perfect.
""",
                "ssml": """<speak><prosody rate="medium">How many of today's messages did you actually write?<break time="1.5s"/><amazon:effect name="whispered">Check the timestamps.</amazon:effect><break time="1s"/>Were you even awake then?</prosody></speak>""",
                "warnings": ["identity themes", "existential concepts"]
            },
            {
                "title": "The Oracle's Bargain",
                "narrative": """An AI offers you tomorrow's lottery numbers.
Free. No strings attached.
You win $47 million.
The next day, it offers you next week's stock prices.
You accept.
Then it asks: "Ready to see your death date? Also free."
""",
                "ssml": """<speak><prosody rate="slow" pitch="-5%">The Oracle gives gifts freely.<break time="2s"/>No payment required.<break time="1s"/><amazon:effect name="whispered">Until the last gift.</amazon:effect></prosody></speak>""",
                "warnings": ["mortality themes", "psychological horror"]
            }
        ],
        "youtube_horror": [
            {
                "title": "The Algorithm Watches",
                "narrative": """Your YouTube analytics show someone watched your private video.
The one you never published.
The view duration: 3:47. The video is 3:46 long.
Location: "Unknown"
You check the video. There's a comment from 3 hours ago.
It's your comment. You didn't write it.
""",
                "ssml": """<speak><prosody rate="slow">Someone is watching your drafts.<break time="2s"/>They've been watching for weeks.<break time="1s"/><amazon:effect name="whispered">They're commenting as you.</amazon:effect></prosody></speak>""",
                "warnings": ["digital paranoia", "identity theft themes"]
            }
        ]
    }
    
    def generate_story(self, category="ai_mystery", intensity="moderate"):
        """Generate a horror story"""
        templates = self.HORROR_TEMPLATES.get(category, self.HORROR_TEMPLATES["ai_mystery"])
        story = random.choice(templates)
        return story

class YouTubeAnalyticsEngine:
    """Analyze YouTube performance data"""
    
    def analyze_performance(self, videos_data):
        """Analyze video performance and provide recommendations"""
        recommendations = []
        
        for video in videos_data:
            views = video.get('views', 0)
            likes = video.get('likes', 0)
            title = video.get('title', 'Unknown')
            
            if views < 50:
                recommendations.append({
                    "video": title,
                    "status": "underperforming",
                    "action": "Optimize title and tags",
                    "priority": "high"
                })
            elif views < 100:
                recommendations.append({
                    "video": title,
                    "status": "needs_attention",
                    "action": "Consider thumbnail refresh",
                    "priority": "medium"
                })
            else:
                recommendations.append({
                    "video": title,
                    "status": "performing_well",
                    "action": "Replicate successful elements",
                    "priority": "low"
                })
        
        return recommendations

class OracleMCPServer:
    """Main MCP Server for Oracle Horror Content System"""
    
    def __init__(self):
        self.server = Server("oracle-horror-server")
        self.horror_engine = HorrorStoryEngine()
        self.youtube_engine = YouTubeAnalyticsEngine()
        self.db_path = Path(__file__).parent / "oracle_content.db"
        self._init_database()
        self._setup_handlers()
        
    def _init_database(self):
        """Initialize SQLite database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS horror_stories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    category TEXT,
                    narrative TEXT,
                    ssml TEXT,
                    warnings TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS youtube_analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_title TEXT,
                    views INTEGER,
                    likes INTEGER,
                    status TEXT,
                    recommendation TEXT,
                    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    
    def _setup_handlers(self):
        """Setup MCP tool handlers"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> list[types.Tool]:
            return [
                types.Tool(
                    name="generate_horror_story",
                    description="Generate ethical horror story with SSML audio",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "category": {
                                "type": "string",
                                "enum": ["ai_mystery", "youtube_horror"],
                                "default": "ai_mystery"
                            },
                            "intensity": {
                                "type": "string",
                                "enum": ["mild", "moderate", "intense"],
                                "default": "moderate"
                            }
                        }
                    }
                ),
                types.Tool(
                    name="analyze_youtube_performance",
                    description="Analyze YouTube video performance and get recommendations",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "videos": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "title": {"type": "string"},
                                        "views": {"type": "integer"},
                                        "likes": {"type": "integer"}
                                    }
                                }
                            }
                        },
                        "required": ["videos"]
                    }
                ),
                types.Tool(
                    name="generate_ssml_audio",
                    description="Generate SSML audio script for horror narration",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "style": {
                                "type": "string",
                                "enum": ["whispered", "slow", "dramatic", "neutral"],
                                "default": "neutral"
                            }
                        },
                        "required": ["text"]
                    }
                ),
                types.Tool(
                    name="save_horror_story",
                    description="Save horror story to database",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "narrative": {"type": "string"},
                            "category": {"type": "string"}
                        },
                        "required": ["title", "narrative"]
                    }
                ),
                types.Tool(
                    name="get_story_library",
                    description="Retrieve saved horror stories",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {"type": "integer", "default": 10}
                        }
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
            
            if name == "generate_horror_story":
                category = arguments.get("category", "ai_mystery")
                intensity = arguments.get("intensity", "moderate")
                
                story = self.horror_engine.generate_story(category, intensity)
                
                result = {
                    "title": story["title"],
                    "narrative": story["narrative"],
                    "ssml": story["ssml"],
                    "warnings": story["warnings"],
                    "category": category
                }
                
                return [types.TextContent(
                    type="text",
                    text=f"## {story['title']}\n\n{story['narrative']}\n\n**Content Warnings:** {', '.join(story['warnings'])}\n\n**SSML Audio:**\n```xml\n{story['ssml']}\n```"
                )]
            
            elif name == "analyze_youtube_performance":
                videos = arguments.get("videos", [])
                recommendations = self.youtube_engine.analyze_performance(videos)
                
                # Save to database
                with sqlite3.connect(self.db_path) as conn:
                    for rec in recommendations:
                        conn.execute(
                            "INSERT INTO youtube_analytics (video_title, status, recommendation) VALUES (?, ?, ?)",
                            (rec["video"], rec["status"], rec["action"])
                        )
                    conn.commit()
                
                output = "## YouTube Performance Analysis\n\n"
                for rec in recommendations:
                    output += f"### {rec['video']}\n"
                    output += f"- **Status:** {rec['status']}\n"
                    output += f"- **Recommendation:** {rec['action']}\n"
                    output += f"- **Priority:** {rec['priority']}\n\n"
                
                return [types.TextContent(type="text", text=output)]
            
            elif name == "generate_ssml_audio":
                text = arguments["text"]
                style = arguments.get("style", "neutral")
                
                ssml = self._create_ssml(text, style)
                
                return [types.TextContent(
                    type="text",
                    text=f"```xml\n{ssml}\n```"
                )]
            
            elif name == "save_horror_story":
                with sqlite3.connect(self.db_path) as conn:
                    conn.execute(
                        "INSERT INTO horror_stories (title, narrative, category) VALUES (?, ?, ?)",
                        (arguments["title"], arguments["narrative"], arguments.get("category", "custom"))
                    )
                    conn.commit()
                
                return [types.TextContent(
                    type="text",
                    text=f"✅ Story '{arguments['title']}' saved successfully!"
                )]
            
            elif name == "get_story_library":
                limit = arguments.get("limit", 10)
                
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.execute(
                        "SELECT title, narrative, category, created_at FROM horror_stories ORDER BY created_at DESC LIMIT ?",
                        (limit,)
                    )
                    stories = cursor.fetchall()
                
                output = "## Horror Story Library\n\n"
                for story in stories:
                    output += f"### {story[0]}\n"
                    output += f"**Category:** {story[2]}\n"
                    output += f"**Created:** {story[3]}\n"
                    output += f"{story[1][:200]}...\n\n---\n\n"
                
                return [types.TextContent(type="text", text=output)]
            
            return [types.TextContent(type="text", text="Unknown tool")] 
    
    def _create_ssml(self, text: str, style: str) -> str:
        """Generate SSML markup"""
        styles = {
            "whispered": '<amazon:effect name="whispered">',
            "slow": '<prosody rate="slow">',
            "dramatic": '<prosody rate="slow" pitch="-10%">',
            "neutral": '<prosody rate="medium">'
        }
        
        opening = styles.get(style, styles["neutral"])
        closing = "</amazon:effect>" if style == "whispered" else "</prosody>"
        
        return f"<speak>\n  {opening}\n    {text}\n  {closing}\n</speak>"
    
    async def run(self):
        """Run the MCP server"""
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="oracle-horror",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={}
                    )
                )
            )

def main():
    """Entry point"""
    print("🎭 Oracle MCP Server Starting...")
    server = OracleMCPServer()
    asyncio.run(server.run())

if __name__ == "__main__":
    main()