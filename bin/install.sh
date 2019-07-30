#!/usr/bin/env bash

sudo apt install -y postgresql libpq-dev python-psycopg2 && pip install psycopg2

# For Python remote debugging
# (check https://raspberrypi.stackexchange.com/questions/70018/remotely-debug-python-code-on-pi-using-eclipse-in-windows for further details)
sudo pip install pydevd

# As detailed https://www.raspberrypi.org/documentation/usage/camera/raspicam/raspivid.md
# to get 'MP4Box' command:
sudo apt install -y gpac


# For tests with 'motion',
# it has been installed the 2019-06 version by:
sudo apt install libmicrohttpd12
# from https://github.com/Motion-Project/motion/releases
sudo dpkg -i pi_stretch_motion_4.2.2-1_armhf.deb

# For CPU temperature reading and other GPIO:
pip install gpiozero
# from gpiozero import CPUTemperature
#
#cpu = CPUTemperature()
#print(cpu.temperature)

# Create forlder where images will be saved:
mkdir /home/pi/meteo/captures/


# A tutorial? about how to use the pressure/humidity/light/temperature sensors with I2C/SPI:
# https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial/all

# https://pypi.org/project/tsl2561/
pip install RPi.GPIO  # Possibly not necessary
python -m pip install Adafruit_GPIO  # Don't know why it was not working without calling by 'python -m'
pip install tsl2561
