import os
from dotenv import load_dotenv

# Load environment variables safely
try:
    load_dotenv()
except (UnicodeDecodeError, FileNotFoundError) as e:
    print(f"Warning: Could not load .env file: {e}")
    print("Please create a proper .env file with UTF-8 encoding")

class Config:
    # Groq Configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # Model Configuration
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Sentence transformer model
    LLM_MODEL = "llama3-8b-8192"  # Groq model
    
    # Chunking Configuration
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # Vector Store Configuration
    VECTOR_DB_PATH = "./chroma_db"
    COLLECTION_NAME = "documents"
    
    # File Upload Configuration
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = ['.pdf', '.docx', '.doc']
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        if not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY environment variable is required")
        return True 