import pandas as pd
import pytest

from src.engines.decision_engine import DecisionEngine


class FakeDataRepository:
    @staticmethod
    async def get_route_costs_total():
        return pd.DataFrame(
            [
                {"route_name": "Warsaw - Berlin", "total_route_cost": 1000},
                {"route_name": "Paris - London", "total_route_cost": 2000},
            ]
        )

    @staticmethod
    async def get_fixed_costs_total():
        return 9000


@pytest.mark.asyncio
async def test_calculate_rates_for_routes():
    engine = DecisionEngine(FakeDataRepository())

    result = await engine.calculate_rates_for_routes(
        routes_info=[
            {"route_name": "Warsaw - Berlin", "monthly_trips": 2},
            {"route_name": "Paris - London", "monthly_trips": 1},
        ],
        monthly_profit_target=6000,
    )

    rates = result["df"].set_index("route_name")["required_rate_per_trip"]

    assert result["total_trips"] == 3
    assert result["total_route_costs"] == 4000
    assert result["total_monthly_costs"] == 9000
    assert result["avg_rate"] == 6333
    assert rates["Warsaw - Berlin"] == 6000
    assert rates["Paris - London"] == 7000


@pytest.mark.asyncio
async def test_calculate_rates_groups_duplicate_routes():
    engine = DecisionEngine(FakeDataRepository())

    result = await engine.calculate_rates_for_routes(
        routes_info=[
            {"route_name": "Warsaw - Berlin", "monthly_trips": 1},
            {"route_name": "Warsaw - Berlin", "monthly_trips": 2},
        ],
        monthly_profit_target=6000,
    )

    trips = result["df"].set_index("route_name")["monthly_trips"]

    assert result["total_trips"] == 3
    assert trips["Warsaw - Berlin"] == 3


@pytest.mark.asyncio
async def test_calculate_rates_raises_error_for_unknown_route():
    engine = DecisionEngine(FakeDataRepository())

    with pytest.raises(ValueError, match=r"Route\(s\) with missing data"):
        await engine.calculate_rates_for_routes(
            routes_info=[{"route_name": "Unknown Route", "monthly_trips": 1}],
            monthly_profit_target=6000,
        )


@pytest.mark.asyncio
async def test_calculate_rates_raises_error_when_total_trips_is_zero():
    engine = DecisionEngine(FakeDataRepository())

    with pytest.raises(ValueError, match="Total monthly trips is zero"):
        await engine.calculate_rates_for_routes(
            routes_info=[{"route_name": "Warsaw - Berlin", "monthly_trips": 0}],
            monthly_profit_target=6000,
        )
