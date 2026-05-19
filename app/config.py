import os
<<<<<<< HEAD
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-string")
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    JWT_REFRESH_TOKEN_EXPIRES = 86400

    ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL")
=======




class Config:
    JWT_SECRET_KEY = "super-secret-key" 
    JWT_SECRET_KEY = "jwt-secret"
    JWT_SECRET_KEY = "super-secret-key"
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    JWT_REFRESH_TOKEN_EXPIRES = 86400

    ELASTIC_HOST = os.getenv("ELASTIC_HOST")  
    ELASTIC_INDEX_USERS = os.getenv("ELASTIC_INDEX_USERS")
    ELASTIC_INDEX_POSTS = os.getenv("ELASTIC_INDEX_POSTS")
    ELASTIC_INDEX_category = os.getenv("ELASTIC_INDEX_category")
    ELASTIC_INDEX_TAGS  = os.getenv("ELASTIC_INDEX_TAGS","tags")




#   ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL")
>>>>>>> 95a2f5c (add category evan)
