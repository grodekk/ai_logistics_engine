import pandas as pd

from src.engines.predictive_engine import PredictiveEngine


class FakeDataRepository:
    @staticmethod
    def get_clients():
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
    def get_clients():
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


def test_calculate_client_scores():
    engine = PredictiveEngine(FakeDataRepository())

    result = engine.calculate_client_scores()

    client_a_score = result.loc[result["client_name"] == "Client A", "score"].iloc[0]
    client_b_score = result.loc[result["client_name"] == "Client B", "score"].iloc[0]

    expected_columns = [
        "client_name",
        "client_class",
        "avg_payment_delay_days",
        "late_payment_count",
        "total_shipments",
        "score",
    ]

    assert list(result.columns) == expected_columns
    assert client_a_score == 100
    assert client_b_score == 80


def test_calculate_client_scores_clips_values_to_valid_range():
    engine = PredictiveEngine(EdgeCaseDataRepository())

    result = engine.calculate_client_scores()

    perfect_client_score = result.loc[result["client_name"] == "Perfect Client", "score"].iloc[0]
    risky_client_score = result.loc[result["client_name"] == "Risky Client", "score"].iloc[0]

    assert perfect_client_score == 100
    assert risky_client_score == 0