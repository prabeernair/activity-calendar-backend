-- DROP DATABASE activity_calendar;
CREATE DATABASE activity_calendar;
\connect activity_calendar;

-- DROP TABLE users;
CREATE TABLE users (
  id                 SERIAL         PRIMARY KEY,
  name               VARCHAR(255),
  email              VARCHAR(255)   UNIQUE NOT NULL,
  magic_link         CHAR(32)       UNIQUE NOT NULL,
  created_at         TIMESTAMP      NOT NULL,
  last_logged_in_at  TIMESTAMP      NOT NULL
);

-- @todo: CREATE TABLE activities
