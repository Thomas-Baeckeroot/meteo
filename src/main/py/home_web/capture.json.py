#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import os

from db_module import get_home
from urllib.parse import parse_qsl

HOME = get_home()
LOGFILE = HOME + "/susanoo-web.log"
logging.basicConfig(
    filename=LOGFILE,
    level=logging.DEBUG,
    format='%(asctime)s\t%(levelname)s\t%(name)s (%(process)d)\t%(message)s')
log = logging.getLogger("capture.json")

# Get the query string from the environment
query_string = os.environ.get("QUERY_STRING")

log.info(f"Start building json for capture '{query_string}'")


def write_content_type():
    print("Content-type: application/json; charset=utf-8\n")
    return


def write_json_content(data_to_print):
    # Serialize the JSON object to a string
    json_data = json.dumps(data_to_print, ensure_ascii=False)  # ensure_ascii=False to allow non-ASCII characters
    # json_data = json.dumps(folder_data, indent=4)

    # Output the JSON data
    print(json_data)


def get_oldest_created_folder(l_folder):
    # log.debug(f"get_oldest_created_folder({l_folder}) starting")
    oldest_folder = None
    oldest_timestamp = float('inf')  # Initialize with a large value

    for dir_name in os.listdir(l_folder):
        # log.debug(f"\tchecking subfolder '{dir_name}'")
        dir_path = os.path.join(l_folder, dir_name)
        if os.path.isdir(dir_path):
            # log.debug(f"\t\tis directory")
            try:
                timestamp = os.path.getctime(dir_path)  # Date of creation
                if timestamp < oldest_timestamp:
                    oldest_folder = dir_path
                    oldest_timestamp = timestamp
            except OSError:
                pass  # Ignore any errors, such as permission denied

    # log.debug(f"get_oldest_created_folder({l_folder}) returning -> '{oldest_folder}'")
    return oldest_folder


def get_newest_modified_folder(l_folder):
    # log.debug(f"get_newest_modified_folder({l_folder}) starting")
    newest_folder = None
    newest_timestamp = 0  # Initialize with zero

    for dir_name in os.listdir(l_folder):
        dir_path = os.path.join(l_folder, dir_name)
        if os.path.isdir(dir_path):
            try:
                timestamp = os.path.getmtime(dir_path)  # Date of modification
                if timestamp > newest_timestamp:
                    newest_folder = dir_path
                    newest_timestamp = timestamp
            except OSError:
                pass  # Ignore any errors, such as permission denied

    # log.debug(f"get_newest_modified_folder({l_folder}) returning -> '{newest_folder}'")
    return newest_folder


def make_json_from_folder(pictures_folder):
    folder_data = {}
    for filename in os.listdir(pictures_folder):
        if filename.endswith(".jpg"):
            # Extract the timestamp from the filename
            timestamp = filename.split("_")[1].split(".")[0]  # Assumes the format is "sensor_YYYY-MM-DDZhh-mm-ss.jpg"
            time_parts = timestamp[-8:].split("-")
            hour_minute = f"{time_parts[0]}h{time_parts[1]}"

            # Get file size
            file_path = os.path.join(pictures_folder, filename)
            fsize = os.path.getsize(file_path)

            # Add an entry to the folder_data dictionary
            folder_data[hour_minute] = {"fSize": fsize, "img": filename}

    return folder_data


