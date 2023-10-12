#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from math import pi

import home_web.db_module as db_module
import logging
import sensors_functions
import utils

logging.basicConfig(
    filename=utils.get_home() + "/meteo/logfile.log",
    level=logging.DEBUG,
    format='%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s')
log = logging.getLogger("hc_sr04_lib_test.py")

import logging

logging.basicConfig(
    filename=utils.get_home() + "/meteo/logfile.log",
    level=logging.DEBUG,
    format='%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s')
log = logging.getLogger("hc_sr04_lib_test.py")

# todo Below variables should be stored in config file ~/.config/meteo.conf
TRIGGER_PIN = 19
ECHO_PIN = 13
MAX_DISTANCE = 400  # Get really noisy over 3~4 meters
UNIT = u'cm'


def volume_water_tank(distance_cm):
    """Return volume in Litre from the height in centimeter, for a circular/conical water tank.
    Sensor measures the distance from a certain height to the surface of water, looking down."""
    # Constants for the tank:
    r_max = 6.5  # Internal radius at very top of the tank, in dm
    d_min = 1.5  # Distance from the sensor to the very top of the tank, in dm
    r_base = 5.2  # Internal radius at the very bottom of the tank (base), in dm
    d_max = 9.144  # Distance from the sensor to the very bottom of the tank (when water volume is considered to be 0L)

    h = d_max - distance_cm / 10  # height of water, in dm
    pct_filling = h / (d_max - d_min)  # Percentage of fulfilling of the tank
    # (0 -> at r_base level, 1 -> at r_max level)
    r_top = r_base * (1. - pct_filling) \
            + r_max * pct_filling  # Radius of surface of water
    volume = h * (pi / 3) * (r_base * r_base + r_top * r_base + r_top * r_top)
    return volume


def measure_distance_once(temp_celcius=20):
    trigger_gpio = TRIGGER_PIN
    echo_gpio = ECHO_PIN
    # TODO Move this method to sensors_function.py
    Bluetin_Echo = __import__("Bluetin_Echo")
    # Initialise Sensor with pins, speed of sound.
    speed_of_sound = 331.5 + (0.6 * temp_celcius)
    echo = Bluetin_Echo.Echo(trigger_gpio, echo_gpio, speed_of_sound)
    # echo.default_unit(UNIT)  # causes 'TypeError: 'str' object is not callable'
    echo.max_distance(value=MAX_DISTANCE, unit=UNIT)

    # Measure Distance n times, return average.
    samples = 20
    result = echo.read(UNIT, samples)
    # result = echo.read()
    # Reset GPIO Pins.
    echo.stop()
    return result


def insert_raw_measures(timestamp, measure, sensor_short_name):
    try:
        conn = db_module.get_conn()
        curs = conn.cursor()
        read_decimals_query = "SELECT decimals FROM sensors WHERE name = '" + sensor_short_name + "';"
        curs.execute(read_decimals_query)
        decimals = int(curs.fetchone()[0])
        insert_query = "INSERT INTO raw_measures VALUES(" \
                       + str(timestamp) + "," \
                       + str(sensors_functions.round_value_decimals(measure, decimals)) + ", '" \
                       + sensor_short_name + "');"
        # + str(measure) + ", '"
        curs.execute(insert_query)
        conn.commit()
    except Exception as error:
        log.exception("Error while creating PostgreSQL table")
    finally:
        # closing database connection.
        if (conn):
            curs.close()
            conn.close()
            log.info("PostgreSQL connection is closed")


def measure_distance(temp_celcius=20, n_loop=10):
    measures = []
    log.debug(" value\t min  \t avg  \t max  \t vol.(L)\tVol(avg)")
    for i in range(n_loop):
        d = measure_distance_once(temp_celcius)
        if d == 0. or d > MAX_DISTANCE:  # ignore measures out of interval [0 MAX_DISTANCE]
            log.warning("Inconsistent measure '{0}' ignored.".format(d))
            n_loop = n_loop - 0.8  # Retry if unable to read, but not infinitely...
        else:
            measures.append(d)
            log.debug("%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f"
                    % (d, min(measures), sum(measures) / len(measures), max(measures),
                       volume_water_tank(d), volume_water_tank( sum(measures) / len(measures))))

    if len(measures) == 0:
        log.error("Unable to measure distance after multiple attempts.")
        return None
    else:
        return sum(measures) / len(measures)


if __name__ == "__main__":
    log.info("_" * 80)
    if len(sys.argv) > 1:
        n_loop = int(sys.argv[1])
    else:
        n_loop = 5
    log.info("{0} loops to be performed...".format(n_loop))

    measure_distance(20, n_loop)
    # sys.stdout.flush()
    exit(0)
