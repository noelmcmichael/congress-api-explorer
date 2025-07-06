"""
Configuration management for Congress API Explorer.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Congress API Configuration
    congress_api_key: str = Field(..., env="CONGRESS_API_KEY")
    congress_api_base_url: str = Field(
        default="https://api.congress.gov/v3",
        env="CONGRESS_API_BASE_URL"
    )
    
    # Cache Configuration
    cache_type: str = Field(default="memory", env="CACHE_TYPE")
    cache_ttl_default: int = Field(default=3600, env="CACHE_TTL_DEFAULT")
    cache_ttl_committee: int = Field(default=86400, env="CACHE_TTL_COMMITTEE")
    cache_ttl_hearing: int = Field(default=21600, env="CACHE_TTL_HEARING")
    cache_ttl_bill: int = Field(default=7200, env="CACHE_TTL_BILL")
    cache_ttl_member: int = Field(default=604800, env="CACHE_TTL_MEMBER")
    
    # Redis Configuration
    redis_host: str = Field(default="localhost", env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")
    redis_db: int = Field(default=0, env="REDIS_DB")
    redis_password: Optional[str] = Field(default=None, env="REDIS_PASSWORD")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )
    
    # MCP Server Configuration
    mcp_server_port: int = Field(default=8000, env="MCP_SERVER_PORT")
    mcp_server_host: str = Field(default="localhost", env="MCP_SERVER_HOST")
    
    # Rate Limiting Configuration
    rate_limit_requests_per_hour: int = Field(default=4500, env="RATE_LIMIT_REQUESTS_PER_HOUR")
    rate_limit_requests_per_minute: int = Field(default=75, env="RATE_LIMIT_REQUESTS_PER_MINUTE")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()


def get_cache_ttl(cache_type: str) -> int:
    """Get appropriate cache TTL based on data type."""
    ttl_map = {
        "committee": settings.cache_ttl_committee,
        "hearing": settings.cache_ttl_hearing,
        "bill": settings.cache_ttl_bill,
        "member": settings.cache_ttl_member,
    }
    return ttl_map.get(cache_type, settings.cache_ttl_default)