def get_json_from_folder(l_sensor, l_year, l_month, l_day):
    captures_folder = "captures/"
    log.debug(os.getcwd())

    if l_sensor:
        if os.path.exists(captures_folder + l_sensor):
            sensor_folder = captures_folder + l_sensor
        else:
            sensor_folder = get_oldest_created_folder(captures_folder)
            log.warning(f"Given sensor '{l_sensor}' was not valid. Will use '{sensor_folder}' instead")
    else:
        sensor_folder = get_oldest_created_folder(captures_folder)
    log.debug(f"sensor_folder = '{sensor_folder}'")

    if l_year:
        if os.path.exists(sensor_folder + l_year):
            year_folder = sensor_folder + l_year
        else:
            year_folder = get_newest_modified_folder(sensor_folder)
            log.warning(f"Given year '{l_year}' was not valid. Will use '{year_folder}' instead")
    else:
        year_folder = get_newest_modified_folder(sensor_folder)
    log.debug(f"       + year = '{year_folder}'")

    if l_month and l_day:
        if os.path.exists(year_folder + "/" + l_month + "-" + l_day):
            pictures_folder = year_folder + "/" + l_month + "-" + l_day
        else:
            pictures_folder = get_newest_modified_folder(year_folder)
            log.warning(f"Given that month-day '{l_month}-{l_day}' was not a valid folder,"
                        f" '{pictures_folder}' will be used instead")
    else:
        pictures_folder = get_newest_modified_folder(year_folder)
    log.debug(f"       + mmdd = '{pictures_folder}'")

    log.info(f"Will get pictures from folder '{pictures_folder}'")

    # FIXME CONTINUE HERE WITH Y M D

    l_folder = "../captures/"
    # get_newest_file(HOME + "/captures/" + camera + "/" + year + "/" + month_day)
    # l_folder_scan = os.scandir(l_folder)

    folder_data = make_json_from_folder(pictures_folder)
    # folder_data = {
    #     "00h00": {"fSize": 46661, "img": "tilleul_2020-12-29Z00-00-08.jpg"},
    #     "00h15": {"fSize": 46673, "img": "tilleul_2020-12-29Z00-15-08.jpg"},
    #     "00h30": {"fSize": 46603, "img": "tilleul_2020-12-29Z00-30-08.jpg"},
    #     "00h45": {"fSize": 46601, "img": "tilleul_2020-12-29Z00-45-08.jpg"},
    #     "01h00": {"fSize": 46731, "img": "tilleul_2020-12-29Z01-00-08.jpg"},
    #     "01h15": {"fSize": 46766, "img": "tilleul_2020-12-29Z01-15-08.jpg"},
    #     "01h30": {"fSize": 46678, "img": "tilleul_2020-12-29Z01-30-08.jpg"},
    #     "01h45": {"fSize": 46473, "img": "tilleul_2020-12-29Z01-45-08.jpg"},
    #     "02h00": {"fSize": 46595, "img": "tilleul_2020-12-29Z02-00-08.jpg"},
    #     "02h15": {"fSize": 46652, "img": "tilleul_2020-12-29Z02-15-08.jpg"},
    #     "02h30": {"fSize": 46627, "img": "tilleul_2020-12-29Z02-30-08.jpg"},
    #     "02h45": {"fSize": 46534, "img": "tilleul_2020-12-29Z02-45-08.jpg"},
    #     "03h00": {"fSize": 46610, "img": "tilleul_2020-12-29Z03-00-09.jpg"},
    #     "03h15": {"fSize": 46596, "img": "tilleul_2020-12-29Z03-15-08.jpg"},
    #     "03h30": {"fSize": 46689, "img": "tilleul_2020-12-29Z03-30-08.jpg"},
    #     "03h45": {"fSize": 46683, "img": "tilleul_2020-12-29Z03-45-08.jpg"},
    #     "04h00": {"fSize": 46603, "img": "tilleul_2020-12-29Z04-00-08.jpg"},
    #     "04h15": {"fSize": 46516, "img": "tilleul_2020-12-29Z04-15-09.jpg"},
    #     "04h30": {"fSize": 46585, "img": "tilleul_2020-12-29Z04-30-08.jpg"},
    #     "04h45": {"fSize": 46519, "img": "tilleul_2020-12-29Z04-45-08.jpg"},
    #     "05h00": {"fSize": 46648, "img": "tilleul_2020-12-29Z05-00-08.jpg"},
    #     "05h15": {"fSize": 46638, "img": "tilleul_2020-12-29Z05-15-08.jpg"},
    #     "05h30": {"fSize": 46593, "img": "tilleul_2020-12-29Z05-30-08.jpg"},
    #     "05h45": {"fSize": 46661, "img": "tilleul_2020-12-29Z05-45-08.jpg"},
    #     "06h00": {"fSize": 46631, "img": "tilleul_2020-12-29Z06-00-08.jpg"},
    #     "06h15": {"fSize": 46609, "img": "tilleul_2020-12-29Z06-15-09.jpg"},
    #     "06h30": {"fSize": 46533, "img": "tilleul_2020-12-29Z06-30-08.jpg"},
    #     "06h45": {"fSize": 46641, "img": "tilleul_2020-12-29Z06-45-08.jpg"},
    #     "07h00": {"fSize": 46604, "img": "tilleul_2020-12-29Z07-00-08.jpg"},
    #     "07h15": {"fSize": 108528, "img": "tilleul_2020-12-29Z07-15-08.jpg"},
    #     "07h30": {"fSize": 791501, "img": "tilleul_2020-12-29Z07-30-08.jpg"},
    #     "07h45": {"fSize": 1087651, "img": "tilleul_2020-12-29Z07-45-08.jpg"},
    #     "08h00": {"fSize": 1093435, "img": "tilleul_2020-12-29Z08-00-08.jpg"},
    #     "08h15": {"fSize": 1116305, "img": "tilleul_2020-12-29Z08-15-08.jpg"},
    #     "08h30": {"fSize": 1160192, "img": "tilleul_2020-12-29Z08-30-08.jpg"},
    #     "08h45": {"fSize": 1153000, "img": "tilleul_2020-12-29Z08-45-08.jpg"},
    #     "09h00": {"fSize": 1116201, "img": "tilleul_2020-12-29Z09-00-08.jpg"},
    #     "09h15": {"fSize": 1186726, "img": "tilleul_2020-12-29Z09-15-08.jpg"},
    #     "09h30": {"fSize": 1119104, "img": "tilleul_2020-12-29Z09-30-08.jpg"},
    #     "09h45": {"fSize": 1109490, "img": "tilleul_2020-12-29Z09-45-08.jpg"},
    #     "10h00": {"fSize": 1143556, "img": "tilleul_2020-12-29Z10-00-08.jpg"},
    #     "10h15": {"fSize": 1162086, "img": "tilleul_2020-12-29Z10-15-11.jpg"},
    #     "10h30": {"fSize": 1179178, "img": "tilleul_2020-12-29Z10-30-09.jpg"},
    #     "10h45": {"fSize": 1170136, "img": "tilleul_2020-12-29Z10-45-09.jpg"},
    #     "11h00": {"fSize": 1138029, "img": "tilleul_2020-12-29Z11-00-08.jpg"},
    #     "11h15": {"fSize": 1187628, "img": "tilleul_2020-12-29Z11-15-08.jpg"},
    #     "11h30": {"fSize": 1142732, "img": "tilleul_2020-12-29Z11-30-08.jpg"},
    #     "11h45": {"fSize": 1195062, "img": "tilleul_2020-12-29Z11-45-08.jpg"},
    #     "12h00": {"fSize": 1113049, "img": "tilleul_2020-12-29Z12-00-08.jpg"},
    #     "12h15": {"fSize": 1147729, "img": "tilleul_2020-12-29Z12-15-08.jpg"},
    #     "12h30": {"fSize": 1048152, "img": "tilleul_2020-12-29Z12-30-08.jpg"},
    #     "12h45": {"fSize": 1007747, "img": "tilleul_2020-12-29Z12-45-08.jpg"},
    #     "13h00": {"fSize": 1116413, "img": "tilleul_2020-12-29Z13-00-08.jpg"},
    #     "13h15": {"fSize": 1160091, "img": "tilleul_2020-12-29Z13-15-08.jpg"},
    #     "13h30": {"fSize": 1114134, "img": "tilleul_2020-12-29Z13-30-08.jpg"},
    #     "13h45": {"fSize": 1131524, "img": "tilleul_2020-12-29Z13-45-08.jpg"},
    #     "14h00": {"fSize": 1101222, "img": "tilleul_2020-12-29Z14-00-08.jpg"},
    #     "14h15": {"fSize": 1057128, "img": "tilleul_2020-12-29Z14-15-08.jpg"},
    #     "14h30": {"fSize": 926505, "img": "tilleul_2020-12-29Z14-30-09.jpg"},
    #     "14h45": {"fSize": 917604, "img": "tilleul_2020-12-29Z14-45-08.jpg"},
    #     "15h00": {"fSize": 947831, "img": "tilleul_2020-12-29Z15-00-09.jpg"},
    #     "15h15": {"fSize": 923159, "img": "tilleul_2020-12-29Z15-15-08.jpg"},
    #     "15h30": {"fSize": 1067316, "img": "tilleul_2020-12-29Z15-30-08.jpg"},
    #     "15h45": {"fSize": 1048425, "img": "tilleul_2020-12-29Z15-45-08.jpg"},
    #     "16h00": {"fSize": 1074060, "img": "tilleul_2020-12-29Z16-00-08.jpg"},
    #     "16h15": {"fSize": 1063189, "img": "tilleul_2020-12-29Z16-15-08.jpg"},
    #     "16h30": {"fSize": 881359, "img": "tilleul_2020-12-29Z16-30-08.jpg"},
    #     "16h45": {"fSize": 135116, "img": "tilleul_2020-12-29Z16-45-08.jpg"},
    #     "17h00": {"fSize": 51957, "img": "tilleul_2020-12-29Z17-00-08.jpg"},
    #     "17h15": {"fSize": 51516, "img": "tilleul_2020-12-29Z17-15-08.jpg"},
    #     "17h30": {"fSize": 51687, "img": "tilleul_2020-12-29Z17-30-08.jpg"},
    #     "17h45": {"fSize": 51324, "img": "tilleul_2020-12-29Z17-45-08.jpg"},
    #     "18h00": {"fSize": 51538, "img": "tilleul_2020-12-29Z18-00-08.jpg"}  # ,
    #     # "18h15": {"fSize": 51325, "img": "tilleul_2020-12-29Z18-15-08.jpg"},
    #     # "18h30": {"fSize": 52295, "img": "tilleul_2020-12-29Z18-30-08.jpg"},
    #     # "18h45": {"fSize": 52862, "img": "tilleul_2020-12-29Z18-45-08.jpg"},
    #     # "19h00": {"fSize": 52527, "img": "tilleul_2020-12-29Z19-00-08.jpg"},
    #     # "19h15": {"fSize": 52930, "img": "tilleul_2020-12-29Z19-15-08.jpg"},
    #     # "19h30": {"fSize": 53194, "img": "tilleul_2020-12-29Z19-30-08.jpg"},
    #     # "19h45": {"fSize": 52433, "img": "tilleul_2020-12-29Z19-45-08.jpg"},
    #     # "20h00": {"fSize": 46629, "img": "tilleul_2020-12-29Z20-00-09.jpg"},
    #     # "20h15": {"fSize": 53649, "img": "tilleul_2020-12-29Z20-15-08.jpg"},
    #     # "20h30": {"fSize": 52832, "img": "tilleul_2020-12-29Z20-30-08.jpg"},
    #     # "20h45": {"fSize": 52934, "img": "tilleul_2020-12-29Z20-45-08.jpg"},
    #     # "21h00": {"fSize": 52507, "img": "tilleul_2020-12-29Z21-00-08.jpg"},
    #     # "21h15": {"fSize": 52917, "img": "tilleul_2020-12-29Z21-15-08.jpg"},
    #     # "21h30": {"fSize": 52495, "img": "tilleul_2020-12-29Z21-30-09.jpg"},
    #     # "21h45": {"fSize": 52760, "img": "tilleul_2020-12-29Z21-45-08.jpg"},
    #     # "22h00": {"fSize": 52590, "img": "tilleul_2020-12-29Z22-00-11.jpg"},
    #     # "22h15": {"fSize": 52538, "img": "tilleul_2020-12-29Z22-15-08.jpg"},
    #     # "22h30": {"fSize": 52606, "img": "tilleul_2020-12-29Z22-30-08.jpg"},
    #     # "22h45": {"fSize": 52790, "img": "tilleul_2020-12-29Z22-45-11.jpg"},
    #     # "23h00": {"fSize": 52672, "img": "tilleul_2020-12-29Z23-00-08.jpg"},
    #     # "23h15": {"fSize": 52675, "img": "tilleul_2020-12-29Z23-15-08.jpg"},
    #     # "23h30": {"fSize": 52871, "img": "tilleul_2020-12-29Z23-30-08.jpg"},
    #     # "23h45": {"fSize": 52755, "img": "tilleul_2020-12-29Z23-45-08.jpg"} */
    # }
    return folder_data


write_content_type()

# Parse the query string to extract parameters
query_params = parse_qsl(query_string)

# Create a dictionary to store the parameters
params = dict(query_params)

# Access the values by key
sensor = params.get("s")
year = params.get("y")
month = params.get("m")
day = params.get("d")

log.debug(f"sensor='{sensor}'\tyear='{year}'\tmonth-day='{month}-{day}'")

data = get_json_from_folder(sensor, year, month, day)
write_json_content(data)
log.info("Terminated building json for capture page")
