#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from math import pi

import home_web.db_module as db_module
import sensors_functions
import utils

# todo Below variables should be stored in config file ~/.config/meteo.conf
TRIGGER_PIN = 22
ECHO_PIN = 23
MAX_DISTANCE = 800  # Get really noisy over 3~4 meters
UNIT = u'cm'


def volume_water_tank(distance_cm):
    """Return volume in Litre from the height in centimeter, for a circular/conical water tank.
    Sensor measures the distance from a certain height to the surface of water, looking down."""
    # Constants for the tank:
    r_max = 6.5  # Internal radius at very top of the tank, in dm
    d_min = 0.5  # Distance from the sensor to the very top of the tank, in dm
    r_base = 5.2  # Internal radius at the very bottom of the tank (base), in dm
    d_max = 12.5  # Distance from the sensor to the very bottom of the tank (when water volume is considered to be 0L)

    h = d_max - distance_cm / 10  # height of water, in dm
    pct_filling = h / (d_max - d_min)  # Percentage of fulfilling of the tank
    # (0 -> at r_base level, 1 -> at r_max level)
    r_top = r_base * (1. - pct_filling)\
        + r_max * pct_filling   # Radius of surface of water
    volume = h * (pi / 3) * (r_base*r_base + r_top*r_base + r_top*r_top)
    return volume


def measure_distance(temp_celcius=20):
    # TODO Move this method to sensors_function.py
    Bluetin_Echo = __import__("Bluetin_Echo")
    # Initialise Sensor with pins, speed of sound.
    speed_of_sound = 331.5 + (0.6 * temp_celcius)
    echo = Bluetin_Echo.Echo(TRIGGER_PIN, ECHO_PIN, speed_of_sound)
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
        insert_query = "INSERT INTO raw_measures VALUES("\
                       + str(timestamp) + "," \
                       + str(sensors_functions.round_value_decimals(measure, decimals)) + ", '" \
                       + sensor_short_name + "');"
        # + str(measure) + ", '"
        curs.execute(insert_query)
        conn.commit()
    except Exception as error:
        print(error)
        print("Error while creating PostgreSQL table", error)
    finally:
        # closing database connection.
        if (conn):
            curs.close()
            conn.close()
            print("PostgreSQL connection is closed")


if __name__ == "__main__":
    print("_" * 80)
    if len(sys.argv) > 1:
        n_loop = int( sys.argv[1] )
    else:
        n_loop = 1
    print(utils.local_timestamp_now() + " - " + str(n_loop) + " loops to be performed...")

    d_min = 99999.9
    d_max = -1.0
    d_total = 0.0
    n_measures = 0

    for i in range(n_loop):
        d = measure_distance()
        if d != 0. and d <= MAX_DISTANCE:  # ignore measures out of interval [0 MAX_DISTANCE]
            n_measures = n_measures + 1
            if d < d_min:
                d_min = d
            if d > d_max:
                d_max = d
            d_total = d_total + d

        # Print result.
        if n_measures != 0:
            print(utils.local_timestamp_now() + " - %.3f -> min-avg-max\t%.3f\t%.3f\t%.3f\t\tvolume = %.3f L" % (d, d_min, d_total/n_measures, d_max, volume_water_tank(d)))

            insert_raw_measures(utils.epoch_now(), d, u'WaterRes')

            sys.stdout.flush()

    sys.stdout.flush()
    # time.sleep(1)
    # os.system("sudo /sbin/shutdown -P now &")
    exit(0)
