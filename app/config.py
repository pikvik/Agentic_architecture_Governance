"""
Configuration management for the Agentic AI Swarm
"""

from typing import Optional
from pydantic import BaseSettings, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Dify Platform Configuration
    dify_api_key: str = Field(..., env="DIFY_API_KEY")
    dify_base_url: str = Field("https://api.dify.ai/v1", env="DIFY_BASE_URL")
    
    # LLM Provider API Keys
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(None, env="ANTHROPIC_API_KEY")
    
    # Database Configuration
    database_url: str = Field("sqlite:///./architecture_governance.db", env="DATABASE_URL")
    redis_url: str = Field("redis://localhost:6379/0", env="REDIS_URL")
    mongodb_url: str = Field("mongodb://localhost:27017/architecture_governance", env="MONGODB_URL")
    
    # Cloud Provider Credentials
    aws_access_key_id: Optional[str] = Field(None, env="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: Optional[str] = Field(None, env="AWS_SECRET_ACCESS_KEY")
    aws_region: str = Field("us-east-1", env="AWS_REGION")
    
    azure_client_id: Optional[str] = Field(None, env="AZURE_CLIENT_ID")
    azure_client_secret: Optional[str] = Field(None, env="AZURE_CLIENT_SECRET")
    azure_tenant_id: Optional[str] = Field(None, env="AZURE_TENANT_ID")
    azure_subscription_id: Optional[str] = Field(None, env="AZURE_SUBSCRIPTION_ID")
    
    google_cloud_project: Optional[str] = Field(None, env="GOOGLE_CLOUD_PROJECT")
    google_application_credentials: Optional[str] = Field(None, env="GOOGLE_APPLICATION_CREDENTIALS")
    
    # Security Configuration
    secret_key: str = Field(..., env="SECRET_KEY")
    jwt_secret_key: str = Field(..., env="JWT_SECRET_KEY")
    encryption_key: str = Field(..., env="ENCRYPTION_KEY")
    
    # External Service APIs
    github_token: Optional[str] = Field(None, env="GITHUB_TOKEN")
    gitlab_token: Optional[str] = Field(None, env="GITLAB_TOKEN")
    azure_devops_token: Optional[str] = Field(None, env="AZURE_DEVOPS_TOKEN")
    
    # Security Tools
    qualys_api_key: Optional[str] = Field(None, env="QUALYS_API_KEY")
    snyk_token: Optional[str] = Field(None, env="SNYK_TOKEN")
    prisma_cloud_token: Optional[str] = Field(None, env="PRISMA_CLOUD_TOKEN")
    
    # Application Configuration
    debug: bool = Field(False, env="DEBUG")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    environment: str = Field("development", env="ENVIRONMENT")
    port: int = Field(8000, env="PORT")
    host: str = Field("0.0.0.0", env="HOST")
    
    # Performance Configuration
    max_concurrent_agents: int = Field(50, env="MAX_CONCURRENT_AGENTS")
    agent_timeout: int = Field(300, env="AGENT_TIMEOUT")
    batch_size: int = Field(10, env="BATCH_SIZE")
    
    # Monitoring
    sentry_dsn: Optional[str] = Field(None, env="SENTRY_DSN")
    prometheus_port: int = Field(9090, env="PROMETHEUS_PORT")
    
    # Email Configuration
    smtp_host: Optional[str] = Field(None, env="SMTP_HOST")
    smtp_port: int = Field(587, env="SMTP_PORT")
    smtp_username: Optional[str] = Field(None, env="SMTP_USERNAME")
    smtp_password: Optional[str] = Field(None, env="SMTP_PASSWORD")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
