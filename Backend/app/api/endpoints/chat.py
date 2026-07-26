import json
import asyncio
from fastapi import APIRouter, Request
from sse_starlette.sse import EventSourceResponse
from Backend.app.schemas.chat import ChatRequest
from Backend.app.services.pinecone_rag import rag_service
from Backend.app.model.loader import model_loader

router = APIRouter()

# Mock Order Database for SQLite Agentic Tool Calling
MOCK_ORDERS = {
    "BD1001": {"status": "In Transit", "location": "Dhaka Hub", "delivery_date": "2026-07-28"},
    "BD1002": {"status": "Delivered", "location": "Chittagong", "delivery_date": "2026-07-20"},
    "BD1003": {"status": "Processing", "location": "Warehouse", "delivery_date": "2026-07-30"}
}

def check_order_tool(query: str) -> str:
    """Agentic Tool: Extracts order ID and checks status."""
    import re
    match = re.search(r'BD\d{4}', query.upper())
    if match:
        order_id = match.group(0)
        if order_id in MOCK_ORDERS:
            info = MOCK_ORDERS[order_id]
            return f"[Tool Action Executed]: Order {order_id} is '{info['status']}' at '{info['location']}'. Expected Delivery: {info['delivery_date']}."
        else:
            return f"[Tool Action Executed]: Order {order_id} was not found in the order database."
    return ""

@router.post("/chat/stream")
async def chat_stream(request_data: ChatRequest):
    user_query = request_data.message
    system_parts = ["You are BanglaSupport-LLM, an intelligent e-commerce customer support assistant."]
    
    # 1. Check Tool Calling
    if request_data.enable_tools:
        tool_output = check_order_tool(user_query)
        if tool_output:
            system_parts.append(f"Tool Context: {tool_output}")

    # 2. Check RAG Retrieval
    if request_data.enable_rag:
        rag_context = rag_service.retrieve(user_query, top_k=2)
        if rag_context:
            system_parts.append("Policy Context:\n" + "\n".join(rag_context))

    system_prompt = "\n".join(system_parts)

    async def event_generator():
        for chunk in model_loader.generate_stream(user_query, system_context=system_prompt):
            yield {
                "event": "message",
                "data": json.dumps({"token": chunk})
            }
            await asyncio.sleep(0.01)
        yield {
            "event": "done",
            "data": json.dumps({"status": "completed"})
        }

    return EventSourceResponse(event_generator())
