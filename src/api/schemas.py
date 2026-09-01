from typing import List

from pydantic import BaseModel, conint


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
