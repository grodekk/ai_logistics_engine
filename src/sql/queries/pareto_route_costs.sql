WITH route_totals AS (
    SELECT r.route_name,
           SUM(r.total_route_cost * cr.shipments) AS total_cost
    FROM routes_costs_total r
    JOIN clients_routes cr ON r.route_name = cr.route_name
    GROUP BY r.route_name
)
SELECT route_name,
       total_cost,
       SUM(total_cost) OVER (ORDER BY total_cost DESC) AS cumulative_cost,
       ROUND(SUM(total_cost) OVER (ORDER BY total_cost DESC) * 100.0 /
             SUM(total_cost) OVER (), 2) AS cumulative_pct
FROM route_totals
ORDER BY total_cost DESC;