WITH route_totals AS (
    SELECT
           r.route_name,
           SUM(r.total_route_cost * cr.shipments) AS route_cost
    FROM routes_costs_total r
    JOIN clients_routes cr ON cr.route_name = r.route_name
    GROUP BY r.route_name
)
SELECT
       route_name,
       route_cost,
       ROUND(route_cost * 100.0 / SUM(route_cost) OVER (), 2) AS cost_share_pct
FROM route_totals
ORDER BY cost_share_pct DESC;