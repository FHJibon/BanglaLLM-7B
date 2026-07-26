import os
import sys
from huggingface_hub import HfApi

def push_models_to_hub(repo_id: str, local_dir: str = "Research/models"):
    token = os.getenv("HUGGINGFACE_TOKEN")
    api = HfApi()
    print(f"Creating or verifying repo: {repo_id}...")
    api.create_repo(repo_id=repo_id, exist_ok=True, private=False)
    print(f"Uploading files from {local_dir} to {repo_id}...")
    api.upload_folder(
        folder_path=local_dir,
        repo_id=repo_id,
        repo_type="model",
        token=token
    )
    print("✓ Model push completed successfully!")

if __name__ == "__main__":
    target_repo = os.getenv("HF_REPO_ID", "FHJibon/BanglaLLM-7B")
    push_models_to_hub(target_repo)