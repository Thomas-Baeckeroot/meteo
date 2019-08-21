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


mkdir ~/workspace/meteo/src/lib 
git clone https://github.com/adafruit/Adafruit_Python_BMP.git

echo "-"
echo "Add below line to crontab of user 'pi':"
echo "* * * * *  /home/pi/meteo/src/main/py/periodical_sensor_reading.py >> /var/log/meteo.log 2>&1"
echo "-"
echo "Add below 3 lines at the end of /etc/rc.local, before last 'exit 0':"
echo "/home/pi/meteo/src/main/py/watchdog_gpio.py >> /var/log/watchdog_gpio.log 2>&1 &"
echo "sudo su - pi -c \"/home/pi/meteo/src/main/py/video_capture_on_motion.py >> /home/pi/meteo/video.log 2>&1\" &"
echo "sudo su - web -c \"/home/pi/meteo/src/main/py/server3.py >> /home/web/server3.log\" &"
echo "-"
echo "With 'sudo raspi-config', you can configure to start without graphical GUI"
