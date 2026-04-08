CREATE OR REPLACE VIEW routes_costs_total AS
SELECT
    route_name,
    fuel + tolls + ferry + hotel AS total_route_cost
FROM routes_costs;