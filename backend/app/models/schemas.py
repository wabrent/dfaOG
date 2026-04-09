from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any
from enum import Enum
from datetime import datetime


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class DimensionScore(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    UNKNOWN = "UNKNOWN"


class AuditRequest(BaseModel):
    protocol_address: str = Field(..., description="Smart contract address to audit")
    protocol_name: Optional[str] = Field(None, description="Optional protocol name for context")
    chain: str = Field("ethereum", description="Blockchain network")
    include_enhanced_data: bool = Field(True, description="Include enhanced data from external APIs")
    
    class Config:
        extra = "forbid"


class DimensionAnalysis(BaseModel):
    tvl_risk: DimensionScore
    approval_risk: DimensionScore
    code_risk: DimensionScore
    governance_risk: DimensionScore
    economic_risk: DimensionScore
    liquidity_risk: DimensionScore


class ProofInfo(BaseModel):
    transaction_hash: str
    settlement_mode: str
    model: str
    timestamp: datetime
    explorer_url: Optional[str] = None


class Recommendation(BaseModel):
    priority: Literal["HIGH", "MEDIUM", "LOW"]
    title: str
    description: str
    action_items: List[str]


class AuditResponse(BaseModel):
    protocol: str
    address: str
    chain: str
    risk_score: int = Field(..., ge=0, le=100)
    risk_level: RiskLevel
    confidence: int = Field(..., ge=0, le=100)
    dimensions: DimensionAnalysis
    key_findings: List[str]
    recommendations: List[Recommendation]
    proof: ProofInfo
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        extra = "forbid"


class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None
    request_id: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    version: str
    opengradient_connected: bool
    cache_available: bool
    timestamp: datetime