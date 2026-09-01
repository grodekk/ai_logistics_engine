class DBLoader:
    def __init__(self, db_service):
        self.db = db_service

    def insert_dataframe(self, table, df, columns):
        values = self._prepare_values(df, columns)
        if values:
            self.db.bulk_insert(table, columns, values)

    @staticmethod
    def _prepare_values(df, columns):
        if df.empty:
            return []
        return [tuple(row) for row in df[columns].to_numpy()]
