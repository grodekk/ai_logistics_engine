CREATE TABLE IF NOT EXISTS routes_costs (
    id SERIAL PRIMARY KEY,
    route_name TEXT NOT NULL,
    fuel NUMERIC(10, 2) NOT NULL,
    tolls NUMERIC(10, 2) DEFAULT 0,
    ferry NUMERIC(10, 2) DEFAULT 0,
    hotel NUMERIC(10, 2) DEFAULT 0
);