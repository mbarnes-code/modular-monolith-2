import logging
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Cyber LLM Server",
    description="Cybersecurity-focused LLM service",
    version="1.0.0"
)


class GenerateRequest(BaseModel):
    """Request model for text generation."""
    prompt: str = Field(..., min_length=1, description="Input prompt for generation")
    max_tokens: int = Field(default=100, ge=1, le=2048, description="Maximum tokens to generate")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature")


class GenerateResponse(BaseModel):
    """Response model for text generation."""
    response: str = Field(..., description="Generated text")
    model: str = Field(..., description="Model identifier")
    tokens_used: int = Field(..., description="Number of tokens used")


@app.get("/", response_model=Dict[str, Any])
async def root():
    """Root endpoint providing service information."""
    logger.info("Root endpoint accessed")
    return {
        "message": "Cyber LLM Server",
        "status": "running",
        "version": "1.0.0",
        "model": "cyber-llm-v1",
        "endpoints": {
            "health": "/health",
            "readiness": "/ready",
            "generate": "/generate"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint for liveness probes."""
    logger.debug("Health check requested")
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/ready")
async def ready():
    """Readiness probe endpoint - checks if model is loaded and ready."""
    logger.debug("Readiness check requested")
    
    # Best practice: Check if model is actually loaded
    # In production, implement actual model status check
    model_loaded = True  # Placeholder
    
    if not model_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded"
        )
    
    return {
        "status": "ready",
        "model_loaded": True,
        "model_version": "cyber-llm-v1"
    }


@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    """
    Generate text using the cybersecurity LLM.
    Best practices: Input validation, error handling, logging.
    """
    logger.info(f"Generation requested with prompt length: {len(request.prompt)}")
    
    try:
        # Best practice: Validate input
        if not request.prompt or not request.prompt.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Prompt cannot be empty"
            )
        
        # In production, this would call the actual vLLM model
        generated_text = f"Generated cybersecurity response for: {request.prompt[:50]}..."
        tokens_used = len(request.prompt.split()) + request.max_tokens
        
        logger.info(f"Generation completed, tokens used: {tokens_used}")
        
        return GenerateResponse(
            response=generated_text,
            model="cyber-llm-v1",
            tokens_used=tokens_used
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Generation failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Generation failed: {str(e)}"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "message": str(exc)
        }
    )


@app.on_event("startup")
async def startup_event():
    """Initialize model and resources on startup."""
    logger.info("Cyber LLM Server starting up...")
    # In production: Load vLLM model here


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    logger.info("Cyber LLM Server shutting down...")
    # In production: Unload model and clean up
