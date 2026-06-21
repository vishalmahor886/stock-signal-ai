from fastapi import FastAPI
from backend.api.routers.signal_api import router as signal_router

app = FastAPI()

app.include_router(signal_router, prefix="/api/signals", tags=["signal"])
