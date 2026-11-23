import os
import sys
import argparse
import requests

API_URL = 'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}'

def synthesize(text, voice_id, output_path, api_key, model_id='eleven_multilingual_v2'):
    headers = {
        'xi-api-key': api_key,
        'Content-Type': 'application/json',
        'Accept': 'audio/mpeg',
    }
    payload = {
        'text': text,
        'model_id': model_id,
        'voice_settings': {
            'stability': 0.5,
            'similarity_boost': 0.75,
        },
    }
    url = API_URL.format(voice_id=voice_id)
    response = requests.post(url, json=payload, headers=headers, timeout=60)
    response.raise_for_status()
    with open(output_path, 'wb') as f:
        f.write(response.content)
    return output_path

def main():
    parser = argparse.ArgumentParser(description='ElevenLabs TTS demo')
    parser.add_argument('text', help='Text to synthesize')
    parser.add_argument('--voice-id', default='21m00Tcm4TlvDq8ikWAM', help='ElevenLabs voice ID')
    parser.add_argument('--output', default='speech.mp3', help='Output mp3 file')
    args = parser.parse_args()

    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        sys.exit('Set ELEVENLABS_API_KEY first')

    try:
        path = synthesize(args.text, args.voice_id, args.output, api_key)
        print(f'Audio saved to {path}')
    except requests.HTTPError as exc:
        sys.exit(f'API request failed: {exc}')

if __name__ == '__main__':
    main()