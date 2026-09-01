from src.api.schemas import ClientScoreResponse, RatesResponse, RouteInput, RouteRateResponse, SummaryStats
from src.core.exceptions import BusinessLogicError
from src.engines.decision_engine import DecisionEngine
from src.engines.predictive_engine import PredictiveEngine
from src.repositories.analytics_repository import AnalyticsRepository
from src.repositories.data_repository import DataRepository


class RouteService:
    def __init__(self, data_repository: DataRepository, decision_engine: DecisionEngine) -> None:
        self.data_repository = data_repository
        self.decision_engine = decision_engine

    def get_available_routes(self) -> list[str]:
        df = self.data_repository.get_route_costs_total()
        routes = df["route_name"].unique().tolist()

        return routes

    def calculate_rates(self, routes: list[RouteInput], monthly_profit_target: float) -> RatesResponse:
        result = self.decision_engine.calculate_rates_for_routes(
            routes_info=[r.model_dump() for r in routes], monthly_profit_target=monthly_profit_target
        )

        route_rows = result["df"].to_dict(orient="records")
        routes_response = [RouteRateResponse(**row) for row in route_rows]

        rates_response = RatesResponse(
            routes=routes_response,
            average_rate_per_trip=result["avg_rate"],
            summary=SummaryStats(
                total_trips=result["total_trips"],
                total_route_costs=result["total_route_costs"],
                total_monthly_costs=result["total_monthly_costs"],
            ),
        )

        return rates_response


class ClientService:
    def __init__(self, scoring_engine: PredictiveEngine) -> None:
        self.scoring_engine = scoring_engine

    def get_client_scores(self) -> list[ClientScoreResponse]:
        df = self.scoring_engine.calculate_client_scores()

        if df.empty:
            raise BusinessLogicError("No client data available for scoring")

        client_rows = df.to_dict(orient="records")

        clients_response = [ClientScoreResponse(**row) for row in client_rows]

        return clients_response


class AnalyticsService:
    def __init__(self, analytics_repository: AnalyticsRepository) -> None:
        self.analytics_repository = analytics_repository

    @staticmethod
    def _to_records(df) -> list[dict]:
        return df.to_dict(orient="records")

    def get_fixed_costs_breakdown(self) -> list[dict]:
        df = self.analytics_repository.get_fixed_costs_breakdown()

        return self._to_records(df)

    def get_route_costs_breakdown(self) -> list[dict]:
        df = self.analytics_repository.get_route_costs_breakdown()

        return self._to_records(df)

    def get_total_monthly_expenses(self) -> dict:
        total = self.analytics_repository.get_total_monthly_expenses()

        return {"total_monthly_expenses": total}

    def get_average_cost_per_shipment(self) -> list[dict]:
        df = self.analytics_repository.get_average_cost_per_shipment()

        return self._to_records(df)

    def get_client_cost_benchmark(self) -> list[dict]:
        df = self.analytics_repository.get_client_cost_benchmark()

        return self._to_records(df)

    def get_top_late_clients(self) -> list[dict]:
        df = self.analytics_repository.get_top_late_clients()

        return self._to_records(df)

    def get_route_cost_share(self) -> list[dict]:
        df = self.analytics_repository.get_route_cost_share()

        return self._to_records(df)

    def get_pareto_route_costs(self) -> list[dict]:
        df = self.analytics_repository.get_pareto_route_costs()

        return self._to_records(df)

    def get_top_route_per_client(self) -> list[dict]:
        df = self.analytics_repository.get_top_route_per_client()

        return self._to_records(df)

    def get_client_risk(self) -> list[dict]:
        df = self.analytics_repository.get_client_risk()

        return self._to_records(df)

    def get_clients_without_routes(self) -> list[dict]:
        df = self.analytics_repository.get_clients_without_routes()

        return self._to_records(df)

    def get_inactive_clients(self) -> list[dict]:
        df = self.analytics_repository.get_inactive_clients()

        return self._to_records(df)
