#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import pathlib
import time
import utils

from gpiozero import CPUTemperature  # If failing: "pip install gpiozero"

logging.basicConfig(
    filename=utils.get_home() + "/susanoo-data.log",  # = /home/pi/susanoo-data.log
    level=logging.DEBUG,
    format='%(asctime)s\t%(levelname)s\t%(name)s (%(process)d)\t%(message)s')
log = logging.getLogger("sensors_functions.py")

# todo Below variable should be stored in a config file ~/.config/meteo.conf (GPIO numbers also could be informed there)
METEO_FOLDER = "/home/pi/meteo"


def round_value_decimals(value, decimals):
    # round() added to truncate insignificant values to save db space
    if decimals > 0:
        return round(value, decimals)
    else:
        return int(round(value, decimals))


def value_cpu_temp():
    cpu_temp = CPUTemperature().temperature
    return cpu_temp


def value_luminosity():
    tsl2561 = __import__("tsl2561")  # If failing, run: "sudo pip3 install Adafruit_GPIO tsl2561" (and also RPi.GPIO ?)
    tsl = tsl2561.TSL2561(debug=True)
    return tsl.lux()


def value_ext_temperature():
    bmp_mod = __import__("Adafruit_BMP.BMP085")
    sensor = bmp_mod.BMP085.BMP085()
    temp = sensor.read_temperature()
    return temp


def value_sealevelpressure():
    config = utils.get_config()
    sensor_known_altitude = config.getfloat('DEFAULT', 'SensorKnownAltitude', fallback=50.0)
    bmp_mod = __import__("Adafruit_BMP.BMP085")
    sensor = bmp_mod.BMP085.BMP085()
    sealevelpressure_hpa = sensor.read_sealevel_pressure(sensor_known_altitude) / 100  # Pa -> hPa
    return sealevelpressure_hpa


def take_picture(camera_name):
    log.debug("Take picture:\t")
    capture_tentatives = 0
    while capture_tentatives < 23:
        picamera = __import__("picamera")
        capture_tentatives = capture_tentatives + 1
        try:
            camera = picamera.PiCamera()  # TODO Duplicated with video_capture_on_motion.py:61
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
            filename = camera_name + "_" + dt_now + ".jpg"
            capture_folder = camera_name + "/" + dt_now[0:4] + "/" + dt_now[5:10]
            base_captures_folder = "captures"  # todo get value from config file
            pathlib.Path(METEO_FOLDER + "/" + base_captures_folder + "/" + capture_folder)\
                .mkdir(mode=0o755, parents=True, exist_ok=True)
            full_path_filename = capture_folder + "/" + filename
            log.debug(full_path_filename)
            camera.capture(METEO_FOLDER + "/" + base_captures_folder + "/" + full_path_filename)
            # todo Test upper with , thumbnail=(64, 48, 35)
            camera.stop_preview()
            camera.close()
            return full_path_filename
        except picamera.exc.PiCameraMMALError:
            log.debug(f"PiCameraMMALError - retrying ({capture_tentatives})")
            time.sleep(capture_tentatives)

        # End of 'while not captured_success and capture_tentatives < 23:'
    log.error("Failed " + str(capture_tentatives) + " times to take picture. Gave up!")
    return None
