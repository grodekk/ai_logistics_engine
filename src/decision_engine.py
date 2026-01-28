import pandas as pd

class DecisionEngine:
    def __init__(self, data_processing):
        self.dp = data_processing

    def calculate_rates_for_routes(self, routes_info, monthly_profit_target):
        df = self._prepare_routes_dataframe(routes_info)
        df = self._merge_route_costs(df)
        self._validate_routes(df)

        df["total_route_cost"] = self._calculate_total_route_cost(df)
        total_monthly_costs = self._get_total_monthly_costs()
        total_route_costs = self._get_total_route_costs(df)
        total_trips = self._get_total_trips(df)

        overhead_per_trip = self._calculate_overhead_per_trip(total_monthly_costs, monthly_profit_target, total_trips)
        df["required_rate_per_trip"] = self._calculate_required_rate(df, overhead_per_trip)
        df["required_rate_per_trip"] = df["required_rate_per_trip"].round(0)

        avg_rate = self._calculate_average_rate(df, total_trips)
        avg_rate = round(avg_rate, 0)

        return {
            "df": df[[
                "route_name",
                "monthly_trips",
                "total_route_cost",
                "required_rate_per_trip"
            ]],
            "avg_rate": avg_rate,
            "total_monthly_costs": total_monthly_costs,
            "total_route_costs": total_route_costs,
            "total_trips": total_trips
        }

    def _merge_route_costs(self, df):
        df_routes = self.dp.get_routes_costs()
        return df.merge(df_routes, on="route_name", how="left")

    @staticmethod
    def _validate_routes(df):
        if df.isnull().any().any():
            missing = df[df.isnull().any(axis=1)]["route_name"].tolist()
            raise ValueError(f"Route(s) not found: {missing}")

    @staticmethod
    def _calculate_total_route_cost(df):
        return df[["fuel", "tolls", "ferry", "hotel"]].fillna(0).sum(axis=1)

    def _get_total_monthly_costs(self):
        return self.dp.get_monthly_costs()["amount"].sum()

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
        return (df["required_rate_per_trip"] * df["monthly_trips"]).sum() / total_trips

    @staticmethod
    def _prepare_routes_dataframe(routes_info):
        df = pd.DataFrame(routes_info)
        df = df.groupby('route_name', as_index=False).agg({'monthly_trips': 'sum'})
        return df