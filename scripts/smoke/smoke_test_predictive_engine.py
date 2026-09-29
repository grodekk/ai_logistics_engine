import asyncio
import selectors

from src.core.config import Config
from src.core.logger_config import configure_logging
from src.db.db_service import DatabaseService
from src.engines.predictive_engine import PredictiveEngine
from src.repositories.data_repository import DataRepository


async def main():
    configure_logging()
    db = DatabaseService(Config())

    try:
        await db.connect()
        data_repository = DataRepository(db)
        engine = PredictiveEngine(data_repository)

        df_scores = await engine.calculate_client_scores()

        print("\n=== SMOKE TEST: PredictiveEngine ===\n")
        print(df_scores)
        print("\nSummary:")
        print(f"Min score: {df_scores['score'].min()}")
        print(f"Max score: {df_scores['score'].max()}")
        print(f"Average score: {df_scores['score'].mean():.2f}")

    finally:
        await db.disconnect()


def create_event_loop():
    return asyncio.SelectorEventLoop(selectors.SelectSelector())


if __name__ == "__main__":
    asyncio.run(main(), loop_factory=create_event_loop)
