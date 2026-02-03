from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from src.db_service import DatabaseService
from src.config import Config
from src.data_processing import DataProcessing
from src.decision_engine import DecisionEngine
from src.predictive_engine import PredictiveEngine

from src.api.exceptions import register_exception_handlers
from src.api.routes import create_routes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


db = DatabaseService(Config())

@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        db.connect()
        logger.info("Database connected")
        yield
    finally:
        db.disconnect()
        logger.info("Database disconnected")

app = FastAPI(title="AI Logistics Engine", version="0.1", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

register_exception_handlers(app)

dp = DataProcessing(db)
decision_engine = DecisionEngine(dp)
predictive_engine = PredictiveEngine(dp)

router = create_routes(dp, decision_engine, predictive_engine)
app.include_router(router)