SELECT
    (
        (SELECT total_fixed_costs
         FROM fixed_costs_total)
        +
        COALESCE(
            (
                SELECT SUM(r.total_route_cost * cr.shipments)
                FROM clients_routes cr
                JOIN routes_costs_total r
                    ON cr.route_name = r.route_name
            ),
            0
        )
    ) AS total_monthly_expenses;