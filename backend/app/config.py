import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    CORS_ORIGINS: List[str] = ["*"]
    
    # Database
    DATABASE_URL: str = "sqlite:///./pathway_ai.db"
    
    # JWT
    JWT_SECRET: str = "supersecretjwtkey_pathwayai_replace_in_production_2026_xyz"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Pricing
    REPORT_PRICE_INR: float = 99.0
    PREMIUM_PRICE_INR: float = 999.0
    
    # Razorpay
    RAZORPAY_KEY_ID: str = "rzp_test_placeholder_key_id"
    RAZORPAY_KEY_SECRET: str = "rzp_test_placeholder_secret_key"
    
    # Admin defaults
    DEFAULT_ADMIN_EMAIL: str = "admin@pathway.ai"
    DEFAULT_ADMIN_PASSWORD: str = "Admin@12345"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
