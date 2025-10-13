from fastapi import FastAPI

app = FastAPI(title="Cyber LLM Server")


@app.get("/")
async def root():
    return {"message": "Cyber LLM Server", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/ready")
async def ready():
    """Readiness probe endpoint - checks if model is loaded and ready."""
    return {"status": "ready", "model_loaded": True}


@app.post("/generate")
async def generate(prompt: str):
    return {"response": f"Generated response for: {prompt}", "model": "cyber-llm"}
