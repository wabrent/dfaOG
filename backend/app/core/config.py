from pydantic_settings import BaseSettings
from typing import List, Optional, Union
import json
import os


class Settings(BaseSettings):
    # OpenGradient Configuration
    opengradient_private_key: str = "test_key_not_set"
    opengradient_settlement_mode: str = "BATCH_HASHED"
    opengradient_model: str = "GPT_5"
    
    # API Keys (Optional)
    defillama_api_key: Optional[str] = None
    etherscan_api_key: Optional[str] = None
    alchemy_api_key: Optional[str] = None
    
    # Backend Configuration
    redis_url: str = "redis://localhost:6379"
    cache_ttl: int = 300
    rate_limit_requests: int = 100
    rate_limit_period: int = 3600
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    cors_origins_raw: Union[str, List[str]] = '["http://localhost:3000"]'
    
    # Security
    api_key: Optional[str] = None
    jwt_secret: Optional[str] = None
    
    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS origins from string or list."""
        if isinstance(self.cors_origins_raw, list):
            return self.cors_origins_raw
        try:
            return json.loads(self.cors_origins_raw)
        except (json.JSONDecodeError, TypeError):
            return ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()