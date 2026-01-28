from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import logging

from src.db_service import DatabaseService
from src.config import Config
from src.data_processing import DataProcessing
from src.decision_engine import DecisionEngine
from src.predictive_engine import PredictiveEngine


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Logistics Engine", version="0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


db = DatabaseService(Config())
db.connect()
dp = DataProcessing(db)
decision_engine = DecisionEngine(dp)
predictive_engine = PredictiveEngine(dp)


class RouteInput(BaseModel):
    route_name: str
    monthly_trips: int


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


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "service": "AI Logistics Engine"}


@app.get("/routes/available", tags=["Routes"])
async def get_available_routes():
    try:
        df = dp.get_routes_costs()
        routes = df['route_name'].unique().tolist()
        return {"routes": routes}

    except Exception as e:
        logger.error(f"Error getting routes: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/decision/rates", response_model=RatesResponse, tags=["Decision Engine"])
async def calculate_route_rates(
        routes: List[RouteInput],
        monthly_profit_target: float
):

    try:
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

    except Exception as e:
        logger.error(f"Error calculating rates: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/clients/scores", response_model=List[ClientScoreResponse], tags=["Predictive Engine"])
async def get_client_scores():
    try:
        df = predictive_engine.calculate_client_scores()
        return [ClientScoreResponse(**row) for row in df.to_dict(orient="records")]

    except Exception as e:
        logger.error(f"Error getting scores: {e}")
        raise HTTPException(status_code=500, detail=str(e))