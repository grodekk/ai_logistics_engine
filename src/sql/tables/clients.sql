CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY,
    client_name TEXT NOT NULL,
    client_class TEXT NOT NULL,
    avg_payment_delay_days INTEGER DEFAULT 0,
    late_payment_count INTEGER DEFAULT 0,
    total_shipments INTEGER DEFAULT 0
);