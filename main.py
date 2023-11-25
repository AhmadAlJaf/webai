import g4f
import json
from flask import Flask, request, jsonify
import logging
from logging.handlers import RotatingFileHandler

# Configure g4f
g4f.debug.logging = True
g4f.check_version = False
print(g4f.version)
print(g4f.Provider.Ails.params)

# Flask app for handling requests
app = Flask(__name__)

# Configure logging
handler = RotatingFileHandler('server.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

def get_ai_response(message):
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo,
            messages=[{"role": "user", "content": message}]
        )
        app.logger.info("Raw AI Response: " + json.dumps(response, indent=4))
        response_text = str(response)
        if len(response_text) > 4000:
            return response_text[:4000] + '... (Response truncated)'
        return response_text
    except Exception as e:
        app.logger.error(f"Error in get_ai_response: {e}")
        return "Error occurred while processing the request."

@app.route('/ai', methods=['POST'])
def handle_request():
    try:
        data = request.json
        message = data.get('message')
        if message:
            response_text = get_ai_response(message)
            return jsonify({'response': response_text})
        else:
            return jsonify({'error': 'No message provided'}), 400
    except Exception as e:
        app.logger.error(f"Error in handle_request: {e}")
        return jsonify({'error': 'An error occurred processing your request.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
