import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "Hamza@123")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "Hamza@935106")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "mysql+pymysql://root:Hamzaanas%40123@localhost/ai_physio_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # To suppress a warning
    COHERE_API_KEY = os.getenv("COHERE_API_KEY", "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")
    BIOBERT_MODEL_PATH = os.getenv("BIOBERT_MODEL_PATH", "models/biobert")
