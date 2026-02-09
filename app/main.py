"""
FastAPI main application entry point with JWT Authentication
"""
import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from app.core.config import settings
from app.api import routes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    description="Todo Backend API with JWT Authentication and Kafka Integration"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Include routers
app.include_router(routes.router)


@app.get("/")
async def root():
    """
    Root endpoint - returns index.html for the login page
    
    Returns:
        HTML content of the login page
    """
    index_path = Path(__file__).parent.parent / "static" / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    else:
        return JSONResponse(
            status_code=200,
            content={"status": "Todo backend running"}
        )


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    
    Returns:
        Health status and version
    """
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "version": settings.APP_VERSION,
            "app": settings.APP_NAME
        }
    )


@app.on_event("startup")
async def startup_event():
    """
    Startup event handler
    """
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Kafka broker: {settings.KAFKA_BROKER}")
    logger.info(f"Kafka topic: {settings.KAFKA_TOPIC}")
    logger.info(f"JWT Algorithm: {settings.ALGORITHM}")
    logger.info(f"Token expiry: {settings.ACCESS_TOKEN_EXPIRE_MINUTES} minutes")
    logger.info("🚀 Server is ready. Visit http://localhost:8000 in your browser")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown event handler
    """
    logger.info(f"Shutting down {settings.APP_NAME}")
    # Close Kafka connections
    from app.services.kafka_service import kafka_service
    kafka_service.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )
