"""
Core configuration settings for Jane Orchestrator.

Constitutional Requirements:
- Secure JWT configuration for unified authentication
- Executive function platform settings
- Development and production environment support
"""

import os


class Settings:
    """Application configuration settings."""

    # JWT Configuration
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "jane-executive-function-secret-change-in-production"
    )

    # Database Configuration
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://jane:jane@localhost:5432/jane_db"
    )

    # Application Configuration
    APP_NAME: str = "Jane Executive Function Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

    # CORS Configuration
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",  # React development server
        "http://localhost:4200",  # Alternative frontend port
        "http://127.0.0.1:3000",
        "http://127.0.0.1:4200"
    ]

    # Executive Function Platform Configuration
    TOTAL_TOOLS: int = 37
    TOTAL_DOMAINS: int = 4

    # Domain Performance Requirements (Constitutional)
    DOMAIN_PERFORMANCE_LIMITS: dict = {
        "security": 1000,      # <1s response time
        "productivity": 2000,  # <2s response time
        "mtg": 3000,          # <3s response time
        "infrastructure": 5000  # <5s response time
    }

    # Executive Function Accommodations
    ADHD_UI_RESPONSE_LIMIT_MS: int = 200  # <200ms for ADHD support
    AUTISM_SENSORY_REDUCTION: bool = True
    COGNITIVE_LOAD_ASSESSMENT: bool = True

    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Security Configuration
    BCRYPT_ROUNDS: int = 12
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Feature Flags
    ENABLE_WEBSOCKETS: bool = True
    ENABLE_METRICS: bool = True
    ENABLE_HEALTH_CHECKS: bool = True


# Global settings instance
settings = Settings()
