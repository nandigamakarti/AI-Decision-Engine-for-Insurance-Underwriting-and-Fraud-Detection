"""
FastAPI Application - Risk Assessment Engine Entry Point
"""

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from config import settings
from api.routes import router as risk_assessment_router
from api.risk_routes import router as risk_calculator_router
from api.proposal_routes import router as proposal_router
from api.ai_risk_routes import router as ai_risk_router
from api.image_routes import router as image_router
from api.medical_code_routes import router as medical_code_router
from services.ollama_service import ollama_service

# Configure logging
logging.basicConfig(
    level=settings.API_LOG_LEVEL.upper(),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on your deployment needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(risk_assessment_router)
app.include_router(risk_calculator_router)
app.include_router(proposal_router)
app.include_router(ai_risk_router)
app.include_router(image_router)
app.include_router(medical_code_router)


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Ollama Base URL: {settings.OLLAMA_BASE_URL}")
    logger.info(f"Ollama Model: {settings.OLLAMA_MODEL}")
    
    # Initialize database (create tables if they don't exist)
    try:
        from db import init_db
        logger.info("Initializing database...")
        init_db()
        logger.info("Database initialized successfully. All tables are ready.")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        logger.warning("Application will continue, but database features may not work.")
    
    # Check Ollama connectivity
    if not ollama_service.health_check():
        logger.warning(
            f"Warning: Could not connect to Ollama at {settings.OLLAMA_BASE_URL}. "
            "Make sure Ollama is running."
        )


@app.get("/", tags=["root"], summary="API Root", description="Welcome message and API information")
async def root():
    """
    Root endpoint providing API information.

    Returns welcome message and links to documentation.
    """
    return {
        "message": "Welcome to Insurance Risk Assessment Engine",
        "version": settings.APP_VERSION,
        "powered_by": "Ollama AI + GPT-OSS-20B",
        "documentation": {
            "swagger": "http://127.0.0.1:8000/docs",
            "redoc": "http://127.0.0.1:8000/redoc",
            "openapi": "http://127.0.0.1:8000/openapi.json"
        },
        "endpoints": {
            "ai_risk_assessment": "POST /api/risk-assessment",
            "health_check": "GET /api/health",
            "ollama_status": "GET /api/ollama-status",
            "database_status": "GET /api/database-status",
            "list_proposals": "GET /api/proposals",
            "rule_based_calculators": {
                "demographic": "POST /api/risk/demographic",
                "financial": "POST /api/risk/financial",
                "medical": "POST /api/risk/medical",
                "regional": "POST /api/risk/regional",
                "claims": "POST /api/risk/claims",
                "agent": "POST /api/risk/agent",
                "product": "POST /api/risk/product",
                "combined": "POST /api/risk/combined"
            },
            "ai_powered_calculators": {
                "demographic": "POST /api/ai-risk/demographic",
                "financial": "POST /api/ai-risk/financial",
                "medical": "POST /api/ai-risk/medical",
                "regional": "POST /api/ai-risk/regional",
                "claims": "POST /api/ai-risk/claims",
                "agent": "POST /api/ai-risk/agent",
                "product": "POST /api/ai-risk/product",
                "combined": "POST /api/ai-risk/combined"
            }
        }
    }


@app.get("/api/ollama-status", tags=["system"], summary="Ollama Service Status")
async def ollama_status():
    """Check if Ollama service is running and accessible."""
    is_healthy = ollama_service.health_check()
    
    if not is_healthy:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "message": f"Could not connect to Ollama at {settings.OLLAMA_BASE_URL}",
                "service": "Ollama"
            }
        )
    
    return {
        "status": "healthy",
        "service": "Ollama",
        "base_url": settings.OLLAMA_BASE_URL,
        "model": settings.OLLAMA_MODEL,
        "temperature": settings.OLLAMA_TEMPERATURE,
        "top_p": settings.OLLAMA_TOP_P
    }


@app.get("/api/database-status", tags=["system"], summary="Database Connection Status")
async def database_status():
    """Check if database is connected and tables are created."""
    try:
        from db import engine
        from sqlalchemy import inspect, text
        
        # Test connection
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        
        # Get table names
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        return {
            "status": "healthy",
            "service": "PostgreSQL",
            "database_url": settings.DATABASE_URL.split("@")[1] if "@" in settings.DATABASE_URL else "hidden",
            "tables_count": len(tables),
            "tables": sorted(tables),
            "message": "Database is connected and tables are ready"
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "message": f"Database connection failed: {str(e)}",
                "service": "PostgreSQL"
            }
        )


def custom_openapi():
    """Customize OpenAPI schema."""
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=settings.APP_DESCRIPTION,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
        log_level=settings.API_LOG_LEVEL
    )
