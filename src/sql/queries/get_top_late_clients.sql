SELECT client_name,
       late_payment_count
FROM clients
ORDER BY late_payment_count DESC
LIMIT 3;