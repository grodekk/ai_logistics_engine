from src.core.paths import SQL_DIR
from src.db.sql_loader import SQLLoader
from src.repositories.query_helpers import fetch_dataframe, fetch_scalar


class AnalyticsRepository:
    def __init__(self, db_service):
        self.db = db_service
        self.sql_loader = SQLLoader(SQL_DIR)

    def get_fixed_costs_breakdown(self):
        query = self.sql_loader.queries.get_fixed_costs_breakdown
        columns = ["cost_name", "amount"]

        return fetch_dataframe(self.db, query, columns, ["amount"])

    def get_route_costs_breakdown(self):
        query = self.sql_loader.queries.get_route_costs_breakdown
        columns = ["route_name", "fuel", "tolls", "ferry", "hotel", "total_route_cost"]
        float_columns = ["fuel", "tolls", "ferry", "hotel", "total_route_cost"]

        return fetch_dataframe(self.db, query, columns, float_columns)

    def get_total_monthly_expenses(self):
        return fetch_scalar(self.db, self.sql_loader.queries.total_monthly_expenses)

    def get_average_cost_per_shipment(self):
        query = self.sql_loader.queries.get_avg_cost_per_shipment
        columns = ["client_name", "avg_cost_per_shipment"]
        float_columns = ["avg_cost_per_shipment"]

        return fetch_dataframe(self.db, query, columns, float_columns)

    def get_client_cost_benchmark(self):
        query = self.sql_loader.queries.client_cost_benchmark
        columns = ["client_name", "avg_cost", "overall_avg", "diff_from_avg", "vs_avg"]
        float_columns = ["avg_cost", "overall_avg", "diff_from_avg"]

        return fetch_dataframe(self.db, query, columns, float_columns)

    def get_top_late_clients(self):
        query = self.sql_loader.queries.get_top_late_clients
        columns = ["client_name", "late_payment_count"]

        return fetch_dataframe(self.db, query, columns)

    def get_route_cost_share(self):
        query = self.sql_loader.queries.route_cost_share_pct
        columns = ["route_name", "route_cost", "cost_share_pct"]
        float_columns = ["route_cost", "cost_share_pct"]

        return fetch_dataframe(self.db, query, columns, float_columns)

    def get_pareto_route_costs(self):
        query = self.sql_loader.queries.pareto_route_costs
        columns = ["route_name", "total_cost", "cumulative_cost", "cumulative_pct"]
        float_columns = ["total_cost", "cumulative_cost", "cumulative_pct"]

        return fetch_dataframe(self.db, query, columns, float_columns)

    def get_top_route_per_client(self):
        query = self.sql_loader.queries.top_route_per_client
        columns = ["client_name", "route_name", "route_cost"]
        float_columns = ["route_cost"]

        return fetch_dataframe(self.db, query, columns, float_columns)

    def get_client_risk(self):
        query = self.sql_loader.queries.risk_query
        columns = ["client_name", "avg_payment_delay_days", "late_payment_count", "risk_level"]

        return fetch_dataframe(self.db, query, columns)

    def get_clients_without_routes(self):
        query = self.sql_loader.queries.audit.clients_without_routes

        return fetch_dataframe(self.db, query, ["client_name"])

    def get_inactive_clients(self):
        query = self.sql_loader.queries.audit.inactive_clients

        return fetch_dataframe(self.db, query, ["client_name", "shipments"])
