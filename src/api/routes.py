from fastapi import APIRouter, Request

from src.api.schemas import ClientScoreResponse, RatesResponse, RouteInput
from src.api.services import AnalyticsService, ClientService, RouteService


def create_routes() -> APIRouter:
    router = APIRouter()

    def get_route_service(request: Request) -> RouteService:
        return RouteService(
            request.app.state.data_repository,
            request.app.state.decision_engine,
        )

    def get_client_service(request: Request) -> ClientService:
        return ClientService(request.app.state.predictive_engine)

    def get_analytics_service(request: Request) -> AnalyticsService:
        return AnalyticsService(request.app.state.analytics_repository)

    @router.get("/health", tags=["Health"])
    async def health_check():
        return {"status": "ok", "service": "AI Logistics Engine"}

    @router.get("/routes/available", tags=["Routes"])
    async def get_available_routes(request: Request):
        route_service = get_route_service(request)
        routes = route_service.get_available_routes()

        return {"routes": routes}

    @router.post("/decision/rates", response_model=RatesResponse, tags=["Decision Engine"])
    async def calculate_route_rates(
        request: Request,
        routes: list[RouteInput],
        monthly_profit_target: float,
    ):
        route_service = get_route_service(request)

        return route_service.calculate_rates(routes, monthly_profit_target)

    @router.get("/clients/scores", response_model=list[ClientScoreResponse], tags=["Predictive Engine"])
    async def get_client_scores(request: Request):
        client_service = get_client_service(request)

        return client_service.get_client_scores()

    @router.get("/analytics/fixed-costs", tags=["Analytics"])
    async def get_fixed_costs_breakdown(request: Request):
        analytics_service = get_analytics_service(request)

        return analytics_service.get_fixed_costs_breakdown()

    @router.get("/analytics/route-costs", tags=["Analytics"])
    async def get_route_costs_breakdown(request: Request):
        analytics_service = get_analytics_service(request)

        return analytics_service.get_route_costs_breakdown()

    @router.get("/analytics/monthly-expenses", tags=["Analytics"])
    async def get_total_monthly_expenses(request: Request):
        analytics_service = get_analytics_service(request)

        return analytics_service.get_total_monthly_expenses()

    @router.get("/analytics/avg-cost-per-shipment", tags=["Analytics"])
    async def get_average_cost_per_shipment(request: Request):
        analytics_service = get_analytics_service(request)

        return analytics_service.get_average_cost_per_shipment()

    @router.get("/analytics/client-benchmark", tags=["Analytics"])
    async def get_client_cost_benchmark(request: Request):
        analytics_service = get_analytics_service(request)

        return analytics_service.get_client_cost_benchmark()

    @router.get("/analytics/top-late-clients", tags=["Analytics"])
    async def get_top_late_clients(request: Request):
        analytics_service = get_analytics_service(request)

        return analytics_service.get_top_late_clients()

    @router.get("/analytics/route-cost-share", tags=["Analytics"])
    async def get_route_cost_share(request: Request):
        analytics_service = get_analytics_service(request)

        return analytics_service.get_route_cost_share()

    @router.get("/analytics/pareto-route-costs", tags=["Analytics"])
    async def get_pareto_route_costs(request: Request):
        analytics_service = get_analytics_service(request)

        return analytics_service.get_pareto_route_costs()

    @router.get("/analytics/top-route-per-client", tags=["Analytics"])
    async def get_top_route_per_client(request: Request):
        analytics_service = get_analytics_service(request)

        return analytics_service.get_top_route_per_client()

    @router.get("/analytics/client-risk", tags=["Analytics"])
    async def get_client_risk(request: Request):
        analytics_service = get_analytics_service(request)

        return analytics_service.get_client_risk()

    @router.get("/analytics/audit/clients-without-routes", tags=["Analytics Audit"])
    async def get_clients_without_routes(request: Request):
        analytics_service = get_analytics_service(request)

        return analytics_service.get_clients_without_routes()

    @router.get("/analytics/audit/inactive-clients", tags=["Analytics Audit"])
    async def get_inactive_clients(request: Request):
        analytics_service = get_analytics_service(request)

        return analytics_service.get_inactive_clients()

    return router