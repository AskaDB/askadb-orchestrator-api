from fastapi import FastAPI
from app.routers import query

app = FastAPI(title="AskaDB Orchestrator API")

app.include_router(query.router)
