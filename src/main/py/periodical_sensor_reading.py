#!/usr/bin/env python

# import calendar
# import datetime
import picamera
import socket
import sqlite3
import sys
# import pydevd  # If failing: "pip install pydevd"
import time
# import tsl2561  # If failing: pip install: Adafruit_GPIO tsl2561 (and also RPi.GPIO ?)
# from gpiozero import CPUTemperature  # If failing: "pip install gpiozero"
# import Adafruit_BMP.BMP085 as BMP085

import sensors_functions as func
import utils
import start_cpu_fan

# path_to_pydevd = "home/pi/.local/bin/pydevd"  # found by 'find / -name pydevd'
# sys.path.append(path_to_pydevd)

# debugger_ip_address = "192.168.0.63"
# pydevd.settrace(debugger_ip_address, port=5678)

METEO_FOLDER = "/home/pi/meteo/"
DB_NAME = METEO_FOLDER + "meteo.db"
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
    while captured_success == False and capture_tentatives < 23:
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

    # Connect or Create DB File
    conn = sqlite3.connect(DB_NAME)
    curs = conn.cursor()

    sensor = "CPU_temp"
    period = 900
    raw_table = "raw_measures_" + sensor
    consolidated_table = "consolidated" + str(period) + "_measures_" + sensor

    sql_insert = "INSERT INTO " + raw_table + "(epochtimestamp,value) VALUES(?,?);"
    cpu_temp = func.value_CPU_temp()
    measure = (utils.epoch_now(), cpu_temp)
    curs.execute(sql_insert, measure)

    print("Added value for " + sensor + "; commiting...")
    conn.commit()
    # if cpu_temp > 40:
    #     start_cpu_fan.start_cpu_fan()
    # if cpu_temp < 20:
    #     start_cpu_fan.stop_cpu_fan()

    # Next sensor:
    sensor = "luminosity"
    period = 900
    raw_table = "raw_measures_" + sensor
    consolidated_table = "consolidated" + str(period) + "_measures_" + sensor

    sql_insert = "INSERT INTO " + raw_table + "(epochtimestamp,value) VALUES(?,?);"

    try:
        measure = (utils.epoch_now(), func.value_luminosity())
        curs.execute(sql_insert, measure)
        print("Added value for " + sensor + "; commiting...")
        conn.commit()
    except IOError:
        print("IOError occurred when reading " + sensor + "!")

    # Next sensor:
    sensor1 = "temperature"
    sensor2 = "pressure"
    period = 900
    raw_table1 = "raw_measures_" + sensor1
    raw_table2 = "raw_measures_" + sensor2
    consolidated_table1 = "consolidated" + str(period) + "_measures_" + sensor1
    consolidated_table2 = "consolidated" + str(period) + "_measures_" + sensor2

    sql_insert1 = "INSERT INTO " + raw_table1 + "(epochtimestamp,value) VALUES(?,?);"
    sql_insert2 = "INSERT INTO " + raw_table2 + "(epochtimestamp,value) VALUES(?,?);"

    try:
        (temp, sealevelpressure) = func.value_temp_and_sealevelpressure()
        measure1 = (utils.epoch_now(), temp)
        measure2 = (utils.epoch_now(), sealevelpressure)
        curs.execute(sql_insert1, measure1)
        curs.execute(sql_insert2, measure2)

        print("Added value for " + sensor1 + " and " + sensor2 + "; commiting...")
        conn.commit()
    except IOError:
        print("IOError occurred when reading " + sensor1 + " and " + sensor2 + "!")

    if CAMERA_ENABLED:
        is300mult = is_multiple(main_call_epoch, 900)  # is True every 5 minutes (300 s.)
        if is300mult:
            print("Once every 5 minutes: Capture picture")
            take_picture()

    if CONSOLIDATE_VAL:
        sql_req = "SELECT MAX(epochtimestamp) FROM " + raw_table + ";"
        curs.execute(sql_req)
        max_epoch_from_raw = curs.fetchall()[0][0]

        sql_req = "SELECT MAX(maxepochtime) FROM " + consolidated_table + ";"
        curs.execute(sql_req)
        max_epoch_from_consolidated = curs.fetchall()[0][0]

        if (max_epoch_from_consolidated is None) or (max_epoch_from_consolidated + period) < max_epoch_from_raw:
            consolidate_from_raw(curs, sensor, period)

    # print("closing cursor...")
    curs.close()

    # Close DB
    # print("closing db...")
    conn.close()
    print(utils.iso_timestamp_now() + " - Terminates " + "_" * 47)


if __name__ == "__main__":
    main()
