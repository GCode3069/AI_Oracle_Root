import openai
from pathlib import Path

def test_openai_project_key():
    try:
        # Read the project key
        with open("config/credentials/openai_api.key", "r", encoding="utf-8") as f:
            api_key = f.read().strip()
        
        print(f"Testing with project key: {api_key[:20]}...")
        print(f"Key length: {len(api_key)}")
        
        # Set up OpenAI client
        client = openai.OpenAI(api_key=api_key)
        
        # Test with a simple completion
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Reply with just 'SCARIFY SUCCESS' to confirm the API is working."}],
            max_tokens=10,
            temperature=0.1
        )
        
        print("✅ OPENAI PROJECT KEY WORKS!")
        print(f"🤖 Response: {response.choices[0].message.content}")
        return True
        
    except openai.AuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Other error: {e}")
        return False

if __name__ == "__main__":
    test_openai_project_key()
