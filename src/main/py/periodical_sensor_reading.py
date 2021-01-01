#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import calendar
# import datetime
# import pydevd  # If failing: "pip install pydevd"
import socket
# import sqlite3
import sys
import time
# import tsl2561  # If failing: pip install: Adafruit_GPIO tsl2561 (and also RPi.GPIO ?)
# from gpiozero import CPUTemperature  # If failing: "pip install gpiozero"
# import Adafruit_BMP.BMP085 as BMP085

import sensors_functions as func
from time import sleep
import utils
import hc_sr04_lib_test
import home_web.db_module as db_module

# path_to_pydevd = "home/pi/.local/bin/pydevd"  # found by 'find / -name pydevd'
# sys.path.append(path_to_pydevd)

# debugger_ip_address = "192.168.0.63"
# pydevd.settrace(debugger_ip_address, port=5678)

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


def copy_values_from_server(sensor_dest, remote_server_src, conn_local_dest):
    (sensor_name, sensor_label_dest, decimals_dest, cumulative_dest, unit_dest,
        consolidated_dest, sensor_type_dest, filepath_last, filepath_data) = sensor_dest
    sensor_name = sensor_name.decode('ascii')
    try:
        conn_remote_src = db_module.get_conn(host=remote_server_src)  # Connect to REMOTE PostgreSQL DB
    except Exception as err:
        print("\tException: {0}".format(err))
        return
    curs_src = conn_remote_src.cursor()
    read_sensors_query = "SELECT sensor_label, decimals, cumulative, unit, consolidated" \
                         "  FROM sensors" \
                         " WHERE name='" + sensor_name + "';"
    curs_src.execute(read_sensors_query)
    (sensor_label_src, decimals_src, cumulative_src, unit_src, consolidated_src) = curs_src.fetchall()[0]
    # FIXME Below UPDATEs have no effect...
    if sensor_label_src != sensor_label_dest:
        print("\tUPDATING sensor_label: \tsrc='" + sensor_label_src + "'\t>>> dest='" + sensor_label_dest + "'")
        print("UPDATE sensors   SET sensor_label='" + sensor_label_src + "' WHERE name='" + sensor_name + "';")
    #    curs_src.execute("UPDATE sensors"
    #                     "   SET sensor_label='" + sensor_label_src +
    #                     "' WHERE name='" + sensor_name + "';")
    if decimals_src != decimals_dest:
        print("\tUPDATING Decimals:     \tsrc='" + str(decimals_src) + "'\t>>> dest='" + str(decimals_dest) + "'")
        curs_src.execute("UPDATE sensors"
                         "   SET decimals=" + str(decimals_src) +
                         " WHERE name='" + sensor_name + "';")
    if cumulative_src != cumulative_dest:
        print("\tUPDATING cumulative: \tsrc='" + str(cumulative_src) + "'\t>>> dest='" + str(cumulative_dest) + "'")
        curs_src.execute("UPDATE sensors"
                         "   SET cumulative=" + str(cumulative_src) +
                         " WHERE name='" + sensor_name + "';")
    if unit_src != unit_dest:
        print("\tUPDATING unit: \tsrc='" + unit_src + "'\t>>> dest='" + unit_dest + "'")
        curs_src.execute("UPDATE sensors"
                         "   SET unit='" + unit_src +
                         "' WHERE name='" + sensor_name + "';")
    if consolidated_src != consolidated_dest:
        print("\tUPDATING consolidated: \tsrc='" + str(consolidated_src) + "'\t>>> dest='" + str(consolidated_dest) + "'")
        curs_src.execute("UPDATE sensors"
                         "   SET consolidated='" + str(consolidated_src) +
                         "' WHERE name='" + str(sensor_name) + "';")

    read_sensors_query = "SELECT epochtimestamp, measure" \
                         "  FROM raw_measures" \
                         " WHERE sensor='" + sensor_name + \
                         "'  AND synchronised='false' " \
                         "ORDER BY epochtimestamp asc LIMIT 3000;"  # PostgreSQL: "FETCH FIRST 10 ROWS ONLY;"
    # print("\tread_sensors_query =\n" + read_sensors_query + "\n----------------------------")
    curs_src.execute(read_sensors_query)
    epochs_and_measures_from_src = curs_src.fetchall()
    n_updates = len(epochs_and_measures_from_src)
    if n_updates > 0:
        insert_measures_to_dest_query = "INSERT INTO raw_measures(epochtimestamp, measure, sensor) VALUES "
        not_first_value = False
        for (epoch_src, measure_src) in epochs_and_measures_from_src:
            # = epoch_and_measure  # todo once working, should be included within for declaration
            if not_first_value:
                insert_measures_to_dest_query = insert_measures_to_dest_query + ","
            insert_measures_to_dest_query = insert_measures_to_dest_query \
                + "(" + str(epoch_src) + ", " + str(measure_src) + ", '" \
                + sensor_name + "')"
            not_first_value = True
        insert_measures_to_dest_query = insert_measures_to_dest_query + ";"
        curs_dest = conn_local_dest.cursor()
        # print("\tinsert_measures_to_dest_query = " + str(len(insert_measures_to_dest_query)) + " bytes/chars")
        # print(insert_measures_to_dest_query)
        # print("\t-----------------------------------------")
        curs_dest.execute(insert_measures_to_dest_query)

        update_synchronised_query = "UPDATE raw_measures" \
                                    "   SET synchronised=true" \
                                    " WHERE epochtimestamp IN ("
        # PostgreSQL? was "UPDATE raw_measures(synchronised) SET true""
        not_first_value = False
        for (epoch_src, measure_src) in epochs_and_measures_from_src:
            if not_first_value:
                update_synchronised_query = update_synchronised_query + ", "
            update_synchronised_query = update_synchronised_query + str(epoch_src)
            not_first_value = True
        update_synchronised_query = update_synchronised_query + ") AND sensor='" + sensor_name + "'"
        # print("\tupdate_synchronised_query =" + str(len(update_synchronised_query)) + " bytes/chars")
        # print(update_synchronised_query)
        # print("\t-----------------------------------------")
        curs_src.execute(update_synchronised_query)

        conn_remote_src.commit()

    conn_local_dest.commit()  # Can be an update of label name or unit, etc... without value

    print("\tImported " + str(n_updates) + " records from " + remote_server_src)

    return


