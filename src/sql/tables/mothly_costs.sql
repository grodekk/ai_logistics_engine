CREATE TABLE IF NOT EXISTS monthly_costs (
    id SERIAL PRIMARY KEY,
    cost_name TEXT NOT NULL,
    amount NUMERIC(10, 2) NOT NULL
);