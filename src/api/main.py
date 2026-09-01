import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.exception_handlers import register_exception_handlers
from src.api.routes import create_routes
from src.core.config import Config
from src.core.logger_config import configure_logging
from src.db.db_service import DatabaseService
from src.engines.decision_engine import DecisionEngine
from src.engines.predictive_engine import PredictiveEngine
from src.repositories.analytics_repository import AnalyticsRepository
from src.repositories.data_repository import DataRepository

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    config = Config()
    db = DatabaseService(config)
    db.connect()

    data_repository = DataRepository(db)
    analytics_repository = AnalyticsRepository(db)
    decision_engine = DecisionEngine(data_repository)
    predictive_engine = PredictiveEngine(data_repository)

    app.state.db = db
    app.state.data_repository = data_repository
    app.state.analytics_repository = analytics_repository
    app.state.decision_engine = decision_engine
    app.state.predictive_engine = predictive_engine

    try:
        logger.info("Application ready")
        yield

    finally:
        logger.info("Application shutting down")
        db.disconnect()
        logger.info("Shutdown complete")


app = FastAPI(
    title="AI Logistics Engine",
    version="0.1",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)
app.include_router(create_routes())
