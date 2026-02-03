from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, conint
from typing import List
from contextlib import asynccontextmanager
from src.db_service import DatabaseService
from src.config import Config
from src.data_processing import DataProcessing
from src.decision_engine import DecisionEngine
from src.predictive_engine import PredictiveEngine
from src.exceptions import BusinessLogicError
import logging
from src.api.exceptions import register_exception_handlers


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

register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


dp = DataProcessing(db)
decision_engine = DecisionEngine(dp)
predictive_engine = PredictiveEngine(dp)