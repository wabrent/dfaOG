from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import time
import uuid

from app.core.config import settings
from app.api.routes import router
from app.services.opengradient_client import get_opengradient_client

app = FastAPI(
    title="DeFi Risk Auditor API",
    description="TEE-verified DeFi protocol risk analysis with on-chain proof",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api", tags=["api"])


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print("Starting DeFi Risk Auditor API...")
    
    # Initialize OpenGradient client
    try:
        client = await get_opengradient_client()
        print(f"✓ OpenGradient initialized with model: {client.model.name}")
        print(f"✓ Settlement mode: {client.settlement_mode.name}")
    except Exception as e:
        print(f"⚠️  OpenGradient initialization failed: {e}")
        print("  Some features may be unavailable")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("Shutting down DeFi Risk Auditor API...")


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add security headers to all responses"""
    response = await call_next(request)
    
    security_headers = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Content-Security-Policy": "default-src 'self'",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "interest-cohort=()",
    }
    
    for header, value in security_headers.items():
        response.headers[header] = value
    
    return response


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "DeFi Risk Auditor API",
        "version": "1.0.0",
        "description": "TEE-verified DeFi protocol risk analysis",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/api/health",
            "audit": "/api/audit",
            "protocols": "/api/protocols",
            "verify": "/api/verify/{tx_hash}",
            "history": "/api/history",
        },
        "openapi_schema": "/openapi.json",
    }


@app.get("/openapi.json", include_in_schema=False)
async def get_openapi():
    """Get OpenAPI schema"""
    return app.openapi()


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info" if settings.debug else "warning",
    )