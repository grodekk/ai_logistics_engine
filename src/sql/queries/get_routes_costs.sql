SELECT route_name,
    fuel,
    tolls,
    ferry,
    hotel,
    fuel + tolls + ferry + hotel AS total_route_cost
FROM routes_costs;