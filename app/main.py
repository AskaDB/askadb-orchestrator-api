from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import query

app = FastAPI(title="AskaDB Orchestrator API")

# Enable CORS for local development and dockerized UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query.router)
