SELECT
    c.client_name,
    c.client_class,
    c.avg_payment_delay_days,
    c.late_payment_count,
    COALESCE(SUM(cr.shipments), 0) AS total_shipments
FROM clients c
LEFT JOIN clients_routes cr
    ON cr.client_name = c.client_name
GROUP BY
    c.client_name,
    c.client_class,
    c.avg_payment_delay_days,
    c.late_payment_count
ORDER BY c.client_name;