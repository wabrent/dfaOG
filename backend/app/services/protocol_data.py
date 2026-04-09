import httpx
from typing import Dict, Any, Optional
import asyncio
from app.core.config import settings


class ProtocolDataService:
    """Service to collect protocol data from various sources"""
    
    def __init__(self):
        self.defillama_api_key = settings.defillama_api_key
        self.etherscan_api_key = settings.etherscan_api_key
        self.alchemy_api_key = settings.alchemy_api_key
        
        # Known protocol addresses
        self.known_protocols = {
            "uniswap_v3": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
            "aave_v3": "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2",
            "compound_v3": "0xc3d688B66703497DAA19211EEdff47f25384cdc3",
            "makerdao": "0x9ef05f7f6deb616fd37ac3c959a2ddd25a54e4f5",
            "lido": "0xae7ab96520de3a18e5e111b5eaab095312d7fe84",
            "curve": "0x90e00ace148ca3b23ac1bc8c240c2a7dd9c2d7f5",
            "balancer": "0xba12222222228d8ba445958a75a0704d566bf2c8",
        }
    
    async def get_protocol_data(self, address: str, chain: str = "ethereum") -> Dict[str, Any]:
        """
        Collect protocol data from various sources
        
        Args:
            address: Smart contract address
            chain: Blockchain network
        
        Returns:
            Dictionary with protocol data
        """
        # Basic protocol info
        protocol_data = {
            "address": address,
            "chain": chain,
            "name": self._identify_protocol(address),
            "tvl": 0,
            "tvl_concentration": "Unknown",
            "approval_patterns": "Unknown",
            "code_audit_score": "Unknown",
            "governance_activity": "Unknown",
            "economic_security": "Unknown",
            "liquidity_depth": "Unknown",
            "age_days": 0,
        }
        
        # Enhanced data collection if API keys are available
        if self.defillama_api_key:
            tvl_data = await self._get_tvl_data(address, chain)
            protocol_data.update(tvl_data)
        
        if self.etherscan_api_key:
            contract_data = await self._get_contract_data(address, chain)
            protocol_data.update(contract_data)
        
        return protocol_data
    
    def _identify_protocol(self, address: str) -> str:
        """Identify protocol by address"""
        address_lower = address.lower()
        for name, known_address in self.known_protocols.items():
            if known_address.lower() == address_lower:
                return name.replace("_", " ").title()
        
        # Try to match by partial address
        for name, known_address in self.known_protocols.items():
            if address_lower.startswith(known_address.lower()[:10]):
                return f"{name.replace('_', ' ').title()} (Related)"
        
        return "Unknown Protocol"
    
    async def _get_tvl_data(self, address: str, chain: str) -> Dict[str, Any]:
        """Get TVL data from DeFiLlama"""
        try:
            async with httpx.AsyncClient() as client:
                # This is a simplified example - actual DeFiLlama API may differ
                response = await client.get(
                    f"https://api.llama.fi/protocol/{address}",
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "tvl": data.get("tvl", 0),
                        "tvl_concentration": self._assess_tvl_concentration(data),
                        "chain_tvls": data.get("chainTvls", {}),
                    }
        except Exception:
            pass
        
        return {"tvl": 0, "tvl_concentration": "Unknown"}
    
    def _assess_tvl_concentration(self, data: Dict[str, Any]) -> str:
        """Assess TVL concentration risk"""
        tvl = data.get("tvl", 0)
        if tvl == 0:
            return "Unknown"
        
        # Simplified logic - in reality would analyze pool distribution
        if tvl > 1000000000:  # > $1B
            return "LOW"  # Large, likely diversified
        elif tvl > 100000000:  # > $100M
            return "MEDIUM"
        else:
            return "HIGH"  # Small TVL = higher concentration risk
    
    async def _get_contract_data(self, address: str, chain: str) -> Dict[str, Any]:
        """Get contract data from Etherscan"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://api.etherscan.io/api",
                    params={
                        "module": "contract",
                        "action": "getsourcecode",
                        "address": address,
                        "apikey": self.etherscan_api_key
                    },
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") == "1":
                        contract_info = data.get("result", [{}])[0]
                        return {
                            "contract_verified": contract_info.get("SourceCode") != "",
                            "compiler_version": contract_info.get("CompilerVersion", "Unknown"),
                            "optimization_used": contract_info.get("OptimizationUsed", "Unknown"),
                        }
        except Exception:
            pass
        
        return {"contract_verified": False}
    
    def get_known_protocols(self) -> Dict[str, str]:
        """Get list of known protocols for UI dropdown"""
        return {
            name.replace("_", " ").title(): address
            for name, address in self.known_protocols.items()
        }


# Global service instance
protocol_data_service: Optional[ProtocolDataService] = None


async def get_protocol_data_service() -> ProtocolDataService:
    """Get or initialize protocol data service"""
    global protocol_data_service
    if protocol_data_service is None:
        protocol_data_service = ProtocolDataService()
    return protocol_data_service