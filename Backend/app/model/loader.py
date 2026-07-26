import os
import sys
from typing import Generator, List
from Backend.app.core.config import settings

class ModelLoader:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.mode = "mock" # 'gpu', 'cpu', 'hf', or 'mock'
        self._init_model()

    def _init_model(self):
        # 1. Try Local GPU Safetensors or Hugging Face Hub Model ID
        target_model = settings.GPU_MODEL_PATH if os.path.exists(settings.GPU_MODEL_PATH) else settings.HF_MODEL_ID
        if settings.DEVICE.lower() == "cuda":
            try:
                from transformers import AutoModelForCausalLM, AutoTokenizer
                import torch
                print(f"Loading model from {target_model}...")
                self.tokenizer = AutoTokenizer.from_pretrained(target_model)
                self.model = AutoModelForCausalLM.from_pretrained(
                    target_model,
                    torch_dtype=torch.bfloat16,
                    device_map="auto"
                )
                self.mode = "gpu"
                return
            except Exception as e:
                print(f"GPU model load failed: {e}. Falling back to CPU GGUF.")

        # 2. Try CPU GGUF
        if os.path.exists(settings.CPU_MODEL_PATH):
            try:
                from llama_cpp import Llama
                print(f"Loading CPU GGUF model from {settings.CPU_MODEL_PATH}...")
                self.model = Llama(
                    model_path=settings.CPU_MODEL_PATH,
                    n_ctx=2048,
                    n_threads=4,
                    verbose=False
                )
                self.mode = "cpu"
                return
            except Exception as e:
                print(f"CPU GGUF model load failed: {e}. Falling back to rule-based fallback.")

        # 3. Fallback mock engine
        print("Using rule-based response generator engine.")
        self.mode = "mock"

    def generate_stream(self, prompt: str, system_context: str = "") -> Generator[str, None, None]:
        full_prompt = f"System: {system_context}\nUser: {prompt}\nAssistant:" if system_context else f"User: {prompt}\nAssistant:"

        if self.mode == "gpu":
            inputs = self.tokenizer(full_prompt, return_tensors="pt").to("cuda")
            outputs = self.model.generate(**inputs, max_new_tokens=512, do_sample=True, temperature=0.7)
            response = self.tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
            for word in response.split(" "):
                yield word + " "
                
        elif self.mode == "cpu":
            stream = self.model(
                full_prompt,
                max_tokens=512,
                stop=["User:", "\n\n"],
                stream=True
            )
            for chunk in stream:
                token = chunk["choices"][0]["text"]
                yield token
                
        else:
            # Smart Mock Bangla Support Generator
            if "BD1001" in prompt:
                resp = "আপনার অর্ডার BD1001 বর্তমানে ট্রানজিটে রয়েছে। ডেলিভারির আনুমানিক সময় ২১শে জুলাই ২০২৬।"
            elif "রিটার্ন" in prompt or "ফেরত" in prompt:
                resp = "পণ্য গ্রহণের ৭ দিনের মধ্যে ডেলিভারি রসিদসহ রিটার্ন রিকোয়েস্ট জমা দিতে হবে। পণ্য অব্যবহৃত ও অক্ষত অবস্থায় থাকা আবশ্যক।"
            elif "ডেলিভারি চার্জ" in prompt or "শিপিং" in prompt:
                resp = "ঢাকার মধ্যে ডেলিভারি চার্জ ৬০ টাকা এবং ঢাকার বাইরে ১৩০ টাকা। ডেলিভারি সময় ৩-৫ কর্মদিবস।"
            elif "পেমেন্ট" in prompt or "বিকাশ" in prompt or "ক্যাশ" in prompt:
                resp = "আমরা ক্যাশ অন ডেলিভারি (COD), বিকাশ, নগদ এবং সকল প্রধান ব্যাংক কার্ড পেমেন্ট গ্রহণ করি।"
            else:
                resp = f"ধন্যবাদ আপনার বার্তার জন্য। BanglaSupport-LLM সিস্টেমে আপনার প্রশ্নটি গৃহীত হয়েছে: '{prompt}'। আমাদের টিম শীঘ্রই সাহায্য করবে।"

            words = resp.split(" ")
            import time
            for word in words:
                time.sleep(0.05)
                yield word + " "

model_loader = ModelLoader()
