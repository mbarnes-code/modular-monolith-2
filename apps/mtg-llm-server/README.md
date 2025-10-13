# MTG LLM Server

Python vLLM server for Magic: The Gathering related LLM tasks.

## Structure

- `src/server.py` - FastAPI application
- `models/` - Model configurations and weights
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container configuration

## Running

```bash
# Development
npx nx serve mtg-llm-server

# Docker
docker build -t mtg-llm-server .
docker run -p 8002:8002 mtg-llm-server
```

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /generate` - Generate text from prompt
