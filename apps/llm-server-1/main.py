from fastapi import FastAPI

app = FastAPI(title="LLM Server 1")


@app.get("/")
async def root():
    return {"message": "LLM Server 1", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/generate")
async def generate(prompt: str):
    return {"response": f"Generated response for: {prompt}", "model": "llm-1"}
