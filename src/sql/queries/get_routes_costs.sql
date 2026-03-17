SELECT route_name,
    COALESCE(fuel, 0) AS fuel,
    COALESCE(tolls, 0) AS tolls,
    COALESCE(ferry, 0) AS ferry,
    COALESCE(hotel, 0) AS hotel,
    COALESCE(fuel, 0) + COALESCE(tolls, 0) + COALESCE(ferry, 0) + COALESCE(hotel, 0) AS total_route_cost
FROM routes_costs;