def rsync_pictures_from_server(local_sensor, remote_server_src, conn_local_dest):
    (sensor_name, sensor_label_dest, decimals_dest, cumulative_dest, unit_dest,
        consolidated_dest, sensor_type_dest, filepath_last_local, filepath_data_local) = local_sensor
    sensor_name = sensor_name.decode('ascii')
    print("\tpicture sensor '" + sensor_name + "'")
    print("\t(filepath_last_local, filepath_data_local) = (\t'" + filepath_last_local + "',\t'" + filepath_data_local + "')")
    try:
        conn_remote_src = db_module.get_conn(host=remote_server_src)  # Connect to REMOTE PostgreSQL DB
    except Exception as err:
        print("\tException: {0}".format(err))
        return
    curs_src = conn_remote_src.cursor()
    read_filepath_query = "SELECT filepath_last, filepath_data" \
                          "  FROM captures" \
                          " WHERE sensor_name='" + sensor_name + "';"
    print("\tread_filepath_query = '" + read_filepath_query + "'")
    curs_src.execute(read_filepath_query)
    (filepath_last_src, filepath_data_src) = curs_src.fetchall()[0]
    print("\t(filepath_last_src, filepath_data_src)   =   (\t'" + filepath_last_src + "',\t'" + filepath_data_src + "')")
    if filepath_last_src != filepath_last_local:
        print("FIXME: Call to .rsync_pictures_from_server() ignored!")
    # rsync -ravz -e "ssh -p 49142" --size-only pi@82.64.89.174:/home/pi/meteo/captures/*.jpg /home/thomas/workspace/meteo/captures/grangette/


