import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL_ID = os.getenv("HF_MODEL_ID")
DEVICE = os.getenv("DEVICE").lower()

MAX_NEW_TOKENS = 1024
TEMPERATURE = 0.5
TOP_P = 0.9
N_CTX = 2048
N_THREADS = 4