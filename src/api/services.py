from typing import List
from src.api.schemas import (RouteInput, RatesResponse, RouteRateResponse,SummaryStats, ClientScoreResponse)
from src.api.exceptions import BusinessLogicError
from src.data_processing import DataProcessing
from src.decision_engine import DecisionEngine
from src.predictive_engine import PredictiveEngine


class RouteService:
    def __init__(self, data_processor: DataProcessing, rate_calculator: DecisionEngine) -> None:
        self.data_processor = data_processor
        self.rate_calculator = rate_calculator

    def get_available_routes(self) -> List[str]:
        df = self.data_processor.get_routes_costs()
        routes = df['route_name'].unique().tolist()
        return routes

    def calculate_rates(self, routes: List[RouteInput], monthly_profit_target: float) -> RatesResponse:

        result = self.rate_calculator.calculate_rates_for_routes(
            routes_info=[r.model_dump() for r in routes],
            monthly_profit_target=monthly_profit_target
        )

        routes_resp = [RouteRateResponse(**row) for row in result["df"].to_dict(orient="records")]

        return RatesResponse(
            routes=routes_resp,
            average_rate_per_trip=result["avg_rate"],
            summary=SummaryStats(
                total_trips=result["total_trips"],
                total_route_costs=result["total_route_costs"],
                total_monthly_costs=result["total_monthly_costs"]
            )
        )


class ClientService:
    def __init__(self, scoring_engine: PredictiveEngine) -> None:
        self.scoring_engine = scoring_engine

    def get_client_scores(self) -> List[ClientScoreResponse]:
        df = self.scoring_engine.calculate_client_scores()

        if df.empty:
            raise BusinessLogicError("No client data available for scoring")

        return [
            ClientScoreResponse(**row)
            for row in df.to_dict(orient="records")
        ]