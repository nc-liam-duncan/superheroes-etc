DROP DATABASE IF EXISTS nc_heroes;
CREATE DATABASE nc_heroes;

DROP DATABASE IF EXISTS nc_heroes_test;
CREATE DATABASE nc_heroes_test;

-- \c nc_heroes

-- -- Create the teams table
-- CREATE TABLE teams (
--     team_id SERIAL PRIMARY KEY,
--     team_name VARCHAR(100),
--     formation_year INT
-- );

-- -- Create the superheroes table
-- CREATE TABLE superheroes (
--     superhero_id SERIAL PRIMARY KEY,
--     alias VARCHAR(100),
--     real_name VARCHAR(100),
--     is_identity_secret BOOLEAN,
--     image_url VARCHAR(500),
--     team_id INT REFERENCES teams(team_id)
-- );

-- -- Insert data into the teams table
-- INSERT INTO teams 
--     (team_name, formation_year) 
-- VALUES
--     ('X-Men', 1963),
--     ('Defenders', 1971),
--     ('Avengers', 1963),
--     ('Starjammers', 1977);

