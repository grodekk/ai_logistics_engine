EXPECTED_COLUMNS = {
    "fuel": 0,
    "tolls": 0,
    "ferry": 0,
    "hotel": 0
}

import math

def normalize_routes(routes):
    return [
        {
            **EXPECTED_COLUMNS,
            **{k: v for k, v in route.items()
               if v is not None and not (isinstance(v, float) and math.isnan(v))}
        }
        for route in routes
    ]