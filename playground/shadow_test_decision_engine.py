from src.db_service import DatabaseService
from src.data_processing import DataProcessing
from src.decision_engine import DecisionEngine
from src.config import Config


def main():
    db = DatabaseService(Config())
    db.connect()

    try:
        dp = DataProcessing(db)
        engine = DecisionEngine(dp)

        routes_info = [
            {"route_name": "Warsaw - Berlin", "monthly_trips": 2},
            {"route_name": "Paris - London", "monthly_trips": 1}
        ]

        monthly_profit_target = 10000

        result = engine.calculate_rates_for_routes(
            routes_info=routes_info,
            monthly_profit_target=monthly_profit_target
        )

        print("\n=== SHADOW TEST: DecisionEngine ===\n")
        print(result["df"])
        print(f"\nTotal trips: {result['total_trips']}")
        print(f"Total route costs: {result['total_route_costs']:.2f}")
        print(f"Total monthly costs: {result['total_monthly_costs']:.2f}")
        print(f"Average required rate per trip: {result['avg_rate']:.2f}")
        print("\n=================================\n")

    finally:
        db.disconnect()


if __name__ == "__main__":
    main()