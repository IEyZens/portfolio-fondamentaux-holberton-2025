import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Dynamic configuration loaded from environment variables."""
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt_dev_secret")
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    PORT = int(os.getenv("FLASK_RUN_PORT", 5000))
    HOST = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
    JWT_ACCESS_TOKEN_EXPIRES = 3600
