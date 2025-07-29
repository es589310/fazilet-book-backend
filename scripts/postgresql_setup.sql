-- PostgreSQL database setup script
-- Bu scripti PostgreSQL-də işə salmaq üçün istifadə edin

-- Database yaradın
CREATE DATABASE kitab_db;

-- İstifadəçi yaradın (əgər yoxdursa)
CREATE USER kitab_user WITH PASSWORD 'kitab_password_123';

-- İcazələr verin
GRANT ALL PRIVILEGES ON DATABASE kitab_db TO kitab_user;

-- Database-ə qoşulun
\c kitab_db;

-- İstifadəçiyə schema icazələri verin
GRANT ALL ON SCHEMA public TO kitab_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO kitab_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO kitab_user;

-- Gələcək cədvəllər üçün icazələr
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO kitab_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO kitab_user;

-- Database məlumatlarını yoxlayın
SELECT current_database(), current_user;

-- Əlaqə məlumatları:
-- Host: localhost
-- Port: 5432
-- Database: kitab_db
-- Username: kitab_user
-- Password: kitab_password_123
