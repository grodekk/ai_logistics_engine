from config import Config
from src.db.db_service import DatabaseService
from src.etl.load.db_loader import DBLoader
from src.etl.exctract import JSONExtractor
from utils import data_path
from src.json_loader import JsonLoader
# from etl.transform.routes_normalizer import normalize_routes
# import pandas as pd

def run():
    config = Config()
    db_service = DatabaseService(config)
    db_loader = DBLoader(db_service)
    json_loader = JsonLoader()
    extractor = JSONExtractor(json_loader)

    try:
        db_service.execute("DROP TABLE IF EXISTS routes_costs, monthly_costs, clients, clients_routes CASCADE")
        db_service.create_sql("tables")
        db_service.create_sql("views")

        json_files = [
            ("monthly_costs.json", "monthly_costs", ["cost_name", "amount"]),
            ("routes_costs.json", "routes_costs", ["route_name", "fuel", "tolls", "ferry", "hotel"]),
            ("clients_routes.json", "clients_routes", ["client_name", "route_name", "shipments"]),
            ("clients.json", "clients", [
                "client_name",
                "client_class",
                "avg_payment_delay_days",
                "late_payment_count",
            ])
        ]

        for filepath, table, columns in json_files:
            full_path = data_path(filepath)
            df = extractor.load_json_to_df(full_path)
            if table == "routes_costs":
                df = df.reindex(columns=columns, fill_value=0)
                df.fillna(0, inplace=True)
            #     routes_list = df.to_dict(orient="records")
            #     routes_list = normalize_routes(routes_list) ## for huge amount of records in json
            #     df = pd.DataFrame(routes_list)

            db_loader.insert_dataframe(table, df, columns)

    finally:
        db_service.disconnect()

if __name__ == "__main__":
    run()