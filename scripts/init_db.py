from src.db_service import DatabaseService
from src.config import Config


def main():
    db = DatabaseService(Config())
    db.connect()
    try:
        db.create_tables()

        db.execute("TRUNCATE monthly_costs")
        db.execute("TRUNCATE routes_costs")
        db.execute("TRUNCATE clients")

        db.insert_json_into_table("monthly_costs.json", "monthly_costs", ["cost_name", "amount"])
        db.insert_json_into_table(
            "routes_costs.json",
            "routes_costs",
            ["route_name", "fuel", "tolls", "ferry", "hotel"]
        )
        db.insert_json_into_table(
            "clients.json",
            "clients",
            ["client_name", "client_class", "avg_payment_delay_days", "late_payment_count", "total_shipments"]
        )

        print("Database initialized and seeded successfully!")

    finally:
        db.disconnect()


if __name__ == "__main__":
    main()