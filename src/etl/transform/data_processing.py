import pandas as pd
from src.etl.load.sql_loader import SQLLoader
from src.utils import SQL_DIR


class DataProcessing:
    def __init__(self, db_service):
        self.db = db_service
        self.sql_loader = SQLLoader(SQL_DIR)


    def get_monthly_costs(self):
        query = self.sql_loader.queries.get_monthly_costs
        rows = self.db.fetch_all(query)
        df = pd.DataFrame(rows, columns=["cost_name", "amount"])
        return self._cast_columns_to_float(df, ["amount"])


    def get_routes_costs(self):
        query =  self.sql_loader.queries.get_routes_costs
        rows = self.db.fetch_all(query)
        df = pd.DataFrame(rows, columns=["route_name", "fuel", "tolls", "ferry", "hotel", "total_route_cost"])
        return self._cast_columns_to_float(df, ["fuel", "tolls", "ferry", "hotel", "total_route_cost"])


    def get_clients(self):
        query = self.sql_loader.queries.get_clients
        rows = self.db.fetch_all(query)
        df = pd.DataFrame(
            rows,
            columns=["client_name", "avg_payment_delay_days", "late_payment_count", "client_class", "total_shipments"]
        )
        df = self._cast_columns_to_float(df, [
                                              "avg_payment_delay_days",
                                              "late_payment_count",
                                              "total_shipments"
        ])
        return df


    @staticmethod
    def _cast_columns_to_float(df, columns):
        for col in columns:
            if col in df.columns:
                df[col] = df[col].astype(float)
        return df