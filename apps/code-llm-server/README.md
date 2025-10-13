# Code LLM Server

Python vLLM server for code generation and analysis tasks.

## Structure

- `src/server.py` - FastAPI application
- `models/` - Model configurations and weights
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container configuration

## Running

```bash
# Development
npx nx serve code-llm-server

# Docker
docker build -t code-llm-server .
docker run -p 8003:8003 code-llm-server
```

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /generate` - Generate text from prompt
