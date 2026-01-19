from src.db_service import DatabaseService
from src.data_processing import DataProcessing
from src.predictive_engine import PredictiveEngine
from src.config import Config


def main():
    db = DatabaseService(Config())
    db.connect()

    try:
        dp = DataProcessing(db)
        engine = PredictiveEngine(dp)

        df_scores = engine.calculate_client_scores()

        print("\n=== SHADOW TEST: PredictiveEngine ===\n")
        print(df_scores)
        print("\nSummary:")
        print(f"Min score: {df_scores['score'].min()}")
        print(f"Max score: {df_scores['score'].max()}")
        print(f"Average score: {df_scores['score'].mean():.2f}")

    finally:
        db.disconnect()


if __name__ == "__main__":
    main()