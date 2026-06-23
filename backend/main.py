from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routers.signal_api import router as signal_router
from backend.services.financial_statement_service import get_financial_statement_for_symbol
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


@app.get("/")
async def home():
    return FileResponse("frontend/signal_terminal.html")


app.include_router(signal_router, prefix="/api/signals", tags=["signal"])

@app.get("/get_financial_statement/{symbol}")
def financial_statement(symbol:str):
    return get_financial_statement_for_symbol(symbol)
