CREATE TABLE IF NOT EXISTS routes_costs (
    id SERIAL PRIMARY KEY,
    route_name TEXT NOT NULL UNIQUE,
    fuel NUMERIC(10, 2) NOT NULL CHECK (fuel > 0),
    tolls NUMERIC(10, 2) NOT NULL DEFAULT 0 CHECK (tolls >= 0),
    ferry NUMERIC(10, 2) NOT NULL DEFAULT 0 CHECK (ferry >= 0),
    hotel NUMERIC(10, 2) NOT NULL DEFAULT 0 CHECK (hotel >= 0)
);