from fastapi import FastAPI

app = FastAPI(title="MTG LLM Server")


@app.get("/")
async def root():
    return {"message": "MTG LLM Server", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/generate")
async def generate(prompt: str):
    return {"response": f"Generated response for: {prompt}", "model": "mtg-llm"}
