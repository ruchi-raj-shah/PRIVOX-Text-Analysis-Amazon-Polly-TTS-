from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import boto3
import base64
from nlp_utils import analyze_text

app = Flask(__name__, template_folder='.')
CORS(app)
polly_client = boto3.client('polly', region_name='us-east-1')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing text'}), 400
        
        # Fix encoding
        raw_text = data['text'].strip()
        text = raw_text.encode('utf-8', errors='ignore').decode('utf-8')
        text = text.replace('’', "'").replace('“', '"').replace('”', '"')
        
        if len(text) > 3000:
            return jsonify({'error': 'Text too long'}), 400
        
        result = analyze_text(text)
        voice = data.get('voice', 'Joanna')
        
        # Polly TTS
        try:
            response = polly_client.synthesize_speech(
                Text=result['redacted'],
                OutputFormat='mp3',
                VoiceId=voice,
                Engine='neural'
            )
            audio_bytes = response['AudioStream'].read()
            result['audio_b64'] = base64.b64encode(audio_bytes).decode()
            result['voice'] = voice
        except Exception as e:
            result['audio_error'] = str(e)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
