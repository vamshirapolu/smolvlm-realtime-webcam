# SmolVLM real-time camera demo

![demo](./demo.png)

This repository is a simple demo for how to use llama.cpp server with SmolVLM 500M to get real-time object detection

## How to setup

1. Install [llama.cpp](https://github.com/ggml-org/llama.cpp)
2. Run `llama-server -hf ggml-org/SmolVLM-500M-Instruct-GGUF`  
   Note: you may need to add `-ngl 99` to enable GPU (if you are using NVidia/AMD/Intel GPU)  
   Note (2): You can also try other models [here](https://github.com/ggml-org/llama.cpp/blob/master/docs/multimodal.md)
3. Open `index.html`
4. Optionally change the instruction (for example, make it returns JSON)
5. Click on "Start" and enjoy

## Setup Instructions for CORS Proxy Server

### Prerequisites

1. **For Ollama (local AI)**:
   - Install [Ollama](https://ollama.ai/)
   - Pull a vision model: `ollama pull llava` or `ollama pull llava:13b`
   - Start Ollama: `ollama serve`

2. **For OpenAI**:
   - Get an OpenAI API key from [OpenAI Platform](https://platform.openai.com/)

### Installation

1. Clone or download this repository
2. Install Python dependencies for the CORS proxy server:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the CORS Proxy Server** (required for Ollama, recommended for OpenAI to avoid CORS):
   ```bash
   python proxy_server.py
   ```
   The proxy server will run on `http://localhost:8080`
   - Health check: `http://localhost:8080/health`
   - Ollama proxy endpoint (POST): `http://localhost:8080/api/generate`
   - OpenAI proxy endpoint (POST): `http://localhost:8080/api/openai`
   - Note: `http://localhost:8080/` returns 404 because the proxy does not serve a web page.

2. **Start Ollama** (if using local AI):
   ```bash
   ollama serve
   ```
   Ollama will run on `http://localhost:11434`

3. **Open the web application**:
   - Open `index.html` in a web browser (or serve it locally, e.g. `python -m http.server 8000` and visit `http://localhost:8000/index.html`)
   - Grant camera permissions when prompted
   - Select your preferred API provider (Ollama or OpenAI)
   - Configure settings and click "Start"

## Configuration

- **API Provider**: Choose between Ollama (local) or OpenAI (cloud)
- **Model**: Specify the model name (e.g., `llava` for Ollama, `gpt-4o` for OpenAI)
- **Interval**: Set how frequently to analyze the camera feed
- **Text-to-Speech**: Toggle spoken responses on/off
- **Release camera on Stop**: Optionally stop the camera stream when you click Stop
- **OpenAI Key**: Set `OPENAI_API_KEY` on the proxy server.

### Proxy Environment Variables (optional)

- `OLLAMA_BASE_URL`: Default Ollama URL used by the proxy (e.g., `http://localhost:11434`)
- `OPENAI_API_BASE`: Override OpenAI base URL (default `https://api.openai.com/v1`)
- `PROXY_HOST`: Bind address for the proxy (default `127.0.0.1`)
- `PROXY_PORT`: Bind port for the proxy (default `8080`)
- `PROXY_DEBUG`: Enable Flask debug mode (`true`/`false`, default `false`)
- `CORS_ORIGINS`: Comma-separated list of allowed origins (defaults to allow all)

## Troubleshooting

### CORS Issues
If you encounter CORS errors, make sure:
1. The proxy server (`proxy_server.py`) is running on port 8080
2. Ollama is running on port 11434
3. You're accessing the web app via `http://` or `https://` (not `file://`)

### Camera Access
- Ensure you've granted camera permissions
- Use HTTPS or localhost for camera access
- Check that no other applications are using the camera

### API Issues
- **Ollama**: Verify the model is installed (`ollama list`) and Ollama is running
- **OpenAI**: Check your API key is valid and has sufficient credits

## Files

- `index.html` - Main web application
- `proxy_server.py` - CORS proxy server for Ollama API
- `transcribe.py` - Audio transcription utility (Whisper)
- `requirements.txt` - Python dependencies
- `demo.png` - Demo screenshot
