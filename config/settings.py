"""Configuration with validation."""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """App configuration for AI Job Assistant."""
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    MODEL_NAME = "gemini-2.0-flash-exp"
    MAX_FILE_SIZE_MB = 10
    TEMPERATURE = 0.4
    MAX_OUTPUT_TOKENS = 3000
    
    @classmethod
    def validate(cls):
        """Validate configuration."""
        if not cls.GEMINI_API_KEY:
            raise ValueError("❌ GEMINI_API_KEY not found. Add it to .env file.")
        return True

settings = Settings()
