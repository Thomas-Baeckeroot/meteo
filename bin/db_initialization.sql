CREATE TABLE IF NOT EXISTS sensors
    (   name            VARBINARY(8),   -- (MariaDB)
    --  name  CHAR(8),  -- PRIMARY KEY" -- (PostgreSQL)
        priority        INTEGER,        -- priority value: from 0 to 100; ie: 20 for main values (temp.)
        sensor_label    TEXT,
        decimals        INTEGER,        -- decimal places: 0 = rounded at unit, 1 = 1/10th of unit, ...
        cumulative      BOOLEAN,        -- ie: True for mm of water, false for temperature
        unit            TEXT,
        consolidated    TEXT,           -- time-range (in s.) for consolidation; ie: 900 -> data consolidated per 15 minutes
        sensor_type     TEXT
        -- sensor_config  TEXT          -- ie 'GPIO23'
    );
CREATE TABLE raw_measures
    (   epochtimestamp  INTEGER,        -- seconds since 1970/01/01, https://www.sqlite.org/draft/lang_datefunc.html
        measure         REAL,
        sensor          VARBINARY(8),   -- (MariaDB) ( PostgreSQL: "sensor  CHAR(8),  -- REFERENCES sensors (name)" )
        synchronised    BOOLEAN DEFAULT false NOT NULL
        -- PRIMARY KEY (epochtimestamp, sensor)
    );
CREATE TABLE consolidated_measures
    (   minepochtime    INTEGER,
        maxepochtime    INTEGER,
        num_values      INTEGER,
        min_value       REAL,
        max_value       REAL,
        mean_value      REAL,
        total_values    REAL,
        sensor          VARBINARY(8),   -- REFERENCES sensors (name) (MariaDB)
    --  sensor          CHAR(8),        -- REFERENCES sensors (name) (PostgreSQL)
        period          INTEGER         -- period in seconds: =900 for 15 minutes periods
    );

-- INSERT INTO sensors VALUES('SensShortName' , p0_100, 'Sensor verbose texte'    , num_dec_0_2, false, 'Unit_cm', '900'); -- later, consolidated should be like '900 86400'
INSERT INTO sensors VALUES('CPU_temp', 10, 'Température CPU (centrale)' , 1, false, '°C' , '900', 'ignored');
INSERT INTO sensors VALUES('CPU_tmp1',  9, 'Température CPU (R0 grange)', 1, false, '°C' , '900', 'CPU_temp');
INSERT INTO sensors VALUES('WaterRes', 50, 'Réserve eau de pluie'       , 1, false, 'cm' , '900', 'water_height');
INSERT INTO sensors VALUES('lum_ext' , 70, 'Luminosité'                 , 0, false, 'lux', '900', 'ignored');
INSERT INTO sensors VALUES('temp_ext', 90, 'Température'                , 1, false, '°C' , '900', 'ignored');
INSERT INTO sensors VALUES('pressure', 80, 'Pression atmosphérique'     , 1, false, 'hPa', '900', 'ignored');


-- OLD TABLES (WITH ONE TABLE PER SENSOR)
BEGIN;
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
BEGIN;
CREATE TABLE raw_measures_luminosity
    (   epochtimestamp  INTEGER,  -- seconds since 1970/01/01, https://www.sqlite.org/draft/lang_datefunc.html
        value           REAL      -- INTEGER might be more compact in DB but REAL kept for consistency with other sensors
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
COMMIT;


BEGIN;
CREATE TABLE raw_measures_temperature
    (   epochtimestamp  INTEGER,  -- seconds since 1970/01/01, https://www.sqlite.org/draft/lang_datefunc.html
        value           REAL
    );
CREATE TABLE consolidated900_measures_temperature  -- consolidated on period of 900 s. (=15 minutes)
    (   minepochtime    INTEGER,
        maxepochtime    INTEGER,
        num_values      INTEGER,
        minvalue        REAL,
        maxvalue        REAL,
        meanvalue       REAL,
        totalvalues     REAL
    );
COMMIT;


BEGIN;
CREATE TABLE raw_measures_pressure
    (   epochtimestamp  INTEGER,  -- seconds since 1970/01/01, https://www.sqlite.org/draft/lang_datefunc.html
        value           REAL
    );
CREATE TABLE consolidated900_measures_pressure  -- consolidated on period of 900 s. (=15 minutes)
    (   minepochtime    INTEGER,
        maxepochtime    INTEGER,
        num_values      INTEGER,
        minvalue        REAL,
        maxvalue        REAL,
        meanvalue       REAL,
        totalvalues     REAL
    );
COMMIT;
