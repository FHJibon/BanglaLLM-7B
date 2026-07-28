from typing import Generator
from huggingface_hub import InferenceClient
from Backend.app.core import config

class ModelLoader:
    def __init__(self):
        self.client = InferenceClient(token=config.HF_TOKEN or None)

    def generate_stream(self, prompt: str, system_context: str = "") -> Generator[str, None, None]:
        messages = [{"role": "system", "content": system_context}] if system_context else []
        messages.append({"role": "user", "content": prompt})

        try:
            stream = self.client.chat_completion(
                messages=messages,
                model=config.HF_MODEL_ID,
                max_tokens=config.MAX_NEW_TOKENS,
                temperature=config.TEMPERATURE,
                top_p=config.TOP_P,
                stream=True
            )
            for chunk in stream:
                content = chunk.choices[0].delta.content if chunk.choices else None
                if content:
                    yield content
        except Exception as e:
            yield f"Hugging Face Cloud API Error: {e}"

model_loader = ModelLoader()