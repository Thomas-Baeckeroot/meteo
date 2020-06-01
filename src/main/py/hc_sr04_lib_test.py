#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import Bluetin_Echo
import psycopg2  # ProgreSQL
import time

import sensors_functions
import utils

TRIGGER_PIN = 22
ECHO_PIN = 23
MAX_DISTANCE = 8  # Get really noisy over 3~4 meters
UNIT = u'cm'


def measure_distance(temp_celcius=20):
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
        connection = psycopg2.connect(database="meteo")
        curs = connection.cursor()
        read_decimals_query = "SELECT decimals FROM SENSORS WHERE names = '" + sensor_short_name + "';"
        curs.execute(read_decimals_query)
        decimals = int(curs.fetchone()[0])
        insert_query = "INSERT INTO raw_measures VALUES("\
                       + str(timestamp) + "," \
                       + str(sensors_functions.round_value_decimals(measure, decimals)) + ", '" \
                       + sensor_short_name + "');"
        # + str(measure) + ", '"
        curs.execute(insert_query)
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        print("Error while creating PostgreSQL table", error)
    finally:
        # closing database connection.
        if (connection):
            curs.close()
            connection.close()
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
            print(utils.local_timestamp_now() + " - %.3f -> min-avg-max\t%.3f\t%.3f\t%.3f" % (d, d_min, d_total/n_measures, d_max))

            insert_raw_measures(utils.epoch_now(), d, u'WaterRes')

            sys.stdout.flush()

    sys.stdout.flush()
    # time.sleep(1)
    # os.system("sudo /sbin/shutdown -P now &")
    exit(0)
