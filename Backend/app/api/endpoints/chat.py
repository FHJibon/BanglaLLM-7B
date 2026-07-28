from fastapi import APIRouter
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
from Backend.app.services.chat import generate_chat_response

class ChatRequest(BaseModel):
    message: str

router = APIRouter()

@router.post("/chat")
async def chat_stream(req: ChatRequest):
    return EventSourceResponse(generate_chat_response(req.message))
