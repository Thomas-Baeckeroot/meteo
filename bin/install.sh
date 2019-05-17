#!/usr/bin/env bash

sudo apt install -y postgresql libpq-dev python-psycopg2 && pip install psycopg2

# As detailed https://www.raspberrypi.org/documentation/usage/camera/raspicam/raspivid.md
# to get 'MP4Box' command:
sudo apt install -y gpac
