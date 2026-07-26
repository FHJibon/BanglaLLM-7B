import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "BanglaSupport-LLM API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Storage & Model Paths (or HuggingFace Hub ID)
    HF_MODEL_ID: str = os.getenv("HF_MODEL_ID", "FHJibon/BanglaLLM-7B")
    GPU_MODEL_PATH: str = os.getenv("GPU_MODEL_PATH", "Research/models/BanglaLLM-7B")
    CPU_MODEL_PATH: str = os.getenv("CPU_MODEL_PATH", "Research/models/banglallm-7b-q4_k_m.gguf")
    DEVICE: str = os.getenv("DEVICE", "cpu")
    
    # Vector DB / RAG Settings
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    PINECONE_ENVIRONMENT: str = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "bangla-support-index")
    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    
    # CORS Origins
    CORS_ORIGINS: list[str] = ["*"]

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
