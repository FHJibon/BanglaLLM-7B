import json
import asyncio
from Backend.app.services.loader import model_loader

DEFAULT_SYSTEM_PROMPT = "তুমি একজন অত্যন্ত দক্ষ ও সহায়ক বাংলা কৃত্রিম বুদ্ধিমত্তা সহকারী (Bangla AI Assistant)। যেকোনো প্রশ্নের উত্তর স্পষ্ট ও নির্ভুলভাবে বাংলায় দাও।"

async def generate_chat_response(message: str, system_context: str = DEFAULT_SYSTEM_PROMPT):
    for chunk in model_loader.generate_stream(message, system_context=system_context):
        yield {"event": "message", "data": json.dumps({"token": chunk})}
        await asyncio.sleep(0.005)
    yield {"event": "done", "data": json.dumps({"status": "completed"})}
