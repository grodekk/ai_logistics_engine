import pandas as pd

class DataProcessing:
    def __init__(self, db_service):
        self.db = db_service

    def get_monthly_costs(self):
        rows = self.db.fetch_all("SELECT cost_name, amount FROM monthly_costs")
        df = pd.DataFrame(rows, columns=["cost_name", "amount"])
        return self._cast_columns_to_float(df, ["amount"])

    def get_routes_costs(self):
        rows = self.db.fetch_all("SELECT route_name, fuel, tolls, ferry, hotel FROM routes_costs")
        df = pd.DataFrame(rows, columns=["route_name", "fuel", "tolls", "ferry", "hotel"])
        return self._cast_columns_to_float(df, ["fuel", "tolls", "ferry", "hotel"])

    @staticmethod
    def _cast_columns_to_float(df, columns):
        for col in columns:
            if col in df.columns:
                df[col] = df[col].astype(float)
        return df