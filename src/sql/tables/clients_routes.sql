CREATE TABLE IF NOT EXISTS clients_routes (
    id SERIAL PRIMARY KEY,
    client_name TEXT NOT NULL,
    route_name TEXT NOT NULL,
    shipments NUMERIC(10, 2) DEFAULT 0
);