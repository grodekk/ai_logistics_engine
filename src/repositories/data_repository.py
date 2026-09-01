from src.core.paths import SQL_DIR
from src.db.sql_loader import SQLLoader
from src.repositories.query_helpers import fetch_dataframe, fetch_scalar


class DataRepository:
    def __init__(self, db_service):
        self.db = db_service
        self.sql_loader = SQLLoader(SQL_DIR)

    def get_fixed_costs_total(self):
        return fetch_scalar(self.db, self.sql_loader.queries.get_fixed_costs_total)

    def get_route_costs_total(self):
        query = self.sql_loader.queries.get_route_costs_total
        columns = ["route_name", "total_route_cost"]
        float_columns = ["total_route_cost"]

        return fetch_dataframe(self.db, query, columns, float_columns)

    def get_clients(self):
        query = self.sql_loader.queries.get_clients
        columns = ["client_name", "client_class", "avg_payment_delay_days", "late_payment_count", "total_shipments"]

        return fetch_dataframe(self.db, query, columns)
