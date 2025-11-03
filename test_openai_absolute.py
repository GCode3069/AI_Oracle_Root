import openai
from pathlib import Path

def test_openai_absolute():
    try:
        # Use absolute path
        key_path = Path(r"F:\AI_Oracle_Root\scarify\config\credentials\openai_api.key")
        api_key = key_path.read_text(encoding="utf-8").strip()
        
        print(f"🔑 Using key: {api_key[:20]}...")
        print(f"📁 Key file: {key_path}")
        
        # Initialize OpenAI client
        client = openai.OpenAI(api_key=api_key)
        
        # Make a simple API call
        print("🔄 Making API call...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Just reply with 'SCARIFY SUCCESS' to confirm everything is working."}
            ],
            max_tokens=10,
            temperature=0.1
        )
        
        result = response.choices[0].message.content
        print("✅ OPENAI API SUCCESS!")
        print(f"🤖 Response: {result}")
        return True
        
    except openai.AuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Other error: {e}")
        import traceback
        print(f"Full error: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    test_openai_absolute()
