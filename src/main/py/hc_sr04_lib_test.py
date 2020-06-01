#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import Bluetin_Echo

from utils import local_timestamp_now

TRIGGER_PIN = 22
ECHO_PIN = 23
MAX_DISTANCE = 8  # Get really noisy over 3~4 meters
UNIT = u'm'

def measure_distance(temp_celcius=20):
    # Initialise Sensor with pins, speed of sound.
    speed_of_sound = 331.5 + ( 0.6 * temp_celcius )
    echo = Bluetin_Echo.Echo(TRIGGER_PIN, ECHO_PIN, speed_of_sound)
    # echo.default_unit(UNIT)  # causes 'TypeError: 'str' object is not callable'
    echo.max_distance(value=MAX_DISTANCE, unit=UNIT)
    
    # Measure Distance n times, return average.
    samples = 20
    result = echo.read(UNIT, samples)
    #result = echo.read()
    # Reset GPIO Pins.
    echo.stop()
    return result


if __name__ == "__main__":
    print("_" * 80)
    if len(sys.argv) > 1:
        n_loop = int( sys.argv[1] )
    else:
        n_loop = 1
    print(local_timestamp_now() + " - " + str(n_loop) + " loops to be performed...")
    
    d_min = 99999
    d_max = -1
    d_total = 0
    n_measures = 0

    for i in range(n_loop):
        d = measure_distance()
        if d!=0 and d<=MAX_DISTANCE:  # ignore measures out of interval [0 MAX_DISTANCE]
            n_measures = n_measures + 1
            if d<d_min:
                d_min = d
            if d>d_max:
                d_max = d
            d_total = d_total + d

        # Print result.
        if n_measures!=0:
            print(local_timestamp_now() + " - %.3f -> min-avg-max\t%.3f\t%.3f\t%.3f" % (d, d_min, d_total/n_measures, d_max))
            sys.stdout.flush()

    sys.stdout.flush()
    os.system("sudo /sbin/shutdown -P +1 &")

