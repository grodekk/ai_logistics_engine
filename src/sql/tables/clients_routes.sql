CREATE TABLE clients_routes (
    id SERIAL PRIMARY KEY,
    client_name TEXT NOT NULL,
    route_name TEXT NOT NULL,
    shipments INTEGER NOT NULL CHECK (shipments > 0),
    CONSTRAINT fk_client
        FOREIGN KEY (client_name) REFERENCES clients(client_name),
    CONSTRAINT fk_route
        FOREIGN KEY (route_name) REFERENCES routes_costs(route_name),
    CONSTRAINT unique_client_route
        UNIQUE (client_name, route_name)
);