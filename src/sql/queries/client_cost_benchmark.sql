WITH client_costs AS (
    SELECT cr.client_name,
           ROUND(SUM(r.total_route_cost * cr.shipments) / NULLIF(SUM(cr.shipments),0), 2) AS avg_cost
    FROM clients_routes cr
    JOIN routes_costs_total r
        ON cr.route_name = r.route_name
    GROUP BY cr.client_name
),
with_avg AS (
    SELECT *,
           AVG(avg_cost) OVER () AS overall_avg
    FROM client_costs
)
SELECT
    client_name,
    avg_cost,
    ROUND(overall_avg, 2) AS overall_avg,
    ROUND(avg_cost - overall_avg, 2) AS diff_from_avg,
    CASE
        WHEN avg_cost > overall_avg THEN 'above'
        ELSE 'below'
    END AS vs_avg
FROM with_avg
ORDER BY avg_cost DESC;