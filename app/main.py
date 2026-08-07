from fastapi import FastAPI,status
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users,items, uploads

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(items.router)
app.include_router(uploads.router)