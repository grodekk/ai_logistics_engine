class PredictiveEngine:
    def __init__(self, data_processing):
        self.dp = data_processing

    def calculate_client_scores(self):
        df_clients = self.dp.get_clients()
        df_clients = self._apply_class_bonus(df_clients)
        df_clients = self._compute_scores(df_clients)
        df_clients = self._clip_scores(df_clients)
        return df_clients[[
            "client_name",
            "client_class",
            "avg_payment_delay_days",
            "late_payment_count",
            "total_shipments",
            "score"
        ]]

    @staticmethod
    def _apply_class_bonus(df):
        class_bonus = {"A": 20, "B": 10, "C": 0}
        df["class_bonus"] = df["client_class"].map(class_bonus).fillna(0)
        return df

    @staticmethod
    def _compute_scores(df):
        df["score"] = (
                100
                - df["avg_payment_delay_days"] * 2
                - df["late_payment_count"] * 5
                + df["class_bonus"]
        )

        return df

    @staticmethod
    def _clip_scores(df):
        df["score"] = df["score"].clip(0, 100)
        return df