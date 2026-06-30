"""
Configuration module for the Risk Assessment Engine.
Loads settings from environment variables.
IMPORTANT: All sensitive settings must be defined in .env file.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_required_env(key: str) -> str:
    """
    Get required environment variable or raise error if not found.
    
    Args:
        key: Environment variable name
        
    Returns:
        Environment variable value
        
    Raises:
        ValueError: If environment variable is not set
    """
    value = os.getenv(key)
    if value is None:
        raise ValueError(
            f"Required environment variable '{key}' is not set. "
            f"Please add it to your .env file."
        )
    return value


class Settings:
    """Application settings."""

    # Database Configuration (REQUIRED - No fallback for security)
    DATABASE_URL: str = get_required_env("DATABASE_URL")

    # Ollama Configuration
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")
    OLLAMA_TEMPERATURE: float = float(os.getenv("OLLAMA_TEMPERATURE", "0.01"))
    OLLAMA_TOP_P: float = float(os.getenv("OLLAMA_TOP_P", "0.9"))
    OLLAMA_TIMEOUT: int = int(os.getenv("OLLAMA_TIMEOUT", "600"))

    # FastAPI Configuration
    API_HOST: str = os.getenv("API_HOST", "127.0.0.1")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_RELOAD: bool = os.getenv("API_RELOAD", "true").lower() == "true"
    API_LOG_LEVEL: str = os.getenv("API_LOG_LEVEL", "info")

    # Application Info
    APP_NAME: str = "Insurance Risk Assessment Engine"
    APP_VERSION: str = "0.2.0"
    APP_DESCRIPTION: str = "AI-Assisted Insurance Underwriting using Ollama"


# Create global settings instance
# This will raise an error immediately if required env vars are missing
settings = Settings()
