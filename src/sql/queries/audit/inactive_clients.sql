SELECT
    c.client_name,
    COALESCE(SUM(cr.shipments), 0) AS shipments
FROM clients c
LEFT JOIN clients_routes cr
    ON c.client_name = cr.client_name
GROUP BY c.client_name
HAVING COALESCE(SUM(cr.shipments), 0) = 0;