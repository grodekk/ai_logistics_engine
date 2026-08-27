SELECT
    rc.route_name,
    rc.fuel,
    rc.tolls,
    rc.ferry,
    rc.hotel,
    rct.total_route_cost
FROM routes_costs rc
JOIN routes_costs_total rct
    ON rct.route_name = rc.route_name
ORDER BY rc.route_name;