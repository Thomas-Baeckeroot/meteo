#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
# import subprocess
import sys
import time  # Import the sleep function from the time module

from utils import get_config
from utils import iso_timestamp_now

# todo Below variables should be stored in config file ~/.config/meteo.conf
# GPIO_YYY_LED = 23
# GPIO_ZZZ_LED = 24
GPIO_WATCHDOG_LED = 25

# GPIO_XXX_BTN_IN = 12
# GPIO_YYY_BTN_IN = 16
# GPIO_ZZZ_BTN_IN = 20
GPIO_SHUTDOWN_BTN_IN = 21


def start_shutdown_process():
    global GPIO_WATCHDOG_LED
    global GPIO_SHUTDOWN_BTN_IN

    print(iso_timestamp_now() + " - Will now blink fast for 1 sec., stop for 1 s. and light on for 1 s.,")
    print("\texpecting no button pressed at end of led off,")
    print("\tand expecting button pressed at end of led on.")
    sys.stdout.flush()

    for x in range(0, 5):
        GPIO.output(GPIO_WATCHDOG_LED, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(GPIO_WATCHDOG_LED, GPIO.LOW)
        time.sleep(0.1)
    time.sleep(1)
    if not GPIO.input(GPIO_SHUTDOWN_BTN_IN):
        print("\tGot button pressed at the end of 1s. LED off => cancel stop request")
        # sys.stdout.flush()  # not necessary here, only if debug required
        return
    GPIO.output(GPIO_WATCHDOG_LED, GPIO.HIGH)
    time.sleep(1)
    if GPIO.input(GPIO_SHUTDOWN_BTN_IN):  # Button NOT pressed
        print("\tGot button unpressed at the end of 1s. LED on => cancel stop request")
        # sys.stdout.flush()  # not necessary here, only if debug required
        return
    print(iso_timestamp_now() + " - => Calling for SHUTDOWN!")
    sys.stdout.flush()
    # os.system("/sbin/shutdown -k now")
    # os.system("/sbin/shutdown -P 1")
    for x in range(0, 5):  # blink fast for 1s (visual confirmation of imminent shutdown)
        GPIO.output(GPIO_WATCHDOG_LED, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(GPIO_WATCHDOG_LED, GPIO.HIGH)
        time.sleep(0.1)
    os.system("/sbin/shutdown -P now &")

    # subprocess.run(["/sbin/shutdown", "-P", "now"])  # Python 3
    # subprocess.call(["/sbin/shutdown", "-P", "now"])  # Python 2
    while True:  # # blink fast until shutdown
        GPIO.output(GPIO_WATCHDOG_LED, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(GPIO_WATCHDOG_LED, GPIO.HIGH)
        time.sleep(0.1)


def main():  # Expected to be launched at startup
    global GPIO_WATCHDOG_LED
    global GPIO_SHUTDOWN_BTN_IN

    print("_" * 80)
    print(iso_timestamp_now() + " - Starting watchdog...")

    config = get_config()
    GPIO_WATCHDOG_LED = int(config['GPIO']['GPIO_WATCHDOG_LED'])
    GPIO_SHUTDOWN_BTN_IN = int(config['GPIO']['GPIO_SHUTDOWN_BTN_IN'])
    print(iso_timestamp_now() + " - GPIOs:")
    print(iso_timestamp_now() + "\tWatchdog LED    -> " + str(GPIO_WATCHDOG_LED) + " (output)")
    print(iso_timestamp_now() + "\tShutdown button -> " + str(GPIO_SHUTDOWN_BTN_IN) + " (input)")

    # GPIO.setwarnings(False)    # Ignore warning for now
    GPIO.setmode(GPIO.BCM)  # Use GPIO numbering

    print(iso_timestamp_now() + " - Using GPIO" + str(GPIO_SHUTDOWN_BTN_IN) + " as input for shutdown button.")
    GPIO.setup(GPIO_SHUTDOWN_BTN_IN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print(iso_timestamp_now() + " - Using GPIO" + str(GPIO_WATCHDOG_LED) + " as output for blinking LED.")
    GPIO.setup(GPIO_WATCHDOG_LED, GPIO.OUT, initial=GPIO.HIGH)

    cycle_length = 5  # time keep watchdog led on off in deci-seconds (5 -> 0.5s on / 0.5s off)
    watchdog_led_status = False
    log_count = 0
    cycle_count = 0
    while True:  # Run forever
        log_count = log_count + 1
        cycle_count = cycle_count + 1

        # blink watchdog:
        if cycle_count >= cycle_length:
            cycle_count = 0
            if watchdog_led_status:
                GPIO.output(GPIO_WATCHDOG_LED, GPIO.LOW)  # Turn off
                watchdog_led_status = False
            else:
                GPIO.output(GPIO_WATCHDOG_LED, GPIO.HIGH)  # Turn on
                watchdog_led_status = True

        if not GPIO.input(GPIO_SHUTDOWN_BTN_IN):
            start_shutdown_process()

        if log_count > 36000:  # One log line per hour...
            print(iso_timestamp_now() + " - still alive...")
            log_count = 0

        time.sleep(0.1)  # length of cycle


if __name__ == "__main__":
    main()
