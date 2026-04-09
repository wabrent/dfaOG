import asyncio
from typing import Dict, Any
from datetime import datetime
from app.services.opengradient_client import get_opengradient_client
from app.services.protocol_data import get_protocol_data_service
from app.models.schemas import AuditRequest, AuditResponse, DimensionAnalysis, ProofInfo, Recommendation


class AuditPipeline:
    """Main pipeline for DeFi protocol risk auditing"""
    
    async def run_audit(self, request: AuditRequest) -> AuditResponse:
        """
        Execute complete audit pipeline
        
        Args:
            request: Audit request with protocol details
        
        Returns:
            Complete audit response with proof
        """
        # Step 1: Collect protocol data
        data_service = await get_protocol_data_service()
        protocol_data = await data_service.get_protocol_data(
            address=request.protocol_address,
            chain=request.chain
        )
        
        # Use provided protocol name if available
        if request.protocol_name:
            protocol_data["name"] = request.protocol_name
        
        # Step 2: Analyze risk using OpenGradient TEE
        og_client = await get_opengradient_client()
        analysis_result = await og_client.analyze_protocol_risk(protocol_data)
        
        # Step 3: Construct response
        response = self._construct_audit_response(
            request=request,
            protocol_data=protocol_data,
            analysis_result=analysis_result
        )
        
        return response
    
    def _construct_audit_response(
        self,
        request: AuditRequest,
        protocol_data: Dict[str, Any],
        analysis_result: Dict[str, Any]
    ) -> AuditResponse:
        """Construct structured audit response"""
        
        # Build dimension analysis
        dimensions = DimensionAnalysis(
            tvl_risk=analysis_result["dimensions"]["tvl_risk"],
            approval_risk=analysis_result["dimensions"]["approval_risk"],
            code_risk=analysis_result["dimensions"]["code_risk"],
            governance_risk=analysis_result["dimensions"]["governance_risk"],
            economic_risk=analysis_result["dimensions"]["economic_risk"],
            liquidity_risk=analysis_result["dimensions"]["liquidity_risk"]
        )
        
        # Build recommendations
        recommendations = []
        for rec_data in analysis_result.get("recommendations", []):
            recommendation = Recommendation(
                priority=rec_data["priority"],
                title=rec_data["title"],
                description=rec_data["description"],
                action_items=rec_data.get("action_items", [])
            )
            recommendations.append(recommendation)
        
        # Build proof info
        proof_data = analysis_result["proof"]
        proof = ProofInfo(
            transaction_hash=proof_data["transaction_hash"],
            settlement_mode=proof_data["settlement_mode"],
            model=proof_data["model"],
            timestamp=proof_data["timestamp"],
            explorer_url=proof_data.get("explorer_url")
        )
        
        # Construct response
        response = AuditResponse(
            protocol=protocol_data["name"],
            address=request.protocol_address,
            chain=request.chain,
            risk_score=analysis_result["risk_score"],
            risk_level=analysis_result["risk_level"],
            confidence=analysis_result["confidence"],
            dimensions=dimensions,
            key_findings=analysis_result.get("key_findings", []),
            recommendations=recommendations,
            proof=proof,
            metadata={
                "data_sources_used": ["basic_protocol_identification"],
                "enhanced_data_included": request.include_enhanced_data,
                "analysis_timestamp": datetime.utcnow().isoformat(),
                "protocol_tvl": protocol_data.get("tvl", 0),
                "contract_verified": protocol_data.get("contract_verified", False)
            }
        )
        
        return response
    
    async def get_protocol_suggestions(self) -> Dict[str, str]:
        """Get suggested protocols for quick analysis"""
        data_service = await get_protocol_data_service()
        return data_service.get_known_protocols()


# Global pipeline instance
audit_pipeline: Optional[AuditPipeline] = None


async def get_audit_pipeline() -> AuditPipeline:
    """Get or initialize audit pipeline"""
    global audit_pipeline
    if audit_pipeline is None:
        audit_pipeline = AuditPipeline()
    return audit_pipeline