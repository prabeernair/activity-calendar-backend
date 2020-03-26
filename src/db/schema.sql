-- @see: https://www.postgresql.org/docs/12/

-- DROP DATABASE IF EXISTS activity_calendar;
CREATE DATABASE activity_calendar;
-- \connect activity_calendar;

-- DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
  id                 SERIAL         PRIMARY KEY,
  name               VARCHAR(255)   ,
  email              VARCHAR(255)   ,
  magic_link         UUID           UNIQUE NOT NULL,
  last_logged_in_at  TIMESTAMP      ,
  created_at         TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at         TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users VALUES (DEFAULT, 'Oleksii', NULL, 'e1fabafc-b024-41ca-b246-85e7f6b70a5a', NULL, DEFAULT, DEFAULT);
-- SELECT * FROM users;

-- DROP TABLE IF EXISTS activities;
CREATE TABLE activities (
  id                 SERIAL         PRIMARY KEY,
  user_id            INTEGER        NOT NULL,
  type               VARCHAR(255)   NOT NULL,
  duration           TSRANGE        NOT NULL,
  fields             JSONB          , -- arbitrary properties, relevant for specific types
  created_at         TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at         TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT activities_user_id_fkey FOREIGN KEY (user_id)
    REFERENCES users (id) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE CASCADE
);
