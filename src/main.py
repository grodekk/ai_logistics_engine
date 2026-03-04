from config import Config
from src.db.db_service import DatabaseService
from src.etl.load import DBLoader
from src.etl.exctract import JSONExtractor
from utils import build_fullpath
from src.json_loader import JsonLoader

def run():
    config = Config()
    db_service = DatabaseService(config)
    db_loader = DBLoader(db_service)
    json_loader = JsonLoader()
    extractor = JSONExtractor(json_loader)

    try:
        db_service.execute("DROP TABLE IF EXISTS routes_costs, monthly_costs, clients CASCADE")
        db_service.create_tables()

        json_files = [
            ("monthly_costs.json", "monthly_costs", ["cost_name", "amount"]),
            ("routes_costs.json", "routes_costs", ["route_name", "fuel", "tolls", "ferry", "hotel"]),
            ("clients.json", "clients", [
                "client_name",
                "client_class",
                "avg_payment_delay_days",
                "late_payment_count",
                "total_shipments"
            ])
        ]

        for filepath, table, columns in json_files:
            full_path = build_fullpath(filepath)
            df = extractor.load_json_to_df(full_path)
            db_loader.insert_dataframe(table, df, columns)

    finally:
        db_service.disconnect()

if __name__ == "__main__":
    run()