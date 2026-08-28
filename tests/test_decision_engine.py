import pandas as pd
import pytest
from src.engines.decision_engine import DecisionEngine


class FakeDataRepository:
    @staticmethod
    def get_route_costs_total():
        return pd.DataFrame([
            {"route_name": "Warsaw - Berlin", "total_route_cost": 1000},
            {"route_name": "Paris - London", "total_route_cost": 2000},
        ])

    @staticmethod
    def get_fixed_costs_total():
        return 9000


def test_calculate_rates_for_routes():
    engine = DecisionEngine(FakeDataRepository())

    result = engine.calculate_rates_for_routes(
        routes_info=[
            {"route_name": "Warsaw - Berlin", "monthly_trips": 2},
            {"route_name": "Paris - London", "monthly_trips": 1},
        ],
        monthly_profit_target=6000,
    )

    df = result["df"]

    warsaw_rate = df.loc[df["route_name"] == "Warsaw - Berlin", "required_rate_per_trip"].iloc[0]
    paris_rate = df.loc[df["route_name"] == "Paris - London", "required_rate_per_trip"].iloc[0]

    assert result["total_trips"] == 3
    assert result["total_route_costs"] == 4000
    assert result["total_monthly_costs"] == 9000
    assert result["avg_rate"] == 6333

    assert warsaw_rate == 6000
    assert paris_rate == 7000


def test_calculate_rates_groups_duplicate_routes():
    engine = DecisionEngine(FakeDataRepository())

    result = engine.calculate_rates_for_routes(
        routes_info=[
            {"route_name": "Warsaw - Berlin", "monthly_trips": 1},
            {"route_name": "Warsaw - Berlin", "monthly_trips": 2},
        ],
        monthly_profit_target=6000,
    )

    df = result["df"]
    warsaw_trips = df.loc[df["route_name"] == "Warsaw - Berlin", "monthly_trips"].iloc[0]

    assert result["total_trips"] == 3
    assert warsaw_trips == 3


def test_calculate_rates_raises_error_for_unknown_route():
    engine = DecisionEngine(FakeDataRepository())

    with pytest.raises(ValueError, match=r"Route\(s\) with missing data"):
        engine.calculate_rates_for_routes(
            routes_info=[{"route_name": "Unknown Route", "monthly_trips": 1}],
            monthly_profit_target=6000,
        )


def test_calculate_rates_raises_error_when_total_trips_is_zero():
    engine = DecisionEngine(FakeDataRepository())

    with pytest.raises(ValueError, match="Total monthly trips is zero"):
        engine.calculate_rates_for_routes(
            routes_info=[{"route_name": "Warsaw - Berlin", "monthly_trips": 0}],
            monthly_profit_target=6000,
        )