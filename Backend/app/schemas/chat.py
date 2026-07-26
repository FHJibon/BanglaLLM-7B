from pydantic import BaseModel
from typing import Optional, List

class ChatMessage(BaseModel):
    role: str # 'user' or 'assistant' or 'system'
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []
    enable_rag: Optional[bool] = True
    enable_tools: Optional[bool] = True

class DocumentUploadResponse(BaseModel):
    filename: str
    status: str
    num_chunks: int
    message: str
