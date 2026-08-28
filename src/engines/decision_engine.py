import pandas as pd


class DecisionEngine:
    def __init__(self, data_repository):
        self.data_repository = data_repository

    def calculate_rates_for_routes(self, routes_info, monthly_profit_target):
        df = self._prepare_routes_dataframe(routes_info)
        df = self._attach_route_costs(df)

        self._validate_routes(df)

        total_fixed_costs = self._get_fixed_costs_total()
        total_route_costs = self._get_total_route_costs(df)
        total_trips = self._get_total_trips(df)

        overhead_per_trip = self._calculate_overhead_per_trip(total_fixed_costs, monthly_profit_target, total_trips)

        df["required_rate_per_trip"] = self._calculate_required_rate(df, overhead_per_trip)
        df["required_rate_per_trip"] = df["required_rate_per_trip"].round(0)

        avg_rate = self._calculate_average_rate(df, total_trips)
        avg_rate = round(avg_rate, 0)

        return {
            "df": df[["route_name", "monthly_trips", "total_route_cost", "required_rate_per_trip"]],
            "avg_rate": avg_rate,
            "total_monthly_costs": total_fixed_costs,
            "total_route_costs": total_route_costs,
            "total_trips": total_trips
        }

    def _attach_route_costs(self, df):
        route_costs = self.data_repository.get_route_costs_total()

        return df.merge(route_costs, on="route_name", how="left")

    def _get_fixed_costs_total(self):
        return self.data_repository.get_fixed_costs_total()

    @staticmethod
    def _validate_routes(df):
        rows_with_missing_data = df.isna().any(axis=1)
        if rows_with_missing_data.any():
            routes_with_missing_data = df.loc[rows_with_missing_data, "route_name"].tolist()
            raise ValueError(f"Route(s) with missing data: {routes_with_missing_data}")

        if df["monthly_trips"].sum() == 0:
            raise ValueError("Total monthly trips is zero — cannot calculate rates")

    @staticmethod
    def _get_total_route_costs(df):
        return (df["total_route_cost"] * df["monthly_trips"]).sum()

    @staticmethod
    def _get_total_trips(df):
        return df["monthly_trips"].sum()

    @staticmethod
    def _calculate_overhead_per_trip(total_monthly_costs, profit_target, total_trips):
        return (total_monthly_costs + profit_target) / total_trips

    @staticmethod
    def _calculate_required_rate(df, overhead_per_trip):
        return df["total_route_cost"] + overhead_per_trip

    @staticmethod
    def _calculate_average_rate(df, total_trips):
        weighted_rates = df["required_rate_per_trip"] * df["monthly_trips"]

        return weighted_rates.sum() / total_trips

    @staticmethod
    def _prepare_routes_dataframe(routes_info):
        df = pd.DataFrame(routes_info)
        df = df.groupby("route_name", as_index=False).agg({"monthly_trips": "sum"})

        return df