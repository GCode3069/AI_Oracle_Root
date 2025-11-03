import anthropic

def test_claude_integration():
    """Test Claude API integration with binary key reading"""
    try:
        # Read Claude API key using binary method
        with open(r"F:\AI_Oracle_Root\scarify\config\credentials\claude_api.key", "rb") as f:
            raw_bytes = f.read()
        
        # Strip BOM if present
        if raw_bytes.startswith(b'\xef\xbb\xbf'):
            clean_bytes = raw_bytes[3:]
        else:
            clean_bytes = raw_bytes
        
        api_key = clean_bytes.decode('utf-8').strip()
        print(f"✅ Claude API key loaded (length: {len(api_key)})")
        print(f"🔑 Key starts with: {api_key[:10]}...")
        
        # Test Claude API
        client = anthropic.Anthropic(api_key=api_key)
        
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=100,
            messages=[
                {"role": "user", "content": "Say 'CLAUDE INTEGRATION SUCCESSFUL' and nothing else."}
            ]
        )
        
        print(f"✅ CLAUDE TEST SUCCESS: {response.content[0].text}")
        return True
        
    except Exception as e:
        print(f"❌ Claude test failed: {e}")
        return False

if __name__ == "__main__":
    test_claude_integration()
