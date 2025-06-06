import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration settings for the AI agent system"""

    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

    # File paths
    PDF_PATH = os.getenv('PDF_PATH', 'resume.pdf')
    TXT_PATH = os.getenv('TXT_PATH', 'personal_info.txt')

    # AI Model settings
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')

    # Response settings
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', '500'))
    TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
    LINKEDIN_THRESHOLD = int(os.getenv('LINKEDIN_THRESHOLD', '8'))

    # Gradio settings
    SERVER_NAME = os.getenv('SERVER_NAME', '0.0.0.0')
    SERVER_PORT = int(os.getenv('SERVER_PORT', '8080'))

    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        required_vars = ['OPENAI_API_KEY', 'GEMINI_API_KEY']
        missing_vars = []

        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)

        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

        # Check if files exist
        if not os.path.exists(cls.PDF_PATH):
            raise FileNotFoundError(f"Resume PDF not found: {cls.PDF_PATH}")

        if not os.path.exists(cls.TXT_PATH):
            raise FileNotFoundError(f"Personal info file not found: {cls.TXT_PATH}")

        return True