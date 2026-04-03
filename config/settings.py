"""Configuration with validation."""
import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    """App configuration for AI Job Assistant."""
    
    def __init__(self):
        # Try Streamlit secrets first (for cloud), fallback to .env (for local)
        try:
            import streamlit as st
            self.GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
        except Exception:
            self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
        
        self.MODEL_NAME = "gemini-2.5-pro"
        self.MAX_FILE_SIZE_MB = 10
        self.TEMPERATURE = 0.4
        self.MAX_OUTPUT_TOKENS = 3000

    def validate(self):
        """Validate configuration."""
        if not self.GEMINI_API_KEY:
            raise ValueError("❌ GEMINI_API_KEY not found. Add it to Streamlit secrets or .env file.")
        return True

settings = Settings()