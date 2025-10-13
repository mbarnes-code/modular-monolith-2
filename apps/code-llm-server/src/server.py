from fastapi import FastAPI

app = FastAPI(title="Code LLM Server")


@app.get("/")
async def root():
    return {"message": "Code LLM Server", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/generate")
async def generate(prompt: str):
    return {"response": f"Generated response for: {prompt}", "model": "code-llm"}
