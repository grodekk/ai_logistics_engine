from src.db_service import DatabaseService
from src.config import Config


db = DatabaseService(Config())
db.connect()

try:
    db.execute("DROP TABLE IF EXISTS routes_costs, monthly_costs, clients CASCADE")
    db.create_tables()

    db.load_json("data/monthly_costs.json",
                 "monthly_costs",
                 ["cost_name", "amount"])

    db.load_json("data/routes_costs.json",
                 "routes_costs",
                 ["route_name", "fuel", "tolls", "ferry", "hotel"])

    db.load_json("data/clients.json",
                 "clients",
                 ["client_name", "client_class", "avg_payment_delay_days",
                          "late_payment_count", "total_shipments"])
finally:
    db.disconnect()