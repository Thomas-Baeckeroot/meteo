source /home/thomas/.basheditor/remote-debugging-v1.sh localhost 33333 #BASHEDITOR-TMP-REMOTE-DEBUGGING-END|Origin line:#!/usr/bin/env bash

# set -x
raspberry_ip_address=192.168.0.169
echo "Copying files to Raspberry PI at ${raspberry_ip_address}..."
rsync -r /home/thomas/workspace/meteo pi@${raspberry_ip_address}:/home/pi
echo "Copy/rsync returned $?"
echo
echo "Launching python..."
echo "--------------------------------------------------------------------------------"
ssh -tt pi@${raspberry_ip_address} /home/pi/meteo/src/main/py/test_remote_interp.py
# ssh -tt pi@${raspberry_ip_address} /home/pi/meteo/src/main/py/watchdog_gpio.py
echo "--------------------------------------------------------------------------------"
echo "ssh/python returned $?"
