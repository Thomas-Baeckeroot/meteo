#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import calendar
# import datetime
import picamera
import psycopg2  # ProgreSQL library
import socket
# import sqlite3
import sys
# import pydevd  # If failing: "pip install pydevd"
import time
# import tsl2561  # If failing: pip install: Adafruit_GPIO tsl2561 (and also RPi.GPIO ?)
# from gpiozero import CPUTemperature  # If failing: "pip install gpiozero"
# import Adafruit_BMP.BMP085 as BMP085

import sensors_functions as func
import utils
import start_cpu_fan
import Bluetin_Echo
import hc_sr04_lib_test

# path_to_pydevd = "home/pi/.local/bin/pydevd"  # found by 'find / -name pydevd'
# sys.path.append(path_to_pydevd)

# debugger_ip_address = "192.168.0.63"
# pydevd.settrace(debugger_ip_address, port=5678)

METEO_FOLDER = "/home/pi/meteo/"
# DB_NAME = METEO_FOLDER + "meteo.db"  # SQLite DB File
CAPTURES_FOLDER = METEO_FOLDER + "captures/"
CAMERA_ENABLED = True
CONSOLIDATE_VAL = False


def is_multiple(value, multiple):
    margin = 30  # 30 s is used as default (script should be launched once per minute)
    if (int(value / margin) % (multiple / margin)) == 0:
        return True
    else:
        return False


def consolidate_from_raw(curs, sensor, period):
    #    consolidate_from_raw(curs, "CPU_temp", 900)
    raw_table = "raw_measures_" + sensor
    consolidated_table = "consolidated" + str(period) + "_measures_" + sensor
    print("consolidate_from_raw:\n\traw_table = " + raw_table + "\n\tconsolidated_table = " + consolidated_table)

    sql_req = "SELECT MAX(epochtimestamp) FROM " + raw_table + ";"
    curs.execute(sql_req)
    max_epoch_from_raw = curs.fetchall()[0][0]

    sql_req = "SELECT MAX(maxepochtime) FROM " + consolidated_table + ";"
    curs.execute(sql_req)
    max_epoch_from_consolidated = curs.fetchall()[0][0]

    sql_req = "SELECT MIN(epochtimestamp) FROM " + raw_table + ";"
    curs.execute(sql_req)
    min_epoch_from_raw = curs.fetchall()[0][0]

    sql_req = "SELECT MIN(maxepochtime) FROM " + consolidated_table + ";"
    curs.execute(sql_req)
    min_epoch_from_consolidated = curs.fetchall()[0][0]

    # TODO Consolidation from raw values table must be done soon...


def take_picture():
    sys.stdout.write("Take picture:\t")
    captured_success = False
    capture_tentatives = 0
    while not captured_success and capture_tentatives < 23:
        capture_tentatives = capture_tentatives + 1
        try:
            camera = picamera.PiCamera()
            # camera.awb_mode = 'sunlight'
            # camera.awb_mode = 'cloudy'
            # camera.awb_mode = 'tungsten'
            camera.awb_mode = 'off'
            # camera.awb_gains = (0.9, 1.9)  # Default (red, blue); each between 0.0 and 8.0
            # camera.awb_gains = (2.0, 1.9) trop rouge
            camera.awb_gains = (1.6, 1.0)
            # camera.awb_gains = (1.6, 1.9) pas assez vert?
            # camera.awb_gains = (1.4, 1.9) un peu trop bleu
            # camera.awb_gains = (1.0, 1.9) trop bleu
            camera.brightness = 46
            camera.resolution = (1296, 972)  # binned mode below 1296x972
            # camera.resolution = (1920, 1080)  # FullHD (unbinned)
            # camera.resolution = (2592, 1944)  # Max. resolution
            camera.start_preview()
            time.sleep(5)
            dt_now = utils.iso_timestamp4files()
            filename = CAPTURES_FOLDER + "camera1_" + dt_now + ".jpg"
            print(filename)
            camera.capture(filename)
            camera.stop_preview()
            camera.close()
            captured_success = True
        except picamera.exc.PiCameraMMALError:
            sys.stdout.write(".")
            time.sleep(capture_tentatives)

    if not captured_success:
        print("Failed " + str(capture_tentatives) + " times to take picture. Gave up!")


