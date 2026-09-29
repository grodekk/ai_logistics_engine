import asyncio
import selectors

from src.core.config import Config
from src.core.logger_config import configure_logging
from src.db.db_service import DatabaseService
from src.engines.decision_engine import DecisionEngine
from src.repositories.data_repository import DataRepository


async def main():
    configure_logging()
    db = DatabaseService(Config())

    try:
        await db.connect()

        data_repository = DataRepository(db)
        engine = DecisionEngine(data_repository)

        routes_info = [
            {"route_name": "Warsaw - Berlin", "monthly_trips": 2},
            {"route_name": "Paris - London", "monthly_trips": 1},
        ]

        result = await engine.calculate_rates_for_routes(
            routes_info=routes_info,
            monthly_profit_target=10000,
        )

        print("\n=== SMOKE TEST: DecisionEngine ===\n")
        print(result["df"])
        print(f"\nTotal trips: {result['total_trips']}")
        print(f"Total route costs: {result['total_route_costs']:.2f}")
        print(f"Total monthly costs: {result['total_monthly_costs']:.2f}")
        print(f"Average required rate per trip: {result['avg_rate']:.2f}")
        print("\n=================================\n")

    finally:
        await db.disconnect()


def create_event_loop():
    return asyncio.SelectorEventLoop(selectors.SelectSelector())


if __name__ == "__main__":
    asyncio.run(main(), loop_factory=create_event_loop)
