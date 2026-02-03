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


# --- Models ---

class RouteInput(BaseModel):
    route_name: str
    monthly_trips: conint(gt=0, le=10000)


class RouteRateResponse(BaseModel):
    route_name: str
    monthly_trips: int
    total_route_cost: float
    required_rate_per_trip: float


class SummaryStats(BaseModel):
    total_trips: int
    total_route_costs: float
    total_monthly_costs: float


class RatesResponse(BaseModel):
    routes: List[RouteRateResponse]
    average_rate_per_trip: float
    summary: SummaryStats


class ClientScoreResponse(BaseModel):
    client_name: str
    client_class: str
    avg_payment_delay_days: int
    late_payment_count: int
    total_shipments: int
    score: float


# --- Endpoints ---

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "service": "AI Logistics Engine"}


@app.get("/routes/available", tags=["Routes"])
async def get_available_routes():
    df = dp.get_routes_costs()
    routes = df['route_name'].unique().tolist()
    return {"routes": routes}


@app.post("/decision/rates", response_model=RatesResponse, tags=["Decision Engine"])
async def calculate_route_rates(
        routes: List[RouteInput],
        monthly_profit_target: float
):
    result = decision_engine.calculate_rates_for_routes(
        routes_info=[r.model_dump() for r in routes],
        monthly_profit_target=monthly_profit_target
    )

    df = result["df"]

    routes_resp = [
        RouteRateResponse(**row)
        for row in df.to_dict(orient="records")
    ]

    return RatesResponse(
        routes=routes_resp,
        average_rate_per_trip=result["avg_rate"],
        summary=SummaryStats(
            total_trips=result["total_trips"],
            total_route_costs=result["total_route_costs"],
            total_monthly_costs=result["total_monthly_costs"]
        )
    )


@app.get("/clients/scores", response_model=List[ClientScoreResponse], tags=["Predictive Engine"])
async def get_client_scores():
    df = predictive_engine.calculate_client_scores()
    if df.empty:
        raise BusinessLogicError("No client data available for scoring")

    return [ClientScoreResponse(**row) for row in df.to_dict(orient="records")]