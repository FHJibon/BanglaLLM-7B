import os
from dotenv import load_dotenv
from huggingface_hub import HfApi

load_dotenv()

token = os.getenv("HUGGINGFACE_TOKEN")
repo_id = os.getenv("HF_REPO_ID", "FHJibon/BanglaLLM-7B")

local_model_path = os.path.join("Research", "models", "BanglaLLM-7B")
if not os.path.exists(local_model_path):
    local_model_path = "Research/models"

print(f"Uploading models from '{local_model_path}' to https://huggingface.co/{repo_id}...")
api = HfApi()
api.create_repo(repo_id=repo_id, exist_ok=True, token=token)
api.upload_folder(folder_path=local_model_path, repo_id=repo_id, token=token)
print("✓ Model uploaded successfully!")