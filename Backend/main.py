import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from Backend.app.api.endpoints.chat import router as chat_router

app = FastAPI(title="Bangla LLM")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api")

if os.path.exists("Frontend"):
    app.mount("/", StaticFiles(directory="Frontend", html=True), name="frontend")
