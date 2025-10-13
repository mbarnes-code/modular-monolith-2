# API Reference

This document provides comprehensive API documentation for all services in the Jane Monorepo.

## Table of Contents

- [Jane Orchestrator API](#jane-orchestrator-api)
- [Cyber LLM Server API](#cyber-llm-server-api)
- [MTG LLM Server API](#mtg-llm-server-api)
- [Code LLM Server API](#code-llm-server-api)
- [Common Patterns](#common-patterns)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)

## Jane Orchestrator API

Base URL: `http://localhost:8000` (development) or `https://api.example.com` (production)

### Health Endpoints

#### GET /health

Check if service is alive.

**Response:**
```json
{
  "status": "healthy"
}
```

**Status Codes:**
- `200`: Service is healthy
- `503`: Service is unhealthy

#### GET /ready

Check if service is ready to accept traffic.

**Response:**
```json
{
  "status": "ready",
  "dependencies": {
    "cyber_llm": "connected",
    "mtg_llm": "connected",
    "code_llm": "connected"
  }
}
```

**Status Codes:**
- `200`: Service is ready
- `503`: Service is not ready

### Query Endpoints

#### POST /query

Submit a query to be processed by the appropriate LLM.

**Request Body:**
```json
{
  "query": "Analyze this code for vulnerabilities",
  "domain": "cyber",
  "context": {
    "language": "python",
    "framework": "django"
  },
  "options": {
    "temperature": 0.7,
    "max_tokens": 1000
  }
}
```

**Parameters:**
- `query` (string, required): The query text
- `domain` (string, required): Target domain (`cyber`, `mtg`, `code`)
- `context` (object, optional): Additional context for the query
- `options` (object, optional): LLM configuration options

**Response:**
```json
{
  "id": "query-123456",
  "status": "completed",
  "domain": "cyber",
  "query": "Analyze this code for vulnerabilities",
  "response": {
    "text": "Found 3 potential vulnerabilities...",
    "confidence": 0.92,
    "sources": ["analysis-engine", "vuln-db"]
  },
  "timestamp": "2025-10-13T09:00:00Z",
  "processing_time": 1.234
}
```

**Status Codes:**
- `200`: Query processed successfully
- `400`: Invalid request
- `422`: Validation error
- `500`: Internal server error

#### GET /query/{query_id}

Retrieve results for a specific query.

**Response:**
```json
{
  "id": "query-123456",
  "status": "completed",
  "domain": "cyber",
  "response": {
    "text": "...",
    "confidence": 0.92
  },
  "timestamp": "2025-10-13T09:00:00Z"
}
```

**Status Codes:**
- `200`: Query found
- `404`: Query not found

### Batch Query Endpoints

#### POST /query/batch

Submit multiple queries at once.

**Request Body:**
```json
{
  "queries": [
    {
      "query": "First query",
      "domain": "cyber"
    },
    {
      "query": "Second query",
      "domain": "mtg"
    }
  ]
}
```

**Response:**
```json
{
  "batch_id": "batch-789",
  "queries": [
    {
      "id": "query-123",
      "status": "processing"
    },
    {
      "id": "query-124",
      "status": "processing"
    }
  ]
}
```

## Cyber LLM Server API

Base URL: `http://localhost:8001` (development)

### Health Endpoints

#### GET /health

Check service health.

**Response:**
```json
{
  "status": "healthy",
  "model": "cyber-model-v1",
  "gpu_available": true
}
```

#### GET /ready

Check if model is loaded and ready.

**Response:**
```json
{
  "status": "ready",
  "model_loaded": true,
  "memory_usage": "2.5GB"
}
```

### Analysis Endpoints

#### POST /analyze

Analyze cybersecurity-related content.

**Request Body:**
```json
{
  "content": "Sample code or log data",
  "analysis_type": "vulnerability",
  "options": {
    "detailed": true,
    "include_remediation": true
  }
}
```

**Parameters:**
- `content` (string, required): Content to analyze
- `analysis_type` (string, required): Type of analysis (`vulnerability`, `threat`, `ioc`)
- `options` (object, optional): Analysis options

**Response:**
```json
{
  "analysis_id": "analysis-456",
  "type": "vulnerability",
  "findings": [
    {
      "severity": "high",
      "category": "sql-injection",
      "description": "Potential SQL injection vulnerability",
      "location": "line 42",
      "remediation": "Use parameterized queries"
    }
  ],
  "confidence": 0.95,
  "timestamp": "2025-10-13T09:00:00Z"
}
```

## MTG LLM Server API

Base URL: `http://localhost:8002` (development)

### Health Endpoints

#### GET /health

Check service health.

**Response:**
```json
{
  "status": "healthy",
  "model": "mtg-model-v1"
}
```

#### GET /ready

Check if model is loaded and ready.

**Response:**
```json
{
  "status": "ready",
  "model_loaded": true
}
```

### MTG Query Endpoints

#### POST /query

Query MTG-related information.

**Request Body:**
```json
{
  "query": "What are the best commanders for a graveyard strategy?",
  "format": "commander",
  "options": {
    "budget": "moderate",
    "color_identity": ["B", "G"]
  }
}
```

**Parameters:**
- `query` (string, required): The MTG-related query
- `format` (string, optional): MTG format (`standard`, `modern`, `commander`)
- `options` (object, optional): Additional filters

**Response:**
```json
{
  "query_id": "mtg-query-789",
  "recommendations": [
    {
      "card_name": "Meren of Clan Nel Toth",
      "relevance": 0.98,
      "reasoning": "Excellent graveyard recursion...",
      "synergies": ["Living Death", "Animate Dead"]
    }
  ],
  "timestamp": "2025-10-13T09:00:00Z"
}
```

#### POST /combo-analysis

Analyze card combos.

**Request Body:**
```json
{
  "cards": ["Thassa's Oracle", "Demonic Consultation"],
  "format": "commander"
}
```

**Response:**
```json
{
  "combo_id": "combo-123",
  "is_valid_combo": true,
  "combo_type": "win-condition",
  "description": "Exile entire library, win with Thassa's Oracle trigger",
  "requirements": ["2 mana", "both cards in hand"],
  "legality": {
    "commander": "legal",
    "modern": "banned"
  }
}
```

## Code LLM Server API

Base URL: `http://localhost:8003` (development)

### Health Endpoints

#### GET /health

Check service health.

**Response:**
```json
{
  "status": "healthy",
  "model": "code-model-v1"
}
```

#### GET /ready

Check if model is loaded and ready.

**Response:**
```json
{
  "status": "ready",
  "model_loaded": true
}
```

### Code Analysis Endpoints

#### POST /analyze

Analyze code for issues.

**Request Body:**
```json
{
  "code": "def vulnerable_function(user_input):\n    sql = f\"SELECT * FROM users WHERE name = '{user_input}'\"",
  "language": "python",
  "analysis_types": ["security", "quality", "performance"]
}
```

**Parameters:**
- `code` (string, required): Code to analyze
- `language` (string, required): Programming language
- `analysis_types` (array, optional): Types of analysis to perform

**Response:**
```json
{
  "analysis_id": "code-analysis-321",
  "language": "python",
  "issues": [
    {
      "type": "security",
      "severity": "critical",
      "line": 2,
      "message": "SQL injection vulnerability",
      "suggestion": "Use parameterized queries or ORM"
    }
  ],
  "metrics": {
    "complexity": 3,
    "maintainability": "B"
  }
}
```

#### POST /generate

Generate code from description.

**Request Body:**
```json
{
  "description": "Create a function that sorts a list of integers in descending order",
  "language": "python",
  "options": {
    "include_tests": true,
    "include_docstring": true
  }
}
```

**Response:**
```json
{
  "generation_id": "gen-654",
  "code": "def sort_descending(numbers: List[int]) -> List[int]:\n    \"\"\"Sort a list of integers in descending order.\"\"\"\n    return sorted(numbers, reverse=True)",
  "tests": "def test_sort_descending():\n    assert sort_descending([3, 1, 2]) == [3, 2, 1]",
  "explanation": "Uses Python's built-in sorted() function with reverse=True"
}
```

## Common Patterns

### Authentication

All API endpoints require authentication using JWT tokens (when enabled).

**Request Header:**
```
Authorization: Bearer <token>
```

### Pagination

List endpoints support pagination:

**Query Parameters:**
- `page` (integer): Page number (default: 1)
- `per_page` (integer): Items per page (default: 20, max: 100)

**Response:**
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "pages": 5
  }
}
```

### Filtering

Use query parameters for filtering:

```
GET /queries?domain=cyber&status=completed&from=2025-10-01
```

### Sorting

Use `sort` parameter:

```
GET /queries?sort=-created_at  # Descending
GET /queries?sort=created_at   # Ascending
```

## Error Handling

All endpoints return consistent error responses.

### Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": [
      {
        "field": "domain",
        "message": "Must be one of: cyber, mtg, code"
      }
    ]
  },
  "timestamp": "2025-10-13T09:00:00Z",
  "request_id": "req-789"
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid request data |
| `UNAUTHORIZED` | 401 | Authentication required |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `RATE_LIMITED` | 429 | Rate limit exceeded |
| `INTERNAL_ERROR` | 500 | Server error |
| `SERVICE_UNAVAILABLE` | 503 | Service temporarily unavailable |

## Rate Limiting

Rate limits apply per API key or IP address.

**Default Limits:**
- 100 requests per minute
- 1000 requests per hour
- 10000 requests per day

**Rate Limit Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1697184000
```

**Rate Limit Exceeded Response:**
```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Rate limit exceeded",
    "retry_after": 60
  }
}
```

## WebSocket API

Real-time updates via WebSocket.

### Connection

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'subscribe',
    channel: 'queries'
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Update:', data);
};
```

### Message Format

**Client to Server:**
```json
{
  "type": "subscribe",
  "channel": "queries",
  "filters": {
    "domain": "cyber"
  }
}
```

**Server to Client:**
```json
{
  "type": "update",
  "channel": "queries",
  "data": {
    "query_id": "query-123",
    "status": "completed",
    "response": {...}
  }
}
```

## SDK Examples

### Python

```python
import requests

base_url = "http://localhost:8000"

# Submit query
response = requests.post(
    f"{base_url}/query",
    json={
        "query": "Analyze this threat",
        "domain": "cyber"
    }
)
result = response.json()
print(result)
```

### JavaScript/TypeScript

```typescript
const baseUrl = 'http://localhost:8000';

// Submit query
const response = await fetch(`${baseUrl}/query`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    query: 'Analyze this threat',
    domain: 'cyber',
  }),
});

const result = await response.json();
console.log(result);
```

## Testing

### Interactive API Documentation

FastAPI provides interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Example cURL Commands

```bash
# Health check
curl http://localhost:8000/health

# Submit query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Test query",
    "domain": "cyber"
  }'

# Get query result
curl http://localhost:8000/query/query-123
```

## Versioning

API versioning uses URL path:

- Current: `/v1/query`
- Future: `/v2/query`

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [OpenAPI Specification](https://swagger.io/specification/)
- [REST API Best Practices](https://restfulapi.net)
