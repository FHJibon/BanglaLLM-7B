import json
import asyncio
from Backend.app.services.loader import model_loader

SYSTEM_PROMPT = "তুমি একজন স্বাভাবিক ও বন্ধুত্বপূর্ণ বাংলা এআই সহকারী। সব প্রশ্নের উত্তর সহজ বাংলায় দাও।"

async def generate_chat_response(message: str, system_context: str = SYSTEM_PROMPT):
    for chunk in model_loader.generate_stream(message, system_context):
        yield {"event": "message", "data": json.dumps({"token": chunk})}
        await asyncio.sleep(0.2)
    yield {"event": "done", "data": json.dumps({"status": "completed"})}