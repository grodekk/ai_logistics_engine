CREATE VIEW fixed_costs_total AS
SELECT
    SUM(amount) AS total_fixed_costs
FROM monthly_costs;