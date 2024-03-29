#!/usr/bin/env bash

# Used at early time for debugging - TODO Drop this file?
# set -x
raspberry_ip_address=192.168.0.174
echo "Copying all files to Raspberry PI at ${raspberry_ip_address}..."
rsync -r /home/thomas/workspace/meteo pi@${raspberry_ip_address}:/home/pi
echo "Copy/rsync returned $?"
echo
echo "Copying web files to Raspberry PI at ${raspberry_ip_address}..."
rsync -r /home/thomas/workspace/meteo/src/main/py/public_html/ web@${raspberry_ip_address}:/home/web
echo "Copy/rsync returned $?"
echo
echo "Launching python..."
echo "--------------------------------------------------------------------------------"
# ssh -tt pi@${raspberry_ip_address} /home/pi/meteo/src/main/py/periodical_sensor_reading.py
# ssh -tt pi@${raspberry_ip_address} /home/pi/meteo/src/main/py/video_capture_on_motion.py
# ssh -tt pi@${raspberry_ip_address} /home/pi/meteo/src/main/py/watchdog_gpio.py
# ssh -tt pi@${raspberry_ip_address} /home/pi/meteo/src/main/py/server2.py
#ssh -tt web@${raspberry_ip_address} /home/pi/meteo/src/main/py/server3.py
echo "--------------------------------------------------------------------------------"
echo "ssh/python returned $?"
