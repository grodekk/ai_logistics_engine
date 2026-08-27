import pandas as pd


def fetch_dataframe(db_service, query, columns, float_columns=None):
    rows = db_service.fetch_all(query)
    df = pd.DataFrame(rows, columns=columns)

    if float_columns:
        df[float_columns] = df[float_columns].astype(float)

    return df

def fetch_scalar(db_service, query):
    rows = db_service.fetch_all(query)
    value = rows[0][0] if rows else None

    return float(value) if value is not None else None