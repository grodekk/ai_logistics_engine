SELECT c.client_name
FROM clients c
LEFT JOIN clients_routes cr ON c.client_name = cr.client_name
WHERE cr.client_name IS NULL;