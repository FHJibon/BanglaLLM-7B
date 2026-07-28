from typing import Generator
from huggingface_hub import InferenceClient
from Backend.app.core import config as settings

class ModelLoader:
    def __init__(self):
        self.client = InferenceClient(token=settings.HF_TOKEN if settings.HF_TOKEN else None)

    def generate_stream(self, prompt: str, system_context: str = "") -> Generator[str, None, None]:
        messages = []
        if system_context:
            messages.append({"role": "system", "content": system_context})
        messages.append({"role": "user", "content": prompt})

        try:
            stream = self.client.chat_completion(
                messages=messages,
                model=settings.HF_MODEL_ID,
                max_tokens=settings.MAX_NEW_TOKENS,
                temperature=settings.TEMPERATURE,
                top_p=settings.TOP_P,
                stream=True
            )

            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"Hugging Face Cloud API Error: {e}"

model_loader = ModelLoader()
