-- sudo apt install sqlite3
-- sqlite3 /home/pi/meteo/meteo.db


BEGIN;
CREATE TABLE sensors
    (   names           TEXT,
        cumulative      BOOLEAN,  -- ie: True for mm of water, false for temperature
        unit            TEXT,
        consolidated    TEXT
    );
COMMIT;

BEGIN;
INSERT INTO sensors VALUES('CPU_temp', 'false', '°C', '900'); -- later, consolidated should be like '900 86400'
CREATE TABLE raw_measures_CPU_temp
    (   epochtimestamp  INTEGER,  -- seconds since 1970/01/01, https://www.sqlite.org/draft/lang_datefunc.html
        value           REAL
    );
CREATE TABLE consolidated900_measures_CPU_temp  -- consolidated on period of 900 s. (=15 minutes)
    (   minepochtime    INTEGER,
        maxepochtime    INTEGER,
        num_values      INTEGER,
        minvalue        REAL,
        maxvalue        REAL,
        meanvalue       REAL,
        totalvalues     REAL
    );
-- CREATE TABLE consolidated86400_measures_CPU_temp  -- consolidated on period of 86400 s. (=1 day)
--     (   minepochtime    INTEGER,
--         maxepochtime    INTEGER,
--         num_values      INTEGER,
--         minvalue        REAL,
--         maxvalue        REAL,
--         meanvalue       REAL,
--         totalvalues     REAL
--     );
COMMIT;





-- For each new sensor:
INSERT INTO sensors VALUES('luminosity', 'false', 'lux', '900'); -- later, consolidated should be like '900 86400'
CREATE TABLE raw_measures_luminosity
    (   epochtimestamp  INTEGER,  -- seconds since 1970/01/01, https://www.sqlite.org/draft/lang_datefunc.html
        value           REAL
    );
CREATE TABLE consolidated900_measures_luminosity  -- consolidated on period of 900 s. (=15 minutes)
    (   minepochtime    INTEGER,
        maxepochtime    INTEGER,
        num_values      INTEGER,
        minvalue        REAL,
        maxvalue        REAL,
        meanvalue       REAL,
        totalvalues     REAL
    );


