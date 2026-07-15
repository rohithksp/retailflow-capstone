-- Create masking policy
CREATE MASKING POLICY mask_email
WITH (email VARCHAR(150))
USING ('***MASKED***'::VARCHAR);

-- Create restricted analyst user and role
CREATE USER analyst_user PASSWORD 'Analyst$2026!';
CREATE ROLE restricted_analyst;
GRANT ROLE restricted_analyst TO analyst_user;

-- Attach masking policy to PII table
ATTACH MASKING POLICY mask_email
ON customer_pii (email)
TO ROLE restricted_analyst
PRIORITY 10;

-- Grant access
GRANT SELECT ON customer_pii TO analyst_user;

-- Test masking
SET SESSION AUTHORIZATION analyst_user;
SELECT customer_id, customer_name, email FROM customer_pii ORDER BY customer_id;
RESET SESSION AUTHORIZATION;
