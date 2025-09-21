-- Initialize PostgreSQL database for the data pipeline

-- Create database if it doesn't exist (this might not be needed in docker-entrypoint-initdb.d)
-- The database creation is handled by the POSTGRES_DB environment variable

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant permissions (if needed)
GRANT ALL PRIVILEGES ON DATABASE pipeline_db TO pipeline_user;