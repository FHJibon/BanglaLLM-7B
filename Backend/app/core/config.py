import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL_ID = os.getenv("HF_MODEL_ID")
GPU_MODEL_PATH = "Research/models/BanglaLLM-7B"
CPU_MODEL_PATH = "Research/models/banglallm-7b-q4_k_m.gguf"
DEVICE = os.getenv("DEVICE").lower()
USE_4BIT = os.getenv("USE_4BIT", "true").lower() in ("true", "1", "yes")

MAX_NEW_TOKENS = 1024
TEMPERATURE = 0.5
TOP_P = 0.9
N_CTX = 2048
N_THREADS = 4
