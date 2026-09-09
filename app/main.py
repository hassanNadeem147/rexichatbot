from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.auth import router as auth_router
from app.api.routes.chatroute import router as chat_router
from app.database.init_db import init_db
from app.logging.logger import logger
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Rexi ChatBot API starting")
    await init_db()
    logger.info("Database initialized successfully")
    yield
    logger.info("Rexi ChatBot API stopped")
app = FastAPI(
    title="Rexi ChatBot",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def home():
    logger.info("Health check requested")
    return {
        "status": "Healthy",
        "code": 200
    }
app.include_router(chat_router)
app.include_router(auth_router)