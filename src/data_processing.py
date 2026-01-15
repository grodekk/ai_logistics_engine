import pandas as pd

class DataProcessing:
    def __init__(self, db_service):
        self.db = db_service

    def get_monthly_costs(self):
        rows = self.db.fetch_all("SELECT cost_name, amount FROM monthly_costs")
        return pd.DataFrame(rows, columns=["cost_name", "amount"])

    def get_routes_costs(self):
        rows = self.db.fetch_all("SELECT route_name, fuel, tolls, ferry, hotel FROM routes_costs")
        return pd.DataFrame(rows, columns=["route_name", "fuel", "tolls", "ferry", "hotel"])