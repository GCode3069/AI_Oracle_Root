import os
from dotenv import load_dotenv

load_dotenv("config/credentials/.env")

api_key = os.getenv("RUNWAYML_API_KEY")

if api_key:
    print(f"✅ API Key found: {api_key[:20]}...")
    print("✅ Setup looks good!")
    print("\n📌 FFmpeg should work via imageio-ffmpeg")
    print("📌 Ready to generate videos!")
else:
    print("❌ API Key not found")
    print("Check config/credentials/.env file")
