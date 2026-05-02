"""Application configuration management"""

from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Application
    app_name: str = Field(default="ProcessDoctor", description="Application name")
    debug: bool = Field(default=False, description="Debug mode")
    log_level: str = Field(default="INFO", description="Logging level")
    
    # Server
    backend_host: str = Field(default="0.0.0.0", description="Backend host")
    backend_port: int = Field(default=8000, description="Backend port")
    
    # CORS
    cors_origins: str = Field(
        default="http://localhost:5173,http://localhost:3000",
        description="Allowed CORS origins (comma-separated)"
    )
    
    # IBM Granite API
    granite_api_key: str = Field(..., description="IBM Granite API key")
    granite_api_url: str = Field(
        default="https://api.granite.ibm.com/v1",
        description="IBM Granite API URL"
    )
    granite_model: str = Field(
        default="granite-13b-chat-v2",
        description="Granite model to use"
    )
    
    # IBM Bob API
    bob_api_key: str = Field(..., description="IBM Bob API key")
    bob_api_url: str = Field(
        default="https://api.bob.ibm.com/v1",
        description="IBM Bob API URL"
    )
    
    # IBM watsonx Orchestrate
    watsonx_orchestrate_api_key: str = Field(..., description="watsonx Orchestrate API key")
    watsonx_orchestrate_url: str = Field(
        default="https://api.watsonx.ibm.com/orchestrate",
        description="watsonx Orchestrate URL"
    )
    
    # GitHub
    github_token: str = Field(..., description="GitHub personal access token")
    github_api_url: str = Field(
        default="https://api.github.com",
        description="GitHub API URL"
    )
    
    # Database (Optional)
    database_url: Optional[str] = Field(
        default=None,
        description="PostgreSQL database URL"
    )
    
    # Redis (Optional)
    redis_url: Optional[str] = Field(
        default=None,
        description="Redis connection URL"
    )
    
    # Security
    secret_key: str = Field(
        default="change-this-in-production",
        description="Secret key for JWT tokens"
    )
    access_token_expire_minutes: int = Field(
        default=30,
        description="Access token expiration time in minutes"
    )
    
    # Rate Limiting
    rate_limit_per_minute: int = Field(
        default=60,
        description="API rate limit per minute"
    )
    
    # Timeouts
    llm_timeout: int = Field(default=120, description="LLM API timeout in seconds")
    github_timeout: int = Field(default=30, description="GitHub API timeout in seconds")
    
    # Processing
    max_workflow_size: int = Field(
        default=1000000,
        description="Maximum workflow file size in bytes"
    )
    max_concurrent_analyses: int = Field(
        default=10,
        description="Maximum concurrent workflow analyses"
    )
    
    @property
    def cors_origins_list(self) -> list[str]:
        """Get CORS origins as a list"""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return not self.debug


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Global settings instance
settings = get_settings()

# Made with Bob
