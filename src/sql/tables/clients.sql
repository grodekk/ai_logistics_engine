CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY,
    client_name TEXT NOT NULL UNIQUE,
    client_class TEXT NOT NULL CHECK (client_class IN ('A', 'B', 'C', 'D')),
    avg_payment_delay_days INTEGER NOT NULL DEFAULT 0 CHECK (avg_payment_delay_days >= 0),
    late_payment_count INTEGER NOT NULL DEFAULT 0 CHECK (late_payment_count >= 0),
    total_shipments INTEGER NOT NULL DEFAULT 0 CHECK (total_shipments >= 0)
);