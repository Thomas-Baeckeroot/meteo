#!/usr/bin/env python

import tsl2561  # If failing, run: pip install Adafruit_GPIO tsl2561 (and also RPi.GPIO ?)
import Adafruit_BMP.BMP085 as BMP085

from gpiozero import CPUTemperature  # If failing: "pip install gpiozero"

SENSOR_KNOWN_ALTITUDE = 230.0  # estimated for St Benoit


def value_CPU_temp():
    return CPUTemperature().temperature


def value_luminosity():
    tsl = tsl2561.TSL2561(debug=True)
    return tsl.lux()


def value_temp_and_sealevelpressure():
    sensor = BMP085.BMP085()
    temp = sensor.read_temperature()
    # round() added to truncate insignificant values to save db space
    sealevelpressure = round(sensor.read_sealevel_pressure(SENSOR_KNOWN_ALTITUDE)) / 100.0
    return (temp, sealevelpressure)
