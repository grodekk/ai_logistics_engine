from src.core.config import Config
from src.db.db_service import DatabaseService
from src.etl.extract.json_extractor import JSONExtractor
from src.etl.load.db_loader import DBLoader
from src.etl.extract.json_loader import JsonLoader
from src.core.paths import data_path
from src.core.logger_config import configure_logging



def main():
    configure_logging()
    confirm = input("This will DROP and recreate database tables. Type RESET to continue: ")

    if confirm != "RESET":
        print("Aborted.")
        return

    config = Config()
    db_service = DatabaseService(config)
    db_loader = DBLoader(db_service)
    json_loader = JsonLoader()
    extractor = JSONExtractor(json_loader)

    try:
        db_service.connect()
        db_service.execute(
            "DROP TABLE IF EXISTS routes_costs, monthly_costs, clients, clients_routes CASCADE"
        )
        db_service.create_tables()
        db_service.create_views()

        json_files = [
            ("monthly_costs.json", "monthly_costs", ["cost_name", "amount"]),
            ("routes_costs.json", "routes_costs", ["route_name", "fuel", "tolls", "ferry", "hotel"]),
            (
                "clients.json",
                "clients",
                [
                    "client_name",
                    "client_class",
                    "avg_payment_delay_days",
                    "late_payment_count",
                ],
            ),
            ("clients_routes.json", "clients_routes", ["client_name", "route_name", "shipments"]),
        ]

        for filepath, table, columns in json_files:
            full_path = data_path(filepath)
            df = extractor.load_json_to_df(full_path)

            if table == "routes_costs":
                df = df.reindex(columns=columns, fill_value=0)
                df.fillna(0, inplace=True)

            db_loader.insert_dataframe(table, df, columns)

        print("Database reset and seeded successfully!")

    finally:
        db_service.disconnect()


if __name__ == "__main__":
    main()