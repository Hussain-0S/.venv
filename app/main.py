import os
from dotenv import load_dotenv
from fastapi.responses import FileResponse
from pathlib import Path

load_dotenv()

from fastapi import FastAPI,status
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users,items, uploads

app = FastAPI()

@app.get("/", include_in_schema=False)
def frontend():
    return FileResponse(
        Path(__file__).parent / "frontend" / "index.html"
    )


allowed_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "auth", "Authorization"],
)

app.include_router(users.router)
app.include_router(items.router)
app.include_router(uploads.router)