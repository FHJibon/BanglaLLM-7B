import os
from dotenv import load_dotenv, find_dotenv
from huggingface_hub import HfApi

load_dotenv(find_dotenv())
token, repo_id = os.getenv("HUGGINGFACE_TOKEN"), os.getenv("HF_REPO_ID", "FHJibon/BanglaLLM-7B")
model_path = "Research/models/BanglaLLM-7B" if os.path.exists("Research/models/BanglaLLM-7B") else "Research/models"

print(f"Uploading '{model_path}' to https://huggingface.co/{repo_id}...")
api = HfApi()
api.create_repo(repo_id=repo_id, exist_ok=True, token=token)
api.upload_folder(folder_path=model_path, repo_id=repo_id, token=token)
print("✓ Upload completed!")