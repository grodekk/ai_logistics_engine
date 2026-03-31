WITH route_costs AS (
    SELECT
        cr.client_name,
        cr.route_name,
        SUM(r.total_route_cost * cr.shipments) AS route_cost
    FROM clients_routes cr
    JOIN routes_costs_total r
        ON cr.route_name = r.route_name
    GROUP BY cr.client_name, cr.route_name
),
ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY client_name
            ORDER BY route_cost DESC
        ) AS rn
    FROM route_costs
)
SELECT
    client_name,
    route_name,
    route_cost
FROM ranked
WHERE rn = 1;