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
    title="Code LLM Server",
    description="Code generation focused LLM service",
    version="1.0.0"
)


class GenerateRequest(BaseModel):
    """Request model for code generation."""
    prompt: str = Field(..., min_length=1, description="Input prompt for generation")
    max_tokens: int = Field(default=100, ge=1, le=2048, description="Maximum tokens to generate")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature")
    language: str = Field(default="python", description="Programming language")


class GenerateResponse(BaseModel):
    """Response model for code generation."""
    response: str = Field(..., description="Generated code")
    model: str = Field(..., description="Model identifier")
    tokens_used: int = Field(..., description="Number of tokens used")
    language: str = Field(..., description="Programming language")


@app.get("/", response_model=Dict[str, Any])
async def root():
    """Root endpoint providing service information."""
    logger.info("Root endpoint accessed")
    return {
        "message": "Code LLM Server",
        "status": "running",
        "version": "1.0.0",
        "model": "code-llm-v1",
        "supported_languages": ["python", "javascript", "typescript", "java", "go", "rust"],
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
    
    model_loaded = True  # Placeholder for actual model check
    
    if not model_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded"
        )
    
    return {
        "status": "ready",
        "model_loaded": True,
        "model_version": "code-llm-v1"
    }


@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    """
    Generate code using the specialized LLM.
    Best practices: Input validation, error handling, logging.
    """
    logger.info(f"Code generation requested for language: {request.language}")
    
    try:
        if not request.prompt or not request.prompt.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Prompt cannot be empty"
            )
        
        # Validate programming language
        supported_languages = ["python", "javascript", "typescript", "java", "go", "rust"]
        if request.language not in supported_languages:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported language. Supported: {', '.join(supported_languages)}"
            )
        
        # In production, this would call the actual vLLM model
        generated_code = f"# Generated {request.language} code for: {request.prompt[:50]}..."
        tokens_used = len(request.prompt.split()) + request.max_tokens
        
        logger.info(f"Code generation completed, tokens used: {tokens_used}")
        
        return GenerateResponse(
            response=generated_code,
            model="code-llm-v1",
            tokens_used=tokens_used,
            language=request.language
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Code generation failed: {e}", exc_info=True)
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
    logger.info("Code LLM Server starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    logger.info("Code LLM Server shutting down...")
