#!/usr/bin/env python

import tsl2561  # If failing, run: pip install Adafruit_GPIO tsl2561 (and also RPi.GPIO ?)
import Adafruit_BMP.BMP085 as BMP085

from gpiozero import CPUTemperature  # If failing: "pip install gpiozero"

SENSOR_KNOWN_ALTITUDE = 230.0  # estimated for St Benoit


def round_value_decimals(value, decimals):
    # round() added to truncate insignificant values to save db space
    if decimals > 0:
        return round(value, decimals)
    else:
        return int(round(value, decimals))


def value_CPU_temp():
    cpu_temp = CPUTemperature().temperature
    return round_value_decimals(cpu_temp, 1)


def value_luminosity():
    tsl = tsl2561.TSL2561(debug=True)
    return round_value_decimals(tsl.lux(), 0)


def value_temp_and_sealevelpressure():
    sensor = BMP085.BMP085()
    temp = sensor.read_temperature()
    sealevelpressure_hpa = sensor.read_sealevel_pressure(SENSOR_KNOWN_ALTITUDE) / 100  # Pa -> hPa
    sealevelpressure_hpa = round_value_decimals(sealevelpressure_hpa, 2)  # keep only 2 decimals
    return temp, sealevelpressure_hpa
