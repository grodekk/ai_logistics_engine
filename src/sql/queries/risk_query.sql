WITH risk_classified AS (
    SELECT
        c.client_name,
        c.avg_payment_delay_days,
        c.late_payment_count,
        CASE
            WHEN c.avg_payment_delay_days > 30
                 AND c.late_payment_count > 10  THEN 'CRITICAL'
            WHEN c.avg_payment_delay_days > 30
                 AND c.late_payment_count <= 10 THEN 'HIGH'
            WHEN c.avg_payment_delay_days > 10
                 AND c.late_payment_count > 3   THEN 'HIGH'
            WHEN c.avg_payment_delay_days > 0
                 OR  c.late_payment_count > 0   THEN 'MEDIUM'
            ELSE                                     'LOW'
        END AS risk_level
    FROM clients c
)
SELECT
    client_name,
    avg_payment_delay_days,
    late_payment_count,
    risk_level
FROM risk_classified
ORDER BY
    CASE risk_level
        WHEN 'CRITICAL' THEN 1
        WHEN 'HIGH'     THEN 2
        WHEN 'MEDIUM'   THEN 3
        ELSE                 4
    END;