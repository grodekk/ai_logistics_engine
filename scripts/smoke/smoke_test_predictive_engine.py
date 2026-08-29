from src.config import Config
from src.db.db_service import DatabaseService
from src.engines.predictive_engine import PredictiveEngine
from src.repositories.data_repository import DataRepository


def main():
    db = DatabaseService(Config())
    db.connect()

    try:
        data_repository = DataRepository(db)
        engine = PredictiveEngine(data_repository)

        df_scores = engine.calculate_client_scores()

        print("\n=== SMOKE TEST: PredictiveEngine ===\n")
        print(df_scores)
        print("\nSummary:")
        print(f"Min score: {df_scores['score'].min()}")
        print(f"Max score: {df_scores['score'].max()}")
        print(f"Average score: {df_scores['score'].mean():.2f}")

    finally:
        db.disconnect()


if __name__ == "__main__":
    main()
