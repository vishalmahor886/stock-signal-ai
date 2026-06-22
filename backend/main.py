from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routers.signal_api import router as signal_router
from backend.api.routers.news_analysis_api import router as news_analysis_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "running"}


app.include_router(signal_router, prefix="/api/signals", tags=["signal"])
