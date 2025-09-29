import asyncio
import aiohttp
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Configuration
ELEVEN_LABS_API_KEY = 'your_eleven_labs_api_key'
RUNWAY_API_KEY = 'your_runway_api_key'
DATABASE_URL = 'sqlite+aiosqlite:///./test.db'  # Example for SQLite, change as needed

# Set up logging
logging.basicConfig(level=logging.INFO)

# Database setup
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_voice_sample(text):
    url = "https://api.elevenlabs.io/v1/voice/generate"
    headers = {
        "Authorization": f"Bearer {ELEVEN_LABS_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "voice_id": "J6RlTvR54IzUb3FxOueW",
        "text": text
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status != 200:
                logging.error(f"Error getting voice sample: {response.status}")
                return None
            return await response.json()

async def create_video(voice_sample_url):
    url = "https://api.runwayml.com/v1/video/generate"
    headers = {
        "Authorization": f"Bearer {RUNWAY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "voice_sample_url": voice_sample_url
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status != 200:
                logging.error(f"Error creating video: {response.status}")
                return None
            return await response.json()

async def track_analytics(event):
    logging.info(f"Tracking event: {event}")
    # Implement your analytics tracking logic here

async def main():
    text = "Hello, this is a test message to generate a voice sample."
    
    voice_sample = await get_voice_sample(text)
    if not voice_sample:
        logging.error("Failed to generate voice sample.")
        return
    
    voice_sample_url = voice_sample.get("url")
    if not voice_sample_url:
        logging.error("Voice sample URL not found.")
        return

    video = await create_video(voice_sample_url)
    if not video:
        logging.error("Failed to create video.")
        return

    await track_analytics("Video created successfully")

if __name__ == "__main__":
    asyncio.run(main())
