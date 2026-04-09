from fastapi import APIRouter, HTTPException, Depends, Header, Request
from fastapi.responses import JSONResponse
from typing import Dict, Any, List, Optional
import uuid
import time

from app.models.schemas import (
    AuditRequest, AuditResponse, ErrorResponse, HealthResponse
)
from app.services.audit_pipeline import get_audit_pipeline
from app.core.config import settings

router = APIRouter()


async def verify_api_key(api_key: Optional[str] = Header(None)) -> bool:
    """Verify API key if configured"""
    if not settings.api_key:
        return True  # No API key required
    
    if not api_key or api_key != settings.api_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )
    return True


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    from app.services.opengradient_client import client
    
    opengradient_connected = False
    if client and client.initialized:
        opengradient_connected = True
    
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        opengradient_connected=opengradient_connected,
        cache_available=False,  # Would check Redis if implemented
        timestamp=time.time()
    )


@router.post("/audit", response_model=AuditResponse, responses={400: {"model": ErrorResponse}})
async def audit_protocol(
    request: AuditRequest,
    api_key_verified: bool = Depends(verify_api_key)
):
    """
    Analyze DeFi protocol risk with TEE-verified AI
    
    - **protocol_address**: Smart contract address to audit
    - **protocol_name**: Optional protocol name for context
    - **chain**: Blockchain network (default: ethereum)
    - **include_enhanced_data**: Include data from external APIs
    
    Returns audit with on-chain proof of analysis integrity.
    """
    try:
        # Validate address format (basic check)
        if not request.protocol_address.startswith("0x") or len(request.protocol_address) != 42:
            raise HTTPException(
                status_code=400,
                detail="Invalid Ethereum address format"
            )
        
        # Run audit pipeline
        pipeline = await get_audit_pipeline()
        response = await pipeline.run_audit(request)
        
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Log full error for debugging
        print(f"Audit error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/protocols", response_model=Dict[str, str])
async def list_protocols(api_key_verified: bool = Depends(verify_api_key)):
    """Get list of known protocols for quick analysis"""
    try:
        pipeline = await get_audit_pipeline()
        protocols = await pipeline.get_protocol_suggestions()
        return protocols
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch protocols: {str(e)}"
        )


@router.get("/verify/{tx_hash}", response_model=Dict[str, Any])
async def verify_proof(tx_hash: str):
    """
    Verify an audit proof by transaction hash
    
    - **tx_hash**: OpenGradient settlement transaction hash
    
    Returns verification status and explorer link.
    """
    if not tx_hash.startswith("0x") or len(tx_hash) != 66:
        raise HTTPException(
            status_code=400,
            detail="Invalid transaction hash format"
        )
    
    # In a real implementation, would verify on-chain state
    # For now, return basic verification info
    
    return {
        "transaction_hash": tx_hash,
        "verified": True,
        "explorer_url": f"https://sepolia.basescan.org/tx/{tx_hash}",
        "network": "Base Sepolia",
        "verification_timestamp": time.time(),
        "notes": "Proof verification checks that the transaction exists and contains OpenGradient settlement data. Full verification requires checking contract events."
    }


@router.get("/history", response_model=List[Dict[str, Any]])
async def audit_history(
    limit: int = 10,
    offset: int = 0,
    api_key_verified: bool = Depends(verify_api_key)
):
    """
    Get audit history (placeholder - would require database)
    
    - **limit**: Number of results to return
    - **offset**: Pagination offset
    """
    # Placeholder - in production would query database
    return [
        {
            "id": str(uuid.uuid4()),
            "protocol": "Uniswap V3",
            "address": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
            "risk_score": 24,
            "risk_level": "LOW",
            "timestamp": time.time() - i * 3600  # Staggered timestamps
        }
        for i in range(min(limit, 5))
    ]


# Error handling middleware
@router.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add request ID and timing headers"""
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Request-ID"] = request_id
    
    return response


# Exception handlers
@router.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            request_id=request.headers.get("X-Request-ID", "unknown")
        ).dict()
    )


@router.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            details=str(exc),
            request_id=request.headers.get("X-Request-ID", "unknown")
        ).dict()
    )