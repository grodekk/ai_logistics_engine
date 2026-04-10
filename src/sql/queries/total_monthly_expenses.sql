SELECT
    (SELECT total_fixed_costs FROM fixed_costs_total)
    +
    (SELECT SUM(r.total_route_cost * cr.shipments)
     FROM clients_routes cr
     JOIN routes_costs_total r ON cr.route_name = r.route_name)
    AS total_monthly_expenses;