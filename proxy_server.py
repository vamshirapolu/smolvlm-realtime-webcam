from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
allowed_origins = os.getenv("CORS_ORIGINS")
if allowed_origins:
    origins = [origin.strip() for origin in allowed_origins.split(",") if origin.strip()]
    CORS(app, origins=origins)
else:
    CORS(app)  # Enable CORS for all routes

@app.route('/api/generate', methods=['POST', 'OPTIONS'])
def proxy_ollama():
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response
    
    try:
        # Get the request data
        data = request.get_json(silent=True) or {}
        if not isinstance(data, dict):
            return jsonify({'error': 'Invalid request body'}), 400
        
        # Default Ollama URL (can be configured)
        ollama_base_url = data.pop("ollama_base_url", None) or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        if not ollama_base_url.startswith(("http://", "https://")):
            return jsonify({'error': 'Invalid Ollama base URL'}), 400
        ollama_base_url = ollama_base_url.rstrip("/")
        if ollama_base_url.endswith("/api/generate"):
            ollama_url = ollama_base_url
        else:
            ollama_url = f"{ollama_base_url}/api/generate"
        
        # Forward the request to Ollama
        response = requests.post(
            ollama_url,
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=120
        )
        
        # Return the response from Ollama
        if response.ok:
            return jsonify(response.json())
        else:
            return jsonify({
                'error': f'Ollama API error: {response.status_code}',
                'message': response.text
            }), response.status_code
            
    except requests.exceptions.ConnectionError:
        return jsonify({
            'error': 'Connection failed',
            'message': 'Could not connect to Ollama. Make sure Ollama is running on localhost:11434'
        }), 503
    except requests.exceptions.Timeout:
        return jsonify({
            'error': 'Request timeout',
            'message': 'Ollama request timed out'
        }), 504
    except Exception as e:
        return jsonify({
            'error': 'Proxy server error',
            'message': str(e)
        }), 500

@app.route('/api/openai', methods=['POST', 'OPTIONS'])
def proxy_openai():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response

    try:
        data = request.get_json(silent=True) or {}
        if not isinstance(data, dict):
            return jsonify({'error': 'Invalid request body'}), 400

        api_key = request.headers.get("Authorization")
        if not api_key:
            env_key = os.getenv("OPENAI_API_KEY", "").strip()
            if env_key:
                api_key = f"Bearer {env_key}"

        if api_key and not api_key.lower().startswith("bearer "):
            api_key = f"Bearer {api_key}"

        if not api_key:
            return jsonify({'error': 'Missing OpenAI API key'}), 401

        openai_base_url = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1").rstrip("/")
        response = requests.post(
            f"{openai_base_url}/chat/completions",
            json=data,
            headers={
                'Content-Type': 'application/json',
                'Authorization': api_key
            },
            timeout=120
        )

        if response.ok:
            return jsonify(response.json())
        return jsonify({
            'error': f'OpenAI API error: {response.status_code}',
            'message': response.text
        }), response.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({
            'error': 'Connection failed',
            'message': 'Could not connect to OpenAI. Check network access.'
        }), 503
    except requests.exceptions.Timeout:
        return jsonify({
            'error': 'Request timeout',
            'message': 'OpenAI request timed out'
        }), 504
    except Exception as e:
        return jsonify({
            'error': 'Proxy server error',
            'message': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Proxy server is running'})

if __name__ == '__main__':
    host = os.getenv("PROXY_HOST", "127.0.0.1")
    port = int(os.getenv("PROXY_PORT", "8080"))
    debug = os.getenv("PROXY_DEBUG", "false").lower() in {"1", "true", "yes", "on"}

    print("Starting CORS proxy server for Ollama...")
    print(f"Server will run on http://{host}:{port}")
    print("Make sure Ollama is running on http://localhost:11434")
    app.run(host=host, port=port, debug=debug)
