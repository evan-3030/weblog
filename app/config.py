import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-string")
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    JWT_REFRESH_TOKEN_EXPIRES = 86400

    ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL")