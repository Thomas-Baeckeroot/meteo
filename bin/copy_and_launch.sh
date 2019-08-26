source /home/thomas/.basheditor/remote-debugging-v1.sh localhost 33333 #BASHEDITOR-TMP-REMOTE-DEBUGGING-END|Origin line:#!/usr/bin/env bash

# set -x
raspberry_ip_address=192.168.0.171
echo "Copying all files to Raspberry PI at ${raspberry_ip_address}..."
rsync -r /home/thomas/workspace/meteo pi@${raspberry_ip_address}:/home/pi
echo "Copy/rsync returned $?"
echo
echo "Copying web files to Raspberry PI at ${raspberry_ip_address}..."
rsync -r /home/thomas/workspace/meteo/src/main/py/home_web/ web@${raspberry_ip_address}:/home/web
echo "Copy/rsync returned $?"
echo
echo "Launching python..."
echo "--------------------------------------------------------------------------------"
# ssh -tt pi@${raspberry_ip_address} /home/pi/meteo/src/main/py/periodical_sensor_reading.py
# ssh -tt pi@${raspberry_ip_address} /home/pi/meteo/src/main/py/video_capture_on_motion.py
# ssh -tt pi@${raspberry_ip_address} /home/pi/meteo/src/main/py/watchdog_gpio.py
# ssh -tt pi@${raspberry_ip_address} /home/pi/meteo/src/main/py/server2.py
ssh -tt web@${raspberry_ip_address} /home/pi/meteo/src/main/py/server3.py
echo "--------------------------------------------------------------------------------"
echo "ssh/python returned $?"
