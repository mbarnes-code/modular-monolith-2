from fastapi import FastAPI

app = FastAPI(title="Orchestrator Service")


@app.get("/")
async def root():
    return {"message": "Orchestrator Service", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/ready")
async def ready():
    """Readiness probe endpoint - checks if service is ready to accept traffic."""
    # Check dependencies (LLM servers, databases, etc.)
    return {"status": "ready", "dependencies": {"llm_servers": "connected"}}
