#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tsl2561  # If failing, run: pip install Adafruit_GPIO tsl2561 (and also RPi.GPIO ?)
import Adafruit_BMP.BMP085 as BMP085

from gpiozero import CPUTemperature  # If failing: "pip install gpiozero"

# todo Below variable should be stored in a config file ~/.config/meteo.conf (GPIO numbers also could be informed there)
SENSOR_KNOWN_ALTITUDE = 230.0  # estimated for St Benoit


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
    tsl = tsl2561.TSL2561(debug=True)
    return tsl


def value_ext_temperature():
    sensor = BMP085.BMP085()
    temp = sensor.read_temperature()
    return temp


def value_sealevelpressure():
    sensor = BMP085.BMP085()
    sealevelpressure_hpa = sensor.read_sealevel_pressure(SENSOR_KNOWN_ALTITUDE) / 100  # Pa -> hPa
    return sealevelpressure_hpa
