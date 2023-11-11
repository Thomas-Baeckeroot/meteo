#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This script should be launched at startup with:
# python ~/meteo/src/main/py/start_cpu_fan.py
# TODO Rename file to cpu_fan.py only

import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library

# todo Below variable should be stored in a config file ~/.config/susanoo_WeatherStation.conf
GPIO_CPU_FAN_RELAY_OUT = 19


def start_cpu_fan():
    GPIO.setmode(GPIO.BCM)  # Use GPIO numbering
    GPIO.setup(GPIO_CPU_FAN_RELAY_OUT, GPIO.OUT, initial=GPIO.LOW)  # low = fan is running
    print("CPU fan started.")


def stop_cpu_fan():
    GPIO.setmode(GPIO.BCM)  # Use GPIO numbering
    GPIO.setup(GPIO_CPU_FAN_RELAY_OUT, GPIO.OUT, initial=GPIO.HIGH)  # high = fan is stopped
    print("CPU fan stopped.")


def main():
    start_cpu_fan()


if __name__ == "__main__":
    main()
