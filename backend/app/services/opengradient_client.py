import asyncio
import os
import json
import re
from typing import Dict, Any, Optional
from datetime import datetime

# Try to import OpenGradient, but provide fallback if not available
try:
    import opengradient as og
    OPENGRADIENT_INSTALLED = True
except ImportError:
    OPENGRADIENT_INSTALLED = False
    og = None

from app.core.config import settings


class OpenGradientClient:
    """Client for OpenGradient TEE-verified inference with fallback support"""
    
    def __init__(self):
        self.private_key = settings.opengradient_private_key
        self.settlement_mode = self._get_settlement_mode(settings.opengradient_settlement_mode)
        self.model = self._get_model(settings.opengradient_model)
        
        # Initialize clients
        self.llm = None
        self.initialized = False
    
    def _get_settlement_mode(self, mode: str):
        """Convert string to OpenGradient settlement mode"""
        if not OPENGRADIENT_INSTALLED:
            return "BATCH_HASHED"
        
        mode_map = {
            "PRIVATE": og.x402SettlementMode.PRIVATE,
            "BATCH_HASHED": og.x402SettlementMode.BATCH_HASHED,
            "INDIVIDUAL_FULL": og.x402SettlementMode.INDIVIDUAL_FULL,
        }
        return mode_map.get(mode.upper(), og.x402SettlementMode.BATCH_HASHED)
    
    def _get_model(self, model_name: str):
        """Convert string to OpenGradient model"""
        if not OPENGRADIENT_INSTALLED:
            return "GPT_5"
        
        model_map = {
            "GPT_5": og.TEE_LLM.GPT_5,
            "GPT_5_MINI": og.TEE_LLM.GPT_5_MINI,
            "CLAUDE_SONNET_4_6": og.TEE_LLM.CLAUDE_SONNET_4_6,
            "CLAUDE_HAIKU_4_5": og.TEE_LLM.CLAUDE_HAIKU_4_5,
            "GEMINI_2_5_PRO": og.TEE_LLM.GEMINI_2_5_PRO,
            "GEMINI_3_PRO": og.TEE_LLM.GEMINI_3_PRO,
            "GROK_4": og.TEE_LLM.GROK_4,
        }
        return model_map.get(model_name, og.TEE_LLM.GPT_5)
    
    async def initialize(self):
        """Initialize OpenGradient clients"""
        if not OPENGRADIENT_INSTALLED:
            print("⚠️  OpenGradient not installed - running in simulation mode")
            self.initialized = True
            return
        
        if not self.private_key or self.private_key == "test_key_not_set":
            print("⚠️  OpenGradient private key not configured - running in simulation mode")
            self.initialized = True
            return
        
        try:
            self.llm = og.LLM(private_key=self.private_key)
            
            # Ensure OPG token approval
            await self.llm.ensure_opg_approval(min_allowance=5)
            
            self.initialized = True
            print(f"✓ OpenGradient initialized with model: {self.model.name}")
        except Exception as e:
            print(f"⚠️  OpenGradient initialization failed: {e}")
            print("  Running in simulation mode")
            self.initialized = True  # Mark as initialized but in simulation mode
    
    async def analyze_protocol_risk(self, protocol_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze DeFi protocol risk using TEE-verified LLM or simulation
        """
        if not self.initialized:
            await self.initialize()
        
        # If OpenGradient is not available or not properly configured, use simulation
        if not OPENGRADIENT_INSTALLED or not self.llm:
            return self._simulate_risk_analysis(protocol_data)
        
        try:
            # Construct analysis prompt
            prompt = self._construct_risk_analysis_prompt(protocol_data)
            
            # Execute TEE-verified inference
            completion = await self.llm.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                x402_settlement_mode=self.settlement_mode,
                temperature=0.1,  # Low temperature for consistent analysis
            )
            
            # Parse response
            analysis = self._parse_llm_response(completion.chat_output['content'])
            
            # Add proof information
            analysis["proof"] = {
                "transaction_hash": completion.transaction_hash,
                "settlement_mode": completion.x402_settlement_mode.name,
                "model": self.model.name,
                "timestamp": completion.timestamp,
                "explorer_url": f"https://sepolia.basescan.org/tx/{completion.transaction_hash}"
            }
            
            return analysis
            
        except Exception as e:
            print(f"⚠️  OpenGradient analysis failed: {e}")
            print("  Falling back to simulation mode")
            return self._simulate_risk_analysis(protocol_data)
    
    def _construct_risk_analysis_prompt(self, protocol_data: Dict[str, Any]) -> str:
        """Construct structured prompt for risk analysis"""
        
        return f"""
        Analyze the DeFi protocol risk based on the following data. Return a JSON response with exact structure:
        
        {{
          "risk_score": 0-100,
          "risk_level": "LOW"|"MEDIUM"|"HIGH"|"CRITICAL",
          "confidence": 0-100,
          "dimensions": {{
            "tvl_risk": "LOW"|"MEDIUM"|"HIGH"|"UNKNOWN",
            "approval_risk": "LOW"|"MEDIUM"|"HIGH"|"UNKNOWN",
            "code_risk": "LOW"|"MEDIUM"|"HIGH"|"UNKNOWN",
            "governance_risk": "LOW"|"MEDIUM"|"HIGH"|"UNKNOWN",
            "economic_risk": "LOW"|"MEDIUM"|"HIGH"|"UNKNOWN",
            "liquidity_risk": "LOW"|"MEDIUM"|"HIGH"|"UNKNOWN"
          }},
          "key_findings": ["finding1", "finding2", "finding3"],
          "recommendations": [
            {{
              "priority": "HIGH"|"MEDIUM"|"LOW",
              "title": "Recommendation title",
              "description": "Detailed description",
              "action_items": ["action1", "action2"]
            }}
          ]
        }}
        
        Protocol Data:
        - Name: {protocol_data.get('name', 'Unknown')}
        - Address: {protocol_data.get('address', 'N/A')}
        - Chain: {protocol_data.get('chain', 'ethereum')}
        - TVL: ${protocol_data.get('tvl', 0):,.0f}
        - TVL Concentration: {protocol_data.get('tvl_concentration', 'Unknown')}
        - Approval Patterns: {protocol_data.get('approval_patterns', 'Unknown')}
        - Code Audit Score: {protocol_data.get('code_audit_score', 'Unknown')}
        - Governance Activity: {protocol_data.get('governance_activity', 'Unknown')}
        - Economic Security: {protocol_data.get('economic_security', 'Unknown')}
        - Liquidity Depth: {protocol_data.get('liquidity_depth', 'Unknown')}
        - Age: {protocol_data.get('age_days', 'Unknown')} days
        
        Analysis Guidelines:
        1. Risk Score: 0-20 LOW, 21-40 MEDIUM, 41-60 HIGH, 61-100 CRITICAL
        2. Confidence: Based on data completeness and reliability
        3. Be conservative - assume worst-case when data is missing
        4. Focus on systemic risks and protocol sustainability
        5. Consider both technical and economic dimensions
        
        Return ONLY the JSON object, no additional text.
        """
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response into structured analysis"""
        # Extract JSON from response (handles potential markdown formatting)
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
        else:
            json_str = response
        
        try:
            analysis = json.loads(json_str)
        except json.JSONDecodeError:
            # Fallback to default analysis
            analysis = self._get_default_analysis()
        
        # Validate structure
        required_keys = ["risk_score", "risk_level", "confidence", "dimensions"]
        for key in required_keys:
            if key not in analysis:
                analysis = self._get_default_analysis()
                break
        
        return analysis
    
    def _simulate_risk_analysis(self, protocol_data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate risk analysis when OpenGradient is not available"""
        print("🔧 Running simulated risk analysis (OpenGradient not available)")
        
        # Simple simulation based on protocol data
        risk_score = 50  # Medium risk by default
        confidence = 70
        
        # Adjust based on TVL if available
        tvl = protocol_data.get('tvl', 0)
        if tvl > 1000000000:  # > $1B TVL
            risk_score = 30  # Lower risk for large protocols
        elif tvl < 1000000:  # < $1M TVL
            risk_score = 70  # Higher risk for small protocols
        
        risk_level = "LOW" if risk_score <= 20 else "MEDIUM" if risk_score <= 40 else "HIGH" if risk_score <= 60 else "CRITICAL"
        
        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "confidence": confidence,
            "dimensions": {
                "tvl_risk": "UNKNOWN",
                "approval_risk": "UNKNOWN",
                "code_risk": "UNKNOWN",
                "governance_risk": "UNKNOWN",
                "economic_risk": "UNKNOWN",
                "liquidity_risk": "UNKNOWN"
            },
            "key_findings": [
                "Analysis performed in simulation mode",
                "OpenGradient TEE-verification not available",
                f"Protocol: {protocol_data.get('name', 'Unknown')}"
            ],
            "recommendations": [
                {
                    "priority": "HIGH",
                    "title": "Enable OpenGradient TEE-verification",
                    "description": "Configure OPENGRADIENT_PRIVATE_KEY environment variable for real TEE-verified analysis",
                    "action_items": ["Set OPENGRADIENT_PRIVATE_KEY in environment variables", "Restart the application"]
                }
            ],
            "proof": {
                "transaction_hash": "0x" + "0" * 64,
                "settlement_mode": "SIMULATION",
                "model": "SIMULATION",
                "timestamp": datetime.utcnow().isoformat(),
                "explorer_url": None
            }
        }
    
    def _get_default_analysis(self) -> Dict[str, Any]:
        """Return default analysis when parsing fails"""
        return {
            "risk_score": 50,
            "risk_level": "MEDIUM",
            "confidence": 50,
            "dimensions": {
                "tvl_risk": "UNKNOWN",
                "approval_risk": "UNKNOWN",
                "code_risk": "UNKNOWN",
                "governance_risk": "UNKNOWN",
                "economic_risk": "UNKNOWN",
                "liquidity_risk": "UNKNOWN"
            },
            "key_findings": ["Insufficient data for comprehensive analysis"],
            "recommendations": [
                {
                    "priority": "HIGH",
                    "title": "Collect more protocol data",
                    "description": "Risk analysis is limited due to missing data points",
                    "action_items": ["Implement data collection from multiple sources"]
                }
            ]
        }


# Global client instance
_client: Optional[OpenGradientClient] = None


async def get_opengradient_client() -> OpenGradientClient:
    """Get or initialize OpenGradient client"""
    global _client
    if _client is None:
        _client = OpenGradientClient()
        await _client.initialize()
    return _client