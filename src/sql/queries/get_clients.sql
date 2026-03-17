SELECT client_name,
    client_class,
    COALESCE(avg_payment_delay_days, 0) AS avg_payment_delay_days,
    COALESCE(late_payment_count, 0) AS late_payment_count,
    COALESCE(total_shipments, 0) AS total_shipments
FROM clients