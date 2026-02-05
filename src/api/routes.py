from fastapi import APIRouter
from typing import List
from src.api.schemas import (RouteInput, RatesResponse, ClientScoreResponse)
from src.api.services import  (RouteService, ClientService)


def create_routes(dp, decision_engine, predictive_engine) -> APIRouter:
    """Factory function to create API routes with injected dependencies"""
    router = APIRouter()

    route_service = RouteService(dp, decision_engine)
    client_service = ClientService(predictive_engine)

    @router.get("/health", tags=["Health"])
    async def health_check():
        """Health check endpoint"""
        return {"status": "ok", "service": "AI Logistics Engine"}


    @router.get("/routes/available", tags=["Routes"])
    async def get_available_routes():
        """Fetches available routes"""
        routes = route_service.get_available_routes()
        return {"routes": routes}


    @router.post("/decision/rates", response_model=RatesResponse, tags=["Decision Engine"])
    async def calculate_route_rates(routes: List[RouteInput], monthly_profit_target: float):
        """Calculates required rates for given routes to meet profit target"""
        return route_service.calculate_rates(routes, monthly_profit_target)


    @router.get("/clients/scores", response_model=List[ClientScoreResponse], tags=["Predictive Engine"])
    async def get_client_scores():
        """Fetches client scores"""
        return client_service.get_client_scores()


    return router