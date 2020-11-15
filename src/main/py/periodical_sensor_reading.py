#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import calendar
# import datetime
import picamera
# import psycopg2 as dbmodule  # ProgreSQL library
import mariadb as dbmodule  # ProgreSQL library
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

# todo Below variables should be stored in config file ~/.config/meteo.conf (GPIO numbers also could be informed there)
METEO_FOLDER = "/home/pi/meteo/"
# DB_NAME = METEO_FOLDER + "meteo.db"  # SQLite DB File
CAPTURES_FOLDER = METEO_FOLDER + "captures/"
CAMERA_NAME = "camera1"
CAMERA_ENABLED = True
CONSOLIDATE_VAL = False
main_call_epoch = utils.epoch_now()


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
            filename = CAPTURES_FOLDER + CAMERA_NAME + "_" + dt_now + ".jpg"
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


def copy_values_from_server(sensor_dest, remote_server_src, conn_local_dest):
    global main_call_epoch
    (sensor_name, sensor_label_dest, decimals_dest, cumulative_dest, unit_dest, consolidated_dest,
     sensor_type_dest) = sensor_dest
    conn_remote_src = dbmodule.connect(database="meteo", host=remote_server_src, )  # Connect to REMOTE PostgreSQL DB
    # FIXME Manage situation where remote is not reachable
    curs_src = conn_remote_src.cursor()

    # name   | priority |        sensor_label         | decimals | cumulative | unit | consolidated | sensor_type
    read_sensors_query = "SELECT sensor_label, decimals, cumulative, unit, consolidated" \
                         "  FROM sensors" \
                         " WHERE name='" + sensor_name + "';"
    curs_src.execute(read_sensors_query)
    (sensor_label_src, decimals_src, cumulative_src, unit_src, consolidated_src) = curs_src.fetchall()[0]
    print("sensor_label: \tsrc='" + sensor_label_src + "'\t>>> dest='" + sensor_label_dest + "'")
    if sensor_label_src != sensor_label_dest:
        curs_src.execute("UPDATE sensors"
                         "   SET sensor_label=" + sensor_label_src +
                         " WHERE name='" + sensor_name + "';")
    print("Decimals:     \tsrc='" + decimals_src + "'\t>>> dest='" + decimals_dest + "'")
    if decimals_src != decimals_dest:
        curs_src.execute("UPDATE sensors"
                         "   SET decimals=" + decimals_src +
                         " WHERE name='" + sensor_name + "';")
    print("cumulative: \tsrc='" + cumulative_src + "'\t>>> dest='" + cumulative_dest + "'")
    if cumulative_src != cumulative_dest:
        curs_src.execute("UPDATE sensors"
                         "   SET cumulative=" + cumulative_src +
                         " WHERE name='" + sensor_name + "';")
    print("unit: \tsrc='" + unit_src + "'\t>>> dest='" + unit_dest + "'")
    if unit_src != unit_dest:
        curs_src.execute("UPDATE sensors"
                         "   SET unit=" + unit_src +
                         " WHERE name='" + sensor_name + "';")
    print("consolidated: \tsrc='" + consolidated_src + "'\t>>> dest='" + consolidated_dest + "'")
    if consolidated_src != consolidated_dest:
        curs_src.execute("UPDATE sensors"
                         "   SET consolidated=" + consolidated_src +
                         " WHERE name='" + sensor_name + "';")

    n_updates = 99999
    # Loop as long as we got updates to synchronise and in the limit of 50s after start of this script
    # (to avoid possible concurrency with other instance that would copy the same data)
    while n_updates > 0 and (utils.epoch_now() - main_call_epoch) < 50:
        read_sensors_query = "SELECT epochtimestamp, measure" \
                             "  FROM raw_measures" \
                             " WHERE sensor='" + sensor_name + \
                             "'  AND synchronised='false' " \
                             "ORDER BY epochtimestamp asc FETCH FIRST 10 ROWS ONLY;"
        curs_src.execute(read_sensors_query)
        epochs_and_measures_from_src = curs_src.fetchall()
        n_updates = len(epochs_and_measures_from_src)
        if n_updates > 0:
            insert_measures_to_dest_query = "INSERT INTO raw_measures(epochtimestamp, measure, sensor) VALUES "
            for (epoch_src, measure_src) in epochs_and_measures_from_src:
                # = epoch_and_measure  # todo once working, should be included within for declaration
                insert_measures_to_dest_query = insert_measures_to_dest_query + \
                                                "(" + str(epoch_src) + ", " + str(measure_src) + ", " \
                                                + sensor_name + ")"
            insert_measures_to_dest_query = insert_measures_to_dest_query + ";"
            curs_dest = conn_local_dest.cursor()
            curs_dest.execute(insert_measures_to_dest_query)

            update_synchronised_query = "UPDATE raw_measures(synchronised)" \
                                        "   SET true" \
                                        " WHERE epoch IN("
            for (epoch_src, measure_src) in epochs_and_measures_from_src:
                update_synchronised_query = update_synchronised_query + str(epoch_src) + ", "
            update_synchronised_query = update_synchronised_query + ") AND sensor='" + sensor_name + "'"
            curs_src.execute(update_synchronised_query)

        print("Imported " + str(n_updates) + " records from " + remote_server_src)

    pass


