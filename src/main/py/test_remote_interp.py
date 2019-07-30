#!/usr/bin/env python

import calendar
import datetime
import picamera
import socket
import sqlite3
import sys
# import pydevd  # If failing: "pip install pydevd"
import time
import tsl2561  # If failing: pip install: Adafruit_GPIO tsl2561 (and also RPi.GPIO ?)
from gpiozero import CPUTemperature  # If failing: "pip install gpiozero"


# path_to_pydevd = "home/pi/.local/bin/pydevd"  # found by 'find / -name pydevd'
# sys.path.append(path_to_pydevd)

# debugger_ip_address = "192.168.0.63"
# pydevd.settrace(debugger_ip_address, port=5678)

METEO_FOLDER = "/home/pi/meteo/"
DB_NAME = METEO_FOLDER + "meteo.db"


def epoch_now():
    return calendar.timegm(time.gmtime())


def is_multiple(value, mult):
    margin = 30  # 30
    if (int(value / margin) % (mult / margin)) == 0:
        return True
    else:
        return False


def value_CPU_temp():
    return CPUTemperature().temperature


def value_luminosity():
    tsl = tsl2561.TSL2561(debug=True)
    return tsl.lux()


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
    CAPTURES_FOLDER = METEO_FOLDER + "captures/"
    captured_sucess = False
    capture_tentatives = 0
    while captured_sucess==False and capture_tentatives<10:
        capture_tentatives = capture_tentatives + 1
        try:
            camera = picamera.PiCamera()
            camera.resolution = (1296, 972)  # binned mode below 1296x972
            # camera.resolution = (1920, 1080)  # FullHD (unbinned)
            # camera.resolution = (2592, 1944)  # Max. resolution
            camera.start_preview()
            time.sleep(5)
            dt_now = datetime.datetime.utcfromtimestamp(epoch_now()).isoformat().replace(':', '-')
            filename = CAPTURES_FOLDER + "camera1_" + dt_now + ".jpg"
            print(filename)
            camera.capture(filename)
            camera.stop_preview()
            captured_sucess=True
        except picamera.exc.PiCameraMMALError:
            sys.stdout.write(".")
            time.sleep(capture_tentatives)

    if captured_sucess == False:
        print("failed " + capture_tentatives + " times to take picture. Gave up!")


def main():  # Expected to be called once per minute
    main_call_epoch = epoch_now()
    print(datetime.datetime.utcfromtimestamp(main_call_epoch).isoformat() + "\tStarting on " + socket.gethostname())

    # Connect or Create DB File
    conn = sqlite3.connect(DB_NAME)
    curs = conn.cursor()
    
    sensor = "CPU_temp"
    period = 900
    raw_table = "raw_measures_" + sensor
    consolidated_table = "consolidated" + str(period) + "_measures_" + sensor

    sql_insert = "INSERT INTO " + raw_table + "(epochtimestamp,value) VALUES(?,?);"
    measure = (epoch_now(), value_CPU_temp())
    curs.execute(sql_insert, measure)

    print("Added value for " + sensor + "; commiting...")
    conn.commit()
    
    sensor = "luminosity"
    period = 900
    raw_table = "raw_measures_" + sensor
    consolidated_table = "consolidated" + str(period) + "_measures_" + sensor

    sql_insert = "INSERT INTO " + raw_table + "(epochtimestamp,value) VALUES(?,?);"
    measure = (epoch_now(), value_luminosity())
    curs.execute(sql_insert, measure)

    print("Added value for " + sensor + "; commiting...")
    conn.commit()

    
    is300mult = is_multiple(main_call_epoch, 300)  # is True every 5 minutes (300 s.)
    if is300mult:
        print("Once every 5 minutes: Capture picture")
        take_picture()
    
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
    print(datetime.datetime.utcfromtimestamp(epoch_now()).isoformat() + " - Terminates " + "_"*47)


if __name__ == "__main__":
    main()