def main():  # Expected to be called once per minute
    main_call_epoch = utils.epoch_now()
    print(utils.iso_timestamp_now() + " - Starting on " + socket.gethostname()
          + " ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
    temp = 15  # default value for later calculation of speed of sound
    first_remote = True
    local_camera_name = None

    conn = db_module.get_conn()
    curs = conn.cursor()

    # name   | priority |        sensor_label         | decimals | cumulative | unit | consolidated | sensor_type
    read_sensors_query = \
        "SELECT  name, sensor_label, decimals, cumulative, unit," \
        "        consolidated, sensor_type, filepath_last, filepath_data " \
        "FROM    sensors " \
        "    LEFT JOIN captures ON sensors.name = captures.sensor_name; "
    curs.execute(read_sensors_query)
    sensors = curs.fetchall()
    for sensor in sensors:
        (sensor_name, sensor_label, decimals, cumulative, unit,
            consolidated, sensor_type, filepath_last, filepath_data) = sensor
        sensor_name = sensor_name.decode('ascii')

        measure = None
        # Below ifs to be replaced by function blocks and dictionary as described
        # at https://stackoverflow.com/questions/11479816/what-is-the-python-equivalent-for-a-case-switch-statement
        if sensor_type == "ignored":
            print("Sensor '" + sensor_name + "' -> -ignoring-")
            # measure = None  # kept as None

        elif sensor_type == "CPU_temp":
            measure = func.value_cpu_temp()
            # start_cpu_fan = __import__("start_cpu_fan")
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

        elif sensor_type == "camera":
            local_camera_name = sensor_name

        elif sensor_type.startswith("remote:"):
            if first_remote:
                sleep(5)  # give time for very last value of remote sensors to be updated
                first_remote = False
            # Another remote PostgreSQL contains the measures. Those not "synchronised" will be copied
            # if having ~Connection refused~~port 5432?~ issues then
            #   -> On remote server, in file postgresql.conf, set "listen_addresses = '*'"
            # 
            #   -> in file pg_hba.conf, add "host    meteo           pi              192.168.0.94/32         trust"
            # (those 2 configuration files are usually in /etc/postgresql/11/main/ )
            # fixme the upper "trust" is not secured and should look for a decent unix authentication later...
            remote_server = sensor_type[7:]
            print("Sensor '" + sensor_name + "' -> reading values from " + remote_server + "...")
            if unit == "picture":
                rsync_pictures_from_server(sensor, remote_server, conn)
            else:
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
        else:
            print("Sensor '" + sensor_name + "' -> No value")

    # end of for-loop on each sensor
    config = utils.get_config()
    # database = config.get('DATABASE', 'Name', fallback='weather_station')

    if local_camera_name is not None:
        is_camera_mult = is_multiple(main_call_epoch, 900)  # is True every 900 s / 15 min
        if is_camera_mult:
            print("Once every 15 minutes: Capture picture")
            picture_name = func.take_picture(local_camera_name)

            # try:
            sql_update = \
                "UPDATE captures         " +\
                "SET    filepath_last = '" + picture_name + "'," +\
                "       filepath_data = '" + picture_name + "' " +\
                "WHERE  sensor_name = '" + local_camera_name + "';"
            # print(sql_update)  # for debugging...
            result = curs.execute(sql_update)
            # except Exception as err:
            if result == 0:
                sql_insert = \
                    "INSERT INTO captures (sensor_name, filepath_last, filepath_data) " +\
                    "VALUES ('" + local_camera_name + "', '" + picture_name + "', '" + picture_name + "')"
                # print(sql_insert)  # for debugging...
                curs.execute(sql_insert)
            
            print("\tUpdated value for camera " + local_camera_name + "; committing...")
            conn.commit()

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
