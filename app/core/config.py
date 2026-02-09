"""
Application configuration
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings"""
    
    # FastAPI
    APP_NAME = "Todo Backend API with Auth"
    APP_VERSION = "2.0.0"
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # Kafka Configuration
    KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "todos")
    
    # Dapr Configuration
    DAPR_HOST = os.getenv("DAPR_HOST", "localhost")
    DAPR_PORT = int(os.getenv("DAPR_PORT", "3500"))
    DAPR_PUBSUB_NAME = os.getenv("DAPR_PUBSUB_NAME", "kafka-pubsub")
    
    # JWT Configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production-environment-variable")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


settings = Settings()
