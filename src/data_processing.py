import pandas as pd

class DataProcessing:
    def __init__(self, db_service):
        self.db = db_service

    def get_monthly_costs(self):
        query = """
        SELECT cost_name, amount
        FROM monthly_costs
        """
        rows = self.db.fetch_all(query)
        df = pd.DataFrame(rows, columns=["cost_name", "amount"])
        return self._cast_columns_to_float(df, ["amount"])

    def get_routes_costs(self):
        query = """
        SELECT route_name, fuel, tolls, ferry, hotel
        FROM routes_costs
        """
        rows = self.db.fetch_all(query)
        df = pd.DataFrame(rows, columns=["route_name", "fuel", "tolls", "ferry", "hotel"])
        return self._cast_columns_to_float(df, ["fuel", "tolls", "ferry", "hotel"])

    def get_clients(self):
        query = """
        SELECT client_name,
               avg_payment_delay_days,
               late_payment_count,
               client_class,
               total_shipments
        FROM clients
        """
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