-- @see: https://www.postgresql.org/docs/12/datatype.html

-- DROP DATABASE IF EXISTS activity_calendar;
CREATE DATABASE activity_calendar;
\connect activity_calendar;

-- DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id                 SERIAL         PRIMARY KEY,
  name               VARCHAR(255)   ,
  email              VARCHAR(255)   UNIQUE NOT NULL,
  magic_link         UUID           UNIQUE NOT NULL,
  last_logged_in_at  TIMESTAMP      NOT NULL,
  created_at         TIMESTAMP      NOT NULL,
  updated_at         TIMESTAMP      NOT NULL
);

-- DROP TABLE IF EXISTS activities;
CREATE TABLE activities (
  id                 SERIAL         PRIMARY KEY,
  user_id            INTEGER        NOT NULL,
  type               VARCHAR(255)   NOT NULL,
  fields             JSONB          , -- arbitrary properties (e.g. "distance" or "surface"), relevant for specific types
  started_at         TIMESTAMP      NOT NULL,
  duration           TSRANGE        NOT NULL,
  created_at         TIMESTAMP      NOT NULL,
  updated_at         TIMESTAMP      NOT NULL,
  CONSTRAINT activities_user_id_fkey FOREIGN KEY (user_id)
    REFERENCES users (id) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE CASCADE
);
