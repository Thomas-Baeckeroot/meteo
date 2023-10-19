#!/usr/bin/env bash

sleep 60
printf -- "\n\n$(date) - Starting meteo server from $0\n" >> /var/services/homes/web/server3.log

# Define the user and virtual environment
WEB_USER="web"
PY_VENV="/usr/local/share/susanoo-py-venv"

# Set environment variables
export PATH="${PY_VENV}/bin:$PATH"
export PYTHONUNBUFFERED=1  # To enforce Python3 to flush immediately the log to the file

cd /var/services/homes/web

# Start the Python web server as the "web" user using sudo
sudo -u "${WEB_USER}" python3 /var/services/homes/meteo/meteo/src/main/py/server3.py >> /var/services/homes/web/server3.log 2>&1 &

exit 0