def main():  # Expected to be called once per minute
    main_call_epoch = utils.epoch_now()
    print(utils.iso_timestamp_now() + " - Starting on " + socket.gethostname() + "-----------------------------------")
    temp = 15  # default value for later calculation of speed of sound

    # conn = sqlite3.connect(DB_NAME)  # Connect or Create SQLite DB File
    conn = psycopg2.connect(database="meteo")  # Connect to PostgreSQL DB
    curs = conn.cursor()

    # name   | priority |        sensor_label         | decimals | cumulative | unit | consolidated | sensor_type
    read_sensors_query = "SELECT name, decimals, consolidated, sensor_type FROM sensors;"
    curs.execute(read_sensors_query)
    sensors = curs.fetchall()
    for sensor in sensors:
        (sensor_name, decimals, consolidated, sensor_type) = sensor

        measure = None
        # Below ifs to be replaced by function blocks and dictionary as described
        # at https://stackoverflow.com/questions/11479816/what-is-the-python-equivalent-for-a-case-switch-statement
        if sensor_type == "ignored":
            print("Ignoring sensor '" + sensor_name + "'...")
            # measure = None  # kept as None

        elif sensor_type == "CPU_temp":
            measure = func.value_cpu_temp()
            # if measure > 40:
            #     start_cpu_fan.start_cpu_fan()
            # if measure < 20:
            #     start_cpu_fan.stop_cpu_fan()

        elif sensor_type == "temperature":
            temp = func.value_ext_temperature()
            measure = temp

        elif sensor_type == "pressure":
            measure = func.value_sealevelpressure()

        elif sensor_type == "luminosity":
            measure = func.value_luminosity()

        elif sensor_type == "distance":
            # Calculate speed (celerity) of sound:
            measure = hc_sr04_lib_test.measure_distance(temp)

        else:
            print("ERROR! Unable to interpret '" + sensor_type + "' as a sensor type! Ignoring sensor '" + sensor_name
                  + "'...")
            # measure = None  # kept as None

        if measure is not None:
            print("sensor '" + sensor_name + "' -> " + str(measure))
            # sql_insert = "INSERT INTO " + raw_table + "(epochtimestamp,value) VALUES(?,?);"
            # curs.execute(sql_insert, measure)  # not supported by PostgreSQL ?
            sql_insert = "INSERT INTO raw_measures(epochtimestamp, measure, sensor) VALUES(" \
                         + str(utils.epoch_now()) + "," \
                         + str(func.round_value_decimals(measure, decimals)) + ", '" \
                         + sensor_name + "');"
            curs.execute(sql_insert)

            print("Added value for " + sensor_name + "; committing...")
            conn.commit()

    # end of for-loop on each sensor

    if CAMERA_ENABLED:
        is_camera_mult = is_multiple(main_call_epoch, 900)  # is True every 900 s / 15 min
        if is_camera_mult:
            print("Once every 15 minutes: Capture picture")
            take_picture()

    if CONSOLIDATE_VAL:
        for sensor in sensors:
            (sensor_name, decimals, consolidated, sensor_type) = sensor
            period = int(consolidated)
            sql_req = "SELECT MAX(epochtimestamp) FROM raw_measures WHERE sensor = '" + sensor_name + "';"
            curs.execute(sql_req)
            max_epoch_from_raw = curs.fetchall()[0][0]

            sql_req = "SELECT MAX(maxepochtime) FROM consolidated_measures WHERE sensor = '" + sensor_name + "';"
            curs.execute(sql_req)
            max_epoch_from_consolidated = curs.fetchall()[0][0]

            if (max_epoch_from_consolidated is None) or (max_epoch_from_consolidated + period) < max_epoch_from_raw:
                consolidate_from_raw(curs, sensor, period)

    # print("closing cursor...")
    curs.close()

    # Close DB
    # print("closing db...")
    conn.close()

    is_daily_run = is_multiple(main_call_epoch, 86400)  # 60x60x24 s = 1 day
    if is_daily_run:
        print("Midnight run: trigger the pictures sorting...")
        # launch_daily_jobs(main_call_epoch)
    else:
        print("(not midnight run)")

    print(utils.iso_timestamp_now() + " - Terminates " + "_" * 47)


if __name__ == "__main__":
    main()
