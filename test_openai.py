import openai
from pathlib import Path

def test_openai():
    try:
        # Read OpenAI key
        api_key = Path("config/credentials/openai_api.key").read_text().strip()
        print(f"Testing with key: {api_key[:10]}...")
        
        # Set up OpenAI client
        client = openai.OpenAI(api_key=api_key)
        
        # Test with a simple completion
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'OpenAI API is working!' in a creative way."}],
            max_tokens=50
        )
        
        print("✅ OPENAI API CONNECTED SUCCESSFULLY!")
        print(f"🤖 Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI test failed: {e}")
        return False

if __name__ == "__main__":
    test_openai()
