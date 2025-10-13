# Jane Orchestrator

The central orchestration service for the Jane Monorepo. This FastAPI service coordinates requests between the Jane UI and specialized LLM servers.

## Purpose

Jane Orchestrator acts as the intelligent routing layer that:
- Receives queries from the Jane UI
- Determines which LLM server(s) to use based on query type and domain
- Manages request/response flow between services
- Handles caching, rate limiting, and error handling
- Aggregates responses from multiple LLM servers when needed

## Technology Stack

- **Framework**: FastAPI 0.115.0
- **Server**: Uvicorn 0.34.2
- **Python**: 3.12
- **Data Validation**: Pydantic 2.0.0

## Setup

### Prerequisites

- Python 3.12.x
- pip

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Key environment variables:
- `ENVIRONMENT`: Environment name (development, staging, production)
- `PORT`: Server port (default: 8000)
- `CYBER_LLM_URL`: URL for Cyber LLM Server
- `MTG_LLM_URL`: URL for MTG LLM Server
- `CODE_LLM_URL`: URL for Code LLM Server
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

## Running the Service

### Development

```bash
# Using NX
npx nx serve jane-orchestrator

# Direct with Uvicorn
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Production

```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker

```bash
# Build
docker build -t jane-orchestrator:latest -f Dockerfile .

# Run
docker run -p 8000:8000 jane-orchestrator:latest
```

## API Endpoints

### Health Endpoints

#### GET /health
Liveness probe - checks if service is running.

**Response:**
```json
{
  "status": "healthy"
}
```

#### GET /ready
Readiness probe - checks if service is ready to accept traffic.

**Response:**
```json
{
  "status": "ready",
  "dependencies": {
    "llm_servers": "connected"
  }
}
```

### Query Endpoints

#### POST /query
Submit a query to be processed by appropriate LLM server.

**Request:**
```json
{
  "query": "Analyze this code for vulnerabilities",
  "domain": "cyber",
  "context": {
    "language": "python"
  }
}
```

**Response:**
```json
{
  "id": "query-123",
  "status": "completed",
  "response": {
    "text": "Analysis results...",
    "confidence": 0.95
  }
}
```

## Architecture

```
Jane UI → Jane Orchestrator → LLM Servers
                ↓
            Cache/DB
```

The orchestrator:
1. Receives query from UI
2. Validates and enriches request
3. Routes to appropriate LLM server(s)
4. Caches results
5. Returns aggregated response

## Deployment

### Environment Variables

See `.env.example` for all available configuration options.

### Kubernetes

Deploy using the provided manifests:

```bash
kubectl apply -k infrastructure/kubernetes/overlays/production/
```

### Docker Compose

```bash
docker-compose -f infrastructure/docker/docker-compose.yml up jane-orchestrator
```

## Development

### Adding New Endpoints

1. Create new route in `src/api/`
2. Add to `main.py` router
3. Write tests
4. Update API documentation

### Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=src --cov-report=html
```

### Logging

The service uses Python's standard logging library:

```python
import logging
logger = logging.getLogger(__name__)
```

Log levels can be configured via `LOG_LEVEL` environment variable.

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9
```

**LLM servers not reachable:**
- Check LLM server URLs in `.env`
- Verify LLM servers are running
- Check network connectivity

**High memory usage:**
- Reduce number of workers
- Check for memory leaks in endpoints
- Review caching strategy

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for development workflow and guidelines.

## License

See repository root for license information.
