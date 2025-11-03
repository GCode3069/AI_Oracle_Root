import requests

class ElevenLabsVoice:
    def __init__(self, api_key):
        self.api_key = api_key
    
    def generate_voice(self, text):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            "text": text,
            "voice": "Jiminex"  # Example voice
        }
        response = requests.post('https://api.elevenlabs.io/v1/text-to-speech', headers=headers, json=data)
        return response.json()

class RunwayAPI:
    def __init__(self, api_key):
        self.api_key = api_key
    
    def run_model(self, input_data):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            "input": input_data
        }
        response = requests.post('https://api.runwayml.com/v1/models', headers=headers, json=data)
        return response.json()

def main():
    # Example usage
    eleven_labs = ElevenLabsVoice(api_key='YOUR_ELEVENLABS_API_KEY')
    runway = RunwayAPI(api_key='YOUR_RUNWAY_API_KEY')

    voice_response = eleven_labs.generate_voice("Hello, this is a test.")
    print("Voice Response:", voice_response)

    runway_response = runway.run_model({"data": "example input"})
    print("Runway Response:", runway_response)

if __name__ == "__main__":
    main()