import os

# Flask secret key for session management
SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")

# Database URI (use SQLite for local dev, PostgreSQL for production)
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///mindmate.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Gemini API Key (for chatbot responses)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "your-gemini-api-key")

# Optional: Debug mode
DEBUG = os.environ.get("FLASK_DEBUG", "True") == "True"

# Optional: Other configuration values
# Example: Maximum chat message length
MAX_CHAT_LENGTH = int(os.environ.get("MAX_CHAT_LENGTH", 1000))

# Example: Allowed origins for CORS (comma-separated)
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "*").split(",")

# Example: Static resource cache timeout
SEND_FILE_MAX_AGE_DEFAULT = 180  # seconds

# Add other app-specific config variables below as needed
