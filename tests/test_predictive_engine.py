import pandas as pd
import pytest

from src.engines.predictive_engine import PredictiveEngine


class FakeDataRepository:
    @staticmethod
    async def get_clients():
        clients = [
            {
                "client_name": "Client A",
                "client_class": "A",
                "avg_payment_delay_days": 5,
                "late_payment_count": 1,
                "total_shipments": 20,
            },
            {
                "client_name": "Client B",
                "client_class": "B",
                "avg_payment_delay_days": 10,
                "late_payment_count": 2,
                "total_shipments": 10,
            },
        ]

        return pd.DataFrame(clients)


class EdgeCaseDataRepository:
    @staticmethod
    async def get_clients():
        clients = [
            {
                "client_name": "Perfect Client",
                "client_class": "A",
                "avg_payment_delay_days": 0,
                "late_payment_count": 0,
                "total_shipments": 50,
            },
            {
                "client_name": "Risky Client",
                "client_class": "C",
                "avg_payment_delay_days": 80,
                "late_payment_count": 10,
                "total_shipments": 2,
            },
        ]

        return pd.DataFrame(clients)


@pytest.mark.asyncio
async def test_calculate_client_scores():
    engine = PredictiveEngine(FakeDataRepository())

    result = await engine.calculate_client_scores()
    scores = result.set_index("client_name")["score"]

    expected_columns = [
        "client_name",
        "client_class",
        "avg_payment_delay_days",
        "late_payment_count",
        "total_shipments",
        "score",
    ]

    assert list(result.columns) == expected_columns
    assert scores["Client A"] == 100
    assert scores["Client B"] == 80


@pytest.mark.asyncio
async def test_calculate_client_scores_clips_values_to_valid_range():
    engine = PredictiveEngine(EdgeCaseDataRepository())

    result = await engine.calculate_client_scores()
    scores = result.set_index("client_name")["score"]

    assert scores["Perfect Client"] == 100
    assert scores["Risky Client"] == 0