def main():  # Expected to be called once per minute
    global main_call_epoch
    print(utils.iso_timestamp_now() + " - Starting on " + socket.gethostname() + " ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
    temp = 15  # default value for later calculation of speed of sound

    # conn = sqlite3.connect(DB_NAME)  # Connect or Create SQLite DB File
    conn = dbmodule.connect(database="meteo")  # Connect to PostgreSQL DB
    curs = conn.cursor()

    # name   | priority |        sensor_label         | decimals | cumulative | unit | consolidated | sensor_type
    read_sensors_query = "SELECT name, sensor_label, decimals, cumulative, unit, consolidated, sensor_type FROM sensors;"
    curs.execute(read_sensors_query)
    sensors = curs.fetchall()
    for sensor in sensors:
        (sensor_name, sensor_label, decimals, cumulative, unit, consolidated, sensor_type) = sensor
        sensor_name = sensor_name.decode('ascii')

        measure = None
        # Below ifs to be replaced by function blocks and dictionary as described
        # at https://stackoverflow.com/questions/11479816/what-is-the-python-equivalent-for-a-case-switch-statement
        if sensor_type == "ignored":
            print("Sensor '" + sensor_name + "' -> -ignoring-")
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

        elif sensor_type.startswith("remote:"):
            # Another remote PostgreSQL contains the measures. Those not "synchronised" will be copied
            # if having ~Connection refused~~port 5432?~ issues then
            #   -> On remote server, in file postgresql.conf, set "listen_addresses = '*'"
            # 
            #   -> in file pg_hba.conf, add "host    meteo           pi              192.168.0.94/32         trust"
            # (those 2 configuration files are usually in /etc/postgresql/11/main/ )
            # fixme the upper "trust" is not secured and should look for a decent unix authentication later...
            remote_server = sensor_type[7:]
            copy_values_from_server(sensor, remote_server, conn)

        else:
            print("Sensor '" + sensor_name + "' -> ERROR! Unable to interpret '" + str(sensor_type)
                  + "' as a sensor type! Skipped...")
            # measure = None  # kept as None

        if measure is not None:
            print("Sensor '" + sensor_name + "' -> " + str(measure))
            # sql_insert = "INSERT INTO " + raw_table + "(epochtimestamp,value) VALUES(?,?);"
            # curs.execute(sql_insert, measure)  # not supported by PostgreSQL ?
            sql_insert = "INSERT INTO raw_measures(epochtimestamp, measure, sensor) VALUES(" \
                         + str(utils.epoch_now()) + "," \
                         + str(func.round_value_decimals(measure, decimals)) + ", '" \
                         + sensor_name + "');"
            # print(str(sql_insert))
            curs.execute(sql_insert)

            print("\tAdded value for " + sensor_name + "; committing...")
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
