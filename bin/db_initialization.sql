-- sudo apt install sqlite3
-- sqlite3 /home/pi/meteo/meteo.db


BEGIN;
CREATE TABLE sensors
    (   names           TEXT,
        priority        INTEGER,  -- priority value: from 0 to 100; ie: 20 for main values (temp.)
        label           TEXT,
        decimals        INTEGER,  -- decimal places: 0 = rounded at unit, 1 = 1/10th of unit, ...
        cumulative      BOOLEAN,  -- ie: True for mm of water, false for temperature
        unit            TEXT,
        consolidated    TEXT  -- time-range (in s.) for consolidation; ie: 900 -> data consolidated per 15 minutes
    );
COMMIT;


-- DROP TABLE TempOldTable;
-- ALTER TABLE sensors RENAME TO TempOldTable;
-- CREATE TABLE sensors
--     (   names           TEXT,
--         priority        INTEGER,  -- priority value: from 0 to 100; ie: 20 for main values (temp.)
--         label           TEXT,
--         decimals        INTEGER,  -- decimal places: 0 = rounded at unit, 1 = 1/10th of unit, ...
--         cumulative      BOOLEAN,  -- ie: True for mm of water, false for temperature
--         unit            TEXT,
--         consolidated    TEXT  -- time-range (in s.) for consolidation; ie: 900 -> data consolidated per 15 minutes
--     );
-- INSERT INTO sensors (names, label, cumulative, unit, consolidated) SELECT names, label, cumulative, unit, consolidated FROM TempOldTable;
-- UPDATE sensors SET decimals=1 WHERE names="CPU_temp";

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


INSERT INTO sensors VALUES('temperature', 'false', '°C', '900'); -- later, consolidated should be like '900 86400'
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

    
INSERT INTO sensors VALUES('pressure', 'false', 'hPa', '900'); -- later, consolidated should be like '900 86400'
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
