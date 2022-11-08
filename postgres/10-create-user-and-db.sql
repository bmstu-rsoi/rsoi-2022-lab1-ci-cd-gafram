-- file: 10-create-user-and-db.sql
CREATE DATABASE persons;
CREATE ROLE program WITH PASSWORD 'test';
GRANT ALL PRIVILEGES ON DATABASE persons TO program;
ALTER ROLE program WITH LOGIN;

CREATE TABLE persons
(
    "Id" SERIAL PRIMARY KEY,
    "Name" VARCHAR(30),
    "Age" INTEGER,
    "Work" VARCHAR(30),
    "Address" VARCHAR(50)
);