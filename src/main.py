"""
Free BARCODE Application - Main Entry Point
Ứng dụng tạo và in QR code cho máy in nhiệt

Chạy: python -m src.main
hoặc: uvicorn src.main:app --host 0.0.0.0 --port 25000
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from pathlib import Path

from .api.routes import router
from .config.settings import (
    LOG_FILE, 
    LOG_FORMAT, 
    LOG_DATE_FORMAT,
    HOST,
    PORT,
    WORKERS
)

# Setup logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt=LOG_DATE_FORMAT
)

# Also log to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT))
logging.getLogger().addHandler(console_handler)


# Create FastAPI app
app = FastAPI(
    title="Free BARCODE API",
    description="API để tạo và in QR code cho máy in nhiệt",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả origin
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả method
    allow_headers=["*"],  # Cho phép tất cả headers
)

# Include API routes
app.include_router(router, prefix="/api", tags=["barcode"])

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Free BARCODE API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Event khi app khởi động"""
    logging.info("✓ Application started successfully")
    logging.info(f"✓ API Documentation: http://{HOST}:{PORT}/docs")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Event khi app tắt"""
    logging.info("Application shutting down...")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.main:app",
        host=HOST,
        port=PORT,
        reload=True,  # Auto reload on code changes
        log_level="info"
    )
