# Cyber LLM Server

Python vLLM server for cybersecurity-related LLM tasks.

## Structure

- `src/server.py` - FastAPI application
- `models/` - Model configurations and weights
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container configuration

## Running

```bash
# Development
npx nx serve cyber-llm-server

# Docker
docker build -t cyber-llm-server .
docker run -p 8001:8001 cyber-llm-server
```

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /generate` - Generate text from prompt
