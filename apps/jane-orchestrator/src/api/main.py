from fastapi import FastAPI

app = FastAPI(title="Orchestrator Service")


@app.get("/")
async def root():
    return {"message": "Orchestrator Service", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
