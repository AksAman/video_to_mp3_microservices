-- POSTGRES

CREATE USER "auth_db_user" WITH PASSWORD 'auth_db_password';

CREATE DATABASE auth_db;

GRANT ALL PRIVILEGES ON DATABASE auth_db TO "auth_db_user";

