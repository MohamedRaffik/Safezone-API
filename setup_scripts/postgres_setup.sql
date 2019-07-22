DROP TABLE IF EXISTS crimes_by_station;
DROP TABLE IF EXISTS crime_info;
DROP TABLE IF EXISTS stations;
DROP TABLE IF EXISTS crime_categories;
DROP EXTENSION IF EXISTS postgis;

CREATE EXTENSION postgis;

CREATE TABLE crime_categories ( 
    id SERIAL PRIMARY KEY, 
    category TEXT, 
    risk_points INTEGER 
);

INSERT INTO crime_categories (category, risk_points) VALUES 
    ('Murder', 20),                
    ('Rape', 17), 
    ('Robbery', 14), 
    ('Felony Assault', 12),
    ('Burglary', 4),
    ('Grand Larceny', 10), 
    ('Petit Larceny', 4), 
    ('Misdemeanor Assault', 7),
    ('Misdemeanor Sex Crimes', 7), 
    ('Kidnapping', 17), 
    ('Offenses against Public Order', 2), 
    ('Shootings', 8);


CREATE TABLE crime_info ( 
    id SERIAL PRIMARY KEY, 
    category_id INTEGER REFERENCES crime_categories(id), 
    crime_date DATE, 
    pd_desc TEXT, 
    ofns_desc TEXT, 
    latitude FLOAT, 
    longitude FLOAT 
);

CREATE TABLE stations (
    id INTEGER PRIMARY KEY, 
    name TEXT, 
    line TEXT, 
    latitude FLOAT, 
    longitude FLOAT 
);

CREATE TABLE crimes_by_station (
    station_id INTEGER REFERENCES stations(id),
    crime_id INTEGER REFERENCES crime_info(id)
);
