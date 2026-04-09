import sys
import os
from unittest.mock import Mock, patch, AsyncMock

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.models.schemas import AuditRequest, AuditResponse, RiskLevel
from app.services.audit_pipeline import AuditPipeline


class TestAuditPipeline:
    """Test cases for the audit pipeline."""

    @patch("app.services.audit_pipeline.get_protocol_data_service")
    @patch("app.services.audit_pipeline.get_opengradient_client")
    async def test_analyze_protocol_mock(self, mock_get_client, mock_get_data_service):
        """Test protocol analysis with mocked dependencies."""
        # Setup mocks
        mock_protocol_data = {
            "name": "Uniswap V3",
            "address": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
            "chain": "ethereum",
            "tvl": 2500000000,
            "risk_factors": []
        }
        mock_data_service = AsyncMock()
        mock_data_service.get_protocol_data.return_value = mock_protocol_data
        mock_get_data_service.return_value = mock_data_service

        mock_ai_response = {
            "risk_score": 24,
            "risk_level": "LOW",
            "confidence": 87,
            "dimensions": {
                "tvl_risk": "LOW",
                "approval_risk": "MEDIUM",
                "code_risk": "LOW",
                "governance_risk": "LOW",
                "economic_risk": "LOW",
                "liquidity_risk": "LOW"
            },
            "key_findings": ["Finding 1", "Finding 2"],
            "recommendations": [],
            "proof": {
                "transaction_hash": "0x1234567890abcdef",
                "settlement_mode": "BATCH_HASHED",
                "model": "GPT-5",
                "timestamp": "2026-04-09T20:52:00Z",
                "explorer_url": "https://sepolia.basescan.org/tx/0x1234567890abcdef"
            }
        }
        mock_client = AsyncMock()
        mock_client.analyze_protocol_risk.return_value = mock_ai_response
        mock_get_client.return_value = mock_client

        # Create pipeline instance
        pipeline = AuditPipeline()

        # Create audit request
        request = AuditRequest(
            protocol_address="0xE592427A0AEce92De3Edee1F18E0157C05861564",
            protocol_name="Uniswap V3",
            chain="ethereum",
            include_enhanced_data=True
        )

        # Execute analysis
        response = await pipeline.run_audit(request)

        # Assertions
        assert response.protocol == "Uniswap V3"
        assert response.risk_score == 24
        assert response.risk_level == RiskLevel.LOW
        assert response.confidence == 87
        assert "tvl_risk" in response.dimensions
        assert len(response.key_findings) == 2

        # Verify mocks were called
        mock_data_service.get_protocol_data.assert_called_once_with(
            address="0xE592427A0AEce92De3Edee1F18E0157C05861564",
            chain="ethereum"
        )
        mock_client.analyze_protocol_risk.assert_called_once_with(mock_protocol_data)

    def test_risk_level_calculation(self):
        """Test risk level calculation from score."""
        # Note: The pipeline currently uses risk_level from AI response
        # This test ensures RiskLevel enum works correctly
        assert RiskLevel.LOW.value == "LOW"
        assert RiskLevel.MEDIUM.value == "MEDIUM"
        assert RiskLevel.HIGH.value == "HIGH"

    @patch("app.services.audit_pipeline.get_protocol_data_service")
    async def test_protocol_suggestions(self, mock_get_data_service):
        """Test protocol suggestions."""
        mock_data_service = AsyncMock()
        mock_data_service.get_known_protocols.return_value = {
            "uniswap": "Uniswap V3",
            "aave": "Aave V3"
        }
        mock_get_data_service.return_value = mock_data_service

        pipeline = AuditPipeline()
        suggestions = await pipeline.get_protocol_suggestions()

        assert suggestions == {"uniswap": "Uniswap V3", "aave": "Aave V3"}
        mock_data_service.get_known_protocols.assert_called_once()


if __name__ == "__main__":
    import asyncio
    
    async def run_tests():
        test = TestAuditPipeline()
        await test.test_analyze_protocol_mock()
        test.test_risk_level_calculation()
        await test.test_protocol_suggestions()
        print("All tests passed!")

    asyncio.run(run_tests())