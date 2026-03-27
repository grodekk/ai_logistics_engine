SELECT
    cr.client_name,
    ROUND(
        SUM(r.total_route_cost * cr.shipments) / SUM(cr.shipments),
        2
    ) AS avg_cost_per_shipment
FROM clients_routes cr
JOIN routes_costs_total r ON cr.route_name = r.route_name
GROUP BY cr.client_name
HAVING SUM(cr.shipments) > 0
ORDER BY avg_cost_per_shipment DESC;